#!/usr/bin/env bash
# Thí nghiệm open-vocabulary: giai đoạn 1 OD (lớp base, 16k) -> giai đoạn 2 OD+VG (8k, như B3b)
# -> test đủ 54 lớp -> AP_base / AP_novel (EVAL_OV.md).
#   tmux new -d -s vifood54_ov 'bash scripts/vifood54/run_ov.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_ov_pipeline.log'
# Train có thể dừng sớm vì lỗi ổ CIFS ("Too many open files"); khi đó dùng checkpoint tốt nhất đã lưu.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
cd "$ROOT/llmdet_vietnamese_food"
W=work_dirs
best() { ls "$1"/best_coco_bbox_mAP_iter_*.pth 2>/dev/null | head -1; }

S1=$W/vifood54_ov_s1_od
[ -f "$S1/iter_16000.pth" ] || python mmdet_train.py configs/grounding_dino_swin_t_vifood54_ov_s1_od.py --work-dir "$S1" --amp \
  || echo "!! giai đoạn 1 dừng sớm, dùng checkpoint tốt nhất"
B1=$(best "$S1"); [ -n "$B1" ] || { echo "không có checkpoint giai đoạn 1"; exit 1; }

S2=$W/vifood54_ov_s2_od_vg
[ -f "$S2/iter_8000.pth" ] || python mmdet_train.py configs/grounding_dino_swin_t_vifood54_ov_s2_od_vg.py --work-dir "$S2" --amp \
  --cfg-options load_from="$B1" || echo "!! giai đoạn 2 dừng sớm, dùng checkpoint tốt nhất"
B2=$(best "$S2"); [ -n "$B2" ] || { echo "không có checkpoint giai đoạn 2"; exit 1; }

for x in "s1 $B1 configs/grounding_dino_swin_t_vifood54_ov_s1_od.py" "s2 $B2 configs/grounding_dino_swin_t_vifood54_ov_s2_od_vg.py"; do
  set -- $x
  OUT=$W/vifood54_ov_test_$1
  [ -f "$OUT/preds.pkl" ] || python mmdet_test.py "$3" "$2" --work-dir "$OUT" --out "$OUT/preds.pkl"
done

cd "$ROOT"
python scripts/vifood54/eval_ov.py \
  --pred B0=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b0/preds.pkl \
  --pred OV_S1_od=llmdet_vietnamese_food/work_dirs/vifood54_ov_test_s1/preds.pkl \
  --pred OV_S2_od_vg=llmdet_vietnamese_food/work_dirs/vifood54_ov_test_s2/preds.pkl \
  --pred 'B1_v2*'=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b1_v2/preds.pkl \
  --pred 'B3b*'=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b3b/preds.pkl
echo "XONG: grounding_data/vifood54/EVAL_OV.md"
