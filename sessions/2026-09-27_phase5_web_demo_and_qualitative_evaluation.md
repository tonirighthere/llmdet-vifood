# NHẬT KÝ PHIÊN LÀM VIỆC: 27/09/2026 (Tối)
## Chủ đề: Triển khai Pha 5 — Xây dựng Ứng dụng Web Demo Tương tác & Định lượng Hiệu năng Suy luận (Inference Benchmark)

---

### 1. Thông tin chung
* **Thời gian**: 27/09/2026 (17:15 – 17:30)
* **Mục tiêu**:
  1. Xây dựng cơ sở tri thức dinh dưỡng chuẩn cho 51 món ăn Việt Nam (`nutrition_vifood_51.json`).
  2. Phát triển ứng dụng Web trực quan hóa (Gradio Web App) hỗ trợ Visual Grounding tiếng Việt tự nhiên và tra cứu dinh dưỡng thời gian thực.
  3. Đo lường tốc độ suy luận (Latency, FPS, VRAM) của mô hình Grounding DINO Swin-T trên GPU RTX 3090.
  4. Xuất ảnh đối sánh trực quan (Qualitative Comparison) giữa 3 mô hình phục vụ slide thuyết trình và Luận văn tốt nghiệp.
* **Người thực hiện**: [Họ và tên của bạn]
* **Môi trường**: PyTorch 2.10, Gradio 5.50.0, MMDetection 3.3.0, GPU NVIDIA RTX 3090 (24GB).

---

### 2. Các công việc kỹ thuật đã hoàn thành

#### 2.1. Xây dựng Cơ sở Tri thức Dinh dưỡng 51 Món Ăn Việt Nam
* File dữ liệu: [`nutrition_vifood_51.json`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/nutrition_vifood_51.json).
* Chi tiết từng món gồm:
  * Tên tiếng Việt và tiếng Anh.
  * Khẩu phần tiêu chuẩn (ví dụ: *1 bát tô, 1 đĩa 6-8 cái, 1 ổ đầy đủ*).
  * Năng lượng (kcal) và hàm lượng 3 nhóm chất dinh dưỡng đa lượng (*Protein, Carbohydrates, Fat*).
  * Phân loại ẩm thực và ghi chú văn hóa / thành phần đặc trưng.

#### 2.2. Xây dựng Ứng dụng Web Demo Tương tác (`app.py`)
* Mã nguồn: [`app.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/app.py).
* Tính năng cốt lõi:
  * **Visual Grounding Tiếng Việt Đa Chế Độ**: Hỗ trợ cả câu miêu tả tự nhiên phong phú (*Exp 3 style*) lẫn danh sách nhãn rời rạc (*Exp 1 style*).
  * **Chuyển đổi Mô hình Linh hoạt**: Người dùng có thể chọn giữa **Exp 3 (Full VI Caption - Khuyên dùng ⭐)**, **Exp 1 (Short VI)** và **Zero-Shot Baseline** để thấy rõ sự khác biệt trực quan.
  * **Tự Động Tính Dinh Dưỡng Bữa Ăn**: Khớp nhãn phát hiện với cơ sở tri thức, tính tổng Calo và hiển thị bảng chi tiết các chất dinh dưỡng của mâm cơm.
  * **Giao diện Hiện đại 3 Tab**:
    * Tab 1: Định vị món ăn & Phân tích dinh dưỡng (kèm 5 ảnh mẫu test nhanh).
    * Tab 2: Báo cáo kết quả thực nghiệm học thuật (COCO Benchmark cho Luận văn).
    * Tab 3: Từ điển tra cứu 51 món ăn Việt Nam.
* Triển khai nền tảng: Chạy ngầm liên tục qua tmux session `vifood_web_app` trên cổng `http://0.0.0.0:7861`.

#### 2.3. Đo Kiểm Hiệu Năng Suy Luận (Inference Benchmark)
Chạy script kiểm thử chuyên dụng [`benchmark_inference_speed.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/benchmark_inference_speed.py) qua 30 lần suy luận liên tiếp trên GPU RTX 3090:

| Chỉ số hiệu năng | Giá trị thực nghiệm | Đánh giá kỹ thuật |
| :--- | :---: | :--- |
| **Độ trễ trung bình (Mean Latency)** | **150.84 ms** | Đạt chuẩn phản hồi nhanh thời gian thực (< 200ms) |
| **Độ trễ trung vị P50** | **147.58 ms** | Rất ổn định, không bị dao động lớn |
| **Độ trễ tối thiểu (Min Latency)** | **139.35 ms** | Tốc độ tối đa khi cache GPU tối ưu |
| **Tốc độ khung hình (Throughput)** | **6.63 FPS** | Đủ phục vụ ứng dụng Web/API cho nhiều người dùng |
| **VRAM tiêu thụ khi suy luận** | **978.7 MB (~0.96 GB)** | Chiếm chưa đến **4%** tổng VRAM 24GB của RTX 3090 |

#### 2.4. Xuất Ảnh Định Tính Đối Sánh (Qualitative Results)
Chạy script [`export_qualitative_results.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/export_qualitative_results.py) trên các ảnh validation mẫu:
* Thư mục lưu kết quả: [`demo_output/qualitative_comparison/`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/demo_output/qualitative_comparison).
* Kết quả phân tích:
  * **Zero-Shot Baseline**: Bỏ sót nhiều món, chỉ bắt được 1-2 box chung chung với confidence thấp.
  * **Exp 1 (Short VI)**: Phát hiện được món nhưng bị box chồng chéo hoặc nhận nhầm vùng rau/nước chấm.
  * **Exp 3 (Full VI Caption ⭐)**: Bắt trọn vẹn và chính xác từng món trong câu miêu tả tự nhiên (ví dụ đĩa Phở, đĩa rau sống, chén nước chấm) với độ tin cậy vượt trội.

#### 2.5. Nâng cấp Bộ Phân Tích Câu Truy Vấn Tiếng Việt Thông Minh (Smart NLP Query Parser)
* **Vấn đề phát hiện khi người dùng test thực tế**:
  * Khi người dùng gõ câu tìm kiếm tự nhiên như `"tìm tôm chiên và chả"`, Grounding DINO mặc định coi cả câu là 1 cụm danh từ duy nhất, dẫn đến việc gán nguyên cả câu `"tìm tôm chiên và chả"` lên cả 2 bounding box và gây lỗi tính dinh dưỡng.
* **Giải pháp đã triển khai trong `app.py`**:
  * Tích hợp hàm `parse_vietnamese_query(text)`:
    1. Tự động loại bỏ các từ tiền tố tìm kiếm (*"tìm", "hãy tìm giúp tôi", "cho tôi hỏi", "ở đâu có"...*).
    2. Tự động bóc tách theo liên từ (*"và", "với", "cùng", "kèm", "ăn kèm", dấu phẩy `,`...*).
    3. Tự động loại bỏ các từ chỉ dụng cụ đựng (*"đĩa", "bát", "tô", "dĩa", "chén", "rổ"...*).
    4. Chuẩn hóa thành định dạng thực thể phân tách: `"tôm chiên . chả ."`.
  * **Kết quả**: Box bên trái gán chính xác nhãn `tôm chiên`, box bên phải gán nhãn `chả`, và bảng dinh dưỡng tính đúng calo cho từng món.

---

#### 2.6. Nghiên cứu Tình huống Thực tế & Phân Tích Lỗi (Error Analysis & Data Scarcity Case Study)
*Phần số liệu cực kỳ đắt giá cho Mục 4.4 (Phân tích lỗi & Hạn chế) của Luận văn tốt nghiệp:*

* **Bối cảnh thử nghiệm**: Bức ảnh bàn tiệc buffet hải sản phức tạp với **hơn 15 đĩa đồ ăn** chen chúc (Cua, Tôm càng, Hàu nướng mỡ hành, Hàu phô mai, Ốc nhồi, Sò huyết, Bề bề, Cá hồi...).
* **Thử nghiệm 1 — Prompt đơn lẻ không có trong ảnh (`"tìm giúp tôi mực ."`):**
  * *Hiện tượng*: Bàn tiệc hoàn toàn KHÔNG có mực, nhưng mô hình lại khoanh vào đĩa ốc nhồi (43.3%) và đĩa sò huyết (36.3%) rồi gán nhãn `mực`.
  * *Nguyên nhân kỹ thuật*:
    1. **Thiếu nhãn cạnh tranh (Lack of Negative Competition)**: Prompt chỉ có 1 từ duy nhất, mô hình bị ép phải tìm vùng có đặc trưng thị giác gần nhất (hải sản vỏ sẫm màu) trong không gian embedding.
    2. **Độ tin cậy thấp (Confidence 36% - 43%)**: Ngưỡng lọc `0.25` quá thấp khiến các box "đoán mò" bị lọt qua. Khi nâng threshold lên $\ge 0.45$, cả 2 box sai biến mất hoàn toàn.
* **Thử nghiệm 2 — Prompt đa nhãn cạnh tranh (`"tìm cua, tôm, hàu, ốc và mực ."`):**
  * *Hiện tượng*:
    * Nhãn ảo `mực` **biến mất hoàn toàn** (không còn bị gán nhầm vào đâu).
    * Đĩa ốc được nhận đúng là `ốc`, đĩa cua được nhận đúng là `cua`.
    * Tuy nhiên, con cua to màu đỏ cam ở giữa bàn bị nhận nhầm thành `tôm 77.6%`, đĩa hàu phô mai màu vàng bị nhận thành `cua 48.5%`, và đĩa bề bề bị nhận thành `cua 54.7%`.
  * *Nguyên nhân sâu xa (Khẳng định giả thuyết thiếu dữ liệu - Data Starvation)*:
    1. **Thiên kiến màu sắc (Color Bias)**: Tập ViFood-1K chỉ có 900 ảnh train (~18 ảnh/lớp). Mô hình mới chỉ học được đặc trưng màu sắc (*"vùng đỏ cam = hải sản tôm/cua"*) chứ chưa học đủ sâu cấu trúc hình học (mai cua vs râu/đốt tôm).
    2. **Biến thể chế biến chưa có trong tập train**: Lớp `hàu` trong tập train chủ yếu là hàu sống/hàu mỡ hành, chưa có biến thể nướng phô mai đút lò màu vàng rực.
    3. **Món nằm ngoài 51 lớp (Unseen Classes)**: Bề bề và cá hồi sashimi không nằm trong danh mục 51 lớp của ViFood-1K, buộc mô hình phải ép gán vào lớp có trong prompt.

---

### 3. Kết luận & Chuyển giao sang Pha 6
* **Pha 5 đã hoàn tất 100% mục tiêu đề ra**.
* Sản phẩm Web Demo tương tác đã sẵn sàng phục vụ trình diễn trước Hội đồng bảo vệ đồ án tốt nghiệp.
* Toàn bộ mã nguồn, dữ liệu dinh dưỡng và ảnh kết quả đã được đóng gói hoàn chỉnh.

---

### 📚 4. BẢN ĐỒ ÁNH XẠ DỮ LIỆU ĐỂ VIẾT BÁO CÁO LUẬN VĂN (THESIS WRITING ROADMAP)

Khi bắt đầu viết Luận văn, bạn chỉ cần mở các file Session tương ứng để lấy toàn bộ bảng số liệu, biểu đồ, câu lệnh và phân tích lý thuyết:

| Chương Luận Văn | Tiêu Đề Chương | Nội Dung Chi Tiết Cần Viết | File Session Tham Khảo Trực Tiếp |
| :---: | :--- | :--- | :--- |
| **Chương 1** | **Mở đầu** | Tính cấp thiết, mục tiêu đề tài, phạm vi 51 món ăn Việt Nam, đóng góp chính. | [Session 01](file:///home/atin/tuan/SoPSoP/sessions/2026-09-15_proposal_and_architecture.md), [Session 08](file:///home/atin/tuan/SoPSoP/sessions/2026-09-26_odvg_enrichment_and_strategy.md) |
| **Chương 2** | **Tổng quan nghiên cứu** | Lý thuyết Open-Vocabulary Object Detection, Grounding DINO, Swin Transformer, BERT, ODVG Dual Caption format. | [Session 01](file:///home/atin/tuan/SoPSoP/sessions/2026-09-15_proposal_and_architecture.md), [Session 02](file:///home/atin/tuan/SoPSoP/sessions/2026-09-16_dataset_survey_and_codebase.md) |
| **Chương 3** | **Xây dựng Bộ dữ liệu ViFood-1K** | Pipeline hợp nhất 3 nguồn Roboflow, lọc nhãn Clean Rebuild v7, gán nhãn bổ sung với Gemini AI, sinh câu mô tả tự nhiên và tính `tokens_positive`. | [Session 03](file:///home/atin/tuan/SoPSoP/sessions/2026-09-17_roboflow_curation_pipeline.md), [Session 04](file:///home/atin/tuan/SoPSoP/sessions/2026-09-20_clean_rebuild_v7.md), [Session 05](file:///home/atin/tuan/SoPSoP/sessions/2026-09-22_gemini_supplement_boxes.md), [Session 07](file:///home/atin/tuan/SoPSoP/sessions/2026-09-25_prepare_vifood_1k.md), [Session 08](file:///home/atin/tuan/SoPSoP/sessions/2026-09-26_odvg_enrichment_and_strategy.md) |
| **Chương 4** | **Thực nghiệm & Đánh giá (Trọng tâm)** | • Thiết lập huấn luyện (Pha 1, 2, 3, 3.5)<br>• Bảng Benchmark 4 mô hình (Pha 4: mAP, Recall, mAP_75)<br>• So sánh Ablation tiếng Việt vs tiếng Anh<br>• Phân tích lỗi (Error Analysis) mâm hải sản. | [Session 09](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase1_sanity_check_and_configs.md), [Session 10](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase2_training_completion.md), [Session 11](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase3_english_ablation_launch.md), [Session 12](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase3_5_exp3_training_completion.md), [Session 13](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase4_benchmark_and_evaluation.md), [Session 14](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase5_web_demo_and_qualitative_evaluation.md) |
| **Chương 5** | **Xây dựng Hệ thống Ứng dụng Thực tế** | Kiến trúc Web App Gradio, bộ phân tích tiếng Việt Smart NLP Parser, module cơ sở tri thức dinh dưỡng 51 món, đo kiểm độ trễ 150ms trên GPU RTX 3090. | [Session 14](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase5_web_demo_and_qualitative_evaluation.md), [`nutrition_vifood_51.json`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/nutrition_vifood_51.json) |
| **Chương 6** | **Kết luận & Hướng phát triển** | Tổng kết thành tựu, giải thích giới hạn 1K ảnh, lộ trình mở rộng dữ liệu lên 5K-10K và thay thế text encoder PhoBERT/XLM-R. | [Session 13](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase4_benchmark_and_evaluation.md), [PLAN_NEXT_STEPS.md](file:///home/atin/tuan/SoPSoP/sessions/PLAN_NEXT_STEPS.md) |

