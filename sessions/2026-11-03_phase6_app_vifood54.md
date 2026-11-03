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
