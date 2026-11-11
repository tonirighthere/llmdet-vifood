# 05/11 — B5: bật đủ 3 loss của LLMDet (bám paper)

## Vì sao
Các run trước (B1-v2, B3, B3b, OV) đặt `lmm=None`: chỉ có loss grounding của Grounding DINO (focal cls + L1 +
GIoU, ở encoder / 6 lớp decoder / nhánh DN). LLMDet (Fu et al., CVPR 2025) thêm giám sát từ LLM:
- **caption ảnh**: LMM (LLaVA-OneVision Qwen2-0.5B) nhìn feature map p4/p5 của detector qua projector, sinh caption chi tiết;
- **caption vùng**: LMM nhìn query decoder đã khớp với box GT (tối đa 16 box/ảnh), sinh cụm mô tả vùng.
LMM chỉ dùng lúc train, suy luận vẫn là Grounding DINO.

## Có sẵn trong repo
- Code LMM trong `mmdet/models/detectors/grounding_dino.py` (LoRA r128, 6 lớp cross-attn mới, projector `mm_projector2.bin`).
- Weight `huggingface/my_llava-onevision-qwen2-0.5b-ov-2/` + projector đã pretrain của LLMDet.
- Dữ liệu VG đã có `conversations` (caption hình thái ảnh) và `region_captions` (theo lớp).
- Checkpoint LLMDet của tác giả (`fushh7/LLMDet`) KHÔNG có (cache chỉ có thư mục refs, chưa tải).

## Sửa
| File | Thay đổi |
| :--- | :--- |
| `mmdet/datasets/odvg.py` | đọc `region_captions`; VG gắn caption vùng cho từng region theo tên lớp |
| `mmdet/datasets/transforms/text_transformers.py` (`RandomSamplingNegPos2`) | dựng hội thoại vùng SAU `od_aug`/`vg_aug` (trước đây dựng trước aug: class dropout/tràn token bỏ box làm `box_index` lệch; OD mode không có `phrases` nên đích luôn là "object"); OD tra lớp gốc qua `label_remap_dict`; đích = caption vùng, không có thì tên lớp |
| `scripts/vifood54/make_lmm_data.py` | `train_od_rfs_lmm.jsonl`: dòng OD nhận `conversations` + `region_captions` của ảnh đó (trước chỉ là câu liệt kê tên lớp) |
| `configs/..._b5_lmm.py` | kế thừa B3b (từ B1-v2, OD+VG, lr 2e-5), `lmm` bật, `num_region_caption=16` cho cả OD và VG; batch 1 × tích lũy 4 (batch 2 OOM ~19 GB trên 3090 dùng chung), 16k iter = cùng 16k mẫu / 4000 bước cập nhật như B3b, mốc lr 12k/15k, val mỗi 2k |
| `scripts/vifood54/run_b5.sh` | train → test (config B1, bỏ khóa lmm) → grounding (B1-v2/B3b/B5) → mAP so sánh |

Kiểm tra: đích LMM giải mã ra đúng caption ảnh / caption vùng ("Chén đồ chấm, nước màu nâu đỏ hoặc vàng, lát ớt đỏ
nổi trên mặt.") cho cả mẫu OD và VG. Chạy thử 80 bước: `loss_lmm_image` ≈ 5.0, `loss_lmm_region` ≈ 3.9, 0.86 s/bước,
PyTorch đỉnh 12.6 GB.

## Đang chạy
`tmux attach -t vifood54_b5`, log `llmdet_vietnamese_food/work_dirs/vifood54_b5_pipeline.log`, ETA train ~3 h 50 + val.
Kết quả ra `grounding_data/vifood54/EVAL_B5.md`, `EVAL_GROUNDING_B5.md`.

## Khác paper / còn mở
- Caption ảnh của mình là caption template hình thái tiếng Việt (vài câu), paper dùng caption chi tiết do
  Qwen2-VL-72B viết (GroundingCap-1M). Bước tiếp: ghép thuộc tính Gemma 12B (`vlm_attrs`, đã xong nửa đầu) vào
  caption ảnh/vùng → B5 + caption VLM.
- Paper khởi tạo từ MM-GDINO và train trên 1M ảnh; ở đây khởi tạo từ B1-v2 (fine-tune ViFood-54) để so trực tiếp với
  B3b (chỉ khác có/không LMM).
- Có thể thử khởi tạo từ checkpoint LLMDet của tác giả (cần tải `fushh7/LLMDet`).

## Dừng (05/11 ~15:50, theo yêu cầu)
Dừng ở bước ~2900/16000. Còn lại `work_dirs/vifood54_b5_lmm/iter_2000.pth` (= best, val mAP 0.343 / AP50 0.420;
B3b cùng lượng mẫu 0.339). Loss caption lúc dừng: ảnh 1.71, vùng 0.72. Chưa chạy test/grounding.
Chạy tiếp từ checkpoint: `python mmdet_train.py configs/grounding_dino_swin_t_vifood54_b5_lmm.py --work-dir
work_dirs/vifood54_b5_lmm --amp --resume` (run_b5.sh bỏ qua bước train khi đã có best_*.pth → cần chạy tay lệnh này).
