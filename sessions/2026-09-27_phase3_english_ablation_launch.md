# NHẬT KÝ PHIÊN LÀM VIỆC: 27/09/2026 (Trưa)
## Chủ đề: Triển khai Pha 3 — Sinh Dữ liệu Tiếng Anh & Khởi chạy Huấn luyện Thí nghiệm 2 (Ablation Study)

---

### 1. Thông tin chung
* **Thời gian**: 27/09/2026 (11:00 – 11:05)
* **Mục tiêu**:
  1. Chuyển đổi toàn bộ bộ dữ liệu ViFood-1K sang grounding caption tiếng Anh chuẩn hóa dựa trên bảng từ điển 51 món ăn (`CLASS_TAXONOMY_51`).
  2. Thiết lập cấu hình và khởi chạy huấn luyện Thí nghiệm 2 (`vifood_en_1k`) với 100% siêu tham số đồng nhất (Fair Comparison) để phục vụ nghiên cứu cắt bỏ (Ablation Study) và so sánh song ngữ (Bilingual Grounding).
* **Cấu hình phần cứng**: NVIDIA GeForce RTX 3090 (24GB VRAM), PyTorch 2.10.0+cu128.

---

### 2. Các công việc kỹ thuật đã thực hiện

#### Bước 3.1: Sinh file nhãn tiếng Anh (ODVG & COCO Format)
* Phát triển script `scripts/convert_vi_to_en_jsonl.py`:
  * Ánh xạ 51 món ăn Việt Nam sang tên tiếng Anh chuyên biệt (ví dụ: `bánh tráng` -> `rice paper`, `phở` -> `Vietnamese Pho`, `nước chấm` -> `dipping sauce`).
  * Tự động tính toán lại chính xác tọa độ ký tự `tokens_positive: [[start, end]]` theo chuỗi caption tiếng Anh mới.
  * Xuất ra 3 file dữ liệu hoàn chỉnh:
    * `grounding_data/vifood/annotations/vifood_train_vg_en.jsonl` (900 mẫu train)
    * `grounding_data/vifood/annotations/vifood_val_vg_en.jsonl` (100 mẫu val)
    * `grounding_data/vifood/annotations/instances_val_en.json` (COCO format tiếng Anh)

#### Bước 3.2: Thiết lập Cấu hình & Khởi chạy Huấn luyện Thí nghiệm 2
* Tạo file cấu hình: [`configs/grounding_dino_swin_t_vifood_en.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/grounding_dino_swin_t_vifood_en.py)
  * Trỏ dataset tới `vifood_train_vg_en.jsonl`.
  * **Giữ nguyên 100% siêu tham số**: AdamW `lr=5e-5`, warmup 500 iters, MultiStepLR `[7000, 9000]`, `max_iters=10000`, `batch_size=4`, `num_workers=4`, random seed.
* Tạo script tmux tự động: [`scripts/train_vifood_en_tmux.sh`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/scripts/train_vifood_en_tmux.sh).
* **Khởi chạy thành công** tiến trình huấn luyện trong phiên tmux `vifood_en_train`.

---

### 3. Trạng thái Huấn luyện Thí nghiệm 2 Ban đầu
* **Session Tmux**: `vifood_en_train`
* **Log file**: `work_dirs/vifood_en_1k/train.log`
* **Tiến độ khởi đầu**:
  * Đạt Iter [50 / 10,000] với tốc độ `0.835s / iteration`.
  * Chiếm dụng VRAM: `5,478 MiB` (~5.5 GB).
  * Loss ban đầu: `19.87` (thấp hơn mốc 23.47 của tiếng Việt do text encoder BERT đã có sẵn vốn từ vựng tiếng Anh).
  * Dự kiến hoàn tất: ~13:20 chiều ngày 27/09/2026 (~2 giờ 18 phút).

---

### 4. Hướng đi tiếp theo (Sau khi Thí nghiệm 2 kết thúc)
* Đánh giá song song checkpoint `exp1 (Vi)` và `exp2 (En)` trên cùng tập validation để lập Bảng kết quả định lượng tổng hợp cho Chương 4 của Luận văn tốt nghiệp.
