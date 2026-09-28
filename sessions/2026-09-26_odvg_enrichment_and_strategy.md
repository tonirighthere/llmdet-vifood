# NHẬT KÝ PHIÊN LÀM VIỆC: 26/09/2026
## Chủ đề: Sinh Dual-Caption Gemini, Đóng gói ODVG JSONL & Định hình Chiến lược Đồ án

---

### 1. Thông tin chung
* **Thời gian**: 26/09/2026
* **Mục tiêu**: Hoàn thiện toàn bộ pipeline làm giàu caption bằng Gemini API, đóng gói chuẩn ODVG JSONL cho LLMDet và định hình chiến lược nghiên cứu cho Đồ án.
* **Người thực hiện**: [Họ và tên của bạn]

---

### 2. Công việc Kỹ thuật Chi tiết
1. **Phát triển Pipeline Làm giàu Dữ liệu đa luồng**:
   - Viết và hoàn thiện `scripts/enrich_and_build_odvg.py` (349 dòng code).
   - **Xây dựng Taxonomy 51 class song ngữ**: Ánh xạ từng món ăn Việt Nam sang tên tiếng Anh ẩm thực chuẩn và đoạn miêu tả ngắn (ví dụ: `bánh bèo` $\rightarrow$ `steamed rice cakes` / `savory steamed rice cakes topped with minced shrimp...`).
   - **Sinh Long Caption đa luồng**:
     - Phân tích 200 tổ hợp món ăn xuất hiện trong 1.000 ảnh.
     - Sử dụng `ThreadPoolExecutor(max_workers=10)` kết nối Gemini API (`gemini-3.6-flash`).
     - Tự động sinh 180 câu Long Caption sinh động, mô tả toàn cảnh màu sắc, cách bài trí và nguyên liệu mâm cơm.
     - Tích hợp bộ nhớ đệm `gemini_captions.json` và cơ chế fallback caption tự động tránh lỗi rate-limit.
2. **Thuật toán Tính toán Character Offsets (`tokens_positive`)**:
   - Đối với bài toán Phrase Grounding trong LLMDet, mỗi Bounding Box phải có nhãn `tokens_positive` chỉ đúng chỉ số index ký tự `[start, end]` trong chuỗi `grounding.caption`.
   - Thuật toán đã duyệt chính xác từng từ tiếng Việt trong câu nối `" . "`, đảm bảo không bị lệch offset kể cả với ký tự Unicode có dấu.
3. **Đóng gói xuất bản dữ liệu**:
   - `grounding_data/vifood/annotations/vifood_train_vg.jsonl`: 900 mẫu huấn luyện chuẩn ODVG.
   - `grounding_data/vifood/annotations/vifood_val_vg.jsonl`: 100 mẫu kiểm thử chuẩn ODVG.
   - `grounding_data/vifood/annotations/instances_val.json`: 100 ảnh, 374 bounding boxes định dạng COCO phục vụ đánh giá $mAP$.
   - `grounding_data/vifood/annotations/label_map.json`: Danh mục 51 classes.

---

### 3. Nghiên cứu Bản chất Ngôn ngữ & Quyết định Chiến lược Đồ án
* **Phân tích vấn đề Tokenizer**:
  - `bert-base-uncased` của LLMDet vốn pretrain trên tiếng Anh.
  - Khi đưa nhãn tiếng Việt có dấu (`"bánh bèo"`), tokenizer sẽ bẻ gãy từ thành các subwords vụn, làm giảm hiệu quả căn chỉnh đặc trưng (Vision-Language Alignment).
* **Quyết định Chiến lược "Ăn điểm cao" cho Đồ án**:
  - **Không chọn một chiều**: Thay vì chỉ dùng tiếng Anh hoặc chỉ dùng tiếng Việt, chọn **Chiến lược Lai Song ngữ có Thực nghiệm Đối chứng (Hybrid Bilingual with Ablation Study)**.
  - Thiết kế bảng thực nghiệm so sánh: Baseline Tiếng Việt (Direct Vietnamese) vs. Baseline Tiếng Anh (English Grounding) vs. Phương pháp Đề xuất (Bilingual Language Bridge / Adapter).
  - Người dùng cuối sử dụng 100% giao diện và prompt Tiếng Việt.

---

### 4. Kết quả & Tình trạng Hiện tại
* ✅ Toàn bộ 1.000 ảnh và nhãn ODVG đã đóng gói hoàn hảo, không có lỗi định dạng.
* ✅ Đã xác định rõ ràng câu chuyện khoa học (Research Story) và cấu trúc các chương cho cuốn Luận văn tốt nghiệp.
* 🚀 Sẵn sàng bấm lệnh huấn luyện mô hình fine-tuning.
