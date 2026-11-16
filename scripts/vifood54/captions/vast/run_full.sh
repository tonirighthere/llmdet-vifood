#!/usr/bin/env bash
# CHẠY CẢ TẬP train (3138 ảnh) với model mô tả đã chọn sau khi chấm chạy thử.
#   DESCRIBER=Qwen/Qwen3-VL-32B-Instruct bash scripts/vifood54/captions/vast/run_full.sh
# Chạy lại được: ảnh nào đã có kết quả thì bỏ qua (dừng/mất kết nối giữa chừng không mất việc).
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
cd "$ROOT"
source scripts/vifood54/captions/vast/serve.sh
C=scripts/vifood54/captions/caption_v2.py
DESCRIBER=${DESCRIBER:?đặt DESCRIBER=<model mô tả đã chọn>}
VERIFIER=${VERIFIER:-google/gemma-4-12B-it}
R=${RUN:-full_$(echo "$DESCRIBER" | sed 's|.*/||; s/-Instruct.*//; s/[^A-Za-z0-9.]/_/g')}

start_vllm "$DESCRIBER" 9100
python3 $C describe --run "$R" --url http://localhost:9100 --workers "${WORKERS:-32}"
stop_vllm 9100
start_vllm "$VERIFIER" 9101
python3 $C verify --run "$R" --url http://localhost:9101 --workers "${WORKERS:-32}"
python3 $C compose --run "$R"
python3 $C translate --run "$R" --url http://localhost:9101 --workers "${WORKERS:-32}"
stop_vllm 9101
python3 $C stats --run "$R"
tar -czf "$ROOT/captions_full.tgz" -C "$ROOT" "grounding_data/vifood54/captions_v2/$R"
echo "XONG -> captions_full.tgz. Chép về rồi HỦY (destroy) instance ngay (máy dừng vẫn tính phí ổ)."
