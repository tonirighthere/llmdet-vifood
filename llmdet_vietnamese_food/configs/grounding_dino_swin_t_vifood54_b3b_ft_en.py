_base_ = 'grounding_dino_swin_t_vifood54_b3b_ft.py'

# ═══════════════════════════════════════════════════════════════════════
# B3b-EN: như B3b (fine-tune 8k iter OD + VG caption 1:1, lr 2e-5) nhưng toàn bộ bằng TIẾNG ANH
# ═══════════════════════════════════════════════════════════════════════
# - Khởi tạo từ B1-EN thay cho B1-v2 (run_en.sh truyền đúng checkpoint best qua --cfg-options load_from=...).
# - OD: như B1-EN (tên lớp EN, cùng RFS, class dropout, negative).
# - VG: annotations_en/train_vg_cap_rfs.jsonl (scripts/vifood54/captions/build_captions_en.py): cùng bố cục, số
#   lượng, lượng từ như bản VI; thuộc tính lấy theo kết quả VLM trên từng ảnh (Gemma xác nhận cái nhìn thấy)
#   thay cho thuộc tính mặc định của lớp. Negative VG lấy từ annotations_en/taxonomy.json (tên EN + lớp dễ nhầm).

ann_dir = '../grounding_data/vifood54/annotations_en/'
load_from = 'work_dirs/vifood54_b1_od_en/best_coco_bbox_mAP_iter_16000.pth'

od_dataset = _base_.od_dataset
od_dataset.update(ann_file=ann_dir + 'train_od_rfs.jsonl', label_map_file=ann_dir + 'label_map.json')
od_dataset['pipeline'][5]['class_drop_file'] = ann_dir + 'class_drop.json'

vg_dataset = _base_.vg_dataset
vg_dataset['ann_file'] = ann_dir + 'train_vg_cap_rfs.jsonl'
vg_dataset['pipeline'][6]['vg_negative_file'] = ann_dir + 'taxonomy.json'

train_dataloader = dict(
    dataset=dict(_delete_=True, type='ConcatDataset', datasets=[od_dataset, vg_dataset]))

# 54 class EN, đúng thứ tự id (annotations_en/label_map.json); val/test dùng GT có tên EN
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
val_dataloader = dict(dataset=dict(metainfo=dict(classes=classes), ann_file=ann_dir + 'instances_val.json'))
test_dataloader = dict(dataset=dict(metainfo=dict(classes=classes), ann_file=ann_dir + 'instances_test.json'))
val_evaluator = dict(ann_file=ann_dir + 'instances_val.json')
test_evaluator = dict(ann_file=ann_dir + 'instances_test.json')
