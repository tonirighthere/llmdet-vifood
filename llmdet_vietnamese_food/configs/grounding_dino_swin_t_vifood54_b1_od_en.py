_base_ = 'grounding_dino_swin_t_vifood54_b1_od.py'

# ═══════════════════════════════════════════════════════════════════════
# B1-EN: như B1-v2 (OD có negative, cùng aug, lr, 16k iter) nhưng tên lớp đưa vào BERT là TIẾNG ANH
# ═══════════════════════════════════════════════════════════════════════
# bert-base-uncased bỏ dấu và cắt tên Việt thành mảnh vô nghĩa ('bánh xèo' -> ban ##h x ##eo, 'cá'/'cà' -> 'ca').
# Dữ liệu annotations_en/ (scripts/vifood54/make_en_data.py): cùng ảnh, box, id lớp, split, RFS, class dropout
# với bộ VI; chỉ đổi chuỗi tên (en_names.PROMPT_EN). So sánh trực tiếp với B1-v2 (test mAP 0.315).

ann_dir = '../grounding_data/vifood54/annotations_en/'

# 54 class EN, đúng thứ tự id (annotations_en/label_map.json)
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

train_pipeline = _base_.train_pipeline
train_pipeline[5]['class_drop_file'] = ann_dir + 'class_drop.json'

train_dataset = _base_.train_dataset
train_dataset.update(ann_file=ann_dir + 'train_od_rfs.jsonl', label_map_file=ann_dir + 'label_map.json',
                     pipeline=train_pipeline)
train_dataloader = dict(dataset=train_dataset)

val_dataloader = dict(dataset=dict(metainfo=dict(classes=classes), ann_file=ann_dir + 'instances_val.json'))
test_dataloader = dict(dataset=dict(metainfo=dict(classes=classes), ann_file=ann_dir + 'instances_test.json'))
val_evaluator = dict(ann_file=ann_dir + 'instances_val.json')
test_evaluator = dict(ann_file=ann_dir + 'instances_test.json')
