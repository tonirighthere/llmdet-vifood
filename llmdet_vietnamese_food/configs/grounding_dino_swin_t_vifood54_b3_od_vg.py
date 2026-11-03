_base_ = 'grounding_dino_swin_t_vifood54_b1_od.py'

# ═══════════════════════════════════════════════════════════════════════
# B3: ViFood-54 — OD (như B1) + VG caption hình thái, trộn ~1:1
# ═══════════════════════════════════════════════════════════════════════
# Câu hỏi: caption mô tả cái nhìn thấy (vị trí, số lượng, lượng từ, thuộc tính hình thái)
# có giúp thêm so với chỉ prompt tên lớp (B1-v2, test mAP 0.315) không?
# - OD: giữ nguyên B1 (train_od_rfs, class dropout, flip + resize/crop, negative từ label_map).
# - VG: train_vg_cap_rfs.jsonl (Pha 2, 6 biến thể/ảnh). SampleCaptionVariant chọn ngẫu nhiên
#   một biến thể mỗi lần load, dùng bản lật khi RandomFlip lật ảnh. vg_aug nối tên lớp KHÔNG có
#   trong ảnh làm negative (ưu tiên lớp dễ nhầm theo taxonomy confusable_with) tới 256 token.
#   Không RandomCrop: crop làm mất box hoặc sai từ chỉ vị trí mà caption đã nêu.
# - Cùng 16k iter / batch hiệu dụng 4 như B1 (cùng lượng tính toán): mỗi nguồn ~ một nửa số bước.

ann_dir = '../grounding_data/vifood54/annotations/'
od_dataset = _base_.train_dataset

vg_pipeline = [
    dict(type='LoadImageFromFile', backend_args=None),
    dict(type='LoadAnnotations', with_bbox=True),
    dict(type='RandomFlip', prob=0.5),
    dict(type='RandomChoiceResize', scales=_base_.train_scales, keep_ratio=True),
    dict(type='FilterAnnotations', min_gt_bbox_wh=(1e-2, 1e-2)),
    dict(type='SampleCaptionVariant'),
    dict(
        type='RandomSamplingNegPos2',
        tokenizer_name=_base_.lang_model_name,
        tokenizer_name2=_base_.lmm_path,
        lmm_max_token_length=_base_.lmm_max_token_length,
        num_region_caption=0,  # lmm=None: không cần hội thoại vùng
        vg_negative_file=ann_dir + 'taxonomy.json',
        max_tokens=256),
    dict(
        type='PackDetInputs',
        meta_keys=('img_id', 'img_path', 'ori_shape', 'img_shape',
                   'scale_factor', 'flip', 'flip_direction', 'text', 'tags', 'contrast_conv',
                   'custom_entities', 'tokens_positive', 'dataset_mode', 'conversations', 'region_conversations'))
]

vg_dataset = dict(
    type='ODVGDataset',
    data_root='',
    ann_file=ann_dir + 'train_vg_cap_rfs.jsonl',
    data_prefix=dict(img='../'),
    filter_cfg=dict(filter_empty_gt=False),
    pipeline=vg_pipeline,
    return_classes=True,
    actual_dataset_mode='VG',
    use_short_cap=False,
    use_uniform_prompt=True,
    clean_caption=False,
    backend_args=None)

train_dataloader = dict(
    dataset=dict(_delete_=True, type='ConcatDataset', datasets=[od_dataset, vg_dataset]))
