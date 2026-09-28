# NHẬT KÝ PHIÊN LÀM VIỆC: 17/09/2026
## Chủ đề: Tích hợp Nguồn Roboflow & Thiết kế Pipeline Curation Dữ liệu

---

### 1. Thông tin chung
* **Thời gian**: 17/09/2026
* **Mục tiêu**: Tích hợp các bộ dữ liệu món ăn thô từ 3 dự án Roboflow mở và xây dựng pipeline sàng lọc nhãn.
* **Người thực hiện**: [Họ và tên của bạn]

---

### 2. Vấn đề của Dữ liệu thô từ Roboflow
* Dữ liệu từ 3 nguồn (`Source A`, `Source B`, `Source C`) có hơn 2.500 ảnh, tuy nhiên gặp phải các nhược điểm nghiêm trọng:
  1. **Nhãn không đồng nhất**: Cùng là món phở nhưng có nguồn ghi `pho_bo`, nguồn ghi `pho`, nguồn ghi `vietnamese noodle`.
  2. **Trùng lặp & Phân mảnh**: Quá nhiều class con lẻ tẻ (hơn 80 class), gây hiện tượng "đuôi dài" (long-tail imbalance), có class chỉ có 2-3 ảnh.
  3. **Hộp ảo (AI-generated candidates)**: Một số nguồn dùng mô hình sơ bộ tự gắn box nháp nhưng chưa qua kiểm duyệt, xuất hiện nhiều box rỗng hoặc vẽ trúng cái đĩa/chiếc thìa.

---

### 3. Công việc chi tiết đã thực hiện
1. **Thiết kế Pipeline xử lý**:
   - Viết module tải trực tiếp dữ liệu qua API / RemoteZip: Cho phép stream file zip từ Roboflow về mà không cần tải thủ công qua trình duyệt.
   - Xây dựng từ điển ánh xạ chuẩn hóa nhãn ban đầu (Label Normalization Map).
2. **Cấu hình công cụ kiểm định**:
   - Viết script chuyển đổi sang định dạng COCO chuẩn tương thích công cụ CVAT / Label Studio.
   - Soạn thảo tài liệu hướng dẫn quy trình kiểm tra nhãn cho các thành viên.

---

### 4. Kết quả đạt được
* Thu thập thành công ~2.000 ảnh thô và lưu trữ tại `vietnamese-food-dataset/data/raw/roboflow_food_v6/`.
* Xác định danh sách các vấn đề chất lượng cần lọc bỏ ở phiên làm việc tiếp theo.
