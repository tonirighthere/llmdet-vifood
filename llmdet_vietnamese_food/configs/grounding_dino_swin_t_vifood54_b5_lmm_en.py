_base_ = 'grounding_dino_swin_t_vifood54_b5_lmm.py'

# ═══════════════════════════════════════════════════════════════════════
# B5-EN: như B5 của Pha 5 (B3b + giám sát LLM: loss caption ảnh + caption vùng, lmm lr ×5, num_region 8,
# batch 1 × tích lũy 4) nhưng toàn bộ bằng TIẾNG ANH: prompt BERT, caption VG, caption ảnh và tên vùng cho Qwen2.
# Khởi tạo từ B1-EN (run_en.sh truyền checkpoint best). Caption ảnh (*_lmm.jsonl) do
# `VIFOOD_LANG=en vlm_captions.py attach` gắn: caption VLM tiếng Anh đã lọc/duyệt nếu có, không thì caption template L2 EN.

ann_dir = '../grounding_data/vifood54/annotations_en/'
load_from = 'work_dirs/vifood54_b1_od_en/best_coco_bbox_mAP_iter_16000.pth'

od_dataset = _base_.od_dataset
od_dataset.update(ann_file=ann_dir + 'train_od_rfs_lmm.jsonl', label_map_file=ann_dir + 'label_map.json')
od_dataset['pipeline'][-2]['class_drop_file'] = ann_dir + 'class_drop.json'

vg_dataset = _base_.vg_dataset
vg_dataset['ann_file'] = ann_dir + 'train_vg_cap_rfs_lmm.jsonl'
vg_dataset['pipeline'][-2]['vg_negative_file'] = ann_dir + 'taxonomy.json'

train_dataloader = dict(
    batch_size=1,
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
