# NHẬT KÝ PHIÊN LÀM VIỆC: 15/09/2026
## Chủ đề: Nghiên cứu Kiến trúc LLMDet và Lập Đề xuất Đồ án Món ăn Việt Nam

---

### 1. Thông tin chung
* **Thời gian**: 15/09/2026
* **Mục tiêu**: Tìm hiểu sâu kiến trúc mô hình LLMDet (CVPR 2025 Highlight), đánh giá tính khả thi và lập đề xuất đề tài tốt nghiệp về Visual Grounding cho ẩm thực Việt Nam.
* **Người thực hiện**: [Họ và tên của bạn]

---

### 2. Bối cảnh & Vấn đề kỹ thuật
* **Bối cảnh Open-Vocabulary Object Detection (OV-OD)**: Các mô hình truyền thống (YOLO, Faster R-CNN) chỉ nhận diện số lượng lớp cố định. Các mô hình Grounding (GLIP, Grounding DINO) bắt đầu nhận diện được theo text prompt nhưng chỉ học trên cụm từ ngắn (short phrases) và thiếu hiểu biết ngữ cảnh toàn cục (global scene context).
* **Đột phá của LLMDet**: Sử dụng MLLM (LLaVA-Qwen2) để giám sát Detector qua hàm mất mát kép:
  1. Image-level Loss ($L_{image\_cap}$): Ép feature map ($P_4, P_5$) chứa tri thức toàn cảnh để sinh Long Caption.
  2. Region-level Loss ($L_{region\_cap}$): Ép Object Query chứa đặc trưng mịn của từng vùng để sinh Short Caption.
  3. Khi suy luận có thể ngắt bỏ LMM, tốc độ bằng Grounding DINO thông thường.
* **Vấn đề bài toán ẩm thực Việt Nam**: Các đề tài trước đây chủ yếu làm phân loại ảnh 1 đĩa (Classification). Mâm cơm Việt Nam có đặc thù nhiều món cùng lúc (sharing table), đòi hỏi mô hình phải định vị và phân biệt chính xác từng món/đĩa dựa trên ngôn ngữ tự nhiên.

---

### 3. Công việc chi tiết đã thực hiện
1. **Phân tích codebase & Lý thuyết**:
   - Soạn thảo tài liệu phân tích chuyên sâu: `llmdet_vietnamese_food/thesis_proposal_analysis.md`.
   - So sánh 2 hướng phát triển: Hướng Sản phẩm (Product/Edge) vs. Hướng Nghiên cứu (Academic/Novelty).
2. **Xây dựng Đề xuất Đồ án (Proposal)**:
   - Soạn thảo tài liệu: `llmdet_vietnamese_food/vietnamese_food_grounding_proposal.md`.
   - Xác định bài toán: *Multimodal Vietnamese Cuisine Grounding trên mâm cơm gia đình*.
   - Đưa ra giải pháp xử lý rào cản ngôn ngữ và cấu trúc phân cấp món ăn (món chính vs món thành phần).
3. **Khởi tạo hạ tầng dự án**:
   - Tách biệt 2 repository con: `llmdet_vietnamese_food` (mô hình/training) và `vietnamese-food-dataset` (thu thập/làm sạch dữ liệu).
   - Thiết lập cấu trúc thư mục chuẩn.

---

### 4. Kết quả đạt được
* Bản Proposal chi tiết dài 170+ dòng định hướng toàn bộ lộ trình 12-16 tuần của Đồ án.
* Báo cáo phân tích kỹ thuật kiến trúc LLMDet sẵn sàng đưa vào Chương 2 (Cơ sở lý thuyết) của Luận văn.

---

### 5. Ghi chú cho Báo cáo Luận văn
> *Nội dung ngày này phục vụ trực tiếp cho **Chương 1 (Giới thiệu bài toán & Mục tiêu đề tài)** và **Chương 2 (Tổng quan về Open-Vocabulary Object Detection và Kiến trúc LLMDet)**.*
