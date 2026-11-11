#!/usr/bin/env python3
"""
Chạy VLM (Gemma 4, local) trên cả tập để lấy thuộc tính NHÌN THẤY của từng lớp trong từng ảnh (như vlm_pilot.py),
ghi ra jsonl để builder ghép lại caption. Chia shard để chạy nhiều đêm, chạy tiếp được khi bị dừng.

Mỗi ảnh, mỗi lớp có thuộc tính trong taxonomy: cắt box lớn nhất, hỏi VLM thuộc tính ứng viên nào nhìn thấy,
tối đa 2 đặc điểm thêm (phải qua lint: không tên lớp khác, không hương vị), dụng cụ đựng, có đúng món không.

    ~/miniconda/envs/gemma_env/bin/python scripts/vifood54/captions/vlm_attrs.py --shard 0 --num-shards 2 \
        --model google/gemma-4-12B-it --load-4bit

Một dòng / ảnh: {"filename", "model", "classes": {tên lớp: {"visible": [...], "extra": [...],
"extra_rejected": [...], "container", "match", "box", "sec"} | {"error": "..."}}}
Shard theo thứ tự filename đã sắp (ảnh thứ i thuộc shard i % num_shards) để mỗi nửa trải đều các nguồn ảnh.
"""
import argparse
import json
import os
import sys
import time

import torch
from PIL import Image, ImageOps
from transformers import AutoModelForImageTextToText, AutoProcessor, AutoTokenizer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from lint import CaptionLinter  # noqa: E402
from vlm_pilot import PROMPT, crop, parse_json  # noqa: E402


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--model', default='google/gemma-4-12B-it')
    p.add_argument('--load-4bit', action='store_true')
    p.add_argument('--split', default='train')
    p.add_argument('--shard', type=int, default=0)
    p.add_argument('--num-shards', type=int, default=2)
    p.add_argument('--limit', type=int, default=0, help='chỉ chạy N ảnh đầu của shard (thử)')
    p.add_argument('--taxonomy', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations/taxonomy.json'))
    p.add_argument('--out-dir', default=os.path.join(ROOT, 'grounding_data/vifood54/vlm_attrs'))
    return p.parse_args()


def main():
    args = parse_args()
    tax = {c['name']: c for c in json.load(open(args.taxonomy, encoding='utf-8'))['classes']}
    names = list(tax)
    linter = CaptionLinter(AutoTokenizer.from_pretrained(os.path.join(ROOT, 'huggingface/bert-base-uncased')), names)

    ann = os.path.join(ROOT, f'grounding_data/vifood54/annotations/{args.split}_vg_cap.jsonl')
    rows = sorted((json.loads(l) for l in open(ann, encoding='utf-8')), key=lambda r: r['filename'])
    rows = [r for i, r in enumerate(rows) if i % args.num_shards == args.shard]
    if args.limit:
        rows = rows[:args.limit]

    os.makedirs(args.out_dir, exist_ok=True)
    tag = args.model.split('/')[-1]
    out_path = os.path.join(args.out_dir, f'{args.split}_{tag}_shard{args.shard}of{args.num_shards}.jsonl')
    done = set()
    if os.path.exists(out_path):
        with open(out_path, encoding='utf-8') as f:
            for line in f:
                try:
                    done.add(json.loads(line)['filename'])
                except (json.JSONDecodeError, KeyError):
                    pass  # dòng cuối ghi dở khi bị dừng
    todo = [r for r in rows if r['filename'] not in done]
    n_crops = sum(len({i['label'] for i in r['detection']['instances'] if tax[names[i['label']]]['visual']['attrs']})
                  for r in todo)
    print(f'[vlm_attrs] {args.split} shard {args.shard}/{args.num_shards}: {len(rows)} ảnh, đã xong {len(done)}, '
          f'còn {len(todo)} ảnh / {n_crops} crop -> {out_path}', flush=True)

    proc = AutoProcessor.from_pretrained(args.model)
    quant = None
    if args.load_4bit:
        from transformers import BitsAndBytesConfig
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_compute_dtype=torch.bfloat16)
    model = AutoModelForImageTextToText.from_pretrained(args.model, dtype=torch.bfloat16, device_map='cuda',
                                                        quantization_config=quant)
    model.eval()

    t_start, n_done = time.time(), 0
    for k, r in enumerate(todo):
        with Image.open(os.path.join(ROOT, r['filename'])) as im:
            img = ImageOps.exif_transpose(im).convert('RGB')
        by_label = {}
        for inst in r['detection']['instances']:
            b = inst['bbox']
            a = (b[2] - b[0]) * (b[3] - b[1])
            if inst['label'] not in by_label or a > by_label[inst['label']][1]:
                by_label[inst['label']] = (b, a)
        classes = {}
        for label, (box, _) in by_label.items():
            c = tax[names[label]]
            attrs = c['visual']['attrs']
            if not attrs:
                continue  # lớp catch-all
            cand = '\n'.join(f'{i}. {a}' for i, a in enumerate(attrs))
            msgs = [{'role': 'user', 'content': [
                {'type': 'image', 'image': crop(img, box)},
                {'type': 'text', 'text': PROMPT.format(name=c['name'], definition=c['visual']['definition'],
                                                       candidates=cand)}]}]
            t0 = time.time()
            try:
                inputs = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                                  return_tensors='pt').to(model.device, dtype=torch.bfloat16)
                with torch.no_grad():
                    gen = model.generate(**inputs, max_new_tokens=160, do_sample=False)
                ans = proc.decode(gen[0, inputs['input_ids'].shape[1]:], skip_special_tokens=True)
            except Exception as e:  # một crop lỗi không làm dừng cả đêm
                classes[c['name']] = {'error': f'{type(e).__name__}: {str(e)[:200]}', 'box': box}
                torch.cuda.empty_cache()
                continue
            n_done += 1
            js = parse_json(ans)
            if js is None:
                classes[c['name']] = {'error': 'json', 'raw': ans[:300], 'box': box}
                continue
            vis = [attrs[i] for i in js.get('visible', []) if isinstance(i, int) and 0 <= i < len(attrs)]
            extra, rejected = [], []
            for e in (js.get('extra') or [])[:2]:
                e = str(e).strip().lower().rstrip('.')
                errs = linter.check(f'một đĩa {c["name"]}, {e}.', [(8, 8 + len(c['name']), c['name'])])
                (rejected if errs or not e else extra).append(e)
            classes[c['name']] = {'visible': vis, 'extra': extra, 'extra_rejected': rejected,
                                  'container': js.get('container'), 'match': js.get('match'),
                                  'box': box, 'sec': round(time.time() - t0, 2)}
        with open(out_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'filename': r['filename'], 'model': args.model, 'classes': classes},
                               ensure_ascii=False) + '\n')
        if (k + 1) % 20 == 0 or k + 1 == len(todo):
            el = time.time() - t_start
            per = el / max(n_done, 1)
            left = sum(len({i['label'] for i in x['detection']['instances'] if tax[names[i['label']]]['visual']['attrs']})
                       for x in todo[k + 1:])
            print(f'[vlm_attrs] {k + 1}/{len(todo)} ảnh · {n_done} crop · {per:.1f}s/crop · '
                  f'còn ~{left * per / 3600:.1f} h', flush=True)


if __name__ == '__main__':
    main()
