_base_ = 'grounding_dino_swin_t_vifood54_b5_lmm_en.py'

# ═══════════════════════════════════════════════════════════════════════
# B5-EN v2 (bước 2): như B5-EN nhưng (a) bắt đầu từ checkpoint đã căn chỉnh connector/LoRA (bước 1),
# (b) ĐÚNG lịch của B3b-EN: batch 2 × tích lũy 2, 8000 iter, mốc lr 6000/7500, val mỗi 1000
# ═══════════════════════════════════════════════════════════════════════
# B5-EN lần 1 chạy batch 1 × 4, 16k iter và được đánh giá ở iter 4000 (4000 mẫu) trong khi B3b-EN ở iter 7000 × batch 2
# (14000 mẫu) -> không so được. Bản này chỉ khác B3b-EN ở 2 loss LLM. VRAM batch 1 đo được 6.5 GB (probe 10/11),
# batch 2 dự kiến ~11-13 GB; nếu OOM: thêm --cfg-options train_dataloader.batch_size=1 optim_wrapper.accumulative_counts=4
# train_cfg.max_iters=16000 (và nhân đôi các mốc).
# run_b5_v2_en.sh đánh giá CẢ checkpoint tốt nhất theo mAP val lẫn checkpoint cuối (iter 8000).

load_from = 'work_dirs/vifood54_b5_align_en/iter_2000.pth'  # detector = B1-EN, connector/LoRA đã căn

train_dataloader = dict(batch_size=2)
optim_wrapper = dict(accumulative_counts=2)

max_iter = 8000
train_cfg = dict(max_iters=max_iter, val_interval=1000)
param_scheduler = [
    dict(type='LinearLR', start_factor=0.01, by_epoch=False, begin=0, end=200),
    dict(type='MultiStepLR', begin=0, end=max_iter, by_epoch=False, milestones=[6000, 7500], gamma=0.1)
]
default_hooks = dict(checkpoint=dict(interval=1000, max_keep_ckpts=1))
