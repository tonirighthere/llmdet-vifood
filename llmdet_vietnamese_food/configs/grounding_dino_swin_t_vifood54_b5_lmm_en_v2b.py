_base_ = 'grounding_dino_swin_t_vifood54_b5_lmm_en_v2.py'

# B5b-EN: như B5-EN v2 (B5a) nhưng caption ảnh cho LLM là bản v2 (caption_v2.py: mô tả từng món + bối cảnh, đã kiểm chứng
# và duyệt)  ->  VIFOOD_LANG=en vlm_captions.py attach --suffix _lmm_v2
# B5b − B5a = tác dụng của chất lượng caption (tương ứng Table 7 của paper). Bước căn chỉnh dùng chung với B5a.

ann_dir = '../grounding_data/vifood54/annotations_en/'
od_dataset = _base_.od_dataset
od_dataset['ann_file'] = ann_dir + 'train_od_rfs_lmm_v2.jsonl'
vg_dataset = _base_.vg_dataset
vg_dataset['ann_file'] = ann_dir + 'train_vg_cap_rfs_lmm_v2.jsonl'
train_dataloader = dict(
    dataset=dict(_delete_=True, type='ConcatDataset', datasets=[od_dataset, vg_dataset]))
