import cv2
import numpy as np

def draw_bboxes(img, bboxes, scores, labels, label_names=None, score_thr=0.25):
    """Draw bounding boxes with modern color palette and styled labels."""
    vis_img = img.copy()
    if vis_img.dtype != np.uint8:
        vis_img = (vis_img * 255).astype(np.uint8)
        
    colors = [
        (46, 204, 113),   # Green
        (52, 152, 219),   # Blue
        (231, 76, 60),    # Red
        (241, 196, 15),   # Yellow
        (155, 89, 182),   # Purple
        (230, 126, 34),   # Orange
        (26, 188, 156),   # Turquoise
        (236, 240, 241)   # Off-white
    ]
    
    h, w = vis_img.shape[:2]
    
    for i, (box, score) in enumerate(zip(bboxes, scores)):
        if score < score_thr:
            continue
        x1, y1, x2, y2 = map(int, box)
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        
        color = colors[i % len(colors)]
        
        # Draw outer box
        cv2.rectangle(vis_img, (x1, y1), (x2, y2), color, 3)
        
        # Prepare label
        name = label_names[i] if label_names and i < len(label_names) else f"Dish {labels[i]}"
        tag = f"{name}: {score*100:.1f}%"
        
        # Tag background
        (tw, th), baseline = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        tag_y1 = max(0, y1 - th - 8)
        tag_y2 = y1
        cv2.rectangle(vis_img, (x1, tag_y1), (x1 + tw + 10, tag_y2), color, -1)
        cv2.putText(vis_img, tag, (x1 + 5, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2, cv2.LINE_AA)
        
    return vis_img

print("Helper draw_bboxes defined successfully.")
