#!/usr/bin/env bash
# B5: như B3b + LMM của LLMDet (loss caption ảnh + caption vùng), rồi đánh giá mAP (test) và grounding câu.
#   tmux new -d -s vifood54_b5 'bash scripts/vifood54/run_b5.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_b5_pipeline.log'
set -euo pipefail
ulimit -n 65535 2>/dev/null || ulimit -n 4096  # CIFS: "Too many open files" làm B3b dừng ở 7550/8000
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/llmdet_vietnamese_food"
export PYTORCH_ALLOC_CONF=expandable_segments:True

[ -f ../grounding_data/vifood54/annotations/train_od_rfs_lmm.jsonl ] || python ../scripts/vifood54/make_lmm_data.py
CFG=configs/grounding_dino_swin_t_vifood54_b5_lmm.py
WD=work_dirs/vifood54_b5_lmm
ls "$WD"/best_coco_bbox_mAP_iter_*.pth >/dev/null 2>&1 || python mmdet_train.py "$CFG" --work-dir "$WD" --amp || true
BEST=$(ls "$WD"/best_coco_bbox_mAP_iter_*.pth | head -1)
OUT=work_dirs/vifood54_v2_test_b5
# Test bằng config B1 (lmm=None): LMM chỉ dùng lúc train, khóa lmm trong checkpoint bị bỏ qua khi nạp
[ -f "$OUT/preds.pkl" ] || python mmdet_test.py configs/grounding_dino_swin_t_vifood54_b1_od.py "$BEST" --work-dir "$OUT" --out "$OUT/preds.pkl"

PYTHONPATH=. python ../scripts/vifood54/eval_grounding.py \
  --model B1_v2=work_dirs/vifood54_b1_od_v2/best_coco_bbox_mAP_iter_16000.pth \
  --model B3b=work_dirs/vifood54_b3b_ft/best_coco_bbox_mAP_iter_6000.pth \
  --model B5="$BEST" \
  --out ../grounding_data/vifood54/EVAL_GROUNDING_B5.md

cd "$ROOT"
python scripts/vifood54/analyze_eval.py \
  --gt grounding_data/vifood54/annotations/instances_test.json \
  --pred B1_v2=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b1_v2/preds.pkl \
  --pred B3b=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b3b/preds.pkl \
  --pred B5=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b5/preds.pkl \
  --out grounding_data/vifood54/EVAL_B5.md --bootstrap 0
echo "XONG: EVAL_B5.md, EVAL_GROUNDING_B5.md"
