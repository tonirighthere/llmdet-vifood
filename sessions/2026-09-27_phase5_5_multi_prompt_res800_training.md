# Session Log: Triển Khai Cải Thiện Bước 2 (Multi-Prompting) & Bước 3 (High-Resolution 800x1333)

**Ngày thực hiện:** 27/09/2026  
**Mục tiêu:** Thực hiện 2 hướng cải thiện tối ưu nhất cho bài toán Grounding DINO trên tập dữ liệu ẩm thực Việt Nam (ViFood-51), kiểm tra tính khả dụng của Google Gemini API, và tiến hành huấn luyện mô hình thế hệ tiếp theo (Experiment 4).

---

## 1. Kiểm Tra Quota & Tính Khả Dụng Gemini API
- **Mục tiêu:** Kiểm tra key `GEMINI_API_KEY` trong môi trường xem có bị cạn hạn mức (rate limit / quota exceeded) hay không.
- **Phương pháp kiểm tra:** Gửi cURL test request trực tiếp đến Google Generative Language API (`v1beta`).
- **Phát hiện:** 
  - Các model cũ (`gemini-2.0-flash`, `gemini-2.5-flash`) đã bị deprecate hoặc không khả dụng trên endpoint, trả về mã 404 NOT_FOUND.
  - Model thế hệ mới nhất khả dụng là **`gemini-3.8-flash`**.
- **Kết quả:** Request thành công với mã **HTTP 200 OK**, trả về kết quả chuẩn xác. API key còn nguyên quota, sẵn sàng phục vụ cho các tác vụ sinh prompt tự động hoặc phân tích thị giác nâng cao.

---

## 2. Bước 2: Tăng Cường Dữ Liệu Qua Multi-Prompting (x3 Dữ Liệu Ngữ Cảnh)
- **Vấn đề đã nhận diện ở Exp 3:** Mô hình chỉ được học dạng prompt đơn điệu `"tên món . tên món ."`, dẫn đến việc khi người dùng nhập câu tự nhiên (như `"tìm đĩa cua"`, `"trong hình có món gì"`), mô hình bị bỡ ngỡ hoặc over-predicting do thiếu sự cạnh tranh ngữ nghĩa.
- **Giải pháp:** Xây dựng script đa dạng hóa prompt: [`scripts/build_multi_prompt_odvg.py`](file:///home/atin/tuan/SoPSoP/scripts/build_multi_prompt_odvg.py).
- **3 Phong cách prompt được tích hợp cho mỗi bức ảnh:**
  1. **Phong cách Miêu tả Chi tiết (Rich Caption):**
     * Ví dụ: `"Một bức ảnh ẩm thực hấp dẫn gồm có cá kho tộ, canh chua và cơm trắng được bày trí đẹp mắt trên bàn ăn."`
  2. **Phong cách Truy vấn Tìm kiếm (Search & Locational Query):**
     * Ví dụ: `"Hãy xác định vị trí của cá kho tộ, canh chua, cơm trắng trong bữa ăn."`
  3. **Phong cách Danh sách Thực thể Chuẩn (Discrete Entity List):**
     * Ví dụ: `"cá kho tộ . canh chua . cơm trắng ."`
- **Tập dữ liệu xuất xưởng:** [`grounding_data/vifood/annotations/vifood_train_vg_vi_multi.jsonl`](file:///home/atin/tuan/SoPSoP/grounding_data/vifood/annotations/vifood_train_vg_vi_multi.jsonl).
  - Tổng số mẫu học: **2,700 mẫu** (900 ảnh $\times$ 3 biến thể văn bản).
  - Kiểm thử chất lượng: **12,084 / 12,084** token spans positive được kiểm tra tự động, đạt độ chính xác **100.00%** tuyệt đối.

---

## 3. Bước 3: Nâng Cấp Độ Phân Giải Đa Tỉ Lệ (Multi-Scale Training Lên Đến 800x1333)
- **Vấn đề đã nhận diện ở Exp 3:** Huấn luyện ở kích thước cố định $640 \times 640$ khiến các chi tiết nhỏ của món ăn (ví dụ: sợi bún, lát ớt, tép tỏi, miếng chả nhỏ) bị mất mát đặc trưng sau qua các tầng downsampling của Swin Transformer.
- **Cấu hình huấn luyện mới:** [`configs/grounding_dino_swin_t_vifood_multi_res800.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/grounding_dino_swin_t_vifood_multi_res800.py).
  - Pipeline hình ảnh: Đa tỉ lệ ngẫu nhiên (Random Choice Multi-Scale):
    `scales = [(480, 1333), (560, 1333), (640, 1333), (720, 1333), (800, 1333)]`.
  - Max scale: Cạnh dài tối đa lên tới 1333 pixel, cạnh ngắn tối đa 800 pixel (chuẩn vàng của Grounding DINO / DINO benchmark).
- **Tối ưu hóa VRAM trên GPU RTX 3090:**
  - VRAM nền của máy chủ đang chiếm ~10.3 GB bởi các tác vụ đồ họa khác.
  - Thiết lập: `batch_size = 2` trên mỗi GPU, kết hợp `accumulative_counts = 2`.
  - Hiệu quả: Duy trì batch size tương đương 4 (đảm bảo độ ổn định gradient và học sâu), nhưng VRAM thực tế chỉ tiêu tốn **~4.4 GB - 4.5 GB**, triệt tiêu 100% rủi ro tràn bộ nhớ (Out-Of-Memory).

---

## 4. Trạng Thái Huấn Luyện (Experiment 4)
- **Lệnh thực thi:**
  ```bash
  python3 mmdet_train.py configs/grounding_dino_swin_t_vifood_multi_res800.py --work-dir work_dirs/vifood_multi_res800 --amp
  ```
- **Quản lý phiên:** Chạy ngầm trong tmux session `vifood_multi_train`.
- **Tốc độ huấn luyện:** ~0.56 giây / iteration.
- **Dung lượng bộ nhớ GPU:** ~4,461 MB / 24,576 MB.
- **Thời gian hoàn thành dự kiến (ETA):** ~1 giờ 33 phút cho toàn bộ 10,000 iterations.
- **Tần suất lưu checkpoint:** Mỗi 2,000 iterations (`iter_2000.pth`, `iter_4000.pth`, ..., `iter_10000.pth`).

---

## 5. Web Demo Phục Vụ Thử Nghiệm Trực Quan
- Web Demo ứng dụng Streamlit (Phase 5) tiếp tục chạy nền ổn định trên cổng `7861` (tmux session `vifood_web_app`).
- Đã trang bị bộ phân tích truy vấn tiếng Việt thông minh `parse_vietnamese_query` để trích xuất món ăn từ câu hỏi tự nhiên của người dùng.
- Sau khi Exp 4 huấn luyện xong, checkpoint `work_dirs/vifood_multi_res800/iter_10000.pth` sẽ được tích hợp trực tiếp vào thanh chọn Model trên Web Demo để đối chứng ngay lập tức.
