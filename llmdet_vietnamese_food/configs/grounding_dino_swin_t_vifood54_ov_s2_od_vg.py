_base_ = 'grounding_dino_swin_t_vifood54_ov_s1_od.py'

# ═══════════════════════════════════════════════════════════════════════
# OV giai đoạn 2: như B3b (fine-tune OD + VG caption 8k iter, lr 2e-5) trên lớp BASE
# ═══════════════════════════════════════════════════════════════════════
# load_from = checkpoint tốt nhất của giai đoạn 1 (scripts/vifood54/run_ov.sh truyền qua --cfg-options).
# Caption VG sinh lại không có lớp novel; negative VG lấy từ taxonomy_base (không có tên novel).

ov_dir = '../grounding_data/vifood54/annotations_ov/'
od_dataset = _base_.train_dataset

vg_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='RandomChoiceResize', scales=_base_.train_scales, keep_ratio=True),
    dict(type='FilterAnnotations', min_gt_bbox_wh=(1e-2, 1e-2)),
    dict(type='SampleCaptionVariant'),
    dict(
        type='RandomSamplingNegPos2',
        tokenizer_name=_base_.lang_model_name,
        tokenizer_name2=_base_.lmm_path,
        lmm_max_token_length=_base_.lmm_max_token_length,
        num_region_caption=0,
        vg_negative_file=ov_dir + 'taxonomy_base.json',
        max_tokens=256),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'flip', 'flip_direction', 'text', 'tags', 'contrast_conv',
                   'custom_entities', 'tokens_positive', 'dataset_mode', 'conversations', 'region_conversations'))
]

vg_dataset = dict(
    type='ODVGDataset',
    data_root='',
    ann_file=ov_dir + 'train_vg_cap_rfs.jsonl',
    data_prefix=dict(img='../'),
    filter_cfg=dict(filter_empty_gt=False),
    pipeline=vg_pipeline,
    return_classes=True,
    actual_dataset_mode='VG',
    use_short_cap=False,
    use_uniform_prompt=True,
    clean_caption=False,
    backend_args=None)

train_dataloader = dict(
    dataset=dict(_delete_=True, type='ConcatDataset', datasets=[od_dataset, vg_dataset]))

max_iter = 8000
train_cfg = dict(max_iters=max_iter, val_interval=1000)
param_scheduler = [
    dict(type='LinearLR', start_factor=0.01, by_epoch=False, begin=0, end=200),
    dict(type='MultiStepLR', begin=0, end=max_iter, by_epoch=False, milestones=[6000, 7500], gamma=0.1)
]
default_hooks = dict(checkpoint=dict(interval=1000))
optim_wrapper = dict(optimizer=dict(lr=0.00002))
