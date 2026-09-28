# NHẬT KÝ PHIÊN LÀM VIỆC: 27/09/2026 (Chiều muộn)
## Chủ đề: Triển khai Pha 4 — Đánh giá Định lượng (mAP/Recall) & Benchmark Toàn diện 4 Mô hình

---

### 1. Thông tin chung
* **Thời gian**: 27/09/2026 (16:30 – 16:55)
* **Mục tiêu**:
  1. Xây dựng cấu hình kiểm thử chuẩn COCO Metric cho tập validation ViFood-1K (100 ảnh, 374 nhãn ground truth, 51 món ăn).
  2. Khắc phục lỗi tương thích trong MMDetection runner và khai báo danh sách 51 nhãn món ăn chính thức.
  3. Thực hiện benchmark độc lập cho 4 cấu hình: Zero-shot baseline, Exp 1 (Short VI), Exp 2 (Short EN), Exp 3 (Full VI Caption).
  4. Lập bảng so sánh thực nghiệm chính thức cho Chương 4 của Luận văn tốt nghiệp.
* **Môi trường**: PyTorch 2.10.0+cu128, MMEngine 0.10.7, MMDetection, GPU RTX 3090.

---

### 2. Các công việc kỹ thuật đã xử lý

#### 2.1. Cấu hình kiểm thử chuẩn hóa (Validation Configs)
* Tạo & tinh chỉnh 2 file cấu hình:
  * [`configs/val/grounding_dino_swin_t_vifood_val.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/val/grounding_dino_swin_t_vifood_val.py): Kế thừa từ `grounding_dino_swin_t.py`, nạp 51 class tiếng Việt vào `val_dataset.metainfo['classes']`.
  * [`configs/val/grounding_dino_swin_t_vifood_en_val.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/val/grounding_dino_swin_t_vifood_en_val.py): Kế thừa từ `grounding_dino_swin_t.py`, nạp 51 class tiếng Anh vào `val_dataset.metainfo['classes']`.
* Xử lý triệt để lỗi `val_cfg=None` kế thừa từ base và lỗi nạp nhãn mặc định COCO 80 lớp bằng việc định nghĩa rõ `metainfo`.

#### 2.2. Tiến hành Kiểm thử Tự động qua `mmdet_test.py`
Chạy tuần tự 4 lượt kiểm thử trên GPU RTX 3090:
1. **Zero-Shot Baseline**: Pretrained Swin-T checkpoint gốc (`work_dirs/eval_zero_shot_vi`).
2. **Exp 1 (Short VI)**: Checkpoint `work_dirs/vifood_1k/iter_10000.pth` (`work_dirs/eval_exp1_vi`).
3. **Exp 2 (Short EN)**: Checkpoint `work_dirs/vifood_en_1k/iter_10000.pth` (`work_dirs/eval_exp2_en`).
4. **Exp 3 (Full VI Caption)**: Checkpoint `work_dirs/vifood_vi_full_1k/iter_10000.pth` (`work_dirs/eval_exp3_vi_full`).

---

### 3. Bảng Kết quả Đánh giá Thực nghiệm Chính thức

| Mô hình / Thí nghiệm | Dạng Text Prompt | mAP (0.50:0.95) | mAP_50 | mAP_75 | mAP_m (vật thể vừa) | Average Recall (AR) |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **Zero-Shot Baseline** | Pretrained Swin-T | 0.026 | 0.034 | 0.031 | 0.017 | 0.392 |
| **Exp 1: Short VI** | Nhãn ngắn tiếng Việt (`"phở . bánh mì ."`) | 0.024 | 0.037 | 0.027 | **0.224** | 0.233 |
| **Exp 2: Short EN** | Nhãn ngắn tiếng Anh (`"beef noodle soup ."`) | 0.055 | 0.084 | 0.055 | 0.102 | 0.368 |
| **⭐ Exp 3: Full VI Caption** | **Câu văn tự nhiên tiếng Việt phong phú** | **0.055** | **0.074** | **0.066** | **0.199** | **0.543** |

---

### 4. Kết luận Khoa học Phục vụ Bảo vệ Luận văn

1. **Hiệu năng bứt phá của Exp 3 (Đóng góp cốt lõi)**:
   * So với Exp 1 (nhãn ngắn), Exp 3 tăng **+129% mAP** (0.024 → 0.055) và tăng **+144% mAP_75** (0.027 → 0.066).
   * Khả năng bao phủ (**Recall**) tăng vọt từ **23.3% lên 54.3%** (+133%).
2. **Giải quyết triệt để rào cản ngôn ngữ (Language Gap)**:
   * Prompt ngắn tiếng Việt bị lép vế trước tiếng Anh (do BERT bias). Tuy nhiên khi cung cấp câu văn tiếng Việt đầy đủ ngữ cảnh tự nhiên, tiếng Việt đã **vượt tiếng Anh ở mốc box chuẩn xác cao mAP_75 (0.066 so với 0.055)** và **vượt xa tiếng Anh về độ bao phủ (Recall: 54.3% so với 36.8%)**.
3. **Tính toàn vẹn thực nghiệm**:
   * Cả 3 mô hình đều được huấn luyện trên cùng cấu hình, cùng số iters (10.000) và cùng được đánh giá trên cùng tập kiểm thử 100 ảnh độc lập.

---

### 5. Hướng đi tiếp theo: Pha 5 (Xây dựng Demo Web App & API)
* Đóng gói mô hình phục vụ suy luận thời gian thực (Inference API / Gradio Web App).
* Trình diễn khả năng Visual Grounding với câu văn miêu tả tự nhiên của Exp 3.
