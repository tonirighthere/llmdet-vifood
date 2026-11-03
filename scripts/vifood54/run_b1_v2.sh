#!/usr/bin/env bash
# B1 (OD + negative) trên nhãn đã sửa (crops_review, 30/10) + đánh giá trên test mới.
# Cùng split ảnh với v1 (build giữ split_manifest), nên B1 cũ và mới so được trên cùng tập test.
#   tmux new -s vifood54_b1_v2 'bash scripts/vifood54/run_b1_v2.sh 2>&1 | tee work_dirs_b1_v2.log'
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/llmdet_vietnamese_food"

CFG=configs/grounding_dino_swin_t_vifood54_b1_od.py
WD=work_dirs/vifood54_b1_od_v2
PRETRAIN=../huggingface/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth
OLD_B1=work_dirs/vifood54_b1_od/best_coco_bbox_mAP_iter_16000.pth

if [ ! -f "$WD/iter_16000.pth" ]; then
  python mmdet_train.py "$CFG" --work-dir "$WD" --amp
fi
BEST=$(ls "$WD"/best_coco_bbox_mAP_iter_*.pth | head -1)

run_test() {  # tên, checkpoint
  local out=work_dirs/vifood54_v2_test_$1
  [ -f "$out/preds.pkl" ] || python mmdet_test.py "$CFG" "$2" --work-dir "$out" --out "$out/preds.pkl"
}
run_test b1_v2 "$BEST"
run_test b1_v1 "$OLD_B1"
run_test b0 "$PRETRAIN"

cd "$ROOT"
python scripts/vifood54/analyze_eval.py \
  --gt grounding_data/vifood54/annotations/instances_test.json \
  --pred B0=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b0/preds.pkl \
  --pred B1_v1=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b1_v1/preds.pkl \
  --pred B1_v2=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b1_v2/preds.pkl \
  --out grounding_data/vifood54/EVAL_V2.md --bootstrap 0
echo "XONG: grounding_data/vifood54/EVAL_V2.md"
