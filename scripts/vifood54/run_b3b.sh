#!/usr/bin/env bash
# B3b: fine-tune từ B1-v2 bằng OD + VG caption, rồi đánh giá mAP (test) và grounding câu.
#   tmux new -d -s vifood54_b3b 'bash scripts/vifood54/run_b3b.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_b3b_pipeline.log'
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/llmdet_vietnamese_food"

CFG=configs/grounding_dino_swin_t_vifood54_b3b_ft.py
WD=work_dirs/vifood54_b3b_ft
ls "$WD"/best_coco_bbox_mAP_iter_*.pth >/dev/null 2>&1 || python mmdet_train.py "$CFG" --work-dir "$WD" --amp
BEST=$(ls "$WD"/best_coco_bbox_mAP_iter_*.pth | head -1)
OUT=work_dirs/vifood54_v2_test_b3b
[ -f "$OUT/preds.pkl" ] || python mmdet_test.py "$CFG" "$BEST" --work-dir "$OUT" --out "$OUT/preds.pkl"

PYTHONPATH=. python ../scripts/vifood54/eval_grounding.py \
  --model B1_v2=work_dirs/vifood54_b1_od_v2/best_coco_bbox_mAP_iter_16000.pth \
  --model B3=$(ls work_dirs/vifood54_b3_od_vg/best_coco_bbox_mAP_iter_*.pth | head -1) \
  --model B3b="$BEST" \
  --out ../grounding_data/vifood54/EVAL_GROUNDING_B3B.md

cd "$ROOT"
python scripts/vifood54/analyze_eval.py \
  --gt grounding_data/vifood54/annotations/instances_test.json \
  --pred B1_v2=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b1_v2/preds.pkl \
  --pred B3=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b3/preds.pkl \
  --pred B3b=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b3b/preds.pkl \
  --out grounding_data/vifood54/EVAL_B3B.md --bootstrap 0
echo "XONG: EVAL_B3B.md, EVAL_GROUNDING_B3B.md"
