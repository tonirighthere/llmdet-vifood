_base_ = 'grounding_dino_swin_t.py'

# ═══════════════════════════════════════════════════════════════════════
# CẢI THIỆN ĐỒ ÁN: MULTI-PROMPTING (X3 DATA) & TĂNG ĐỘ PHÂN GIẢI (RES 800)
# ═══════════════════════════════════════════════════════════════════════
# 1. Dữ liệu: 2.700 mẫu đa phong cách (Mô tả tự nhiên, Tìm kiếm & Định vị, Nhãn rời rạc)
# 2. Độ phân giải: Multi-scale lên tới (800, 1333) giúp bắt chi tiết topping & mâm nhiều đĩa
# 3. Phần cứng: Tối ưu cho NVIDIA GeForce RTX 3090 (24GB VRAM)

model = dict(
    lmm=None,
    test_cfg=dict(max_per_img=300, chunked_size=-1)
)

data_root = '../grounding_data/vifood/'

# Multi-scale training pipeline (High Resolution up to 800x1333)
train_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(
        type='RandomChoiceResize',
        scales=[(480, 1333), (560, 1333), (640, 1333), (720, 1333), (800, 1333)],
        keep_ratio=True),
    dict(type='FilterAnnotations', min_gt_bbox_wh=(1e-2, 1e-2)),
    dict(
        type='RandomSamplingNegPos2',
        tokenizer_name=_base_.lang_model_name,
        tokenizer_name2=_base_.lmm_path,
        lmm_max_token_length=_base_.lmm_max_token_length,
        num_region_caption=_base_.num_region_caption,
        num_sample_negative=85,
        max_tokens=256),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'flip', 'flip_direction', 'text', 'tags', 'contrast_conv',
                   'custom_entities', 'tokens_positive', 'dataset_mode', 'conversations', 'region_conversations'))
]

# Train dataset: 2,700 samples multi-prompting (3 styles per image)
vifood_train_dataset = dict(
    type='ODVGDataset',
    data_root=data_root,
    ann_file='annotations/vifood_train_vg_vi_multi.jsonl',
    label_map_file=None,
    data_prefix=dict(img='images/'),
    filter_cfg=dict(filter_empty_gt=False),
    pipeline=train_pipeline,
    return_classes=True,
    actual_dataset_mode='VG',
    use_short_cap=False,
    use_uniform_prompt=True,
    clean_caption=False,
    backend_args=None)

train_dataloader = dict(
    _delete_=True,
    batch_size=2,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(type='DefaultSampler', shuffle=True),
    batch_sampler=dict(type='AspectRatioBatchSampler'),
    dataset=vifood_train_dataset)

# Validation pipeline and dataset
base_test_pipeline = _base_.test_pipeline
base_test_pipeline[-1]['meta_keys'] = (
    'img_id', 'img_path', 'ori_shape', 'img_shape',
    'scale_factor', 'text', 'custom_entities', 'caption_prompt'
)

val_dataset = dict(
    type='CocoDataset',
    data_root=data_root,
    ann_file='annotations/instances_val.json',
    data_prefix=dict(img='images/val2017/'),
    test_mode=True,
    pipeline=base_test_pipeline,
    return_classes=True)

val_dataloader = None
val_cfg = None
val_evaluator = None

test_dataloader = dict(
    _delete_=True,
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=val_dataset)

test_evaluator = dict(
    _delete_=True,
    type='CocoMetric',
    ann_file=data_root + 'annotations/instances_val.json',
    metric='bbox')

# Optimizer: Accumulative counts = 2 for effective batch size 4
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    accumulative_counts=2,
    optimizer=dict(type='AdamW', lr=0.00005, weight_decay=0.0001),
    clip_grad=dict(max_norm=0.1, norm_type=2),
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'backbone': dict(lr_mult=0.1),
            'language_model': dict(lr_mult=0.1),
        }))

# Schedule: 10,000 iters
max_iter = 10000
train_cfg = dict(
    _delete_=True,
    type='IterBasedTrainLoop',
    max_iters=max_iter)

param_scheduler = [
    dict(type='LinearLR', start_factor=0.001, by_epoch=False, begin=0, end=500),
    dict(
        type='MultiStepLR',
        begin=0,
        end=max_iter,
        by_epoch=False,
        milestones=[7000, 9000],
        gamma=0.1)
]

default_hooks = dict(
    checkpoint=dict(
        type='CheckpointHook',
        by_epoch=False,
        interval=2000,
        max_keep_ckpts=5,
        save_best=None),
    logger=dict(type='LoggerHook', interval=50))
