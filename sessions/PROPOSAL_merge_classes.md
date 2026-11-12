# ĐỀ XUẤT GỘP / SỬA LỚP (mục C9) — CHƯA ÁP DỤNG

Lập 12/11/2026. Quyết định của nhóm: **gộp lớp**, phạm vi chốt sau khi soát nhãn (việc 0.5). File này chỉ là số liệu +
phương án; bộ nhãn 54 lớp và mọi kết quả hiện tại giữ nguyên cho tới khi chốt.

Số liệu: `EVAL_EN.md` (test 414 ảnh), `BUILD_REPORT.md`, `vlm_attrs/train_*.jsonl` (Gemma-12B hỏi trên crop "ảnh có đúng là
món này không"). Cột Gemma chỉ là tín hiệu gợi ý: Gemma không nhận ra nhiều món vùng miền, không phải cứ "không" là nhãn sai.

## 1. Nhóm A — đề xuất làm (ít rủi ro)

| Lớp (tên EN) | ảnh train | box test | AP B1-EN / B3b-EN | Gemma đánh "không đúng món" (crop train) | Nhầm chính ở test (B3b-EN) | Đề xuất | Lý do |
|---|---|---|---|---|---|---|---|
| món tráng miệng (dessert) | 57 | 12 | 0.003 / 0.002 | – | – | GỘP vào `món ăn khác` | Hai lớp gom, không có hình thái chung; AP ≈ 0; tên EN "dessert" không giúp |
| thịt bò (sliced beef) | 53 | 11 | 0.015 / 0.004 | 3/53 | – | BỎ lớp (xóa box) | Chủ yếu là lát bò nằm trong tô phở/bún (box lồng trong box món khác); AP ≈ 0 ở mọi mô hình |
| chả giò (vietnamese pork ham) | 139 | 40 | 0.107 / 0.153 | 139/139 | square rice cake 10% | ĐỔI TÊN hiển thị thành `giò lụa` (không đổi box) | Nhãn thực tế là giò lụa (ghi chú taxonomy); tên gây hiểu nhầm với nem rán; tên EN đã là "vietnamese pork ham" |

Sau nhóm A: 54 → **52 lớp**.

## 2. Nhóm B — cặp giống hình (cân nhắc; đổi bản chất bài toán)

| Lớp (tên EN) | ảnh train | box test | AP B1-EN / B3b-EN | Gemma đánh "không đúng món" (crop train) | Nhầm chính ở test (B3b-EN) | Đề xuất | Lý do |
|---|---|---|---|---|---|---|---|
| bánh chưng (square rice cake) | 55 | 59 | 0.297 / 0.278 | 13/55 | cylindrical rice cake 31% | GỘP với `bánh tét` → "bánh chưng / bánh tét"? | Nhầm 31% → bánh tét; khác nhau chủ yếu ở hình khối khi còn nguyên, cắt lát thì gần như không phân biệt được |
| bánh tét (cylindrical rice cake) | 142 | 68 | 0.669 / 0.690 | 43/142 | square rice cake 13% | (cùng cặp trên) |  |
| ngao sò (clams and scallops) | 57 | 17 | 0.248 / 0.186 | 1/57 | sea snails 53% | GỘP với `ốc` → "ngao sò ốc"? | Nhầm 53% → ốc. Lưu ý `ốc` đang là lớp novel của bộ OV |
| ốc (sea snails) | 85 | 20 | 0.319 / 0.327 | 0/85 | – | (cùng cặp trên) |  |
| mì Quảng (quang noodles) | 176 | 24 | 0.210 / 0.216 | 43/176 | cao lau noodles 38% | GỘP với `cao lầu`? | Nhầm 38% → cao lầu và 21% chiều ngược lại. Lưu ý `cao lầu` đang là lớp novel |
| cao lầu (cao lau noodles) | 109 | 29 | 0.301 / 0.315 | 22/109 | quang noodles 21%; other dish 21% | (cùng cặp trên) |  |

Được: mAP tăng (bỏ được các cặp nhầm lớn nhất). Mất: phân biệt chi tiết — vốn là chỗ caption / LLM được kỳ vọng giúp
(nếu gộp thì không còn chỗ để B5 thể hiện); dinh dưỡng của hai món trong cặp phải lấy trung bình; phải chọn lại 8 lớp novel.
**Khuyến nghị: không gộp nhóm B**, giữ làm nơi đo tác dụng của caption v2.

## 3. Nhóm C — AP thấp nhưng là món thật (không gộp, soát nhãn)

| Lớp (tên EN) | ảnh train | box test | AP B1-EN / B3b-EN | Gemma đánh "không đúng món" (crop train) | Nhầm chính ở test (B3b-EN) | Đề xuất | Lý do |
|---|---|---|---|---|---|---|---|
| mực (squid) | 73 | 22 | 0.034 / 0.029 | 5/73 | – | SOÁT NHÃN | AP ≈ 0.03 dù có 73 ảnh train; test bỏ sót 13/22 → nghi nhãn không nhất quán (mực trong lẩu/món khác lúc khoanh lúc không) |
| bún thịt nướng (grilled pork noodle bowl) | 54 | 9 | 0.038 / 0.027 | 12/54 | – | SOÁT NHÃN + thêm ảnh | Chỉ 9 box test → AP rất nhiễu; 54 ảnh train |
| gà luộc (boiled chicken) | 90 | 11 | 0.087 / 0.079 | 2/90 | – | SOÁT NHÃN | 11 box test; có thể lẫn với `gà quay` / `món ăn khác` |
| canh (clear vegetable soup) | 105 | 14 | 0.213 / 0.270 | 2/105 | dipping sauce 43% | SOÁT NHÃN | 43% bị gọi thành `đồ chấm` (bát canh nhỏ giống chén nước chấm) |
| bánh căn (mini savory pancakes) | 88 | 42 | 0.405 / 0.401 | 42/88 | – | SOÁT NHÃN | Gemma đánh "không" 42/88 crop; test bỏ sót 27/42; giống `bánh khọt` |

## 4. Nếu chốt gộp — việc phải làm (theo thứ tự)

1. `scripts/vifood54/taxonomy.json`: thêm vào `merge_into` (đã được `build_vifood54.py` hỗ trợ), ví dụ
   `{"món tráng miệng": "món ăn khác"}`; xóa mục lớp bị gộp khỏi `classes`; lớp bị bỏ hẳn (`thịt bò`) cần thêm một
   danh sách `drop` trong `build_vifood54.py` (chưa có — khoảng 5 dòng). **Id lớp sẽ đánh lại** → mọi file dưới đây phải sinh lại.
2. `scripts/vifood54/captions/en_names.py`: bỏ khóa của lớp đã gộp trong `PROMPT_EN`, `VISUAL_EN`.
3. `nutrition_vifood54.json`: bỏ / gộp mục tương ứng.
4. Sinh lại dữ liệu: `build_vifood54.py --keep-split` → `build_captions.py` → `make_en_data.py` → `build_captions_en.py`
   → `build_lmm_en.py` → `make_ov_split.py --en`.
5. Sửa tuple `classes` trong các config `*_en.py` (và `base_classes` của bộ OV).
6. **Train lại** B1-EN (≈4 h) → B3b-EN (≈2 h) → mọi run sau đó. Kết quả cũ (54 lớp) giữ làm phụ lục, không so trực tiếp.

Vì bước 6, nên chốt C9 **trước** khi chạy B5 v2 / OV-EN, nếu không sẽ phải train hai lần.
