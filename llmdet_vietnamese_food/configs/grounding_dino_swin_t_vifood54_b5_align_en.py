_base_ = 'grounding_dino_swin_t_vifood54_b5_lmm_en.py'

# ═══════════════════════════════════════════════════════════════════════
# B5-EN bước 1 (căn chỉnh, = Step 1 của LLMDet): detector ĐỨNG YÊN, chỉ học phần nối sang LLM
# ═══════════════════════════════════════════════════════════════════════
# Vì sao: mm_projector2.bin được căn với đặc trưng MM-GDINO gốc, còn B1-EN đã fine-tune encoder 16k iter.
# B5-EN lần 1 bắt đầu với loss_lmm_image ≈ 3.0 / region ≈ 1.6 và dồn gradient đó thẳng vào detector
# (val mAP tốt nhất ở iter 4000/16000, các mốc sau không vượt). Paper tách riêng bước này "để ghép LLM mà không phá đặc trưng đã pretrain".
# Ở đây: freeze_detector=True -> chỉ connector, region_connector, LoRA, cross-attn của Qwen2 được cập nhật.
# Detector không đổi nên mAP val = B1-EN; chỉ cần iter_2000.pth làm load_from cho bước 2 (..._b5_lmm_en_v2.py).

model = dict(freeze_detector=True)

train_dataloader = dict(batch_size=2)
optim_wrapper = dict(accumulative_counts=2)  # batch hiệu dụng 4; lr phần LLM = 2e-5 × 5 = 1e-4 (kế thừa)

max_iter = 2000  # × batch 2 = 4000 mẫu ≈ nửa epoch OD+VG
train_cfg = dict(max_iters=max_iter, val_interval=max_iter)
param_scheduler = [
    dict(type='LinearLR', start_factor=0.01, by_epoch=False, begin=0, end=200),
    dict(type='MultiStepLR', begin=0, end=max_iter, by_epoch=False, milestones=[max_iter], gamma=1.0)
]
default_hooks = dict(checkpoint=dict(interval=max_iter, max_keep_ckpts=1))
