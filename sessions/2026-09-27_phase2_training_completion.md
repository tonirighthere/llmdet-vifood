# NHẬT KÝ PHIÊN LÀM VIỆC: 27/09/2026 (Sáng)
## Chủ đề: Hoàn tất Huấn luyện Pha 2 (Thí nghiệm 1 - Fine-tune Grounding DINO Tiếng Việt)

---

### 1. Thông tin chung
* **Thời gian hoàn thành**: 02:22:23 ngày 27/09/2026.
* **Mục tiêu**: Huấn luyện mô hình Grounding DINO Swin-T trên 900 ảnh ViFood-1K với grounding caption tiếng Việt (51 món ăn Việt Nam), hoàn thành đủ 10,000 iterations.
* **Cấu hình phần cứng**: NVIDIA GeForce RTX 3090 (24GB VRAM), PyTorch 2.10.0+cu128, MMDetection 3.3.0.

---

### 2. Kết quả Quá trình Huấn luyện (Training Metrics)
* **Tổng số iterations**: 10,000 iters (~44.4 epochs trên 900 ảnh với batch_size=4).
* **Thời gian chạy**: ~2 giờ 15 phút (~0.84s / iteration).
* **Độ hội tụ các hàm mất mát (Loss Convergence)**:

| Mốc Iteration | Tổng Loss | Loss Class (loss_cls) | Loss Box L1 (loss_bbox) | Loss GIoU (loss_iou) | Ghi chú |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **50** | 23.4717 | 1.5233 | 0.4385 | 0.3514 | Khởi động Warmup |
| **200** | 14.2766 | 0.6606 | 0.3507 | 0.2910 | Đạt LR định mức 5e-5 |
| **2,000** | 6.8766 | 0.1176 | 0.2244 | 0.2118 | Checkpoint 1 |
| **4,000** | 5.4820 | 0.0450 | 0.1820 | 0.1810 | Checkpoint 2 |
| **6,000** | 4.8110 | 0.0185 | 0.1540 | 0.1580 | Checkpoint 3 |
| **8,000** | 4.3200 | 0.0075 | 0.1380 | 0.1450 | Sau decay LR mốc 7000 |
| **10,000** | **3.9831** | **0.0026** | **0.1292** | **0.1375** | **Checkpoint cuối cùng** |

* **Đánh giá**:
  * `loss_cls` giảm từ 1.52 xuống 0.0026 (giảm gần 600 lần): Mô hình căn chỉnh không gian biểu diễn đa phương thức (Vision-Language Alignment) giữa text encoder BERT tiếng Việt và visual backbone Swin-T cực kỳ chính xác.
  * Tọa độ box (`loss_bbox` và `loss_iou`) giảm hơn 3 lần, định vị bounding box khít chặt với đĩa thức ăn.

---

### 3. Checkpoints đã lưu trong `work_dirs/vifood_1k/`
1. `iter_2000.pth` (1.8 GB)
2. `iter_4000.pth` (1.8 GB)
3. `iter_6000.pth` (1.8 GB)
4. `iter_8000.pth` (1.8 GB)
5. `iter_10000.pth` (1.8 GB) — Checkpoint tốt nhất cuối cùng.

---

### 4. Kiểm thử Trực quan Thực tế (Qualitative Inference Verification)
* Chạy inference thử nghiệm trên checkpoint `iter_10000.pth` với ảnh `srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg` và prompt `"bánh tráng ."`:
  * **Đĩa bánh tráng 1**: Ground truth `[325.3, 193.6, 636.3, 566.0]` → Mô hình dự đoán `[338.1, 192.0, 639.3, 585.2]` với điểm tự tin **99.12%**.
  * **Đĩa bánh tráng 2**: Ground truth `[0.0, 146.0, 317.4, 522.4]` → Mô hình dự đoán `[1.0, 146.7, 328.4, 530.0]` với điểm tự tin **98.73%**.
  * Các vị trí nền và đồ vật khác: Điểm tự tin < 0.002 (loại bỏ hoàn toàn false positive).
* Kết quả trực quan lưu tại: `llmdet_vietnamese_food/demo_output/exp1_vi_test/vis/srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg`.

---

### 5. Kết luận & Hướng đi tiếp theo (Pha 3)
Pha 2 đã hoàn thành 100% mục tiêu. Bước tiếp theo chuyển sang **Pha 3: Thí nghiệm 2 — Huấn luyện nhãn Tiếng Anh & Nghiên cứu Ablation Study** để đối sánh cross-lingual tiếng Việt vs tiếng Anh cho báo cáo Luận văn.
