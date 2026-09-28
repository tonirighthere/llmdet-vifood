import os, sys
sys.path.insert(0, '/home/atin/tuan/SoPSoP/llmdet_vietnamese_food')

import torch
from mmengine.registry import init_default_scope
init_default_scope('mmdet')

from mmdet.apis import init_detector, inference_detector

config_file = 'configs/val/grounding_dino_swin_t_vifood_val.py'
checkpoint_file = 'work_dirs/vifood_vi_full_1k/iter_10000.pth'

print("Initializing detector...")
model = init_detector(config_file, checkpoint_file, device='cuda:0')
print("Model initialized successfully!")

img_path = '../grounding_data/vifood/images/val2017/srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg'
prompt = "bánh tráng . nem chua ."

print("Running inference...")
result = inference_detector(model, img_path, text_prompt=prompt, custom_entities=True)
pred = result.pred_instances
print("Number of detected instances:", len(pred))

mask = pred.scores > 0.25
filtered_boxes = pred.bboxes[mask].cpu().numpy()
filtered_scores = pred.scores[mask].cpu().numpy()
filtered_labels = pred.labels[mask].cpu().numpy()

print(f"Detected {len(filtered_boxes)} boxes with score > 0.25:")
for box, score, label in zip(filtered_boxes, filtered_scores, filtered_labels):
    print(f" - Box: {box}, Score: {score:.3f}, Label: {label}")
