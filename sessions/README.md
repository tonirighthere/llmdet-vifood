# MỤC LỤC NHẬT KÝ CÁC PHIÊN LÀM VIỆC (DAILY SESSIONS LOG)
## Đồ án: Phát hiện và Định vị Món ăn Việt Nam (LLMDet Vietnamese Food)

---

Thư mục này lưu trữ chi tiết tiến độ công việc kỹ thuật đã thực hiện theo từng ngày. Mỗi phiên làm việc (session) ghi chép đầy đủ: mục tiêu, vấn đề kỹ thuật, giải pháp, file code phát triển, kết quả định lượng và ghi chú đóng góp cho Luận văn tốt nghiệp.

### 📚 Danh sách các Phiên làm việc (Sessions):

| Ngày | Phiên làm việc | Trọng tâm công việc | Liên kết trực tiếp |
| :---: | :--- | :--- | :--- |
| **15/09/2026** | **Session 01** | Nghiên cứu kiến trúc LLMDet (CVPR 2025) & Soạn thảo Đề xuất Đồ án (Proposal) | [2026-09-15_proposal_and_architecture.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-15_proposal_and_architecture.md) |
| **16/09/2026** | **Session 02** | Khảo sát dữ liệu món ăn hiện có & Bóc tách cấu trúc mã nguồn LLMDet | [2026-09-16_dataset_survey_and_codebase.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-16_dataset_survey_and_codebase.md) |
| **17/09/2026** | **Session 03** | Tích hợp 3 nguồn Roboflow & Thiết kế pipeline sàng lọc nhãn thô | [2026-09-17_roboflow_curation_pipeline.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-17_roboflow_curation_pipeline.md) |
| **20/09/2026** | **Session 04** | Hoàn thiện pipeline Clean Rebuild v7 (Hợp nhất phân cấp 43 classes, lọc box rác) | [2026-09-20_clean_rebuild_v7.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-20_clean_rebuild_v7.md) |
| **22/09/2026** | **Session 05** | Gán nhãn bổ sung bán tự động với Gemini API (quét đĩa còn sót trên mâm cơm) | [2026-09-22_gemini_supplement_boxes.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-22_gemini_supplement_boxes.md) |
| **23/09/2026** | **Session 06** | Thiết lập môi trường PyTorch 2.10, MMDet 3.3.0 & Tải trọng số BERT, Grounding DINO | [2026-09-23_environment_setup_and_weights.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-23_environment_setup_and_weights.md) |
| **25/09/2026** | **Session 07** | Trích xuất bộ dữ liệu ViFood-1K (900 train / 100 val) & Chuyển đổi tọa độ box | [2026-09-25_prepare_vifood_1k.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-25_prepare_vifood_1k.md) |
| **26/09/2026** | **Session 08** | Sinh Dual-Caption Gemini, tính tokens_positive, đóng gói ODVG JSONL & Định hình chiến lược Đồ án | [2026-09-26_odvg_enrichment_and_strategy.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-26_odvg_enrichment_and_strategy.md) |
| **27/09/2026** | **Session 09** | Pha 1: Fix lỗi môi trường PyTorch 2.6/Transformers, Sanity check Zero-shot & Thiết lập Config Huấn luyện ViFood | [2026-09-27_phase1_sanity_check_and_configs.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase1_sanity_check_and_configs.md) |
| **27/09/2026** | **Session 10** | Pha 2: Hoàn tất Huấn luyện 10,000 iters Thí nghiệm 1 (Fine-tune Grounding DINO Tiếng Việt) & Kiểm chứng Trực quan | [2026-09-27_phase2_training_completion.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase2_training_completion.md) |
| **27/09/2026** | **Session 11** | Pha 3: Sinh Dữ liệu Tiếng Anh & Hoàn tất Huấn luyện Thí nghiệm 2 (Ablation Study) | [2026-09-27_phase3_english_ablation_launch.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase3_english_ablation_launch.md) |
| **27/09/2026** | **Session 12** | Pha 3.5: Hoàn tất Huấn luyện 10,000 iters Thí nghiệm 3 (Full VI Natural Caption Grounding — Đóng góp cốt lõi) | [2026-09-27_phase3_5_exp3_training_completion.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase3_5_exp3_training_completion.md) |
| **27/09/2026** | **Session 13** | Pha 4: Đánh giá Định lượng COCO Metric (mAP/Recall) & Lập Bảng Benchmark Toàn diện 4 Mô hình | [2026-09-27_phase4_benchmark_and_evaluation.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase4_benchmark_and_evaluation.md) |
| **27/09/2026** | **Session 14** | Pha 5: Xây dựng Ứng dụng Web Demo Tương tác (Gradio), Tích hợp Module Dinh Dưỡng & Đo Hiệu năng Suy luận | [2026-09-27_phase5_web_demo_and_qualitative_evaluation.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase5_web_demo_and_qualitative_evaluation.md) |
| **27/09/2026** | **Session 15** | Pha 5.5: Triển khai Cải tiến Bước 2 (Multi-Prompting x3) & Bước 3 (High-Res 800 Multi-Scale Training), Kiểm tra Gemini API | [2026-09-27_phase5_5_multi_prompt_res800_training.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase5_5_multi_prompt_res800_training.md) |
| **28/09/2026** | **Session 16** | Pha 5.6: Hoàn tất Huấn luyện Exp 4 (10,000 iters), Đánh giá Benchmark Định lượng COCO & Cập nhật Web Demo | [2026-09-28_phase5_6_exp4_evaluation_and_app_update.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-28_phase5_6_exp4_evaluation_and_app_update.md) |
| **27/10/2026** | **Session 17** | Pha 0 ViFood-54: taxonomy 54 lớp, gộp 2 zip CVAT, split theo ảnh gốc, cân bằng lớp (RFS + class dropout), B0 zero-shot & khởi chạy B1 (OD + negative) — kế hoạch tiếp: [PLAN_VIFOOD54.md](PLAN_VIFOOD54.md) | [2026-10-27_vifood54_phase0_b1_od.md](2026-10-27_vifood54_phase0_b1_od.md) |
| **28/10/2026** | **Session 18** | Pha 1: test B1 (mAP 0.310) + phân tích lỗi; Pha 2: bộ sinh caption hình thái (attribute bank, lint BERT bỏ dấu, 6 biến thể/ảnh) | [2026-10-28_phase1_b1_od_training_completion.md](2026-10-28_phase1_b1_od_training_completion.md) · [2026-10-28_phase2_morphology_captions.md](2026-10-28_phase2_morphology_captions.md) |
| **31/10/2026** | **Session 19** | Nhãn sửa qua crops_review; taxonomy v2 (trường visual, supercategory, confusable_with, ov_split, nutrition_key); build lại Pha 0/2 giữ split; train lại B1 | [2026-10-31_relabel_taxonomy_v2.md](2026-10-31_relabel_taxonomy_v2.md) |
| **31/10/2026** | **Session 20** | Pha 3: loader caption VG (biến thể + bản lật, negative khó từ confusable_with), config B3 trộn OD+VG, chạy B3 | [2026-10-31_phase3_b3.md](2026-10-31_phase3_b3.md) |
| **01/11/2026** | **Session 21** | Grounding câu (B3 L2 R@1 0.774 vs B1-v2 0.363), B3b tốt nhất (mAP 0.323); thí nghiệm OV base/novel | [2026-10-31_phase3_b3.md](2026-10-31_phase3_b3.md) · [2026-11-01_ov_experiment.md](2026-11-01_ov_experiment.md) |

---

### 🎯 Hướng dẫn sử dụng toàn diện khi Viết Báo cáo Luận văn:
* **Chương 1 (Mở đầu & Mục tiêu đề tài)**: Tham khảo `Session 01` và `Session 08`.
* **Chương 2 (Tổng quan Open-Vocabulary & Grounding DINO)**: Tham khảo `Session 01` và `Session 02`.
* **Chương 3 (Xây dựng Bộ dữ liệu ViFood-1K)**: Tham khảo `Session 03`, `Session 04`, `Session 05`, `Session 07` và `Session 08`.
* **Chương 4 (Thực nghiệm, Benchmark & Phân tích lỗi)**: Tham khảo `Session 09`, `Session 10`, `Session 11`, `Session 12`, `Session 13` và phần Case Study trong `Session 14`.
* **Chương 5 (Xây dựng Ứng dụng Web Demo & Dinh dưỡng)**: Tham khảo `Session 14` và file `nutrition_vifood_51.json`.
* **Chương 6 (Kết luận & Hướng phát triển mở rộng)**: Tham khảo `Session 13`, `Session 14` và `PLAN_NEXT_STEPS.md`.
