#!/usr/bin/env python3
"""
AP_base / AP_novel trên test ViFood-54 (prompt đủ 54 lớp, kiểu generalized open-vocabulary).

    python scripts/vifood54/eval_ov.py --pred B0=.../preds.pkl --pred OV_S1=.../preds.pkl ...
"""
import argparse
import json
import os
import sys

import numpy as np
from pycocotools.coco import COCO

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from analyze_eval import coco_eval, load_dets, per_class_ap  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--gt', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations/instances_test.json'))
    p.add_argument('--ov', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations_ov/ov_classes.json'))
    p.add_argument('--pred', action='append', required=True, help='TÊN=preds.pkl (TÊN có "*" = đã thấy lớp novel khi train)')
    p.add_argument('--out', default=os.path.join(ROOT, 'grounding_data/vifood54/EVAL_OV.md'))
    args = p.parse_args()

    import contextlib
    import io
    with contextlib.redirect_stdout(io.StringIO()):
        gt = COCO(args.gt)
    names = {c['id']: c['name'] for c in gt.loadCats(gt.getCatIds())}
    novel = json.load(open(args.ov, encoding='utf-8'))['novel_ids']
    base = [c for c in gt.getCatIds() if c not in novel]

    def ap_subset(dets, cats):
        ev = coco_eval(gt, dets) if cats is None else None
        if cats is not None:
            from pycocotools.cocoeval import COCOeval
            with contextlib.redirect_stdout(io.StringIO()):
                ev = COCOeval(gt, gt.loadRes(dets), 'bbox')
                ev.params.catIds = cats
                ev.evaluate()
                ev.accumulate()
                ev.summarize()
        return ev

    rows, novel_rows = [], {}
    for spec in args.pred:
        name, path = spec.split('=', 1)
        dets = load_dets(path)
        ev_all = ap_subset(dets, None)
        ev_b = ap_subset(dets, base)
        ev_n = ap_subset(dets, novel)
        rows.append((name, ev_all.stats[0], ev_b.stats[0], ev_n.stats[0], ev_n.stats[1], ev_n.stats[8]))
        novel_rows[name] = per_class_ap(ev_n, novel)

    L = ['# Open-vocabulary trên test ViFood-54', '',
         f'- Novel ({len(novel)}): ' + ', '.join(names[i] for i in novel),
         f'- Base: {len(base)} lớp. Prompt test đủ 54 tên (generalized): lớp novel phải thắng cả lớp base trong prompt.',
         '- `*` = đã thấy lớp novel khi train (không phải OV, chỉ để làm trần trên).', '',
         '| Mô hình | mAP (54) | AP_base | AP_novel | AP50_novel | AR@100_novel |',
         '|---|---|---|---|---|---|']
    for name, a, b, n, n50, nar in rows:
        L.append(f'| {name} | {a:.3f} | {b:.3f} | {n:.3f} | {n50:.3f} | {nar:.3f} |')
    L += ['', '## AP theo lớp novel (AP / AP50)', '', '| lớp | ' + ' | '.join(novel_rows) + ' |',
          '|---|' + '---|' * len(novel_rows)]
    for c in novel:
        L.append(f'| {names[c]} | ' + ' | '.join(f'{novel_rows[m][c][0]:.3f} / {novel_rows[m][c][1]:.3f}'
                                                  for m in novel_rows) + ' |')
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
