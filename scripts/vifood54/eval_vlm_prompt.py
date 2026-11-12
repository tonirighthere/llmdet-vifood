#!/usr/bin/env python3
"""
scripts/vifood54/eval_vlm_prompt.py
===================================
Đánh giá end-to-end Bước 1 của pipeline (VLM tự khám phá món) trên test ViFood-54:

  A) VLM liệt kê món đúng tới đâu: precision / recall / F1 của tập món VLM nêu so với tập lớp có trong GT (theo ảnh),
     recall theo lớp, và các món VLM xếp vào "ngoài 54 lớp".
  B) Prompt do VLM chọn có thay được prompt đủ 54 tên không: mAP / AP50 của detector với 3 kiểu prompt
       full54   đủ 54 tên (cách đánh giá chuẩn)
       vlm      chỉ các món VLM nêu (ảnh VLM lỗi hoặc không nêu món nào -> dùng 54 tên)
       oracle   chỉ các lớp có trong GT (trần trên của mọi bộ chọn prompt)

Cần GPU (detector) + API key Gemini (vifood54_vlm.load_api_key). Kết quả VLM được lưu để chạy lại không gọi API nữa.

    cd llmdet_vietnamese_food
    PYTHONPATH=. python ../scripts/vifood54/eval_vlm_prompt.py --limit 20      # thử
    PYTHONPATH=. python ../scripts/vifood54/eval_vlm_prompt.py                 # 414 ảnh -> EVAL_VLM_PROMPT.md
"""
from __future__ import annotations

import argparse
import collections
import contextlib
import io
import json
import os
import sys

import numpy as np
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'llmdet_vietnamese_food'))


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser()
    p.add_argument('--gt', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations/instances_test.json'),
                   help='GT tên Việt (id lớp giống bộ EN)')
    p.add_argument('--model', default=None, help='tên trong vifood54_core.MODELS (mặc định: mô hình đầu tiên có checkpoint)')
    p.add_argument('--vlm-cache', default=os.path.join(ROOT, 'grounding_data/vifood54/vlm_prompt_test.jsonl'))
    p.add_argument('--no-vlm-call', action='store_true', help='chỉ dùng kết quả VLM đã lưu, không gọi API')
    p.add_argument('--score-thr', type=float, default=0.05, help='ngưỡng giữ box khi tính mAP (thấp để không cắt đường PR)')
    p.add_argument('--limit', type=int, default=0)
    p.add_argument('--out', default=os.path.join(ROOT, 'grounding_data/vifood54/EVAL_VLM_PROMPT.md'))
    return p.parse_args()


def load_cache(path: str) -> dict[str, dict]:
    if not os.path.exists(path):
        return {}
    with open(path, encoding='utf-8') as f:
        return {r['file_name']: r for r in map(json.loads, f) if not r.get('error')}


def coco_map(gt, dets: list[dict], img_ids: list[int]) -> tuple[float, float]:
    from pycocotools.cocoeval import COCOeval
    if not dets:
        return 0.0, 0.0
    with contextlib.redirect_stdout(io.StringIO()):
        ev = COCOeval(gt, gt.loadRes(dets), 'bbox')
        ev.params.imgIds = img_ids
        ev.evaluate()
        ev.accumulate()
        ev.summarize()
    return float(ev.stats[0]), float(ev.stats[1])


def main() -> None:
    args = parse_args()
    import vifood54_core as core
    import vifood54_vlm as vlm_mod
    from pycocotools.coco import COCO

    model = args.model or next(iter(core.MODELS))
    with contextlib.redirect_stdout(io.StringIO()):
        gt = COCO(args.gt)
    id2name = {c['id']: c['name'] for c in gt.dataset['categories']}
    name2id = {v: k for k, v in id2name.items()}
    assert set(name2id) == set(core.CLASS_NAMES), '--gt phải là bộ tên Việt (annotations/instances_test.json)'
    images = gt.loadImgs(sorted(gt.getImgIds()))
    if args.limit:
        images = images[:args.limit]
    cache = load_cache(args.vlm_cache)

    dets: dict[str, list[dict]] = collections.defaultdict(list)
    tp = fp = fn = n_fallback = 0
    cls_hit, cls_gt, other = collections.Counter(), collections.Counter(), collections.Counter()
    for k, im in enumerate(images, 1):
        img = np.array(ImageOps.exif_transpose(Image.open(os.path.join(ROOT, im['file_name']))).convert('RGB'))
        gt_names = {id2name[a['category_id']] for a in gt.imgToAnns[im['id']]}
        v = cache.get(im['file_name'])
        if v is None and not args.no_vlm_call:
            r = vlm_mod.describe(img)
            v = {'file_name': im['file_name'], 'dishes': [d['name'] for d in r['dishes']], 'other': r['other'],
                 'model': r['model'], 'error': r['error']}
            with open(args.vlm_cache, 'a', encoding='utf-8') as f:
                f.write(json.dumps(v, ensure_ascii=False) + '\n')
            if v['error']:
                v = None
        vlm_names = set(v['dishes']) if v else set()
        if v:
            tp += len(vlm_names & gt_names)
            fp += len(vlm_names - gt_names)
            fn += len(gt_names - vlm_names)
            for n in gt_names:
                cls_gt[n] += 1
                cls_hit[n] += n in vlm_names
            other.update(v['other'])
        prompts = {'full54': None, 'oracle': sorted(gt_names) or None, 'vlm': sorted(vlm_names) or None}
        n_fallback += prompts['vlm'] is None
        for kind, classes in prompts.items():
            for it in core.detect(img, model, args.score_thr, classes):
                x1, y1, x2, y2 = it['box']
                dets[kind].append({'image_id': im['id'], 'category_id': name2id[it['name']],
                                   'bbox': [x1, y1, x2 - x1, y2 - y1], 'score': it['score']})
        if k % 25 == 0:
            print(f'{k}/{len(images)}', flush=True)

    img_ids = [im['id'] for im in images]
    prec, rec = tp / max(tp + fp, 1), tp / max(tp + fn, 1)
    L = ['# Đánh giá end-to-end: prompt do VLM chọn so với prompt đủ 54 tên (test ViFood-54)', '',
         f'- Detector: {model}; {len(images)} ảnh; VLM: {vlm_mod.MODELS[0]} (kết quả lưu ở `{os.path.relpath(args.vlm_cache, ROOT)}`)',
         f'- Ảnh VLM lỗi hoặc không nêu món nào (dùng 54 tên): {n_fallback}', '',
         '## A. VLM liệt kê món (theo cặp ảnh–lớp)', '',
         '| Precision | Recall | F1 | đúng | thừa | sót |', '|---|---|---|---|---|---|',
         f'| {prec:.3f} | {rec:.3f} | {2 * prec * rec / max(prec + rec, 1e-9):.3f} | {tp} | {fp} | {fn} |', '',
         '## B. Detector với từng kiểu prompt', '', '| Prompt | mAP | AP50 |', '|---|---|---|']
    for kind in ('full54', 'vlm', 'oracle'):
        m, m50 = coco_map(gt, dets[kind], img_ids)
        L.append(f'| {kind} | {m:.3f} | {m50:.3f} |')
    L += ['', '## Recall của VLM theo lớp (thấp nhất trước; lớp ≥ 3 ảnh test)', '', '| lớp | ảnh có lớp | VLM nêu | recall |',
          '|---|---|---|---|']
    for n in sorted(cls_gt, key=lambda n: cls_hit[n] / cls_gt[n]):
        if cls_gt[n] >= 3:
            L.append(f'| {n} | {cls_gt[n]} | {cls_hit[n]} | {cls_hit[n] / cls_gt[n]:.2f} |')
    L += ['', '## Món VLM xếp ngoài 54 lớp (20 món nhiều nhất)', '',
          ', '.join(f'{n} ({c})' for n, c in other.most_common(20)) or '—']
    with open(args.out, 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('\n'.join(L[:16]))
    print('->', args.out)


if __name__ == '__main__':
    main()
