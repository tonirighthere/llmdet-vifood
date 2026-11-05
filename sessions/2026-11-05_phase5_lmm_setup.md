# NHẬT KÝ PHIÊN LÀM VIỆC: 05/11/2026
## Chủ đề: Pha 5 — bật giám sát LLM (đúng thiết kế LLMDet) + OV giám sát yếu (OV-W) + nền LLMDet thật

---

### 1. Vì sao làm lại Pha 5
- Mọi run trước đều `lmm=None` → mới là fine-tune Grounding DINO, chưa có thành phần "LLM" của LLMDet.
  Cổng "B5 chỉ chạy nếu B3 > B1" không đúng: B3 đo loss gióng hàng qua BERT, không dự báo loss sinh caption;
  và B3b (0.323) đã > B1-v2 (0.315).
- Mọi run khởi tạo từ MM-GDINO, chưa từng dùng checkpoint LLMDet (đã train trên GroundingCap-1M).
- OV: món "chưa thấy" chỉ học được nếu tên nó xuất hiện đâu đó trong dữ liệu train (paper: LCS-558k chỉ có caption,
  box giả). OV-W = lớp novel không có box người gán, chỉ có tên trong caption ảnh → đúng tinh thần paper.

### 2. Thiết kế (một forward, một backward)
```
ảnh → Swin-T → encoder (memory, C=256) → decoder → box ───────────────► L_align + L_box
                          │ p5 20×20 + p4 27×27 = 1130 token
                          ▼ connector 256→896 (mm_projector2.bin)
"<image>\nDescribe the image in detail." → Qwen2-0.5B (LoRA) → CE với caption VLM đã duyệt → loss_lmm_image
query khớp box GT (≤ num_region_caption) + cross-attn → Qwen2 → CE với tên món     → d1.loss_lmm_region
```
Qwen2 đóng băng (chỉ LoRA, cross-attn, connector học). Test/app: bỏ LLM (`strip_lmm.py`), detector chạy như B3b.
Caption ảnh đi vào tokenizer Qwen2 (giữ dấu) → không cần lint bỏ dấu BERT; chỉ cần đúng sự thật.

### 3. Thay đổi code
| File | Thay đổi |
| :--- | :--- |
| `mmdet/datasets/transforms/text_transformers.py` | **Sửa lỗi**: hội thoại vùng được chọn TRƯỚC `od_aug` → class dropout / tràn token bỏ box làm `box_index` lệch hoặc vượt số box (crash hoặc sai vùng); ở OD mode tên vùng rơi vào `except` → LLM học chữ "object". Nay chọn SAU aug, OD lấy tên lớp từ label map theo class id gốc (`gt_class_ids`, trước remap). Không đổi hành vi khi `lmm=None` |
| `mmdet/models/detectors/grounding_dino.py` | Batch không có region nào (ảnh không box ở OV-W) → trả loss 0 trước `torch.cat` list rỗng |
| `scripts/vifood54/captions/vlm_captions.py` (mới) | `generate`: Gemma-4 viết caption có điều kiện theo box GT, lọc câu suy đoán / hương vị, gắn cờ khi nhắc món không có box hoặc thiếu món GT, chạy tiếp được giữa chừng. `attach`: gắn caption vào `conversations` của OD + VG → `*_lmm.jsonl` (`--ov`, `--strip-novel`) |
| `scripts/vifood54/captions/review_captions.py` (mới) | Gradio duyệt / sửa / loại caption, ảnh flagged trước → `captions_reviewed.jsonl` |
| `configs/..._b5_lmm.py` (mới) | = B3b + lmm; batch 1 × accumulative 4; `num_region_caption` 8; lr ×5 cho `lmm`, `connector` |
| `configs/..._ov_s2_lmm.py`, `..._ov_s2_lmm_nonovel.py` (mới) | OV-W: như OV-S2 + lmm, giữ ảnh chỉ có món novel (`keep_empty=False`); bản ablation bỏ câu có tên novel |
| `scripts/vifood54/strip_lmm.py` (mới) | Bỏ `lmm.*`, `connector.*`, `region_connector.*`, `image_seperate.*`, `ref_point_head.*` |
| `scripts/vifood54/run_lmm.sh` (mới) | `b5 \| ov \| ov_nonovel`: train → strip → test → đánh giá; `SMOKE=1` chạy 40 iter |
| `scripts/vifood54/run_llmdet_base.sh` (mới) | B0-LLMDet (zero-shot, tên Việt + Anh) và B1-L (công thức B1, khởi tạo LLMDet) |

### 4. HƯỚNG DẪN CHẠY (người train)
Tất cả lệnh chạy từ gốc repo, môi trường `vifood` (trừ bước 1 dùng môi trường có Gemma 4).

**Bước 0 — nền LLMDet (song song với bước 1, chỉ cần GPU)**
```bash
huggingface-cli download fushh7/LLMDet --local-dir huggingface/llmdet   # xem file .pth Swin-T bản mmdet
LLMDET_CKPT=../huggingface/llmdet/<file>.pth bash scripts/vifood54/run_llmdet_base.sh
```
→ `EVAL_LLMDET_BASE.md`, `EVAL_OV_LLMDET_B0.md`. Nếu checkpoint chỉ có bản HF (transformers) thì báo lại, cần chuyển đổi.

**Bước 1 — sinh caption (~8 s/ảnh, 3138 ảnh ≈ 7 h, chạy lại được giữa chừng)**
```bash
python scripts/vifood54/captions/vlm_captions.py generate --limit 20 --load-4bit   # thử 20 ảnh, đọc file kết quả
python scripts/vifood54/captions/vlm_captions.py generate --load-4bit              # chạy hết
```
Đầu ra `grounding_data/vifood54/annotations/vlm_captions.jsonl` (`raw`, `caption` sau lọc, `status` auto/flagged, `issues`).

**Bước 2 — duyệt tay**
```bash
python scripts/vifood54/captions/review_captions.py --reviewer <tên> --port 7863
```
Ưu tiên: hết ảnh flagged → ảnh của 8 lớp novel → mẫu ngẫu nhiên ~20% ảnh auto (ghi lại tỉ lệ phải sửa/loại cho luận văn).
Caption bị loại hoặc flagged chưa duyệt → train dùng caption template L2.

**Bước 3 — gắn caption vào dữ liệu train**
```bash
python scripts/vifood54/captions/vlm_captions.py attach                     # B5
python scripts/vifood54/captions/vlm_captions.py attach --ov                # OV-W
python scripts/vifood54/captions/vlm_captions.py attach --ov --strip-novel  # ablation OV-W
```

**Bước 4 — smoke test rồi train** (tắt app trước, cần ~20+ GB VRAM)
```bash
SMOKE=1 bash scripts/vifood54/run_lmm.sh b5     # log phải có loss_lmm_image, d1.loss_lmm_region giảm dần
tmux new -d -s vifood54_b5 'bash scripts/vifood54/run_lmm.sh b5 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_b5_pipeline.log'
SMOKE=1 bash scripts/vifood54/run_lmm.sh ov
tmux new -d -s vifood54_ovw 'bash scripts/vifood54/run_lmm.sh ov 2>&1 | tee llmdet_vietnamese_food/work_dirs/vifood54_ovw_pipeline.log'
bash scripts/vifood54/run_lmm.sh ov_nonovel
```
- OOM: giảm `num_region` trong config 8 → 4, rồi thêm `model.lmm_max_token_length=768` qua `--cfg-options`.
- Smoke OV lỗi ở ảnh không box (dn query / loss rỗng): đặt lại `keep_empty=True` trong `..._ov_s2_lmm.py` (mất ~271 ảnh chỉ có caption) và báo lại.
- `loss_lmm_image` không giảm sau ~1k iter: connector lệch với encoder đã fine-tune → báo lại để thêm bước căn connector (Step 1 của paper).
- Ghi work_dirs ra ổ local, không ghi lên ổ CIFS (lỗi "Too many open files" làm B3b dừng sớm).

### 5. Bảng kết quả cần điền
| ID | Câu hỏi | So với | File |
| :--- | :--- | :--- | :--- |
| B0-LLMDet | Zero-shot của LLMDet trên món Việt | B0 (MM-GDINO) | `EVAL_LLMDET_BASE.md`, `EVAL_OV_LLMDET_B0.md` |
| B1-L | Khởi tạo LLMDet có tốt hơn MM-GDINO? | B1-v2 | `EVAL_LLMDET_BASE.md` |
| B5 | Giám sát LLM (caption ảnh + vùng) có giúp? | B3b (cùng dữ liệu box, cùng iter) | `EVAL_B5.md`, `EVAL_GROUNDING_B5.md` |
| OV-W | Tên novel trong caption có giúp nhận món không có box? | OV-S2, OV-W nonovel, B3b* | `EVAL_OV_LMM.md` |

Nếu B1-L > B1-v2: chạy thêm B5 từ B1-L (`B5_FROM=... run_lmm.sh b5`) và B3b từ B1-L để so công bằng.
