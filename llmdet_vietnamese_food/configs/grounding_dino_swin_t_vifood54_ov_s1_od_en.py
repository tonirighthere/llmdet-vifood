_base_ = 'grounding_dino_swin_t_vifood54_ov_s1_od.py'

# ═══════════════════════════════════════════════════════════════════════
# OV-S1-EN: như OV giai đoạn 1 (B1 chỉ trên 46 lớp BASE, 16k iter) nhưng tên lớp TIẾNG ANH
# ═══════════════════════════════════════════════════════════════════════
# Dữ liệu: python scripts/vifood54/make_ov_split.py --en  ->  grounding_data/vifood54/annotations_ov_en/
# 8 lớp novel bị bỏ box + tên khi train. Val chỉ lớp base; test đủ 54 tên EN -> AP_base / AP_novel (eval_ov.py).
# Đây là mốc cho OV-W-EN (..._ov_s2_lmm_en.py).

ov_dir = '../grounding_data/vifood54/annotations_ov_en/'
en_dir = '../grounding_data/vifood54/annotations_en/'

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

train_dataset = _base_.train_dataset
train_dataset.update(ann_file=ov_dir + 'train_od_rfs.jsonl', label_map_file=ov_dir + 'label_map_base.json')
train_dataset['pipeline'][-2]['class_drop_file'] = ov_dir + 'class_drop.json'
train_dataloader = dict(dataset=dict(_delete_=True, **train_dataset))

val_dataloader = dict(dataset=dict(metainfo=dict(classes=base_classes), ann_file=ov_dir + 'instances_val_base.json'))
val_evaluator = dict(ann_file=ov_dir + 'instances_val_base.json')
test_dataloader = dict(dataset=dict(metainfo=dict(classes=classes), ann_file=en_dir + 'instances_test.json'))
test_evaluator = dict(ann_file=en_dir + 'instances_test.json')
