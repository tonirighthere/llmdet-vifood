import os, sys
sys.path.insert(0, '/home/atin/tuan/SoPSoP/llmdet_vietnamese_food')

import cv2
import numpy as np
import torch
from mmengine.registry import init_default_scope
init_default_scope('mmdet')
from mmdet.apis import init_detector, inference_detector

out_dir = 'demo_output/qualitative_comparison'
os.makedirs(out_dir, exist_ok=True)

models = {
    "zero_shot": ('configs/val/grounding_dino_swin_t_vifood_val.py', '/home/atin/tuan/SoPSoP/huggingface/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth'),
    "exp1_vi_short": ('configs/val/grounding_dino_swin_t_vifood_val.py', 'work_dirs/vifood_1k/iter_10000.pth'),
    "exp3_vi_full": ('configs/val/grounding_dino_swin_t_vifood_val.py', 'work_dirs/vifood_vi_full_1k/iter_10000.pth')
}

samples = [
    {
        "name": "sample_pho",
        "path": '../grounding_data/vifood/images/val2017/srcB_623_jpg.rf.9787785936d42bb9d0b9ac5ba40945ef.jpg',
        "prompt": "Bát phở bò nóng hổi ăn kèm đĩa rau sống và chén nước chấm.",
        "short_prompt": "phở . rau sống . nước chấm ."
    },
    {
        "name": "sample_banh_trang",
        "path": '../grounding_data/vifood/images/val2017/srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg',
        "prompt": "Trên bàn có hai đĩa bánh tráng nướng giòn.",
        "short_prompt": "bánh tráng ."
    }
]

colors = [(46, 204, 113), (52, 152, 219), (231, 76, 60), (241, 196, 15), (155, 89, 182)]

for m_key, (cfg_p, w_p) in models.items():
    print(f"Loading model [{m_key}]...")
    model = init_detector(cfg_p, w_p, device='cuda:0')
    
    for s in samples:
        img_bgr = cv2.imread(s['path'])
        p = s['prompt'] if m_key == 'exp3_vi_full' else s['short_prompt']
        is_custom = (m_key != 'exp3_vi_full')
        
        with torch.no_grad():
            res = inference_detector(model, img_bgr, text_prompt=p, custom_entities=is_custom)
            
        pred = res.pred_instances
        mask = pred.scores > 0.20
        boxes = pred.bboxes[mask].cpu().numpy()
        scores = pred.scores[mask].cpu().numpy()
        labels = pred.labels[mask].cpu().numpy()
        names = getattr(pred, 'label_names', None)
        
        vis = img_bgr.copy()
        for i, (b, sc) in enumerate(zip(boxes, scores)):
            x1, y1, x2, y2 = map(int, b)
            col = colors[i % len(colors)]
            cv2.rectangle(vis, (x1, y1), (x2, y2), col, 3)
            tag_name = names[i] if names and i < len(names) else f"Dish {labels[i]}"
            tag = f"{tag_name}: {sc*100:.1f}%"
            (tw, th), _ = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)
            cv2.rectangle(vis, (x1, max(0, y1-th-8)), (x1+tw+8, y1), col, -1)
            cv2.putText(vis, tag, (x1+4, y1-4), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2, cv2.LINE_AA)
            
        save_path = os.path.join(out_dir, f"{s['name']}_{m_key}.jpg")
        cv2.imwrite(save_path, vis)
        print(f"Saved: {save_path} ({len(boxes)} boxes)")

print("\nAll qualitative comparison images exported successfully to:", out_dir)
