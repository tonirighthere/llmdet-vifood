#!/usr/bin/env python3
"""
scripts/vifood54/captions/caption_v2.py
=======================================
Caption ảnh v2 cho loss LLM (B5b, OV-W): dài và riêng theo ảnh hơn bản template (~40 từ), ít ảo giác hơn bản VLM tự do.

Nguyên tắc (ánh xạ paper LLMDet, mục 3 + Table 7):
  - VLM KHÔNG đặt tên món, KHÔNG nói vị trí / số lượng: ba thứ này lấy từ nhãn (box GT).
  - VLM chỉ trả lời câu hỏi hẹp trên CROP từng món (dụng cụ, màu, thành phần lộ ra, cách bày) và trên ảnh gốc (bối cảnh).
  - Mỗi chi tiết phải qua lượt kiểm chứng có/không (nên dùng model KHÁC lượt mô tả) trước khi vào caption.
  - Caption train là tiếng Anh; bản tiếng Việt dịch TỪNG CÂU 1:1 chỉ để người duyệt đọc. Duyệt bản Việt = duyệt bản Anh.

Các bước (mỗi bước chạy lại được giữa chừng; 1, 2, 4 cần GPU, 3 chỉ CPU):
  1) describe   VLM mô tả từng món + bối cảnh           -> captions_v2/describe.jsonl
  2) verify     VLM (model khác) xác nhận từng chi tiết  -> captions_v2/verify.jsonl
  3) compose    ghép đoạn văn EN 80–120 từ, lọc, gắn cờ  -> captions_v2/composed.jsonl
  4) translate  dịch từng câu sang tiếng Việt            -> annotations_en/vlm_captions.jsonl
  rồi: VIFOOD_LANG=en review_captions.py  ->  VIFOOD_LANG=en vlm_captions.py attach --suffix _lmm_v2

    M1=llava-hf/llava-onevision-qwen2-7b-ov-hf; M2=huggingface/gemma-4-12B-it
    python scripts/vifood54/captions/caption_v2.py describe  --model $M1 --limit 50
    python scripts/vifood54/captions/caption_v2.py verify    --model $M2 --load-4bit
    python scripts/vifood54/captions/caption_v2.py compose
    python scripts/vifood54/captions/caption_v2.py translate --model $M2 --load-4bit
    python scripts/vifood54/captions/caption_v2.py stats     # số từ, tỉ lệ chi tiết bị loại, cờ
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import statistics
import sys
import time
from typing import Any, Iterator, Optional

os.environ['VIFOOD_LANG'] = 'en'  # caption v2 chỉ có bản tiếng Anh (annotations_en/)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from builder_en import COUNT_WORDS, SIZE_EN, _article, _cap, location_en  # noqa: E402
from en_names import CONTAINER_EN  # noqa: E402
from layout import group_instances  # noqa: E402
from vlm_captions import ANN, RAW, CaptionFilter, load_taxonomy, read_jsonl  # noqa: E402

OUT_DIR = os.path.join(ROOT, 'grounding_data/vifood54/captions_v2')
DESCRIBE, VERIFY, COMPOSED = (os.path.join(OUT_DIR, f) for f in ('describe.jsonl', 'verify.jsonl', 'composed.jsonl'))
CONTAINERS = sorted({u[0] for u in CONTAINER_EN.values()} | {'banana leaf'})  # plate, bowl, small bowl, basket...
MAX_PHRASE_WORDS = 8

DISH_PROMPT = """This crop shows a Vietnamese dish labeled "{name}" ({definition}).
List only what is clearly VISIBLE in this crop. Use short lowercase English phrases of 2-6 words.
Do not name any dish. Do not mention taste, smell or texture. Do not guess.
Return JSON only:
{{"container": "one of: {containers}, none, unclear",
  "colors": ["up to 3 phrases: a color plus the part it belongs to, e.g. 'clear brown broth'"],
  "components": ["up to 5 visible ingredients or parts, e.g. 'sliced green onions', 'halved boiled egg'"],
  "arrangement": "one phrase starting with a past participle, e.g. 'cut into thick slices', or ''"}}"""

SCENE_PROMPT = """This photo shows a Vietnamese meal. Ignore the food itself and describe only the setting that is clearly visible.
Use short lowercase English phrases of 2-6 words. Do not name any dish. Do not guess.
Return JSON only:
{{"surface": "what the dishes stand on, e.g. 'dark wooden table', or ''",
  "utensils": ["up to 3, e.g. 'wooden chopsticks', 'metal spoon'"],
  "other_objects": ["up to 4 non-food objects, e.g. 'glass of water', 'paper napkins'"],
  "background": "one phrase, e.g. 'blurred restaurant interior', or ''"}}"""

VERIFY_PROMPT = """Look at the image. For each numbered phrase answer "yes" only if it is clearly visible in the image, otherwise "no".
{items}
Return JSON only, e.g. {{"1": "yes", "2": "no"}}"""

TRANSLATE_PROMPT = """Translate each numbered English sentence into natural Vietnamese. Translate faithfully, add nothing.
Keep every placeholder like [[3]] exactly as it is. Return a JSON list of {n} strings in the same order, nothing else.
{items}"""


# ───────────────────────────── tiện ích ─────────────────────────────

def append_jsonl(path: str, row: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(row, ensure_ascii=False) + '\n')


def done_files(path: str) -> set[str]:
    return {r['filename'] for r in read_jsonl(path)} if os.path.exists(path) else set()


def parse_json(text: str) -> Optional[Any]:
    m = re.search(r'[\[{].*[\]}]', text, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group())
    except json.JSONDecodeError:
        return None


def crop_box(img, box: list[float], margin: float = 0.15):
    x1, y1, x2, y2 = box
    mw, mh = (x2 - x1) * margin, (y2 - y1) * margin
    return img.crop((max(0, x1 - mw), max(0, y1 - mh), min(img.width, x2 + mw), min(img.height, y2 + mh)))


def largest_boxes(row: dict) -> dict[int, list[float]]:
    """class id -> box lớn nhất của lớp đó trong ảnh (crop đại diện, như vlm_attrs.py)."""
    best: dict[int, tuple[float, list[float]]] = {}
    for inst in row['detection']['instances']:
        b = inst['bbox']
        area = (b[2] - b[0]) * (b[3] - b[1])
        if inst['label'] not in best or area > best[inst['label']][0]:
            best[inst['label']] = (area, b)
    return {k: v[1] for k, v in best.items()}


class PhraseCleaner:
    """Chuẩn hóa + loại cụm VLM trả về: quá dài, có tên món, từ hương vị, từ suy đoán."""

    def __init__(self, classes: list[dict]):
        self.filt = CaptionFilter(classes)

    def clean(self, phrase: Any) -> Optional[str]:
        if not isinstance(phrase, str):
            return None
        p = re.sub(r'\s+', ' ', phrase.strip().lower().strip('.,;:!"\''))
        if not p or p in ('none', 'unclear', 'n/a') or not re.fullmatch(r"[a-z][a-z0-9 ,'\-]*", p):
            return None
        if len(p.split()) > MAX_PHRASE_WORDS or self.filt.dishes_in(p):
            return None
        if self.filt.spec_re.search(p) or self.filt.taste_re.search(self.filt.allow_re.sub(' ', p)):
            return None
        return p

    def clean_list(self, items: Any, k: int) -> list[str]:
        out: list[str] = []
        for x in items if isinstance(items, list) else []:
            c = self.clean(x)
            if c and c not in out:
                out.append(c)
        return out[:k]


class VLM:
    """Model ảnh-văn bản của HF (LLaVA-OneVision-hf, Gemma...) qua chat template; ask() trả chuỗi sinh ra."""

    def __init__(self, model: str, load_4bit: bool):
        import torch
        from transformers import AutoModelForImageTextToText, AutoProcessor
        quant = None
        if load_4bit:
            from transformers import BitsAndBytesConfig
            quant = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type='nf4',
                                       bnb_4bit_compute_dtype=torch.bfloat16)
        self.torch = torch
        self.name = model
        self.proc = AutoProcessor.from_pretrained(model)
        self.model = AutoModelForImageTextToText.from_pretrained(
            model, dtype=torch.bfloat16, device_map='cuda', quantization_config=quant).eval()

    def ask(self, images: list, text: str, max_new_tokens: int = 200) -> str:
        content = [{'type': 'image', 'image': im} for im in images] + [{'type': 'text', 'text': text}]
        inputs = self.proc.apply_chat_template(
            [{'role': 'user', 'content': content}], add_generation_prompt=True, tokenize=True, return_dict=True,
            return_tensors='pt').to(self.model.device, dtype=self.torch.bfloat16)
        with self.torch.no_grad():
            gen = self.model.generate(**inputs, max_new_tokens=max_new_tokens, do_sample=False)
        return self.proc.decode(gen[0, inputs['input_ids'].shape[1]:], skip_special_tokens=True).strip()


def load_rows(args: argparse.Namespace, done: set[str]) -> list[dict]:
    rows = [r for r in read_jsonl(args.ann) if r['detection']['instances'] and r['filename'] not in done]
    return rows[:args.limit] if args.limit else rows


def open_image(filename: str):
    from PIL import Image, ImageOps
    return ImageOps.exif_transpose(Image.open(os.path.join(ROOT, filename))).convert('RGB')


# ───────────────────────────── 1) describe ─────────────────────────────

def cmd_describe(args: argparse.Namespace) -> None:
    classes = load_taxonomy()
    cleaner = PhraseCleaner(classes)
    rows = load_rows(args, done_files(DESCRIBE))
    print(f'describe: còn {len(rows)} ảnh')
    vlm = VLM(args.model, args.load_4bit)
    t0 = time.time()
    for k, row in enumerate(rows, 1):
        img = open_image(row['filename'])
        dishes: dict[str, dict] = {}
        for label, box in largest_boxes(row).items():
            c = classes[label]
            if not c['visual']['attrs']:  # lớp gom (other dish, dessert): không có hình thái chung -> không hỏi
                continue
            ans = parse_json(vlm.ask([crop_box(img, box)], DISH_PROMPT.format(
                name=c['name'], definition=c['visual']['definition'], containers=', '.join(CONTAINERS))))
            if not isinstance(ans, dict):
                dishes[str(label)] = {'error': 'json'}
                continue
            cont = str(ans.get('container', '')).strip().lower()
            dishes[str(label)] = {
                'container': cont if cont in CONTAINERS else '',
                'colors': cleaner.clean_list(ans.get('colors'), 3),
                'components': cleaner.clean_list(ans.get('components'), 5),
                'arrangement': cleaner.clean(ans.get('arrangement')) or '',
                'box': box,
            }
        sc = parse_json(vlm.ask([img], SCENE_PROMPT))
        scene = {'error': 'json'} if not isinstance(sc, dict) else {
            'surface': cleaner.clean(sc.get('surface')) or '',
            'utensils': cleaner.clean_list(sc.get('utensils'), 3),
            'other_objects': cleaner.clean_list(sc.get('other_objects'), 4),
            'background': cleaner.clean(sc.get('background')) or '',
        }
        append_jsonl(DESCRIBE, {'filename': row['filename'], 'model': vlm.name, 'dishes': dishes, 'scene': scene})
        if k % 20 == 0:
            print(f'{k}/{len(rows)} · {(time.time() - t0) / k:.1f}s/ảnh', flush=True)


# ───────────────────────────── 2) verify ─────────────────────────────

def phrases_of(d: dict, keys: tuple[str, ...]) -> list[str]:
    out: list[str] = []
    for key in keys:
        v = d.get(key)
        out += v if isinstance(v, list) else ([v] if v else [])
    return out


DISH_KEYS, SCENE_KEYS = ('colors', 'components', 'arrangement'), ('surface', 'utensils', 'other_objects', 'background')


def ask_yes_no(vlm: VLM, image, phrases: list[str]) -> dict[str, bool]:
    if not phrases:
        return {}
    items = '\n'.join(f'{i}. {p}' for i, p in enumerate(phrases, 1))
    ans = parse_json(vlm.ask([image], VERIFY_PROMPT.format(items=items), max_new_tokens=16 * len(phrases) + 16))
    if not isinstance(ans, dict):
        return {p: False for p in phrases}  # không đọc được -> coi như chưa xác nhận
    return {p: str(ans.get(str(i), 'no')).strip().lower().startswith('y') for i, p in enumerate(phrases, 1)}


def cmd_verify(args: argparse.Namespace) -> None:
    done = done_files(VERIFY)
    rows = [r for r in read_jsonl(DESCRIBE) if r['filename'] not in done]
    if args.limit:
        rows = rows[:args.limit]
    print(f'verify: còn {len(rows)} ảnh')
    vlm = VLM(args.model, args.load_4bit)
    t0 = time.time()
    for k, row in enumerate(rows, 1):
        img = open_image(row['filename'])
        ok: dict[str, dict[str, bool]] = {}
        for label, d in row['dishes'].items():
            if 'error' not in d:
                ok[label] = ask_yes_no(vlm, crop_box(img, d['box']), phrases_of(d, DISH_KEYS))
        scene_ok = {} if 'error' in row['scene'] else ask_yes_no(vlm, img, phrases_of(row['scene'], SCENE_KEYS))
        append_jsonl(VERIFY, {'filename': row['filename'], 'model': vlm.name, 'dishes': ok, 'scene': scene_ok})
        if k % 20 == 0:
            print(f'{k}/{len(rows)} · {(time.time() - t0) / k:.1f}s/ảnh', flush=True)


# ───────────────────────────── 3) compose ─────────────────────────────

def join_and(xs: list[str]) -> str:
    return xs[0] if len(xs) == 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


def relation(a, b) -> Optional[str]:
    """Quan hệ vị trí của 2 nhóm lớp theo tâm box lớn nhất (mặt phẳng ảnh); None nếu quá gần nhau."""
    (ax, ay), (bx, by) = a.center, b.center
    dx, dy = ax - bx, ay - by
    if max(abs(dx), abs(dy)) < 0.12:
        return None
    if abs(dx) >= abs(dy):
        return 'to the left of' if dx < 0 else 'to the right of'
    return 'above' if dy < 0 else 'below'


def compose_row(row: dict, desc: dict, ver: Optional[dict], classes: list[dict], filt: CaptionFilter,
                max_words: int) -> dict:
    names = [c['name'] for c in classes]
    groups = group_instances(row['detection']['instances'], names, row['width'], row['height'])
    for g in groups:  # tâm (0..1) của box lớn nhất
        b = max(g.boxes, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))
        g.center = ((b[0] + b[2]) / 2 / row['width'], (b[1] + b[3]) / 2 / row['height'])
    issues: list[str] = []
    n_claim = n_kept = 0

    def confirmed(label: Optional[str], phrases: list[str]) -> list[str]:
        nonlocal n_claim, n_kept
        n_claim += len(phrases)
        if ver is None:
            kept = phrases
        else:
            table = ver['scene'] if label is None else ver['dishes'].get(label, {})
            kept = [p for p in phrases if table.get(p)]
        n_kept += len(kept)
        return kept

    per_dish = 5 if len(groups) <= 3 else 3  # ảnh nhiều món: bớt chi tiết mỗi món để không quá dài
    sentences: list[str] = []
    for g in groups:
        c = classes[g.label]
        d = desc['dishes'].get(str(g.label), {})
        if 'error' in d:
            issues.append(f'FLAG VLM lỗi JSON: {g.name}')
            d = {}
        units = c['visual']['units'] if g.n == 1 else c['visual'].get('multi_units') or c['visual']['units']
        sing, plur = units[0]
        cont = d.get('container', '')
        if g.n == 1 and cont in CONTAINERS and cont != 'banana leaf':
            sing = cont
        size = SIZE_EN[g.size()] if 'small' not in sing and c['visual']['attrs'] else ''
        head = f'{size} {sing}'.strip()
        np_ = f'{_article(head)} {head} of {g.name}' if g.n == 1 else f'{COUNT_WORDS.get(g.n, "several")} {plur} of {g.name}'
        loc, _ = location_en(g)
        verb = 'is' if g.n == 1 else 'are'
        sentences.append(f'{_cap(loc)} there {verb} {np_}.')
        details = confirmed(str(g.label), d.get('colors', []) + d.get('components', []))[:per_dish]
        arr = confirmed(str(g.label), [d['arrangement']] if d.get('arrangement') else [])
        pron = 'It' if g.n == 1 else 'They'
        if details:
            sentences.append(f'{pron} {"shows" if g.n == 1 else "show"} {join_and(details)}.')
        if arr:
            sentences.append(f'{pron} {verb} {arr[0]}.')
    for a, b in zip(groups, groups[1:3]):  # tối đa 2 quan hệ giữa các món lớn nhất
        rel = relation(a, b)
        if rel:
            sentences.append(f'The {a.name} {"is" if a.n == 1 else "are"} {rel} the {b.name}.')
    sc = desc['scene'] if 'error' not in desc['scene'] else {}
    surface = confirmed(None, [sc['surface']] if sc.get('surface') else [])
    if surface:
        sentences.append(f'The dishes are set on {_article(surface[0])} {surface[0]}.')
    objs = confirmed(None, sc.get('utensils', []) + sc.get('other_objects', []))
    if objs:
        sentences.append(f'Also visible: {join_and(objs)}.')
    bg = confirmed(None, [sc['background']] if sc.get('background') else [])
    if bg:
        sentences.append(f'The background shows {_article(bg[0])} {bg[0]}.')

    while len(' '.join(sentences).split()) > max_words and len(sentences) > len(groups):
        sentences.pop()  # bỏ từ cuối (bối cảnh trước), không bao giờ bỏ câu giới thiệu món
    caption = ' '.join(sentences)
    gt = {g.name for g in groups}
    if filt.dishes_in(caption) != gt:
        issues.append('FLAG tên món trong caption khác nhãn')
    n_words = len(caption.split())
    if n_words < 50:
        issues.append(f'FLAG caption ngắn ({n_words} từ)')
    if ver is not None and n_claim >= 4 and n_kept / n_claim < 0.5:
        issues.append(f'FLAG kiểm chứng loại {n_claim - n_kept}/{n_claim} chi tiết')
    return {'filename': row['filename'], 'gt': sorted(gt), 'sentences': sentences, 'caption': caption,
            'raw': json.dumps({'describe': desc, 'verify': ver}, ensure_ascii=False),
            'status': 'flagged' if any(i.startswith('FLAG') for i in issues) else 'auto', 'issues': issues,
            'model': desc.get('model', '') + (' + ' + ver['model'] if ver else ' (chưa kiểm chứng)'),
            'n_words': n_words, 'n_claim': n_claim, 'n_kept': n_kept}


def cmd_compose(args: argparse.Namespace) -> None:
    classes = load_taxonomy()
    filt = CaptionFilter(classes)
    desc = {r['filename']: r for r in read_jsonl(DESCRIBE)}
    ver = {r['filename']: r for r in read_jsonl(VERIFY)} if os.path.exists(VERIFY) else {}
    out = []
    for row in read_jsonl(args.ann):
        f = row['filename']
        if f not in desc or (f not in ver and not args.allow_unverified):
            continue
        out.append(compose_row(row, desc[f], ver.get(f), classes, filt, args.max_words))
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(COMPOSED, 'w', encoding='utf-8') as fo:
        for r in out:
            fo.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'{os.path.relpath(COMPOSED, ROOT)}: {len(out)} ảnh')
    print_stats(out)


def print_stats(rows: list[dict]) -> None:
    if not rows:
        print('chưa có caption nào')
        return
    words = [r['n_words'] for r in rows]
    claim, kept = sum(r['n_claim'] for r in rows), sum(r['n_kept'] for r in rows)
    st = collections.Counter(r['status'] for r in rows)
    flags = collections.Counter(i.split(':')[0].split('(')[0].strip() for r in rows for i in r['issues'])
    print(f'số từ: TB {statistics.mean(words):.0f} · trung vị {statistics.median(words):.0f} · '
          f'min {min(words)} · max {max(words)} (paper LLMDet ~115)')
    print(f'chi tiết VLM: {claim} nêu ra, {kept} qua kiểm chứng ({kept / max(claim, 1):.0%}); '
          f'TB {kept / len(rows):.1f} chi tiết / ảnh')
    print(f'trạng thái: {dict(st)}; cờ: {dict(flags)}')


# ───────────────────────────── 4) translate ─────────────────────────────

def protect(sentences: list[str], name_vi: dict[str, str], filt: CaptionFilter) -> tuple[list[str], list[str]]:
    """Thay tên món EN bằng [[k]] để model không tự dịch tên; trả (câu đã che, tên Việt theo k)."""
    table: list[str] = []

    def sub(m: re.Match) -> str:
        vi = name_vi[filt.surface[m.group(1).lower()]]
        if vi not in table:
            table.append(vi)
        return f'[[{table.index(vi)}]]'

    return [filt.dish_re.sub(sub, s) for s in sentences], table


def restore(sentences: list[str], table: list[str]) -> Optional[list[str]]:
    out = []
    for s in sentences:
        ids = re.findall(r'\[\[(\d+)\]\]', s)
        if any(int(i) >= len(table) for i in ids):
            return None
        out.append(re.sub(r'\[\[(\d+)\]\]', lambda m: table[int(m.group(1))], s))
    return out


def translate_row(vlm: VLM, sentences: list[str], name_vi: dict[str, str], filt: CaptionFilter) -> Optional[list[str]]:
    masked, table = protect(sentences, name_vi, filt)
    items = '\n'.join(f'{i}. {s}' for i, s in enumerate(masked, 1))
    ans = parse_json(vlm.ask([], TRANSLATE_PROMPT.format(n=len(masked), items=items), max_new_tokens=60 * len(masked)))
    if not isinstance(ans, list) or len(ans) != len(masked) or not all(isinstance(x, str) for x in ans):
        return None
    for src, dst in zip(masked, ans):  # số placeholder phải giữ nguyên ở từng câu -> bản Việt khớp 1:1 bản Anh
        if sorted(re.findall(r'\[\[\d+\]\]', src)) != sorted(re.findall(r'\[\[\d+\]\]', dst)):
            return None
    return restore(ans, table)


def cmd_translate(args: argparse.Namespace) -> None:
    classes = load_taxonomy()
    filt = CaptionFilter(classes)
    name_vi = {c['name']: c['name_vi'] for c in classes}
    done = done_files(RAW)
    rows = [r for r in read_jsonl(COMPOSED) if r['filename'] not in done]
    if args.limit:
        rows = rows[:args.limit]
    print(f'translate: còn {len(rows)} ảnh -> {os.path.relpath(RAW, ROOT)}')
    vlm = None if args.skip else VLM(args.model, args.load_4bit)
    for k, r in enumerate(rows, 1):
        vi = None if vlm is None else translate_row(vlm, r['sentences'], name_vi, filt)
        if vi is None and vlm is not None:  # thử lại từng câu
            parts = [translate_row(vlm, [s], name_vi, filt) for s in r['sentences']]
            vi = [p[0] for p in parts] if all(parts) else None
        if vi is None:
            r = dict(r, status='flagged', issues=r['issues'] + ['FLAG chưa có bản dịch tiếng Việt'])
        else:
            r = dict(r, sentences_vi=vi, caption_vi=' '.join(vi))
        append_jsonl(RAW, r)
        if k % 50 == 0:
            print(f'{k}/{len(rows)}', flush=True)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    for name in ('describe', 'verify', 'translate'):
        s = sub.add_parser(name)
        s.add_argument('--model', default='llava-hf/llava-onevision-qwen2-7b-ov-hf')
        s.add_argument('--load-4bit', action='store_true')
        s.add_argument('--limit', type=int, default=0, help='chỉ chạy N ảnh (thử)')
        s.add_argument('--ann', default=os.path.join(ANN, 'train_od.jsonl'), help='mỗi ảnh một dòng, đủ 54 lớp GT')
    sub.choices['translate'].add_argument('--skip', action='store_true',
                                          help='không dịch (không cần GPU): chép sang vlm_captions.jsonl, gắn cờ mọi ảnh')
    c = sub.add_parser('compose')
    c.add_argument('--ann', default=os.path.join(ANN, 'train_od.jsonl'))
    c.add_argument('--max-words', type=int, default=140)
    c.add_argument('--allow-unverified', action='store_true', help='ghép cả ảnh chưa qua bước verify (chỉ để thử)')
    sub.add_parser('stats')
    args = p.parse_args()
    if args.cmd == 'stats':
        print_stats(list(read_jsonl(COMPOSED)) if os.path.exists(COMPOSED) else [])
        return
    {'describe': cmd_describe, 'verify': cmd_verify, 'compose': cmd_compose, 'translate': cmd_translate}[args.cmd](args)


if __name__ == '__main__':
    main()
