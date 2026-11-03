_base_ = 'grounding_dino_swin_t_vifood54_b3_od_vg.py'

# ═══════════════════════════════════════════════════════════════════════
# B3b: fine-tune tiếp từ B1-v2 bằng OD + VG caption (trộn ~1:1)
# ═══════════════════════════════════════════════════════════════════════
# Kết quả trước (test): B1-v2 mAP 0.315 nhưng grounding câu L2 R@1 0.363; B3 (train từ đầu,
# OD+VG) grounding L2 0.774 nhưng mAP 0.220. B3b bắt đầu từ B1-v2 đã hội tụ OD, thêm 8k bước
# trộn OD + VG để học grounding câu mà vẫn giữ OD (dữ liệu, pipeline, negative giống B3).

load_from = 'work_dirs/vifood54_b1_od_v2/best_coco_bbox_mAP_iter_16000.pth'

max_iter = 8000
train_cfg = dict(max_iters=max_iter, val_interval=1000)
param_scheduler = [
    dict(type='LinearLR', start_factor=0.01, by_epoch=False, begin=0, end=200),
    dict(type='MultiStepLR', begin=0, end=max_iter, by_epoch=False, milestones=[6000, 7500], gamma=0.1)
]
default_hooks = dict(checkpoint=dict(interval=1000))
# lr nhỏ hơn B1 (5e-5) vì bắt đầu từ checkpoint đã hội tụ
optim_wrapper = dict(optimizer=dict(lr=0.00002))
