#!/usr/bin/env python3
"""
Caption LMM tiếng Anh cho B5-EN, dùng cả đặc điểm VLM tự thêm (`extra` trong vlm_attrs/, bản dịch
annotations_en/translations_vi_en.json của translate_en.py).

Chỉ thay đích của loss LMM: `conversations` (caption ảnh) và `region_captions` (caption vùng). Caption grounding cho BERT
(`grounding`) và dòng OD giữ nguyên như dữ liệu B3b-EN đã train, để B5-EN khác B3b-EN đúng ở phần giám sát LLM.

    python scripts/vifood54/captions/build_lmm_en.py

1) chép đầu vào của build_captions_en.py sang thư mục tạm, dựng caption ở đó (không ghi đè annotations_en/*_vg_cap*);
2) ghép conversations + region_captions mới vào annotations_en/train_{od_rfs,vg_cap_rfs}.jsonl
   -> annotations_en/train_{od_rfs,vg_cap_rfs}_lmm.jsonl (bản cũ đổi tên *.bak_template).
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ANN = os.path.join(ROOT, 'grounding_data/vifood54/annotations_en')
INPUTS = ['taxonomy.json', 'label_map.json', 'train_od.jsonl', 'val_od.jsonl', 'test_od.jsonl', 'train_od_rfs.jsonl',
          'translations_vi_en.json']


def read_jsonl(path):
    with open(path, encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path, rows):
    with open(path, 'w', encoding='utf-8') as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--ann-dir', default=ANN)
    p.add_argument('--keep-tmp', action='store_true')
    args = p.parse_args()

    tmp_root = tempfile.mkdtemp(prefix='vifood54_lmm_en_')
    tmp_ann = os.path.join(tmp_root, 'annotations_en')
    os.makedirs(tmp_ann)
    for f in INPUTS:
        shutil.copy(os.path.join(args.ann_dir, f), tmp_ann)
    subprocess.run([sys.executable, os.path.join(HERE, 'build_captions_en.py'), '--ann-dir', tmp_ann], check=True)

    new = {r['filename']: r for r in read_jsonl(os.path.join(tmp_ann, 'train_vg_cap.jsonl'))}
    for name in ('train_od_rfs', 'train_vg_cap_rfs'):
        rows = read_jsonl(os.path.join(args.ann_dir, f'{name}.jsonl'))
        out, n_new, n_same = [], 0, 0
        for r in rows:
            v = new.get(r['filename'])
            if v is None:
                out.append(r)
                continue
            old = r.get('conversations', [{}, {}])[1].get('value') if 'conversations' in r else None
            n_same += old == v['conversations'][1]['value']
            n_new += 1
            out.append(dict(r, conversations=v['conversations'], region_captions=v['region_captions']))
        dst = os.path.join(args.ann_dir, f'{name}_lmm.jsonl')
        if os.path.exists(dst) and not os.path.exists(dst + '.bak_template'):
            os.replace(dst, dst + '.bak_template')
        write_jsonl(dst, out)
        print(f'{os.path.relpath(dst, ROOT)}: {len(out)} dòng, {n_new} có caption LMM mới '
              f'({n_same} trùng caption ảnh cũ của dòng), grounding giữ nguyên')
    report = os.path.join(tmp_root, 'CAPTION_REPORT_EN.md')
    shutil.copy(report, os.path.join(args.ann_dir, '..', 'CAPTION_REPORT_LMM_EN.md'))
    print('báo cáo -> grounding_data/vifood54/CAPTION_REPORT_LMM_EN.md')
    if args.keep_tmp:
        print('thư mục tạm:', tmp_root)
    else:
        shutil.rmtree(tmp_root)


if __name__ == '__main__':
    main()
