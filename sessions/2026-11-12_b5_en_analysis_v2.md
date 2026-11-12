# 12/11/2026 — Phân tích B5-EN lần 1 và B5-EN v2 (căn chỉnh + đúng lịch B3b-EN)

## Kết quả B5-EN lần 1 (`EVAL_EN.md`, `EVAL_GROUNDING_EN.md`)
| Mô hình | mAP | AP50 | AP75 | names R@1 | L1 R@1 | L2 R@1 | AP hiếm / thường / phổ biến |
|---|---|---|---|---|---|---|---|
| B1-EN | 0.384 | 0.475 | 0.433 | 0.860 | 0.716 | 0.612 | 0.295 / 0.403 / 0.449 |
| B3b-EN | 0.387 | 0.484 | 0.432 | 0.859 | 0.808 | 0.830 | 0.300 / 0.406 / 0.450 |
| B5-EN (iter 4000) | 0.375 | 0.469 | 0.420 | 0.854 | 0.750 | 0.685 | 0.300 / 0.389 / 0.440 |

(AP theo tần suất: hiếm ≤ 60 ảnh train — 13 lớp; phổ biến > 150 — 8 lớp; tính từ bảng AP theo lớp.)
B5-EN thấp hơn B3b-EN 23 lớp, cao hơn 11 lớp; lớp hiếm ngang nhau.

## Vì sao chưa kết luận được "LLM không giúp"
1. **So sánh không cùng lượng train**: B5-EN được đánh giá ở checkpoint iter 4000 × batch 1 = 4000 mẫu (1000 bước cập nhật);
   B3b-EN ở iter 7000 × batch 2 = 14000 mẫu (3500 bước). L2 R@1 0.685 nằm giữa B1-EN (0.612) và B3b-EN (0.830) đúng như một
   mô hình mới học được ~1/3 đường. Checkpoint chọn theo mAP val, trong khi lợi ích của caption nằm ở grounding câu.
2. **Thiếu bước căn chỉnh (Step 1 của paper)** — giả thuyết: connector `mm_projector2.bin` căn với MM-GDINO gốc, không phải
   B1-EN đã fine-tune. Loss LLM lúc đầu cao (ảnh 3.05, vùng 1.62) và gradient của nó đi thẳng vào detector; mAP val tốt nhất
   ở iter 4000/16000, các mốc sau không vượt được.
3. **Caption cho LLM còn ngắn và có nhiễu**: TB 40 từ (paper ~115), ghép template + đặc điểm VLM, có cụm sai
   ("shrimp, clear broth", "sticky rice, fibrous coating", "dipping sauce, round shape").
4. Chưa rõ (cần log): `clip_grad max_norm=0.1` tính chung detector + LLM — nếu gradient nhánh LLM lớn, phần cập nhật
   detector bị co lại. So `grad_norm` trong log B5-EN với B3b-EN.

## Thay đổi
| File | Nội dung |
| :--- | :--- |
| `mmdet/models/detectors/grounding_dino.py` | cờ `freeze_detector` (mặc định tắt): chỉ `lmm.*`, `connector.*`, `region_connector.*`, `image_seperate.*`, `ref_point_head.*` được học |
| `configs/..._b5_align_en.py` | bước 1: `freeze_detector=True`, batch 2 × 2, 2000 iter, lr phần LLM 1e-4 |
| `configs/..._b5_lmm_en_v2.py` | bước 2: load bước 1, **đúng lịch B3b-EN** (batch 2 × 2, 8000 iter, mốc 6000/7500, val mỗi 1000) |
| `scripts/vifood54/run_b5_v2_en.sh` | bước 1 → bước 2 → strip best + last → test → grounding → `EVAL_EN_B5V2.md`, `EVAL_GROUNDING_EN_B5V2.md`; `SMOKE=1` |
| `scripts/vifood54/analyze_eval.py` | bảng "AP theo tần suất lớp" (đọc `stats.train.images` trong taxonomy cạnh `--gt`; `--rare-max`, `--freq-min`) |

## Chạy
```bash
bash scripts/vifood54/run_phase0_b5_diag.sh        # nếu chưa: B5-EN lần 1 ở iter 16000 (không train)
SMOKE=1 bash scripts/vifood54/run_b5_v2_en.sh      # VRAM batch 2 + loss LLM
tmux new -d -s training 'bash scripts/vifood54/run_b5_v2_en.sh 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_b5_v2_en.log'
```
OOM ở batch 2: xem ghi chú trong `..._b5_lmm_en_v2.py`.

## Cách đọc kết quả
- Bước 1 xong: `loss_lmm_image` phải giảm rõ so với 3.05 (kỳ vọng < 2).
- B5v2_last vs B3b-EN: cùng lượng train, chỉ khác 2 loss LLM. Nhìn L2 R@1, AP lớp hiếm, khoảng tin cậy mAP.
- Nếu B5v2 vẫn < B3b-EN ngoài CI: nguyên nhân còn lại là chất lượng caption (mục 3) hoặc clip_grad (mục 4).
