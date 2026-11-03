# NHẬT KÝ PHIÊN LÀM VIỆC: 01/11/2026
## Chủ đề: Thí nghiệm open-vocabulary (base / novel)

---

### 1. Giao thức
- Novel = 8 lớp `ov_split: novel` trong taxonomy: bánh giò, bánh pía, cao lầu, cơm tấm, nem chua, súp cua, ốc, quẩy
  (B0 gần 0 ở cả 8 lớp; B1-v2 trải 0.17–0.72 → có lớp dễ và khó). Base = 46 lớp còn lại.
- Train: giữ ảnh, bỏ **box + tên** lớp novel khỏi mọi giám sát (prompt OD, negative OD/VG, caption VG). 271 ảnh chỉ có
  box novel không còn box → FilterAnnotations bỏ qua khi load (không dùng làm ảnh nền).
- Chọn checkpoint trên val **chỉ lớp base** (`instances_val_base.json`, prompt 46 tên) → thông tin novel không rò vào việc chọn.
- Test: prompt đủ 54 tên (generalized OV: lớp novel phải thắng cả lớp base trong prompt) → AP_base, AP_novel.
- Công thức như B3b: giai đoạn 1 OD 16k iter (lớp base) → giai đoạn 2 fine-tune OD + VG 8k iter, lr 2e-5.
  Đánh giá cả 2 giai đoạn để thấy caption có giúp món chưa thấy không.

### 2. Code
| File | Nội dung |
| :--- | :--- |
| `scripts/vifood54/make_ov_split.py` | → `grounding_data/vifood54/annotations_ov/`: train_od(_rfs) bỏ box novel, RFS + class_drop tính lại, `label_map_base.json`, `taxonomy_base.json` (confusable bỏ novel), caption VG sinh lại, `instances_val_base.json`, `ov_classes.json`; kiểm tra rò rỉ theo ranh giới từ (`ốc` ≠ `ruốc`) |
| `configs/grounding_dino_swin_t_vifood54_ov_s1_od.py`, `..._ov_s2_od_vg.py` | 2 giai đoạn; val base, test 54 lớp |
| `scripts/vifood54/eval_ov.py` | AP tất cả / AP_base / AP_novel + AP từng lớp novel (COCOeval với catIds con) |
| `scripts/vifood54/run_ov.sh` | train 2 giai đoạn (chịu được dừng sớm do lỗi CIFS) → test → `EVAL_OV.md` |

Kiểm tra: bỏ 1483 box novel; OD rfs 3957 mẫu; VG 2867 ảnh / 3686 mẫu rfs; 0 tên novel trong caption và trong 300 prompt
lấy mẫu sau pipeline; val 46 lớp, test 54 lớp.

### 3. Mốc so sánh (test, prompt 54 lớp)
| Mô hình | mAP (54) | AP_base | AP_novel | AP50_novel |
| :--- | :---: | :---: | :---: | :---: |
| B0 (zero-shot) | 0.015 | 0.016 | 0.010 | 0.014 |
| B1-v2* (đã thấy novel) | 0.315 | 0.299 | 0.407 | 0.516 |
| B3b* (đã thấy novel) | 0.323 | 0.307 | 0.419 | 0.540 |

### 4. Chạy
tmux `vifood54_ov`, bắt đầu 01/11 19:53 (giai đoạn 1 ETA ~2h53, giai đoạn 2 ~1h35, test + đánh giá ~10 phút).
Log: `llmdet_vietnamese_food/work_dirs/vifood54_ov_pipeline.log`.

### 5. Kết quả (02/11, `EVAL_OV.md`, `EVAL_OV_PROMPTS.md`)
Train xong không lỗi. Val (base): giai đoạn 1 tốt nhất 0.368, giai đoạn 2 0.281.

Test, prompt đủ 54 lớp; 8 lớp novel được gọi bằng tên Việt (`vi`), tên Anh trong taxonomy (`en`) hoặc tên Việt + cụm
hình thái 2–3 từ (`desc`, vd. `cao lầu sợi vàng`, `quẩy thanh chiên`; rút gọn để prompt ≤ 256 token BERT):

| Mô hình | AP_base | AP_novel vi | AP_novel en | AP_novel desc |
| :--- | :---: | :---: | :---: | :---: |
| B0 (zero-shot) | 0.016 | 0.010 | 0.065 | 0.026 |
| OV giai đoạn 1 (OD, base) | 0.320 | 0.048 | **0.082** | 0.021 |
| OV giai đoạn 2 (+ caption) | 0.323 | 0.034 | 0.072 | 0.025 |
| B3b* (đã thấy novel) | 0.307 | 0.419 | — | — |

Nhận xét:
1. Tổng quát sang món chưa thấy **yếu**: tốt nhất 0.082, chỉ ~20% trần trên có giám sát (0.419).
2. AR@100_novel cao (0.75) nhưng AP thấp: model **khoanh được** món mới nhưng **gán tên món base nhìn giống nhất**
   (cao lầu→mì Quảng 11/29, quẩy→nem rán 7/12, súp cua→bánh canh 6/11, nem chua→gỏi cuốn / bánh bột lọc 22/42,
   cơm tấm→bún thịt nướng 7/13). Hiệu chỉnh điểm lớp base sau dự đoán không đổi AP (AP xếp hạng theo từng lớp).
3. **Tên tiếng Anh tốt hơn tên Việt** (0.082 vs 0.048; quẩy 0.217, súp cua 0.208, cao lầu 0.175): BERT tiếng Anh
   (bỏ dấu) không có tri thức về tên món Việt chưa thấy, chỉ tri thức tiếng Anh từ pretrain chuyển được. Fine-tune trên
   base còn tăng chút cho tên Anh (B0 0.065 → 0.082).
4. Cụm hình thái ngắn không giúp (0.021–0.026); caption giai đoạn 2 không giúp OV (vi 0.048→0.034, en 0.082→0.072),
   chỉ nhỉnh ở `desc` (0.021→0.025).
5. Prompt chỉ có 8 tên novel còn tệ hơn (S1 0.028, B3b* 0.229) vì ảnh test có rất nhiều món base bị gán nhầm thành
   tên novel → giữ giao thức generalized 54 tên.

Kết luận cho luận văn: với món Việt, open-vocabulary bị giới hạn bởi bộ mã hóa văn bản tiếng Anh và độ giống hình
giữa món mới với món đã học; muốn thêm món mới vẫn cần dữ liệu có nhãn (vài chục ảnh/lớp đã cho AP 0.2–0.7).
Hướng tiếp (ngoài phạm vi): text encoder đa ngữ / tiếng Việt, hoặc vài ảnh mẫu (few-shot) cho món mới.
