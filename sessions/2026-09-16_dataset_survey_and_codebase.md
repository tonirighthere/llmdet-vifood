# NHẬT KÝ PHIÊN LÀM VIỆC: 16/09/2026
## Chủ đề: Khảo sát Nguồn Dữ liệu Món ăn & Bóc tách Mã nguồn LLMDet

---

### 1. Thông tin chung
* **Thời gian**: 16/09/2026
* **Mục tiêu**: Khảo sát hiện trạng các bộ dữ liệu món ăn Việt Nam hiện có và bóc tách luồng mã nguồn huấn luyện của LLMDet.
* **Người thực hiện**: [Họ và tên của bạn]

---

### 2. Khảo sát Hiện trạng Dữ liệu (State of Data)
* **Khảo sát các tập dữ liệu công khai**:
  * **Food-101**: 101 món phương Tây, chỉ là Classification ảnh đơn lẻ.
  * **VinAI Food-20 / VFOOD**: Dữ liệu món Việt Nam nhưng chủ yếu ở dạng phân loại 1 đĩa/bát ở chính giữa khung hình.
  * **Khoảng trống tri thức (Knowledge Gap)**: Chưa có tập dữ liệu công khai nào có ảnh mâm cơm thực tế (3 - 8 món/bàn) kèm Bounding Box và mô tả Grounding Caption tự nhiên.
* **Quyết định**: Cần tự xây dựng bộ benchmark mang tên **ViFood-Grounding** để phục vụ việc huấn luyện và đánh giá.

---

### 3. Công việc chi tiết đã thực hiện
1. **Bóc tách mã nguồn LLMDet**:
   - Nghiên cứu cơ chế nạp dữ liệu ODVG trong `mmdet/datasets/odvg.py`: Hiểu cách lớp `ODVGDataset` đọc file JSONL, xử lý 2 trường hợp `actual_dataset_mode='OD'` và `actual_dataset_mode='VG'`.
   - Phân tích cơ chế căn chỉnh tokens (`tokens_positive`): Mỗi bounding box cần trỏ chính xác vào chỉ số ký tự `[start_char, end_char]` trong câu `caption` tổng.
   - Biên soạn tài liệu hướng dẫn kỹ thuật mã nguồn: `llmdet_vietnamese_food/llmdet_codebase_guide.md` (giải thích chi tiết tác dụng của từng file `configs/`, `mmdet/`, `llava/`, `hf_model/`).
2. **Khởi tạo kế hoạch gán nhãn**:
   - Thiết lập cấu trúc thư mục dữ liệu đích: `grounding_data/vifood/images/` và `grounding_data/vifood/annotations/`.

---

### 4. Kết quả đạt được
* Tài liệu `llmdet_codebase_guide.md` dài 260+ dòng làm kim chỉ nam kỹ thuật cho nhóm.
* Xác định rõ định dạng đầu ra bắt buộc của dữ liệu: File định dạng JSONL (ODVG format).

---

### 5. Ghi chú cho Báo cáo Luận văn
> *Phần so sánh các bộ dữ liệu Food AI sẽ đưa vào **Chương 2 (Khảo sát các nghiên cứu liên quan)**.*
