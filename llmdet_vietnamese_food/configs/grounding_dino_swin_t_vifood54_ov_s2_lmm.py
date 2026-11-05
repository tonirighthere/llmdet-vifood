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

model = dict(lmm=_base_.lmm_path, num_region_caption=num_region)

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
default_hooks = dict(checkpoint=dict(max_keep_ckpts=1))
