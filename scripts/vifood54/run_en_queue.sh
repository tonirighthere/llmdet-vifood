#!/usr/bin/env bash
# Hàng đợi GPU cho pipeline tiếng Anh (GPU 24 GB dùng chung, ~11 GB bị dịch vụ khác chiếm -> chạy tuần tự):
#   1) chờ tmux vifood54_en (B1-EN -> B3b-EN -> đánh giá) xong; đo VRAM thật của B5-EN (40 iter, batch 1 và 2)
#   2) nền LLMDet EN: B0-LLMDet-EN (zero-shot) + B1-L-EN (16k iter)
#   3) Gemma (huggingface/gemma-4-12B-it, 4-bit, chỉ văn bản): dịch 3052 đặc điểm VLM thêm -> translations_vi_en.json
#      (KHÔNG tự build lại caption: B3b-EN đã train với caption hiện tại)
#   4) Gemma sinh caption VLM tiếng Anh cho loss LMM (Pha 5, ~7 h) -> annotations_en/vlm_captions.jsonl
# Dừng ở đó: duyệt tay (review_captions.py) và B5-EN (~20 GB VRAM, tắt app) do người chạy quyết định.
#   tmux new -d -s training 'bash scripts/vifood54/run_en_queue.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_en_queue.log'
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT"
GEMMA=$ROOT/huggingface/gemma-4-12B-it
PY_GEMMA=$HOME/miniconda/envs/gemma_env/bin/python

while tmux has-session -t =training 2>/dev/null; do sleep 300; done

echo "[queue] $(date) vifood54_en xong -> đo VRAM B5-EN"
(
  cd llmdet_vietnamese_food
  B1=$(ls work_dirs/vifood54_b1_od_en/best_coco_bbox_mAP_iter_*.pth | head -1)
  for bs in 1 2; do
    WD=work_dirs/vifood54_b5_en_probe_bs$bs
    python mmdet_train.py configs/grounding_dino_swin_t_vifood54_b5_lmm_en.py --work-dir "$WD" --amp \
      --cfg-options load_from="$B1" train_dataloader.batch_size=$bs optim_wrapper.accumulative_counts=$((4 / bs)) \
      train_cfg.max_iters=40 train_cfg.val_interval=100000 default_hooks.logger.interval=10 \
      default_hooks.checkpoint.interval=100000 > "$WD.log" 2>&1
    MEM=$(grep -oE "memory: [0-9]+" "$WD.log" | awk '{print $2}' | sort -n | tail -1)
    LMM=$(grep -oE "loss_lmm_image: [0-9.]+" "$WD.log" | tail -1)
    echo "[queue] B5-EN batch $bs: max_memory_allocated ${MEM:-OOM/lỗi} MiB, $LMM (log $WD.log)" \
      | tee -a work_dirs/vifood54_b5_en_probe.txt
    rm -f "$WD"/*.pth  # save_last ghi checkpoint có Qwen (~2 GB)
  done
)
echo "[queue] $(date) -> nền LLMDet EN"
bash scripts/vifood54/run_llmdet_base_en.sh

echo "[queue] $(date) dịch đặc điểm VLM bằng Gemma"
HF_HUB_OFFLINE=1 $PY_GEMMA -u scripts/vifood54/captions/translate_en.py --load-4bit --model "$GEMMA"

echo "[queue] $(date) caption VLM tiếng Anh (Pha 5)"
VIFOOD_LANG=en HF_HUB_OFFLINE=1 $PY_GEMMA -u scripts/vifood54/captions/vlm_captions.py generate --load-4bit --model "$GEMMA"
echo "[queue] $(date) XONG — tiếp theo: VIFOOD_LANG=en review_captions.py, rồi RUN_B5=1 run_en.sh"
