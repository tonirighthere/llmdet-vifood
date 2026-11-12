import os
import sys
import zipfile
import cv2
import torch

# Ensure path
WORKSPACE_DIR = '/home/atin/tuan/SoPSoP'
LLMDET_DIR = os.path.join(WORKSPACE_DIR, 'llmdet_vietnamese_food')
sys.path.insert(0, LLMDET_DIR)
os.chdir(LLMDET_DIR)

from mmengine.registry import init_default_scope
init_default_scope('mmdet')
from mmdet.apis import init_detector, inference_detector

config_file = os.path.join(LLMDET_DIR, 'configs/val/grounding_dino_swin_t_vifood_val.py')
checkpoint_file = os.path.join(LLMDET_DIR, 'work_dirs/vifood_multi_res800/iter_10000.pth')

print("Loading model...", flush=True)
model = init_detector(config_file, checkpoint_file, device='cuda:0')
print("Model loaded successfully!", flush=True)

with zipfile.ZipFile(os.path.join(WORKSPACE_DIR, 'vifood2.zip'), 'r') as z:
    classes = [c.strip() for c in z.read('obj.names').decode('utf-8').splitlines() if c.strip()]

prompt = ' . '.join(classes) + ' .'
print(f"Classes ({len(classes)}): {classes[:5]} ... {classes[-3:]}", flush=True)

# Extract 3 sample images
os.makedirs('/tmp/vifood_test', exist_ok=True)
with zipfile.ZipFile(os.path.join(WORKSPACE_DIR, 'vifood_2999.zip'), 'r') as z:
    sample_names = z.namelist()[:3]
    for s in sample_names:
        z.extract(s, '/tmp/vifood_test')

for s in sample_names:
    img_path = os.path.join('/tmp/vifood_test', s)
    img_bgr = cv2.imread(img_path)
    h, w = img_bgr.shape[:2]
    with torch.no_grad():
        result = inference_detector(model, img_bgr, text_prompt=prompt, custom_entities=True)
    pred = result.pred_instances
    mask = pred.scores > 0.20
    boxes = pred.bboxes[mask].cpu().numpy()
    scores = pred.scores[mask].cpu().numpy()
    labels = pred.labels[mask].cpu().numpy()
    
    print(f"\n=== Image: {s} ({w}x{h}) ===", flush=True)
    print(f"Detected {len(boxes)} boxes (conf > 0.20):", flush=True)
    for b, sc, lb in zip(boxes, scores, labels):
        cls_name = classes[lb] if lb < len(classes) else f'unk_{lb}'
        print(f"  - Class {lb} ({cls_name}): score={sc:.3f}, box={[round(x, 1) for x in b]}", flush=True)

print("\nDone sanity check!", flush=True)
