# NHẬT KÝ PHIÊN LÀM VIỆC: 23/09/2026 – 24/09/2026
## Chủ đề: Cài đặt Môi trường Huấn luyện & Tải Trọng số Pretrained

---

### 1. Thông tin chung
* **Thời gian**: 23/09/2026 – 24/09/2026
* **Mục tiêu**: Cài đặt môi trường Deep Learning tương thích hoàn toàn với kiến trúc LLMDet và tải các trọng số pretrained cốt lõi.
* **Người thực hiện**: [Họ và tên của bạn]
* **Cấu hình phần cứng**: Máy trạm GPU NVIDIA GeForce RTX 3090 (24GB VRAM), RAM 64GB, CPU Intel Xeon / AMD tương đương.

---

### 2. Thiết lập Môi trường (Environment Setup)
* **Các thư viện đã cài đặt và kiểm thử tính tương thích**:
  * Python `3.11.x` trong môi trường Conda `/home/atin/miniconda/`.
  * PyTorch `2.10.0+cu128`, Torchvision `0.25.0`, CUDA Version `13.0`.
  * OpenMMLab Core: MMDetection `3.3.0`, MMEngine `0.10.7`.
  * HuggingFace: Transformers `4.57.1`, Accelerate `1.11.0`, PEFT `0.17.1`, Timm `1.0.29`.
* **Ghi nhận**: Tất cả thư viện biên dịch CUDA C++ thành công, sẵn sàng hỗ trợ Multi-scale Deformable Attention trong Grounding DINO.

---

### 3. Tải và Xác thực Trọng số Pretrained
* Phát triển script `scripts/download_weights.py` (89 dòng code):
  1. **Text Backbone**: Tải toàn bộ `google-bert/bert-base-uncased` (gồm `pytorch_model.bin`, `vocab.txt`, `config.json`) lưu vào `huggingface/bert-base-uncased/`.
  2. **Detector Backbone**: Tải checkpoint `grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth` (1.09 GB) từ OpenMMLab lưu vào `huggingface/mm_grounding_dino/`.
  3. Tích hợp cơ chế kiểm tra dung lượng file và thanh tiến trình `reporthook` tránh lỗi mạng ngắt quãng.

---

### 4. Kết quả đạt được
* Môi trường thực nghiệm hoàn chỉnh không bị xung đột phiên bản.
* Đã tải sẵn sàng các trọng số nặng cần thiết cho quá trình fine-tuning.
