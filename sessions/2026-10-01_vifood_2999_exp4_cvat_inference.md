# Nhật Ký Thực Nghiệm: Suy Luận Nhãn Tự Động Với Mô Hình Exp 4 Cho Dataset ViFood 2.999 Ảnh & Đóng Gói CVAT

**Ngày thực hiện:** 01/10/2026  
**Mục tiêu:** Sử dụng mô hình tối ưu nhất **Experiment 4: Multi-Prompt & High-Res 800** (`work_dirs/vifood_multi_res800/iter_10000.pth`) để suy luận bounding box và nhãn 51 lớp món ăn Việt Nam cho tập dữ liệu 2.999 ảnh (`vifood_2999.zip`), sau đó đóng gói chuẩn các định dạng để upload trực tiếp lên công cụ gán nhãn CVAT.

---

## 1. Cấu Hình Thực Nghiệm & Pipeline

- **Dataset đầu vào:** [`vifood_2999.zip`](file:///home/atin/tuan/SoPSoP/vifood_2999.zip) (2.999 ảnh món ăn Việt Nam).
- **Mô hình suy luận:** Grounding DINO Swin-T Multi-Prompt & High-Res 800 (Trọng số `work_dirs/vifood_multi_res800/iter_10000.pth`).
- **Prompt:** Toàn bộ 51 lớp món ăn Việt Nam được phân tách theo chuẩn Grounding DINO:
  `bánh bèo . bánh bột lọc . bánh canh . bánh chưng . bánh cuốn . bánh căn . bánh giò . bánh khọt . bánh mì . bánh pía . bánh tráng . bánh tét . bánh xèo . bánh đúc . bún bò Huế . bún . bún mắm . bún riêu . bún thịt nướng . bún đậu mắm tôm . canh chua . cao lầu . cháo lòng . chả . cua . cá chiên . cơm chiên . cơm tấm . gà luộc . gỏi . gỏi cuốn . heo quay . hàu . hủ tiếu . lẩu . mì Quảng . mực . nem chua . ngao sò . phở . rau sống . súp cua . thịt bò . rau luộc . tôm . xôi xéo . ốc . món ăn khác . rau xào . nước chấm . gà quay .`
- **Cơ chế lọc nhãn & Post-processing:**
  - Ngưỡng Confidence: $0.25$ (Đã tinh chỉnh tăng từ $0.22 \rightarrow 0.25$ để tối ưu độ chuẩn xác, loại bỏ các box nhiễu/hallucination).
  - Cross-class NMS ($IoU = 0.60$): Khử triệt để hiện tượng trùng lặp bounding box giữa nhiều nhãn khác nhau trên cùng một đĩa thức ăn.
- **Phần cứng thực thi:** NVIDIA GeForce RTX 3090 (24 GB VRAM).
- **Tốc độ suy luận:** ~4.8 - 5.7 ảnh/giây.

---

## 2. Thống Kê Định Lượng Kết Quả Gán Nhãn (Ngưỡng Conf = 0.25)

- **Tổng số ảnh xử lý:** 2.999 / 2.999 ảnh (100%).
- **Tổng số bounding box phát hiện:** **16.378 bounding boxes** (giảm từ 27.428 ở conf 0.22, loại bỏ 40.3% box không chắc chắn).
- **Trung bình box/ảnh:** **5.46 boxes/ảnh**.
- **Số ảnh không phát hiện box (0 box):** 140 ảnh (chiếm 4.7%).
- **Số box nhiều nhất trên 1 bức ảnh:** 32 boxes.

### Phân Bố Top 15 Món Ăn Xuất Hiện Nhiều Nhất (Conf >= 0.25):
1. **bún đậu mắm tôm**: 3.866 boxes (23.6%)
2. **nước chấm**: 2.435 boxes (14.9%)
3. **rau sống**: 2.265 boxes (13.8%)
4. **bánh khọt**: 1.379 boxes (8.4%)
5. **bánh tét**: 1.269 boxes (7.7%)
6. **bánh bột lọc**: 845 boxes (5.2%)
7. **cao lầu**: 602 boxes (3.7%)
8. **rau luộc**: 560 boxes (3.4%)
9. **xôi xéo**: 327 boxes (2.0%)
10. **ốc**: 220 boxes (1.3%)
11. **tôm**: 213 boxes (1.3%)
12. **gỏi**: 203 boxes (1.2%)
13. **lẩu**: 177 boxes (1.1%)
14. **cháo lòng**: 160 boxes (1.0%)
15. **rau xào**: 157 boxes (1.0%)

---

## 3. Các Gói Dữ Liệu Nhãn Xuất Xưởng Phục Vụ CVAT (Phiên Bản Conf = 0.25)

Đã tạo sẵn 3 file ZIP chuẩn hóa ở thư mục gốc workspace:

1. **[`vifood_2999_labels_cvat.zip`](file:///home/atin/tuan/SoPSoP/vifood_2999_labels_cvat.zip)** (0.78 MB) - **KHUYẾN NGHỊ SỐ 1 CHO CVAT**:
   - Định dạng: **YOLO 1.1 / Darknet** (Tương thích 100% với chuẩn cấu trúc của `vifood2.zip`).
   - Cấu trúc bên trong file zip:
     ```
     ├── obj.names                     # Danh sách 51 tên class tiếng Việt
     ├── obj.data                      # Khai báo cấu hình classes = 51
     ├── train.txt                     # 2.999 dòng trỏ tới data/obj_train_data/<img_name>
     └── obj_train_data/               # 2.999 file .txt chứa tọa độ YOLO chuẩn hóa
     ```
   - **Cách upload lên CVAT:**
     - Trong Task của CVAT, chọn **Actions** $\rightarrow$ **Upload annotations**.
     - Chọn định dạng: **YOLO 1.1**.
     - Chọn file [`vifood_2999_labels_cvat.zip`](file:///home/atin/tuan/SoPSoP/vifood_2999_labels_cvat.zip).

2. **[`vifood_2999_cvat_xml.zip`](file:///home/atin/tuan/SoPSoP/vifood_2999_cvat_xml.zip)** (0.34 MB):
   - Định dạng: **CVAT for images 1.1** (Định dạng XML native của CVAT).
   - Chứa file `annotations.xml` đầy đủ thuộc tính bounding box, tọa độ `xtl, ytl, xbr, ybr` và `score`.
   - **Cách upload lên CVAT:**
     - Chọn **Upload annotations** $\rightarrow$ định dạng: **CVAT 1.1**.

3. **[`vifood_2999_cvat_coco.zip`](file:///home/atin/tuan/SoPSoP/vifood_2999_cvat_coco.zip)** (0.53 MB):
   - Định dạng: **COCO 1.0** (Chứa file `instances_default.json`).
   - Tương thích upload vào CVAT dưới dạng format **COCO 1.0**.

---

## 4. Script Tái Lập (Reproducibility)

Script điều phối toàn bộ quá trình đã được lưu tại:
[`scripts/infer_vifood_2999_exp4_cvat.py`](file:///home/atin/tuan/SoPSoP/scripts/infer_vifood_2999_exp4_cvat.py).
Mọi kết quả suy luận thô và tọa độ từng box được lưu trong cache persistent:
[`work_dirs/vifood_2999_cvat/detections_cache.jsonl`](file:///home/atin/tuan/SoPSoP/work_dirs/vifood_2999_cvat/detections_cache.jsonl).
