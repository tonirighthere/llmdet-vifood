# NHẬT KÝ PHIÊN LÀM VIỆC: 30–31/10/2026
## Chủ đề: Nhãn đã sửa (crops_review) → taxonomy v2 → build lại Pha 0, Pha 2 → train lại B1

---

### 1. Nhãn mới
Người dùng sửa nhãn trên web app `crops_review/` (http://localhost:7860), xuất `crops_review/exports/*_corrected.zip`
và chép đè vào `zip/vifood.zip`, `zip/vifood2999.zip` (md5 trùng nhau, đã kiểm tra).

Audit log `crops_review/crops.db`: 182 box đổi lớp, 46 box xóa. Hay gặp nhất: `rau luộc→rau sống` 16,
`bánh bèo→bánh khọt` 12, `món ăn khác→bánh bèo` 11, `món ăn khác→chả giò` 9, `canh→món ăn khác` 8.

Box bị xóa được ghi thành dòng `# DELETED <cls> ...` trong file YOLO. Đã sửa `build_vifood54.py` để bỏ qua dòng
bắt đầu bằng `#` (trước đó sẽ lỗi `int('#')`).

### 2. Taxonomy v2 (`scripts/vifood54/taxonomy.json`, nguồn sự thật duy nhất)
Mỗi trường đều có bước pipeline dùng tới (mô tả trong `schema` của file):

| Trường | Dùng ở đâu |
| :--- | :--- |
| `id`, `name` | id = thứ tự obj.names; `name` là prompt nguyên văn cho BERT |
| `en` | báo cáo, so sánh zero-shot |
| `aliases` | app (truy vấn người dùng), prompt OV. **Không** vào prompt train (giữ công thức B1) |
| `group` | dish / side / sauce / catch_all; catch_all không có thuộc tính hình thái |
| `supercategory` (11 nhóm) | AP theo nhóm, phân tầng split OV |
| `visual.definition` | 1 câu chỉ mô tả cái nhìn thấy: caption vùng, prompt LMM (Pha 5), bảng luận văn |
| `visual.units / multi_units / attrs` | bộ sinh caption (trước nằm ở `captions/visual_bank.json`, đã gộp và xóa file đó) |
| `confusable_with` (33 cặp, 2 chiều) | lớp dễ nhầm + dấu hiệu nhìn thấy của lớp này; dùng làm negative khó cho VG (Pha 3), cặp theo dõi khi đánh giá |
| `ov_split` | 8 lớp novel tạm chọn (cao lầu, bánh pía, ốc, quẩy, súp cua, cơm tấm, nem chua, bánh giò), chốt sau B1-v2 |
| `nutrition_key` | khóa trong `nutrition_vifood_51.json`; null với nem rán, món tráng miệng, quẩy (cần bổ sung) |
| `label_notes` | thực tế nhãn khác tên gọi (chả giò = giò lụa, heo quay gồm sườn nướng...) |

Bản `grounding_data/vifood54/annotations/taxonomy.json` do build xuất thêm `stats` (ảnh/box mỗi split).
`build_vifood54.py` kiểm tra schema (`validate_taxonomy`); test mới `test_definitions_and_cues_pass_lint`
đảm bảo định nghĩa không chứa tên lớp khác và cả định nghĩa lẫn dấu hiệu phân biệt đều không có từ hương vị (16/16 test đạt).
Dữ liệu ảnh xem lại khi soạn: `bánh đúc` chủ yếu là bánh đúc lá dứa xanh cắt hình thoi (sửa thuộc tính);
`bánh tráng` gồm cả bánh tráng nướng; `chả giò` vẫn chủ yếu là giò lụa, có lẫn vài ảnh cuốn chiên.

### 3. Build lại
- **Giữ split cũ** (`--keep-split`, mặc định đọc `split_manifest.json` trước khi ghi đè): 3956/3956 ảnh giữ split → không rò rỉ,
  so được B1 cũ và mới trên cùng tập ảnh test. Bản cũ lưu ở `grounding_data/vifood54/annotations_v1/`.
- Pha 0: 3956 ảnh, 18 200 box (cũ 18 253); train_rfs 4164 mẫu/epoch (cũ 4142).
  Khác biệt nhãn: train 154 ảnh (163 đổi lớp, 51 xóa), val 13 ảnh (20 / 2), test 19 ảnh (20 / 3).
- Pha 2: caption lỗi lint train 10/18 828, val 8/2 424, test 0/2 484 (đều do quá 160 token).

### 4. Train lại B1
`scripts/vifood54/run_b1_v2.sh` trong tmux `vifood54_b1_v2` (bắt đầu 31/10 00:01, ETA ~3h15):
train → test B1-v2, B1-v1 (checkpoint cũ), B0 trên test mới → `grounding_data/vifood54/EVAL_V2.md`.
Log: `llmdet_vietnamese_food/work_dirs/vifood54_b1_v2_pipeline.log`.

### 5. Kết quả B1-v2 (31/10 03:44, `grounding_data/vifood54/EVAL_V2.md`)
| Mô hình (test mới, 414 ảnh, 1898 box) | mAP | AP50 | AP75 | AR@100 |
| :--- | :---: | :---: | :---: | :---: |
| B0 zero-shot | 0.015 | 0.020 | 0.016 | 0.368 |
| B1-v1 (nhãn cũ) | 0.315 | 0.394 | 0.355 | 0.809 |
| B1-v2 (nhãn mới) | 0.315 | 0.394 | 0.357 | 0.808 |

- Val tốt nhất: v2 0.348 vs v1 0.347; đường cong gần như trùng.
- Sửa ~1% box không đổi được mAP tổng: nhiễu nhãn không phải nút thắt. B1-v1 tăng từ 0.310 (test cũ) lên 0.315 chỉ nhờ nhãn test sạch hơn.
- Theo lớp có lên có xuống (bún thịt nướng +0.06, quẩy +0.08, gà quay +0.05, cơm tấm +0.08; rau xào −0.05, bún bò Huế −0.05, cháo lòng −0.05) nhưng các lớp này chỉ 9–30 box test, nằm trong dao động ngẫu nhiên.
- Lỗi chính không đổi: món giống nhau (bánh chưng→bánh tét 34%, ngao sò→ốc 47%, xôi→cơm chiên 36%, nem chua→gỏi cuốn 26%), lớp yếu (thịt bò, lẩu, mực, gỏi, cua, canh < 0.06).
- Quyết định: dùng B1-v2 làm mốc cho B3; B3 nhắm đúng lỗi món giống nhau bằng caption hình thái + negative khó từ `confusable_with`.
