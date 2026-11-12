#!/usr/bin/env python3
"""
vifood54_vlm.py
===============
Bước "nhìn ảnh trước" cho demo ViFood-54: Gemini liệt kê các món có trong ảnh (chọn trong 54 lớp của
taxonomy) và viết caption hình thái theo văn phong caption lúc train B3/B3b: số lượng + lượng từ + tên lớp +
vị trí (9 vùng) + đặc điểm nhìn thấy, không hương vị. Detector sau đó khoanh box cho từng tên món trong
caption (`vifood54_core.ground`, giống `eval_grounding.py`).

API key: biến môi trường GEMINI_API_KEY / GOOGLE_API_KEY, hoặc file `.env` / `.gemini_key` cạnh file
này (đã gitignore). Không có key mặc định trong mã, key không được in ra log.
Ảnh được gửi lên Google Gemini API; kết quả được nhớ theo hash ảnh trong phiên chạy.
"""
import hashlib
import io
import json
import os
import re
import time

from PIL import Image

import vifood54_core as core

HERE = os.path.dirname(os.path.abspath(__file__))
MODELS = ['gemini-3.5-flash-lite', 'gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-flash-latest']
TIMEOUT_S = int(os.environ.get('GEMINI_TIMEOUT_S', 45))  # mỗi model
BUDGET_S = int(os.environ.get('GEMINI_BUDGET_S', 60))  # tổng mọi lần thử, quá thì bỏ (rơi về prompt 54 lớp)
_CACHE = {}


def load_api_key():
    for k in ('GEMINI_API_KEY', 'GOOGLE_API_KEY'):
        if os.environ.get(k, '').strip():
            return os.environ[k].strip()
    for fn in ('.env', '.gemini_key'):
        p = os.path.join(HERE, fn)
        if not os.path.exists(p):
            continue
        with open(p, encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith(('GEMINI_API_KEY=', 'GOOGLE_API_KEY=')):
                    return line.split('=', 1)[1].strip().strip('"\'')
                if line and '=' not in line and not line.startswith('#'):
                    return line
    return None


def _menu():
    lines = []
    for c in core.TAXONOMY:
        alias = f" (còn gọi: {', '.join(c['aliases'])})" if c['aliases'] else ''
        lines.append(f"- {c['name']}{alias}: {c['visual']['definition']}")
    return '\n'.join(lines)


REGIONS = ['góc trên bên trái', 'phía trên', 'góc trên bên phải', 'bên trái', 'chính giữa', 'bên phải',
           'góc dưới bên trái', 'phía dưới', 'góc dưới bên phải']

PROMPT = f"""Bạn nhận diện món ăn Việt Nam trong ảnh. Danh mục gồm 54 lớp (tên lớp: cách nhận biết bằng mắt):
{_menu()}

Nhìn kỹ ảnh rồi:
1. Liệt kê MỌI món thấy rõ, kể cả rau sống, rau luộc, chén nước chấm. "name" phải là đúng một tên lớp trong
   danh mục (viết y hệt, có dấu). Món không thuộc danh mục -> đưa vào "other" kèm tên tiếng Việt và tên tiếng Anh
   ngắn gọn mô tả đúng món (ví dụ {{"name_vi": "bún chả", "name_en": "grilled pork with rice noodles"}}). "count": số phần/đĩa/tô/chén/chiếc
   nhìn thấy. "position": vị trí theo người xem ảnh, chọn trong: {', '.join(REGIONS)}, "rải rác trên bàn".
2. Viết "caption" tiếng Việt mô tả ảnh cho mô hình khoanh vùng, mỗi món một câu ngắn, theo mẫu:
   "Ở bên trái có một tô phở, nước dùng trong, bánh phở trắng và thịt bò tái." /
   "Hai rổ rau sống nằm ở bên trái và bên phải, nhiều loại lá." /
   "Một chén đồ chấm nằm ở góc dưới bên trái, lát ớt đỏ nổi trên mặt."
   Quy tắc caption:
   - Gọi mỗi món bằng ĐÚNG tên lớp trong danh mục (không dùng tên gọi khác), kèm số lượng và lượng từ.
   - Vị trí dùng đúng các cụm ở trên. Đặc điểm chỉ là thứ nhìn thấy: màu, hình dạng, thành phần, cách bày.
   - Không nhắc tên lớp nào khác ngoài các món có trong ảnh. Không dùng từ "của".
   - Không dùng từ hương vị, mùi, cảm giác hay cảm xúc (thơm, ngon, đậm đà, cay, giòn, mềm, hấp dẫn...).
   - Tối đa 120 từ.
Trả về JSON thuần:
{{"dishes": [{{"name": "...", "count": 1, "position": "..."}}], "other": [{{"name_vi": "...", "name_en": "..."}}],
  "caption": "...", "description": "một câu mô tả bữa ăn"}}"""

def _hash(pil):
    buf = io.BytesIO()
    pil.save(buf, format='PNG')
    return hashlib.sha1(buf.getvalue()).hexdigest()


def _to_class(name):
    """Tên Gemini trả -> tên lớp (khớp đúng, rồi qua tên gọi khác/cụm con)."""
    if name in core.BY_NAME:
        return name
    low = name.strip().lower()
    for c in core.CLASS_NAMES:
        if c.lower() == low:
            return c
    hits = core.parse_sentence(name)
    return hits[0]['name'] if hits else None


def describe(img_rgb):
    """-> dict(dishes=[{'name','count','position','raw'}], other=[str], caption, description,
    model, ms, cached, error)."""
    pil = Image.fromarray(img_rgb).convert('RGB')
    pil.thumbnail((1280, 1280))
    key = _hash(pil)
    if key in _CACHE:
        return dict(_CACHE[key], cached=True)
    api_key = load_api_key()
    if not api_key:
        return dict(dishes=[], other=[], caption='', description='', model=None, ms=0, cached=False,
                    error='Chưa có API key Gemini (đặt GEMINI_API_KEY hoặc file .gemini_key).')
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=api_key, http_options=types.HttpOptions(timeout=TIMEOUT_S * 1000))
    t0, last = time.time(), ''
    for m in MODELS + MODELS[:1]:  # hết lượt thì thử lại model đầu sau 3 s (503 thường thoáng qua)
        if last and time.time() - t0 > BUDGET_S:
            break
        if last and m == MODELS[0]:
            time.sleep(3)
        try:
            res = client.models.generate_content(
                model=m, contents=[pil, PROMPT],
                config=types.GenerateContentConfig(
                    response_mime_type='application/json', temperature=0.0,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)))
            data = json.loads(re.sub(r'^```(json)?|```$', '', res.text.strip()).strip())
        except Exception as e:  # thử model tiếp theo
            code = re.search(r'\b(4\d\d|5\d\d)\b', str(e))
            last = f"{m}: {code.group(1) + ' ' if code else ''}{type(e).__name__}"
            print(f'[vifood54_vlm] {last}: {str(e)[:100]}', flush=True)
            continue
        dishes, other, other_open = {}, [], []
        for o in data.get('other') or []:  # món ngoài 54 lớp: chuỗi (bản cũ) hoặc {name_vi, name_en}
            vi = (o.get('name_vi') or o.get('name') or '').strip() if isinstance(o, dict) else str(o).strip()
            en = (o.get('name_en') or '').strip() if isinstance(o, dict) else ''
            if vi and vi not in other:
                other.append(vi)
                other_open.append({'name_vi': vi, 'name_en': en})
        for d in data.get('dishes') or []:
            raw = d.get('name', '') if isinstance(d, dict) else str(d)
            cls = _to_class(raw)
            if cls is None:
                if raw and raw not in other:
                    other.append(raw)
                    other_open.append({'name_vi': raw, 'name_en': ''})
                continue
            cnt = int(d.get('count', 1) or 1) if isinstance(d, dict) else 1
            if cls in dishes:
                dishes[cls]['count'] += cnt
            else:
                dishes[cls] = {'name': cls, 'count': cnt, 'raw': raw,
                               'position': d.get('position', '') if isinstance(d, dict) else ''}
        out = dict(dishes=list(dishes.values()), other=other, other_open=other_open, caption=str(data.get('caption') or '').strip(),
                   description=data.get('description', ''),
                   model=m, ms=(time.time() - t0) * 1000, cached=False, error=None)
        _CACHE[key] = out
        return out
    return dict(dishes=[], other=[], caption='', description='', model=None, ms=(time.time() - t0) * 1000,
                cached=False, error=f'Gọi Gemini thất bại ({last}; 503 = Google quá tải, 429 = hết quota).')


# ───────────────────────────── caption -> prompt grounding ─────────────────────────────

MAX_TOKENS = 250  # 256 token BERT trừ [CLS]/[SEP]; dài hơn thì điểm ra NaN
_LINTER = None


def _linter():
    global _LINTER
    if _LINTER is None:
        import sys
        from transformers import AutoTokenizer
        sys.path.insert(0, os.path.join(core.ROOT, 'scripts/vifood54/captions'))
        from lint import CaptionLinter
        tok = AutoTokenizer.from_pretrained(os.path.join(core.ROOT, 'huggingface/bert-base-uncased'))
        _LINTER = CaptionLinter(tok, core.CLASS_NAMES, max_tokens=MAX_TOKENS)
    return _LINTER


def _spans(text):
    return [(e['span'][0], e['span'][1], e['surface']) for e in core.parse_sentence(text)]


def prepare_caption(caption, dishes=()):
    """Caption Gemini -> caption đưa vào detector: thêm câu cho món Gemini liệt kê mà caption không nhắc,
    bỏ bớt câu cuối nếu quá MAX_TOKENS. -> (caption, cảnh báo lint)."""
    lint = _linter()
    sents = [x.strip() for x in re.split(r'(?<=[.!?])\s+', ' '.join((caption or '').split())) if x.strip()]
    # câu không nhắc món nào mà có từ hương vị -> bỏ (không giúp khoanh box)
    sents = [x for x in sents if core.parse_sentence(x) or not lint.check(x, [])]
    text = ' '.join(x if x[-1] in '.!?' else x + '.' for x in sents)
    named = {e['name'] for e in core.parse_sentence(text)}
    for d in dishes:
        if d['name'] not in named:
            where = f" ở {d['position']}" if d.get('position') and d['position'] in REGIONS else ''
            text += f" Có {d['count']} phần {d['name']}{where}."
    while lint.n_tokens(text) > MAX_TOKENS and text.count('.') > 1:
        text = text[:text.rstrip('.').rfind('.') + 1]
    warnings = [w for w in lint.check(text, _spans(text)) if not w.startswith('span lệch')]
    return text.strip(), warnings


def keep_counts(items, dishes):
    """Giữ tối đa `count` box mỗi món (theo điểm), count lấy từ Gemini; món không có count giữ nguyên."""
    cap = {d['name']: d['count'] for d in dishes}
    out, used = [], {}
    for it in sorted(items, key=lambda x: -x['score']):
        n = used.get(it['name'], 0)
        if it['name'] in cap and n >= cap[it['name']]:
            continue
        used[it['name']] = n + 1
        out.append(it)
    return out


if __name__ == '__main__':
    import sys
    import numpy as np
    r = describe(np.array(Image.open(sys.argv[1]).convert('RGB')))
    print(json.dumps(r, ensure_ascii=False, indent=2))
    print(prepare_caption(r['caption'], r['dishes']))
