#!/usr/bin/env python3
"""
scripts/vifood54/build_vifood54.py
==================================
Pha 0: Chuẩn hóa dữ liệu ViFood-54 từ các export CVAT (YOLO 1.1).

1. Đọc taxonomy.json (54 tên nguồn -> class đích, gộp nhãn đồng nghĩa).
2. Gộp nhiều zip CVAT, đối chiếu ảnh trên đĩa, đổi tọa độ YOLO -> pixel (theo kích
   thước ảnh sau khi xoay EXIF, giống CVAT và mmcv).
3. Nhóm ảnh gốc: bản augment Roboflow (`*_jpg.rf.<hash>`) + ảnh gần trùng (dHash)
   được gom thành một group, cả group luôn nằm chung một split.
4. Chia train/val/test theo group, phân tầng theo lớp (ưu tiên lớp hiếm).
5. Cân bằng tập train:
   - lớp hiếm: repeat factor sampling kiểu LVIS r(c)=max(1, sqrt(t/f(c))), làm tròn ngẫu nhiên
     (mmengine ClassBalancedDataset làm tròn lên nên 1.01 -> 2, gần như nhân đôi mọi ảnh).
     Các bản lặp được augment vị trí (flip/crop/scale) trong config nên mỗi lần nhìn khác nhau.
   - lớp đầu (đồ chấm, rau sống...): luôn đi kèm món khác nên không bỏ ảnh được; thay vào đó
     ghi class_drop.json p(c)=1-cap/f_rfs(c) để RandomSamplingNegPos2 bỏ lớp đó khỏi giám sát
     (box + tên trong prompt) với xác suất p(c) mỗi lần lấy mẫu.
6. Xuất ODVG (mode OD), label_map, COCO val/test và báo cáo thống kê.

Ví dụ:
    python scripts/vifood54/build_vifood54.py --head-cap 400
"""

import argparse
import collections
import json
import math
import os
import random
import re
import zipfile

import numpy as np
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERE = os.path.dirname(os.path.abspath(__file__))

# (tên nguồn, zip CVAT, thư mục ảnh tương đối root). Ổ CIFS không hỗ trợ symlink nên
# `filename` trong annotation là đường dẫn tương đối từ root dự án (data_root = root).
# Ảnh vifood được giải nén từ zip/images.zip (chỉ ảnh có file label).
DEFAULT_SOURCES = [
    ('vifood', 'zip/vifood.zip', 'grounding_data/vifood54/images/vifood'),
    ('vifood2999', 'zip/vifood2999.zip', 'vifood_2999_extracted'),
]


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--root', default=ROOT, help='Thư mục gốc dự án SoPSoP')
    p.add_argument('--taxonomy', default=os.path.join(HERE, 'taxonomy.json'))
    p.add_argument('--out', default='grounding_data/vifood54', help='Thư mục đầu ra (tương đối root)')
    p.add_argument('--val-ratio', type=float, default=0.1)
    p.add_argument('--test-ratio', type=float, default=0.1)
    p.add_argument('--head-cap', type=int, default=400,
                   help='Số ảnh/epoch hiệu dụng mong muốn cho lớp đầu (class dropout); 0 = tắt')
    p.add_argument('--dhash-thr', type=int, default=4, help='Ngưỡng Hamming dHash để coi là ảnh gần trùng')
    p.add_argument('--repeat-thr', type=float, default=0.05,
                   help='Ngưỡng tần suất ảnh t cho repeat factor sampling (lớp có f(c) < t được lặp)')
    p.add_argument('--seed', type=int, default=2026)
    p.add_argument('--keep-split', default='grounding_data/vifood54/annotations/split_manifest.json',
                   help='split_manifest của lần build trước: ảnh cũ giữ split (rỗng = chia lại từ đầu)')
    return p.parse_args()


# ───────────────────────────── taxonomy ─────────────────────────────

def load_taxonomy(path):
    with open(path, encoding='utf-8') as f:
        tax = json.load(f)
    classes = tax['classes']
    name_to_id = {c['name']: i for i, c in enumerate(classes)}
    merge = tax.get('merge_into', {})
    validate_taxonomy(tax)
    src_to_id = {}
    for src in tax['source_names']:
        target = merge.get(src, src)
        if target not in name_to_id:
            raise ValueError(f'Tên nguồn "{src}" không ánh xạ được vào taxonomy')
        src_to_id[src] = name_to_id[target]
    return tax, classes, src_to_id


REQUIRED = ('id', 'name', 'en', 'aliases', 'group', 'supercategory', 'visual', 'confusable_with',
            'ov_split', 'nutrition_key', 'label_notes')


def validate_taxonomy(tax):
    """Schema v2 (xem tax['schema']): báo lỗi sớm thay vì để lỗi ở bước caption/train."""
    names = [c['name'] for c in tax['classes']]
    assert len(set(names)) == len(names), 'tên lớp trùng'
    for i, c in enumerate(tax['classes']):
        missing = [k for k in REQUIRED if k not in c]
        assert not missing, f'{c["name"]}: thiếu trường {missing}'
        assert c['id'] == i, f'{c["name"]}: id {c["id"]} != vị trí {i}'
        assert c['group'] in ('dish', 'side', 'sauce', 'catch_all'), c['name']
        assert c['supercategory'] in tax['supercategories'], c['name']
        assert c['ov_split'] in ('base', 'novel'), c['name']
        v = c['visual']
        assert v['definition'] and v['units'], c['name']
        assert bool(v['attrs']) == (c['group'] != 'catch_all'), f'{c["name"]}: attrs chỉ để trống cho catch_all'
        for o in c['confusable_with']:
            assert o['name'] in names and o['name'] != c['name'] and o['cue'], f'{c["name"]}: confusable {o}'
        for a in c['aliases']:
            assert a not in names, f'{c["name"]}: alias "{a}" trùng tên lớp khác'


# ───────────────────────────── đọc dữ liệu ─────────────────────────────

def dhash(img, size=8):
    g = img.convert('L').resize((size + 1, size), Image.BILINEAR)
    a = np.asarray(g, dtype=np.int16)
    bits = (a[:, 1:] > a[:, :-1]).flatten()
    return int(''.join('1' if b else '0' for b in bits), 2)


def roboflow_base(stem):
    """srcB_103_jpg.rf.<hash> -> srcB_103 ; ảnh thường giữ nguyên."""
    return re.sub(r'(_jpg|_jpeg|_png)?\.rf\.[0-9a-f]{16,}$', '', stem)


def load_sources(root, sources, tax, src_to_id):
    records = []
    dropped_total = collections.Counter()
    for src_name, zip_rel, img_rel in sources:
        zf = zipfile.ZipFile(os.path.join(root, zip_rel))
        names = [l.strip() for l in zf.read('obj.names').decode('utf-8').splitlines() if l.strip()]
        if names != tax['source_names']:
            raise ValueError(f'{zip_rel}: obj.names khác taxonomy.source_names')
        img_dir = os.path.join(root, img_rel)
        lines = [l.strip() for l in zf.read('train.txt').decode('utf-8').splitlines() if l.strip()]
        label_files = {n for n in zf.namelist() if n.startswith('obj_train_data/') and n.endswith('.txt')}
        skipped = collections.Counter()
        for line in lines:
            fname = os.path.basename(line)
            stem = os.path.splitext(fname)[0]
            label_name = f'obj_train_data/{stem}.txt'
            if label_name not in label_files:
                skipped['no_label'] += 1
                continue
            img_path = os.path.join(img_dir, fname)
            with Image.open(img_path) as im:
                exif_rotated = im.getexif().get(0x0112, 1) not in (1, None)
                im = ImageOps.exif_transpose(im)
                w, h = im.size
                hsh = dhash(im)
            boxes = []
            for ann in zf.read(label_name).decode('utf-8').splitlines():
                parts = ann.split()
                # dòng '# DELETED ...' do crops_review đánh dấu box bị xóa
                if len(parts) < 5 or parts[0].startswith('#'):
                    continue
                cid = src_to_id[names[int(parts[0])]]
                cx, cy, bw, bh = map(float, parts[1:5])
                x1 = max(0.0, (cx - bw / 2) * w)
                y1 = max(0.0, (cy - bh / 2) * h)
                x2 = min(float(w), (cx + bw / 2) * w)
                y2 = min(float(h), (cy + bh / 2) * h)
                if x2 - x1 < 1 or y2 - y1 < 1:
                    continue
                boxes.append({'bbox': [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)], 'label': cid})
            if not boxes:
                skipped['empty_label'] += 1  # ảnh đã lọc bỏ, không dùng làm negative
                continue
            records.append({
                'source': src_name,
                'filename': f'{img_rel}/{fname}',
                'width': w, 'height': h,
                'exif_rotated': exif_rotated,
                'base': f'{src_name}/{roboflow_base(stem)}',
                'dhash': hsh,
                'boxes': boxes,
            })
        kept = sum(1 for r in records if r['source'] == src_name)
        print(f'  {src_name}: {len(lines)} ảnh trong train.txt -> giữ {kept}, bỏ {dict(skipped)}')
        dropped_total.update({f'{src_name}:{k}': v for k, v in skipped.items()})
    return records, dropped_total


# ───────────────────────────── nhóm ảnh gốc ─────────────────────────────

def build_groups(records, dhash_thr):
    parent = list(range(len(records)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i, j):
        pi, pj = find(i), find(j)
        if pi != pj:
            parent[pj] = pi

    by_base = collections.defaultdict(list)
    for i, r in enumerate(records):
        by_base[r['base']].append(i)
    for idxs in by_base.values():
        for j in idxs[1:]:
            union(idxs[0], j)

    hashes = np.array([r['dhash'] for r in records], dtype=np.uint64)
    near_pairs = 0
    for i in range(len(records)):
        x = np.bitwise_xor(hashes[i + 1:], hashes[i])
        dist = np.unpackbits(x.view(np.uint8).reshape(-1, 8), axis=1).sum(axis=1)
        for k in np.nonzero(dist <= dhash_thr)[0]:
            union(i, i + 1 + int(k))
            near_pairs += 1

    groups = collections.defaultdict(list)
    for i in range(len(records)):
        groups[find(i)].append(i)
    gid_of = {}
    for gid, (_, idxs) in enumerate(sorted(groups.items())):
        for i in idxs:
            gid_of[i] = gid
    for i, r in enumerate(records):
        r['group'] = gid_of[i]
    return near_pairs


# ───────────────────────────── chia split ─────────────────────────────

def stratified_group_split(records, num_classes, ratios, seed, prior=None):
    """Gán cả group vào split; group chứa lớp hiếm được xếp trước, chọn split thiếu nhiều nhất.

    prior: {filename: split} của lần build trước. Group có ảnh đã chia giữ split cũ (đa số), để
    sửa nhãn không làm ảnh train cũ rơi vào test mới; chỉ group mới được chia theo tầng.
    """
    rng = random.Random(seed)
    groups = collections.defaultdict(list)
    for i, r in enumerate(records):
        groups[r['group']].append(i)
    fixed = {}
    for gid, idxs in groups.items():
        old = collections.Counter(prior[records[i]['filename']] for i in idxs
                                  if prior and records[i]['filename'] in prior)
        if old:
            fixed[gid] = old.most_common(1)[0][0]

    def class_counts(idxs):
        c = collections.Counter()
        for i in idxs:
            for k in {b['label'] for b in records[i]['boxes']}:
                c[k] += 1
        return c

    total = class_counts(range(len(records)))
    group_items = []
    for gid, idxs in groups.items():
        cc = class_counts(idxs)
        rarity = min((total[k] for k in cc), default=10 ** 9)
        group_items.append((rarity, rng.random(), gid, idxs, cc))
    group_items.sort(key=lambda x: (x[0], x[1]))

    split_names = list(ratios)
    target = {s: {k: total[k] * ratios[s] for k in range(num_classes)} for s in split_names}
    have = {s: collections.Counter() for s in split_names}

    for _, _, gid, idxs, cc in group_items:
        if gid in fixed:
            for k, v in cc.items():
                have[fixed[gid]][k] += v
            for i in idxs:
                records[i]['split'] = fixed[gid]
    for _, _, gid, idxs, cc in group_items:
        if gid in fixed:
            continue

        def score(s):
            # deficit tương đối, lớp hiếm có trọng số lớn hơn
            return sum((target[s][k] - have[s][k]) / max(target[s][k], 1e-6) / math.sqrt(total[k])
                       for k in cc)
        best = max(split_names, key=lambda s: (score(s), ratios[s]))
        for k, v in cc.items():
            have[best][k] += v
        for i in idxs:
            records[i]['split'] = best


# ───────────────────────────── cân bằng train ─────────────────────────────

def class_drop_probs(train_rfs, cap):
    """p(c) = 1 - cap / số ảnh chứa c sau RFS, chỉ cho lớp vượt cap."""
    if cap <= 0:
        return {}
    freq = collections.Counter()
    for r in train_rfs:
        for k in {b['label'] for b in r['boxes']}:
            freq[k] += 1
    return {k: round(1 - cap / v, 3) for k, v in sorted(freq.items()) if v > cap}


def repeat_factors(train, num_classes, thr):
    n = len(train)
    freq = collections.Counter()
    for r in train:
        for k in {b['label'] for b in r['boxes']}:
            freq[k] += 1
    cat_rep = {k: max(1.0, math.sqrt(thr / (freq[k] / n))) for k in freq}
    img_rep = [max([cat_rep[b['label']] for b in r['boxes']], default=1.0) for r in train]
    return cat_rep, img_rep


# ───────────────────────────── xuất file ─────────────────────────────

def to_odvg(r, classes):
    instances = [{'bbox': b['bbox'], 'label': b['label'], 'category': classes[b['label']]['name']}
                 for b in r['boxes']]
    names = list(dict.fromkeys(classes[b['label']]['name'] for b in r['boxes']))
    short = ' . '.join(names) + ' .' if names else ''
    return {
        'filename': r['filename'],
        'height': r['height'],
        'width': r['width'],
        'group': r['group'],
        'detection': {'instances': instances},
        # RandomSamplingNegPos2 luôn đọc conversations; với lmm=None trường này không vào loss
        'conversations': [
            {'from': 'human', 'value': '<image>\nDescribe the image in detail.'},
            {'from': 'gpt', 'value': short},
        ],
    }


def to_coco(records, classes):
    images, anns = [], []
    for img_id, r in enumerate(records):
        images.append({'id': img_id, 'file_name': r['filename'], 'width': r['width'], 'height': r['height']})
        for b in r['boxes']:
            x1, y1, x2, y2 = b['bbox']
            w, h = round(x2 - x1, 2), round(y2 - y1, 2)
            anns.append({'id': len(anns) + 1, 'image_id': img_id, 'category_id': b['label'],
                         'bbox': [x1, y1, w, h], 'area': round(w * h, 2), 'iscrowd': 0})
    cats = [{'id': i, 'name': c['name'], 'supercategory': c['group']} for i, c in enumerate(classes)]
    return {'images': images, 'annotations': anns, 'categories': cats}


def write_jsonl(path, rows):
    with open(path, 'w', encoding='utf-8') as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + '\n')


def class_table(classes, splits):
    """Bảng (#ảnh / #box) theo lớp cho từng split."""
    header = '| id | class | ' + ' | '.join(f'{s} img/box' for s in splits) + ' |'
    lines = [header, '|' + '---|' * (2 + len(splits))]
    stats = {}
    for s, recs in splits.items():
        img_c, box_c = collections.Counter(), collections.Counter()
        for r in recs:
            for b in r['boxes']:
                box_c[b['label']] += 1
            for k in {b['label'] for b in r['boxes']}:
                img_c[k] += 1
        stats[s] = (img_c, box_c)
    for i, c in enumerate(classes):
        cells = ' | '.join(f'{stats[s][0][i]}/{stats[s][1][i]}' for s in splits)
        lines.append(f'| {i} | {c["name"]} | {cells} |')
    return '\n'.join(lines), stats


def with_stats(tax, splits):
    """Bản taxonomy xuất kèm dữ liệu: thêm `stats` (số ảnh/box mỗi split) vào từng lớp."""
    out = json.loads(json.dumps(tax))
    for c in out['classes']:
        c['stats'] = {}
    for s, rs in splits.items():
        for c in out['classes']:
            c['stats'][s] = {'images': 0, 'boxes': 0}
        for r in rs:
            labels = [b['label'] for b in r['boxes']]
            for k in set(labels):
                out['classes'][k]['stats'][s]['images'] += 1
            for k in labels:
                out['classes'][k]['stats'][s]['boxes'] += 1
    return out


def main():
    args = parse_args()
    root = os.path.abspath(args.root)
    out_dir = os.path.join(root, args.out)
    ann_dir = os.path.join(out_dir, 'annotations')
    os.makedirs(ann_dir, exist_ok=True)

    tax, classes, src_to_id = load_taxonomy(args.taxonomy)
    print(f'Taxonomy: {len(tax["source_names"])} tên nguồn -> {len(classes)} class')

    print('Đọc nhãn & ảnh...')
    records, skipped = load_sources(root, DEFAULT_SOURCES, tax, src_to_id)
    near_pairs = build_groups(records, args.dhash_thr)
    n_groups = len({r['group'] for r in records})
    print(f'  {len(records)} ảnh, {n_groups} ảnh gốc (group), {near_pairs} cặp gần trùng dHash')

    prior = None
    keep = os.path.join(root, args.keep_split) if args.keep_split else ''
    if keep and os.path.exists(keep):
        with open(keep, encoding='utf-8') as f:
            prior = {k: v['split'] for k, v in json.load(f).items()}
        n_old = sum(r['filename'] in prior for r in records)
        print(f'  Giữ split cũ ({keep}): {n_old}/{len(records)} ảnh đã có split')
    ratios = {'train': 1 - args.val_ratio - args.test_ratio, 'val': args.val_ratio, 'test': args.test_ratio}
    stratified_group_split(records, len(classes), ratios, args.seed, prior)
    splits = {s: [r for r in records if r['split'] == s] for s in ratios}
    for s in ('val', 'test'):
        assert not ({r['group'] for r in splits[s]} & {r['group'] for r in splits['train']})

    train = splits['train']
    cat_rep, img_rep = repeat_factors(train, len(classes), args.repeat_thr)

    # ── ghi file ──
    write_jsonl(os.path.join(ann_dir, 'train_od.jsonl'), [to_odvg(r, classes) for r in train])
    # file train đã nhân bản theo repeat factor (làm tròn ngẫu nhiên, cố định theo seed)
    rng = random.Random(args.seed)
    train_rfs = []
    for r, rep in zip(train, img_rep):
        n = int(math.floor(rep)) + (1 if rng.random() < rep - math.floor(rep) else 0)
        train_rfs.extend([r] * n)
    write_jsonl(os.path.join(ann_dir, 'train_od_rfs.jsonl'), [to_odvg(r, classes) for r in train_rfs])
    drop_prob = class_drop_probs(train_rfs, args.head_cap)
    with open(os.path.join(ann_dir, 'class_drop.json'), 'w', encoding='utf-8') as f:
        json.dump({str(k): v for k, v in drop_prob.items()}, f, indent=2)
    for s in ('val', 'test'):
        write_jsonl(os.path.join(ann_dir, f'{s}_od.jsonl'), [to_odvg(r, classes) for r in splits[s]])
        with open(os.path.join(ann_dir, f'instances_{s}.json'), 'w', encoding='utf-8') as f:
            json.dump(to_coco(splits[s], classes), f, ensure_ascii=False)

    # label_map cho train: chỉ tên lớp. (RandomSamplingNegPos2 hiểu 'a/b' là chọn ngẫu nhiên một tên;
    # alias trong taxonomy dành cho app/OV, không trộn vào prompt train để giữ công thức B1.)
    label_map = {str(i): c['name'] for i, c in enumerate(classes)}
    with open(os.path.join(ann_dir, 'label_map.json'), 'w', encoding='utf-8') as f:
        json.dump(label_map, f, ensure_ascii=False, indent=2)
    with open(os.path.join(ann_dir, 'taxonomy.json'), 'w', encoding='utf-8') as f:
        json.dump(with_stats(tax, splits), f, ensure_ascii=False, indent=1)

    manifest = {r['filename']: {'split': r['split'], 'group': r['group'], 'base': r['base']}
                for r in records}
    with open(os.path.join(ann_dir, 'split_manifest.json'), 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=1)

    # ── báo cáo ──
    table, stats = class_table(classes, {'train': train, 'train_rfs': train_rfs,
                                         'val': splits['val'], 'test': splits['test']})
    eff = {k: round(stats['train_rfs'][0][k] * (1 - drop_prob.get(k, 0))) for k in range(len(classes))}
    drop_lines = ['| class | ảnh train_rfs | p drop | ảnh hiệu dụng/epoch |', '|---|---|---|---|']
    for k, p in drop_prob.items():
        drop_lines.append(f'| {classes[k]["name"]} | {stats["train_rfs"][0][k]} | {p} | {eff[k]} |')
    eff_sorted = sorted(eff.values())
    rep_lines = ['| class | train img | repeat factor |', '|---|---|---|']
    for k in sorted(cat_rep, key=lambda k: -cat_rep[k]):
        if cat_rep[k] > 1.0:
            rep_lines.append(f'| {classes[k]["name"]} | {stats["train"][0][k]} | {cat_rep[k]:.2f} |')
    n_exif = sum(r['exif_rotated'] for r in records)

    report = f"""# ViFood-54 — báo cáo build

- Taxonomy: {len(tax['source_names'])} tên nguồn → **{len(classes)} class** (gộp: {tax.get('merge_into')})
- Tổng: {len(records)} ảnh, {sum(len(r['boxes']) for r in records)} box, **{n_groups} ảnh gốc** (group), {near_pairs} cặp gần trùng dHash (≤{args.dhash_thr})
- Ảnh bị bỏ (không có label / label rỗng): {dict(skipped)}
- Ảnh có EXIF xoay: {n_exif} (kích thước đã tính sau khi xoay)
- Split theo group (seed={args.seed}): train {len(train)} ảnh / val {len(splits['val'])} / test {len(splits['test'])}
- Oversample lớp hiếm (repeat_thr={args.repeat_thr}, làm tròn ngẫu nhiên): `train_od_rfs.jsonl` = **{len(train_rfs)} mẫu/epoch**
- Class dropout lớp đầu (head_cap={args.head_cap}): `class_drop.json`; số ảnh hiệu dụng/lớp/epoch min {eff_sorted[0]}, median {eff_sorted[len(eff_sorted) // 2]}, max {eff_sorted[-1]}

## Số ảnh/box theo lớp
{table}

## Class dropout (lớp đầu)
{chr(10).join(drop_lines)}

## Repeat factor (lớp hiếm)
{chr(10).join(rep_lines)}
"""
    with open(os.path.join(out_dir, 'BUILD_REPORT.md'), 'w', encoding='utf-8') as f:
        f.write(report)
    print(report)


if __name__ == '__main__':
    main()
