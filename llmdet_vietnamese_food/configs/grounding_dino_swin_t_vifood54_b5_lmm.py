_base_ = 'grounding_dino_swin_t_vifood54_b3b_ft.py'

# ═══════════════════════════════════════════════════════════════════════
# B5: B3b + giám sát LLM (đúng thiết kế LLMDet) — câu hỏi: loss sinh caption có giúp thêm không?
# ═══════════════════════════════════════════════════════════════════════
# Giống B3b (fine-tune từ B1-v2, OD + VG trộn ~1:1, 8k iter, lr 2e-5) + 2 loss của LMM
# (LLaVA-OneVision Qwen2-0.5B, LoRA; chỉ dùng lúc train, bỏ khi test bằng strip_lmm.py):
#   - loss_lmm_image: p5 (20x20) + p4 (27x27) của encoder -> connector 256->896 -> Qwen2 sinh lại
#     caption ảnh chi tiết (VLM đã lọc/duyệt, scripts/vifood54/captions/vlm_captions.py attach)
#   - d1.loss_lmm_region: query khớp box GT (+ cross-attn vào memory) -> Qwen2 sinh tên món
# Khác B3b đúng 2 chỗ: conversations (caption VLM thay template) và lmm bật -> so B5 vs B3b là tác dụng của LMM.

ann_dir = '../grounding_data/vifood54/annotations/'
num_region = 8  # paper 16; 8 để vừa RTX 3090 (giảm 4 nếu OOM)

model = dict(lmm=_base_.lmm_path, num_region_caption=num_region)

od_dataset = _base_.od_dataset
od_dataset['ann_file'] = ann_dir + 'train_od_rfs_lmm.jsonl'
od_dataset['pipeline'][-2]['num_region_caption'] = num_region   # RandomSamplingNegPos2
vg_dataset = _base_.vg_dataset
vg_dataset['ann_file'] = ann_dir + 'train_vg_cap_rfs_lmm.jsonl'
vg_dataset['pipeline'][-2]['num_region_caption'] = num_region

train_dataloader = dict(
    batch_size=1,
    dataset=dict(_delete_=True, type='ConcatDataset', datasets=[od_dataset, vg_dataset]))

optim_wrapper = dict(
    accumulative_counts=4,  # batch hiệu dụng 4 như B1/B3/B3b
    paramwise_cfg=dict(custom_keys={
        # LoRA + cross-attn trong Qwen và connector: lr 1e-4 như paper (detector giữ 2e-5)
        'lmm': dict(lr_mult=5.0),
        'connector': dict(lr_mult=5.0),       # khớp cả region_connector
    }))

# checkpoint chứa cả Qwen (~1-2 GB/file) -> giữ ít
default_hooks = dict(checkpoint=dict(max_keep_ckpts=1))
