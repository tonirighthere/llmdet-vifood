#!/usr/bin/env python3
"""
Kiểm tra máy thuê có ĐỦ mọi thứ để train B5b / OV-S1 / OV-W trước khi tốn giờ GPU.

    python scripts/vifood54/vast_train/check_train_data.py            # dữ liệu gốc (sau khi giải nén 3 zip)
    python scripts/vifood54/vast_train/check_train_data.py --stage ready --load-ckpt   # sau publish/attach/make_ov_split

Kiểm tra: file annotation mà các config dùng, MỌI ảnh mà các file đó tham chiếu (đường dẫn tương đối gốc repo),
model nền trong huggingface/, checkpoint (tùy chọn nạp thử bằng torch.load). Thiếu bất kỳ thứ gì -> thoát mã 1.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Iterator

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
EN = 'grounding_data/vifood54/annotations_en'
OV = 'grounding_data/vifood54/annotations_ov_en'
W = 'llmdet_vietnamese_food/work_dirs'

BASE_FILES: list[str] = [
    f'{EN}/{n}' for n in ('taxonomy.json', 'label_map.json', 'class_drop.json', 'instances_val.json',
                          'instances_test.json', 'train_od.jsonl', 'train_od_rfs.jsonl', 'train_vg_cap_rfs.jsonl',
                          'train_od_rfs_lmm.jsonl', 'train_vg_cap_rfs_lmm.jsonl', 'test_vg_cap.jsonl')
] + [
    'huggingface/bert-base-uncased/config.json',
    'huggingface/bert-base-uncased/vocab.txt',
    'huggingface/my_llava-onevision-qwen2-0.5b-ov-2/config.json',
    'huggingface/my_llava-onevision-qwen2-0.5b-ov-2/model.safetensors',
    'huggingface/my_llava-onevision-qwen2-0.5b-ov-2/mm_projector2.bin',
    'huggingface/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth',
    'grounding_data/vifood54/captions_v2/full_Qwen3_VL_32B/translated.jsonl',
]
CKPTS: list[str] = [
    f'{W}/vifood54_b1_od_en/best_coco_bbox_mAP_iter_16000.pth',   # load_from của bước căn chỉnh B5
    f'{W}/vifood54_b3b_ft_en/best_coco_bbox_mAP_iter_7000.pth',   # mốc so sánh B3b-EN
]
READY_FILES: list[str] = [
    f'{EN}/vlm_captions.jsonl',
    f'{EN}/train_od_rfs_lmm_v2.jsonl', f'{EN}/train_vg_cap_rfs_lmm_v2.jsonl',             # B5b
    f'{OV}/train_od_rfs.jsonl', f'{OV}/label_map_base.json', f'{OV}/class_drop.json',      # OV-S1
    f'{OV}/instances_val_base.json', f'{OV}/ov_classes.json',
    f'{OV}/train_od_rfs_lmm.jsonl', f'{OV}/train_vg_cap_rfs_lmm.jsonl',                    # OV-W
]


def image_refs(rel: str) -> Iterator[str]:
    path = os.path.join(ROOT, rel)
    if rel.endswith('.jsonl'):
        with open(path, encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    yield json.loads(line)['filename']
    else:
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
        for im in data.get('images', []):
            yield im['file_name']


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--stage', choices=['data', 'ready'], default='data')
    p.add_argument('--load-ckpt', action='store_true', help='nạp thử checkpoint bằng torch.load (chậm ~1 phút)')
    args = p.parse_args()

    files = BASE_FILES + CKPTS + (READY_FILES if args.stage == 'ready' else [])
    missing = [f for f in files if not os.path.isfile(os.path.join(ROOT, f))]
    empty = [f for f in files if f not in missing and os.path.getsize(os.path.join(ROOT, f)) == 0]
    for f in files:
        mark = 'THIẾU' if f in missing else ('RỖNG' if f in empty else 'ok')
        print(f'  [{mark:5s}] {f}')

    ann = [f for f in files if f.startswith('grounding_data/vifood54/annotations') and f not in missing
           and (f.endswith('.jsonl') or 'instances_' in f)]
    refs: set[str] = set()
    for f in ann:
        refs.update(image_refs(f))
    no_img = sorted(r for r in refs if not os.path.isfile(os.path.join(ROOT, r)))
    print(f'ảnh được tham chiếu: {len(refs)} · thiếu: {len(no_img)}')
    for r in no_img[:5]:
        print('   thiếu ảnh:', r)

    bad_ckpt: list[str] = []
    if args.load_ckpt:
        import torch
        for c in CKPTS:
            if c in missing:
                continue
            try:
                sd = torch.load(os.path.join(ROOT, c), map_location='cpu', weights_only=False)
                n = len(sd.get('state_dict', sd))
                print(f'  nạp được {c}: {n} tensor')
            except (RuntimeError, OSError, EOFError, ValueError) as e:  # file hỏng / tải dở
                bad_ckpt.append(c)
                print(f'  !! không nạp được {c}: {e}')

    if missing or empty or no_img or bad_ckpt:
        sys.exit(f'!! CHƯA ĐỦ: {len(missing)} file thiếu, {len(empty)} file rỗng, {len(no_img)} ảnh thiếu, '
                 f'{len(bad_ckpt)} checkpoint lỗi')
    print(f'OK ({args.stage}): đủ dữ liệu')


if __name__ == '__main__':
    main()
