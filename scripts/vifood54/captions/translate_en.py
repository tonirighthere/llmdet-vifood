#!/usr/bin/env python3
"""
Dịch sang tiếng Anh (Gemma 4 local, chỉ văn bản — không gửi ảnh/văn bản ra ngoài) các cụm mô tả hình thái
dùng trong caption: `definition` + `attrs` của taxonomy (theo từng lớp, có ngữ cảnh tên món) và các đặc điểm VLM
thêm (`extra` trong vlm_attrs/*.jsonl). Thuộc tính VLM giữ lại (`visible`) đúng là chuỗi taxonomy nên không cần dịch
riêng. Không chạy lại VLM trên ảnh.

    HF_HUB_OFFLINE=1 ~/miniconda/envs/gemma_env/bin/python -u scripts/vifood54/captions/translate_en.py --load-4bit

Ra grounding_data/vifood54/annotations_en/translations_vi_en.json: {"taxonomy": {tên VI: {"definition", "attrs"}},
"phrases": {cụm VI: cụm EN}}. Ghi sau mỗi lô, chạy lại thì bỏ qua phần đã dịch.
"""
import argparse
import glob
import json
import os
import re
import sys
import time

import torch
from transformers import AutoModelForImageTextToText, AutoProcessor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from en_names import PROMPT_EN  # noqa: E402

RULES = """Rules:
- Each output is a short, natural English phrase (lowercase, at most 10 words), faithful to the Vietnamese.
- Describe only what is visible: colors, shapes, cutting, arrangement, toppings, ingredients.
- Do not add taste, smell or texture words (delicious, fragrant, spicy, crispy, soft, chewy, tender, rich).
- "ruốc" is "floss" (do not say shrimp or pork unless the Vietnamese does); "giò" is "pork roll" except
  "giò heo" = "pork knuckle"; "hành phi" = "fried shallots"; "mỡ hành" = "scallion oil"; "lạc" = "peanuts";
  "lá dong" = "dong leaves"; "lạt" = "bamboo strings"; "bánh đa" = "rice crackers"; "dồi" = "blood sausage".
- Keep "hoặc" as "or"."""

TAX_PROMPT = """You translate visual descriptions of a Vietnamese dish for an image-captioning dataset.
Dish: {vi} ({en}).
{rules}

Translate this JSON object. Return only JSON with the same keys: "definition" (one English sentence, no dish name)
and "attrs" (a list with exactly {n} English phrases, same order).
{payload}"""

PHRASE_PROMPT = """You translate short Vietnamese phrases that describe what is visible in a crop of a food photo,
for an image-captioning dataset.
{rules}

Translate each of the {n} phrases below. Return only a JSON list of exactly {n} English strings, same order.
{payload}"""


def parse_json(text):
    m = re.search(r'(\{.*\}|\[.*\])', text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def clean(s):
    return re.sub(r'\s+', ' ', str(s)).strip().strip('."').lower()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--model', default='google/gemma-4-12B-it')
    p.add_argument('--load-4bit', action='store_true')
    p.add_argument('--batch', type=int, default=40)
    p.add_argument('--taxonomy', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations/taxonomy.json'))
    p.add_argument('--vlm-dir', default=os.path.join(ROOT, 'grounding_data/vifood54/vlm_attrs'))
    p.add_argument('--out', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations_en/translations_vi_en.json'))
    p.add_argument('--limit', type=int, default=0, help='chỉ dịch N lô cụm VLM (thử)')
    p.add_argument('--skip-taxonomy', action='store_true',
                   help='bỏ dịch definition/attrs taxonomy (đã dịch tay trong en_names.VISUAL_EN), chỉ dịch cụm VLM')
    args = p.parse_args()

    tax = json.load(open(args.taxonomy, encoding='utf-8'))['classes']
    extras = set()
    for f in sorted(glob.glob(os.path.join(args.vlm_dir, 'train_*.jsonl'))):
        for line in open(f, encoding='utf-8'):
            for v in json.loads(line)['classes'].values():
                extras.update(v.get('extra') or [])
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    out = json.load(open(args.out, encoding='utf-8')) if os.path.exists(args.out) else {'taxonomy': {}, 'phrases': {}}

    def save():
        tmp = args.out + '.tmp'
        json.dump(out, open(tmp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        os.replace(tmp, args.out)

    proc = AutoProcessor.from_pretrained(args.model)
    quant = None
    if args.load_4bit:
        from transformers import BitsAndBytesConfig
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_compute_dtype=torch.bfloat16)
    model = AutoModelForImageTextToText.from_pretrained(args.model, dtype=torch.bfloat16, device_map='cuda',
                                                        quantization_config=quant)
    model.eval()

    def ask(text, max_new):
        msgs = [{'role': 'user', 'content': [{'type': 'text', 'text': text}]}]
        inputs = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                          return_tensors='pt').to(model.device)
        with torch.no_grad():
            gen = model.generate(**inputs, max_new_tokens=max_new, do_sample=False)
        return proc.decode(gen[0, inputs['input_ids'].shape[1]:], skip_special_tokens=True)

    t0 = time.time()
    for c in ([] if args.skip_taxonomy else tax):
        v = c['visual']
        if c['name'] in out['taxonomy'] or (not v['attrs'] and not v['definition']):
            continue
        payload = json.dumps({'definition': v['definition'], 'attrs': v['attrs']}, ensure_ascii=False)
        for _ in range(3):
            js = parse_json(ask(TAX_PROMPT.format(vi=c['name'], en=PROMPT_EN[c['name']], rules=RULES,
                                                  n=len(v['attrs']), payload=payload), 600))
            if isinstance(js, dict) and isinstance(js.get('attrs'), list) and len(js['attrs']) == len(v['attrs']):
                out['taxonomy'][c['name']] = {'definition': str(js.get('definition', '')).strip(),
                                              'attrs': [clean(a) for a in js['attrs']]}
                break
        else:
            print(f'[translate] lỗi lớp {c["name"]}', flush=True)
        save()
    print(f'[translate] taxonomy {len(out["taxonomy"])} lớp, {time.time() - t0:.0f}s', flush=True)

    todo = sorted(e for e in extras if e not in out['phrases'])
    print(f'[translate] cụm VLM: {len(extras)}, còn {len(todo)}', flush=True)
    batches = [todo[i:i + args.batch] for i in range(0, len(todo), args.batch)]
    if args.limit:
        batches = batches[:args.limit]

    def run(batch):
        payload = json.dumps(batch, ensure_ascii=False)
        js = parse_json(ask(PHRASE_PROMPT.format(rules=RULES, n=len(batch), payload=payload), 25 * len(batch) + 50))
        if isinstance(js, list) and len(js) == len(batch):
            for vi, en in zip(batch, js):
                out['phrases'][vi] = clean(en)
            return True
        if len(batch) == 1:
            print(f'[translate] bỏ cụm không dịch được: {batch[0]!r}', flush=True)
            return False
        h = len(batch) // 2  # lệch số phần tử -> chia đôi lô
        return run(batch[:h]) & run(batch[h:])

    t1 = time.time()
    for k, b in enumerate(batches):
        run(b)
        save()
        if (k + 1) % 5 == 0 or k + 1 == len(batches):
            per = (time.time() - t1) / (k + 1)
            print(f'[translate] lô {k + 1}/{len(batches)} · {per:.0f}s/lô · còn ~{per * (len(batches) - k - 1) / 60:.0f} phút',
                  flush=True)
    print(f'[translate] xong: {len(out["phrases"])} cụm -> {args.out}', flush=True)


if __name__ == '__main__':
    main()
