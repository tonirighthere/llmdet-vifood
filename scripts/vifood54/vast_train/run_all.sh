#!/usr/bin/env bash
# Chạy toàn bộ thí nghiệm trên máy thuê, KHÔNG cần người trông (chạy trong tmux sau setup_train.sh):
#   bash scripts/vifood54/vast_train/run_all.sh 2>&1 | tee -a /workspace/run_all.log
# Thứ tự mặc định: preds (B1/B3b test) -> smoke (40 iter, đo VRAM + tốc độ) -> b5b -> s1 (OV-S1) -> w (OV-W) -> pack.
# Chạy lại được: các script con tự bỏ qua bước đã có checkpoint/kết quả. Chọn bước: STEPS="b5b pack" bash run_all.sh
# Một bước lỗi KHÔNG chặn bước sau (trừ smoke); trạng thái ghi ở /workspace/run_all_status.txt.
set -uo pipefail
ROOT=$(cd "$(dirname "$0")/../../.." && pwd)
cd "$ROOT"
STEPS=${STEPS:-"preds smoke b5b s1 w pack"}
STATUS=/workspace/run_all_status.txt
W=llmdet_vietnamese_food/work_dirs
TEST_CFG=configs/grounding_dino_swin_t_vifood54_b1_od_en.py
export PYTORCH_ALLOC_CONF=expandable_segments:True

step() {  # <tên> <lệnh...>
  local name=$1; shift
  local t0=$SECONDS
  echo; echo "######## $(date '+%F %T') BẮT ĐẦU $name"
  if "$@"; then st=OK; else st="LỖI($?)"; fi
  local m=$(( (SECONDS - t0) / 60 ))
  echo "######## $(date '+%F %T') $name: $st sau $m phút"
  echo "$(date '+%F %T') $name $st ${m}ph" >> "$STATUS"
  [ "$st" = OK ]
}

do_preds() {  # preds.pkl test của B1-EN, B3b-EN: run_b5_v2_en.sh dùng để so ghép cặp / bootstrap
  (cd llmdet_vietnamese_food
   for x in "b1 work_dirs/vifood54_b1_od_en/best_coco_bbox_mAP_iter_16000.pth" \
            "b3b work_dirs/vifood54_b3b_ft_en/best_coco_bbox_mAP_iter_7000.pth"; do
     set -- $x
     out=work_dirs/vifood54_en_test_$1
     [ -f "$out/preds.pkl" ] || python mmdet_test.py "$TEST_CFG" "$2" --work-dir "$out" --out "$out/preds.pkl" || exit 1
   done)
}

do_smoke() {  # 40 iter mỗi bước của B5b: lỗi config / OOM lộ ra ngay, đo s/iter để ước thời gian
  [ -f /workspace/.smoke_ok ] && { echo "smoke đã qua"; return 0; }
  SMOKE=1 bash scripts/vifood54/run_b5_v2_en.sh b || return 1
  echo "--- bộ nhớ GPU (MB) và thời gian/iter ở cuối smoke:"
  for d in "$W"/vifood54_b5_align_en_smoke "$W"/vifood54_b5_lmm_en_v2b_smoke; do
    f=$(ls -t "$d"/*/vis_data/scalars.json 2>/dev/null | head -1)
    [ -n "$f" ] && python - "$f" <<'PY'
import json, sys
rows = [json.loads(l) for l in open(sys.argv[1]) if '"time"' in l]
if rows:
    t = sum(r['time'] for r in rows[-4:]) / len(rows[-4:])
    print(f"{sys.argv[1].split('/')[-4]}: memory {max(r.get('memory', 0) for r in rows)} MB · {t:.2f} s/iter"
          f" -> 8000 iter ≈ {t * 8000 / 3600:.1f} h, 16000 iter ≈ {t * 16000 / 3600:.1f} h")
PY
  done
  rm -rf "$W"/vifood54_b5_align_en_smoke "$W"/vifood54_b5_lmm_en_v2b_smoke
  touch /workspace/.smoke_ok
}

do_pack() {  # kết quả nhỏ gọn để tải về: bảng EVAL, preds, checkpoint detector (đã bỏ LLM), log; KHÔNG kèm iter_*.pth
  local out=/workspace/results_train.tgz
  local list=$(mktemp)
  ls grounding_data/vifood54/EVAL_*.md 2>/dev/null >> "$list"
  find "$W" -not -path '*/vifood54_b5_lmm_en/*' \( -name 'preds.pkl' -o -name '*_det.pth' \
       -o \( -name 'best_coco_bbox_mAP_iter_*.pth' -path '*ov_s1*' \) \
       -o -name '*.log' -o -name 'scalars.json' \) 2>/dev/null >> "$list"
  ls grounding_data/vifood54/annotations_ov_en/ov_classes.json "$STATUS" /workspace/run_all.log 2>/dev/null >> "$list"
  tar -czf "$out" -T "$list" && echo "-> $out $(du -h "$out" | cut -f1)"
  rm -f "$list"
}

for s in $STEPS; do
  case $s in
    preds) step preds do_preds ;;
    smoke) step smoke do_smoke || { echo "!! SMOKE lỗi: dừng để sửa (gửi Claude log phía trên)"; exit 1; } ;;
    b5b)   step B5b bash scripts/vifood54/run_b5_v2_en.sh b ;;
    s1)    step OV-S1 bash scripts/vifood54/run_ov_en.sh s1 ;;
    w)     step OV-W bash scripts/vifood54/run_ov_en.sh w ;;
    pack)  step pack do_pack ;;
    *) echo "bước không hợp lệ: $s" ;;
  esac
done
echo; echo "=== TRẠNG THÁI"; cat "$STATUS"
echo "XONG. Tải /workspace/results_train.tgz về (scp) rồi DESTROY instance."
