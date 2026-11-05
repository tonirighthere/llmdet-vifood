# KẾ HOẠCH CHI TIẾT — GIAI ĐOẠN VIFOOD-54
## Đồ án: LLMDet Vietnamese Food Grounding
### Lập: 27/10/2026 · Rút gọn 27/10 (chỉ giữ run cần thiết, xem mục 9) · Thay thế phần "việc tiếp theo" trong `PLAN_NEXT_STEPS.md` (bản đó là của ViFood-1K / 51 class)

---

## 0. HIỆN TRẠNG

| Hạng mục | Trạng thái | Ghi chú |
| :--- | :---: | :--- |
| Rà soát pipeline cũ | ✅ | 3 lỗi gốc: VG mode **không có negative**; `lmm=None` nên caption dài không vào loss; caption dạy ngược (53% caption nhắc lớp không có box, từ hương vị, BERT bỏ dấu: `của→cua`, `gói→gỏi`, `cạnh→canh`, `lâu→lẩu`) |
| Nhãn sửa qua crops_review + taxonomy v2 + build lại Pha 0/2 (30–31/10) | ✅ | 163 box đổi lớp, 51 box xóa ở train; split giữ nguyên; `sessions/2026-10-31_relabel_taxonomy_v2.md` |
| B1 trên nhãn mới (`work_dirs/vifood54_b1_od_v2`) | ✅ | test mới: B1-v2 0.315 = B1-v1 0.315 (`EVAL_V2.md`); B1-v2 là mốc so sánh cho B3 |
| Pha 3: loader VG (biến thể + bản lật, negative khó, ConcatDataset OD+VG) | ✅ | dry-run: span 0 lỗi, vị trí khớp 447/447, ≤256 token; `sessions/2026-10-31_phase3_b3.md` |
| Caption hình thái (Pha 2) | ✅ | `grounding_data/vifood54/annotations/*_vg_cap*.jsonl`, `CAPTION_REPORT.md` |
| Taxonomy 54 class | ✅ | `scripts/vifood54/taxonomy.json`; `chả giò` ≠ `nem rán` (không gộp); id class = id `obj.names` |
| Dữ liệu ViFood-54 | ✅ | 3956 ảnh / 18 253 box / 3204 ảnh gốc; split theo ảnh gốc train 3138 / val 404 / test 414 |
| Cân bằng lớp | ✅ | RFS cho lớp hiếm (`train_od_rfs.jsonl`, 4142 mẫu/epoch) + class dropout cho `đồ chấm`, `rau sống`, `món ăn khác` (`class_drop.json`) + flip/crop |
| B0 zero-shot (test) | ✅ | mAP 0.015 · AP50 0.019 · AP75 0.016 |
| B1 OD + negative | ✅ | val 0.347 · **test mAP 0.310 / AP50 0.388** · cổng Pha 1 đạt · phân tích: `grounding_data/vifood54/EVAL_B0_B1.md` |
| App / dinh dưỡng | ⚠️ | `app.py`, `vlm_discovery.py` (`CANONICAL_51_DISHES`), `nutrition_vifood_51.json` vẫn là 51 lớp cũ |

Chi tiết Pha 0: `sessions/2026-10-27_vifood54_phase0_b1_od.md` · Thống kê lớp: `grounding_data/vifood54/BUILD_REPORT.md`.

---

## 1. NGUYÊN TẮC XUYÊN SUỐT

1. **Caption chỉ mô tả cái nhìn thấy**: hình dạng, màu, bề mặt, thành phần lộ ra, dụng cụ đựng, số lượng, vị trí. Không hương vị, mùi, cảm xúc, nguồn gốc vùng miền, cách nấu không nhìn thấy.
2. **Không có token "mồ côi"**: mọi tên lớp xuất hiện trong caption phải gắn với box; kiểm tra sau khi BERT bỏ dấu (lint tự động, không kiểm bằng mắt).
3. **Vị trí và số lượng lấy từ box GT**, không lấy từ LLM.
4. **Prompt train phải giống prompt test**: luôn có negative; ngân sách 256 token BERT (54 lớp ≈ 224 token).
5. **Mọi so sánh trên cùng test split** (`instances_test.json`); val chỉ để chọn checkpoint.
6. Mỗi thí nghiệm có một config riêng, một work_dir riêng, một dòng trong bảng kết quả (mục 8).
7. **Tiết kiệm GPU**: chỉ train khi run đó trả lời một câu hỏi mà luận văn cần; ablation nào không đổi kết luận thì bỏ. Mọi thứ đo được không cần train (phân tích lỗi, grounding câu, so sánh prompt) thì làm bằng inference trên checkpoint có sẵn.

---

## 2. PHA 1 — CHỐT B1 (cổng quyết định) · ✅ XONG 28/10

**Kết luận** (chi tiết `sessions/2026-10-28_phase1_b1_od_training_completion.md` mục 8–9):
- Test mAP 0.310 (B0 0.015) → đạt cổng, B1 là baseline chính.
- Tên dính chữ sau khi bỏ dấu: 0 nhầm ở score ≥ 0.3 → **giữ tên tiếng Việt**, không thêm tiếng Anh.
- Lỗi chính là món giống hình (`bánh chưng`→`bánh tét`, `xôi`→`cơm chiên`, `ngao sò`→`ốc`, `nem chua`→`gỏi cuốn`, `bún riêu`↔`bún bò Huế`, `cao lầu`→`mì Quảng`) → attribute bank Pha 2 ưu tiên thuộc tính phân biệt các cặp này.
- **Giữ 16k iter** cho B3 (val chưa bão hòa trước khi giảm LR).
- Việc phụ: kiểm tra tay nhãn `chả giò` (AP 0.10, hay bị đoán thành `bánh tráng`).

Nội dung gốc của pha:

**Việc làm**
1. Khi B1 xong: test checkpoint best
   ```bash
   cd llmdet_vietnamese_food
   python mmdet_test.py configs/grounding_dino_swin_t_vifood54_b1_od.py \
       work_dirs/vifood54_b1_od/best_coco_bbox_mAP_iter_*.pth --work-dir work_dirs/vifood54_b1_od_test
   ```
2. Viết `scripts/vifood54/analyze_eval.py`: từ file dự đoán (`--out` pkl) + `instances_test.json` xuất
   - AP/AP50 theo lớp, sắp xếp tăng dần;
   - ma trận nhầm lẫn lớp (IoU ≥ 0.5, pred lớp A trùng GT lớp B);
   - các cặp cần theo dõi:
     - giống nhau về hình: `chả giò`↔`nem rán`, `bánh căn`↔`bánh khọt`, `bánh bèo`↔`bánh bột lọc`, `bún tươi`↔các món bún;
     - **dính nhau sau khi BERT bỏ dấu** (`scripts/vifood54/check_tokenizer.py`): `quẩy`→`quay` nằm trong `heo quay`/`gà quay`; `lẩu`→`lau` nằm trong `cao lầu`; `bánh căn`→`ban ##h can` là tiền tố của `bánh canh`; `canh`⊂`bánh canh`, `cua`⊂`súp cua`, `gỏi`⊂`gỏi cuốn`, `tôm`⊂`bún đậu mắm tôm`; gần trùng `cá chiên`↔`cơm chiên`, `mực`↔`ốc`.
3. Lưu ảnh định tính 20 ảnh test (GT vs pred) để dùng trong luận văn.
4. **Chọn lịch train cho các run sau từ đường val của B1**: nếu mAP val bão hòa sớm (ví dụ best ở iter 8k–10k), các run sau dùng `max_iter` ≈ best + 2k và dời milestones tương ứng → tiết kiệm 30–40% thời gian mỗi run.

**Cổng quyết định**
- B1 mAP test ≥ ~0.15 (gấp nhiều lần B0 và Exp4 ~0.05) → giả thuyết "thiếu negative" được xác nhận, B1 thành baseline chính, sang Pha 2.
- Nếu không tăng rõ → **dừng, debug trước** (kiểm tra tokens_positive sau `clean_name().lower()`, label remap trong `od_aug`, prompt test có đúng 54 lớp, thử tắt class dropout/RFS để cô lập).

5. **Quyết định xử lý tiếng Việt bị BERT bỏ dấu** (không tốn run riêng):
   - Nếu các cặp "dính nhau sau bỏ dấu" ở trên **không** nhầm nhiều hơn các cặp khác → giữ nguyên tên tiếng Việt.
   - Nếu nhầm rõ (ví dụ `quẩy` bị dự đoán ở `gà quay`) → chỉ những lớp đó dùng tên kèm tiếng Anh trong cả label map và prompt test (ví dụ `quẩy fried dough sticks`, `lẩu hotpot`), gộp vào B3. Chỉ áp cho vài lớp vì prompt 54 lớp đã ~224/256 token.
   - Không đổi text encoder (PhoBERT/XLM-R mất alignment ảnh–chữ đã pretrain, cần pretrain lại quy mô lớn) và không thêm token mới vào vocab — ghi vào hạn chế/hướng phát triển.

**Xong khi**: có bảng AP theo lớp + ma trận nhầm lẫn của B0 và B1 trên test, và đã chốt cách xử lý tên lớp bị dính.

---

## 3. PHA 2 — BỘ SINH CAPTION HÌNH THÁI · ✅ XONG 28/10 (chờ duyệt tay bank)

**Kết quả** (chi tiết `sessions/2026-10-28_phase2_morphology_captions.md`): code ở `scripts/vifood54/captions/`;
thuộc tính hình thái nằm trong `taxonomy.json` v2 (trường `visual`, từ 30/10); 6 biến thể/ảnh, lint đạt 99.9% (biến thể lỗi chỉ do quá dài),
15/15 unit test. Phát hiện: `chả giò` trong nhãn là giò lụa, `nem rán` là cuốn chiên.

Nội dung gốc của pha:

Thư mục mới: `scripts/vifood54/captions/`.

### 2.1 Bộ thuộc tính hình thái (attribute bank) — `taxonomy.json`, thêm trường `visual`
Mỗi lớp (trừ `catch_all`) có:
```json
"visual": {
  "vessel":     ["tô", "bát"],
  "shape":      ["sợi bánh dẹt", "..."],
  "color":      ["nước dùng trong", "..."],
  "components": ["lát thịt mỏng màu nâu hồng", "hành lá xanh"],
  "surface":    ["bề mặt bóng dầu"]
}
```
- Soạn tay cho 52 lớp món (2 lớp catch_all không có); mỗi trường 2–4 cụm để đa dạng.
- `chả giò` và `nem rán` phải có thuộc tính **phân biệt được bằng mắt** (ví dụ vỏ bánh tráng phồng rộp vs vỏ bánh đa nem mịn, kích thước cuốn, cách cắt) — lấy từ quan sát ảnh train, không đoán.
- Cấm dùng tên lớp khác trong thuộc tính (ví dụ `bánh bèo` viết "ruốc màu cam", không viết "tôm").

### 2.2 Bố cục từ box GT — `layout.py`
- Vị trí theo lưới 3×3 trên tâm box: `góc trên bên trái`, `phía trên`, `chính giữa`, `bên phải`, ...
- Kích thước tương đối theo diện tích box/ảnh: `lớn`, `vừa`, `nhỏ`.
- Đếm theo lớp: `một`, `hai`, `ba`, `nhiều`.
- Từ nối an toàn (không trùng tên lớp sau khi bỏ dấu): dùng `kế bên`, `gần`, `phía`… **không** dùng `bên cạnh`, `của`, `gói`, `lâu`, `cà`.

### 2.3 Template & ghép caption — `builder.py`
Mỗi ảnh sinh K biến thể cho từng mức:
| Mức | Ví dụ |
| :--- | :--- |
| L1 cụm | "một tô phở, một đĩa rau sống và hai chén đồ chấm" |
| L2 dài | "Chính giữa là một tô phở lớn có sợi bánh dẹt và hành lá xanh. Phía trái có một đĩa rau sống lá xanh. Góc dưới bên phải là hai chén đồ chấm nhỏ màu nâu đỏ." |
| Vùng | "tô phở có sợi bánh dẹt và lát thịt mỏng" (chỉ dùng nếu chạy B5) |

- Ghép theo đoạn, **ghi offset ký tự lúc ghép** (không `str.find` sau đó).
- Lớp `catch_all` (`món ăn khác`, `món tráng miệng`): chỉ nêu tên, không thuộc tính.
- Mỗi caption kèm `flip_variant` (đã đổi trái↔phải) để dùng khi ảnh bị lật.

### 2.4 Lint — `lint.py` (chạy trên mọi caption, fail là loại)
1. Tokenize bằng chính BERT của model (đã bỏ dấu); mọi chuỗi token trùng tên một lớp phải nằm trong span đã đăng ký của đúng lớp đó. Danh sách từ thường bị đọc thành tên lớp lấy từ `check_tokenizer.py`: `của→cua, cạnh→canh, gói→gỏi, lâu→lẩu, óc→ốc, mức/mục→mực, hậu→hàu, phố/phó→phở, quay/quầy→quẩy, xởi→xôi`. Lưu ý `quay` là từ thật trong tên `heo quay`/`gà quay` — chỉ hợp lệ khi nằm trong span của 2 lớp đó.
2. Từ điển cấm hương vị/cảm xúc: `thơm, ngon, đậm đà, ngọt, cay, chua, béo, bùi, hương vị, hấp dẫn, thèm, ấm cúng, quê nhà, truyền thống, đặc sản, tinh hoa, nóng hổi, ...`.
3. Độ dài: caption + negative ≤ 256 token.
4. Span khớp tuyệt đối: `caption[s:e] == tên lớp`.
5. Unit test `tests/test_captions.py` cho các ca khó: `bún tươi` cạnh `bún riêu`, `canh` vs `cạnh`, `cua` vs `của`, ảnh 30+ box.

### 2.5 Xuất dữ liệu — `build_captions.py`
- `train_vg_cap.jsonl`: mỗi dòng có `grounding.variants: [{caption, flip_caption, regions:[{bbox, phrase, tokens_positive}]}]` (K = 6, gồm cả L1 và L2) + `conversations` (L2) + `region_captions`.
- `val_vg_cap.jsonl`, `test_vg_cap.jsonl` cho đánh giá grounding câu tự nhiên (mục 7).
- Báo cáo: số caption khác nhau / ảnh, phân bố độ dài token, tỉ lệ lint pass, 30 ví dụ ngẫu nhiên để duyệt tay.

**Xong khi**: lint pass 100%, duyệt tay 50 caption không thấy sai thuộc tính rõ ràng, unit test xanh.

---

## 4. PHA 3 — LOADER & PIPELINE CHO CAPTION · ~1.5 ngày

1. **Chọn biến thể ngẫu nhiên mỗi lần load**: `ODVGDataset` giữ toàn bộ `variants`; transform mới `RandomCaptionVariant` (đặt **sau** `RandomFlip`) chọn 1 biến thể, dùng `flip_caption` nếu ảnh đã lật.
2. **Negative cho VG mode** (hoàn thiện `# TODO: add neg` trong `vg_aug`): nối thêm `" . ".join(lớp âm)` sau caption, lấy mẫu từ label map, không trùng lớp dương, dừng khi chạm 256 token; tokens_positive của lớp dương giữ nguyên offset.
3. **Pipeline VG**: flip có, **không** RandomCrop (crop làm sai từ vị trí); resize đa tỉ lệ giữ nguyên.
4. **Trộn dữ liệu**: `ConcatDataset[OD (train_od_rfs), VG (train_vg_cap)]`, tỉ lệ mặc định 1:1 (cấu hình được).
5. Mở rộng `dryrun` (`/tmp/capaudit/dryrun_b1.py` → `scripts/vifood54/dryrun.py`): kiểm span sau `lower()`, kiểm caption flip khớp hướng box, đếm token.

**Xong khi**: dry-run 500 mẫu mỗi dataset 0 lỗi, smoke train 40 iter chạy end-to-end.

---

## 5. ~~PHA 4 — THUỘC TÍNH THEO ẢNH BẰNG VLM~~ — ĐÃ BỎ

Xem mục 9. Attribute bank theo lớp + bố cục từ box GT đã đủ cho caption đúng và không cần thêm run.

---

## 6. PHA 5 — BẬT LMM (đúng thiết kế LLMDet) · ~2 ngày · **chỉ chạy nếu B3 > B1**

- Config `lmm=lmm_path` (Qwen2-0.5B); `conversations` = caption L2; region caption = mức "Vùng"; `num_region_caption` 8–16.
- Kiểm tra bộ nhớ RTX 3090: batch 1, `accumulative_counts=4`, `with_cp=True`; nếu OOM giảm `num_region_caption`, `lmm_max_token_length`.
- Qwen tokenizer giữ dấu tiếng Việt → caption dài vào loss nguyên vẹn (khác BERT).
- So sánh với B3 cùng số iter. Nếu B3 không hơn B1 thì bỏ cả pha này (caption không giúp thì LMM học caption cũng khó giúp).

---

## 7. ĐÁNH GIÁ BỔ SUNG

1. **Closed-set**: mAP/AP50/AP75 + AP theo lớp trên test (54 lớp, prompt đầy đủ).
2. **Open-vocabulary** (để được nói "OV" trong luận văn):
   - Thêm `--novel-classes` vào `build_vifood54.py`: chọn ~8 lớp novel (tần suất trung bình, nhìn khác biệt, ví dụ `cao lầu, bánh pía, ốc, quẩy, súp cua, cơm tấm, nem chua, bánh giò` — chốt sau khi xem B1 per-class), bỏ box + tên của chúng khỏi train, giữ ảnh.
   - Báo cáo AP_base / AP_novel riêng: **chỉ 1 run** với cấu hình tốt nhất (B1 hoặc B3) trên split novel, so với B0 (không cần train).
3. **Grounding câu tự nhiên** (chỉ inference, không train): trên `test_vg_cap.jsonl`, đưa caption L1/L2 làm prompt cho B0/B1/B3, đo Recall@1 (IoU 0.5) theo từng cụm tên món.
5. **Caption hương vị vs hình thái** (thay cho run B3-taste, chỉ inference): dùng checkpoint B3, prompt cùng ảnh bằng caption hình thái và caption có từ hương vị, so Recall@1 → đủ minh họa model không dựa được vào từ hương vị.
4. **Nhầm lẫn**: ma trận nhầm và các cặp ở Pha 1.

---

## 8. MA TRẬN THÍ NGHIỆM — RÚT GỌN (cùng split, cùng test)

Chỉ còn **3 run train mới** sau B1 (B3, OV, và B5 nếu có điều kiện), khoảng 6–9 giờ GPU.

| ID | Câu hỏi luận văn trả lời | Config | Điều kiện chạy | Trạng thái |
| :--- | :--- | :--- | :--- | :---: |
| B0 | Mốc zero-shot | checkpoint gốc, không train | — | ✅ 0.015 |
| B1 | Thêm negative (OD mode) có sửa được lỗi gốc không? | `..._vifood54_b1_od.py` | — | ✅ test 0.310 |
| B1-v2 | Sửa nhãn (crops_review) có giúp không? Cùng config B1, nhãn mới, cùng split | `..._vifood54_b1_od.py` → `work_dirs/vifood54_b1_od_v2` | — | ✅ test 0.315 (B1 cũ trên test mới cũng 0.315) |
| B3 | Caption hình thái + bố cục (L1+L2 trộn, biến thể ngẫu nhiên) có giúp thêm không? | `..._b3_od_vg.py` → `work_dirs/vifood54_b3_od_vg` | so với B1-v2 | ⚖️ mAP 0.220 < 0.315 nhưng grounding câu L2 R@1 0.774 vs B1-v2 0.363 (`EVAL_GROUNDING.md`) |
| B3b | Fine-tune từ B1-v2 bằng OD+VG: giữ mAP mà vẫn có grounding câu? | `..._b3b_ft.py` → `work_dirs/vifood54_b3b_ft` (8k iter, lr 2e-5) | sau grounding test | ✅ **tốt nhất**: test mAP 0.323 (B1-v2 0.315), grounding L2 R@1 0.663 (B1-v2 0.363, B3 0.774); best iter 6000, run dừng ở 7550/8000 do lỗi CIFS "Too many open files" |
| B5 | Giám sát LLM (caption ảnh VLM đã duyệt + caption vùng) có giúp thêm không? | `..._b5_lmm.py` (= B3b + lmm) | **cổng cũ "chỉ khi B3 > B1" đã bỏ (05/11)** — đây là thành phần cốt lõi của LLMDet; so với B3b | ⬜ code xong, chờ caption (`sessions/2026-11-05_phase5_lmm_setup.md`) |
| B0-LLMDet / B1-L | Checkpoint LLMDet (GroundingCap-1M) có tốt hơn MM-GDINO? | `run_llmdet_base.sh` | — | ⬜ |
| OV-W | Tên món novel chỉ có trong caption (không box) có giúp nhận món mới? | `..._ov_s2_lmm.py` (+ `_nonovel`) | sau caption | ⬜ |
| OV | Có tổng quát sang món chưa thấy không? | `..._ov_s1_od.py` (16k, base) → `..._ov_s2_od_vg.py` (8k, như B3b); split `annotations_ov/` | sau B3b | ✅ AP_novel: vi 0.048, en 0.082 (tốt nhất), mô tả 0.021; caption (S2) không giúp OV; B0 0.010, trần trên 0.419 (`EVAL_OV.md`, `EVAL_OV_PROMPTS.md`) |

Inference-only (không tốn train): per-class + nhầm lẫn cho B0/B1/B3, grounding câu tự nhiên, caption hương vị vs hình thái.

---

## 9. ĐÃ BỎ ĐỂ TIẾT KIỆM TÀI NGUYÊN

| Bỏ | Lý do |
| :--- | :--- |
| B1a (bỏ cân bằng lớp) | Ablation phụ, không đổi kết luận chính; per-class của B1 đã cho thấy lớp hiếm có học được không |
| B2 (chỉ caption L1) | Gộp vào B3: L1 và L2 cùng là biến thể caption, tách ra chỉ tốn thêm 1 run |
| B3-taste (train với caption hương vị) | Thay bằng phép so sánh inference ở mục 7.5 |
| B4 + Pha 4 (VLM sinh thuộc tính) | Tốn API/GPU + duyệt tay; attribute bank + bố cục GT đã đủ |
| B6 (alias tiếng Anh) | Không thuộc câu hỏi chính (caption tiếng Việt); có thể đo nhanh bằng inference đổi prompt nếu cần |
| Smoke train nhiều lần | Chỉ dry-run dataloader (vài phút CPU) + 1 smoke 40 iter cho mỗi config mới |

---

## 10. PHA 6 — CẬP NHẬT DEMO & DINH DƯỠNG · ✅ XONG 03/11 (`app_vifood54.py`, cổng 7862; xem `sessions/2026-11-03_phase6_app_vifood54.md`)

- `nutrition_vifood_51.json` → `nutrition_vifood54.json`: đổi tên (`bún→bún tươi`, `nước chấm→đồ chấm`, `chả→chả giò`, `xôi xéo→xôi`, `canh chua→canh`), thêm `nem rán`, `quẩy`, `món tráng miệng`.
- `vlm_discovery.py`: `CANONICAL_51_DISHES` → đọc từ `taxonomy.json`.
- `app.py`: checkpoint B-tốt-nhất, prompt 54 lớp, bảng kết quả mới, đổi chữ "51 món".

---

## 11. PHA 7 — LUẬN VĂN

- Chương 3: quy trình ViFood-54 (gộp nguồn, nhóm ảnh gốc, split theo nhóm, cân bằng lớp), lý do không gộp `chả giò`/`nem rán`.
- Chương 4: bảng mục 8 (+ lý do bỏ ở mục 9), per-class, ma trận nhầm, OV, phân tích lỗi pipeline cũ (thiếu negative, caption mồ côi, BERT bỏ dấu) như một đóng góp phương pháp.

---

## 12. LỊCH ĐỀ XUẤT (rút gọn)

| Ngày | Việc | GPU |
| :--- | :--- | :--- |
| 28/10 | Pha 1: test + phân tích B1, chốt `max_iter` cho run sau; bắt đầu attribute bank | inference |
| 29–30/10 | Pha 2 (builder, layout, lint, unit test) | rảnh |
| 31/10 | Pha 3 (loader, negative VG, trộn dữ liệu) → chạy B3 qua đêm | B3 |
| 01/11 | Phân tích B3 + inference grounding/hương vị; build split OV → chạy OV | OV |
| 02–03/11 | Nếu B3 > B1: Pha 5 (LMM) → B5; nếu không: bỏ, sang Pha 6 | B5? |
| 04/11 | Pha 6 (app, dinh dưỡng) | — |
| 05/11 → | Pha 7 (viết) | — |

---

## 13. RỦI RO & CÁCH XỬ LÝ

| Rủi ro | Xử lý |
| :--- | :--- |
| B1 không tăng mAP | Dừng ở cổng Pha 1, debug theo checklist mục 2 |
| `chả giò` / `nem rán` khó phân biệt (ít ảnh `nem rán`: 62 train) | Thuộc tính phân biệt trong attribute bank; theo dõi cặp nhầm; cân nhắc gán nhãn thêm |
| Prompt vượt 256 token khi thêm caption + negative | Ngân sách token trong `vg_aug`; giảm số negative trước, không cắt caption |
| LMM OOM trên 3090 | batch 1 + accumulate, giảm region caption, giữ `with_cp`; nếu vẫn OOM thì bỏ B5 |
| Caption sai thuộc tính so với ảnh thật | Thuộc tính chung theo lớp chỉ dùng mô tả ổn định ở mọi ảnh của lớp đó; chi tiết riêng từng ảnh chỉ lấy từ box GT (vị trí, kích thước, số lượng) |
| GPU dùng chung (app chiếm ~3.5 GB) | Kiểm tra VRAM trước mỗi run; app không chạy khi train LMM |
