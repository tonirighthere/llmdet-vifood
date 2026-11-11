#!/usr/bin/env python3
"""
Sinh caption grounding TIẾNG ANH cho ViFood-54 (bản song song của build_captions.py, cùng số biến thể, cùng seed,
cùng lint trên token BERT) từ annotations_en/ của make_en_data.py.

Khác bản tiếng Việt: ảnh train có kết quả VLM (vlm_attrs/*.jsonl, Gemma xác nhận thuộc tính nào thật sự nhìn thấy
trên crop) thì mỗi lớp chỉ dùng các thuộc tính VLM giữ lại (+ đặc điểm VLM thêm nếu đã có bản dịch, bỏ cụm tả dụng
cụ/nền), thay vì thuộc tính mặc định của lớp — template cũ khẳng định nhiều thứ không có trong ảnh (vd. `rau sống ·
xếp đầy kín` bị VLM loại 90%). Val/test không có VLM nên giữ thuộc tính taxonomy. Tắt bằng --no-vlm.

    python scripts/vifood54/captions/build_captions_en.py

Đầu ra (grounding_data/vifood54/annotations_en/): {train,val,test}_vg_cap.jsonl, train_vg_cap_rfs.jsonl,
../CAPTION_REPORT_EN.md
"""
import argparse
import collections
import glob
import json
import os
import random
import re
import statistics

from transformers import AutoTokenizer

from build_captions import LEVELS, pct, read_jsonl, regions_for, seed_of, write_jsonl
from builder_en import CaptionBuilderEN
from en_names import CONTAINER_EN
from layout import group_instances
from lint import TASTE_ALLOW_EN, TASTE_WORDS_EN, CaptionLinter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
# đặc điểm VLM thêm nhưng tả dụng cụ / nền / bố cục chứ không phải món
NOT_FOOD_EN = re.compile(r'\b(plate|bowl|dish|tray|basket|pot|cup|glass|spoon|chopsticks?|fork|knife|table|'
                         r'background|napkin|cloth|paper|box|bag|rim|border|pattern|wooden|ceramic|metal)\b')


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument('--ann-dir', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations_en'))
    p.add_argument('--tokenizer', default=os.path.join(ROOT, 'huggingface/bert-base-uncased'))
    p.add_argument('--vlm-dir', default=os.path.join(ROOT, 'grounding_data/vifood54/vlm_attrs'))
    p.add_argument('--no-vlm', action='store_true', help='chỉ dùng thuộc tính taxonomy (đối chứng đúng với bản VI)')
    p.add_argument('--max-tokens', type=int, default=160)
    p.add_argument('--examples', type=int, default=30)
    p.add_argument('--seed', type=int, default=2026)
    return p.parse_args()


class AttrSource:
    """Thuộc tính cho từng (ảnh, lớp): VLM nếu có, không thì taxonomy. Lọc trước mọi cụm chứa tên lớp / từ hương vị."""

    def __init__(self, tax, linter, vlm_dir, translations):
        self.linter = linter
        self.stats = collections.Counter()
        self.bad_attrs = collections.Counter()
        self.vi2en = {}
        self.bank = {}
        for c in tax:
            v = c['visual']
            ok = [a for a in v['attrs'] if self.ok(c['name'], a)]
            self.bank[c['name']] = {'units': [tuple(u) for u in v['units']],
                                    'multi_units': [tuple(u) for u in v['multi_units']] if v.get('multi_units') else None,
                                    'attrs': ok}
            self.vi2en[c['name_vi']] = (c['name'], dict(zip(v['attrs_vi'], v['attrs'])))
        self.extra_en = translations
        self.vlm = {}
        if vlm_dir:
            for f in sorted(glob.glob(os.path.join(vlm_dir, 'train_*.jsonl'))):
                for line in open(f, encoding='utf-8'):
                    r = json.loads(line)
                    self.vlm[r['filename']] = r['classes']

    def ok(self, name, attr):
        """Cụm đứng sau tên lớp trong câu mẫu có qua lint không (tên lớp khác, hương vị)."""
        head = f'a bowl of {name}'
        a = len(head) - len(name)
        errs = self.linter.check(f'{head}, {attr}.', [(a, a + len(name), name)])
        if errs:
            self.bad_attrs[attr] += 1
        return not errs

    def pool(self, filename):
        """({tên EN: [thuộc tính]}, {tên EN: lượng từ}) cho các lớp có kết quả VLM trên ảnh này; (None, None) nếu không."""
        classes = self.vlm.get(filename)
        if classes is None:
            return None, None
        out, units = {}, {}
        for vi, v in classes.items():
            if 'error' in v:
                self.stats['vlm_error'] += 1
                continue
            name, amap = self.vi2en[vi]
            attrs = [amap[a] for a in v['visible'] if a in amap and amap[a] in self.bank[name]['attrs']]
            n_extra = 0
            for e in v.get('extra') or []:
                en = self.extra_en.get(e)
                if en and not NOT_FOOD_EN.search(en) and en not in attrs and self.ok(name, en):
                    attrs.append(en)
                    n_extra += 1
            self.stats['vlm_classes'] += 1
            self.stats['vlm_attrs_kept'] += len(attrs) - n_extra
            self.stats['vlm_attrs_default'] += len(self.bank[name]['attrs'])
            self.stats['vlm_extra_used'] += n_extra
            self.stats['vlm_empty'] += not attrs
            out[name] = attrs
            if v.get('container') in CONTAINER_EN:
                units[name] = CONTAINER_EN[v['container']]
                self.stats['vlm_container_used'] += 1
        return out, units


def build_row(row, class_names, builder, linter, attrs, stats, failures):
    insts = row['detection']['instances']
    groups = group_instances(insts, class_names, row['width'], row['height'])
    pool, units = attrs.pool(row['filename']) if attrs else (None, None)
    stats['images_vlm'] += pool is not None
    variants = []
    for k, level in enumerate(LEVELS):
        plan, cap, spans = builder.build(groups, level, seed_of(row['filename'], k), pool, units)
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
        'grounding': {'caption': first_l2['caption'], 'regions': first_l2['regions'], 'variants': variants},
        'conversations': [{'from': 'human', 'value': '<image>\nDescribe the image in detail.'},
                          {'from': 'gpt', 'value': first_l2['caption']}],
        'region_captions': {str(g.label): builder.region_caption(g.name, pool, units) for g in groups},
    }


def main():
    args = parse_args()
    tax = json.load(open(os.path.join(args.ann_dir, 'taxonomy.json'), encoding='utf-8'))['classes']
    class_names = [c['name'] for c in tax]
    tok = AutoTokenizer.from_pretrained(args.tokenizer)
    linter = CaptionLinter(tok, class_names, args.max_tokens, TASTE_WORDS_EN, TASTE_ALLOW_EN)
    tr_path = os.path.join(args.ann_dir, 'translations_vi_en.json')
    translations = json.load(open(tr_path, encoding='utf-8')).get('phrases', {}) if os.path.exists(tr_path) else {}
    src = AttrSource(tax, linter, None if args.no_vlm else args.vlm_dir, translations)
    builder = CaptionBuilderEN(src.bank, linter.n_tokens, args.max_tokens)

    report_split, out_rows, all_failures = {}, {}, []
    for split in ('train', 'val', 'test'):
        stats = collections.defaultdict(list)
        stats.update({'variants': 0, 'failed': 0, 'images_without_variant': 0, 'images_vlm': 0})
        rows = read_jsonl(os.path.join(args.ann_dir, f'{split}_od.jsonl'))
        out = [o for o in (build_row(r, class_names, builder, linter, src if split == 'train' else None, stats,
                                     all_failures) for r in rows) if o]
        write_jsonl(os.path.join(args.ann_dir, f'{split}_vg_cap.jsonl'), out)
        out_rows[split] = out
        report_split[split] = (len(rows), len(out), stats)
        print(f'{split}: {len(out)}/{len(rows)} ảnh (VLM {stats["images_vlm"]}), '
              f'biến thể lỗi {stats["failed"]}/{stats["variants"]}')

    by_file = {r['filename']: r for r in out_rows['train']}
    rfs = [by_file[r['filename']] for r in read_jsonl(os.path.join(args.ann_dir, 'train_od_rfs.jsonl'))
           if r['filename'] in by_file]
    write_jsonl(os.path.join(args.ann_dir, 'train_vg_cap_rfs.jsonl'), rfs)

    s = src.stats
    L = ['# ViFood-54 — báo cáo caption hình thái TIẾNG ANH', '',
         f'- Biến thể / ảnh: {LEVELS}; ngân sách {args.max_tokens} token BERT / caption',
         f'- `train_vg_cap_rfs.jsonl`: {len(rfs)} dòng (theo train_od_rfs)',
         '- Thuộc tính VLM (train): ' + ('tắt (--no-vlm)' if args.no_vlm else f'{s["vlm_classes"]} lượt lớp-ảnh')
         + ('' if args.no_vlm else
            f'; giữ {s["vlm_attrs_kept"]}/{s["vlm_attrs_default"]} thuộc tính taxonomy, thêm {s["vlm_extra_used"]} '
            f'đặc điểm VLM (bản dịch có {len(translations)} cụm), {s["vlm_empty"]} lượt không còn thuộc tính, '
            f'{s["vlm_error"]} lượt VLM lỗi (dùng taxonomy); lượng từ theo dụng cụ VLM thấy: {s["vlm_container_used"]} lượt'),
         f'- Cụm bị lint loại trước khi ghép: {sum(src.bad_attrs.values())} '
         f'({", ".join(f"{a!r}" for a, _ in src.bad_attrs.most_common(8))})', '',
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
    out_md = os.path.normpath(os.path.join(args.ann_dir, '..', 'CAPTION_REPORT_EN.md'))
    open(out_md, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('->', out_md)


if __name__ == '__main__':
    main()
