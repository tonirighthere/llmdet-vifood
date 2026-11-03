#!/usr/bin/env bash
# B3 (OD như B1 + VG caption hình thái, trộn ~1:1) + đánh giá trên test, so với B0 và B1-v2.
#   tmux new -d -s vifood54_b3 'bash scripts/vifood54/run_b3.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_b3_pipeline.log'
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/llmdet_vietnamese_food"

CFG=configs/grounding_dino_swin_t_vifood54_b3_od_vg.py
WD=work_dirs/vifood54_b3_od_vg

if [ ! -f "$WD/iter_16000.pth" ]; then
  python mmdet_train.py "$CFG" --work-dir "$WD" --amp
fi
BEST=$(ls "$WD"/best_coco_bbox_mAP_iter_*.pth | head -1)
OUT=work_dirs/vifood54_v2_test_b3
[ -f "$OUT/preds.pkl" ] || python mmdet_test.py "$CFG" "$BEST" --work-dir "$OUT" --out "$OUT/preds.pkl"

cd "$ROOT"
python scripts/vifood54/analyze_eval.py \
  --gt grounding_data/vifood54/annotations/instances_test.json \
  --pred B0=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b0/preds.pkl \
  --pred B1_v2=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b1_v2/preds.pkl \
  --pred B3=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b3/preds.pkl \
  --out grounding_data/vifood54/EVAL_B3.md --bootstrap 0
echo "XONG: grounding_data/vifood54/EVAL_B3.md"
