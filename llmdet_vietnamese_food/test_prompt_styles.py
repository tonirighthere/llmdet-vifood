import os, sys
sys.path.insert(0, '/home/atin/tuan/SoPSoP/llmdet_vietnamese_food')

import torch
from mmengine.registry import init_default_scope
init_default_scope('mmdet')

from mmdet.apis import init_detector, inference_detector

config_file = 'configs/val/grounding_dino_swin_t_vifood_val.py'
checkpoint_file = 'work_dirs/vifood_vi_full_1k/iter_10000.pth'

model = init_detector(config_file, checkpoint_file, device='cuda:0')
img_path = '../grounding_data/vifood/images/val2017/srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg'

test_prompts = [
    ("bánh tráng .", True),
    ("bánh tráng . nem chua .", True),
    ("Trên bàn có đĩa bánh tráng thơm giòn.", False)
]

for prompt, custom_ent in test_prompts:
    print(f"\n--- Testing prompt: '{prompt}' (custom_entities={custom_ent}) ---")
    result = inference_detector(model, img_path, text_prompt=prompt, custom_entities=custom_ent)
    pred = result.pred_instances
    mask = pred.scores > 0.25
    filtered_boxes = pred.bboxes[mask].cpu().numpy()
    filtered_scores = pred.scores[mask].cpu().numpy()
    filtered_labels = pred.labels[mask].cpu().numpy()
    label_names = getattr(pred, 'label_names', None)
    if label_names is not None:
        filtered_names = [label_names[i] for i in range(len(mask)) if mask[i]]
    else:
        filtered_names = []
    print(f"Detected {len(filtered_boxes)} boxes:")
    for i in range(len(filtered_boxes)):
        name = filtered_names[i] if i < len(filtered_names) else f"Class {filtered_labels[i]}"
        print(f"  Box {i+1}: {filtered_boxes[i]}, Score: {filtered_scores[i]:.3f}, Name/Label: {name}")
