#!/usr/bin/env python3
"""
scripts/vifood54/captions/vlm_captions.py
=========================================
Caption ảnh chi tiết cho loss LMM image-level (Pha 5 / B5, OV-W) — thay caption template L2.

Caption này chỉ đi vào tokenizer Qwen2 của LMM (giữ dấu tiếng Việt), KHÔNG đi vào BERT,
nên không cần lint bỏ dấu; chỉ cần đúng sự thật (paper LLMDet, Table 7: ảo giác làm giảm APr).

1) generate  VLM (Gemma 4) viết caption có điều kiện theo box GT (tên, số lượng, vị trí), lọc tự động:
             bỏ câu suy đoán / hương vị, gắn cờ khi nhắc món không có box hoặc thiếu món GT.
             Chạy lại được giữa chừng (bỏ qua ảnh đã có).
       python scripts/vifood54/captions/vlm_captions.py generate --load-4bit
2) duyệt tay: scripts/vifood54/captions/review_captions.py  -> captions_reviewed.jsonl
3) attach    gắn caption vào conversations của jsonl train (OD + VG) -> *_lmm.jsonl
       python scripts/vifood54/captions/vlm_captions.py attach                    # B5
       python scripts/vifood54/captions/vlm_captions.py attach --ov               # OV-W (caption có tên novel)
       python scripts/vifood54/captions/vlm_captions.py attach --ov --strip-novel # OV ablation (bỏ câu có tên novel)

Tiếng Anh (pipeline EN, 09/11): đặt VIFOOD_LANG=en cho cả generate / review_captions.py / attach -> đọc và ghi trong
annotations_en/ (tên lớp EN, prompt EN, lọc câu suy đoán / hương vị EN). Gemma nên tải sẵn vào huggingface/:
       VIFOOD_LANG=en python scripts/vifood54/captions/vlm_captions.py generate --load-4bit \
           --model huggingface/gemma-4-12B-it
       VIFOOD_LANG=en python scripts/vifood54/captions/vlm_captions.py attach
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import sys
import time
from typing import Iterator, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
LANG = os.environ.get('VIFOOD_LANG', 'vi')
ANN = os.path.join(ROOT, 'grounding_data/vifood54/annotations' + ('_en' if LANG == 'en' else ''))
ANN_OV = os.path.join(ROOT, 'grounding_data/vifood54/annotations_ov')
RAW = os.path.join(ANN, 'vlm_captions.jsonl')
REVIEWED = os.path.join(ANN, 'captions_reviewed.jsonl')
sys.path.insert(0, HERE)
from layout import group_instances  # noqa: E402
from builder_en import location_en  # noqa: E402
from lint import TASTE_ALLOW, TASTE_ALLOW_EN, TASTE_WORDS, TASTE_WORDS_EN  # noqa: E402

PROMPT = """Đây là ảnh một bữa ăn Việt Nam. Các món đã được xác định chắc chắn trong ảnh (tên – số lượng – vị trí):
{items}

Hãy viết một đoạn mô tả chi tiết bằng tiếng Việt (5–8 câu, khoảng 80–150 từ) về những gì NHÌN THẤY trong ảnh:
- nhắc từng món ở trên bằng ĐÚNG tên đã cho, kèm dụng cụ đựng, màu sắc, hình dạng, thành phần lộ ra và vị trí tương đối giữa các món;
- có thể tả bối cảnh (mặt bàn, đũa, thìa, ly nước, khăn giấy, ánh sáng).
Không gọi tên món ăn nào khác ngoài danh sách. Không nói về hương vị, mùi, độ giòn mềm, cảm xúc, nguồn gốc.
Không suy đoán (không dùng "có lẽ", "dường như", "có thể là"). Chỉ trả về đoạn văn, không tiêu đề, không gạch đầu dòng."""

SPECULATIVE = ['có lẽ', 'dường như', 'có vẻ', 'có thể là', 'hình như', 'gợi ý', 'cho thấy', 'chắc là', 'tạo cảm giác']
TASTE = [w for w in TASTE_WORDS if w != 'vị'] + ['hương vị', 'đậm vị']  # 'vị' đơn lẻ trùng 'vị trí'
REVIEW_STATUSES = ('approved', 'edited', 'rejected')

PROMPT_EN = """This is a photo of a Vietnamese meal. These dishes are certainly in the image (name – count – position):
{items}

Write one detailed paragraph in English (5–8 sentences, about 80–150 words) describing what is VISIBLE in the image:
- mention every dish above using EXACTLY the given name, with its container, colors, shape, visible ingredients and its
  position relative to the other dishes;
- you may describe the setting (table surface, chopsticks, spoons, glasses, napkins, lighting).
Do not name any other dish. Do not mention taste, smell, texture (crispy, soft...), feelings or origin.
Do not speculate (no "probably", "seems", "might be"). Return only the paragraph, no title, no bullet points."""
SPECULATIVE_EN = ['probably', 'perhaps', 'possibly', 'likely', 'seems', 'seem', 'appears to', 'appear to', 'might',
                  'may be', 'could be', 'suggests', 'suggesting', 'presumably', 'it looks like']
TASTE_EN = [w for w in TASTE_WORDS_EN if w not in ('warm', 'cold', 'nice', 'beautiful')]  # 'warm lighting' hợp lệ
if LANG == 'en':
    PROMPT, SPECULATIVE, TASTE, TASTE_ALLOW = PROMPT_EN, SPECULATIVE_EN, TASTE_EN, TASTE_ALLOW_EN


def _word_re(words: list[str]) -> re.Pattern:
    alt = '|'.join(re.escape(w) for w in sorted(set(words), key=len, reverse=True))
    return re.compile(r'(?<!\w)(' + alt + r')(?!\w)', re.IGNORECASE)


def read_jsonl(path: str) -> Iterator[dict]:
    with open(path, encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def write_jsonl(path: str, rows: list[dict]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def load_taxonomy() -> list[dict]:
    with open(os.path.join(ANN, 'taxonomy.json'), encoding='utf-8') as f:
        return json.load(f)['classes']


class CaptionFilter:
    """Lọc câu + gắn cờ. Tên món khớp theo bề mặt có dấu (tên lớp + aliases), cụm dài trước:
    'bánh canh' không bị tính là 'canh'."""

    def __init__(self, classes: list[dict]):
        self.surface: dict[str, str] = {}
        for c in classes:
            # bản EN: aliases trong taxonomy vẫn là tên Việt -> chỉ khớp tên EN
            for s in [c['name']] + (c.get('aliases', []) if LANG == 'vi' else []):
                self.surface.setdefault(s.lower(), c['name'])
        self.dish_re = _word_re(list(self.surface))
        self.spec_re = _word_re(SPECULATIVE)
        self.taste_re = _word_re(TASTE)
        self.allow_re = _word_re(TASTE_ALLOW)

    def dishes_in(self, text: str) -> set[str]:
        return {self.surface[m.group(1).lower()] for m in self.dish_re.finditer(text)}

    @staticmethod
    def sentences(text: str) -> list[str]:
        text = re.sub(r'\s+', ' ', text.replace('*', '').replace('#', '')).strip()
        return [s.strip() for s in re.split(r'(?<=[.!?])\s+', text) if s.strip()]

    def clean(self, raw: str, gt_names: set[str]) -> tuple[str, list[str]]:
        kept, issues = [], []
        for s in self.sentences(raw):
            if self.spec_re.search(s):
                issues.append(f'bỏ câu suy đoán: {s[:60]}')
                continue
            if self.taste_re.search(self.allow_re.sub(' ', s)):
                issues.append(f'bỏ câu hương vị: {s[:60]}')
                continue
            kept.append(s)
        caption = ' '.join(kept)
        extra = self.dishes_in(caption) - gt_names
        missing = gt_names - self.dishes_in(caption)
        if extra:
            issues.append('FLAG nhắc món không có box: ' + ', '.join(sorted(extra)))
        if missing:
            issues.append('FLAG thiếu món GT: ' + ', '.join(sorted(missing)))
        if len(caption.split()) < (40 if LANG == 'en' else 30):
            issues.append('FLAG caption quá ngắn')
        return caption, issues


def describe_items(row: dict, names: list[str]) -> str:
    groups = group_instances(row['detection']['instances'], names, row['width'], row['height'])
    if LANG == 'en':
        return '\n'.join(f'- {g.name} – {g.n} – {location_en(g)[0]}' for g in groups)
    return '\n'.join(f'- {g.name} – {g.n} – {g.location()[0]}' for g in groups)


# ───────────────────────────── generate ─────────────────────────────

def cmd_generate(args: argparse.Namespace) -> None:
    import torch
    from PIL import Image, ImageOps
    from transformers import AutoModelForImageTextToText, AutoProcessor

    classes = load_taxonomy()
    names = [c['name'] for c in classes]
    filt = CaptionFilter(classes)
    done = {r['filename'] for r in read_jsonl(args.out)} if os.path.exists(args.out) else set()
    rows = [r for r in read_jsonl(args.ann) if r['detection']['instances'] and r['filename'] not in done]
    if args.limit:
        rows = rows[:args.limit]
    print(f'{len(done)} ảnh đã có, còn {len(rows)} ảnh')

    quant = None
    if args.load_4bit:
        from transformers import BitsAndBytesConfig
        quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4', bnb_4bit_compute_dtype=torch.bfloat16)
    proc = AutoProcessor.from_pretrained(args.model)
    model = AutoModelForImageTextToText.from_pretrained(args.model, dtype=torch.bfloat16, device_map='cuda',
                                                        quantization_config=quant).eval()
    t0 = time.time()
    with open(args.out, 'a', encoding='utf-8') as fout:
        for k, row in enumerate(rows, 1):
            img = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, row['filename']))).convert('RGB')
            msgs = [{'role': 'user', 'content': [
                {'type': 'image', 'image': img},
                {'type': 'text', 'text': PROMPT.format(items=describe_items(row, names))}]}]
            inputs = proc.apply_chat_template(msgs, add_generation_prompt=True, tokenize=True, return_dict=True,
                                              return_tensors='pt').to(model.device, dtype=torch.bfloat16)
            with torch.no_grad():
                gen = model.generate(**inputs, max_new_tokens=args.max_new_tokens, do_sample=False)
            raw = proc.decode(gen[0, inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()
            gt = {names[i['label']] for i in row['detection']['instances']}
            caption, issues = filt.clean(raw, gt)
            status = 'flagged' if any(i.startswith('FLAG') for i in issues) else 'auto'
            fout.write(json.dumps({'filename': row['filename'], 'gt': sorted(gt), 'raw': raw, 'caption': caption,
                                   'status': status, 'issues': issues, 'model': args.model},
                                  ensure_ascii=False) + '\n')
            fout.flush()
            if k % 20 == 0:
                print(f'{k}/{len(rows)} · {(time.time() - t0) / k:.1f}s/ảnh')


# ───────────────────────────── attach ─────────────────────────────

def final_captions(accept: set[str]) -> tuple[dict[str, str], collections.Counter]:
    """filename -> caption dùng được: bản duyệt tay (dòng sau ghi đè dòng trước) ưu tiên hơn bản VLM tự lọc."""
    caps: dict[str, str] = {}
    status: dict[str, str] = {}
    if not os.path.exists(RAW):  # chưa sinh caption VLM: mọi ảnh dùng caption template L2
        return caps, collections.Counter()
    for r in read_jsonl(RAW):
        caps[r['filename']], status[r['filename']] = r['caption'], r['status']
    if os.path.exists(REVIEWED):
        for r in read_jsonl(REVIEWED):
            status[r['filename']] = r['status']
            if r['status'] in ('approved', 'edited'):
                caps[r['filename']] = r['caption']
    stat = collections.Counter(status.values())
    return {f: c for f, c in caps.items() if status[f] in accept and c}, stat


def strip_sentences(text: str, pattern: re.Pattern) -> str:
    return ' '.join(s for s in CaptionFilter.sentences(text) if not pattern.search(s))


def cmd_attach(args: argparse.Namespace) -> None:
    accept = set(args.accept.split(','))
    if args.ov and LANG == 'en':
        raise SystemExit('chưa có bộ OV tiếng Anh (annotations_ov/ là tiếng Việt)')
    caps, stat = final_captions(accept)
    print('trạng thái caption VLM:', dict(stat), '→ dùng', len(caps), 'ảnh (accept =', sorted(accept), ')')
    ann_dir = ANN_OV if args.ov else ANN
    novel_re: Optional[re.Pattern] = None
    if args.strip_novel:
        classes = load_taxonomy()
        novel = [s for c in classes if c['ov_split'] == 'novel' for s in [c['name']] + c.get('aliases', [])]
        novel_re = _word_re(novel)
    suffix = '_lmm_nonovel' if args.strip_novel else '_lmm'

    vg_rows = list(read_jsonl(os.path.join(ann_dir, 'train_vg_cap_rfs.jsonl')))
    template = {r['filename']: r['conversations'][1]['value'] for r in vg_rows}  # caption L2 làm dự phòng
    for name, rows in (('train_od_rfs', list(read_jsonl(os.path.join(ann_dir, 'train_od_rfs.jsonl')))),
                       ('train_vg_cap_rfs', vg_rows)):
        src = collections.Counter()
        out = []
        for r in rows:
            f = r['filename']
            if f in caps:
                text, src['vlm'] = caps[f], src['vlm'] + 1
            elif f in template:
                text, src['template_L2'] = template[f], src['template_L2'] + 1
            else:
                text, src['tên món'] = r['conversations'][1]['value'], src['tên món'] + 1
            if novel_re is not None:
                text = strip_sentences(text, novel_re)
            out.append(dict(r, conversations=[r['conversations'][0], {'from': 'gpt', 'value': text}]))
        path = os.path.join(ann_dir, f'{name}{suffix}.jsonl')
        write_jsonl(path, out)
        print(f'{os.path.relpath(path, ROOT)}: {len(out)} dòng, nguồn caption {dict(src)}')


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    g = sub.add_parser('generate')
    g.add_argument('--model', default='google/gemma-4-12B-it')
    g.add_argument('--ann', default=os.path.join(ANN, 'train_od.jsonl'), help='mỗi ảnh một dòng, đủ 54 lớp GT')
    g.add_argument('--out', default=RAW)
    g.add_argument('--load-4bit', action='store_true')
    g.add_argument('--max-new-tokens', type=int, default=400)
    g.add_argument('--limit', type=int, default=0, help='chỉ chạy N ảnh (thử)')
    a = sub.add_parser('attach')
    a.add_argument('--ov', action='store_true', help='ghi vào annotations_ov/ (OV-W)')
    a.add_argument('--strip-novel', action='store_true', help='bỏ câu có tên lớp novel (ablation OV)')
    a.add_argument('--accept', default='approved,edited,auto',
                   help='trạng thái được dùng; còn lại (flagged, rejected) dùng caption template L2')
    args = p.parse_args()
    {'generate': cmd_generate, 'attach': cmd_attach}[args.cmd](args)


if __name__ == '__main__':
    main()
