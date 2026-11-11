_base_ = 'grounding_dino_swin_t_vifood54_ov_s2_od_vg.py'

# ═══════════════════════════════════════════════════════════════════════
# OV-W: open-vocabulary giám sát yếu — lớp novel KHÔNG có box, chỉ có tên trong caption ảnh
# ═══════════════════════════════════════════════════════════════════════
# Như OV giai đoạn 2 (fine-tune từ OV-S1, OD + VG lớp base, 8k iter) + LMM như B5.
# Caption ảnh (vlm_captions.py attach --ov) nhắc cả món novel -> LLM buộc detector mã hóa món novel
# dù không có box (giống LCS trong GroundingCAP-1M). So với OV-S2: cùng box, cùng prompt BERT.
# Ablation: ..._ov_s2_lmm_nonovel.py (bỏ câu có tên novel) để tách tác dụng của tên novel khỏi LMM.
# load_from = checkpoint tốt nhất của OV-S1 (run_lmm.sh truyền qua --cfg-options).

ov_dir = '../grounding_data/vifood54/annotations_ov/'
cap_suffix = '_lmm'
num_region = 8

# lmm_grad_ckpt + lmm_sparse_logits: checkpoint từng lớp Qwen2 + chỉ tính lm_head ở token có nhãn. Cùng loss
# (fp32: lệch grad 1.4e-5), VRAM phần LMM / ảnh từ >5 GB xuống ~0.5-2 GB (đo 09/11, sessions/2026-11-09_english_pipeline.md)
model = dict(lmm=_base_.lmm_path, num_region_caption=num_region, lmm_grad_ckpt=True, lmm_sparse_logits=True)

od_dataset = _base_.od_dataset
od_dataset['ann_file'] = ov_dir + f'train_od_rfs{cap_suffix}.jsonl'
od_dataset['pipeline'][-2]['num_region_caption'] = num_region
# Giữ ảnh chỉ có món novel (không còn box base): không có loss box/region, vẫn có loss caption ảnh
od_dataset['pipeline'][4]['keep_empty'] = False  # FilterAnnotations (Load, Load, Flip, RandomChoice, Filter)
vg_dataset = _base_.vg_dataset
vg_dataset['ann_file'] = ov_dir + f'train_vg_cap_rfs{cap_suffix}.jsonl'
vg_dataset['pipeline'][-2]['num_region_caption'] = num_region

train_dataloader = dict(
    batch_size=1,
    dataset=dict(_delete_=True, type='ConcatDataset', datasets=[od_dataset, vg_dataset]))

optim_wrapper = dict(
    accumulative_counts=4,
    paramwise_cfg=dict(custom_keys={
        'lmm': dict(lr_mult=5.0),
        'connector': dict(lr_mult=5.0),
    }))
# batch 1 × tích lũy 4 = batch hiệu dụng 4 như base (2 × 2), nhưng mỗi iter chỉ 1 ảnh -> cần GẤP ĐÔI iter để thấy cùng
# số mẫu / số bước cập nhật (16k iter = 16k mẫu = 4000 bước, như 8k iter × batch 2). Mốc lr / val / checkpoint nhân 2.
max_iter = 16000
train_cfg = dict(max_iters=max_iter, val_interval=2000)
param_scheduler = [
    dict(type='LinearLR', start_factor=0.01, by_epoch=False, begin=0, end=400),
    dict(type='MultiStepLR', begin=0, end=max_iter, by_epoch=False, milestones=[12000, 15000], gamma=0.1)
]
# checkpoint chứa cả Qwen (~1-2 GB/file) -> giữ ít
default_hooks = dict(checkpoint=dict(interval=2000, max_keep_ckpts=1))
