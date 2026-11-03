#!/usr/bin/env python3
"""
Thử VLM (Gemma 4, chạy local) để làm caption khớp ảnh hơn mà KHÔNG phá grounding.

Cách làm: VLM không viết lại cả caption (sẽ mất vị trí span, có thể thêm tên món không có box).
Với mỗi lớp trong ảnh, cắt box lớn nhất, hỏi VLM:
  - thuộc tính nào trong danh sách ứng viên của taxonomy NHÌN THẤY trong crop,
  - thêm tối đa 2 đặc điểm hình thái khác (màu, hình dạng, thành phần lộ ra),
  - dụng cụ đựng.
Kết quả thay `attrs` của lớp đó cho riêng ảnh này; builder vẫn ghép caption và ghi span như cũ,
và mọi cụm VLM đề xuất phải qua lint (không tên lớp khác, không hương vị).

    ~/miniconda/envs/gemma_env/bin/python scripts/vifood54/captions/vlm_pilot.py --n 6
"""
import argparse
import json
import os
import random
import re
import sys
import time

import torch
from PIL import Image, ImageOps
from transformers import AutoModelForImageTextToText, AutoProcessor, AutoTokenizer

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from lint import CaptionLinter  # noqa: E402

PROMPT = """Ảnh là một món ăn Việt Nam đã được gán nhãn là "{name}".
Định nghĩa hình ảnh của món này: {definition}.

Nhiệm vụ: chỉ mô tả những gì NHÌN THẤY trong ảnh (màu, hình dạng, thành phần lộ ra, cách bày, dụng cụ đựng).
Không nói về hương vị, mùi, độ giòn/mềm, cảm xúc. Không nhắc tên món ăn nào khác.

1. Trong các đặc điểm sau, đặc điểm nào thật sự nhìn thấy trong ảnh? Trả về số thứ tự:
{candidates}
2. Thêm tối đa 2 đặc điểm hình thái khác nhìn thấy rõ, mỗi cái 2–6 từ tiếng Việt, viết thường.
3. Món được đựng trong gì (một từ: tô, bát, đĩa, chén, mẹt, nồi, rổ, khay, lá, không rõ)?
4. Ảnh có đúng là "{name}" không (có / không / không chắc)?

Chỉ trả về JSON: {{"visible": [số], "extra": ["..."], "container": "...", "match": "..."}}"""


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--model', default='google/gemma-4-E4B-it')
    p.add_argument('--ann', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations/train_vg_cap.jsonl'))
    p.add_argument('--taxonomy', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations/taxonomy.json'))
    p.add_argument('--n', type=int, default=6, help='số ảnh thử')
    p.add_argument('--seed', type=int, default=7)
    p.add_argument('--load-4bit', action='store_true', help='nén 4-bit (bitsandbytes), cần cho bản 12B trên 24 GB')
    p.add_argument('--out', default=os.path.join(ROOT, 'grounding_data/vifood54/VLM_PILOT.md'))
    return p.parse_args()


def crop(img, box, margin=0.15):
    x1, y1, x2, y2 = box
    mw, mh = (x2 - x1) * margin, (y2 - y1) * margin
    return img.crop((max(0, x1 - mw), max(0, y1 - mh), min(img.width, x2 + mw), min(img.height, y2 + mh)))


def parse_json(text):
    m = re.search(r'\{.*\}', text, re.S)
    try:
        return json.loads(m.group()) if m else None
    except json.JSONDecodeError:
        return None


def main():
    args = parse_args()
    tax = {c['name']: c for c in json.load(open(args.taxonomy, encoding='utf-8'))['classes']}
    names = list(tax)
    linter = CaptionLinter(AutoTokenizer.from_pretrained(os.path.join(ROOT, 'huggingface/bert-base-uncased')), names)

    proc = AutoProcessor.from_pretrained(args.model)
    quant = None
    if args.load_4bit:
        from transformers import BitsAndBytesConfig
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_compute_dtype=torch.bfloat16)
    model = AutoModelForImageTextToText.from_pretrained(args.model, dtype=torch.bfloat16, device_map='cuda',
                                                        quantization_config=quant)
    model.eval()

    rows = [json.loads(l) for l in open(args.ann, encoding='utf-8')]
    rng = random.Random(args.seed)
    rows = [r for r in rows if 2 <= len({i['label'] for i in r['detection']['instances']}) <= 4]
    sample = rng.sample(rows, args.n)

    out = [f'# Thử VLM `{args.model}` sửa thuộc tính caption ({args.n} ảnh train)', '']
    t_all, n_calls = time.time(), 0
    for r in sample:
        img = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, r['filename']))).convert('RGB')
        out += [f'## `{os.path.basename(r["filename"])}`', '',
                f'- caption hiện tại: {r["grounding"]["caption"]}', '']
        by_label = {}
        for inst in r['detection']['instances']:
            b = inst['bbox']
            if inst['label'] not in by_label or (b[2] - b[0]) * (b[3] - b[1]) > by_label[inst['label']][1]:
                by_label[inst['label']] = (b, (b[2] - b[0]) * (b[3] - b[1]))
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
            inputs = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True,
                                              return_dict=True, return_tensors='pt').to(model.device, dtype=torch.bfloat16)
            t0 = time.time()
            with torch.no_grad():
                gen = model.generate(**inputs, max_new_tokens=160, do_sample=False)
            ans = proc.decode(gen[0, inputs['input_ids'].shape[1]:], skip_special_tokens=True)
            n_calls += 1
            js = parse_json(ans)
            if js is None:
                out.append(f'- **{c["name"]}**: không đọc được JSON: `{ans[:200]}`')
                continue
            vis = [attrs[i] for i in js.get('visible', []) if isinstance(i, int) and 0 <= i < len(attrs)]
            extras = []
            for e in js.get('extra', [])[:2]:
                e = str(e).strip().lower().rstrip('.')
                errs = linter.check(f'một đĩa {c["name"]}, {e}.', [(8, 8 + len(c['name']), c['name'])])
                extras.append((e, errs))
            out.append(f'- **{c["name"]}** ({time.time() - t0:.1f}s) · đựng: {js.get("container")} · đúng món: {js.get("match")}')
            out.append(f'  - nhìn thấy: {vis} · bị loại: {[a for a in attrs if a not in vis]}')
            out.append('  - VLM thêm: ' + '; '.join(f'{e} ✅' if not errs else f'{e} ❌ {errs[0]}' for e, errs in extras))
        out.append('')
    out.insert(1, f'- {n_calls} lần gọi, TB {(time.time() - t_all) / max(n_calls, 1):.1f}s/lần, '
                  f'VRAM đỉnh {torch.cuda.max_memory_allocated() / 2 ** 30:.1f} GB')
    open(args.out, 'w', encoding='utf-8').write('\n'.join(out) + '\n')
    print('\n'.join(out))


if __name__ == '__main__':
    main()
