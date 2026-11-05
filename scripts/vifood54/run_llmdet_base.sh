#!/usr/bin/env bash
# Nền LLMDet thật (thay MM-GDINO): B0-LLMDet (zero-shot) + B1-L (công thức B1, khởi tạo từ checkpoint LLMDet).
# Câu hỏi: trọng số đã được LLM giám sát trên GroundingCap-1M có tốt hơn MM-GDINO khi fine-tune món Việt không?
#   LLMDET_CKPT=../huggingface/llmdet/<file swin-t mmdet>.pth bash scripts/vifood54/run_llmdet_base.sh
#   (đường dẫn tương đối từ llmdet_vietnamese_food/; checkpoint Swin-T bản mmdet trong repo HF fushh7/LLMDet)
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/llmdet_vietnamese_food"
W=work_dirs
CFG=configs/grounding_dino_swin_t_vifood54_b1_od.py
CKPT=${LLMDET_CKPT:?đặt LLMDET_CKPT=đường dẫn checkpoint LLMDet Swin-T (mmdet)}
DET=../huggingface/llmdet/llmdet_swin_t_det.pth
best() { ls "$1"/best_coco_bbox_mAP_iter_*.pth 2>/dev/null | head -1; }

mkdir -p "$(dirname "$DET")"
[ -f "$DET" ] || python ../scripts/vifood54/strip_lmm.py "$CKPT" "$DET"

# B0-LLMDet: tên Việt và tên Anh cho lớp novel (so với B0 MM-GDINO 0.010 / 0.065)
for x in "vi $CFG" "en configs/grounding_dino_swin_t_vifood54_ov_test_en.py"; do
  set -- $x
  OUT=$W/vifood54_test_b0_llmdet_$1
  [ -f "$OUT/preds.pkl" ] || python mmdet_test.py "$2" "$DET" --work-dir "$OUT" --out "$OUT/preds.pkl"
done

# B1-L: đúng công thức B1 (16k iter), chỉ đổi khởi tạo
WD=$W/vifood54_b1_llmdet
[ -f "$WD/iter_16000.pth" ] || python mmdet_train.py "$CFG" --work-dir "$WD" --amp --cfg-options load_from="$DET" \
  || echo "!! train dừng sớm, dùng checkpoint tốt nhất"
BEST=$(best "$WD"); [ -n "$BEST" ] || { echo "không có checkpoint B1-L"; exit 1; }
OUT=$W/vifood54_test_b1_llmdet
[ -f "$OUT/preds.pkl" ] || python mmdet_test.py "$CFG" "$BEST" --work-dir "$OUT" --out "$OUT/preds.pkl"

cd "$ROOT"
P=llmdet_vietnamese_food/$W
python scripts/vifood54/analyze_eval.py --gt grounding_data/vifood54/annotations/instances_test.json \
  --pred B0=$P/vifood54_v2_test_b0/preds.pkl --pred B0_LLMDet=$P/vifood54_test_b0_llmdet_vi/preds.pkl \
  --pred B1_v2=$P/vifood54_v2_test_b1_v2/preds.pkl --pred B1_L=$P/$(basename "$OUT")/preds.pkl \
  --out grounding_data/vifood54/EVAL_LLMDET_BASE.md
python scripts/vifood54/eval_ov.py \
  --pred B0_vi=$P/vifood54_v2_test_b0/preds.pkl \
  --pred B0_LLMDet_vi=$P/vifood54_test_b0_llmdet_vi/preds.pkl \
  --pred B0_LLMDet_en=$P/vifood54_test_b0_llmdet_en/preds.pkl \
  --out grounding_data/vifood54/EVAL_OV_LLMDET_B0.md
echo "XONG: EVAL_LLMDET_BASE.md, EVAL_OV_LLMDET_B0.md — B1-L > B1-v2 thì dùng B1-L làm điểm xuất phát cho B5"
