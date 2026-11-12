#!/usr/bin/env bash
# Giai đoạn 0 — chẩn đoán B5-EN, không train.
#   H1: B5 kém vì đánh giá checkpoint iter 4000 (chọn theo mAP val), chưa kịp học grounding câu?
#   -> đánh giá checkpoint cuối (iter 16000) trên test (mAP + grounding), và grounding trên VAL cho mọi model
#      để từ nay chọn checkpoint theo L2 R@1 val thay vì chỉ mAP.
#   tmux new -d -s training 'bash scripts/vifood54/run_phase0_b5_diag.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_en_b5_phase0.log'
set -euo pipefail
ulimit -n 65535 2>/dev/null || ulimit -n 4096  # CIFS: "Too many open files"
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
A=$ROOT/grounding_data/vifood54/annotations_en
OUT=$ROOT/grounding_data/vifood54
cd "$ROOT/llmdet_vietnamese_food"
export PYTORCH_ALLOC_CONF=expandable_segments:True

CFG=configs/grounding_dino_swin_t_vifood54_b1_od_en.py   # detector thuần, 54 lớp EN
B1=work_dirs/vifood54_b1_od_en/best_coco_bbox_mAP_iter_16000.pth
B3B=work_dirs/vifood54_b3b_ft_en/best_coco_bbox_mAP_iter_7000.pth
B5=work_dirs/vifood54_b5_lmm_en/best_det.pth           # iter 4000
B5L=work_dirs/vifood54_b5_lmm_en/last_det.pth          # iter 16000
TEST_L=work_dirs/vifood54_en_test_b5_last

# 1. bỏ Qwen/connector khỏi checkpoint cuối
[ -f "$B5L" ] || python ../scripts/vifood54/strip_lmm.py work_dirs/vifood54_b5_lmm_en/iter_16000.pth "$B5L"

# 2. mAP test của checkpoint cuối
[ -f "$TEST_L/preds.pkl" ] || python mmdet_test.py "$CFG" "$B5L" --work-dir "$TEST_L" --out "$TEST_L/preds.pkl"

# 3. grounding test của checkpoint cuối (B1/B3b/B5 best đã có trong EVAL_GROUNDING_EN.md)
PYTHONPATH=. python ../scripts/vifood54/eval_grounding.py --lang en --config "$CFG" --ann "$A/test_vg_cap.jsonl" \
  --model B5_EN_last="$B5L" --out "$OUT/EVAL_GROUNDING_EN_B5LAST.md"

# 4. grounding VAL cho cả 4 model -> thước đo chọn checkpoint
PYTHONPATH=. python ../scripts/vifood54/eval_grounding.py --lang en --config "$CFG" --ann "$A/val_vg_cap.jsonl" \
  --model B1_EN="$B1" --model B3b_EN="$B3B" --model B5_EN_it4000="$B5" --model B5_EN_it16000="$B5L" \
  --out "$OUT/EVAL_GROUNDING_EN_VAL.md"

# 5. mAP test so sánh (cùng GT)
cd "$ROOT"
python scripts/vifood54/analyze_eval.py --gt "$A/instances_test.json" \
  --pred B3b_EN=llmdet_vietnamese_food/work_dirs/vifood54_en_test_b3b/preds.pkl \
  --pred B5_EN_it4000=llmdet_vietnamese_food/work_dirs/vifood54_en_test_b5/preds.pkl \
  --pred B5_EN_it16000=llmdet_vietnamese_food/$TEST_L/preds.pkl \
  --out grounding_data/vifood54/EVAL_EN_B5LAST.md --bootstrap 0
echo "XONG GIAI ĐOẠN 0: EVAL_GROUNDING_EN_B5LAST.md, EVAL_GROUNDING_EN_VAL.md, EVAL_EN_B5LAST.md"
