# KẾ HOẠCH HÀNH ĐỘNG CHI TIẾT — GIAI ĐOẠN TIẾP THEO
## Đồ án: LLMDet Vietnamese Food Grounding
### Ngày lập: 26/09/2026 | Cập nhật: 27/09/2026

---

## HIỆN TRẠNG (Cập nhật 27/09/2026 — 17:00)

| Hạng mục | Trạng thái | Chi tiết |
| :--- | :---: | :--- |
| Ảnh train | ✅ | 900 ảnh trong `grounding_data/vifood/images/train2017/` |
| Ảnh val | ✅ | 100 ảnh trong `grounding_data/vifood/images/val2017/` |
| Nhãn ODVG Train (VI short) | ✅ | `vifood_train_vg.jsonl` — 900 mẫu, 51 classes, caption dạng `"bánh bèo . phở ."` |
| Nhãn ODVG Train (EN short) | ✅ | `vifood_train_vg_en.jsonl` — 900 mẫu, tên tiếng Anh |
| Nhãn ODVG Val | ✅ | `vifood_val_vg.jsonl` + `vifood_val_vg_en.jsonl` |
| Nhãn COCO Val | ✅ | `instances_val.json` + `instances_val_en.json` (374 annotations, 51 classes) |
| **Nhãn ODVG Full VI Caption** | ✅ | `vifood_train_vg_vi_full.jsonl` (900 mẫu, 4402 regions verified) |
| BERT weights | ✅ | `huggingface/bert-base-uncased/` |
| Grounding DINO Swin-T checkpoint | ✅ | 1.09 GB tại `huggingface/mm_grounding_dino/` |
| Exp 1 checkpoint (VI short) | ✅ | `work_dirs/vifood_1k/iter_10000.pth` — loss 3.98, mAP 0.024, AR 0.233 |
| Exp 2 checkpoint (EN short) | ✅ | `work_dirs/vifood_en_1k/iter_10000.pth` — loss 3.82, mAP 0.055, AR 0.368 |
| ⭐ Exp 3 checkpoint (Full VI) | ✅ | `work_dirs/vifood_vi_full_1k/iter_10000.pth` — loss 4.47, mAP 0.055, AR 0.543 |
| Benchmark Pha 4 | ✅ | Hoàn tất 4/4 mô hình trên 100 ảnh val, log chi tiết tại Session 13 |
| **Web Demo Pha 5** | ✅ | Đang chạy tại `http://0.0.0.0:7861` (tmux `vifood_web_app`), latency 150.8ms, 6.6 FPS |
| GPU | ✅ | RTX 3090 24GB — VRAM web app chỉ ăn ~1GB, hoàn toàn ổn định |
| Môi trường | ✅ | PyTorch 2.10 + MMDet 3.3.0 + Gradio 5.50.0 |

---

## TỔNG QUAN 7 PHA

```
Pha 1 ─── Pha 2 ──────── Pha 3 ──────── Pha 3.5 ─────────── Pha 4 ────── Pha 5 ────── Pha 6
Sanity    Fine-tune       Ablation       ★ FULL VI CAPTION   Evaluation   Web App      Luận văn
Check     Exp 1 (VI)      Exp 2 (EN)     Exp 3 (ĐÓNG GÓP    Tổng hợp     + Demo       + Slide
                                          CHÍNH)
✅ Done   ✅ Done         ✅ Done        ✅ Done             ✅ Done      ✅ Done      ⬜ Next
27/09     27/09           27/09          27/09 chiều          27/09 tối    27/09 đêm    28/09-05/10
```

> **⭐ Pha 3.5 (Exp 3: Full Vietnamese Caption Grounding)** là **ĐÓNG GÓP CHÍNH** của đồ án — thay vì chỉ dùng prompt dạng ngắn `"bánh bèo . phở ."`, mô hình sẽ được train với caption tiếng Việt tự nhiên mô tả bữa ăn, grounding trực tiếp từ ngôn ngữ tự nhiên tới bounding box.

---

## PHA 1: SANITY CHECK & TẠO CONFIG ✅ HOÀN THÀNH

- [x] Fix lỗi PyTorch 2.6+ (`weights_only=False`)
- [x] Fix Transformers 4.40+ (`apply_chunking_to_forward` → `pytorch_utils`)
- [x] Cài dependencies (`terminaltables`, `pycocotools`, `shapely`, NLTK)
- [x] Chạy Zero-shot inference EN + VI trên `srcB_602_jpg`
- [x] Tạo `configs/grounding_dino_swin_t_vifood.py`
- [x] Log: [2026-09-27_phase1_sanity_check_and_configs.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase1_sanity_check_and_configs.md)

---

## PHA 2: THÍ NGHIỆM 1 — FINE-TUNE TIẾNG VIỆT (SHORT) ✅ HOÀN THÀNH

- [x] Train 10,000 iters, `batch_size=4`, `lr=5e-5` trên `vifood_train_vg.jsonl`
- [x] Loss hội tụ: 23.47 → **3.98**, `loss_cls` giảm ~600x (1.52 → 0.0026)
- [x] Kiểm chứng: phát hiện "bánh tráng" với confidence 99.12% và 98.73%
- [x] 5 checkpoints: `iter_2000.pth` → `iter_10000.pth` tại `work_dirs/vifood_1k/`
- [x] Log: [2026-09-27_phase2_training_completion.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase2_training_completion.md)

---

## PHA 3: THÍ NGHIỆM 2 — FINE-TUNE TIẾNG ANH / ABLATION ✅ HOÀN THÀNH

- [x] Viết `scripts/convert_vi_to_en_jsonl.py` — chuyển đổi nhãn VI → EN
- [x] Sinh `vifood_train_vg_en.jsonl`, `vifood_val_vg_en.jsonl`, `instances_val_en.json`
- [x] Tạo config `grounding_dino_swin_t_vifood_en.py` (hyperparams giống hệt Exp 1)
- [x] Khởi chạy train tại tmux `vifood_en_train` → `work_dirs/vifood_en_1k/`
- [x] Train hoàn tất 10.000 iters lúc 13:21 ngày 27/09, loss hội tụ: 3.8197
- [x] Checkpoint: `work_dirs/vifood_en_1k/iter_10000.pth` (1.85 GB)
- [x] Log: [2026-09-27_phase3_english_ablation_launch.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase3_english_ablation_launch.md) và [2026-09-27_phase3_5_exp3_training_completion.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase3_5_exp3_training_completion.md)

---

## ⭐ PHA 3.5: THÍ NGHIỆM 3 — FULL VIETNAMESE CAPTION GROUNDING (ĐÓNG GÓP CHÍNH)

### Tầm quan trọng

Đây là **đóng góp cốt lõi** của đồ án tốt nghiệp, phân biệt công trình với mọi baseline:

| Phương pháp | Caption Grounding | Ví dụ |
| :--- | :--- | :--- |
| Exp 1 (Short VI) | Tên ngắn nối dấu chấm | `"bánh bèo . chả . nước chấm ."` |
| Exp 2 (Short EN) | English short labels | `"steamed rice cakes . Vietnamese sausage ."` |
| **Exp 3 (Full VI)** ⭐ | **Câu miêu tả tự nhiên tiếng Việt** | `"Trên bàn có một đĩa bánh bèo rắc tôm cháy, bên cạnh là chén nước chấm và đĩa chả lụa thái lát."` |

**Lý do khoa học**: Grounding DINO sử dụng text encoder (BERT) để ghép nối ngôn ngữ ↔ vùng ảnh. Khi caption chứa mô tả phong phú về vị trí, đặc điểm, ngữ cảnh — mô hình học được nhiều tín hiệu hơn để phân biệt các món tương tự.

### Bước 3.5.1: Sinh Caption Tiếng Việt Tự Nhiên bằng Gemini API

**Script**: `scripts/generate_full_vietnamese_captions.py`

**Input**: Đọc `vifood_train_vg.jsonl` và `vifood_val_vg.jsonl` — lấy danh sách món ăn + bbox cho mỗi ảnh.

**Xử lý**: Với mỗi ảnh, gọi Gemini API (gemini-3.6-flash) với prompt dạng:

```
Bạn là chuyên gia ẩm thực Việt Nam. Hãy viết MỘT câu miêu tả ngắn gọn (50-120 từ)
về bữa ăn trong ảnh, gồm các món sau: bánh bèo, chả, nước chấm, bún, rau sống.

YÊU CẦU BẮT BUỘC:
1. Phải nhắc đến TẤT CẢ tên món trong danh sách ở dạng NGUYÊN GỐC (giữ chính xác dấu)
2. Miêu tả đặc điểm, cách bày trí, nguyên liệu đặc trưng
3. Câu phải tự nhiên, mạch lạc, không liệt kê đơn giản
4. KHÔNG thêm món nào không có trong danh sách
```

**Output**: Với mỗi mẫu, tạo caption giàu ngữ nghĩa và tính `tokens_positive` (character offset `[start, end]`) chính xác cho từng tên món trong câu:

```json
{
  "filename": "train2017/srcA_H-000_jpg.rf.xxx.jpg",
  "height": 640, "width": 640,
  "detection": { "instances": [...] },
  "grounding": {
    "caption": "Bữa ăn trưa đậm chất miền Trung với đĩa bánh bèo trắng mịn rắc tôm cháy vàng ruộm, bên cạnh là chén nước chấm pha chua ngọt, đĩa chả lụa thái lát mỏng, tô bún tươi và rổ rau sống xanh mướt.",
    "regions": [
      {
        "bbox": [165.57, 159.54, 285.22, 326.5],
        "phrase": "bánh bèo",
        "tokens_positive": [[46, 54]]
      },
      {
        "bbox": [387.25, 54.73, 460.53, 153.05],
        "phrase": "nước chấm",
        "tokens_positive": [[99, 108]]
      }
    ]
  },
  "conversations": [
    {"from": "human", "value": "<image>\nMô tả chi tiết bữa ăn trong hình."},
    {"from": "gpt", "value": "Bữa ăn trưa đậm chất miền Trung với đĩa bánh bèo trắng mịn..."}
  ]
}
```

**Chiến lược sinh caption ổn định**:
1. **Gemini API chính**: Gọi API cho mỗi ảnh (rate limit xử lý bằng retry + sleep)
2. **Template fallback**: Nếu API fail, dùng template có sẵn dựa theo tổ hợp món (`_generate_template_caption()`)
3. **Post-process bắt buộc**: Sau khi sinh caption, verify rằng TẤT CẢ tên món đều xuất hiện chính xác trong câu. Nếu thiếu → retry hoặc chèn thêm.
4. **Cache persistent**: Lưu kết quả Gemini vào `cache/gemini_full_vi_captions.json` để tái sử dụng

**Output files**:
- `grounding_data/vifood/annotations/vifood_train_vg_vi_full.jsonl` (900 mẫu)
- `grounding_data/vifood/annotations/vifood_val_vg_vi_full.jsonl` (100 mẫu)

### Bước 3.5.2: Tạo Config Training cho Exp 3

**File**: `configs/grounding_dino_swin_t_vifood_vi_full.py`

Nội dung:
- Kế thừa `grounding_dino_swin_t.py`
- `lmm=None` (Detector-only)
- `ann_file='annotations/vifood_train_vg_vi_full.jsonl'`
- **Hyperparams giống 100% Exp 1 & Exp 2** (fair ablation):
  - `batch_size=4`, `lr=5e-5`, `max_iters=10000`
  - `warmup=500`, `milestones=[7000, 9000]`
  - `backbone lr_mult=0.1`
- `clean_caption=False` (giữ nguyên dấu tiếng Việt)
- `use_short_cap=False` (sử dụng full caption)

### Bước 3.5.3: Train Exp 3

```bash
# Chạy trong tmux session (sau khi Exp 2 xong)
tmux new-session -d -s vifood_vi_full "cd /home/atin/tuan/SoPSoP/llmdet_vietnamese_food && \
python mmdet_train.py \
    configs/grounding_dino_swin_t_vifood_vi_full.py \
    --work-dir work_dirs/vifood_vi_full_1k \
    --amp 2>&1 | tee work_dirs/vifood_vi_full_1k/train.log ; exec bash"
```

**Thời gian dự kiến**: ~2.3 giờ (10,000 iters × 0.83s/iter)
**Lưu checkpoints**: `work_dirs/vifood_vi_full_1k/iter_2000.pth` → `iter_10000.pth`

### Bước 3.5.4: Chạy Demo Trực quan Exp 3

```bash
python image_demo.py \
    ../grounding_data/vifood/images/val2017/srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg \
    configs/grounding_dino_swin_t_vifood_vi_full.py \
    --weights work_dirs/vifood_vi_full_1k/iter_10000.pth \
    --texts "Trên bàn có đĩa bánh tráng nướng giòn rắc hành phi." \
    --pred-score-thr 0.3 \
    --out-dir ./demo_output/exp3_vi_full \
    --cfg-options model.lmm=None
```

## ⭐ PHA 3.5: THÍ NGHIỆM 3 — FULL VIETNAMESE CAPTION GROUNDING ✅ HOÀN THÀNH

- [x] Sinh 900 train + 100 val full natural captions với 4.402 regions verified (`vifood_train_vg_vi_full.jsonl`)
- [x] Tạo config training `configs/grounding_dino_swin_t_vifood_vi_full.py`
- [x] Train 10.000 iters trong tmux `vifood_vi_full_train`, loss: 40.5 → 4.4720
- [x] Checkpoint cuối: `work_dirs/vifood_vi_full_1k/iter_10000.pth` (1.85 GB)
- [x] Log: [2026-09-27_phase3_5_exp3_training_completion.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase3_5_exp3_training_completion.md)

---

## PHA 4: ĐÁNH GIÁ TỔNG HỢP & SO SÁNH ✅ HOÀN THÀNH

### Bảng Kết quả So sánh Benchmark (Chương 4 Luận văn)

```
┌──────────────────────────────────────┬───────┬────────┬────────┬────────┬────────────────────────┐
│ Mô hình / Thí nghiệm                 │  mAP  │ mAP_50 │ mAP_75 │ Recall │ Ghi chú                │
├──────────────────────────────────────┼───────┼────────┼────────┼────────┼────────────────────────┤
│ Zero-shot (pretrained, chưa FT)     │ 0.026 │ 0.034  │ 0.031  │ 0.392  │ Baseline gốc           │
│ Exp 1: FT Short Vietnamese          │ 0.024 │ 0.037  │ 0.027  │ 0.233  │ "phở . bánh mì ."      │
│ Exp 2: FT Short English             │ 0.055 │ 0.084  │ 0.055  │ 0.368  │ "Vietnamese Pho ."     │
│ ⭐ Exp 3: FT Full Vietnamese Caption │ 0.055 │ 0.074  │ 0.066  │ 0.543  │ ĐÓNG GÓP CHÍNH (+129%) │
└──────────────────────────────────────┴───────┴────────┴────────┴────────┴────────────────────────┘
```

- [x] Bước 4.1: Đo mAP độc lập cho cả 4 mô hình trên 100 ảnh validation
- [x] Bước 4.2: Lập bảng so sánh và phân tích chuyên sâu
- [x] Log: [2026-09-27_phase4_benchmark_and_evaluation.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase4_benchmark_and_evaluation.md)

### Bước 4.3: Phân tích Chuyên sâu

1. **Cross-lingual gap**: Chênh mAP giữa Exp 1 (VI short) vs Exp 2 (EN short) → Ảnh hưởng ngôn ngữ
2. **Caption richness gain**: Chênh mAP giữa Exp 1 (VI short) vs Exp 3 (VI full) → Lợi ích của ngữ cảnh phong phú
3. **Per-class analysis**: Xuất bảng mAP theo từng class (51 lớp) — highlight các class có cải thiện nhiều nhất
4. **Confusion matrix / Error analysis**: Screenshot False Positive/Negative tiêu biểu
5. **Qualitative comparison**: So sánh ảnh demo cùng 1 ảnh val qua 4 mô hình (bố trí 2×2 grid)

---

## PHA 5: XÂY DỰNG WEB APP DEMO & TRA CỨU DINH DƯỠNG ✅ HOÀN THÀNH
- [x] Bước 5.1: Xây dựng cơ sở tri thức dinh dưỡng 51 món Việt (`nutrition_vifood_51.json`) với đầy đủ Calo, Đạm, Tinh bột, Béo và ghi chú.
- [x] Bước 5.2: Xây dựng ứng dụng Gradio tương tác cao (`app.py`), hỗ trợ Visual Grounding câu tự nhiên và nhãn ngắn, tự động tính tổng calo mâm cơm.
- [x] Bước 5.3: Hỗ trợ so sánh trực quan giữa 3 mô hình (Exp 3 Full VI, Exp 1 Short VI, Baseline Zero-Shot) và tích hợp 5 ảnh mẫu kiểm thử nhanh.
- [x] Bước 5.4: Đo kiểm hiệu năng suy luận trên RTX 3090 (`benchmark_inference_speed.py`): độ trễ **150.84 ms** (6.63 FPS), VRAM chỉ tiêu tốn **~0.96 GB**.
- [x] Bước 5.5: Xuất bộ ảnh đối sánh định tính (`export_qualitative_results.py` → `demo_output/qualitative_comparison/`).
- [x] Khởi chạy Web App thường trực tại: `http://0.0.0.0:7861` (tmux session `vifood_web_app`).
- [x] Log chi tiết: [2026-09-27_phase5_web_demo_and_qualitative_evaluation.md](file:///home/atin/tuan/SoPSoP/sessions/2026-09-27_phase5_web_demo_and_qualitative_evaluation.md)

---

## PHA 6: VIẾT LUẬN VĂN & BẢO VỆ (Ngày 05/10 – 11/10)

### Cấu trúc Luận văn

| Chương | Nội dung | Nguồn tham khảo |
| :---: | :--- | :--- |
| **1** | Giới thiệu, mục tiêu, phạm vi, đóng góp | Session 01 |
| **2** | Tổng quan: OV-OD, Grounding DINO, LLMDet, BERT, ODVG | Session 01, 02 |
| **3** | Xây dựng ViFood-Grounding-1K: Thu thập, sàng lọc, Gemini enrichment, đóng gói ODVG | Session 03–08 |
| **4** | Thực nghiệm: Zero-shot, Exp1 (VI short), Exp2 (EN), **Exp3 (Full VI Caption)**, Ablation, Per-class | Pha 2+3+3.5+4 |
| **5** | Hệ thống demo: Backend/Frontend, Language Bridge, Module dinh dưỡng, FPS benchmark | Pha 5 |
| **6** | Kết luận & Hướng phát triển | Tổng hợp |

### Điểm nhấn Chương 4 (Thực nghiệm)

> **Giả thuyết**: Sử dụng caption tiếng Việt tự nhiên giàu ngữ cảnh (thay vì nhãn ngắn) giúp mô hình Visual Grounding học được các tín hiệu ngữ nghĩa phong phú hơn, cải thiện độ chính xác phát hiện trên dữ liệu ẩm thực Việt Nam.
>
> **Thí nghiệm kiểm chứng**: So sánh 4 cấu hình (Zero-shot / Short VI / Short EN / Full VI) trên cùng bộ val 100 ảnh, cùng hyperparams, cùng backbone.

### Chuẩn bị Bảo vệ
- [ ] Slide 15-20 trang
- [ ] Video quay demo sản phẩm (dự phòng nếu demo live lỗi)
- [ ] Bảng so sánh mAP in A3/A4
- [ ] Câu hỏi phản biện thường gặp:
  - "Tại sao không dùng YOLO-World?" → Khả năng Fine-grained Grounding mà YOLO thiếu
  - "1.000 ảnh có ít quá không?" → LLMDet pretrained trên triệu ảnh, 1K đủ cho domain adaptation
  - "Xử lý tiếng Việt thế nào?" → Show bảng Ablation VI vs EN + Full VI caption
  - **"Full VI caption có thực sự giúp ích?"** → Show bảng mAP tăng + per-class analysis + ví dụ trực quan

---

## CHECKLIST TỔNG HỢP

### Pha 1 — Sanity Check (27/09) ✅
- [x] Chạy `image_demo.py` zero-shot trên 1 ảnh val (EN + VI)
- [x] Tạo `configs/grounding_dino_swin_t_vifood.py`
- [x] Fix lỗi tương thích PyTorch 2.6+ & Transformers 4.40+
- [x] Log: `2026-09-27_phase1_sanity_check_and_configs.md`

### Pha 2 — Thí nghiệm 1: Short Vietnamese (27/09) ✅
- [x] Train Exp 1 (10,000 iters) → Loss 23.47 → 3.98
- [x] Kiểm chứng trực quan (confidence 99%+)
- [x] Lưu 5 checkpoints tại `work_dirs/vifood_1k/`
- [x] Log: `2026-09-27_phase2_training_completion.md`

### Pha 3 — Thí nghiệm 2: Short English (27/09) 🔄
- [x] Viết script `convert_vi_to_en_jsonl.py`
- [x] Sinh `vifood_train_vg_en.jsonl` + `vifood_val_vg_en.jsonl` + `instances_val_en.json`
- [x] Tạo config `grounding_dino_swin_t_vifood_en.py`
- [x] Khởi chạy train Exp 2 tại tmux `vifood_en_train`
- [ ] Chờ xong (ETA ~13:20)
- [x] Log: `2026-09-27_phase3_english_ablation_launch.md`

### ⭐ Pha 3.5 — Thí nghiệm 3: Full Vietnamese Caption (27/09 chiều) ⬜
- [ ] Viết script `scripts/generate_full_vietnamese_captions.py`
- [ ] Gọi Gemini API sinh caption TV tự nhiên cho 900+100 ảnh
- [ ] Verify tokens_positive chính xác cho mọi tên món
- [ ] Xuất `vifood_train_vg_vi_full.jsonl` + `vifood_val_vg_vi_full.jsonl`
- [ ] Tạo config `configs/grounding_dino_swin_t_vifood_vi_full.py`
- [ ] Train Exp 3 (10,000 iters, ~2.3 giờ)
- [ ] Chạy demo trực quan
- [ ] Log: `2026-09-27_phase35_full_vi_caption.md`

### Pha 4 — Đánh giá Tổng hợp (28/09) ⬜
- [ ] Đo mAP zero-shot baseline
- [ ] Đo mAP Exp 1 (Short VI)
- [ ] Đo mAP Exp 2 (Short EN)
- [ ] Đo mAP Exp 3 (Full VI Caption)
- [ ] Lập bảng so sánh 4 mô hình
- [ ] Phân tích per-class + failure cases
- [ ] So sánh trực quan 2×2 grid

### Pha 5 — Web App (29/09 – 04/10) ⬜
- [ ] Convert checkpoint → HuggingFace
- [ ] Xây Backend API
- [ ] Xây Frontend tiếng Việt
- [ ] Module dinh dưỡng 51 món
- [ ] Đo FPS / Latency

### Pha 6 — Luận văn (05/10 – 11/10) ⬜
- [ ] Viết Chương 1 + 2
- [ ] Viết Chương 3 (trích session logs)
- [ ] Viết Chương 4 (bảng mAP + biểu đồ + **Full VI Caption analysis**)
- [ ] Viết Chương 5 (hệ thống demo)
- [ ] Viết Chương 6 (kết luận)
- [ ] Slide + video demo

---

## GHI CHÚ KỸ THUẬT QUAN TRỌNG

### Về `tokens_positive` trong Full VI Caption

Khi caption là câu tự nhiên dài, việc tính `tokens_positive` phức tạp hơn caption ngắn:

```python
caption = "Trên bàn có đĩa bánh bèo trắng mịn rắc tôm cháy"
# "bánh bèo" xuất hiện tại vị trí [18, 26]
# => tokens_positive = [[18, 26]]

# Nếu 1 tên món xuất hiện NHIỀU LẦN trong caption:
# => Chỉ lấy lần xuất hiện ĐẦU TIÊN (consistency)
# => Nhiều box cùng class chia sẻ cùng tokens_positive
```

### Xử lý edge cases khi sinh caption
1. **Món trùng tên / tên ngắn** (`bún`, `chả`): Đảm bảo substring match chính xác, tránh match sai (ví dụ "bún" trong "bún bò Huế")
2. **Số lượng box nhiều** (>10 boxes/ảnh): Caption dài hơn nhưng vẫn giới hạn ~120 từ
3. **Gemini API rate limit**: Sleep 0.5s giữa các request, retry 3 lần với backoff
4. **Validation**: Sau khi sinh, chạy script kiểm tra tất cả `tokens_positive` đều hợp lệ
