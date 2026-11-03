_base_ = 'grounding_dino_swin_t.py'

# ═══════════════════════════════════════════════════════════════════════
# B1: ViFood-54 — OD mode có negative (kiểm chứng giả thuyết thiếu negative)
# ═══════════════════════════════════════════════════════════════════════
# - Dữ liệu: scripts/vifood54/build_vifood54.py (2 zip CVAT, 54 class, chả giò và nem rán
#   là 2 lớp riêng, split theo ảnh gốc). Mỗi mẫu train: prompt = lớp dương + lớp âm
#   lấy ngẫu nhiên từ label_map (RandomSamplingNegPos2.od_aug), khớp với prompt lúc test.
# - Cân bằng lớp: lớp hiếm lặp theo repeat factor (train_od_rfs.jsonl), lớp đầu bị
#   class dropout (class_drop.json), augment vị trí bằng flip + resize/crop ngẫu nhiên.
# - Đường dẫn ảnh trong annotation tương đối từ root dự án, nên data_root='' và
#   ann_file/data_prefix đều bắt đầu bằng '../' (chạy từ llmdet_vietnamese_food/).

model = dict(
    lmm=None,
    test_cfg=dict(max_per_img=300, chunked_size=-1)
)

ann_dir = '../grounding_data/vifood54/annotations/'

# 54 class, đúng thứ tự id trong taxonomy.json / instances_*.json
classes = (
    'bánh bèo', 'bánh bột lọc', 'bánh canh', 'bánh chưng', 'bánh cuốn',
    'bánh căn', 'bánh giò', 'bánh khọt', 'bánh mì', 'bánh pía',
    'bánh tráng', 'bánh tét', 'bánh xèo', 'bánh đúc', 'bún bò Huế',
    'bún tươi', 'bún mắm', 'bún riêu', 'bún thịt nướng', 'bún đậu mắm tôm',
    'canh', 'cao lầu', 'cháo lòng', 'chả giò', 'cua',
    'cá chiên', 'cơm chiên', 'cơm tấm', 'gà luộc', 'gỏi',
    'gỏi cuốn', 'heo quay', 'hàu', 'hủ tiếu', 'lẩu',
    'mì Quảng', 'mực', 'nem chua', 'ngao sò', 'phở',
    'rau sống', 'súp cua', 'thịt bò', 'rau luộc', 'tôm',
    'xôi', 'ốc', 'món ăn khác', 'rau xào', 'đồ chấm',
    'gà quay', 'nem rán', 'món tráng miệng', 'quẩy'
)

train_scales = [(480, 1333), (512, 1333), (544, 1333), (576, 1333),
                (608, 1333), (640, 1333), (672, 1333), (704, 1333),
                (736, 1333), (768, 1333), (800, 1333)]

train_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(type='LoadAnnotations', with_bbox=True),
    # Augment vị trí: an toàn ở OD mode vì prompt chỉ là tên lớp, không có từ chỉ vị trí
    dict(type='RandomFlip', prob=0.5),
    dict(
        type='RandomChoice',
        transforms=[
            [dict(type='RandomChoiceResize', scales=train_scales, keep_ratio=True)],
            [
                dict(type='RandomChoiceResize',
                     scales=[(400, 4200), (500, 4200), (600, 4200)],
                     keep_ratio=True),
                dict(type='RandomCrop',
                     crop_type='absolute_range',
                     crop_size=(384, 600),
                     allow_negative_crop=False),
                dict(type='RandomChoiceResize', scales=train_scales, keep_ratio=True),
            ],
        ]),
    dict(type='FilterAnnotations', min_gt_bbox_wh=(1e-2, 1e-2)),
    dict(
        type='RandomSamplingNegPos2',
        tokenizer_name=_base_.lang_model_name,
        tokenizer_name2=_base_.lmm_path,
        lmm_max_token_length=_base_.lmm_max_token_length,
        num_region_caption=_base_.num_region_caption,
        num_sample_negative=85,
        class_drop_file=ann_dir + 'class_drop.json',
        max_tokens=256),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'flip', 'flip_direction', 'text', 'tags', 'contrast_conv',
                   'custom_entities', 'tokens_positive', 'dataset_mode', 'conversations', 'region_conversations'))
]

train_dataset = dict(
    type='ODVGDataset',
    data_root='',
    ann_file=ann_dir + 'train_od_rfs.jsonl',
    label_map_file=ann_dir + 'label_map.json',
    data_prefix=dict(img='../'),
    filter_cfg=dict(filter_empty_gt=False),
    pipeline=train_pipeline,
    return_classes=True,
    actual_dataset_mode='OD',
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
    dataset=train_dataset)

test_pipeline = _base_.test_pipeline
test_pipeline[-1]['meta_keys'] = (
    'img_id', 'img_path', 'ori_shape', 'img_shape',
    'scale_factor', 'text', 'custom_entities', 'caption_prompt'
)


def _coco_split(split):
    return dict(
        type='CocoDataset',
        data_root='',
        metainfo=dict(classes=classes),
        ann_file=ann_dir + f'instances_{split}.json',
        data_prefix=dict(img='../'),
        test_mode=True,
        pipeline=test_pipeline,
        return_classes=True)


val_dataloader = dict(
    _delete_=True,
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=_coco_split('val'))

test_dataloader = dict(
    _delete_=True,
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=_coco_split('test'))

val_evaluator = dict(
    _delete_=True,
    type='CocoMetric',
    ann_file=ann_dir + 'instances_val.json',
    metric='bbox',
    classwise=True)

test_evaluator = dict(
    _delete_=True,
    type='CocoMetric',
    ann_file=ann_dir + 'instances_test.json',
    metric='bbox',
    classwise=True)

# Optimizer giống Exp4 (lr 5e-5, batch hiệu dụng 4) để so sánh công bằng
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

# ~4.1k mẫu/epoch (sau RFS), batch 2 -> ~2.07k iter/epoch; 16k iter ≈ 7.7 epoch
max_iter = 16000
train_cfg = dict(
    _delete_=True,
    type='IterBasedTrainLoop',
    max_iters=max_iter,
    val_interval=2000)
val_cfg = dict(type='ValLoop')
test_cfg = dict(type='TestLoop')

param_scheduler = [
    dict(type='LinearLR', start_factor=0.001, by_epoch=False, begin=0, end=500),
    dict(
        type='MultiStepLR',
        begin=0,
        end=max_iter,
        by_epoch=False,
        milestones=[12000, 15000],
        gamma=0.1)
]

default_hooks = dict(
    checkpoint=dict(
        type='CheckpointHook',
        by_epoch=False,
        interval=2000,
        max_keep_ckpts=3,
        save_best='coco/bbox_mAP',
        rule='greater'),
    logger=dict(type='LoggerHook', interval=50))
