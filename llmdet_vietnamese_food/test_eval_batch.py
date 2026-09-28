import os, sys
sys.path.insert(0, '/home/atin/tuan/SoPSoP/llmdet_vietnamese_food')

import torch
from mmengine.registry import init_default_scope
init_default_scope('mmdet')

from mmengine.config import Config
from mmengine.runner import Runner
from mmdet.registry import MODELS, DATASETS
from mmengine.dataset import DefaultSampler
from torch.utils.data import DataLoader

cfg = Config.fromfile('configs/val/grounding_dino_swin_t_vifood_val.py')
dataset = DATASETS.build(cfg.val_dataset)
print(f"Dataset size: {len(dataset)}")
sample = dataset[0]
print("Data sample text type:", type(sample['data_samples'].text))
print("Data sample text len:", len(sample['data_samples'].text))
print("First 3 classes:", sample['data_samples'].text[:3])
print("Data sample custom_entities:", getattr(sample['data_samples'], 'custom_entities', None))

model = MODELS.build(cfg.model)
checkpoint = torch.load('work_dirs/vifood_1k/iter_10000.pth', map_location='cpu')
if 'state_dict' in checkpoint:
    state_dict = checkpoint['state_dict']
else:
    state_dict = checkpoint
model.load_state_dict(state_dict, strict=False)
model.eval()
model.cuda()

# Collate batch
from mmdet.datasets import pseudo_collate
batch = pseudo_collate([sample])
data_batch = model.data_preprocessor(batch, training=False)

with torch.no_grad():
    results = model.predict(data_batch['inputs'], data_batch['data_samples'])

print(f"Number of pred instances: {len(results[0].pred_instances)}")
if len(results[0].pred_instances) > 0:
    print("Scores top 10:", results[0].pred_instances.scores[:10])
    print("Labels top 10:", results[0].pred_instances.labels[:10])
    print("Label names top 10:", getattr(results[0].pred_instances, 'label_names', [])[:10])
    print("Bboxes top 10:", results[0].pred_instances.bboxes[:10])
