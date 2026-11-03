#!/usr/bin/env python3
"""
Đánh giá grounding câu tự nhiên trên test ViFood-54 (chỉ inference, plan mục 7.3 + 7.5).

Mỗi ảnh test, mỗi kiểu prompt, model nhận caption + tokens_positive của từng tên món trong câu
(1 entity = 1 lớp có mặt) và phải khoanh box cho từng entity. Đo theo entity:
  - R@1: box điểm cao nhất của entity trùng (IoU ≥ 0.5) một box GT của lớp đó;
  - R@n: lớp có n box GT, lấy n box điểm cao nhất, ghép tham lam -> tỉ lệ box GT được tìm thấy.

Kiểu prompt (đều chỉ chứa lớp có mặt, không negative):
  names     'phở. rau sống.'                   — mốc: chỉ tên món
  L1        caption liệt kê có đếm             — 2 biến thể / ảnh
  L2        caption hình thái + vị trí         — 4 biến thể / ảnh
  L2_taste  L2 chèn thêm cụm hương vị cuối mỗi câu (model không thể nhìn thấy) — cùng 4 biến thể

    cd llmdet_vietnamese_food
    PYTHONPATH=. python ../scripts/vifood54/eval_grounding.py --model B1_v2=work_dirs/.../best.pth ...
"""
import argparse
import collections
import json
import os
import random

import numpy as np
import torch
from mmdet.apis import init_detector
from mmengine.dataset import Compose, pseudo_collate

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
TASTE = ['thơm ngon', 'vị đậm đà', 'ngọt thanh', 'béo ngậy', 'nóng hổi', 'cay nồng', 'hấp dẫn']


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--config', default='configs/grounding_dino_swin_t_vifood54_b1_od.py')
    p.add_argument('--model', action='append', required=True, help='TÊN=checkpoint.pth')
    p.add_argument('--ann', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations/test_vg_cap.jsonl'))
    p.add_argument('--out', default=os.path.join(ROOT, 'grounding_data/vifood54/EVAL_GROUNDING.md'))
    p.add_argument('--limit', type=int, default=0, help='chỉ lấy N ảnh đầu (thử nhanh)')
    p.add_argument('--seed', type=int, default=0)
    return p.parse_args()


def entities_from_regions(caption, regions):
    """-> (tokens_positive theo entity, nhãn lớp của entity, GT box theo entity)."""
    spans, boxes = {}, collections.defaultdict(list)
    for r in regions:
        s, e = r['tokens_positive'][0]
        spans[r['phrase']] = (s, e)
        boxes[r['phrase']].append(r['bbox'])
    names = list(spans)
    assert all(caption[spans[n][0]:spans[n][1]] == n for n in names)
    return [[list(spans[n])] for n in names], names, [boxes[n] for n in names]


def names_prompt(regions):
    names = list(dict.fromkeys(r['phrase'] for r in regions))
    text, tp = '', []
    for n in names:
        tp.append([[len(text), len(text) + len(n)]])
        text += n + '. '
    boxes = [[r['bbox'] for r in regions if r['phrase'] == n] for n in names]
    return text.strip(), tp, names, boxes


def add_taste(caption, tokens_positive, rng):
    """Chèn ', <hương vị>' trước dấu chấm kết thúc mỗi câu; dời span phía sau cho đúng."""
    out, shift, inserts = [], 0, []
    for i, ch in enumerate(caption):
        if ch == '.':
            ins = ', ' + rng.choice(TASTE)
            out.append(ins)
            inserts.append((i, len(ins)))
        out.append(ch)
    text = ''.join(out)

    def moved(x):
        return x + sum(k for p, k in inserts if p < x)

    return text, [[[moved(s), moved(e)] for s, e in ent] for ent in tokens_positive]


def iou(a, b):
    ix = max(0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / u if u > 0 else 0.0


def score_entities(pred, gts_by_entity):
    """pred: InstanceData (bboxes, scores, labels = chỉ số entity). -> list (hit@1, found, n_gt)."""
    boxes = pred.bboxes.cpu().numpy()
    scores = pred.scores.cpu().numpy()
    labels = pred.labels.cpu().numpy()
    res = []
    for j, gts in enumerate(gts_by_entity):
        idx = np.where(labels == j)[0]
        idx = idx[np.argsort(-scores[idx])]
        hit1 = bool(len(idx)) and max(iou(boxes[idx[0]], g) for g in gts) >= 0.5
        used, found = set(), 0
        for k in idx[:len(gts)]:
            best = max(((iou(boxes[k], g), gi) for gi, g in enumerate(gts) if gi not in used), default=(0, -1))
            if best[0] >= 0.5:
                used.add(best[1])
                found += 1
        res.append((hit1, found, len(gts)))
    return res


def main():
    args = parse_args()
    rows = [json.loads(l) for l in open(args.ann, encoding='utf-8')]
    if args.limit:
        rows = rows[:args.limit]

    # dựng toàn bộ prompt một lần (giống nhau cho mọi model)
    rng = random.Random(args.seed)
    jobs = []  # (kiểu, ảnh, text, tokens_positive, tên entity, GT box)
    for r in rows:
        img = os.path.join(ROOT, r['filename'])
        regions = r['grounding']['variants'][0]['regions']
        t, tp, names, boxes = names_prompt(regions)
        jobs.append(('names', img, t, tp, names, boxes))
        for v in r['grounding']['variants']:
            tp, names, boxes = entities_from_regions(v['caption'], v['regions'])
            jobs.append((v['level'], img, v['caption'], tp, names, boxes))
            if v['level'] == 'L2':
                t2, tp2 = add_taste(v['caption'], tp, rng)
                assert all(t2[s:e] == n for (s, e), n in zip([x[0] for x in tp2], names))
                jobs.append(('L2_taste', img, t2, tp2, names, boxes))
    kinds = ['names', 'L1', 'L2', 'L2_taste']
    print({k: sum(j[0] == k for j in jobs) for k in kinds}, 'prompt')

    results = {}
    per_class = {}
    for spec in args.model:
        name, ckpt = spec.split('=', 1)
        model = init_detector(args.config, ckpt, device='cuda')
        model.eval()
        # pipeline test của config, bỏ LoadAnnotations (không có GT) và giữ tokens_positive trong meta
        steps = [dict(t) for t in model.cfg.test_dataloader.dataset.pipeline if t['type'] != 'LoadAnnotations']
        steps[-1]['meta_keys'] = ('img_id', 'img_path', 'ori_shape', 'img_shape', 'scale_factor',
                                  'text', 'custom_entities', 'tokens_positive')
        pipeline = Compose(steps)
        acc = {k: [] for k in kinds}
        cls = collections.defaultdict(lambda: collections.defaultdict(list))
        for i, (kind, img, text, tp, names, boxes) in enumerate(jobs):
            data = pipeline(dict(img_path=img, img_id=i, text=text, custom_entities=False, tokens_positive=tp))
            with torch.no_grad():
                pred = model.test_step(pseudo_collate([data]))[0].pred_instances
            for n, sc in zip(names, score_entities(pred, boxes)):
                acc[kind].append(sc)
                cls[n][kind].append(sc[0])
            if i % 500 == 0:
                print(f'{name}: {i}/{len(jobs)}', flush=True)
        results[name] = acc
        per_class[name] = cls
        del model
        torch.cuda.empty_cache()

    def r1(xs):
        return np.mean([x[0] for x in xs]) if xs else float('nan')

    def rn(xs):
        return sum(x[1] for x in xs) / max(1, sum(x[2] for x in xs))

    L = ['# Grounding câu tự nhiên trên test ViFood-54 (inference)', '',
         f'- {len(rows)} ảnh test; prompt chỉ chứa lớp có mặt; 1 entity = 1 lớp trong câu. IoU ≥ 0.5.',
         '- R@1: box điểm cao nhất của entity đúng; R@n: tỉ lệ box GT tìm được bằng n box điểm cao nhất (n = số box GT của lớp).',
         f'- Số entity: ' + ', '.join(f'{k} {len(results[next(iter(results))][k])}' for k in kinds), '',
         '| Mô hình | ' + ' | '.join(f'{k} R@1' for k in kinds) + ' | ' + ' | '.join(f'{k} R@n' for k in kinds) + ' |',
         '|---|' + '---|' * (2 * len(kinds))]
    for name, acc in results.items():
        L.append(f'| {name} | ' + ' | '.join(f'{r1(acc[k]):.3f}' for k in kinds) + ' | '
                 + ' | '.join(f'{rn(acc[k]):.3f}' for k in kinds) + ' |')

    L += ['', '## R@1 theo lớp: L2 so với names (lớp ≥ 5 entity test)', '',
          '| lớp | ' + ' | '.join(f'{m} names / L2 / L2_taste' for m in results) + ' |',
          '|---|' + '---|' * len(results)]
    any_m = next(iter(per_class))
    for c in sorted(per_class[any_m], key=lambda c: -len(per_class[any_m][c]['names'])):
        if len(per_class[any_m][c]['names']) < 5:
            continue
        cells = []
        for m in results:
            d = per_class[m][c]
            cells.append(' / '.join(f'{np.mean(d[k]):.2f}' for k in ('names', 'L2', 'L2_taste')))
        L.append(f'| {c} | ' + ' | '.join(cells) + ' |')
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L[:12]))
    print('->', args.out)


if __name__ == '__main__':
    main()
