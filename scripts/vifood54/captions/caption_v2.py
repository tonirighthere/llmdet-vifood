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

Các bước (mỗi bước chạy lại được giữa chừng; 1, 2, 4 cần GPU, 3 chỉ CPU). Mỗi lần chạy nằm trong
captions_v2/<run>/ (--run), để so nhiều model trên cùng ảnh:
  1) describe   VLM mô tả từng món + bối cảnh           -> <run>/describe.jsonl
  2) verify     VLM (model khác) xác nhận từng chi tiết  -> <run>/verify.jsonl
  3) compose    ghép đoạn văn EN 80–120 từ, lọc, gắn cờ  -> <run>/composed.jsonl
  4) translate  dịch từng câu sang tiếng Việt            -> <run>/translated.jsonl
  5) compare    so nhiều run trên cùng ảnh               -> captions_v2/COMPARE.md + compare_scores.csv
  6) publish    chép run được chọn sang annotations_en/vlm_captions.jsonl
  rồi: VIFOOD_LANG=en review_captions.py  ->  VIFOOD_LANG=en vlm_captions.py attach --suffix _lmm_v2

Gọi model (--backend):
  vllm (mặc định)  máy chủ vLLM chạy riêng (`vllm serve`, API kiểu OpenAI); --workers yêu cầu song song, vLLM tự gom lô.
                   Xem scripts/vifood54/captions/vast/RUNBOOK.md.
  hf               transformers trên GPU máy này, tuần tự (dự phòng khi vLLM chưa hỗ trợ model).

    C=scripts/vifood54/captions/caption_v2.py
    python $C describe  --run q32 --url http://localhost:8000 --limit 50 --workers 32
    python $C verify    --run q32 --url http://localhost:8001 --workers 32
    python $C compose   --run q32 && python $C stats --run q32
    python $C translate --run q32 --url http://localhost:8001 --workers 32
    python $C compare   --runs q8,q32,q72
    python $C publish   --run q32
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import re
import statistics
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Callable, Iterator, Optional

os.environ['VIFOOD_LANG'] = 'en'  # caption v2 chỉ có bản tiếng Anh (annotations_en/)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
sys.path.insert(0, HERE)
from builder_en import COUNT_WORDS, SIZE_EN, _article, _cap, location_en  # noqa: E402
from en_names import CONTAINER_EN  # noqa: E402
from layout import group_instances  # noqa: E402
from vlm_captions import ANN, RAW, CaptionFilter, load_taxonomy, read_jsonl  # noqa: E402

OUT_DIR = os.path.join(ROOT, 'grounding_data/vifood54/captions_v2')
# đường dẫn của run hiện tại; set_run() gán lại khi có --run
DESCRIBE = VERIFY = COMPOSED = TRANSLATED = ''


def set_run(run: str) -> None:
    global DESCRIBE, VERIFY, COMPOSED, TRANSLATED
    d = os.path.join(OUT_DIR, run)
    DESCRIBE, VERIFY, COMPOSED, TRANSLATED = (os.path.join(d, f) for f in (
        'describe.jsonl', 'verify.jsonl', 'composed.jsonl', 'translated.jsonl'))


set_run('default')
MAX_SIDE_CROP, MAX_SIDE_SCENE = 768, 1280  # cạnh dài tối đa (px) ảnh gửi VLM: giới hạn số token ảnh -> lô lớn hơn
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

_WRITE_LOCK = threading.Lock()


def append_jsonl(path: str, row: dict) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with _WRITE_LOCK, open(path, 'a', encoding='utf-8') as f:
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


def shrink(img, max_side: int):
    """Thu nhỏ (giữ tỉ lệ) để cạnh dài <= max_side; không phóng to."""
    if max(img.size) <= max_side:
        return img
    img = img.copy()
    img.thumbnail((max_side, max_side))
    return img


def crop_box(img, box: list[float], margin: float = 0.15):
    x1, y1, x2, y2 = box
    mw, mh = (x2 - x1) * margin, (y2 - y1) * margin
    return shrink(img.crop((max(0, x1 - mw), max(0, y1 - mh), min(img.width, x2 + mw), min(img.height, y2 + mh))),
                  MAX_SIDE_CROP)


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


class OpenAIVLM:
    """Gọi máy chủ vLLM (`vllm serve`, API /v1/chat/completions kiểu OpenAI). An toàn khi gọi từ nhiều luồng:
    mỗi luồng gửi một yêu cầu, vLLM tự gom các yêu cầu đang chờ thành lô trên GPU."""

    def __init__(self, url: str, model: Optional[str] = None, timeout: int = 300, retries: int = 3):
        import urllib.request
        self.req = urllib.request
        self.base = url.rstrip('/')
        if not self.base.endswith('/v1'):
            self.base += '/v1'
        self.timeout, self.retries = timeout, retries
        if model is None:  # tên model vLLM đang phục vụ
            with self.req.urlopen(self.base + '/models', timeout=30) as r:
                model = json.load(r)['data'][0]['id']
        self.name = model

    @staticmethod
    def _data_url(img) -> str:
        import base64
        import io
        buf = io.BytesIO()
        img.save(buf, format='JPEG', quality=90)
        return 'data:image/jpeg;base64,' + base64.b64encode(buf.getvalue()).decode()

    def ask(self, images: list, text: str, max_new_tokens: int = 200) -> str:
        content = [{'type': 'image_url', 'image_url': {'url': self._data_url(im)}} for im in images]
        content.append({'type': 'text', 'text': text})
        body = json.dumps({'model': self.name, 'messages': [{'role': 'user', 'content': content}],
                           'temperature': 0.0, 'max_tokens': max_new_tokens}).encode()
        last: Optional[Exception] = None
        for attempt in range(self.retries):
            try:
                rq = self.req.Request(self.base + '/chat/completions', data=body,
                                      headers={'Content-Type': 'application/json'})
                with self.req.urlopen(rq, timeout=self.timeout) as r:
                    return (json.load(r)['choices'][0]['message']['content'] or '').strip()
            except Exception as e:  # mạng / máy chủ quá tải: thử lại có giãn cách
                last = e
                time.sleep(2 * (attempt + 1))
        raise RuntimeError(f'vLLM {self.base}: {last}')


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


def make_vlm(args: argparse.Namespace):
    if args.backend == 'vllm':
        return OpenAIVLM(args.url, args.served_model)
    if args.workers != 1:
        print('backend hf: chạy tuần tự (--workers bị bỏ qua)')
        args.workers = 1
    return VLM(args.model, args.load_4bit)


def run_parallel(items: list, work: Callable[[Any], dict], out_path: str, workers: int, label: str) -> None:
    """Chạy work(item) song song, ghi từng kết quả ngay khi xong (dừng giữa chừng không mất việc).
    Lỗi ở một ảnh chỉ in ra, ảnh đó chạy lại ở lần sau (vì chưa có trong file)."""
    t0, n_ok, n_err = time.time(), 0, 0
    with ThreadPoolExecutor(max_workers=max(1, workers)) as ex:
        futs = {ex.submit(work, it): it for it in items}
        for k, f in enumerate(as_completed(futs), 1):
            try:
                append_jsonl(out_path, f.result())
                n_ok += 1
            except Exception as e:  # không dừng cả đợt vì một ảnh
                n_err += 1
                print(f'!! {label}: {futs[f].get("filename", "?")}: {type(e).__name__}: {str(e)[:160]}', flush=True)
            if k % 50 == 0 or k == len(items):
                el = time.time() - t0
                print(f'{label} {k}/{len(items)} · {el / k:.2f}s/ảnh (thực tế, đã song song) · '
                      f'còn ~{el / k * (len(items) - k) / 60:.0f} phút · lỗi {n_err}', flush=True)


def load_rows(args: argparse.Namespace, done: set[str]) -> list[dict]:
    rows = [r for r in read_jsonl(args.ann) if r['detection']['instances'] and r['filename'] not in done]
    return rows[:args.limit] if args.limit else rows


def open_image(filename: str):
    from PIL import Image, ImageOps
    path = os.path.join(ROOT, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(f'không thấy ảnh {path} (giải nén gói ảnh vào gốc repo, giữ nguyên đường dẫn)')
    return ImageOps.exif_transpose(Image.open(path)).convert('RGB')


# ───────────────────────────── 1) describe ─────────────────────────────

def describe_row(vlm, row: dict, classes: list[dict], cleaner: PhraseCleaner) -> dict:
    img = open_image(row['filename'])
    dishes: dict[str, dict] = {}
    for label, box in largest_boxes(row).items():
        c = classes[label]
        if not c['visual']['attrs']:  # lớp gom (other dish, dessert): không có hình thái chung -> không hỏi
            continue
        ans = parse_json(vlm.ask([crop_box(img, box)], DISH_PROMPT.format(
            name=c['name'], definition=c['visual']['definition'], containers=', '.join(CONTAINERS)),
            max_new_tokens=220))
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
    sc = parse_json(vlm.ask([shrink(img, MAX_SIDE_SCENE)], SCENE_PROMPT, max_new_tokens=160))
    scene = {'error': 'json'} if not isinstance(sc, dict) else {
        'surface': cleaner.clean(sc.get('surface')) or '',
        'utensils': cleaner.clean_list(sc.get('utensils'), 3),
        'other_objects': cleaner.clean_list(sc.get('other_objects'), 4),
        'background': cleaner.clean(sc.get('background')) or '',
    }
    return {'filename': row['filename'], 'model': vlm.name, 'dishes': dishes, 'scene': scene}


def cmd_describe(args: argparse.Namespace) -> None:
    classes = load_taxonomy()
    cleaner = PhraseCleaner(classes)
    rows = load_rows(args, done_files(DESCRIBE))
    print(f'describe [{os.path.relpath(DESCRIBE, ROOT)}]: còn {len(rows)} ảnh')
    if not rows:
        return
    vlm = make_vlm(args)
    run_parallel(rows, lambda r: describe_row(vlm, r, classes, cleaner), DESCRIBE, args.workers, 'describe')


# ───────────────────────────── 2) verify ─────────────────────────────

def phrases_of(d: dict, keys: tuple[str, ...]) -> list[str]:
    out: list[str] = []
    for key in keys:
        v = d.get(key)
        out += v if isinstance(v, list) else ([v] if v else [])
    return out


DISH_KEYS, SCENE_KEYS = ('colors', 'components', 'arrangement'), ('surface', 'utensils', 'other_objects', 'background')


def ask_yes_no(vlm: Any, image, phrases: list[str]) -> dict[str, bool]:
    if not phrases:
        return {}
    items = '\n'.join(f'{i}. {p}' for i, p in enumerate(phrases, 1))
    ans = parse_json(vlm.ask([image], VERIFY_PROMPT.format(items=items), max_new_tokens=16 * len(phrases) + 16))
    if not isinstance(ans, dict):
        return {p: False for p in phrases}  # không đọc được -> coi như chưa xác nhận
    return {p: str(ans.get(str(i), 'no')).strip().lower().startswith('y') for i, p in enumerate(phrases, 1)}


def verify_row(vlm, row: dict) -> dict:
    img = open_image(row['filename'])
    ok: dict[str, dict[str, bool]] = {}
    for label, d in row['dishes'].items():
        if 'error' not in d:
            ok[label] = ask_yes_no(vlm, crop_box(img, d['box']), phrases_of(d, DISH_KEYS))
    scene_ok = {} if 'error' in row['scene'] else ask_yes_no(vlm, shrink(img, MAX_SIDE_SCENE),
                                                              phrases_of(row['scene'], SCENE_KEYS))
    return {'filename': row['filename'], 'model': vlm.name, 'dishes': ok, 'scene': scene_ok}


def cmd_verify(args: argparse.Namespace) -> None:
    done = done_files(VERIFY)
    rows = [r for r in read_jsonl(DESCRIBE) if r['filename'] not in done]
    if args.limit:
        rows = rows[:args.limit]
    print(f'verify [{os.path.relpath(VERIFY, ROOT)}]: còn {len(rows)} ảnh')
    if not rows:
        return
    vlm = make_vlm(args)
    desc_model = rows[0].get('model', '')
    if desc_model and desc_model == vlm.name:
        print(f'!! CẢNH BÁO: model kiểm chứng trùng model mô tả ({desc_model}) -> kiểm chứng chéo mất tác dụng')
    run_parallel(rows, lambda r: verify_row(vlm, r), VERIFY, args.workers, 'verify')


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


SCENE_WORDS = {'tablecloth', 'table', 'surface', 'spoon', 'spoons', 'chopstick', 'chopsticks', 'fork', 'knife',
               'napkin', 'rim', 'plate', 'plates', 'bowl', 'tray', 'basket', 'placemat', 'mat', 'saucer',
               'glass', 'glasses', 'mug', 'mugs', 'cup', 'cups', 'bottle', 'teapot', 'beer'}
STOP_WORDS = {'a', 'an', 'the', 'and', 'of', 'with', 'on', 'in'}


def clean_details(phrases: list[str]) -> list[str]:
    """Chi tiết của MÓN: bỏ cụm tả bàn / bát đĩa / dụng cụ (thuộc bối cảnh) và cụm trùng (cùng tập từ hoặc tập con)."""
    out: list[str] = []
    seen: list[set[str]] = []
    for p in phrases:
        words = set(re.findall(r"[a-z]+", p.lower()))
        if words & SCENE_WORDS:
            continue
        key = words - STOP_WORDS
        if not key or any(key <= k or k <= key for k in seen):
            continue
        seen.append(key)
        out.append(p)
    return out


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

    # ít món -> nhiều chi tiết mỗi món (caption ~100-140 từ như paper); nhiều món -> ít hơn. Quá 140 từ thì tự bớt (bên dưới)
    per_dish = {1: 10, 2: 8, 3: 6}.get(len(groups), 4 if len(groups) <= 5 else 3)
    blocks: list[tuple[str, list[str], list[str], str, str]] = []  # (câu giới thiệu, chi tiết, cách bày, đại từ, động từ)
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
        details = clean_details(confirmed(str(g.label), d.get('colors', []) + d.get('components', [])))
        arr = confirmed(str(g.label), [d['arrangement']] if d.get('arrangement') else [])
        blocks.append((f'{_cap(loc)} there {verb} {np_}.', details, arr, 'It' if g.n == 1 else 'They', verb))
    scene: list[str] = []
    for a, b in zip(groups, groups[1:3]):  # tối đa 2 quan hệ giữa các món lớn nhất
        rel = relation(a, b)
        if rel:
            scene.append(f'The {a.name} {"is" if a.n == 1 else "are"} {rel} the {b.name}.')
    sc = desc['scene'] if 'error' not in desc['scene'] else {}
    surface = confirmed(None, [sc['surface']] if sc.get('surface') else [])
    if surface:
        scene.append(f'The dishes are set on {_article(surface[0])} {surface[0]}.')
    objs = confirmed(None, sc.get('utensils', []) + sc.get('other_objects', []))
    if objs:
        scene.append(f'Also visible: {join_and(objs)}.')
    bg = confirmed(None, [sc['background']] if sc.get('background') else [])
    if bg:
        scene.append(f'The background shows {_article(bg[0])} {bg[0]}.')

    def render(per: int, with_arr: bool) -> list[str]:
        out: list[str] = []
        for intro, details, arr, pron, verb in blocks:
            out.append(intro)
            if details[:per]:
                out.append(f'{pron} {"shows" if pron == "It" else "show"} {join_and(details[:per])}.')
            if arr and with_arr:
                out.append(f'{pron} {verb} {arr[0]}.')
        return out

    def n_words_of(xs: list[str]) -> int:
        return len(' '.join(xs).split())

    # Quá dài: bỏ câu bối cảnh (từ cuối) trước, rồi bớt cách bày, rồi bớt dần chi tiết mỗi món.
    # KHÔNG BAO GIỜ bỏ câu giới thiệu món -> mọi món có nhãn đều có tên trong caption.
    sentences = render(per_dish, True)
    extra = list(scene)
    while extra and n_words_of(sentences + extra) > max_words:
        extra.pop()
    if n_words_of(sentences + extra) > max_words:
        for per, with_arr in [(per_dish, False)] + [(k, False) for k in range(per_dish - 1, -1, -1)]:
            sentences = render(per, with_arr)
            if n_words_of(sentences) <= max_words:
                break
    sentences = sentences + extra
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


def translate_row(vlm: Any, sentences: list[str], name_vi: dict[str, str], filt: CaptionFilter) -> Optional[list[str]]:
    masked, table = protect(sentences, name_vi, filt)
    items = '\n'.join(f'{i}. {s}' for i, s in enumerate(masked, 1))
    ans = parse_json(vlm.ask([], TRANSLATE_PROMPT.format(n=len(masked), items=items), max_new_tokens=60 * len(masked)))
    if not isinstance(ans, list) or len(ans) != len(masked) or not all(isinstance(x, str) for x in ans):
        return None
    for src, dst in zip(masked, ans):  # số placeholder phải giữ nguyên ở từng câu -> bản Việt khớp 1:1 bản Anh
        if sorted(re.findall(r'\[\[\d+\]\]', src)) != sorted(re.findall(r'\[\[\d+\]\]', dst)):
            return None
    return restore(ans, table)


def translate_one(vlm, r: dict, name_vi: dict[str, str], filt: CaptionFilter) -> dict:
    vi = None if vlm is None else translate_row(vlm, r['sentences'], name_vi, filt)
    if vi is None and vlm is not None:  # thử lại từng câu
        parts = [translate_row(vlm, [s], name_vi, filt) for s in r['sentences']]
        vi = [p[0] for p in parts] if all(parts) else None
    if vi is None:
        return dict(r, status='flagged', issues=r['issues'] + ['FLAG chưa có bản dịch tiếng Việt'])
    return dict(r, sentences_vi=vi, caption_vi=' '.join(vi))


def cmd_translate(args: argparse.Namespace) -> None:
    classes = load_taxonomy()
    filt = CaptionFilter(classes)
    name_vi = {c['name']: c['name_vi'] for c in classes}
    done = done_files(TRANSLATED)
    rows = [r for r in read_jsonl(COMPOSED) if r['filename'] not in done]
    if args.limit:
        rows = rows[:args.limit]
    print(f'translate [{os.path.relpath(TRANSLATED, ROOT)}]: còn {len(rows)} ảnh')
    if not rows:
        return
    vlm = None if args.skip else make_vlm(args)
    run_parallel(rows, lambda r: translate_one(vlm, r, name_vi, filt), TRANSLATED, args.workers, 'translate')


# ───────────────────────────── 5) compare / 6) publish ─────────────────────────────

def cmd_compare(args: argparse.Namespace) -> None:
    """Đặt caption của nhiều run cạnh nhau trên CÙNG ảnh cho người chấm; kèm số liệu tự động mỗi run."""
    runs = [r.strip() for r in args.runs.split(',') if r.strip()]
    data: dict[str, dict[str, dict]] = {}
    for run in runs:
        set_run(run)
        path = TRANSLATED if os.path.exists(TRANSLATED) else COMPOSED
        if not os.path.exists(path):
            raise SystemExit(f'run {run}: chưa có {os.path.relpath(path, ROOT)}')
        data[run] = {r['filename']: r for r in read_jsonl(path)}
    common = sorted(set.intersection(*(set(d) for d in data.values())))
    if args.limit:
        common = common[:args.limit]
    if not common:
        raise SystemExit('các run không có ảnh chung')
    L = [f'# So sánh caption v2 giữa các model ({len(common)} ảnh chung)', '',
         '| Run | Model mô tả + kiểm chứng | Số từ TB | Chi tiết nêu / qua kiểm chứng | Tỉ lệ bị loại | Chi tiết qua kiểm chứng / ảnh | Ảnh bị gắn cờ |',
         '|---|---|---|---|---|---|---|']
    for run in runs:
        rows = [data[run][f] for f in common]
        claim, kept = sum(r['n_claim'] for r in rows), sum(r['n_kept'] for r in rows)
        L.append(f'| {run} | {rows[0].get("model", "")} | {statistics.mean(r["n_words"] for r in rows):.0f} | '
                 f'{claim} / {kept} | {1 - kept / max(claim, 1):.0%} | {kept / len(rows):.1f} | '
                 f'{sum(r["status"] == "flagged" for r in rows)} |')
    L += ['', 'Người chấm: đọc bản tiếng Việt (bản Anh để đối chiếu), điền `compare_scores.csv`: số câu SAI so với ảnh, '
          'số chi tiết CHUNG CHUNG (vd "green leaves" thay vì gọi đúng loại rau), điểm tổng 1–5. '
          'Thứ tự các run trong từng ảnh được giữ cố định; nên chấm mà không nhìn tên run.', '']
    for f in common:
        L += [f'## `{os.path.basename(f)}`', '', f'Món (nhãn): {", ".join(data[runs[0]][f]["gt"])}', '']
        for i, run in enumerate(runs):
            r = data[run][f]
            L += [f'**[{chr(65 + i)}]** ({r["n_words"]} từ, {r["n_kept"]}/{r["n_claim"]} chi tiết)', '',
                  '> ' + (r.get('caption_vi') or '(chưa dịch)'), '', f'<sub>EN: {r["caption"]}</sub>', '']
    out_md = os.path.join(OUT_DIR, 'COMPARE.md')
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(out_md, 'w', encoding='utf-8') as fo:
        fo.write('\n'.join(L) + '\n')
    out_csv = os.path.join(OUT_DIR, 'compare_scores.csv')
    if not os.path.exists(out_csv):  # không ghi đè điểm đã chấm
        with open(out_csv, 'w', encoding='utf-8') as fo:
            fo.write('filename,run_letter,run,n_wrong_sentences,n_generic_details,overall_1to5,note\n')
            for f in common:
                for i, run in enumerate(runs):
                    fo.write(f'{os.path.basename(f)},{chr(65 + i)},{run},,,,\n')
    print(f'-> {os.path.relpath(out_md, ROOT)}, {os.path.relpath(out_csv, ROOT)}')
    print('\n'.join(L[:3 + len(runs)]))


def cmd_publish(args: argparse.Namespace) -> None:
    """Chép bản dịch của run được chọn sang annotations_en/vlm_captions.jsonl (đầu vào review_captions / attach)."""
    if not os.path.exists(TRANSLATED):
        raise SystemExit(f'chưa có {os.path.relpath(TRANSLATED, ROOT)} -> chạy translate trước')
    rows = list(read_jsonl(TRANSLATED))
    if os.path.exists(RAW) and not args.force:
        raise SystemExit(f'{os.path.relpath(RAW, ROOT)} đã có; thêm --force để ghi đè (bản cũ đổi tên .bak)')
    if os.path.exists(RAW):
        os.replace(RAW, RAW + '.bak')
    with open(RAW, 'w', encoding='utf-8') as fo:
        for r in rows:
            fo.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'{len(rows)} caption -> {os.path.relpath(RAW, ROOT)}')
    print_stats(rows)


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest='cmd', required=True)
    for name in ('describe', 'verify', 'translate'):
        s = sub.add_parser(name)
        s.add_argument('--run', default='default', help='tên lần chạy: captions_v2/<run>/')
        s.add_argument('--backend', choices=['vllm', 'hf'], default='vllm')
        s.add_argument('--url', default='http://localhost:8000', help='máy chủ vLLM (backend vllm)')
        s.add_argument('--served-model', default=None, help='tên model trên máy chủ vLLM (mặc định: hỏi /v1/models)')
        s.add_argument('--workers', type=int, default=32, help='số yêu cầu gửi song song (backend vllm)')
        s.add_argument('--model', default='llava-hf/llava-onevision-qwen2-7b-ov-hf', help='backend hf: model HF')
        s.add_argument('--load-4bit', action='store_true', help='backend hf')
        s.add_argument('--limit', type=int, default=0, help='chỉ chạy N ảnh (thử)')
        s.add_argument('--ann', default=os.path.join(ANN, 'train_od.jsonl'), help='mỗi ảnh một dòng, đủ 54 lớp GT')
    sub.choices['translate'].add_argument('--skip', action='store_true',
                                          help='không dịch (không cần GPU): gắn cờ mọi ảnh')
    c = sub.add_parser('compose')
    c.add_argument('--run', default='default')
    c.add_argument('--ann', default=os.path.join(ANN, 'train_od.jsonl'))
    c.add_argument('--max-words', type=int, default=140)
    c.add_argument('--allow-unverified', action='store_true', help='ghép cả ảnh chưa qua bước verify (chỉ để thử)')
    st = sub.add_parser('stats')
    st.add_argument('--run', default='default')
    cp = sub.add_parser('compare')
    cp.add_argument('--runs', required=True, help='vd q8,q32,q72')
    cp.add_argument('--limit', type=int, default=0)
    pb = sub.add_parser('publish')
    pb.add_argument('--run', required=True)
    pb.add_argument('--force', action='store_true')
    args = p.parse_args()
    if getattr(args, 'run', None):
        set_run(args.run)
    if args.cmd == 'stats':
        print_stats(list(read_jsonl(COMPOSED)) if os.path.exists(COMPOSED) else [])
        return
    {'describe': cmd_describe, 'verify': cmd_verify, 'compose': cmd_compose, 'translate': cmd_translate,
     'compare': cmd_compare, 'publish': cmd_publish}[args.cmd](args)


if __name__ == '__main__':
    main()
