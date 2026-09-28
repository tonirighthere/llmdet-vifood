# NHẬT KÝ PHIÊN LÀM VIỆC: 27/09/2026
## Chủ đề: Hoàn thành Pha 1 — Sanity Check Inference & Thiết lập Config Huấn luyện ViFood

---

### 1. Thông tin chung
* **Thời gian**: 27/09/2026
* **Mục tiêu**: Kiểm thử thông luồng toàn bộ pipeline Grounding DINO từ load dữ liệu, nạp checkpoint pretrained đến forward pass inference trên GPU, đồng thời xây dựng các file cấu hình huấn luyện và đánh giá mAP cho tập dữ liệu món ăn Việt Nam (ViFood).
* **Người thực hiện**: [Họ và tên của bạn]
* **Cấu hình phần cứng**: NVIDIA GeForce RTX 3090 (24GB VRAM), PyTorch 2.10.0+cu128, MMDetection 3.3.0, Transformers 4.57.1.

---

### 2. Các vấn đề kỹ thuật đã xử lý (Troubleshooting & Compatibility Fixes)
Trong quá trình chạy thực tế, phát hiện và khắc phục triệt để 4 lỗi tương thích môi trường quan trọng:
1. **PyTorch 2.6+ `torch.load` default `weights_only=True`**:
   * *Hiện tượng*: Khi MMEngine nạp checkpoint pretrained, PyTorch chặn do đối tượng `HistoryBuffer` trong checkpoint.
   * *Khắc phục*: Tích hợp cơ chế hook an toàn cho `torch.load` trong `mmdet/__init__.py` để cho phép nạp các checkpoint MMEngine hợp lệ.
2. **Transformers 4.40+ chuyển đổi module nội bộ**:
   * *Hiện tượng*: `ImportError: cannot import name 'apply_chunking_to_forward' from 'transformers.modeling_utils'`.
   * *Khắc phục*: Cập nhật đường dẫn import trong `ram/models/bert.py` và `mmdet/models/utils/vlfuse_helper.py` sang `transformers.pytorch_utils`.
3. **Bổ sung thư viện định dạng & metric**:
   * Cài đặt bổ sung: `terminaltables`, `pycocotools`, `shapely` phục vụ xử lý polygon và tính toán mAP COCO metric.
4. **NLTK Text Tagger**:
   * Tải và giải nén các gói ngôn ngữ: `averaged_perceptron_tagger_eng`, `averaged_perceptron_tagger`, `punkt`, `punkt_tab` phục vụ cơ chế POS tagging trích xuất cụm danh từ (noun phrase extraction) cho Grounding DINO.

---

### 3. Kết quả Sanity Check Inference (Bước 1.1)
* Chạy inference thành công trên ảnh thực tế `srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg` thuộc tập val:
  * **Thử nghiệm Zero-shot tiếng Anh** (`--texts "food . dish . plate ."`): Mô hình trích xuất visual tokens và bounding box chính xác các đĩa thức ăn. Kết quả lưu tại `llmdet_vietnamese_food/demo_output/zero_shot/vis/`.
  * **Thử nghiệm Zero-shot tiếng Việt** (`--texts "bánh tráng ."`): Mô hình phân tích thành công cụm từ tiếng Việt, chạy forward pass mượt mà trên GPU. Kết quả lưu tại `llmdet_vietnamese_food/demo_output/zero_shot_vi/vis/`.
* **Kết luận**: Pipeline mô hình, text encoder (BERT) và visual backbone (Swin-T) hoàn toàn thông suốt, sẵn sàng cho huấn luyện.

---

### 4. Thiết lập File Cấu hình Huấn luyện & Đánh giá (Bước 1.2 & 1.3)
1. **File cấu hình huấn luyện**: [`configs/grounding_dino_swin_t_vifood.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/grounding_dino_swin_t_vifood.py)
   * **Base**: Kế thừa kiến trúc chuẩn `grounding_dino_swin_t.py`.
   * **Cơ chế Detector-only**: Thiết lập `model.lmm = None` giúp tiết kiệm VRAM, tối ưu hóa tốc độ huấn luyện trên GPU RTX 3090 24GB.
   * **Dataset**: Định hình `ODVGDataset` trỏ vào `grounding_data/vifood/annotations/vifood_train_vg.jsonl` (900 ảnh train, chế độ `actual_dataset_mode='VG'`).
   * **Dataloader**: `batch_size=4`, `num_workers=4`, 225 batch/epoch.
   * **Schedule & Optimizer**: AdamW với `lr=5e-5`, warmup 500 iters, MultiStepLR milestones tại `[7000, 9000]`, tổng 10,000 iters (~44 epoch). Checkpoint lưu định kỳ mỗi 2,000 iters kèm đánh giá mAP tự động.
2. **File cấu hình kiểm thử độc lập**: [`configs/val/grounding_dino_swin_t_vifood_val.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/val/grounding_dino_swin_t_vifood_val.py)
   * Đánh giá trực tiếp trên `instances_val.json` (100 ảnh, 374 bboxes, 51 món ăn Việt Nam) sử dụng thước đo chuẩn `CocoMetric`.
3. **Kiểm tra nạp dữ liệu (Sanity Dataloader Test)**:
   * Chạy thử nghiệm nạp batch thực tế từ `configs/grounding_dino_swin_t_vifood.py`: Dataloader khởi tạo thành công 225 batches, tải trơn tru tensor ảnh, bounding boxes và text grounding annotations.

---

### 5. Kết luận & Sẵn sàng cho Pha 2
Pha 1 đã hoàn tất 100% mục tiêu kỹ thuật. Tất cả rào cản môi trường và mã nguồn đã được giải quyết. Có thể bấm lệnh huấn luyện Thí nghiệm 1 (Fine-tune với nhãn tiếng Việt) ngay lập tức.
