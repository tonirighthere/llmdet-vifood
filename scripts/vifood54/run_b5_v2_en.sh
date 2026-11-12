#!/usr/bin/env bash
# B5-EN v2: bước 1 căn chỉnh connector/LoRA (detector đứng yên, 2000 iter) -> bước 2 đúng lịch B3b-EN (batch 2, 8000 iter)
# -> đánh giá CẢ checkpoint tốt nhất (mAP val) và checkpoint cuối: mAP test (+ AP theo tần suất lớp, bootstrap CI) và
# grounding câu, đặt cạnh B1-EN / B3b-EN / B5-EN lần 1. Chạy lại được: bước nào đã có kết quả thì bỏ qua.
#   tmux new -d -s training 'bash scripts/vifood54/run_b5_v2_en.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_b5_v2_en.log'
#   SMOKE=1 bash scripts/vifood54/run_b5_v2_en.sh   # 40 iter mỗi bước: kiểm tra VRAM batch 2 và loss LLM, không đánh giá
#   bash scripts/vifood54/run_b5_v2_en.sh b         # B5b: caption v2 (caption_v2.py -> attach --suffix _lmm_v2); mặc định 'a' = caption hiện tại
set -euo pipefail
ulimit -n 65535 2>/dev/null || ulimit -n 4096  # CIFS: "Too many open files"
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
A=$ROOT/grounding_data/vifood54/annotations_en
cd "$ROOT/llmdet_vietnamese_food"
export PYTORCH_ALLOC_CONF=expandable_segments:True
W=work_dirs
TEST_CFG=configs/grounding_dino_swin_t_vifood54_b1_od_en.py   # detector thuần, 54 lớp EN
ALIGN_CFG=configs/grounding_dino_swin_t_vifood54_b5_align_en.py
VARIANT=${1:-a}
case "$VARIANT" in
  a) B5_CFG=configs/grounding_dino_swin_t_vifood54_b5_lmm_en_v2.py;  S2=$W/vifood54_b5_lmm_en_v2;  LMM=train_vg_cap_rfs_lmm.jsonl ;;
  b) B5_CFG=configs/grounding_dino_swin_t_vifood54_b5_lmm_en_v2b.py; S2=$W/vifood54_b5_lmm_en_v2b; LMM=train_vg_cap_rfs_lmm_v2.jsonl ;;
  *) echo "biến thể không hợp lệ: $VARIANT (a | b)"; exit 1 ;;
esac
TAG=B5${VARIANT}
S1=$W/vifood54_b5_align_en   # bước căn chỉnh dùng chung cho a và b (caption hiện tại)
best() { ls "$1"/best_coco_bbox_mAP_iter_*.pth 2>/dev/null | head -1; }

[ -f "$A/train_vg_cap_rfs_lmm.jsonl" ] || { echo "thiếu *_lmm.jsonl -> python scripts/vifood54/captions/build_lmm_en.py"; exit 1; }
[ -f "$A/$LMM" ] || { echo "thiếu $LMM -> VIFOOD_LANG=en python scripts/vifood54/captions/vlm_captions.py attach --suffix _lmm_v2"; exit 1; }

if [ "${SMOKE:-0}" = 1 ]; then
  O=(train_cfg.max_iters=40 train_cfg.val_interval=40 default_hooks.logger.interval=5 default_hooks.checkpoint.interval=40)
  python mmdet_train.py "$ALIGN_CFG" --work-dir "${S1}_smoke" --amp --cfg-options "${O[@]}"
  python mmdet_train.py "$B5_CFG" --work-dir "${S2}_smoke" --amp --cfg-options "${O[@]}" load_from="${S1}_smoke/iter_40.pth"
  echo "SMOKE xong: xem memory và loss_lmm_image / d1.loss_lmm_region trong log của ${S1}_smoke, ${S2}_smoke"; exit 0
fi

# ── bước 1: căn chỉnh (detector không đổi) ──
[ -f "$S1/iter_2000.pth" ] || python mmdet_train.py "$ALIGN_CFG" --work-dir "$S1" --amp
# ── bước 2: train chung grounding + 2 loss LLM ──
[ -f "$S2/iter_8000.pth" ] || python mmdet_train.py "$B5_CFG" --work-dir "$S2" --amp \
  || echo "!! bước 2 dừng sớm, dùng checkpoint đã lưu"
BEST=$(best "$S2"); [ -n "$BEST" ] || { echo "không có checkpoint bước 2"; exit 1; }
LAST=$(ls -t "$S2"/iter_*.pth | head -1)
echo "best = $BEST ; last = $LAST"

MODELS=(--model B3b_EN="$(best $W/vifood54_b3b_ft_en)")
[ -f $W/vifood54_b5_lmm_en/best_det.pth ] && MODELS+=(--model B5_EN_v1=$W/vifood54_b5_lmm_en/best_det.pth)
PREDS=(--pred B1_EN=llmdet_vietnamese_food/$W/vifood54_en_test_b1/preds.pkl
       --pred B3b_EN=llmdet_vietnamese_food/$W/vifood54_en_test_b3b/preds.pkl)
[ -f $W/vifood54_en_test_b5/preds.pkl ] && PREDS+=(--pred B5_EN_v1=llmdet_vietnamese_food/$W/vifood54_en_test_b5/preds.pkl)
if [ "$VARIANT" = b ]; then  # đặt B5a cạnh B5b nếu đã chạy
  for k in best last; do
    [ -f $W/vifood54_b5_lmm_en_v2/${k}_det.pth ] && MODELS+=(--model B5a_$k=$W/vifood54_b5_lmm_en_v2/${k}_det.pth) || true
    [ -f $W/vifood54_en_test_b5v2_$k/preds.pkl ] && PREDS+=(--pred B5a_$k=llmdet_vietnamese_food/$W/vifood54_en_test_b5v2_$k/preds.pkl) || true
  done
fi
SUF=$([ "$VARIANT" = a ] && echo "" || echo "b")
for x in "best $BEST" "last $LAST"; do
  set -- $x
  DET=$S2/${1}_det.pth
  OUT=$W/vifood54_en_test_b5v2${SUF}_$1
  [ -f "$DET" ] || python ../scripts/vifood54/strip_lmm.py "$2" "$DET"
  [ -f "$OUT/preds.pkl" ] || python mmdet_test.py "$TEST_CFG" "$DET" --work-dir "$OUT" --out "$OUT/preds.pkl"
  MODELS+=(--model ${TAG}_$1="$DET")
  PREDS+=(--pred ${TAG}_$1=llmdet_vietnamese_food/$OUT/preds.pkl)
done

PYTHONPATH=. python ../scripts/vifood54/eval_grounding.py --lang en --config "$TEST_CFG" --ann "$A/test_vg_cap.jsonl" \
  "${MODELS[@]}" --out ../grounding_data/vifood54/EVAL_GROUNDING_EN_B5V2${SUF^^}.md

cd "$ROOT"
python scripts/vifood54/analyze_eval.py --gt "$A/instances_test.json" "${PREDS[@]}" \
  --baseline B3b_EN --out grounding_data/vifood54/EVAL_EN_B5V2${SUF^^}.md --bootstrap "${BOOTSTRAP:-300}"
echo "XONG: EVAL_EN_B5V2${SUF^^}.md (mAP + CI + so ghép cặp với B3b-EN + AP theo tần suất lớp), EVAL_GROUNDING_EN_B5V2${SUF^^}.md"
