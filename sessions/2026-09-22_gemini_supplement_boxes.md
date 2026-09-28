# NHẬT KÝ PHIÊN LÀM VIỆC: 22/09/2026
## Chủ đề: Bổ sung Bounding Box Bán tự động bằng Vision-Language Model (Gemini)

---

### 1. Thông tin chung
* **Thời gian**: 22/09/2026
* **Mục tiêu**: Tận dụng khả năng Zero-shot của mô hình đa phương thức Gemini để phát hiện các đĩa món ăn còn sót trên mâm cơm mà các nhãn cũ chưa khoanh vùng.
* **Người thực hiện**: [Họ và tên của bạn]

---

### 2. Ý tưởng & Cơ chế Kỹ thuật
* **Vấn đề thực tế**: Trong một bức ảnh mâm cơm gia đình có 5-6 đĩa thức ăn, nhưng người gán nhãn thủ công hoặc dataset cũ chỉ khoanh 1-2 đĩa chính (ví dụ khoanh bát phở nhưng bỏ sót đĩa quẩy, bát nước chấm hay đĩa rau sống).
* **Giải pháp đề xuất**: Xây dựng script `vietnamese-food-dataset/scripts/supplement_gemini_boxes.py` (401 dòng code):
  1. **Bảo tồn Ground Truth**: Giữ nguyên 100% tất cả các bounding box đã có nhãn chuẩn của con người.
  2. **VLM Scanning**: Đưa ảnh vào Gemini API để mô hình liệt kê tất cả các món ăn có trong ảnh kèm tọa độ tương đối.
  3. **IoU Matching & Deduplication**:
     - Tính $IoU$ giữa box do Gemini đề xuất với tất cả các box cũ.
     - Nếu $IoU \ge 0.4$: Vị trí này đã có nhãn $\rightarrow$ Bỏ qua (không ghi đè).
     - Nếu $IoU < 0.4$: Đây là một món ăn mới bị sót $\rightarrow$ Bổ sung vào dataset.
  4. **Lọc phi ẩm thực (Non-food Filtering)**: Loại bỏ các vật dụng bàn ăn như bát rỗng, đũa, thìa, cốc, khăn giấy... bằng tập luật `IGNORE_ITEMS`.
  5. **Checkpointing**: Lưu cache tiến độ để có thể dừng/chạy tiếp mà không tốn quota API.

---

### 3. Kết quả đạt được
* Số lượng bounding box trên toàn bộ tập dữ liệu tăng thêm đáng kể (~20-30% số box), đặc biệt là các thành phần món phụ (rau sống, nước chấm, dưa góp).
* Đóng gói tập dữ liệu cập nhật mới `vietnamese_food_dataset_2000.zip` và `vifood2.zip`.

---

### 4. Ghi chú cho Báo cáo Luận văn
> *Nội dung này là minh chứng cho đóng góp: **"Quy trình gán nhãn bán tự động ứng dụng Mô hình Thị giác - Ngôn ngữ lớn (VLM-assisted Semi-Automatic Annotation Pipeline)"**.*
