# NHẬT KÝ PHIÊN LÀM VIỆC: 03/11/2026
## Chủ đề: Pha 6 — demo ViFood-54 (54 lớp, checkpoint B3b, tìm món theo câu, dinh dưỡng)

---

### 1. Quyết định
- Viết app mới `llmdet_vietnamese_food/app_vifood54.py` thay vì sửa `app.py`: `app.py` đang có thay đổi chưa commit
  của người khác (VLM Gemini, Exp 1–4 trên 51 lớp) và phụ thuộc `portion_estimator.py` / `vlm_discovery.py` chưa nằm
  trong git. App cũ vẫn chạy được ở cổng 7861.
- Bỏ bước Gemini "khám phá món" ở app mới: với 54 lớp, prompt đủ tên lớp (đúng cách đánh giá COCO) đã vừa 224/256 token,
  không cần VLM chọn trước lớp. Tránh phụ thuộc dịch vụ ngoài và API key.
- `portion_estimator.py` cũ tra DB bằng `dish_key.lower()` nên các khóa có chữ hoa (`bún bò Huế`, `mì Quảng`) luôn rơi vào
  giá trị dự phòng. App mới tra theo đúng tên lớp và chọn nhóm khẩu phần từ taxonomy, không dùng danh sách tên cứng.

### 2. File mới
| File | Nội dung |
| :--- | :--- |
| `nutrition_vifood54.json` | 54 món theo tên lớp; 51 món lấy từ `nutrition_vifood_51.json` qua `taxonomy.nutrition_key`; thêm `nem rán`, `quẩy`, `món tráng miệng` (`estimated: true`, cần đối chiếu Bảng thành phần thực phẩm Việt Nam) |
| `vifood54_core.py` | `detect` (prompt 54 lớp), `parse_sentence` + `ground` (tên lớp / tên gọi khác trong câu → tokens_positive, như `eval_grounding.py`), `Nutrition` (hệ số khẩu phần theo nhóm: món nước / nước chấm / rau / món đĩa từ taxonomy), `draw` (PIL, chữ có dấu) |
| `app_vifood54.py` | Gradio 4 tab: nhận diện 54 món + dinh dưỡng; tìm món theo câu; kết quả thực nghiệm; từ điển 54 món (định nghĩa hình thái + dinh dưỡng). Cổng 7862 (biến `PORT`) |
| `demo_examples_vifood54.json` | 6 ảnh test mà B3b nhận đúng bộ lớp cả 2 chế độ (ảnh mẫu được chọn, không đại diện cho độ chính xác chung) |

### 3. Kiểm tra
- Lõi: tách câu đúng cụm dài trước (`bún bò Huế`, `bún đậu mắm tôm`), alias (`nước chấm` → `đồ chấm`).
- Qua `gradio_client` với app đang chạy: nhận diện 1.3 s (lần đầu) / ~0.3 s, tìm theo câu ~0.2 s trên RTX 3090.

### 4. Chạy
```bash
tmux new -d -s vifood54_app 'cd llmdet_vietnamese_food && python app_vifood54.py'   # http://<server>:7862
```

### 5. Còn hạn chế
- Nhãn chữ trên ảnh có thể chồng nhau khi 2 box cùng mép trên.
- Khẩu phần suy từ diện tích box (heuristic), không phải ước lượng thể tích.

## Bổ sung: Gemini nhìn ảnh trước để liệt kê món (cùng ngày)

Theo yêu cầu, tab "Nhận diện 54 món" có thêm bước Gemini liệt kê món trước khi detector khoanh box.

| File | Thay đổi |
| :--- | :--- |
| `vifood54_vlm.py` (mới) | `list_dishes(img)`: gửi ảnh + danh mục 54 lớp (tên, tên gọi khác, định nghĩa hình thái từ taxonomy) cho Gemini, yêu cầu JSON `{dishes:[{name,count}], other, description}`; tên trả về được đưa về lớp qua tên lớp/tên gọi khác, món ngoài danh mục vào `other`. Timeout 45 s/model (`GEMINI_TIMEOUT_S`), thử `gemini-3.6-flash` → `3.5-flash` → `flash-latest`, thử lại model đầu sau 3 s; nhớ theo hash ảnh trong phiên. `prompt_classes(names)` = món Gemini thấy + `confusable_with` của chúng (giữ negative như lúc train). Key lấy từ `GEMINI_API_KEY`/`GOOGLE_API_KEY` hoặc `.env`/`.gemini_key` (gitignore); không có key mặc định trong mã, không in key |
| `vifood54_core.py` | `detect(..., classes=None, return_best=False)`: prompt tuỳ chọn, trả thêm điểm box cao nhất mỗi lớp |
| `app_vifood54.py` | Radio 3 chế độ: (1) Gemini liệt kê → detector với prompt rút gọn, chỉ giữ box món Gemini thấy (mặc định); (2) prompt đủ 54 lớp → chỉ giữ box món Gemini xác nhận; (3) chỉ detector, không gửi ảnh ra ngoài. Bảng Gemini: món, số đếm, số box, điểm cao nhất, món ngoài 54 lớp, box bị bỏ vì Gemini không liệt kê. Gemini lỗi → tự dùng prompt 54 lớp, không lọc |

Kiểm tra (ảnh bánh xèo `srcB_1015`, B3b, ngưỡng 0.3):
- Gemini (1 lần gọi thành công, 18.5 s): bánh xèo ×2, rau sống ×2, đồ chấm ×1, bánh tráng ×1; ngoài danh mục: trà đá.
- Chế độ 1 (prompt 8 lớp): 6 box, đủ 2 rổ rau sống; điểm cao nhất bánh xèo 0.43 / rau sống 0.38 / đồ chấm 0.65.
- Chế độ 2 và 3 (prompt 54 lớp): 5 box, 1 rổ rau sống; đồ chấm 0.47. Bánh tráng dưới ngưỡng ở cả hai (0.21 / 0.11).
- Sau đó key trả 503 (Google quá tải) rồi 429 (hết quota) cho mọi model → chưa đo được trên 5 ảnh mẫu còn lại; app
  đã xử lý đúng nhánh lỗi (rơi về prompt 54 lớp).

Hạn chế / việc còn mở:
- Chưa đo trên tập test: muốn kết luận chế độ 1 có tốt hơn prompt 54 lớp thì cần chạy hết 414 ảnh test (≈ 414 lần gọi,
  cần quota) hoặc dùng Gemma cục bộ đã tải. Lưu ý chế độ 1 làm prompt test khác prompt đánh giá COCO.
- Gemini chậm (~18 s/ảnh) so với detector (~0.3 s) và gửi ảnh lên Google.
- `vlm_discovery.py` (file chưa commit của app cũ) có API key viết cứng trong mã: không nên commit file đó.

Cập nhật: theo yêu cầu, tab nhận diện chỉ còn một chế độ **Gemini liệt kê món → detector khoanh box** (bỏ radio chọn
chế độ, bỏ "54 lớp → Gemini lọc" và "chỉ detector"). Gemini lỗi (không key, 503, 429) thì vẫn tự dùng prompt 54 lớp,
không lọc, và ghi rõ trên giao diện.

### Cập nhật 2: Gemini viết caption hình thái → detector khoanh theo caption

Vấn đề với prompt rút gọn (người dùng chạy trên ảnh tiệc hải sản kiểu Âu): prompt còn 11 lớp → box của món không có
trong prompt bị gán lớp gần nhất (9 box "hàu" phủ cả bàn), lọc cứng theo Gemini xoá các box khác. Prompt 54 lớp chỉ ra
1 box hàu đúng. Rút prompt đi ngược kết quả B0→B1 (cần negative).

Luồng mới (theo yêu cầu "qua VLM trước để rõ các món và viết caption mô tả"):
1. `vifood54_vlm.describe(img)`: Gemini trả `dishes` (tên lớp, count, position trong 9 vùng / "rải rác trên bàn"),
   `other`, `caption`, `description`. Prompt đưa 54 lớp + định nghĩa hình thái, 3 câu mẫu theo văn phong caption L2,
   quy tắc: đúng tên lớp, số lượng + lượng từ, vị trí, chỉ đặc điểm nhìn thấy, không "của" (BERT bỏ dấu → `cua`),
   không từ hương vị, ≤120 từ.
2. `prepare_caption`: bỏ câu không có tên món mà có từ hương vị; thêm câu "Có N phần <món> ở <vị trí>." cho món
   Gemini liệt kê nhưng caption không nhắc; cắt câu cuối nếu > 250 token BERT; lint (`captions/lint.py`) → cảnh báo.
3. `core.ground(img, model, caption)`: mỗi tên món trong caption là một entity (như `eval_grounding.py`, B3b R@1
   L2 = 0.663); `keep_counts` giữ tối đa `count` box mỗi món theo Gemini.
4. App: caption hiện trong ô sửa được + nút "Khoanh lại theo caption này" (không gọi lại Gemini). Gemini lỗi → prompt
   54 lớp. Timeout 45 s/model, tổng tối đa 60 s (`GEMINI_BUDGET_S`).

Thử với Gemini thật (`gemini-3.5-flash-lite`, 18–30 s/ảnh, B3b, ngưỡng 0.3), 3 ảnh mẫu đều đúng bộ món:
- bánh xèo + rau sống + đồ chấm: 4 box (bánh xèo 2, rau sống 1/2, đồ chấm 1); caption gộp các món vào một câu.
- nem chua + rau sống: đúng 2 món; Gemini thêm "món ăn khác" ×6 cho ớt/hoa trang trí → 1 box sai (0.19).
- bánh bột lọc + đồ chấm: 2 box đúng (0.31, 0.55); Gemini đếm 4 bánh nhưng detector cho 1 box bao cả đĩa.
Lần gọi thứ 3 gặp 504/503 nhiều lần (143 s) → thêm giới hạn tổng 60 s.

Còn mở: chưa đo luồng này trên 414 ảnh test (cần quota Gemini); điểm grounding thấp hơn chế độ OD nên box thứ 2 trở đi
của cùng món hay dưới ngưỡng.
