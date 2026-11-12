#!/usr/bin/env bash
# Open-vocabulary TIẾNG ANH: OV-S1-EN (mốc, 46 lớp base) -> OV-W-EN (căn chỉnh 2000 iter + train chung 8000 iter, caption có
# tên novel) [-> ablation bỏ tên novel] -> test đủ 54 tên EN -> AP_base / AP_novel (EVAL_OV_EN.md).
#   bash scripts/vifood54/run_ov_en.sh s1          # chỉ mốc OV-S1-EN (~4 h GPU), không cần caption v2
#   bash scripts/vifood54/run_ov_en.sh w           # OV-W-EN (cần S1 + *_lmm.jsonl trong annotations_ov_en/)
#   bash scripts/vifood54/run_ov_en.sh nonovel     # ablation
#   bash scripts/vifood54/run_ov_en.sh eval        # chỉ gộp bảng từ các preds đã có
set -euo pipefail
ulimit -n 65535 2>/dev/null || ulimit -n 4096
MODE=${1:?s1 | w | nonovel | eval}
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
OV=$ROOT/grounding_data/vifood54/annotations_ov_en
EN=$ROOT/grounding_data/vifood54/annotations_en
cd "$ROOT"
[ -f "$OV/train_od_rfs.jsonl" ] || python scripts/vifood54/make_ov_split.py --en
cd "$ROOT/llmdet_vietnamese_food"
export PYTORCH_ALLOC_CONF=expandable_segments:True
W=work_dirs
TEST_CFG=configs/grounding_dino_swin_t_vifood54_b1_od_en.py   # detector thuần, prompt 54 tên EN
PRE=../huggingface/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth
best() { ls "$1"/best_coco_bbox_mAP_iter_*.pth 2>/dev/null | head -1; }
test_ckpt() {  # <tên> <checkpoint detector>
  local out=$W/vifood54_ov_en_test_$1
  [ -f "$out/preds.pkl" ] || python mmdet_test.py "$TEST_CFG" "$2" --work-dir "$out" --out "$out/preds.pkl"
}

S1=$W/vifood54_ov_s1_od_en
if [ "$MODE" = s1 ]; then
  [ -f "$S1/iter_16000.pth" ] || python mmdet_train.py configs/grounding_dino_swin_t_vifood54_ov_s1_od_en.py \
    --work-dir "$S1" --amp || echo "!! S1 dừng sớm, dùng checkpoint tốt nhất"
  test_ckpt b0 "$PRE"
  test_ckpt s1 "$(best "$S1")"
elif [ "$MODE" = w ] || [ "$MODE" = nonovel ]; then
  B1=$(best "$S1"); [ -n "$B1" ] || { echo "chưa có OV-S1-EN: bash scripts/vifood54/run_ov_en.sh s1"; exit 1; }
  if [ "$MODE" = w ]; then SUF=_lmm; CFG=configs/grounding_dino_swin_t_vifood54_ov_s2_lmm_en.py
  else SUF=_lmm_nonovel; CFG=configs/grounding_dino_swin_t_vifood54_ov_s2_lmm_nonovel_en.py; fi
  [ -f "$OV/train_od_rfs$SUF.jsonl" ] || { echo "thiếu $OV/train_od_rfs$SUF.jsonl -> VIFOOD_LANG=en python scripts/vifood54/captions/vlm_captions.py attach --ov $([ "$MODE" = nonovel ] && echo --strip-novel)"; exit 1; }
  AL=$W/vifood54_ov_align_en; WD=$W/vifood54_ov_s2${SUF}_en
  # bước căn chỉnh: detector đứng yên (dùng chung cho w và nonovel, caption có tên novel không ảnh hưởng detector ở bước này)
  [ -f "$AL/iter_2000.pth" ] || python mmdet_train.py configs/grounding_dino_swin_t_vifood54_ov_s2_lmm_en.py --work-dir "$AL" --amp \
    --cfg-options load_from="$B1" model.freeze_detector=True train_cfg.max_iters=2000 train_cfg.val_interval=2000 \
    default_hooks.checkpoint.interval=2000
  [ -f "$WD/iter_8000.pth" ] || python mmdet_train.py "$CFG" --work-dir "$WD" --amp --cfg-options load_from="$AL/iter_2000.pth" \
    || echo "!! $WD dừng sớm, dùng checkpoint đã lưu"
  LAST=$(ls -t "$WD"/iter_*.pth | head -1)   # checkpoint cuối: val chỉ có lớp base nên không dùng để chọn cho novel
  [ -f "$WD/last_det.pth" ] || python ../scripts/vifood54/strip_lmm.py "$LAST" "$WD/last_det.pth"
  test_ckpt "$MODE" "$WD/last_det.pth"
fi

cd "$ROOT"
P=llmdet_vietnamese_food/$W
ARGS=()
for x in "B0_EN b0" "OV_S1_EN s1" "OV_W_EN w" "OV_W_nonovel_EN nonovel"; do
  set -- $x
  if [ -f "$P/vifood54_ov_en_test_$2/preds.pkl" ]; then ARGS+=(--pred "$1=$P/vifood54_ov_en_test_$2/preds.pkl"); fi
done
if [ -f "$P/vifood54_en_test_b3b/preds.pkl" ]; then ARGS+=(--pred "B3b_EN*=$P/vifood54_en_test_b3b/preds.pkl"); fi
[ ${#ARGS[@]} -gt 0 ] || { echo "chưa có preds nào"; exit 1; }
python scripts/vifood54/eval_ov.py --gt "$EN/instances_test.json" --ov "$OV/ov_classes.json" "${ARGS[@]}" \
  --out grounding_data/vifood54/EVAL_OV_EN.md
echo "XONG: grounding_data/vifood54/EVAL_OV_EN.md"
