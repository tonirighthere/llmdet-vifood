#!/usr/bin/env bash
# Hàm dùng chung: bật / tắt máy chủ vLLM cho một model. `source` file này, không chạy trực tiếp.
#   start_vllm <model> <port>   -> chạy nền, chờ tới khi /v1/models trả lời (gồm cả thời gian tải model lần đầu)
#   stop_vllm <port>
#   drop_model <model>          -> xóa model khỏi cache HF để giải phóng ổ (ổ máy thuê có hạn)
WS=${WS:-/workspace}
export HF_HOME=${HF_HOME:-$WS/hf}
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
  rm -rf "$HF_HOME/hub/models--$(echo "$1" | sed 's|/|--|g')"
  df -h "$WS" | tail -1
}
