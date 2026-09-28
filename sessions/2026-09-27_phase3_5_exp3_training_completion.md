# NHẬT KÝ PHIÊN LÀM VIỆC: 27/09/2026 (Chiều)
## Chủ đề: Hoàn tất Huấn luyện Exp 2 (Short EN) & Triển khai Thành công Exp 3 (Full Vietnamese Caption Grounding)

---

### 1. Thông tin chung
* **Thời gian**: 27/09/2026 (11:05 – 16:25)
* **Mục tiêu**:
  1. Giám sát và ghi nhận hoàn tất huấn luyện Thí nghiệm 2 (Short English Ablation).
  2. Triển khai Pha 3.5: Sinh tập dữ liệu caption câu văn tự nhiên tiếng Việt phong phú (`vifood_train_vg_vi_full.jsonl`).
  3. Cấu hình và huấn luyện hoàn chỉnh Thí nghiệm 3 — Đóng góp cốt lõi của đồ án.
* **Cấu hình phần cứng**: NVIDIA GeForce RTX 3090 (24GB VRAM), CUDA 13.0 / Driver 580.126.09.

---

### 2. Các kết quả kỹ thuật đạt được

#### 2.1. Hoàn tất Huấn luyện Thí nghiệm 2 (Short EN)
* **Thời điểm kết thúc**: 13:21:49 ngày 27/09/2026.
* **Số iteration**: 10.000 / 10.000 iter.
* **Loss hội tụ**: Giảm từ 19.87 xuống **3.8197** (`loss_cls=0.0033`, `loss_bbox=0.1227`, `loss_iou=0.1335`).
* **Checkpoint đã lưu**: `llmdet_vietnamese_food/work_dirs/vifood_en_1k/iter_10000.pth` (1.85 GB).

#### 2.2. Triển khai Pha 3.5: Sinh Dữ liệu Caption Tiếng Việt Tự Nhiên Đầy Đủ
* Phát triển script `scripts/generate_full_vietnamese_captions.py`:
  * Hệ thống 50+ mẫu template ngữ cảnh kết hợp từ điển đặc trưng 51 món ăn Việt Nam.
  * Tự động ánh xạ và kiểm định tọa độ `tokens_positive` ở cấp độ ranh giới từ (word boundaries).
  * **Kiểm định 100% tự động**: Tất cả 4.402 regions (4.028 train + 374 val) đều hợp lệ, không lỗi lệch token.
  * Độ dài caption trung bình đạt **161 ký tự** (so với ~30 ký tự của nhãn ngắn).
* Xuất ra 2 file dữ liệu:
  * `grounding_data/vifood/annotations/vifood_train_vg_vi_full.jsonl` (900 mẫu train)
  * `grounding_data/vifood/annotations/vifood_val_vg_vi_full.jsonl` (100 mẫu val)

#### 2.3. Huấn luyện Thí nghiệm 3 (Full VI Caption Grounding)
* **Config**: [`configs/grounding_dino_swin_t_vifood_vi_full.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/grounding_dino_swin_t_vifood_vi_full.py) (giữ nguyên 100% siêu tham số với Exp 1 và Exp 2).
* **Tmux session**: `vifood_vi_full_train`.
* **Khởi chạy**: 13:55:33 — **Hoàn tất**: 16:24:44 (2 giờ 29 phút).
* **Số iteration**: 10.000 / 10.000 iter.
* **Loss hội tụ**: Giảm mạnh từ **40.4938** xuống **4.4720** (`loss_cls=0.0395`, `loss_bbox=0.1419`, `loss_iou=0.1477`).
* **Checkpoints đã lưu**:
  * `work_dirs/vifood_vi_full_1k/iter_10000.pth` (1.85 GB)
  * Các mốc checkpoint trung gian: `iter_2000`, `iter_4000`, `iter_6000`, `iter_8000`.

---

### 3. Tình trạng Checkpoints Toàn bộ 3 Thí nghiệm

| Thí nghiệm | Dạng Prompt | Thư mục Lưu Checkpoint | Trọng số cuối |
|:---|:---|:---|:---|
| **Exp 1** *(Short VI)* | Nhãn tiếng Việt ngắn | `work_dirs/vifood_1k/` | `iter_10000.pth` (1.85 GB) |
| **Exp 2** *(Short EN)* | Nhãn tiếng Anh ngắn | `work_dirs/vifood_en_1k/` | `iter_10000.pth` (1.85 GB) |
| **Exp 3** *(Full VI)* | Caption câu văn tự nhiên TV | `work_dirs/vifood_vi_full_1k/` | `iter_10000.pth` (1.85 GB) |
