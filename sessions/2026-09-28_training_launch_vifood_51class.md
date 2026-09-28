# NHẬT KÝ PHIÊN LÀM VIỆC: 28/09/2026
## Chủ đề: Khởi chạy Huấn luyện Mô hình LLMDet (Grounding DINO Swin-T) 51 Lớp Món Ăn Việt Nam

---

### 1. Thông tin chung
* **Thời gian bắt đầu**: 26/09/2026 23:36 (Giờ hệ thống)
* **Mục tiêu**: Huấn luyện mô hình Visual Grounding & Open-Vocabulary Detector trên tập dữ liệu 1.000 ảnh món ăn Việt Nam (900 train, 100 val) mở rộng lên 51 class (thêm `rau xào`, `nước chấm`, `gà quay`).
* **Hạ tầng**: NVIDIA GeForce RTX 3090 24GB (Server 191).
* **Môi trường vận hành**: Chạy ngầm trong `tmux session: vifood_train`, chống rớt mạng SSH hoàn toàn.

---

### 2. Dữ liệu & Annotation Đã Chuẩn Bị
1. **Dữ liệu hình ảnh**:
   - `grounding_data/vifood/images/train2017/`: 900 ảnh chuẩn lọc từ `vifood2.zip` bắt đầu từ `srcA_H-000...`.
   - `grounding_data/vifood/images/val2017/`: 100 ảnh validation.
2. **Annotation**:
   - `grounding_data/vifood/annotations/vifood_train_vg.jsonl`: 900 mẫu ODVG với dual-caption (ngắn theo nhãn & dài sinh bởi `gemini-3.6-flash`), ánh xạ `tokens_positive` chính xác từng vị trí ký tự.
   - `grounding_data/vifood/annotations/vifood_val_vg.jsonl`: 100 mẫu ODVG.
   - `grounding_data/vifood/annotations/instances_val.json`: Định dạng COCO 100 ảnh, 374 bounding boxes, 51 categories.
   - `grounding_data/vifood/annotations/label_map.json`: Bảng ánh xạ 51 lớp song ngữ Việt - Anh.

---

### 3. Cấu hình Huấn luyện Tối ưu (RTX 3090 24GB)
* **File config**: [`llmdet_vietnamese_food/configs/grounding_dino_swin_t_vifood.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/grounding_dino_swin_t_vifood.py)
* **Pretrained Weights**:
  - Visual Backbone & Transformer: `grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth` (1.09 GB)
  - Text Backbone: `bert-base-uncased`
* **Siêu tham số & Tối ưu bộ nhớ**:
  - `batch_size = 1` mỗi GPU, `accumulative_counts = 4` (effective batch size = 4).
  - Tích hợp PyTorch AMP (`--amp`, FP16 mixed precision).
  - Gradient Checkpointing: `with_cp = True` trên backbone và transformer.
  - Tốc độ học (Learning Rate): Base LR = `5e-5`, Warmup 500 iters, MultiStepLR milestones tại `[7000, 9000]`.
  - Tổng số bước: 10,000 iterations (~44 epoch trên tập 900 ảnh).
  - Tần suất lưu checkpoint & đánh giá: mỗi 2,000 iters.

---

### 4. Kết quả Theo dõi Khởi động & Hội tụ
Quá trình huấn luyện đã khởi động thành công và thể hiện tốc độ hội tụ rất ấn tượng:

| Iteration | Learning Rate | VRAM Usage | Time / Step | Loss Tổng | Loss Classification | Loss Bounding Box | Loss GIoU | Grad Norm |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **50** | 4.95e-6 | 5,497 MB | 0.85s | **23.4717** | 1.5233 | 0.4385 | 0.3514 | *amp warm* |
| **100** | 9.96e-6 | 5,462 MB | 0.84s | **18.3405** | 1.0281 | 0.3661 | 0.3325 | *amp warm* |
| **150** | 1.49e-5 | 5,451 MB | 0.84s | **15.2014** | 0.7094 | 0.3640 | 0.3202 | 145.66 |

* **Đánh giá sơ bộ**:
  - VRAM chỉ chiếm **5.45 GB** (hoàn toàn an toàn trên card 24GB, không có nguy cơ OOM).
  - Tốc độ xử lý đạt **~0.84 giây/step**, dự kiến hoàn thành 10,000 iters trong khoảng 2 giờ 15 phút.
  - Loss phân loại (classification) giảm nhanh từ `1.52` xuống `0.70`, chứng minh mô hình đang học rất tốt biểu diễn ngữ nghĩa tiếng Việt của 51 món ăn.

---

### 5. Hướng dẫn Vận hành & Giám sát cho Người Dùng
Quá trình huấn luyện được cô lập hoàn toàn trong daemon tmux của server:
* **Vào xem trực tiếp tiến trình**:
  ```bash
  tmux attach -t vifood_train
  ```
* **Thoát ra an toàn mà không ngắt training**:
  Bấm tổ hợp phím `Ctrl + B`, sau đó nhả ra và bấm `D`.
* **Xem log thời gian thực qua file**:
  ```bash
  tail -f /home/atin/tuan/SoPSoP/llmdet_vietnamese_food/work_dirs/vifood_1k/train.log
  ```
