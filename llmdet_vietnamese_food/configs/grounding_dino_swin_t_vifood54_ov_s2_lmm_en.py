_base_ = 'grounding_dino_swin_t_vifood54_ov_s2_lmm.py'

# ═══════════════════════════════════════════════════════════════════════
# OV-W-EN: open-vocabulary giám sát yếu, TIẾNG ANH — lớp novel không có box, chỉ có tên trong caption ảnh cho LLM
# ═══════════════════════════════════════════════════════════════════════
# Như ..._ov_s2_lmm.py nhưng: dữ liệu annotations_ov_en/, lịch như B5-EN v2 (batch 2 × tích lũy 2, 8000 iter).
# load_from do run_ov_en.sh truyền: bước căn chỉnh (cùng config này + model.freeze_detector=True, 2000 iter) chạy từ
# OV-S1-EN, rồi bước train chung chạy từ checkpoint đã căn chỉnh.
# Caption: VIFOOD_LANG=en vlm_captions.py attach --ov [--strip-novel] [--suffix ...]; đổi file bằng
#   --cfg-options hoặc sửa cap_suffix dưới đây ('_lmm' | '_lmm_nonovel').

ov_dir = '../grounding_data/vifood54/annotations_ov_en/'
en_dir = '../grounding_data/vifood54/annotations_en/'
cap_suffix = '_lmm'

base_classes = (
    'steamed rice cakes', 'tapioca dumplings', 'thick noodle soup', 'square rice cake', 'steamed rice rolls',
    'mini savory pancakes', 'mini crispy pancakes', 'baguette sandwich', 'rice paper', 'cylindrical rice cake',
    'sizzling crepe', 'steamed savory cake', 'hue beef noodle soup', 'rice vermicelli', 'fermented fish noodle soup',
    'crab noodle soup', 'grilled pork noodle bowl', 'tofu and noodle platter', 'clear vegetable soup', 'pork offal congee',
    'vietnamese pork ham', 'whole crab', 'fried fish', 'fried rice', 'boiled chicken',
    'shredded salad', 'fresh spring rolls', 'roast pork', 'oyster', 'hu tieu noodles',
    'hotpot', 'quang noodles', 'squid', 'clams and scallops', 'pho noodle soup',
    'fresh herbs and greens', 'sliced beef', 'boiled vegetables', 'shrimp', 'sticky rice',
    'other dish', 'stir-fried vegetables', 'dipping sauce', 'roasted chicken', 'fried spring rolls',
    'dessert'
)
classes = (
    'steamed rice cakes', 'tapioca dumplings', 'thick noodle soup', 'square rice cake', 'steamed rice rolls',
    'mini savory pancakes', 'pyramid rice dumpling', 'mini crispy pancakes', 'baguette sandwich', 'pia pastry',
    'rice paper', 'cylindrical rice cake', 'sizzling crepe', 'steamed savory cake', 'hue beef noodle soup',
    'rice vermicelli', 'fermented fish noodle soup', 'crab noodle soup', 'grilled pork noodle bowl', 'tofu and noodle platter',
    'clear vegetable soup', 'cao lau noodles', 'pork offal congee', 'vietnamese pork ham', 'whole crab',
    'fried fish', 'fried rice', 'broken rice', 'boiled chicken', 'shredded salad',
    'fresh spring rolls', 'roast pork', 'oyster', 'hu tieu noodles', 'hotpot',
    'quang noodles', 'squid', 'fermented pork', 'clams and scallops', 'pho noodle soup',
    'fresh herbs and greens', 'crab soup', 'sliced beef', 'boiled vegetables', 'shrimp',
    'sticky rice', 'sea snails', 'other dish', 'stir-fried vegetables', 'dipping sauce',
    'roasted chicken', 'fried spring rolls', 'dessert', 'fried dough sticks'
)

od_dataset = _base_.od_dataset
od_dataset.update(ann_file=ov_dir + f'train_od_rfs{cap_suffix}.jsonl', label_map_file=ov_dir + 'label_map_base.json')
od_dataset['pipeline'][-2]['class_drop_file'] = ov_dir + 'class_drop.json'
vg_dataset = _base_.vg_dataset
vg_dataset['ann_file'] = ov_dir + f'train_vg_cap_rfs{cap_suffix}.jsonl'
vg_dataset['pipeline'][-2]['vg_negative_file'] = ov_dir + 'taxonomy_base.json'

train_dataloader = dict(
    batch_size=2,
    dataset=dict(_delete_=True, type='ConcatDataset', datasets=[od_dataset, vg_dataset]))
optim_wrapper = dict(accumulative_counts=2)

max_iter = 8000
train_cfg = dict(max_iters=max_iter, val_interval=1000)
param_scheduler = [
    dict(type='LinearLR', start_factor=0.01, by_epoch=False, begin=0, end=200),
    dict(type='MultiStepLR', begin=0, end=max_iter, by_epoch=False, milestones=[6000, 7500], gamma=0.1)
]
default_hooks = dict(checkpoint=dict(interval=1000, max_keep_ckpts=1))

val_dataloader = dict(dataset=dict(metainfo=dict(classes=base_classes), ann_file=ov_dir + 'instances_val_base.json'))
val_evaluator = dict(ann_file=ov_dir + 'instances_val_base.json')
test_dataloader = dict(dataset=dict(metainfo=dict(classes=classes), ann_file=en_dir + 'instances_test.json'))
test_evaluator = dict(ann_file=en_dir + 'instances_test.json')
