#!/usr/bin/env bash
# Train có giám sát LLM (B5 / OV-W) -> bỏ LLM khỏi checkpoint -> test -> đánh giá.
# Cần trước: caption VLM + attach (xem sessions/2026-11-05_phase5_lmm_setup.md).
#   bash scripts/vifood54/run_lmm.sh b5            # B5  (từ B1-v2, so với B3b)
#   bash scripts/vifood54/run_lmm.sh ov            # OV-W (từ OV-S1, caption có tên novel)
#   bash scripts/vifood54/run_lmm.sh ov_nonovel    # ablation OV-W: caption bỏ câu có tên novel
#   B5_FROM=work_dirs/vifood54_b1_llmdet/best_...pth bash scripts/vifood54/run_lmm.sh b5   # B5 từ B1-L
#   SMOKE=1 bash scripts/vifood54/run_lmm.sh b5    # 40 iter kiểm tra end-to-end (VRAM, loss LMM), không đánh giá
#   tmux new -d -s vifood54_b5 'bash scripts/vifood54/run_lmm.sh b5 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_b5_pipeline.log'
set -uo pipefail
MODE=${1:?b5 | ov | ov_nonovel}
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/llmdet_vietnamese_food"
W=work_dirs
TEST_CFG=configs/grounding_dino_swin_t_vifood54_b1_od.py   # test 54 lớp, không lmm
best() { ls "$1"/best_coco_bbox_mAP_iter_*.pth 2>/dev/null | head -1; }

case "$MODE" in
  b5)         CFG=configs/grounding_dino_swin_t_vifood54_b5_lmm.py; WD=$W/vifood54_b5_lmm; ANN=../grounding_data/vifood54/annotations/train_od_rfs_lmm.jsonl
              # mặc định từ B1-v2 (so thẳng với B3b); B5_FROM=<ckpt B1-L> nếu B1-L tốt hơn (khi đó so với B3b chạy lại từ B1-L)
              EXTRA=(); [ -n "${B5_FROM:-}" ] && EXTRA=(--cfg-options load_from="$B5_FROM") ;;
  ov)         CFG=configs/grounding_dino_swin_t_vifood54_ov_s2_lmm.py; WD=$W/vifood54_ov_s2_lmm; ANN=../grounding_data/vifood54/annotations_ov/train_od_rfs_lmm.jsonl ;;
  ov_nonovel) CFG=configs/grounding_dino_swin_t_vifood54_ov_s2_lmm_nonovel.py; WD=$W/vifood54_ov_s2_lmm_nonovel; ANN=../grounding_data/vifood54/annotations_ov/train_od_rfs_lmm_nonovel.jsonl ;;
  *) echo "MODE không hợp lệ: $MODE"; exit 1 ;;
esac
[ -f "$ANN" ] || { echo "Thiếu $ANN -> chạy scripts/vifood54/captions/vlm_captions.py attach trước"; exit 1; }
if [ "$MODE" != b5 ]; then
  S1=$(best $W/vifood54_ov_s1_od); [ -n "$S1" ] || { echo "thiếu checkpoint OV-S1 (run_ov.sh)"; exit 1; }
  EXTRA=(--cfg-options load_from="$S1")
fi

if [ "${SMOKE:-0}" = 1 ]; then
  python mmdet_train.py "$CFG" --work-dir "${WD}_smoke" --amp \
    --cfg-options train_cfg.max_iters=40 train_cfg.val_interval=40 default_hooks.logger.interval=5 \
    ${EXTRA[@]:1}
  echo "SMOKE xong: kiểm tra loss_lmm_image / d1.loss_lmm_region trong log và VRAM"; exit 0
fi

[ -f "$WD/iter_8000.pth" ] || python mmdet_train.py "$CFG" --work-dir "$WD" --amp "${EXTRA[@]}" \
  || echo "!! train dừng sớm, dùng checkpoint tốt nhất"
BEST=$(best "$WD"); [ -n "$BEST" ] || { echo "không có checkpoint"; exit 1; }
DET="$WD/best_det.pth"
python ../scripts/vifood54/strip_lmm.py "$BEST" "$DET"
OUT=$W/vifood54_test_$MODE
[ -f "$OUT/preds.pkl" ] || python mmdet_test.py "$TEST_CFG" "$DET" --work-dir "$OUT" --out "$OUT/preds.pkl"

if [ "$MODE" = b5 ]; then
  PYTHONPATH=. python ../scripts/vifood54/eval_grounding.py \
    --model B3b="$(best $W/vifood54_b3b_ft)" --model B5="$DET" \
    --out ../grounding_data/vifood54/EVAL_GROUNDING_B5.md
  cd "$ROOT"
  python scripts/vifood54/analyze_eval.py --gt grounding_data/vifood54/annotations/instances_test.json \
    --pred B1_v2=llmdet_vietnamese_food/$W/vifood54_v2_test_b1_v2/preds.pkl \
    --pred B3b=llmdet_vietnamese_food/$W/vifood54_v2_test_b3b/preds.pkl \
    --pred B5=llmdet_vietnamese_food/$OUT/preds.pkl \
    --out grounding_data/vifood54/EVAL_B5.md
  echo "XONG: EVAL_B5.md, EVAL_GROUNDING_B5.md"
else
  cd "$ROOT"
  P=llmdet_vietnamese_food/$W
  ARGS=(--pred B0=$P/vifood54_v2_test_b0/preds.pkl --pred OV_S1_od=$P/vifood54_ov_test_s1/preds.pkl
        --pred OV_S2_od_vg=$P/vifood54_ov_test_s2/preds.pkl)
  for m in ov ov_nonovel; do
    [ -f "$P/vifood54_test_$m/preds.pkl" ] && ARGS+=(--pred "OV_W_${m}=$P/vifood54_test_$m/preds.pkl")
  done
  python scripts/vifood54/eval_ov.py "${ARGS[@]}" --pred 'B3b*'=$P/vifood54_v2_test_b3b/preds.pkl \
    --out grounding_data/vifood54/EVAL_OV_LMM.md
  echo "XONG: EVAL_OV_LMM.md"
fi
