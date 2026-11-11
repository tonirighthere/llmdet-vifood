#!/usr/bin/env bash
# Nền LLMDet, bản TIẾNG ANH (song song run_llmdet_base.sh của Pha 5, prompt tên Việt):
#   B0-LLMDet-EN: zero-shot LLMDet Swin-T với 54 tên EN;  B1-L-EN: công thức B1-EN, khởi tạo từ LLMDet thay MM-GDINO.
# Câu hỏi: trọng số LLMDet (GroundingCap-1M) có tốt hơn MM-GDINO khi fine-tune món Việt bằng prompt tiếng Anh?
#   bash scripts/vifood54/run_llmdet_base_en.sh     # cần huggingface/llmdet/tiny.pth (fushh7/LLMDet)
set -uo pipefail
ulimit -n 65535 2>/dev/null || ulimit -n 4096
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/llmdet_vietnamese_food"
export PYTORCH_ALLOC_CONF=expandable_segments:True
W=work_dirs
CFG=configs/grounding_dino_swin_t_vifood54_b1_od_en.py
DET=../huggingface/llmdet/llmdet_swin_t_det.pth
best() { ls "$1"/best_coco_bbox_mAP_iter_*.pth 2>/dev/null | head -1; }
[ -f "$DET" ] || python ../scripts/vifood54/strip_lmm.py ../huggingface/llmdet/tiny.pth "$DET"

OUT0=$W/vifood54_en_test_b0_llmdet
[ -f "$OUT0/preds.pkl" ] || python mmdet_test.py "$CFG" "$DET" --work-dir "$OUT0" --out "$OUT0/preds.pkl"

WD=$W/vifood54_b1_llmdet_en
[ -f "$WD/iter_16000.pth" ] || python mmdet_train.py "$CFG" --work-dir "$WD" --amp --cfg-options load_from="$DET" \
  || echo "!! train dừng sớm, dùng checkpoint tốt nhất"
BEST=$(best "$WD"); [ -n "$BEST" ] || { echo "không có checkpoint B1-L-EN"; exit 1; }
OUT=$W/vifood54_en_test_b1_llmdet
[ -f "$OUT/preds.pkl" ] || python mmdet_test.py "$CFG" "$BEST" --work-dir "$OUT" --out "$OUT/preds.pkl"

cd "$ROOT"
P=llmdet_vietnamese_food/$W
ARGS=(--pred B0_MMGDINO_VI=$P/vifood54_v2_test_b0/preds.pkl --pred B0_LLMDet_EN=$P/vifood54_en_test_b0_llmdet/preds.pkl
      --pred B1_v2_VI=$P/vifood54_v2_test_b1_v2/preds.pkl)
[ -f "$P/vifood54_en_test_b1/preds.pkl" ] && ARGS+=(--pred B1_EN=$P/vifood54_en_test_b1/preds.pkl)
ARGS+=(--pred B1_L_EN=$P/vifood54_en_test_b1_llmdet/preds.pkl)
python scripts/vifood54/analyze_eval.py --gt grounding_data/vifood54/annotations_en/instances_test.json \
  "${ARGS[@]}" --out grounding_data/vifood54/EVAL_LLMDET_BASE_EN.md --bootstrap 0
echo "XONG: EVAL_LLMDET_BASE_EN.md — B1-L-EN > B1-EN thì dùng B1-L-EN làm điểm xuất phát cho B3b-EN/B5-EN"
