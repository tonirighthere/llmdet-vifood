#!/usr/bin/env python3
"""
scripts/vifood54/captions/build_captions.py
===========================================
Pha 2: sinh caption grounding hình thái cho ViFood-54 từ annotation OD của build_vifood54.py.

Mỗi ảnh: K biến thể (mặc định 2 × L1 + 4 × L2), mỗi biến thể có bản gốc và bản lật trái↔phải
(dùng khi RandomFlip lật ảnh), kèm regions/tokens_positive tính lúc ghép. Mọi biến thể qua lint
(token BERT đã bỏ dấu, từ hương vị, độ dài); biến thể lỗi bị loại.

    python scripts/vifood54/captions/build_captions.py

Đầu ra (grounding_data/vifood54/annotations/):
  {train,val,test}_vg_cap.jsonl   một dòng / ảnh
  train_vg_cap_rfs.jsonl          theo đúng thứ tự + lặp của train_od_rfs.jsonl
  ../CAPTION_REPORT.md            thống kê, lỗi lint, ví dụ ngẫu nhiên để duyệt tay
"""
import argparse
import collections
import hashlib
import json
import os
import random
import statistics

from transformers import AutoTokenizer

from builder import CaptionBuilder
from layout import group_instances
from lint import CaptionLinter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
LEVELS = ['L1', 'L1', 'L2', 'L2', 'L2', 'L2']


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--ann-dir', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations'))
    p.add_argument('--tokenizer', default=os.path.join(ROOT, 'huggingface/bert-base-uncased'))
    p.add_argument('--max-tokens', type=int, default=160, help='ngân sách token BERT cho caption (256 - negative)')
    p.add_argument('--examples', type=int, default=30)
    p.add_argument('--seed', type=int, default=2026)
    return p.parse_args()


def seed_of(filename, k):
    return int(hashlib.md5(f'{filename}#{k}'.encode()).hexdigest()[:8], 16)


def regions_for(instances, spans):
    by_label = {label: (s, e, name) for s, e, name, label in spans}
    return [{'bbox': inst['bbox'], 'phrase': by_label[inst['label']][2],
             'tokens_positive': [[by_label[inst['label']][0], by_label[inst['label']][1]]]}
            for inst in instances]


def build_row(row, class_names, builder, linter, stats, failures):
    insts = row['detection']['instances']
    groups = group_instances(insts, class_names, row['width'], row['height'])
    variants = []
    for k, level in enumerate(LEVELS):
        plan, cap, spans = builder.build(groups, level, seed_of(row['filename'], k))
        fcap, fspans = builder.render(groups, plan, flip=True)
        errs = linter.check(cap, [s[:3] for s in spans]) + linter.check(fcap, [s[:3] for s in fspans])
        missing = {g.label for g in groups} - {s[3] for s in spans}
        if missing:
            errs.append(f'thiếu lớp trong caption: {missing}')
        stats['variants'] += 1
        if errs:
            stats['failed'] += 1
            failures.append((row['filename'], level, cap, errs))
            continue
        stats[f'tokens_{level}'].append(linter.n_tokens(cap))
        variants.append({'level': level, 'caption': cap, 'regions': regions_for(insts, spans),
                         'flip_caption': fcap, 'flip_regions': regions_for(insts, fspans)})
    if not variants:
        stats['images_without_variant'] += 1
        return None
    stats['unique_per_image'].append(len({v['caption'] for v in variants}))
    first_l2 = next((v for v in variants if v['level'] == 'L2'), variants[0])
    return {
        'filename': row['filename'], 'height': row['height'], 'width': row['width'], 'group': row['group'],
        'detection': row['detection'],
        # tương thích ODVGDataset hiện tại (1 caption); Pha 3 chọn ngẫu nhiên trong variants
        'grounding': {'caption': first_l2['caption'], 'regions': first_l2['regions'], 'variants': variants},
        'conversations': [{'from': 'human', 'value': '<image>\nDescribe the image in detail.'},
                          {'from': 'gpt', 'value': first_l2['caption']}],
        'region_captions': {str(g.label): builder.region_caption(g.name) for g in groups},
    }


def read_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(l) for l in f]


def write_jsonl(path, rows):
    with open(path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def pct(xs, q):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(q * len(xs)))] if xs else 0


def main():
    args = parse_args()
    # thuộc tính hình thái nằm trong taxonomy (trường `visual`), bản xuất kèm dữ liệu của build_vifood54
    with open(os.path.join(args.ann_dir, 'taxonomy.json'), encoding='utf-8') as f:
        tax = json.load(f)['classes']
    class_names = [c['name'] for c in tax]
    bank = {c['name']: c['visual'] for c in tax}

    tok = AutoTokenizer.from_pretrained(args.tokenizer)
    linter = CaptionLinter(tok, class_names, args.max_tokens)
    builder = CaptionBuilder(bank, linter.n_tokens, args.max_tokens)

    report_split = {}
    out_rows = {}
    all_failures = []
    for split in ('train', 'val', 'test'):
        stats = collections.defaultdict(list)
        stats.update({'variants': 0, 'failed': 0, 'images_without_variant': 0})
        rows = read_jsonl(os.path.join(args.ann_dir, f'{split}_od.jsonl'))
        out = []
        for r in rows:
            o = build_row(r, class_names, builder, linter, stats, all_failures)
            if o:
                out.append(o)
        write_jsonl(os.path.join(args.ann_dir, f'{split}_vg_cap.jsonl'), out)
        out_rows[split] = out
        report_split[split] = (len(rows), len(out), stats)
        print(f'{split}: {len(out)}/{len(rows)} ảnh, biến thể lỗi {stats["failed"]}/{stats["variants"]}')

    by_file = {r['filename']: r for r in out_rows['train']}
    rfs = [by_file[r['filename']] for r in read_jsonl(os.path.join(args.ann_dir, 'train_od_rfs.jsonl'))
           if r['filename'] in by_file]
    write_jsonl(os.path.join(args.ann_dir, 'train_vg_cap_rfs.jsonl'), rfs)

    # ── báo cáo ──
    L = ['# ViFood-54 — báo cáo caption hình thái (Pha 2)', '',
         f'- Biến thể / ảnh: {LEVELS}; ngân sách {args.max_tokens} token BERT / caption',
         f'- `train_vg_cap_rfs.jsonl`: {len(rfs)} dòng (theo train_od_rfs)', '',
         '| split | ảnh | ảnh có caption | biến thể lỗi lint | caption khác nhau / ảnh (TB) | token L1 TB / p95 / max | token L2 TB / p95 / max |',
         '|---|---|---|---|---|---|---|']
    for split, (n_in, n_out, st) in report_split.items():
        t1, t2 = st['tokens_L1'], st['tokens_L2']
        L.append(f'| {split} | {n_in} | {n_out} | {st["failed"]}/{st["variants"]} | '
                 f'{statistics.mean(st["unique_per_image"]):.2f} | '
                 f'{statistics.mean(t1):.0f} / {pct(t1, .95)} / {max(t1)} | {statistics.mean(t2):.0f} / {pct(t2, .95)} / {max(t2)} |')
    L += ['', f'## Lỗi lint ({len(all_failures)} biến thể bị loại)', '']
    reasons = collections.Counter(e.split(':')[0] for _, _, _, errs in all_failures for e in errs)
    L += [f'- {k}: {v}' for k, v in reasons.most_common()] or ['- không có']
    for fn, level, cap, errs in all_failures[:10]:
        L.append(f'- `{os.path.basename(fn)}` {level}: {cap[:160]} → {errs[:2]}')

    rng = random.Random(args.seed)
    L += ['', f'## {args.examples} ví dụ ngẫu nhiên (train) để duyệt tay', '']
    for r in rng.sample(out_rows['train'], args.examples):
        v = rng.choice(r['grounding']['variants'])
        L.append(f'- `{os.path.basename(r["filename"])}` [{v["level"]}] {v["caption"]}')
        L.append(f'  - lật: {v["flip_caption"]}')
    with open(os.path.join(args.ann_dir, '..', 'CAPTION_REPORT.md'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(L) + '\n')
    print('->', os.path.normpath(os.path.join(args.ann_dir, '..', 'CAPTION_REPORT.md')))


if __name__ == '__main__':
    main()
