#!/usr/bin/env bash
# Pipeline TIẾNG ANH: B1-EN (OD, tên lớp EN) -> B3b-EN (OD + VG caption EN) [-> B5-EN nếu RUN_B5=1], rồi đánh giá
# mAP test + grounding câu, đặt cạnh bản tiếng Việt (B1-v2, B3b). Chạy lại được: bước nào đã có kết quả thì bỏ qua.
#   tmux new -d -s training 'bash scripts/vifood54/run_en.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_en_pipeline.log'
#   RUN_B5=1 bash scripts/vifood54/run_en.sh      # thêm B5-EN (B5 Pha 5 + EN; ~20 GB VRAM, tắt app trước)
set -euo pipefail
ulimit -n 65535 2>/dev/null || ulimit -n 4096  # CIFS: "Too many open files"
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
A=$ROOT/grounding_data/vifood54/annotations_en
cd "$ROOT"

# ── dữ liệu (CPU, vài phút) ──
[ -f "$A/label_map.json" ] || python scripts/vifood54/make_en_data.py
[ -f "$A/train_vg_cap_rfs.jsonl" ] || (cd scripts/vifood54/captions && python build_captions_en.py)
# caption ảnh/vùng cho loss LMM: template EN + đặc điểm VLM đã dịch (build_lmm_en.py) -> *_lmm.jsonl.
# KHÔNG gọi vlm_captions.py attach ở đây: lệnh đó ghi đè *_lmm.jsonl bằng template L2 / caption VLM chưa duyệt.
[ "${RUN_B5:-0}" != 1 ] || [ -f "$A/train_vg_cap_rfs_lmm.jsonl.bak_template" ] \
  || python scripts/vifood54/captions/build_lmm_en.py

cd "$ROOT/llmdet_vietnamese_food"
export PYTORCH_ALLOC_CONF=expandable_segments:True

# train_test <config> <work_dir> <iter cuối> <test_out> [--cfg-options ...] -> in đường dẫn checkpoint đem test
# (log train ra stderr để tee vẫn thấy; chỉ dòng cuối stdout là đường dẫn checkpoint)
train_test() {
  local cfg=$1 wd=$2 last=$3 out=$4; shift 4
  [ -f "$wd/iter_$last.pth" ] || python mmdet_train.py "$cfg" --work-dir "$wd" --amp "$@" >&2 \
    || echo "!! $wd: train dừng sớm, dùng checkpoint tốt nhất" >&2
  local best; best=$(ls "$wd"/best_coco_bbox_mAP_iter_*.pth | head -1)
  [ -n "$best" ] || { echo "!! $wd: không có checkpoint" >&2; exit 1; }
  if [[ "$cfg" == *lmm* ]]; then  # bỏ Qwen/connector như run_lmm.sh: test là detector thuần
    [ -f "$wd/best_det.pth" ] || python ../scripts/vifood54/strip_lmm.py "$best" "$wd/best_det.pth" >&2
    best=$wd/best_det.pth
  fi
  # test bằng config B1-EN (lmm=None, 54 lớp EN)
  [ -f "$out/preds.pkl" ] || python mmdet_test.py configs/grounding_dino_swin_t_vifood54_b1_od_en.py "$best" \
    --work-dir "$out" --out "$out/preds.pkl" >&2
  echo "$best"
}

B1=$(train_test configs/grounding_dino_swin_t_vifood54_b1_od_en.py work_dirs/vifood54_b1_od_en 16000 \
  work_dirs/vifood54_en_test_b1 | tail -1)
B3B=$(train_test configs/grounding_dino_swin_t_vifood54_b3b_ft_en.py work_dirs/vifood54_b3b_ft_en 8000 \
  work_dirs/vifood54_en_test_b3b --cfg-options load_from="$B1" | tail -1)
MODELS=(--model B1_EN="$B1" --model B3b_EN="$B3B")
PREDS=(--pred B1_EN=llmdet_vietnamese_food/work_dirs/vifood54_en_test_b1/preds.pkl
       --pred B3b_EN=llmdet_vietnamese_food/work_dirs/vifood54_en_test_b3b/preds.pkl)
if [ "${RUN_B5:-0}" = 1 ]; then  # B5 batch 1 x accum 4, 16k iter (cờ lmm_grad_ckpt/lmm_sparse_logits)
  B5=$(train_test configs/grounding_dino_swin_t_vifood54_b5_lmm_en.py work_dirs/vifood54_b5_lmm_en 16000 \
    work_dirs/vifood54_en_test_b5 --cfg-options load_from="$B1" | tail -1)
  MODELS+=(--model B5_EN="$B5")
  PREDS+=(--pred B5_EN=llmdet_vietnamese_food/work_dirs/vifood54_en_test_b5/preds.pkl)
fi

PYTHONPATH=. python ../scripts/vifood54/eval_grounding.py --lang en \
  --config configs/grounding_dino_swin_t_vifood54_b1_od_en.py --ann "$A/test_vg_cap.jsonl" \
  "${MODELS[@]}" --out ../grounding_data/vifood54/EVAL_GROUNDING_EN.md

cd "$ROOT"
# cùng ảnh/box/id lớp nên preds VI và EN so được trên cùng GT (category_id = id lớp)
python scripts/vifood54/analyze_eval.py --gt "$A/instances_test.json" \
  --pred B1_v2_VI=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b1_v2/preds.pkl \
  --pred B3b_VI=llmdet_vietnamese_food/work_dirs/vifood54_v2_test_b3b/preds.pkl \
  "${PREDS[@]}" --out grounding_data/vifood54/EVAL_EN.md --bootstrap 0
echo "XONG: EVAL_EN.md, EVAL_GROUNDING_EN.md"
