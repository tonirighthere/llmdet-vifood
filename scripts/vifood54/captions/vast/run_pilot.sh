#!/usr/bin/env bash
# CHẠY THỬ trên máy thuê: cùng N ảnh (mặc định 50) cho 3 model mô tả, cùng 1 model kiểm chứng + dịch -> COMPARE.md để
# người chấm chọn model chạy cả tập. Thứ tự tải model được sắp để ổ 140 GB không bị đầy (xóa model nhỏ sau khi dùng).
#   bash scripts/vifood54/captions/vast/run_pilot.sh
#   N=30 DESCRIBERS="Qwen/Qwen3-VL-8B-Instruct Qwen/Qwen3-VL-32B-Instruct" bash .../run_pilot.sh
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../../.." && pwd)
cd "$ROOT"
source scripts/vifood54/captions/vast/serve.sh
C=scripts/vifood54/captions/caption_v2.py
N=${N:-50}
# Mô tả: 8B (nhanh, mốc dưới) -> 72B nén AWQ (gần paper) -> 32B (ứng viên chính, giữ lại cho lần chạy cả tập)
DESCRIBERS=${DESCRIBERS:-"Qwen/Qwen3-VL-8B-Instruct Qwen/Qwen2.5-VL-72B-Instruct-AWQ Qwen/Qwen3-VL-32B-Instruct"}
VERIFIER=${VERIFIER:-google/gemma-4-12B-it}   # PHẢI khác dòng model mô tả; đổi qua biến này nếu vLLM chưa hỗ trợ
run_name() { echo "$1" | sed 's|.*/||; s/-Instruct.*//; s/[^A-Za-z0-9.]/_/g'; }

RUNS=()
for M in $DESCRIBERS; do
  R=pilot_$(run_name "$M"); RUNS+=("$R")
  start_vllm "$M" 9100
  python3 $C describe --run "$R" --url http://localhost:9100 --limit "$N" --workers 32
  stop_vllm 9100
  [ "$M" = "Qwen/Qwen3-VL-32B-Instruct" ] || drop_model "$M"
done

start_vllm "$VERIFIER" 9101
for R in "${RUNS[@]}"; do
  python3 $C verify --run "$R" --url http://localhost:9101 --workers 32
  python3 $C compose --run "$R"
  python3 $C translate --run "$R" --url http://localhost:9101 --workers 32
done
stop_vllm 9101
python3 $C compare --runs "$(IFS=,; echo "${RUNS[*]}")"
tar -czf "$ROOT/captions_pilot.tgz" -C "$ROOT" grounding_data/vifood54/captions_v2
echo "XONG chạy thử -> captions_pilot.tgz (chép về, chấm COMPARE.md / compare_scores.csv)."
echo "Máy vẫn đang tính tiền: nếu chưa chạy cả tập ngay, HỦY (destroy) instance."
