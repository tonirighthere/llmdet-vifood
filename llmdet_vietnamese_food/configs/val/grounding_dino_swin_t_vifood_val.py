_base_ = '../grounding_dino_swin_t.py'

# 51 Vietnamese dish classes
classes = (
    'bánh bèo', 'bánh bột lọc', 'bánh canh', 'bánh chưng', 'bánh cuốn',
    'bánh căn', 'bánh giò', 'bánh khọt', 'bánh mì', 'bánh pía',
    'bánh tráng', 'bánh tét', 'bánh xèo', 'bánh đúc', 'bún bò Huế',
    'bún', 'bún mắm', 'bún riêu', 'bún thịt nướng', 'bún đậu mắm tôm',
    'canh chua', 'cao lầu', 'cháo lòng', 'chả', 'cua',
    'cá chiên', 'cơm chiên', 'cơm tấm', 'gà luộc', 'gỏi',
    'gỏi cuốn', 'heo quay', 'hàu', 'hủ tiếu', 'lẩu',
    'mì Quảng', 'mực', 'nem chua', 'ngao sò', 'phở',
    'rau sống', 'súp cua', 'thịt bò', 'rau luộc', 'tôm',
    'xôi xéo', 'ốc', 'món ăn khác', 'rau xào', 'nước chấm',
    'gà quay'
)

model = dict(
    lmm=None,
    test_cfg=dict(max_per_img=300, chunked_size=-1)
)

dataset_type = 'CocoDataset'
data_root = '../grounding_data/vifood/'

base_test_pipeline = _base_.test_pipeline
base_test_pipeline[-1]['meta_keys'] = ('img_id', 'img_path', 'ori_shape',
                                       'img_shape', 'scale_factor', 'text',
                                       'custom_entities', 'caption_prompt')

dataset = dict(
    type=dataset_type,
    data_root=data_root,
    metainfo=dict(classes=classes),
    ann_file='annotations/instances_val.json',
    data_prefix=dict(img='images/val2017/'),
    test_mode=True,
    pipeline=base_test_pipeline,
    return_classes=True)

val_evaluator = dict(
    _delete_=True,
    type='CocoMetric',
    ann_file=data_root + 'annotations/instances_val.json',
    metric='bbox')

val_dataloader = dict(
    _delete_=True,
    batch_size=1,
    num_workers=2,
    persistent_workers=True,
    drop_last=False,
    sampler=dict(type='DefaultSampler', shuffle=False),
    dataset=dataset)
test_dataloader = val_dataloader

test_evaluator = val_evaluator
