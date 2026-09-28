import os, sys
sys.path.insert(0, '/home/atin/tuan/SoPSoP/llmdet_vietnamese_food')

from mmengine.config import Config
from mmengine.registry import init_default_scope
init_default_scope('mmdet')
from mmdet.registry import DATASETS, MODELS

cfg_path = 'configs/grounding_dino_swin_t_vifood_multi_res800.py'
print(f"Loading config: {cfg_path} ...")
cfg = Config.fromfile(cfg_path)

print("Building train dataset...")
train_dataset = DATASETS.build(cfg.vifood_train_dataset)
print(f"Train dataset size: {len(train_dataset)} samples (successfully loaded 2,700 samples!)")

sample0 = train_dataset[0]
print("Sample 0 caption:", sample0['data_samples'].text)
print("Sample 0 tokens_positive:", sample0['data_samples'].tokens_positive)

sample1 = train_dataset[1]
print("Sample 1 caption:", sample1['data_samples'].text)
print("Sample 1 tokens_positive:", sample1['data_samples'].tokens_positive)

sample2 = train_dataset[2]
print("Sample 2 caption:", sample2['data_samples'].text)
print("Sample 2 tokens_positive:", sample2['data_samples'].tokens_positive)

print("\nBuilding model...")
model = MODELS.build(cfg.model)
print("Model built successfully!")
