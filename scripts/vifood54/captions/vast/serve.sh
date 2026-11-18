#!/usr/bin/env bash
# Hàm dùng chung: bật / tắt máy chủ vLLM cho một model. `source` file này, không chạy trực tiếp.
#   start_vllm <model> <port>   -> chạy nền, chờ tới khi /v1/models trả lời (gồm cả thời gian tải model lần đầu)
#   stop_vllm <port>
#   drop_model <model>          -> xóa model khỏi cache HF để giải phóng ổ (ổ máy thuê có hạn)
WS=${WS:-/workspace}
export HF_HOME=${HF_HOME:-$WS/hf}
export HF_HUB_DISABLE_XET=${HF_HUB_DISABLE_XET:-1}  # tránh cache xet trùng lặp làm đầy ổ
LOGDIR=${LOGDIR:-$WS/logs}
mkdir -p "$LOGDIR"

start_vllm() {
  local model=$1 port=$2
  if curl -sf "http://localhost:$port/v1/models" > /dev/null || ss -ltn 2>/dev/null | grep -q ":$port "; then echo "!! cổng $port đang bận"; return 1; fi
  local log="$LOGDIR/vllm_$(echo "$model" | tr '/' '_')_$port.log"
  # ảnh đã được caption_v2.py thu nhỏ (cạnh dài <= 1280) -> 4096 token là đủ cho 1 ảnh + lệnh + trả lời
  nohup vllm serve "$model" --port "$port" --max-model-len "${MAX_LEN:-4096}" \
    --gpu-memory-utilization "${GPU_UTIL:-0.92}" --max-num-seqs "${MAX_SEQS:-64}" \
    --limit-mm-per-prompt '{"image": 1}' ${VLLM_EXTRA:-} > "$log" 2>&1 &
  echo $! > "$LOGDIR/vllm_$port.pid"
  echo "vLLM $model :$port (log $log) — chờ sẵn sàng..."
  for _ in $(seq 1 360); do  # tối đa 60 phút (tải model ~70 GB)
    if curl -sf "http://localhost:$port/v1/models" > /dev/null; then echo "sẵn sàng"; return 0; fi
    if ! kill -0 "$(cat "$LOGDIR/vllm_$port.pid")" 2>/dev/null; then echo "!! vLLM thoát, xem $log"; tail -20 "$log"; return 1; fi
    sleep 10
  done
  echo "!! quá 60 phút chưa sẵn sàng, xem $log"; return 1
}

stop_vllm() {
  local pidf="$LOGDIR/vllm_$1.pid"
  [ -f "$pidf" ] && kill "$(cat "$pidf")" 2>/dev/null || true
  sleep 15  # chờ giải phóng VRAM
  rm -f "$pidf"
}

drop_model() {
  # HF hub bản mới lưu dữ liệu chung ở hub/blobs, thư mục models--* chỉ chứa symlink -> xóa thư mục rồi dọn blob mồ côi
  rm -rf "$HF_HOME/hub/models--$(echo "$1" | sed 's|/|--|g')"
  python3 - <<'PY'
import os
hub = os.path.join(os.environ['HF_HOME'], 'hub')
used = {os.path.realpath(os.path.join(d, f)) for m in os.listdir(hub) if m.startswith('models--')
        for d, _, fs in os.walk(os.path.join(hub, m)) for f in fs if os.path.islink(os.path.join(d, f))}
freed = 0
for d, _, fs in os.walk(os.path.join(hub, 'blobs')):
    for f in fs:
        p = os.path.join(d, f)
        if os.path.realpath(p) not in used:
            freed += os.path.getsize(p)
            os.remove(p)
print(f'dọn blob không dùng: {freed / 1e9:.1f} GB')
PY
  df -h "$WS" | tail -1
}
