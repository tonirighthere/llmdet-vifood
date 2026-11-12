import os
import sys
import zipfile
import cv2
import torch
import numpy as np

WORKSPACE_DIR = '/home/atin/tuan/SoPSoP'
LLMDET_DIR = os.path.join(WORKSPACE_DIR, 'llmdet_vietnamese_food')
sys.path.insert(0, LLMDET_DIR)
os.chdir(LLMDET_DIR)

from mmengine.registry import init_default_scope
init_default_scope('mmdet')
from mmdet.apis import init_detector, inference_detector

config_file = os.path.join(LLMDET_DIR, 'configs/val/grounding_dino_swin_t_vifood_val.py')
checkpoint_file = os.path.join(LLMDET_DIR, 'work_dirs/vifood_multi_res800/iter_10000.pth')

model = init_detector(config_file, checkpoint_file, device='cuda:0')

with zipfile.ZipFile(os.path.join(WORKSPACE_DIR, 'vifood2.zip'), 'r') as z:
    classes = [c.strip() for c in z.read('obj.names').decode('utf-8').splitlines() if c.strip()]

prompt = ' . '.join(classes) + ' .'

with zipfile.ZipFile(os.path.join(WORKSPACE_DIR, 'vifood_2999.zip'), 'r') as z:
    names = z.namelist()[:5]
    for n in names:
        z.extract(n, '/tmp/vifood_test')

def nms(boxes, scores, iou_thr=0.5):
    if len(boxes) == 0:
        return []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        ovr = inter / (areas[i] + areas[order[1:]] - inter)
        inds = np.where(ovr <= iou_thr)[0]
        order = order[inds + 1]
    return keep

print("=== EVALUATION OF THRESHOLDS ===")
for name in names:
    img_path = os.path.join('/tmp/vifood_test', name)
    img_bgr = cv2.imread(img_path)
    with torch.no_grad():
        res = inference_detector(model, img_bgr, text_prompt=prompt, custom_entities=True)
    pred = res.pred_instances
    scores = pred.scores.cpu().numpy()
    boxes = pred.bboxes.cpu().numpy()
    labels = pred.labels.cpu().numpy()
    
    print(f"\nImage: {name} (shape {img_bgr.shape[:2]})")
    for thr in [0.20, 0.22, 0.25, 0.30]:
        mask = scores >= thr
        b_thr = boxes[mask]
        s_thr = scores[mask]
        l_thr = labels[mask]
        # raw count
        raw_count = len(b_thr)
        # NMS per class
        cls_nms_keep = []
        for c in np.unique(l_thr):
            c_mask = l_thr == c
            c_idx = np.where(c_mask)[0]
            k = nms(b_thr[c_idx], s_thr[c_idx], iou_thr=0.5)
            cls_nms_keep.extend(c_idx[k])
        # Cross-class NMS
        cross_nms_keep = nms(b_thr, s_thr, iou_thr=0.6)
        print(f"  Thr {thr:.2f}: raw={raw_count}, per-class NMS={len(cls_nms_keep)}, cross-class NMS(0.6)={len(cross_nms_keep)}")
        if thr == 0.22:
            print("    Detections (cross NMS):")
            for idx in cross_nms_keep:
                print(f"      - {classes[l_thr[idx]]} ({s_thr[idx]:.3f})")
