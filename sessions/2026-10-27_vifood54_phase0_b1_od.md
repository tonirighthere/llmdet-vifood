# NHẬT KÝ PHIÊN LÀM VIỆC: 27/10/2026
## Chủ đề: Pha 0 — Chuẩn hóa ViFood-54 & Thí nghiệm B1 (OD mode có negative)

---

### 1. Lý do
Rà soát pipeline cũ cho thấy mọi thí nghiệm (Exp1–Exp4) đều train ở **VG mode không có negative**
(`label_map_file=None`, `vg_aug` còn `# TODO: add neg`): prompt train chỉ chứa món có trong ảnh,
trong khi prompt test chứa toàn bộ class → AR cao (0.56) nhưng mAP thấp (~0.05).
B1 kiểm chứng giả thuyết này bằng OD mode: prompt = lớp dương + lớp âm lấy mẫu từ label map.

### 2. Dữ liệu ViFood-54 (`scripts/vifood54/build_vifood54.py`)
- Nguồn: `zip/vifood.zip` (ảnh từ `zip/images.zip`, giải nén vào `grounding_data/vifood54/images/vifood/`)
  + `zip/vifood2999.zip` (ảnh ở `vifood_2999_extracted/`). Ảnh không có file label bị bỏ
  (24 ảnh trong images.zip), ảnh có file label rỗng bị bỏ (22 ảnh vifood2999).
- Taxonomy (`scripts/vifood54/taxonomy.json`): **54 class**, id class = id trong `obj.names`.
  `chả giò` và `nem rán` là **2 món khác nhau, không gộp** (bản đầu có gộp, đã bỏ theo yêu cầu).
- 3956 ảnh, 18 253 box, **3204 ảnh gốc** (gộp bản augment Roboflow `*.rf.<hash>` + 169 cặp gần trùng dHash).
- Split theo ảnh gốc, phân tầng theo lớp (seed 2026): **train 3138 / val 404 / test 414**, không rò rỉ group.
- Cân bằng lớp:
  - Lớp hiếm: repeat factor sampling r(c)=max(1, √(0.05/f(c))), làm tròn ngẫu nhiên → `train_od_rfs.jsonl` 4142 mẫu/epoch
    (lẩu ×2.25, bún mắm ×1.79, nem rán ×1.59...). Không dùng `ClassBalancedDataset` của mmengine vì nó làm tròn lên (1.01 → 2).
  - Lớp đầu: `đồ chấm` (1294 ảnh) và `rau sống` (1030) luôn đi kèm món khác nên bỏ ảnh chỉ loại được 3 ảnh.
    Thay bằng **class dropout** (`class_drop.json`): mỗi mẫu bỏ lớp đó khỏi giám sát (box + tên trong prompt)
    với p = 0.77 / 0.694 → ~400 ảnh hiệu dụng/epoch, không sinh negative sai.
  - Augment vị trí: RandomFlip + RandomChoice(resize đa tỉ lệ | resize + RandomCrop + resize).
- Báo cáo đầy đủ theo lớp: `grounding_data/vifood54/BUILD_REPORT.md`.

### 3. Thay đổi code
- `mmdet/datasets/transforms/text_transformers.py` (`RandomSamplingNegPos2`):
  - tham số `class_drop_file`; lớp bị drop không được lấy làm negative trong cùng mẫu;
  - copy label map trước khi chọn alias `a/b` (hiện chưa lớp nào có alias);
  - cắt `gt_ignore_flags` khi box bị bỏ (lỗi tiềm ẩn có sẵn: `check_for_positive_overflow` bỏ box nhưng không cắt cờ).
- Config: `configs/grounding_dino_swin_t_vifood54_b1_od.py` (OD mode, val mỗi 2000 iter, lưu best `coco/bbox_mAP`, CocoMetric classwise).

### 4. Kiểm tra
- Dry-run 300 mẫu: 0 lỗi span; prompt 11–224 token (TB 165, giới hạn 256); TB 1.7 lớp dương / 38 lớp âm mỗi prompt.
- Smoke train 40 iter + val: chạy end-to-end, 0.69 s/iter, ~5 GB VRAM; `grad_norm: nan` ở iter đầu là do AMP dò loss scale (Exp4 cũng vậy).
- **B0 zero-shot trên test ViFood-54 (54 class)**: mAP 0.015 | AP50 0.019 | AP75 0.016.

### 5. Trạng thái Hoàn thành
- **Hoàn tất**: 03:13:00 ngày 28/10/2026 (đủ 16,000 / 16,000 iters).
- **Kết quả**: Best val `bbox_mAP` = **0.3470** (mAP@50 = 0.4260, mAP@75 = 0.3880) tại iter 16,000 (gấp 7 lần Exp4 cũ và gấp 23 lần B0 zero-shot).
- **Checkpoint lưu trữ**: `llmdet_vietnamese_food/work_dirs/vifood54_b1_od/best_coco_bbox_mAP_iter_16000.pth`.
- **Nhật ký chi tiết**: Xem đầy đủ bảng metrics, loss convergence và AP 54 lớp tại [`sessions/2026-10-28_phase1_b1_od_training_completion.md`](file:///home/atin/tuan/SoPSoP/sessions/2026-10-28_phase1_b1_od_training_completion.md).
