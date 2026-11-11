# 09/11/2026 — Chuyển pipeline sang tiếng Anh (prompt BERT + caption) và gộp nhánh Pha 5

## Vì sao
`bert-base-uncased` của Grounding DINO bỏ dấu và cắt tên tiếng Việt thành mảnh vô nghĩa: `bánh xèo` → `ban ##h x ##eo`,
`cá chiên` → `ca chi ##en`, `cá`/`cà` cùng thành `ca`, `của` → `cu ##a` (trùng lớp `cua`). 46/54 tên Việt bị cắt subword,
tên Anh 22/54 và là từ BERT đã gặp lúc tiền huấn luyện. Bộ tiếng Việt giữ nguyên làm đối chứng (B1-v2, B3b).

## Dữ liệu tiếng Anh (`grounding_data/vifood54/annotations_en/`)
- `scripts/vifood54/captions/en_names.py`: `PROMPT_EN` (54 tên, chọn sao cho không tên nào là chuỗi token con của tên khác:
  `cua` → `whole crab`, `bánh chưng` → `square rice cake`, `thịt bò` → `sliced beef`, `canh` → `clear vegetable soup`,
  `chả giò` (giò lụa) → `vietnamese pork ham`), `UNIT_EN` (lượng từ số ít/số nhiều), `VISUAL_EN` (dịch tay 54 định nghĩa +
  208 thuộc tính, cùng thứ tự với bản Việt). Dịch tay vì cache HF lại bị dọn 09/11 14:19, mất trọng số Gemma.
- `scripts/vifood54/make_en_data.py`: cùng ảnh/box/id lớp/split/RFS/class dropout; đổi `label_map`, `category`,
  `instances_{val,test}.json`, `taxonomy.json` (name EN, `name_vi`, confusable EN).
- `scripts/vifood54/captions/builder_en.py` + `build_captions_en.py`: cùng bố cục L1/L2, 6 biến thể, seed, lint trên token
  BERT (`lint.py` nhận danh sách từ hương vị EN). **Ảnh train dùng thuộc tính VLM đã xác nhận** (vlm_attrs shard 0+1) thay
  thuộc tính mặc định: giữ 17425/26699; 45 lượt lớp-ảnh không còn thuộc tính. Val/test dùng thuộc tính taxonomy.
  Kết quả: 0 biến thể lỗi lint, token L2 TB 51 / p95 112 / max 160 (`CAPTION_REPORT_EN.md`).
- `make_lmm_data.py --od/--vg/--out` → `annotations_en/train_od_rfs_lmm.jsonl` (caption ảnh EN cho loss LMM).
- Chưa có: 3052 đặc điểm VLM tự thêm (`extra`) chưa dịch — `captions/translate_en.py` (Gemma, chỉ văn bản) sẵn sàng,
  cần tải lại Gemma.

## Gộp nhánh `truong/phase5-lmm` (commit 3d5cd26, fast-forward, chưa push)
- Thay đổi cục bộ cất ở `git stash` ("local truoc khi pull phase5-lmm") và `/tmp/merge_backup_phase5/`.
- `text_transformers.py`: lấy bản của nhánh (chọn region sau aug, đích vùng OD = tên lớp từ label map). Bản cục bộ cũ
  (đích vùng = region caption) bỏ. `PLAN_VIFOOD54.md`: bản nhánh + dòng ghi chú app 03/11.
- `configs/..._b5_lmm.py`: lấy bản nhánh (num_region 8, lmm lr ×5, batch 1 × 4, 8k iter). Config B5 cục bộ cũ (16k iter)
  ở `/tmp/merge_backup_phase5/b5_lmm_local_moved.py`; bản đã chạy dở (iter 2900) còn trong `work_dirs/vifood54_b5_lmm/`.
- Lưu ý: B5 của nhánh = 8000 iter × batch 1 = 8k mẫu, B3b = 8000 × batch 2 = 16k mẫu → đã sửa thành 16k iter (mục "Rà code").

## Config + chạy
| Run | Config | Khởi tạo | So với |
| :--- | :--- | :--- | :--- |
| B1-EN | `..._b1_od_en.py` | MM-GDINO (như B1-v2) | B1-v2 (test 0.315) |
| B3b-EN | `..._b3b_ft_en.py` | B1-EN best | B3b (0.323, grounding L2 R@1 0.663) |
| B5-EN | `..._b5_lmm_en.py` (= B5 Pha 5 + EN) | B1-EN best | B3b-EN; VRAM đo ở mục "Rà code" bên dưới |

```bash
tmux attach -t vifood54_en   # log: llmdet_vietnamese_food/work_dirs/vifood54_en_pipeline.log
RUN_B5=1 bash scripts/vifood54/run_en.sh   # khi GPU rảnh: bỏ qua bước đã xong, chạy thêm B5-EN
```
`run_en.sh`: train → (B5: `strip_lmm.py`) → test bằng config B1-EN → `eval_grounding.py --lang en` (cụm hương vị EN cho
L2_taste) → `analyze_eval.py` trên GT EN, đặt cạnh preds VI (cùng id lớp) → `EVAL_EN.md`, `EVAL_GROUNDING_EN.md`.

Bắt đầu 09/11 23:15 (B1-EN ~4 h, B3b-EN ~2 h). Iter 50: loss 35.3 (B1-v2 tiếng Việt cùng iter: 40.7); `grad_norm nan`
ở 100 iter đầu giống B1-v2 (AMP dò loss scale).

## Tải mô hình (user đồng ý 09/11 23:25)
- Tải vào `huggingface/` trên ổ mạng (gitignore) thay vì `~/.cache` — cache HF đã bị dọn 2 lần:
  `huggingface/gemma-4-12B-it/` (23.9 GB, ~100 MB/s) và `huggingface/llmdet/tiny.pth` (LLMDet Swin-T, 2.26 GB; chỉ file này,
  không tải cả repo ~13 GB). Script dùng `--model huggingface/gemma-4-12B-it` + `HF_HUB_OFFLINE=1`.
- `strip_lmm.py tiny.pth -> llmdet_swin_t_det.pth`: giữ 908 khóa, bỏ 722 (`lmm` 705, connector, region_connector,
  ref_point_head, image_seperate). Nạp vào config B1-EN: thiếu 0, thừa 0, lệch shape 0.

## Caption VLM tiếng Anh cho loss LMM (`vlm_captions.py` của Pha 5)
- `VIFOOD_LANG=en` cho generate / review_captions.py / attach: đọc ghi trong `annotations_en/`, prompt EN, vị trí theo
  `builder_en.location_en`, lọc câu suy đoán / hương vị EN (bỏ `warm`/`cold` vì "warm lighting" hợp lệ), chỉ khớp tên EN
  (aliases trong taxonomy là tên Việt). `attach` chạy được khi chưa có caption VLM (mọi ảnh dùng template L2); `--ov` bị
  chặn ở EN (chưa có bộ OV tiếng Anh).
- Hiện `annotations_en/train_{od_rfs,vg_cap_rfs}_lmm.jsonl` = template L2 EN (4164 dòng mỗi file); B5-EN đọc 2 file này.

## Hàng đợi GPU (`scripts/vifood54/run_en_queue.sh`, tmux `vifood54_en_queue`)
1. chờ `vifood54_en` (B1-EN → B3b-EN → đánh giá) xong;
2. `run_llmdet_base_en.sh`: B0-LLMDet-EN (zero-shot) + B1-L-EN (B1-EN khởi tạo LLMDet, 16k iter) → `EVAL_LLMDET_BASE_EN.md`;
3. `translate_en.py` (Gemma, chỉ văn bản): 3052 đặc điểm VLM → `annotations_en/translations_vi_en.json`; KHÔNG tự build
   lại caption (B3b-EN đã train với caption hiện tại);
4. `VIFOOD_LANG=en vlm_captions.py generate` (~7 h) → `annotations_en/vlm_captions.jsonl`.
Log `llmdet_vietnamese_food/work_dirs/vifood54_en_queue.log`. Gemma chưa chạy thử được trên GPU (chỉ còn ~7 GB trống lúc
B1-EN train) — lỗi nạp model sẽ hiện ở bước 3.

## Rà code nhánh Pha 5 + giảm VRAM B5 (09/11 tối)
Ổn: chọn region sau aug (box_index trỏ đúng gt cuối, OD lấy tên theo class id gốc); xử lý batch không có region;
`strip_lmm.py` (LLMDet tiny: 908 khóa khớp 100%); `vlm_captions.py` lọc/gắn cờ/attach; region conversation ≤ 39 token
(cắt ở 40 trong grounding_dino — sát giới hạn, tên dài hơn sẽ mất token nhãn).

Lỗi đã sửa:
1. **LMM không hề được checkpoint**: `checkpoint_wrapper(self.lmm)` chỉ bọc `forward()`, còn loss gọi
   `lmm.detection_forward()`; checkpoint từng lớp của Qwen2 chỉ bật khi `self.training`, mà loss gọi `lmm.eval()`.
   Thêm 2 cờ (mặc định tắt, config khác không đổi):
   - `lmm_grad_ckpt=True`: checkpoint từng lớp Qwen2 cả khi eval (`modeling_qwen2.py`: `checkpoint_in_eval`, non-reentrant);
   - `lmm_sparse_logits=True`: chỉ tính `lm_head` ở token có nhãn thay vì cả ~1300 token (logits fp32 × 151936 từ vựng).
   Đo riêng loss caption ảnh (1 ảnh, 162 token chữ + 1130 token ảnh, fp16, GPU dùng chung còn ~6 GB):
   | Cờ | VRAM thêm |
   | :--- | ---: |
   | cũ (không cờ) | OOM (> ~6 GB) |
   | chỉ logits thưa | ~2.8 GB |
   | chỉ checkpoint | ~3.1–3.6 GB |
   | cả hai | ~0.5–2.2 GB |
   Tương đương: fp32 loss y hệt, grad lệch 1.4e-5; fp16 lệch 0.76% (làm tròn do kích thước matmul khác).
   Script: `/tmp/b5mem/lmm_mem_test.py` (đo), `/tmp/b5mem/lmm_fp32_test.py` (tương đương). Bản gốc 2 file sửa:
   `/tmp/merge_backup_phase5/{modeling_qwen2,grounding_dino}.py.orig`.
2. **B5 / OV-W chỉ thấy nửa số mẫu so với B3b / OV-S2**: đổi batch 2×2 -> 1×4 nhưng giữ 8000 iter (= 8k mẫu, 2000 bước
   cập nhật thay vì 16k mẫu, 4000 bước). `..._b5_lmm.py`, `..._ov_s2_lmm.py` (+ nonovel, B5-EN kế thừa): 16000 iter,
   warmup 400, milestones 12000/15000, val/checkpoint mỗi 2000; `run_lmm.sh` chờ `iter_16000.pth`. `run_en.sh` đang chạy
   nên hàng đợi tự sửa mốc B5-EN 8000 -> 16000 sau khi nó xong.
3. `review_captions.py` vẽ nhãn box tiếng Việt cả khi `VIFOOD_LANG=en` -> đọc `train_od.jsonl` theo `ANN`.

VRAM thật của cả B5: lần chạy B5 cục bộ trước (batch 1, 16 region, KHÔNG có 2 cờ) đã chỉ ~12.8 GB max_allocated —
con số "~20 GB" trong ghi chú Pha 5 là của batch 2. Với 2 cờ còn thấp hơn; hàng đợi đo thật 40 iter batch 1 và batch 2
ngay sau khi `vifood54_en` xong -> `llmdet_vietnamese_food/work_dirs/vifood54_b5_en_probe.txt`. Nếu batch 2 vừa: có thể
chạy B5 đúng lịch B3b (batch 2 × 2, 8000 iter).

## Rà lại caption EN (10/11, trước khi B3b-EN dùng tới)
- Tự động: 47 472 caption (gồm bản lật) — span khớp tên lớp, đủ lớp GT, 0 lỗi lint.
- Lỗi ý nghĩa tìm được (có cả ở bản VI): lượng từ chọn ngẫu nhiên nên mâu thuẫn thuộc tính dụng cụ
  ("a **basket** of fresh herbs and greens, piled to fill the **plate**", "a small bowl of rice vermicelli, served
  separately on a plate"). Sửa trong `builder_en.py` / `build_captions_en.py`:
  - ảnh train, lớp có 1 box: lượng từ = dụng cụ VLM thấy (`container`: đĩa→plate, tô/bát→bowl, chén→small bowl, rổ→basket,
    mẹt→bamboo tray, khay→tray, nồi→pot; `lá`/`không rõ` giữ taxonomy). Lớp nhiều box giữ lượng từ số nhiều taxonomy —
    bản đầu áp cho cả nhiều box sinh "five plates of cylindrical rice cake" (5 khoanh trên cùng 1 đĩa) nên đã bỏ;
  - mọi split: bỏ thuộc tính dụng cụ (on/in/to fill the plate|bowl|..., bamboo tray..., metal pot) khác dụng cụ của lượng từ.
  Sau sửa: 0 mâu thuẫn; token L2 TB 51 / p95 113 / max 160; `train_{od_rfs,vg_cap_rfs}_lmm.jsonl` gắn lại.
- Còn lại (không đổi so với VI, giữ so sánh công bằng): val/test dùng thuộc tính taxonomy, gồm cả thuộc tính VLM hay loại;
  vài cụm hơi gượng ("a serving of other dish", "a pot of hotpot", "bowls of grilled pork noodle bowl") do tên lớp đã cố định
  khi B1-EN train. 208 thuộc tính dịch tay (`en_names.VISUAL_EN`) chưa có người đọc duyệt.

- Soát lại bản dịch tay (10/11, `annotations_en/TRANSLATION_REVIEW.md`), sửa 8 chỗ lệch nghĩa: bánh khọt `điểm nhân` ->
  "dotted with orange-pink topping"; bánh pía "flaky" (kết cấu) -> "layered", bỏ "salted" (VI chỉ nói lòng đỏ trứng);
  bánh đúc "smooth ... block" trùng "smooth" của thuộc tính khác -> "green or white rice-flour block"; cơm chiên
  "red carrots" -> "diced orange carrots"; ngao sò "two-part" -> "bivalve" (thuộc tính + định nghĩa); rau sống `xếp đầy kín`
  "piled to fill the plate" (VI không nói đĩa, gây mâu thuẫn dụng cụ) -> "densely piled"; xôi `đắp thành đĩa hoặc nắm`
  "shaped as a mound or ball" -> "heaped on a plate or pressed into a ball". Dựng lại taxonomy EN (chỉ chép
  `taxonomy.json`, không ghi đè file B1-EN đang đọc), caption, `*_lmm.jsonl`: 0 lỗi lint.

## Việc còn lại
- Duyệt tay caption VLM EN: `VIFOOD_LANG=en python scripts/vifood54/captions/review_captions.py --reviewer <tên>`, rồi
  `VIFOOD_LANG=en vlm_captions.py attach`, rồi `RUN_B5=1 bash scripts/vifood54/run_en.sh` (~20 GB VRAM, tắt app).
- Nếu B1-L-EN > B1-EN: chạy lại B3b-EN/B5-EN từ B1-L-EN (`--cfg-options load_from=...`).
- Thuộc tính taxonomy bị VLM loại ≥89% (xem `2026-11-03_vlm_attrs_shard.md`) vẫn nằm trong caption val/test.
- OV tiếng Anh (OV-W) chưa có bộ dữ liệu `annotations_ov` bản EN.

## Kết quả B1-EN (2026-11-10)

- Val mAP theo 2k iter: 0.197 → 0.289 → 0.343 → 0.366 → 0.389 → 0.404 → 0.405 → 0.406 (best iter 16000).
- **Test: mAP 0.384 / AP50 0.475 / AR@100 0.827**, so với B1-v2 tiếng Việt 0.315 / 0.394 / 0.808 (+6.9 điểm mAP; cùng ảnh, box, split, lịch train). Hơn cả B3b VI (0.323).
- Theo lớp: 35/54 lớp tăng >1 điểm, 15 lớp giảm. Tăng mạnh: whole crab +0.44, pho +0.36, shredded salad +0.32, stir-fried vegetables +0.27, hotpot +0.23. Giảm: crab soup −0.18, rice paper −0.12 (lớp ~10–30 box test, nhiễu lớn).
- Cặp dính chữ ở bản VI giảm bỏ sót rõ: quẩy 11/12 → 3/12, cao lầu 22/29 → 6/29, cua 8/11 → 4/11. Cặp giống hình (bánh căn/khọt, chả giò/nem rán) vẫn khó như cũ.
- Chi tiết: `grounding_data/vifood54/EVAL_B1_EN_VS_VI.md`.

### Sự cố 03:20–07:43 (GPU đứng không ~4,4 h)
- `run_en.sh` bị sửa lúc 23:28 khi bash đang đọc dở → lỗi cú pháp ngay sau B1, B3b-EN không chạy.
- `run_en_queue.sh` chờ bằng `tmux has-session -t vifood54_en`, khớp tiền tố với chính `vifood54_en_queue` → chờ mãi. Sửa thành `-t =vifood54_en` (khớp đúng tên); bỏ bước sed, đặt luôn B5 16000 iter trong `run_en.sh`.
- `analyze_eval.py`: WATCH_PAIRS viết theo tên VI → KeyError với GT tiếng Anh; thêm tra qua `en_names.PROMPT_EN`.
- Chạy lại 07:43: B3b-EN (8000 iter, ~1,5 h) → đánh giá; hàng đợi chạy tiếp sau đó.

## Kết quả B3b-EN (2026-11-10)

Chạy trong tmux `training` (07:55 → 10:56), 8000 iter từ B1-EN; best val 0.411 @ iter 7000 (B1-EN 0.406).

| Mô hình | test mAP | AP50 | names R@1 | L1 R@1 | L2 R@1 | L2_taste R@1 |
|---|---|---|---|---|---|---|
| B1-v2 VI | 0.315 | 0.394 | 0.851 | 0.366 | 0.363 | 0.360 |
| B3 VI | – | – | 0.813 | 0.718 | 0.774 | 0.775 |
| B3b VI | 0.323 | 0.405 | 0.843 | 0.582 | 0.663 | 0.652 |
| B1-EN | 0.384 | 0.475 | 0.860 | 0.716 | 0.612 | 0.641 |
| B3b-EN | 0.387 | 0.484 | 0.859 | 0.808 | 0.830 | 0.827 |

- B3b-EN giữ mAP của B1-EN (+0.003) và tên lớp (R@1 0.859), đồng thời grounding câu L2 tăng từ 0.612 lên 0.830 — tốt nhất từ trước tới giờ, vượt cả B3 VI (0.774, vốn phải đánh đổi mAP/names).
- Lớp tụt L2 so với B1-EN: broken rice 0.77→0.52, boiled chicken 0.61→0.42, clams and scallops 0.46→0.39.
- Nhầm mới nổi ở B3b-EN: quang↔cao lau (9 + 6 box), thick noodle soup→crab noodle soup 58%, hue beef→crab noodle soup 30%.
- Báo cáo: `grounding_data/vifood54/EVAL_EN.md`, `EVAL_GROUNDING_EN.md`.

## Caption LMM tiếng Anh cho B5-EN (2026-11-10 tối)
- Dừng `vlm_captions.py generate` EN (17 s/ảnh → ~16 h); 35 ảnh đã sinh cất ở `annotations_en/vlm_captions_aborted35.jsonl.bak`
  (để `attach` không dùng nhầm). Không có caption đoạn văn VI do Gemma viết: nhánh `vifood54-pipeline` chỉ chạy
  `vlm_attrs.py` (thuộc tính theo box). `truong/phase5-lmm` không có commit mới, đã nằm trong `main`.
- `translate_en.py --skip-taxonomy` (cờ mới; taxonomy đã dịch tay): 3052/3052 cụm `extra` → `translations_vi_en.json`,
  0 lỗi, ~45 phút, Gemma 4-bit 8.6 GB.
- `captions/build_lmm_en.py` (mới): dựng caption ở thư mục tạm, chỉ thay `conversations` + `region_captions` của
  `train_{od_rfs,vg_cap_rfs}_lmm.jsonl`; `grounding`/box giữ nguyên dữ liệu B3b-EN (đã so). 6977 lượt lớp-ảnh, thêm 11534
  đặc điểm VLM, 223 cụm bị lint loại. Bản template cũ: `*_lmm.jsonl.bak_template`. Báo cáo `CAPTION_REPORT_LMM_EN.md`.
  Caption không dài hơn (TB 40 từ, cũ 42): builder vẫn bốc 1–2 thuộc tính/món theo ngân sách 160 token BERT.
- `run_en.sh`: bỏ `vlm_captions.py attach` (ghi đè *_lmm.jsonl) → `build_lmm_en.py` nếu chưa dựng.
- Probe B5-EN 40 iter batch 1: max_memory_allocated 6.5 GB, 1.2 s/iter, `loss_lmm_image` 3.05, `loss_lmm_region` 1.62,
  val mAP iter 40 = 0.406 (= B1-EN). 16000 iter ≈ 5.5–6 h. Log `work_dirs/vifood54_b5_en_probe_bs1.log.txt`.
