# NHẬT KÝ PHIÊN LÀM VIỆC: 25/09/2026
## Chủ đề: Trích xuất Bộ Dữ liệu ViFood-1K & Phân chia Train/Val

---

### 1. Thông tin chung
* **Thời gian**: 25/09/2026
* **Mục tiêu**: Trích xuất bộ dữ liệu chuẩn hóa 1.000 ảnh từ kho `vifood2.zip`, phân chia train/val và tạo file metadata thô.
* **Người thực hiện**: [Họ và tên của bạn]

---

### 2. Kỹ thuật Triển khai
* Xây dựng script `scripts/prepare_vifood_1k.py` (172 dòng code):
  1. **Đọc metadata từ kho zip**:
     - Phân tích danh mục 51 lớp món ăn trong `obj.names` (đã bổ sung rau xào, nước chấm, gà quay).
     - Đọc danh sách 1.000 ảnh đầu tiên từ file `train.txt`.
  2. **Chuyển đổi hệ tọa độ nhãn**:
     - Đọc file tọa độ YOLO normalized `[class_id, x_center, y_center, width, height]`.
     - Chuyển đổi chính xác sang hệ tọa độ pixel tuyệt đối góc trên-trái và góc dưới-phải:
       $$x_1 = (x_{center} - w/2) \times W, \quad y_1 = (y_{center} - h/2) \times H$$
       $$x_2 = (x_{center} + w/2) \times W, \quad y_2 = (y_{center} + h/2) \times H$$
  3. **Phân chia tập dữ liệu**:
     - **Tập Train (90%)**: 900 ảnh, lưu vào `grounding_data/vifood/images/train2017/`.
     - **Tập Val (10%)**: 100 ảnh, lưu vào `grounding_data/vifood/images/val2017/`.
  4. **Xuất Cache**: Lưu toàn bộ thông tin đối tượng vào `grounding_data/vifood/cache/vifood_1k_raw.json`.

---

### 3. Kết quả đạt được
* Đã sao chép và phân loại đầy đủ 1.000 bức ảnh độ phân giải cao vào cấu trúc thư mục chuẩn COCO/ODVG.
* Metadata thô hoàn thành, sẵn sàng cho công đoạn làm giàu ngôn ngữ (Language Enrichment) bằng Gemini.
