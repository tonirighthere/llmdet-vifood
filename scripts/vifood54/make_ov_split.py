#!/usr/bin/env python3
"""
scripts/vifood54/make_ov_split.py
=================================
Split open-vocabulary cho ViFood-54: lớp `ov_split == 'novel'` trong taxonomy bị loại khỏi MỌI
giám sát khi train (box, tên trong prompt OD, negative, caption VG), ảnh vẫn giữ (giao thức base/novel
kiểu OV-COCO / LVIS). Val để chọn checkpoint chỉ gồm lớp base; test giữ nguyên 54 lớp
(prompt đủ 54 tên) để đo AP_base / AP_novel.

Đọc annotation đã build (Pha 0 + Pha 2), không đổi split ảnh.

    python scripts/vifood54/make_ov_split.py

Đầu ra grounding_data/vifood54/annotations_ov/:
  train_od.jsonl, train_od_rfs.jsonl   box novel đã bỏ; RFS tính lại trên lớp base
  class_drop.json                       class dropout tính lại
  label_map_base.json                   chỉ lớp base (id gốc -> tên)
  taxonomy_base.json                    lớp base, confusable_with bỏ lớp novel (negative VG)
  train_vg_cap_rfs.jsonl                caption sinh lại không có lớp novel (ảnh không còn box base bị bỏ)
  instances_val_base.json               val chỉ lớp base
  ov_classes.json                       danh sách base / novel
"""
import argparse
import collections
import hashlib
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, 'captions'))
from build_vifood54 import class_drop_probs, repeat_factors  # noqa: E402


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--ann-dir', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations'))
    p.add_argument('--out', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations_ov'))
    p.add_argument('--head-cap', type=int, default=400)
    p.add_argument('--repeat-thr', type=float, default=0.05)
    p.add_argument('--seed', type=int, default=2026)
    return p.parse_args()


def read_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(l) for l in f]


def write_jsonl(path, rows):
    with open(path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def strip_novel(row, novel, names):
    insts = [i for i in row['detection']['instances'] if i['label'] not in novel]
    present = list(dict.fromkeys(names[i['label']] for i in insts))
    short = ' . '.join(present) + ' .' if present else ''
    return dict(row, detection={'instances': insts},
                conversations=[row['conversations'][0], {'from': 'gpt', 'value': short}])


def main():
    args = parse_args()
    os.makedirs(args.out, exist_ok=True)
    tax = json.load(open(os.path.join(args.ann_dir, 'taxonomy.json'), encoding='utf-8'))
    classes = tax['classes']
    names = [c['name'] for c in classes]
    novel = {c['id'] for c in classes if c['ov_split'] == 'novel'}
    base = [c['id'] for c in classes if c['id'] not in novel]
    print('novel:', [names[i] for i in sorted(novel)])

    # ── OD train ──
    train = [strip_novel(r, novel, names) for r in read_jsonl(os.path.join(args.ann_dir, 'train_od.jsonl'))]
    write_jsonl(os.path.join(args.out, 'train_od.jsonl'), train)
    recs = [{'boxes': r['detection']['instances']} for r in train]
    _, img_rep = repeat_factors(recs, len(classes), args.repeat_thr)
    rng = random.Random(args.seed)
    rfs = []
    for r, rep in zip(train, img_rep):
        n = int(math.floor(rep)) + (1 if rng.random() < rep - math.floor(rep) else 0)
        rfs.extend([r] * n)
    write_jsonl(os.path.join(args.out, 'train_od_rfs.jsonl'), rfs)
    drop = class_drop_probs([{'boxes': r['detection']['instances']} for r in rfs], args.head_cap)
    json.dump({str(k): v for k, v in drop.items()}, open(os.path.join(args.out, 'class_drop.json'), 'w'), indent=2)
    json.dump({str(i): names[i] for i in base}, open(os.path.join(args.out, 'label_map_base.json'), 'w',
                                                     encoding='utf-8'), ensure_ascii=False, indent=2)

    base_names = {names[i] for i in base}
    tax_base = {'classes': [dict(c, confusable_with=[o for o in c['confusable_with'] if o['name'] in base_names])
                            for c in classes if c['id'] not in novel]}
    json.dump(tax_base, open(os.path.join(args.out, 'taxonomy_base.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    # ── VG caption (sinh lại, giống build_captions nhưng trên box base) ──
    from transformers import AutoTokenizer
    from build_captions import build_row
    from builder import CaptionBuilder
    from lint import CaptionLinter
    tok = AutoTokenizer.from_pretrained(os.path.join(ROOT, 'huggingface/bert-base-uncased'))
    linter = CaptionLinter(tok, names, 160)  # lint với đủ 54 tên: caption không được nhắc lớp novel
    builder = CaptionBuilder({c['name']: c['visual'] for c in classes}, linter.n_tokens, 160)
    stats = collections.defaultdict(list)
    stats.update({'variants': 0, 'failed': 0, 'images_without_variant': 0})
    failures = []
    vg = {}
    for r in train:
        if r['detection']['instances']:
            o = build_row(r, names, builder, linter, stats, failures)
            if o:
                vg[r['filename']] = o
    vg_rfs = [vg[r['filename']] for r in rfs if r['filename'] in vg]
    write_jsonl(os.path.join(args.out, 'train_vg_cap_rfs.jsonl'), vg_rfs)

    # ── val chỉ lớp base ──
    coco = json.load(open(os.path.join(args.ann_dir, 'instances_val.json'), encoding='utf-8'))
    coco['annotations'] = [a for a in coco['annotations'] if a['category_id'] not in novel]
    coco['categories'] = [c for c in coco['categories'] if c['id'] not in novel]
    json.dump(coco, open(os.path.join(args.out, 'instances_val_base.json'), 'w', encoding='utf-8'), ensure_ascii=False)

    json.dump({'base': [names[i] for i in base], 'novel': [names[i] for i in sorted(novel)],
               'novel_ids': sorted(novel)},
              open(os.path.join(args.out, 'ov_classes.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # ── kiểm tra rò rỉ ──
    novel_names = {names[i] for i in novel}
    leak_od = sum(i['label'] in novel for r in rfs for i in r['detection']['instances'])
    import re
    novel_re = [re.compile(r'(?<!\w)' + re.escape(n) + r'(?!\w)', re.I) for n in novel_names]  # 'ốc' ≠ 'ruốc'
    leak_vg = sum(any(x.search(v['caption']) or x.search(v['flip_caption']) for x in novel_re)
                  for r in vg_rfs for v in r['grounding']['variants'])
    n_removed = sum(1 for r in read_jsonl(os.path.join(args.ann_dir, 'train_od.jsonl'))
                    for i in r['detection']['instances'] if i['label'] in novel)
    print(f'train {len(train)} ảnh, bỏ {n_removed} box novel; train_od_rfs {len(rfs)}; '
          f'VG {len(vg)} ảnh / rfs {len(vg_rfs)}, biến thể lỗi {stats["failed"]}/{stats["variants"]}; '
          f'val base {len(coco["annotations"])} box; rò rỉ novel: OD {leak_od}, caption {leak_vg}')
    assert leak_od == 0 and leak_vg == 0


if __name__ == '__main__':
    main()
