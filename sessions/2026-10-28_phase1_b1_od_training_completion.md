# NHẬT KÝ PHIÊN LÀM VIỆC: 28/10/2026
## Chủ đề: Hoàn tất Huấn luyện Pha 1 — Baseline B1 (OD mode có negative sampling)

---

### 1. Thông tin chung
* **Thời gian hoàn thành**: 03:13:00 ngày 28/10/2026.
* **Thời gian huấn luyện**: ~3 giờ 33 phút (bắt đầu 23:40:37 ngày 27/10/2026).
* **Mục tiêu**: Huấn luyện mô hình Grounding DINO Swin-T trên ViFood-54 (54 class) ở **OD mode** với negative sampling (prompt gồm lớp dương + lớp âm lấy mẫu ngẫu nhiên từ label map 54 class), Repeat Factor Sampling (RFS) và Class Dropout cho lớp đầu (`đồ chấm`, `rau sống`).
* **Cấu hình phần cứng**: NVIDIA RTX 3090 (24GB VRAM), PyTorch + MMDetection 3.3.0, FP16 AMP. Tốc độ trung bình: ~0.67s / iteration, bộ nhớ VRAM sử dụng ~5.1 GB.
* **Config huấn luyện**: [`llmdet_vietnamese_food/configs/grounding_dino_swin_t_vifood54_b1_od.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/configs/grounding_dino_swin_t_vifood54_b1_od.py).
* **Thư mục lưu trữ**: [`llmdet_vietnamese_food/work_dirs/vifood54_b1_od/`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/work_dirs/vifood54_b1_od/).

---

### 2. Checkpoints lưu trữ
1. **`best_coco_bbox_mAP_iter_16000.pth`** (674 MB) — **[Checkpoint tốt nhất dùng để Test / Suy luận]**:
   * Đạt val `bbox_mAP`: **0.3470** tại iter 16,000.
   * File đã được strip optimizer state, chỉ lưu model weights.
2. **`iter_16000.pth`** (1.8 GB) — Checkpoint đầy đủ cuối cùng (chứa cả weights, optimizer AdamW, learning rate scheduler state để resume nếu cần).
3. **`last_checkpoint`** — Trỏ tới `iter_16000.pth`.
4. *(Các snapshot trung gian: `iter_12000.pth`, `iter_14000.pth` có thể xóa để tiết kiệm 3.6 GB).*

---

### 3. Động lực học Hàm mất mát (Training Loss Convergence)

| Mốc Iteration | Tổng Loss | Loss Class (`loss_cls`) | Loss Box L1 (`loss_bbox`) | Loss GIoU (`loss_iou`) | Text Enc LR | Model Base LR | Ghi chú |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **50** | 41.8428 | 2.7229 | 0.4328 | 0.2878 | 4.95e-06 | 3.96e-05 | Khởi động Warmup |
| **100** | 41.3336 | 2.7671 | 0.3680 | 0.2729 | 9.96e-06 | 7.97e-05 | Warmup tiếp tục |
| **200** | 36.7195 | 2.4063 | 0.3336 | 0.2533 | 2.00e-05 | 1.60e-04 | Gần đạt LR định mức |
| **500** | 32.3481 | 2.0824 | 0.3246 | 0.2578 | 5.00e-05 | 4.00e-04 | Hết Warmup, bắt đầu ổn định |
| **1,000** | 27.7294 | 1.6773 | 0.3523 | 0.2537 | 5.00e-05 | 4.00e-04 | Loss class giảm sâu |
| **2,000** | 25.9161 | 1.5882 | 0.2877 | 0.2178 | 5.00e-05 | 4.00e-04 | Val Checkpoint 1 (mAP 0.082) |
| **4,000** | 24.2130 | 1.4317 | 0.3178 | 0.2361 | 5.00e-05 | 4.00e-04 | Val Checkpoint 2 (mAP 0.172) |
| **6,000** | 20.9808 | 1.1678 | 0.3089 | 0.2352 | 5.00e-05 | 4.00e-04 | Val Checkpoint 3 (mAP 0.226) |
| **8,000** | 21.7597 | 1.1983 | 0.3455 | 0.2447 | 5.00e-05 | 4.00e-04 | Val Checkpoint 4 (mAP 0.274) |
| **10,000** | 20.3588 | 1.2235 | 0.2839 | 0.2148 | 5.00e-05 | 4.00e-04 | Val Checkpoint 5 (mAP 0.315) |
| **12,000** | 17.6703 | 0.9504 | 0.2768 | 0.2286 | 5.00e-05 | 4.00e-04 | Val Checkpoint 6 (mAP 0.338) |
| **14,000** | 18.3875 | 0.9676 | 0.3221 | 0.2220 | 5.00e-06 | 4.00e-05 | Decay LR lần 1 mốc 13k |
| **16,000** | **18.1603** | **1.0394** | **0.2752** | **0.2254** | **5.00e-07** | **4.00e-06** | **Decay LR lần 2, mAP Best 0.347** |

---

### 4. Tiến trình Đánh giá Validation (Val Metrics qua từng chu kỳ 2,000 iters)
Đánh giá trên tập `val` (404 ảnh ViFood-54, prompt chứa đầy đủ 54 class):

| Checkpoint | mAP (0.50:0.95) | mAP@50 | mAP@75 | mAP (Small) | mAP (Medium) | mAP (Large) | Ghi chú |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Iter 2,000** | 0.082 | 0.103 | 0.091 | 0.195 | 0.169 | 0.083 | Bắt đầu nhận diện được món |
| **Iter 4,000** | 0.172 | 0.217 | 0.188 | 0.344 | 0.215 | 0.176 | Vượt mốc Cổng quyết định (0.15) |
| **Iter 6,000** | 0.226 | 0.279 | 0.246 | 0.369 | 0.248 | 0.232 | Tăng đều đặn |
| **Iter 8,000** | 0.274 | 0.338 | 0.305 | 0.348 | 0.281 | 0.281 | |
| **Iter 10,000** | 0.315 | 0.387 | 0.350 | 0.344 | 0.307 | 0.322 | Vượt mốc 0.30 mAP |
| **Iter 12,000** | 0.338 | 0.416 | 0.378 | 0.333 | 0.324 | 0.347 | Chuẩn bị decay LR |
| **Iter 14,000** | 0.342 | 0.421 | 0.382 | 0.330 | 0.326 | 0.350 | Tinh chỉnh sau decay |
| **Iter 16,000** | **0.3470** | **0.4260** | **0.3880** | **0.3260** | **0.3230** | **0.3570** | **Best Checkpoint** |

* **Average Recall (AR) tại Iter 16,000**:
  * AR @ maxDets=100: **0.824**
  * AR @ maxDets=300 / 1000: **0.824**
  * AR (Small): **0.667**
  * AR (Medium): **0.709**
  * AR (Large): **0.830**

---

### 5. Bảng Điểm AP Chi Tiết Theo 54 Lớp (Validation tại Iter 16,000)

| STT | Tên lớp món ăn | mAP (0.50:0.95) | mAP_50 | mAP_75 | mAP_m | mAP_l | Đánh giá sơ bộ |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| 1 | **bánh pía** | **0.812** | 0.971 | 0.909 | 1.000 | 0.811 | Nhận diện xuất sắc |
| 2 | **bánh mì** | **0.800** | 0.864 | 0.864 | - | 0.800 | Rất cao, đặc trưng rõ |
| 3 | **cơm chiên** | **0.765** | 0.829 | 0.829 | - | 0.771 | Tốt |
| 4 | **bánh tét** | **0.695** | 0.896 | 0.783 | 0.000 | 0.710 | Rất cao |
| 5 | **bánh khọt** | **0.674** | 0.785 | 0.743 | 0.796 | 0.680 | Rất tốt |
| 6 | **đồ chấm** | **0.659** | 0.832 | 0.691 | 0.644 | 0.688 | Class drop phát huy hiệu quả |
| 7 | **cháo lòng** | **0.640** | 0.837 | 0.784 | - | 0.640 | Tốt |
| 8 | **bún đậu mắm tôm**| **0.622** | 0.819 | 0.782 | - | 0.622 | Tốt |
| 9 | **rau sống** | **0.618** | 0.743 | 0.664 | 0.368 | 0.644 | Class drop phát huy hiệu quả |
| 10 | **bánh chưng** | **0.597** | 0.703 | 0.601 | - | 0.597 | Khá cao |
| 11 | **bánh bèo** | **0.593** | 0.905 | 0.680 | 0.636 | 0.602 | Cao |
| 12 | **bánh xèo** | **0.583** | 0.704 | 0.640 | - | 0.584 | Cao |
| 13 | **nem rán** | **0.578** | 0.638 | 0.638 | 0.425 | 0.598 | RFS x1.59 hoạt động tốt |
| 14 | **gỏi cuốn** | **0.571** | 0.765 | 0.639 | - | 0.571 | Tốt |
| 15 | **bún tươi** | **0.567** | 0.638 | 0.638 | 0.449 | 0.631 | Tốt |
| 16 | **bánh đúc** | **0.505** | 0.586 | 0.586 | - | 0.505 | Khá |
| 17 | **bánh căn** | **0.503** | 0.552 | 0.534 | 0.102 | 0.623 | Khá |
| 18 | **hàu** | **0.407** | 0.512 | 0.472 | 0.147 | 0.441 | |
| 19 | **bánh bột lọc** | **0.407** | 0.621 | 0.415 | - | 0.408 | |
| 20 | **mì Quảng** | **0.404** | 0.517 | 0.502 | 0.556 | 0.410 | |
| 21 | **gà quay** | **0.399** | 0.433 | 0.428 | - | 0.400 | Không bị quẩy đè nhiều |
| 22 | **súp cua** | **0.394** | 0.533 | 0.420 | 0.530 | 0.400 | |
| 23 | **bánh cuốn** | **0.391** | 0.463 | 0.436 | 0.129 | 0.413 | |
| 24 | **cơm tấm** | **0.377** | 0.498 | 0.461 | - | 0.377 | |
| 25 | **xôi** | **0.367** | 0.418 | 0.397 | 0.159 | 0.398 | |
| 26 | **cá chiên** | **0.335** | 0.443 | 0.359 | - | 0.337 | |
| 27 | **nem chua** | **0.316** | 0.489 | 0.327 | 0.504 | 0.315 | |
| 28 | **ốc** | **0.310** | 0.358 | 0.327 | 0.042 | 0.339 | |
| 29 | **bánh tráng** | **0.308** | 0.380 | 0.377 | 0.682 | 0.261 | |
| 30 | **bún bò Huế** | **0.301** | 0.370 | 0.370 | 0.000 | 0.322 | Cần phân tích nhầm món nước |
| 31 | **bánh giò** | **0.293** | 0.391 | 0.391 | 0.027 | 0.313 | |
| 32 | **bún riêu** | **0.293** | 0.315 | 0.315 | - | 0.293 | |
| 33 | **cua** | **0.279** | 0.325 | 0.325 | 0.404 | 0.295 | |
| 34 | **rau luộc** | **0.219** | 0.232 | 0.232 | 0.632 | 0.176 | |
| 35 | **tôm** | **0.200** | 0.245 | 0.223 | 0.132 | 0.221 | |
| 36 | **món ăn khác** | **0.198** | 0.271 | 0.238 | 0.126 | 0.208 | |
| 37 | **rau xào** | **0.196** | 0.214 | 0.206 | - | 0.202 | |
| 38 | **heo quay** | **0.174** | 0.195 | 0.184 | - | 0.178 | |
| 39 | **phở** | **0.167** | 0.235 | 0.183 | - | 0.169 | Món nước hay nhầm nhau |
| 40 | **gỏi** | **0.163** | 0.169 | 0.169 | - | 0.167 | |
| 41 | **bún mắm** | **0.147** | 0.196 | 0.158 | - | 0.148 | RFS x1.79 vẫn hơi thấp |
| 42 | **cao lầu** | **0.133** | 0.177 | 0.151 | 0.165 | 0.137 | |
| 43 | **quẩy** | **0.115** | 0.144 | 0.123 | - | 0.118 | Cần check nhầm gà quay |
| 44 | **bún thịt nướng** | **0.109** | 0.134 | 0.124 | - | 0.110 | |
| 45 | **canh** | **0.099** | 0.110 | 0.110 | 0.053 | 0.111 | Nhầm với các món nước |
| 46 | **bánh canh** | **0.099** | 0.116 | 0.116 | - | 0.108 | Nhầm bún / phở |
| 47 | **hủ tiếu** | **0.087** | 0.105 | 0.105 | - | 0.089 | Nhầm bún / phở |
| 48 | **món tráng miệng**| **0.086** | 0.095 | 0.095 | - | 0.098 | Đa dạng thị giác |
| 49 | **chả giò** | **0.080** | 0.091 | 0.088 | 0.025 | 0.093 | **Nghi nhầm sang nem rán** |
| 50 | **ngao sò** | **0.058** | 0.069 | 0.068 | - | 0.060 | |
| 51 | **gà luộc** | **0.034** | 0.047 | 0.034 | - | 0.035 | |
| 52 | **thịt bò** | **0.021** | 0.027 | 0.024 | - | 0.022 | Thành phần trong tô |
| 53 | **mực** | **0.018** | 0.025 | 0.016 | - | 0.020 | |
| 54 | **lẩu** | **0.000** | 0.000 | 0.000 | 0.000 | 0.000 | Rất ít mẫu, cấu trúc phức tạp |

---

### 6. Phân tích Sơ bộ & Ý nghĩa Kết quả cho Luận văn / Báo cáo
1. **Xác nhận Giả thuyết Cốt lõi**:
   * Trước B1: Các phiên huấn luyện cũ (Exp1–Exp4) chạy ở Visual Grounding (VG) mode không có negative sampling, dẫn đến prompt test 54 lớp bị dương tính giả hàng loạt (`mAP ~ 0.05`).
   * Với B1: Khi chuyển sang **OD mode** với negative sampling động (1.7 positive / 38 negative mỗi prompt), `mAP` val tăng vọt lên **0.3470** (~**gấp 7 lần** Exp4 cũ và gấp 23 lần B0 zero-shot 0.015).
   * **Kết luận**: Khẳng định vai trò quyết định của việc căn chỉnh phân phối prompt huấn luyện và kiểm thử đối với mô hình Open-Vocabulary Object Detection (Grounding DINO).

2. **Hiệu quả của Cân bằng Dữ liệu (RFS & Class Dropout)**:
   * **Class Dropout** cho `đồ chấm` (drop p=0.77) và `rau sống` (drop p=0.694): Mô hình không bị thiên lệch (bias) dự đoán áp đảo vào hai lớp xuất hiện liên tục này. Cả hai lớp vẫn đạt điểm AP cao (`0.659` và `0.618`) trong khi các lớp chính khác không bị triệt tiêu.
   * **Nem rán** được hưởng lợi từ RFS (x1.59) đạt AP `0.578`. Tuy nhiên, `chả giò` chỉ đạt `0.080`, cho thấy khả năng cao mô hình đang gom chung các thể loại nem/chả giò vào `nem rán`.

3. **Hiện tượng Tokenizer & Chữ có dấu**:
   * `quẩy` đạt `0.115` và `gà quay` đạt `0.399`. Cần phân tích ma trận nhầm lẫn ở bước Test để xem có hiện tượng dự đoán `quẩy` vào `gà quay` (do BERT tách thành token `quay`) hay không.
   * Cụm các món nước (`phở`, `hủ tiếu`, `bánh canh`, `canh`, `bún mắm`) đều có AP thấp (< 0.20), phản ánh khó khăn trong việc phân biệt các món nước chứa nhiều thành phần chồng lấp.

---

### 7. Bước tiếp theo
Chạy kiểm thử trên tập `test` (414 ảnh) và xuất file dự đoán `.pkl` để vẽ ma trận nhầm lẫn:
```bash
cd llmdet_vietnamese_food
python mmdet_test.py configs/grounding_dino_swin_t_vifood54_b1_od.py \
    work_dirs/vifood54_b1_od/best_coco_bbox_mAP_iter_16000.pth \
    --work-dir work_dirs/vifood54_b1_od_test \
    --out work_dirs/vifood54_b1_od_test/preds.pkl
```

---

### 8. Kết quả TEST (414 ảnh, 1901 box) — đã chạy 28/10 tối
Lệnh ở mục 7 đã chạy; phân tích bằng `scripts/vifood54/analyze_eval.py` → `grounding_data/vifood54/EVAL_B0_B1.md`.

| Mô hình | mAP | AP50 | AP75 | AR@100 |
| :--- | :---: | :---: | :---: | :---: |
| B0 zero-shot | 0.015 | 0.019 | 0.016 | 0.367 |
| **B1 OD + negative** | **0.310** | **0.388** | **0.349** | **0.806** |

**Cổng quyết định Pha 1: ĐẠT** (≥ 0.15). Test thấp hơn val (0.347) ~0.04, trong mức bình thường.

### 9. Phân tích lỗi trên test
1. **Tên bị BERT làm dính chữ KHÔNG phải nguồn lỗi chính.** Ở score ≥ 0.3: 0 box nhầm giữa `quẩy`↔`gà quay`/`heo quay`, `lẩu`↔`cao lầu`, `bánh căn`↔`bánh canh`, `canh`↔`bánh canh`, `cua`↔`súp cua`, `tôm`↔`bún đậu mắm tôm`, `cá chiên`↔`cơm chiên`, `mực`↔`ốc`. Chỉ có vài box score thấp (< 0.1) `heo quay`→`quẩy` (4). → **Quyết định: giữ nguyên tên tiếng Việt, không thêm tên tiếng Anh.**
2. **Lỗi chính là nhầm món giống nhau về hình** (score ≥ 0.3): `bánh chưng`→`bánh tét` 34%, `xôi`→`cơm chiên` 37%, `ngao sò`→`ốc` 47%, `nem chua`→`gỏi cuốn` 21%, `bún riêu`↔`bún bò Huế` ~20%, `cao lầu`→`mì Quảng`, `gà quay`→`cá chiên` 25%. → đúng loại lỗi mà caption hình thái có thuộc tính phân biệt (vuông/trụ, vỏ/không vỏ, màu nước dùng...) nhắm tới — động lực cho B3.
3. **Lớp yếu do score thấp, không phải không thấy**: ở score ≥ 0.1 phần lớn GT "bỏ sót" ở 0.3 đã có box (nhưng hay sai lớp): `chả giò` (AP 0.10, nhầm `bánh tráng`, `heo quay`), `tôm`, `mực`, `heo quay`, `thịt bò`, `lẩu`, `gà luộc`.
4. **`chả giò` thấp bất thường** (133 ảnh train nhưng AP 0.10, kém `nem rán` 0.27 với 62 ảnh). Không nhầm sang `nem rán`; hay bị đoán thành `bánh tráng`. Nên kiểm tra tay nhãn `chả giò` (ảnh lẫn nem cuốn bánh tráng, chả giò cắt khúc trong đĩa bún...).
5. **Lịch train**: val tăng đều tới khi giảm LR ở 12k (0.338 → 0.347 ở 16k), chưa bão hòa trước khi giảm LR → **giữ 16k iter** cho B3 để so sánh công bằng; không rút ngắn được mà không đổi kết quả.
6. Bootstrap CI chưa chạy (B1 vs B0 chênh quá lớn, không cần); sẽ chạy khi so B3 với B1.
