_base_ = 'grounding_dino_swin_t.py'

# Disable LMM branch for Detector-only fine-tuning on RTX 3090 (24GB)
model = dict(
    lmm=None,
    test_cfg=dict(max_per_img=300, chunked_size=-1)
)

data_root = '../grounding_data/vifood/'

# Train dataset: 900 Vietnamese food images with ODVG format
vifood_train_dataset = dict(
    type='ODVGDataset',
    data_root=data_root,
    ann_file='annotations/vifood_train_vg.jsonl',
    label_map_file=None,
    data_prefix=dict(img='images/'),
    filter_cfg=dict(filter_empty_gt=False),
    pipeline=_base_.train_pipeline,
    return_classes=True,
    actual_dataset_mode='VG',
    use_short_cap=False,
    use_uniform_prompt=True,
    clean_caption=False,
    backend_args=None)

train_dataloader = dict(
    _delete_=True,
    batch_size=4,
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

val_dataloader = dict(
    _delete_=True,
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=val_dataset)

test_dataloader = val_dataloader

val_evaluator = dict(
    _delete_=True,
    type='CocoMetric',
    ann_file=data_root + 'annotations/instances_val.json',
    metric='bbox')

test_evaluator = val_evaluator

# Fine-tuning optimizer with domain-adapted learning rates
optim_wrapper = dict(
    _delete_=True,
    type='OptimWrapper',
    optimizer=dict(type='AdamW', lr=0.00005, weight_decay=0.0001),
    clip_grad=dict(max_norm=0.1, norm_type=2),
    paramwise_cfg=dict(
        custom_keys={
            'absolute_pos_embed': dict(decay_mult=0.),
            'backbone': dict(lr_mult=0.1),
            'language_model': dict(lr_mult=0.1),
        }))

# Iteration-based training schedule: 10,000 iterations (~44 epochs on 900 images @ bs=4)
# Pure training loop without mid-train evaluation interruption
max_iter = 10000
train_cfg = dict(
    _delete_=True,
    type='IterBasedTrainLoop',
    max_iters=max_iter)

val_cfg = None
val_dataloader = None
val_evaluator = None

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
    checkpoint=dict(by_epoch=False, interval=2000, max_keep_ckpts=5),
    visualization=dict(type='GroundingVisualizationHook'),
    logger=dict(type='LoggerHook', interval=50))

log_processor = dict(by_epoch=False)
auto_scale_lr = dict(base_batch_size=16, enable=False)

load_from = '../huggingface/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth'
