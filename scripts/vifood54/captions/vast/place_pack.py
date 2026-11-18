#!/usr/bin/env python3
"""
Đặt gói dữ liệu caption (zip hoặc tar, cấu trúc thư mục bất kỳ) vào đúng chỗ trong repo trên máy thuê.

    python3 scripts/vifood54/captions/vast/place_pack.py /workspace/caption_pack.zip [--check-only]

- Tìm train_od.jsonl, taxonomy.json, label_map.json ở bất kỳ đâu trong gói -> grounding_data/vifood54/annotations_en/
- Mỗi ảnh mà train_od.jsonl cần (cột `filename`, tương đối gốc repo): nếu chưa ở đúng đường dẫn thì tìm trong gói
  theo phần đuôi đường dẫn dài nhất trùng khớp, rồi chuyển về đúng chỗ.
- Báo số ảnh tìm thấy / thiếu; thiếu ảnh hoặc thiếu train_od.jsonl / taxonomy.json -> thoát mã 1.
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import shutil
import sys
import tarfile
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
ANN = os.path.join(ROOT, 'grounding_data/vifood54/annotations_en')
REQUIRED = ('train_od.jsonl', 'taxonomy.json')
OPTIONAL = ('label_map.json', 'val_od.jsonl', 'test_od.jsonl')


def extract(archive: str, dest: str) -> None:
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as z:
            bad = [n for n in z.namelist() if n.startswith('/') or '..' in n.split('/')]
            if bad:
                sys.exit(f'!! gói có đường dẫn không an toàn: {bad[:3]}')
            z.extractall(dest)
    elif tarfile.is_tarfile(archive):
        with tarfile.open(archive) as t:
            try:
                t.extractall(dest, filter='data')
            except TypeError:  # Python < 3.12 không có filter
                t.extractall(dest)
    else:
        sys.exit(f'!! {archive} không phải zip/tar (link Drive sai hoặc tải về trang HTML?)')


def rank(path: str) -> tuple[int, int]:
    """Ưu tiên file nằm trong thư mục annotations_en/ (gói có thể chứa cả annotations/ tiếng Việt), rồi đường dẫn ngắn."""
    return (0 if 'annotations_en' in path.replace('\\', '/').split('/') else 1, len(path))


def index_tree(top: str) -> tuple[dict[str, list[str]], dict[str, str]]:
    by_base: dict[str, list[str]] = collections.defaultdict(list)
    named: dict[str, str] = {}
    for d, _, files in os.walk(top):
        for f in files:
            p = os.path.join(d, f)
            by_base[f].append(p)
            if f in REQUIRED + OPTIONAL and (f not in named or rank(p) < rank(named[f])):
                named[f] = p
    return by_base, named


def best_match(rel: str, cands: list[str]) -> str | None:
    """Ứng viên có phần đuôi đường dẫn trùng `rel` dài nhất (tránh nhầm 2 ảnh cùng tên ở 2 thư mục)."""
    want = rel.replace('\\', '/').split('/')
    scored = []
    for c in cands:
        parts = c.replace('\\', '/').split('/')
        k = 0
        while k < min(len(parts), len(want)) and parts[-1 - k] == want[-1 - k]:
            k += 1
        scored.append((k, c))
    scored.sort(reverse=True)
    if not scored or (len(scored) > 1 and scored[0][0] == scored[1][0]):
        return None  # mơ hồ
    return scored[0][1]


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('archive')
    p.add_argument('--raw', default=None, help='thư mục giải nén (mặc định: pack_raw cạnh file gói)')
    p.add_argument('--check-only', action='store_true', help='chỉ báo cáo, không chuyển file')
    args = p.parse_args()
    args.raw = args.raw or os.path.join(os.path.dirname(os.path.abspath(args.archive)), 'pack_raw')

    if not os.path.isdir(args.raw) or not os.listdir(args.raw):
        os.makedirs(args.raw, exist_ok=True)
        print(f'giải nén {args.archive} -> {args.raw}')
        extract(args.archive, args.raw)
    by_base, named = index_tree(args.raw)

    for f in REQUIRED:
        if f not in named and not os.path.exists(os.path.join(ANN, f)):
            sys.exit(f'!! gói thiếu {f}')
    os.makedirs(ANN, exist_ok=True)
    for f, src in named.items():
        print(f'  {f:16s} <- {os.path.relpath(src, args.raw)}')
        if not args.check_only:
            shutil.copy2(src, os.path.join(ANN, f))

    od = os.path.join(ANN, 'train_od.jsonl') if not args.check_only else named.get('train_od.jsonl',
                                                                                  os.path.join(ANN, 'train_od.jsonl'))
    with open(od, encoding='utf-8') as fh:
        rows = [json.loads(line) for line in fh if line.strip()]
    n_inst = sum(len(r.get('detection', {}).get('instances', [])) for r in rows)
    print(f'train_od.jsonl: {len(rows)} ảnh, {n_inst} box')

    ok = moved = 0
    missing: list[str] = []
    for r in rows:
        rel = r['filename']
        dst = os.path.join(ROOT, rel)
        if os.path.isfile(dst):
            ok += 1
            continue
        src = best_match(rel, by_base.get(os.path.basename(rel), []))
        if src is None:
            missing.append(rel)
            continue
        if not args.check_only:
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)
        moved += 1
    print(f'ảnh: {ok} đã đúng chỗ, {moved} {"sẽ" if args.check_only else "đã"} chuyển, {len(missing)} THIẾU')
    if missing:
        print('  ví dụ thiếu:', *missing[:5], sep='\n    ')
        sys.exit(1)
    print('OK: dữ liệu đủ để sinh caption')


if __name__ == '__main__':
    main()
