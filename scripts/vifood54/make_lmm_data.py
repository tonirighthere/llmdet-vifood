#!/usr/bin/env python3
"""
Dữ liệu cho B5 (LLMDet đủ 3 loss): thêm caption ảnh (`conversations`) và caption vùng (`region_captions`)
của tập VG vào từng dòng OD, để mẫu OD cũng có đích cho loss LMM ảnh/vùng như GroundingCap của paper.
Dòng OD ban đầu chỉ có câu liệt kê tên lớp làm caption ảnh.

    python scripts/vifood54/make_lmm_data.py            # -> annotations/train_od_rfs_lmm.jsonl
"""
import argparse
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ANN = os.path.join(ROOT, 'grounding_data/vifood54/annotations')


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--od', default=os.path.join(ANN, 'train_od_rfs.jsonl'))
    p.add_argument('--vg', default=os.path.join(ANN, 'train_vg_cap.jsonl'))
    p.add_argument('--out', default=os.path.join(ANN, 'train_od_rfs_lmm.jsonl'))
    args = p.parse_args()

    vg = {}
    for line in open(args.vg, encoding='utf-8'):
        r = json.loads(line)
        vg[r['filename']] = r
    n, miss = 0, 0
    with open(args.out, 'w', encoding='utf-8') as f:
        for line in open(args.od, encoding='utf-8'):
            r = json.loads(line)
            v = vg.get(r['filename'])
            if v is None:
                miss += 1
            else:
                r['conversations'] = v['conversations']
                r['region_captions'] = v['region_captions']
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
            n += 1
    print(f'{n} dòng OD, {n - miss} có caption ảnh/vùng, {miss} không có (giữ caption tên lớp) -> {args.out}')


if __name__ == '__main__':
    main()
