"""Trích ví dụ caption dài được sửa theo phán đoán VLM (Gemma) để xem tay.

Với mỗi ảnh đã có kết quả VLM: mỗi đặc điểm mẫu (taxonomy attrs) xuất hiện trong caption mà VLM
không xác nhận ('visible') bị bỏ, thay bằng đặc điểm VLM thấy nhưng caption chưa nói, hoặc đặc điểm
VLM tự thêm ('extra', đã lọc các cụm tả dụng cụ/nền). Chỉ để minh họa, chưa ghi vào dữ liệu train.

    python scripts/vifood54/captions/vlm_revise_examples.py --n 5
"""
import argparse
import json
import os
import re

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
ANN = os.path.join(ROOT, 'grounding_data/vifood54/annotations')
VLM_DIR = os.path.join(ROOT, 'grounding_data/vifood54/vlm_attrs')
# cụm VLM thêm nhưng tả dụng cụ / nền / bố cục chứ không phải món
NOT_FOOD = re.compile(r'đĩa|bát|chén|tô|khay|rổ|mẹt|nồi|ly|cốc|muỗng|thìa|đũa|nền|bàn|khăn|hoa văn|viền|giấy|hộp|túi')


def revise(caption, classes, tax):
    """Trả về (caption mới, danh sách thay đổi)."""
    sents = [s for s in re.split(r'(?<=\.)\s+', caption) if s]
    out, changes = [], []
    for s in sents:
        for name, v in classes.items():
            if 'error' in v or name not in s:
                continue
            attrs = tax[name]['visual']['attrs']
            visible = set(v.get('visible') or [])
            pool = [a for a in v.get('visible') or [] if f', {a}' not in caption and f', {a}' not in s]
            pool += [e for e in v.get('extra') or [] if not NOT_FOOD.search(e) and e not in s]
            for a in attrs:
                if f', {a}' in s and a not in visible:
                    new = pool.pop(0) if pool else None
                    s = s.replace(f', {a}', f', {new}' if new else '', 1)
                    changes.append((name, a, new))
        out.append(s)
    return ' '.join(out), changes


def draw(img, inst, vlm_boxes, font):
    d = ImageDraw.Draw(img)
    for it in inst:
        b = it['bbox']
        hl = any(abs(b[0] - x[0]) < 1 and abs(b[1] - x[1]) < 1 for x in vlm_boxes)
        col = (255, 60, 60) if hl else (255, 210, 0)
        d.rectangle(b, outline=col, width=4 if hl else 2)
        tw = d.textlength(it['category'], font=font)
        d.rectangle([b[0], b[1], b[0] + tw + 6, b[1] + font.size + 6], fill=col)
        d.text((b[0] + 3, b[1] + 2), it['category'], fill=(0, 0, 0), font=font)
    return img


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--vlm', default=os.path.join(VLM_DIR, 'train_gemma-4-12B-it_shard0of2.jsonl'))
    p.add_argument('--n', type=int, default=5)
    p.add_argument('--min-changes', type=int, default=3)
    p.add_argument('--out-dir', default=os.path.join(VLM_DIR, 'examples'))
    args = p.parse_args()

    tax = {c['name']: c for c in json.load(open(os.path.join(ANN, 'taxonomy.json'), encoding='utf-8'))['classes']}
    caps = {}
    for line in open(os.path.join(ANN, 'train_vg_cap.jsonl'), encoding='utf-8'):
        r = json.loads(line)
        caps[r['filename']] = r
    vlm = [json.loads(l) for l in open(args.vlm, encoding='utf-8')]

    cands = []
    for v in vlm:
        r = caps.get(v['filename'])
        if not r:
            continue
        cap = r['grounding']['caption']
        new, ch = revise(cap, v['classes'], tax)
        if len(ch) >= args.min_changes:
            cands.append((len(cap), v, r, new, ch))
    cands.sort(key=lambda x: -x[0])
    # chọn ảnh dài nhất nhưng đa dạng món
    picked, seen = [], set()
    for c in cands:
        names = frozenset(c[1]['classes'])
        if len(names & seen) > len(names) // 2:
            continue
        picked.append(c)
        seen |= names
        if len(picked) == args.n:
            break

    os.makedirs(args.out_dir, exist_ok=True)
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
    md = ['# Ví dụ caption dài được VLM (Gemma 4 12B, 4-bit) sửa', '',
          f'Nguồn: `{os.path.relpath(args.vlm, ROOT)}` (shard 0). {len(cands)} ảnh có ≥{args.min_changes} thay đổi; '
          f'chọn {len(picked)} ảnh caption dài nhất, đa dạng món.', '',
          'Box **đỏ** = crop gửi VLM (box lớn nhất mỗi món), vàng = box khác. '
          'Trong caption sửa: ~~gạch~~ = đặc điểm VLM không thấy, **đậm** = đặc điểm thay vào (VLM thấy).',
          'Chỉ minh họa — chưa ghi vào dữ liệu train.', '']
    for k, (_, v, r, new, ch) in enumerate(picked, 1):
        with Image.open(os.path.join(ROOT, r['filename'])) as im:
            img = ImageOps.exif_transpose(im).convert('RGB')
        boxes = [c['box'] for c in v['classes'].values() if 'box' in c]
        draw(img, r['detection']['instances'], boxes, font).save(os.path.join(args.out_dir, f'ex{k}.jpg'), quality=90)
        cap = r['grounding']['caption']
        marked = cap
        for name, old, nw in ch:
            marked = marked.replace(f', {old}', f', ~~{old}~~' + (f' **{nw}**' if nw else ''), 1)
        md += [f'## {k}. `{os.path.basename(r["filename"])}`', '', f'![ex{k}](examples/ex{k}.jpg)', '',
               '**Caption gốc:**', '', f'> {cap}', '', '**Thay đổi:**', '', f'> {marked}', '',
               '**Caption sau sửa:**', '', f'> {new}', '',
               '| Món | VLM: đúng món? | Đặc điểm VLM thấy | VLM thêm | Đựng trong |', '|---|---|---|---|---|']
        for name, c in v['classes'].items():
            if 'error' in c:
                md.append(f'| {name} | lỗi | | | |')
                continue
            md.append(f'| {name} | {c["match"]} | {", ".join(c["visible"]) or "—"} | '
                      f'{", ".join(c["extra"]) or "—"} | {c["container"]} |')
        md.append('')
    out_md = os.path.join(VLM_DIR, 'VLM_REVISE_EXAMPLES.md')
    open(out_md, 'w', encoding='utf-8').write('\n'.join(md))
    print(f'{len(cands)} ứng viên, ghi {len(picked)} ví dụ -> {out_md}')


if __name__ == '__main__':
    main()
