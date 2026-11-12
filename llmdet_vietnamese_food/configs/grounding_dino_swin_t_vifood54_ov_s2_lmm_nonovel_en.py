_base_ = 'grounding_dino_swin_t_vifood54_ov_s2_lmm_en.py'

# Ablation OV-W-EN: caption đã bỏ mọi câu có tên món novel (VIFOOD_LANG=en vlm_captions.py attach --ov --strip-novel).
# OV-W-EN − bản này = tác dụng của việc tên novel xuất hiện trong caption.

ov_dir = '../grounding_data/vifood54/annotations_ov_en/'
od_dataset = _base_.od_dataset
od_dataset['ann_file'] = ov_dir + 'train_od_rfs_lmm_nonovel.jsonl'
vg_dataset = _base_.vg_dataset
vg_dataset['ann_file'] = ov_dir + 'train_vg_cap_rfs_lmm_nonovel.jsonl'
train_dataloader = dict(
    dataset=dict(_delete_=True, type='ConcatDataset', datasets=[od_dataset, vg_dataset]))
