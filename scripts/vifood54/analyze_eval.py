#!/usr/bin/env python3
"""
scripts/vifood54/analyze_eval.py
================================
Phân tích kết quả test của một hoặc nhiều mô hình (file preds.pkl do `mmdet_test.py --out` tạo).

Xuất (Markdown):
  - mAP / AP50 tổng và AP, AP50 theo lớp (pycocotools);
  - khoảng tin cậy 95% của mAP bằng bootstrap theo ảnh;
  - ma trận nhầm lẫn: với mỗi GT, dự đoán score >= --score-thr có IoU lớn nhất (>= --iou-thr)
    thuộc lớp nào; top cặp nhầm và các cặp cần theo dõi (giống hình / dính chữ sau khi BERT bỏ dấu).

    python scripts/vifood54/analyze_eval.py \
        --gt grounding_data/vifood54/annotations/instances_test.json \
        --pred B0=llmdet_vietnamese_food/work_dirs/vifood54_b0_zeroshot_test/preds.pkl \
        --pred B1=llmdet_vietnamese_food/work_dirs/vifood54_b1_od_test/preds.pkl \
        --out grounding_data/vifood54/EVAL_B0_B1.md
"""
import argparse
import collections
import contextlib
import io
import os
import pickle

import numpy as np
from pycocotools.coco import COCO
from pycocotools.cocoeval import COCOeval

# cặp cần theo dõi: (a, b, lý do)
WATCH_PAIRS = [
    ('chả giò', 'nem rán', 'giống hình'),
    ('bánh căn', 'bánh khọt', 'giống hình'),
    ('bánh bèo', 'bánh bột lọc', 'giống hình'),
    ('gỏi', 'gỏi cuốn', 'giống hình + lồng chữ'),
    ('quẩy', 'gà quay', 'dính chữ (quay)'),
    ('quẩy', 'heo quay', 'dính chữ (quay)'),
    ('lẩu', 'cao lầu', 'dính chữ (lau)'),
    ('bánh căn', 'bánh canh', 'dính chữ (can)'),
    ('canh', 'bánh canh', 'lồng chữ'),
    ('cua', 'súp cua', 'lồng chữ'),
    ('tôm', 'bún đậu mắm tôm', 'lồng chữ'),
    ('cá chiên', 'cơm chiên', 'gần trùng chữ'),
    ('mực', 'ốc', 'gần trùng chữ'),
    ('lẩu', 'tôm', 'gần trùng chữ'),
]


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--gt', required=True)
    p.add_argument('--pred', action='append', required=True, help='TÊN=đường_dẫn_preds.pkl')
    p.add_argument('--out', required=True)
    p.add_argument('--score-thr', type=float, default=0.3)
    p.add_argument('--iou-thr', type=float, default=0.5)
    p.add_argument('--bootstrap', type=int, default=200)
    p.add_argument('--seed', type=int, default=0)
    return p.parse_args()


def load_dets(path):
    """preds.pkl -> list COCO detections (bbox xywh, category_id = label)."""
    with open(path, 'rb') as f:
        preds = pickle.load(f)
    dets = []
    for r in preds:
        inst = r['pred_instances']
        for b, s, l in zip(inst['bboxes'].tolist(), inst['scores'].tolist(), inst['labels'].tolist()):
            dets.append({'image_id': int(r['img_id']), 'category_id': int(l),
                         'bbox': [b[0], b[1], b[2] - b[0], b[3] - b[1]], 'score': float(s)})
    return dets


def coco_eval(gt, dets, img_ids=None):
    with contextlib.redirect_stdout(io.StringIO()):
        dt = gt.loadRes(dets) if dets else COCO()
        ev = COCOeval(gt, dt, 'bbox')
        if img_ids is not None:
            ev.params.imgIds = img_ids
        ev.evaluate()
        ev.accumulate()
        ev.summarize()
    return ev


def per_class_ap(ev, cat_ids):
    prec = ev.eval['precision']  # [T, R, K, A, M]
    out = {}
    for k, cid in enumerate(cat_ids):
        p = prec[:, :, k, 0, -1]
        p50 = prec[0, :, k, 0, -1]
        out[cid] = (float(np.mean(p[p > -1])) if (p > -1).any() else float('nan'),
                    float(np.mean(p50[p50 > -1])) if (p50 > -1).any() else float('nan'))
    return out


def bootstrap_map(gt, dets, n, seed):
    """Bootstrap theo ảnh: lấy mẫu có hoàn lại ảnh, đánh giá lại (đổi id để ảnh lặp được tính riêng)."""
    rng = np.random.default_rng(seed)
    img_ids = gt.getImgIds()
    by_img = collections.defaultdict(list)
    for d in dets:
        by_img[d['image_id']].append(d)
    vals = []
    for _ in range(n):
        pick = rng.choice(img_ids, size=len(img_ids), replace=True)
        images, anns, ds = [], [], []
        for new_id, old_id in enumerate(pick):
            images.append({**gt.imgs[old_id], 'id': new_id})
            for a in gt.imgToAnns[old_id]:
                anns.append({**a, 'id': len(anns) + 1, 'image_id': new_id})
            ds.extend({**d, 'image_id': new_id} for d in by_img[old_id])
        g = COCO()
        g.dataset = {'images': images, 'annotations': anns, 'categories': gt.dataset['categories']}
        with contextlib.redirect_stdout(io.StringIO()):
            g.createIndex()
        vals.append(coco_eval(g, ds).stats[0])
    return np.percentile(vals, [2.5, 97.5])


def iou(box, boxes):
    x1 = np.maximum(box[0], boxes[:, 0]); y1 = np.maximum(box[1], boxes[:, 1])
    x2 = np.minimum(box[0] + box[2], boxes[:, 0] + boxes[:, 2])
    y2 = np.minimum(box[1] + box[3], boxes[:, 1] + boxes[:, 3])
    inter = np.clip(x2 - x1, 0, None) * np.clip(y2 - y1, 0, None)
    return inter / (box[2] * box[3] + boxes[:, 2] * boxes[:, 3] - inter + 1e-9)


def confusion(gt, dets, score_thr, iou_thr):
    """conf[gt_cat][pred_cat] = số GT có dự đoán tốt nhất (IoU lớn nhất) thuộc pred_cat; -1 = bỏ sót."""
    by_img = collections.defaultdict(list)
    for d in dets:
        if d['score'] >= score_thr:
            by_img[d['image_id']].append(d)
    conf = collections.defaultdict(collections.Counter)
    for img_id in gt.getImgIds():
        ds = by_img[img_id]
        boxes = np.array([d['bbox'] for d in ds]) if ds else np.zeros((0, 4))
        for a in gt.imgToAnns[img_id]:
            if not len(boxes):
                conf[a['category_id']][-1] += 1
                continue
            ious = iou(np.array(a['bbox']), boxes)
            j = int(np.argmax(ious))
            conf[a['category_id']][ds[j]['category_id'] if ious[j] >= iou_thr else -1] += 1
    return conf


def main():
    args = parse_args()
    with contextlib.redirect_stdout(io.StringIO()):
        gt = COCO(args.gt)
    cats = {c['id']: c['name'] for c in gt.dataset['categories']}
    name2id = {v: k for k, v in cats.items()}
    cat_ids = sorted(cats)
    n_gt = collections.Counter(a['category_id'] for a in gt.dataset['annotations'])

    runs = {}
    for spec in args.pred:
        name, path = spec.split('=', 1)
        dets = load_dets(path)
        ev = coco_eval(gt, dets)
        runs[name] = {
            'stats': ev.stats,
            'per_class': per_class_ap(ev, cat_ids),
            'ci': bootstrap_map(gt, dets, args.bootstrap, args.seed) if args.bootstrap else None,
            'conf': confusion(gt, dets, args.score_thr, args.iou_thr),
        }
        print(f'{name}: mAP {ev.stats[0]:.3f} AP50 {ev.stats[1]:.3f}')

    names = list(runs)
    L = [f'# Đánh giá trên `{os.path.basename(args.gt)}` ({len(gt.getImgIds())} ảnh, '
         f'{len(gt.dataset["annotations"])} box, {len(cats)} lớp)', '']
    L += ['## Tổng', '', '| Mô hình | mAP | 95% CI (bootstrap ảnh) | AP50 | AP75 | AP_s | AP_m | AP_l | AR@100 |',
          '|---|---|---|---|---|---|---|---|---|']
    for n in names:
        s, ci = runs[n]['stats'], runs[n]['ci']
        ci_s = f'{ci[0]:.3f}–{ci[1]:.3f}' if ci is not None else '-'
        L.append(f'| {n} | {s[0]:.3f} | {ci_s} | {s[1]:.3f} | {s[2]:.3f} | {s[3]:.3f} | {s[4]:.3f} | {s[5]:.3f} | {s[8]:.3f} |')

    last = names[-1]
    L += ['', f'## AP theo lớp (sắp theo AP của {last}, tăng dần)', '',
          '| lớp | #GT test | ' + ' | '.join(f'{n} AP / AP50' for n in names) + ' |',
          '|---|---|' + '---|' * len(names)]
    for cid in sorted(cat_ids, key=lambda c: runs[last]['per_class'][c][0]):
        cells = ' | '.join(f'{runs[n]["per_class"][cid][0]:.3f} / {runs[n]["per_class"][cid][1]:.3f}' for n in names)
        L.append(f'| {cats[cid]} | {n_gt[cid]} | {cells} |')

    for n in names:
        conf = runs[n]['conf']
        pairs = []
        for g, row in conf.items():
            for p, c in row.items():
                if p not in (-1, g):
                    pairs.append((c, cats[g], cats[p], c / sum(row.values())))
        pairs.sort(reverse=True)
        L += ['', f'## {n}: nhầm lẫn (score ≥ {args.score_thr}, IoU ≥ {args.iou_thr})', '',
              '| GT | dự đoán thành | số box | % GT của lớp |', '|---|---|---|---|']
        for c, g, p, r in pairs[:20]:
            L.append(f'| {g} | {p} | {c} | {r:.0%} |')
        L += ['', f'### {n}: cặp theo dõi', '', '| cặp | lý do | a→b | b→a | bỏ sót a | bỏ sót b |', '|---|---|---|---|---|---|']
        for a, b, why in WATCH_PAIRS:
            ia, ib = name2id[a], name2id[b]
            ra, rb = conf.get(ia, collections.Counter()), conf.get(ib, collections.Counter())
            ta, tb = max(sum(ra.values()), 1), max(sum(rb.values()), 1)
            L.append(f'| {a} ↔ {b} | {why} | {ra[ib]}/{ta} | {rb[ia]}/{tb} | {ra[-1]}/{ta} | {rb[-1]}/{tb} |')

    with open(args.out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('->', args.out)


if __name__ == '__main__':
    main()
