#!/usr/bin/env bash
# Cài đặt máy thuê để train B5b / OV-S1 / OV-W (chạy MỘT LẦN, ~30-60 phút; chạy lại được, bước đã xong sẽ bỏ qua).
# Template vifood-train: image vastai/pytorch:2.10.0-cuda-12.8.1-py311-24.04-2026-10-23 (giống server nhóm: torch 2.10 cu128, py3.11)
#   git clone --depth 1 -b truong/b5-en-v2 https://github.com/tonirighthere/llmdet-vifood.git /workspace/llmdet-vifood
#   bash /workspace/llmdet-vifood/scripts/vifood54/vast_train/setup_train.sh 2>&1 | tee /workspace/setup.log
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
cd "$ROOT"
DL=${DL:-/workspace/dl}
mkdir -p "$DL"
log() { echo; echo "== $(date +%H:%M:%S) $*"; }
# Drive (thư mục vifood-caption-vast, chia sẻ "bất kỳ ai có link")
declare -A ZIPS=(
  [vifood54_dataset.zip]=1yq8ScWV6iIBhHdGlbn0-eJbUHhf6zTMQ
  [vifood54_pretrained.zip]=1NDlOEs6TNZi8QkB1sfQR8CLMJFZrvG8Y
  [vifood54_checkpoints_en.zip]=1aalv-G_1Bp-7iFTvhIWydYnOycI_tJvu
)

log "1/7 công cụ hệ thống"
need=(); for c in unzip tmux; do command -v $c >/dev/null || need+=($c); done
[ ${#need[@]} -eq 0 ] || { apt-get update -qq && apt-get install -y -qq "${need[@]}"; }
command -v nvcc >/dev/null || export PATH=/usr/local/cuda/bin:$PATH
nvcc --version | tail -1 || { echo "!! không có nvcc (cần image bản đầy đủ CUDA, không phải 'mini') để build mmcv"; exit 1; }

log "2/7 kiểm tra torch / GPU"
python - <<'PY'
import torch
assert torch.__version__.startswith('2.10'), f'torch {torch.__version__} (server nhóm dùng 2.10.0+cu128)'
assert torch.cuda.is_available(), 'không thấy GPU'
p = torch.cuda.get_device_properties(0)
print(f'torch {torch.__version__} cuda {torch.version.cuda} | {p.name} {p.total_memory / 2**30:.0f} GB sm_{p.major}{p.minor}')
assert p.total_memory / 2**30 >= 22, 'GPU < 24 GB: server nhóm (RTX 3090 24 GB) là mức tối thiểu đã chạy được'
PY

log "3/7 thư viện Python (phiên bản theo pip_freeze_server.txt)"
pip install -q "numpy==2.3.5" "transformers==4.57.1" "tokenizers==0.22.2" "huggingface_hub==0.36.1" \
  "safetensors==0.7.0" "accelerate==1.11.0" "peft==0.17.1" "timm==1.0.29" "mmengine==0.10.7" "fairscale==0.4.13" \
  "lvis==0.5.3" "pycocotools==2.0.11" "jsonlines==4.0.0" "nltk==3.10.3" "sentencepiece==0.2.1" "einops==0.8.2" \
  "scipy==1.17.0" "shapely==2.1.2" "terminaltables==3.1.10" "addict==2.4.0" "yapf==0.43.0" "termcolor==3.3.0" \
  "rich==13.9.4" "matplotlib==3.10.8" "pandas==2.3.3" "PyYAML==6.0.3" "regex==2026.1.15" "opencv-python-headless" \
  "gdown==6.1.0" ninja psutil
python -c "import nltk; [nltk.download(p, quiet=True) for p in ('punkt', 'punkt_tab', 'averaged_perceptron_tagger', 'averaged_perceptron_tagger_eng')]"

log "4/7 mmcv 2.2.0 (build có CUDA ops cho đúng GPU này, ~5-15 phút)"
if python -c "from mmcv.ops import MultiScaleDeformableAttention" 2>/dev/null; then
  echo "mmcv đã có"
else
  # Không có wheel mmcv cho torch 2.10 -> build từ source. Sửa chuẩn C++14 -> C++17 (torch >= 2.1 bắt buộc C++17).
  ARCH=$(python -c "import torch; m, n = torch.cuda.get_device_capability(); print(f'{m}.{n}')")
  SRC=/workspace/mmcv_src
  rm -rf "$SRC" && mkdir -p "$SRC"
  URL=$(python -c "import json, urllib.request as u; d = json.load(u.urlopen('https://pypi.org/pypi/mmcv/2.2.0/json')); print([x['url'] for x in d['urls'] if x['packagetype'] == 'sdist'][0])")
  curl -sSL "$URL" -o "$SRC/mmcv-2.2.0.tar.gz"   # sdist; KHÔNG dùng pip download (setup.py cần torch, môi trường cô lập không có)
  tar -xzf "$SRC/mmcv-2.2.0.tar.gz" -C "$SRC"
  cd "$SRC"/mmcv-2.2.0
  sed -i 's/c++14/c++17/g' setup.py
  echo "  setup.py: $(grep -c 'c++17' setup.py) chỗ C++17, $(grep -c 'c++14' setup.py) chỗ C++14 | arch $ARCH | $(nproc) CPU"
  MMCV_WITH_OPS=1 FORCE_CUDA=1 TORCH_CUDA_ARCH_LIST="$ARCH" MAX_JOBS=$(nproc) \
    pip install -v --no-build-isolation . > /workspace/mmcv_build.log 2>&1 \
    || { echo "!! build mmcv lỗi -> gửi Claude 40 dòng cuối:"; grep -nE "error|Error" /workspace/mmcv_build.log | tail -20; tail -20 /workspace/mmcv_build.log; exit 1; }
  cd "$ROOT"
fi
python - <<'PY'
import mmcv, torch
from mmcv.ops import MultiScaleDeformableAttention
attn = MultiScaleDeformableAttention(embed_dims=32, num_heads=4, num_levels=1, num_points=2, batch_first=True).cuda()
# query: (B=1, Nq=5, C=32); value: (B=1, H*W=16, C=32); 1 mức đặc trưng 4x4
q, v = torch.rand(1, 5, 32).cuda(), torch.rand(1, 16, 32).cuda()
out = attn(q, value=v, reference_points=torch.rand(1, 5, 1, 2).cuda(),
           spatial_shapes=torch.tensor([[4, 4]]).cuda(), level_start_index=torch.tensor([0]).cuda())
assert out.shape == (1, 5, 32), out.shape
print('mmcv', mmcv.__version__, '| MultiScaleDeformableAttention CUDA ok')
PY

log "5/7 tải + giải nén dữ liệu (~7 GB)"
for z in "${!ZIPS[@]}"; do
  [ -s "$DL/$z.done" ] && continue
  [ -s "$DL/$z" ] || python -m gdown "${ZIPS[$z]}" -O "$DL/$z"
  unzip -q -o "$DL/$z" -d "$ROOT" -x 'README_DATA.md'
  echo ok > "$DL/$z.done"
  echo "  giải nén xong $z"
done
python scripts/vifood54/vast_train/check_train_data.py --stage data --load-ckpt

log "6/7 caption v2 -> dữ liệu train (B5b: _lmm_v2; OV-W: annotations_ov_en/*_lmm)"
export VIFOOD_LANG=en
ACCEPT=approved,edited,auto,flagged   # 'flagged' ở bản full chủ yếu là 'caption ngắn' (ảnh 1 món), vẫn đã qua kiểm chứng
python scripts/vifood54/captions/caption_v2.py publish --run full_Qwen3_VL_32B --force
python scripts/vifood54/captions/vlm_captions.py attach --suffix _lmm_v2 --accept "$ACCEPT"
[ -f grounding_data/vifood54/annotations_ov_en/train_od_rfs.jsonl ] || python scripts/vifood54/make_ov_split.py --en
python scripts/vifood54/captions/vlm_captions.py attach --ov --accept "$ACCEPT"

log "7/7 kiểm tra cuối"
python scripts/vifood54/vast_train/check_train_data.py --stage ready
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
df -h /workspace | tail -1
echo "XONG setup. Tiếp (trong tmux):  bash scripts/vifood54/vast_train/run_all.sh 2>&1 | tee /workspace/run_all.log"
