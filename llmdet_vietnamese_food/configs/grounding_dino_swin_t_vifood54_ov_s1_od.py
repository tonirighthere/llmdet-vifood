_base_ = 'grounding_dino_swin_t_vifood54_b1_od.py'

# ═══════════════════════════════════════════════════════════════════════
# OV giai đoạn 1: như B1 nhưng chỉ lớp BASE (scripts/vifood54/make_ov_split.py)
# ═══════════════════════════════════════════════════════════════════════
# 8 lớp novel (taxonomy ov_split) bị bỏ khỏi box, prompt và negative khi train; ảnh giữ nguyên.
# Val (chọn checkpoint) chỉ lớp base. Test kế thừa B1: đủ 54 lớp -> đo AP_base / AP_novel.

ov_dir = '../grounding_data/vifood54/annotations_ov/'

base_classes = (
    'bánh bèo', 'bánh bột lọc', 'bánh canh', 'bánh chưng', 'bánh cuốn',
    'bánh căn', 'bánh khọt', 'bánh mì', 'bánh tráng', 'bánh tét',
    'bánh xèo', 'bánh đúc', 'bún bò Huế', 'bún tươi', 'bún mắm',
    'bún riêu', 'bún thịt nướng', 'bún đậu mắm tôm', 'canh', 'cháo lòng',
    'chả giò', 'cua', 'cá chiên', 'cơm chiên', 'gà luộc',
    'gỏi', 'gỏi cuốn', 'heo quay', 'hàu', 'hủ tiếu',
    'lẩu', 'mì Quảng', 'mực', 'ngao sò', 'phở',
    'rau sống', 'thịt bò', 'rau luộc', 'tôm', 'xôi',
    'món ăn khác', 'rau xào', 'đồ chấm', 'gà quay', 'nem rán',
    'món tráng miệng'
)

train_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    dict(
        type='RandomChoice',
        transforms=[
            [dict(type='RandomChoiceResize', scales=_base_.train_scales, keep_ratio=True)],
            [
                dict(type='RandomChoiceResize',
                     scales=[(400, 4200), (500, 4200), (600, 4200)],
                     keep_ratio=True),
                dict(type='RandomCrop',
                     crop_type='absolute_range',
                     crop_size=(384, 600),
                     allow_negative_crop=False),
                dict(type='RandomChoiceResize', scales=_base_.train_scales, keep_ratio=True),
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
        class_drop_file=ov_dir + 'class_drop.json',
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
    ann_file=ov_dir + 'train_od_rfs.jsonl',
    label_map_file=ov_dir + 'label_map_base.json',
    data_prefix=dict(img='../'),
    filter_cfg=dict(filter_empty_gt=False),
    pipeline=train_pipeline,
    return_classes=True,
    actual_dataset_mode='OD',
    use_short_cap=False,
    use_uniform_prompt=True,
    clean_caption=False,
    backend_args=None)

train_dataloader = dict(dataset=dict(_delete_=True, **train_dataset))

val_dataloader = dict(
    dataset=dict(
        metainfo=dict(classes=base_classes),
        ann_file=ov_dir + 'instances_val_base.json'))
val_evaluator = dict(ann_file=ov_dir + 'instances_val_base.json')
