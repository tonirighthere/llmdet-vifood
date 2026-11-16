#!/usr/bin/env bash
# Chạy MỘT LẦN trên máy thuê (Vast.ai), trong terminal của instance, sau khi đã chép caption_pack.tar lên /workspace.
#   export HF_TOKEN=hf_...      # bắt buộc nếu model kiểm chứng là Gemma (repo có cổng chấp nhận điều khoản)
#   bash setup.sh               # (tải riêng file này, hoặc chạy từ repo đã clone)
set -euo pipefail
WS=${WS:-/workspace}
BRANCH=${BRANCH:-truong/b5-en-v2}
cd "$WS"
[ -d llmdet-vifood ] || git clone --depth 1 -b "$BRANCH" https://github.com/tonirighthere/llmdet-vifood.git
cd llmdet-vifood
[ -f "$WS/caption_pack.tar" ] || { echo "chưa có $WS/caption_pack.tar (chép từ server nhóm: xem RUNBOOK.md)"; exit 1; }
[ -f grounding_data/vifood54/annotations_en/train_od.jsonl ] || tar -xf "$WS/caption_pack.tar"
python3 - <<'PY'
import importlib, subprocess, sys
need = []
try:
    import vllm
    from packaging.version import Version
    if Version(vllm.__version__.split('+')[0]) < Version('0.11.0'):
        need.append('vllm>=0.11.0')
    print('vllm', vllm.__version__)
except ImportError:
    need.append('vllm>=0.11.0')
for m in ('PIL', 'huggingface_hub'):
    try:
        importlib.import_module(m)
    except ImportError:
        need.append({'PIL': 'pillow'}.get(m, m))
if need:
    print('cài:', need)
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', *need])
PY
# Template vLLM của Vast tự chạy model trong VLLM_MODEL (chiếm VRAM + cổng 8000/18000) -> tắt hẳn, script tự bật model riêng (cổng 9100/9101)
supervisorctl stop vllm 2>/dev/null || true
pkill -f "vllm serve" 2>/dev/null || true
sleep 5
USED=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits | head -1)
[ "${USED:-0}" -lt 2000 ] || { echo "!! GPU còn bận ${USED} MiB — xem nvidia-smi, tắt tiến trình đó rồi chạy lại setup.sh"; exit 1; }
export HF_HOME=${HF_HOME:-$WS/hf}
[ -z "${HF_TOKEN:-}" ] || python3 -c "from huggingface_hub import login; login('$HF_TOKEN')"
python3 scripts/vifood54/captions/test_caption_v2.py > /dev/null && echo "test CPU caption_v2: ok"
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
df -h "$WS" | tail -1
echo "XONG setup. Tiếp: bash scripts/vifood54/captions/vast/run_pilot.sh"
