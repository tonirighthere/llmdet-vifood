# NHẬT KÝ PHIÊN LÀM VIỆC: 28/10/2026 (tối)
## Chủ đề: Pha 2 — Bộ sinh caption hình thái cho ViFood-54

---

### 1. Mục tiêu
Sinh caption grounding tiếng Việt **chỉ mô tả cái nhìn thấy** (hình dạng, màu, thành phần lộ ra, dụng cụ,
vị trí, số lượng), không hương vị, không tên món "mồ côi" (không có box), an toàn với BERT bỏ dấu.

### 2. Quan sát dữ liệu trước khi soạn thuộc tính
Montage 7 crop/lớp cho cả 54 lớp (ảnh train). Phát hiện:
- **`chả giò` trong nhãn là giò lụa / chả lụa** (khoanh giò hồng, bọc lá chuối), không phải cuốn chiên;
  cuốn chiên là `nem rán`. Giải thích vì sao B1 không nhầm 2 lớp này. Đã sửa trường `en` trong taxonomy
  (`vietnamese pork roll (giò lụa)` / `fried spring rolls`); **tên lớp giữ nguyên**.
- `heo quay` gồm cả sườn và thịt heo nướng; `thịt bò` thường là lát bò trong tô phở; `bánh tét` có cả nguyên đòn lẫn khoanh cắt.
- Cặp hay nhầm ở B1 có khác biệt nhìn thấy rõ: `bánh chưng` vuông bọc lá dong / `bánh tét` hình trụ, khoanh tròn;
  `ngao sò` vỏ hai mảnh có gân / `ốc` vỏ xoắn có đốm; `xôi` hạt nếp dính khối / `cơm chiên` hạt rời lẫn rau củ.

### 3. Code (`scripts/vifood54/captions/`)
| File | Nội dung |
| :--- | :--- |
| `visual_bank.json` | 52 lớp có `units`, `attrs` (3–5 cụm), `multi_units` (lượng từ khi ≥2 box); 2 lớp catch-all không có thuộc tính |
| `lint.py` | Kiểm tra trên **token BERT đã bỏ dấu**: tên lớp ngoài span, từ hương vị/cảm xúc (ngoài span, cho phép `cà chua`), span khớp, ≤160 token |
| `layout.py` | Vị trí lưới 3×3 từ tâm box, kích thước (lớn ≥20% / nhỏ ≤2% diện tích ảnh), đếm; lật trái↔phải |
| `builder.py` | Ghép L1 (liệt kê có đếm) / L2 (mỗi lớp một câu: vị trí + đếm + lượng từ + tên + 1–2 thuộc tính); offset ghi lúc ghép; tự bớt thuộc tính khi vượt ngân sách |
| `build_captions.py` | 6 biến thể/ảnh (2 L1 + 4 L2), mỗi biến thể có bản lật; xuất jsonl + `CAPTION_REPORT.md` |
| `test_captions.py` | 15 test (của/cua, cạnh/canh, bún tươi + bún riêu, từ hương vị, toàn bộ bank qua lint, span/flip/ngân sách với 1–32 box) — **15/15 đạt** |

Lint đã bắt và buộc sửa các va chạm thật trong bản nháp: `bánh trắng`→`bánh tráng`, `phô mai`→`phở`, `cánh`→`canh`, `thơm`, `rau mùi`.

### 4. Kết quả (`grounding_data/vifood54/CAPTION_REPORT.md`)
| split | ảnh | biến thể bị loại | caption khác nhau/ảnh | token L1 TB/max | token L2 TB/p95/max |
| :--- | :---: | :---: | :---: | :---: | :---: |
| train | 3138 | 13/18 828 | 5.89 | 21 / 92 | 65 / 147 / 160 |
| val | 404 | 12/2 424 | 5.88 | 21 / 91 | 64 / 134 / 160 |
| test | 414 | 0/2 484 | 5.88 | 21 / 73 | 64 / 150 / 160 |

- Biến thể bị loại đều do vượt 160 token (ảnh rất nhiều món); mọi ảnh vẫn còn ≥1 biến thể.
- Đầu ra: `{train,val,test}_vg_cap.jsonl`, `train_vg_cap_rfs.jsonl` (4142 dòng, theo RFS).
  Mỗi dòng: `grounding.variants[]` (caption, regions, flip_caption, flip_regions), `grounding.caption/regions`
  (= biến thể L2 đầu, tương thích loader hiện tại), `conversations`, `region_captions`.

Ví dụ:
> Ở chính giữa có một bát hủ tiếu lớn, lá xanh trên mặt, trứng cút trắng và lát thịt. Ở bên phải có một đĩa tôm, thân cong màu cam đỏ.

### 5. Việc còn lại của Pha 2
- [ ] Duyệt tay 50 caption (30 ví dụ đã có trong báo cáo) — **cần người hiểu món duyệt `visual_bank.json`**.
- Tiếp theo: Pha 3 (loader chọn biến thể ngẫu nhiên + bản lật, negative cho VG mode, trộn OD + VG) rồi chạy B3.
