#!/usr/bin/env python3
"""
Bộ annotation TIẾNG ANH cho ViFood-54: cùng ảnh, box, id lớp và split với annotations/ (tiếng Việt), chỉ đổi chuỗi
tên lớp đưa vào BERT sang tiếng Anh (en_names.PROMPT_EN). Bộ tiếng Việt giữ nguyên làm đối chứng.

    python scripts/vifood54/make_en_data.py               # rồi: python scripts/vifood54/captions/build_captions_en.py

Ra grounding_data/vifood54/annotations_en/:
  taxonomy.json          name = tên EN, name_vi = khóa VI; visual = bản dịch (units là cặp [số ít, số nhiều]);
                         confusable_with đổi sang tên EN (negative VG ưu tiên lớp dễ nhầm)
  label_map.json         id -> tên EN (prompt OD)
  {train,val,test}_od.jsonl, train_od_rfs.jsonl, train_od_full.jsonl   `category` đổi sang tên EN
  class_drop.json        chép nguyên (theo id)
  instances_{val,test}.json   categories.name đổi sang tên EN (CocoDataset lọc lớp theo tên trong metainfo)
"""
import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(HERE, 'captions'))
from en_names import PROMPT_EN, VISUAL_EN, units_en  # noqa: E402


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--src', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations'))
    p.add_argument('--dst', default=os.path.join(ROOT, 'grounding_data/vifood54/annotations_en'))
    args = p.parse_args()
    os.makedirs(args.dst, exist_ok=True)

    tax = json.load(open(os.path.join(args.src, 'taxonomy.json'), encoding='utf-8'))
    en = {}
    for c in tax['classes']:
        en[c['name']] = PROMPT_EN[c['name']]
    assert len(set(en.values())) == len(en), 'tên EN trùng nhau'

    out_cls = []
    for c in tax['classes']:
        d, attrs = VISUAL_EN[c['name']]
        v = c['visual']
        e = dict(c)
        e.update({
            'name': en[c['name']], 'name_vi': c['name'],
            'visual': {'definition': d, 'attrs': attrs, 'units': units_en(v['units']),
                       'multi_units': units_en(v['multi_units']) if v.get('multi_units') else None,
                       'attrs_vi': v['attrs']},
            'confusable_with': [{'name': en[o['name']], 'cue': o.get('cue', '')}
                                for o in c.get('confusable_with', [])],
        })
        out_cls.append(e)
    out_tax = dict(tax, classes=out_cls,
                   note='Bản tiếng Anh sinh bởi scripts/vifood54/make_en_data.py; name = prompt EN, name_vi = khóa gốc')
    json.dump(out_tax, open(os.path.join(args.dst, 'taxonomy.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    lm = json.load(open(os.path.join(args.src, 'label_map.json'), encoding='utf-8'))
    json.dump({k: en[v] for k, v in lm.items()}, open(os.path.join(args.dst, 'label_map.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=2)

    for fn in ('train_od.jsonl', 'val_od.jsonl', 'test_od.jsonl', 'train_od_rfs.jsonl', 'train_od_full.jsonl'):
        src = os.path.join(args.src, fn)
        if not os.path.exists(src):
            continue
        n = 0
        with open(src, encoding='utf-8') as fi, open(os.path.join(args.dst, fn), 'w', encoding='utf-8') as fo:
            for line in fi:
                r = json.loads(line)
                for inst in r['detection']['instances']:
                    inst['category'] = en[inst['category']]
                fo.write(json.dumps(r, ensure_ascii=False) + '\n')
                n += 1
        print(f'{fn}: {n} dòng')

    shutil.copy(os.path.join(args.src, 'class_drop.json'), os.path.join(args.dst, 'class_drop.json'))
    for split in ('val', 'test'):
        coco = json.load(open(os.path.join(args.src, f'instances_{split}.json'), encoding='utf-8'))
        for c in coco['categories']:
            c['name'] = en[c['name']]
        json.dump(coco, open(os.path.join(args.dst, f'instances_{split}.json'), 'w', encoding='utf-8'), ensure_ascii=False)
        print(f'instances_{split}.json: {len(coco["images"])} ảnh, {len(coco["annotations"])} box')
    print('->', args.dst)


if __name__ == '__main__':
    main()
