#!/usr/bin/env bash
# Chạy trên SERVER CỦA NHÓM (nơi có ảnh + annotations_en/*.jsonl): đóng gói đúng những gì máy thuê cần để sinh caption v2.
#   bash scripts/vifood54/captions/vast/pack_for_caption.sh            # -> caption_pack.tar (ảnh train + annotation)
#   SPLITS="train val" bash scripts/vifood54/captions/vast/pack_for_caption.sh   # thêm ảnh val nếu cần
# Đường dẫn trong gói giữ nguyên tương đối gốc repo -> trên máy thuê chỉ cần `tar -xf` ở gốc repo.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
cd "$ROOT"
A=grounding_data/vifood54/annotations_en
OUT=${OUT:-$ROOT/caption_pack.tar}
LIST=$(mktemp)
for f in taxonomy.json label_map.json; do echo "$A/$f" >> "$LIST"; done
for s in ${SPLITS:-train}; do
  [ -f "$A/${s}_od.jsonl" ] || { echo "thiếu $A/${s}_od.jsonl (chạy scripts/vifood54/make_en_data.py)"; exit 1; }
  echo "$A/${s}_od.jsonl" >> "$LIST"
  python3 -c "
import json, sys
for line in open('$A/${s}_od.jsonl', encoding='utf-8'):
    print(json.loads(line)['filename'])" >> "$LIST"
done
sort -u "$LIST" -o "$LIST"
MISSING=$(while read -r f; do [ -f "$f" ] || echo "$f"; done < "$LIST" | head -5)
[ -z "$MISSING" ] || { echo "thiếu file (5 file đầu):"; echo "$MISSING"; exit 1; }
tar -cf "$OUT" -T "$LIST"
echo "-> $OUT: $(($(wc -l < "$LIST") - 2)) file, $(du -h "$OUT" | cut -f1)"
rm -f "$LIST"
