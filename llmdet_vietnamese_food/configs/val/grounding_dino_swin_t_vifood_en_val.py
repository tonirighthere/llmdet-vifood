_base_ = '../grounding_dino_swin_t.py'

# 51 English dish classes
classes = (
    'steamed rice cakes', 'tapioca dumplings', 'thick noodle soup',
    'square sticky rice cake', 'steamed rice rolls', 'mini savory pancakes',
    'pyramid rice dumpling', 'mini crispy pancakes', 'Vietnamese baguette',
    'pia pastry', 'rice paper', 'cylindrical rice cake', 'sizzling crepe',
    'steamed savory cake', 'Hue beef noodle soup', 'rice vermicelli',
    'fermented fish noodle soup', 'crab noodle soup',
    'grilled pork noodle bowl', 'tofu and noodle platter',
    'sweet and sour soup', 'Cao Lau noodles', 'pork offal congee',
    'Vietnamese sausage', 'crab', 'fried fish', 'fried rice', 'broken rice',
    'boiled chicken', 'Vietnamese salad', 'fresh spring rolls', 'roast pork',
    'oyster', 'Hu Tieu noodles', 'hotpot', 'Quang noodles', 'squid',
    'fermented pork', 'clams and scallops', 'Vietnamese Pho',
    'fresh herbs and greens', 'crab asparagus soup', 'beef dish',
    'boiled vegetables', 'shrimp', 'turmeric sticky rice', 'sea snails',
    'other Vietnamese dish', 'stir-fried vegetables', 'dipping sauce',
    'roasted chicken'
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
    ann_file='annotations/instances_val_en.json',
    data_prefix=dict(img='images/val2017/'),
    test_mode=True,
    pipeline=base_test_pipeline,
    return_classes=True)

val_evaluator = dict(
    _delete_=True,
    type='CocoMetric',
    ann_file=data_root + 'annotations/instances_val_en.json',
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
