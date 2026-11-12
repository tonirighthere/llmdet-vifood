#!/usr/bin/env python3
"""
vlm_grounding_pipeline.py
=========================
[LEGACY — ViFood-51, Exp 4] Không chạy được trên repo hiện tại: import `vlm_discovery` (không có trong git), trọng số
`vifood_multi_res800`. Pipeline hiện tại: `vifood54_vlm.py` + `vifood54_core.py` + `app_vifood54.py`;
đánh giá end-to-end: `scripts/vifood54/eval_vlm_prompt.py`.

Pipeline hợp nhất VLM-guided Food Grounding & Nutrition Analysis:
  1. VLM (Gemini) tự khám phá món ăn từ ảnh (Zero-Prompt User).
  2. Tạo prompt có cấu trúc và kích hoạt Grounding DINO (Exp 4).
  3. Cơ chế 2 tầng Cross-Validation lọc bỏ ảo giác (Anti-Hallucination).
  4. Portion Estimator tính khẩu phần & vi chất từ Bounding Box.
  5. Xuất báo cáo dinh dưỡng tổng thể bữa ăn kèm khuyến nghị sức khỏe.
"""

import os
import sys
import time
import json
from typing import Dict, Any, List, Optional, Tuple, Union
import numpy as np
from PIL import Image
import cv2
import torch

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from vlm_discovery import VLMFoodDiscoverer, CANONICAL_51_DISHES
from portion_estimator import PortionEstimator

try:
    from mmengine.registry import init_default_scope
    init_default_scope('mmdet')
    from mmdet.apis import init_detector, inference_detector
except Exception as e:
    pass


class VLMGroundedFoodAnalyzer:
    """Pipeline trọn vẹn kết hợp VLM + Grounding DINO + Portion Estimator."""

    def __init__(
        self,
        config_path: Optional[str] = None,
        weights_path: Optional[str] = None,
        device: str = 'cuda:0',
        gemini_api_key: Optional[str] = None
    ):
        self.device = device if torch.cuda.is_available() else 'cpu'
        self.config_path = config_path or os.path.join(
            CURRENT_DIR, 'configs/val/grounding_dino_swin_t_vifood_val.py'
        )
        self.weights_path = weights_path or os.path.join(
            CURRENT_DIR, 'work_dirs/vifood_multi_res800/iter_10000.pth'
        )

        print("[Pipeline] Đang khởi tạo VLM Food Discoverer...")
        self.vlm = VLMFoodDiscoverer(api_key=gemini_api_key)

        print("[Pipeline] Đang khởi tạo Portion Estimator...")
        self.portion_estimator = PortionEstimator()

        self.model = None
        self._init_detector()

    def _init_detector(self):
        """Khởi tạo Grounding DINO detector."""
        if not os.path.exists(self.weights_path):
            print(f"[Pipeline] ⚠️ Cảnh báo: Weights {self.weights_path} không tồn tại. Thử Exp 3...")
            alt_weights = os.path.join(CURRENT_DIR, 'work_dirs/vifood_vi_full_1k/iter_10000.pth')
            if os.path.exists(alt_weights):
                self.weights_path = alt_weights

        print(f"[Pipeline] Đang tải mô hình Grounding DINO ({self.weights_path}) lên {self.device}...")
        try:
            self.model = init_detector(self.config_path, self.weights_path, device=self.device)
        except Exception as e:
            print(f"[Pipeline] Lỗi tải detector: {e}")
            self.model = None

    def _apply_nms(self, detected_boxes: List[Dict[str, Any]], iou_thr: float = 0.55) -> List[Dict[str, Any]]:
        """Lọc các box trùng lặp bằng Non-Maximum Suppression trên từng loại món."""
        if not detected_boxes:
            return []
        sorted_boxes = sorted(detected_boxes, key=lambda x: x["score"], reverse=True)
        kept = []
        for b in sorted_boxes:
            box1 = b["box"]
            overlap = False
            for k in kept:
                # Chỉ lọc trùng nếu cùng tên món
                if b["label_name"] == k["label_name"]:
                    box2 = k["box"]
                    x1 = max(box1[0], box2[0])
                    y1 = max(box1[1], box2[1])
                    x2 = min(box1[2], box2[2])
                    y2 = min(box1[3], box2[3])
                    inter = max(0.0, x2 - x1) * max(0.0, y2 - y1)
                    area1 = max(0.0, box1[2] - box1[0]) * max(0.0, box1[3] - box1[1])
                    area2 = max(0.0, box2[2] - box2[0]) * max(0.0, box2[3] - box2[1])
                    union = area1 + area2 - inter
                    iou = inter / max(union, 1e-6)
                    if iou > iou_thr:
                        overlap = True
                        break
            if not overlap:
                kept.append(b)
        return kept

    def analyze_image(
        self,
        img_input: Union[str, Image.Image, np.ndarray],
        conf_thr: float = 0.20,
        manual_prompt: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Thực hiện toàn bộ quy trình nhận diện & phân tích dinh dưỡng.

        Args:
            img_input: đường dẫn file ảnh, PIL Image, hoặc numpy ndarray RGB
            conf_thr: ngưỡng tin cậy của Detector (mặc định 0.20)
            manual_prompt: nếu được cung cấp thì bỏ qua bước VLM (chế độ thủ công)
            use_cache: sử dụng cache cho VLM

        Returns:
            dict chứa toàn bộ kết quả phân tích
        """
        t_start = time.time()

        # 1. Chuẩn bị định dạng ảnh
        if isinstance(img_input, str):
            pil_img = Image.open(img_input).convert('RGB')
            img_np = np.array(pil_img)
        elif isinstance(img_input, Image.Image):
            pil_img = img_input.convert('RGB')
            img_np = np.array(pil_img)
        else:
            img_np = img_input
            pil_img = Image.fromarray(img_np).convert('RGB')

        img_h, img_w = img_np.shape[:2]
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

        # 2. Bước 1: VLM Khám phá (nếu không có manual_prompt)
        t_vlm_0 = time.time()
        if manual_prompt and manual_prompt.strip():
            # Chế độ thủ công
            vlm_info = {
                "canonical_dishes": [d.strip() for d in manual_prompt.split('.') if d.strip()],
                "raw_dishes": [d.strip() for d in manual_prompt.split('.') if d.strip()],
                "meal_description": "Nhận diện theo prompt chỉ định từ người dùng.",
                "health_assessment": "",
                "cached": False,
                "vlm_model": "manual_prompt"
            }
            detector_prompt = " . ".join(vlm_info["canonical_dishes"]) + " ."
            vlm_latency_ms = 0.0
        else:
            # Tự động qua VLM
            vlm_info = self.vlm.discover_dishes(pil_img, use_cache=use_cache)
            vlm_latency_ms = (time.time() - t_vlm_0) * 1000

            canonical = vlm_info.get("canonical_dishes", [])
            # Ưu tiên các món nằm trong ontology 51 lớp ViFood đã train
            known_dishes = [d for d in canonical if d in CANONICAL_51_DISHES]
            prompt_dishes = known_dishes if known_dishes else canonical[:4]

            if not prompt_dishes:
                prompt_dishes = ["món ăn"]

            detector_prompt = " . ".join(prompt_dishes) + " ."

        # 3. Bước 2: Grounding DINO Định vị
        t_det_0 = time.time()
        detected_boxes = []
        detector_latency_ms = 0.0

        if self.model is not None:
            with torch.no_grad():
                result = inference_detector(
                    self.model,
                    img_bgr,
                    text_prompt=detector_prompt,
                    custom_entities=True
                )
            detector_latency_ms = (time.time() - t_det_0) * 1000

            pred = result.pred_instances
            mask = pred.scores >= conf_thr

            boxes = pred.bboxes[mask].cpu().numpy()
            scores = pred.scores[mask].cpu().numpy()
            labels = pred.labels[mask].cpu().numpy()
            label_names_all = getattr(pred, 'label_names', None)

            for i, (box, score) in enumerate(zip(boxes, scores)):
                if label_names_all is not None and i < len(label_names_all):
                    label_name = label_names_all[i]
                else:
                    idx = int(labels[i])
                    cand = vlm_info.get("canonical_dishes", [])
                    label_name = cand[idx] if idx < len(cand) else f"dish_{idx}"

                detected_boxes.append({
                    "box": [float(c) for c in box],
                    "score": float(score),
                    "label_name": label_name
                })

            # NMS Deduplication để tránh tính trùng calo cho cùng 1 đĩa thức ăn
            detected_boxes = self._apply_nms(detected_boxes, iou_thr=0.55)

        # 4. Bước 3: Anti-Hallucination & Cross-Validation
        verified_dishes_set = set()
        portion_results = []

        for item in detected_boxes:
            box = item["box"]
            dish_name = item["label_name"]
            verified_dishes_set.add(dish_name)

            portion_info = self.portion_estimator.estimate_portion(
                bbox=box,
                img_shape=(img_h, img_w),
                dish_key=dish_name
            )
            portion_info["confidence"] = round(item["score"], 3)
            portion_info["box"] = [round(c, 1) for c in box]
            portion_results.append(portion_info)

        # Kiểm tra món VLM đề xuất nhưng Detector không thấy (Hallucination check)
        hallucinated_dishes = []
        for d in vlm_info.get("canonical_dishes", []):
            if not any(d.lower() in v.lower() or v.lower() in d.lower() for v in verified_dishes_set):
                hallucinated_dishes.append(d)

        # 5. Bước 4: Tổng hợp dinh dưỡng bữa ăn
        meal_summary = self.portion_estimator.summarize_meal(portion_results)

        total_latency_ms = (time.time() - t_start) * 1000

        return {
            "vlm_info": vlm_info,
            "detector_prompt": detector_prompt,
            "detected_portions": portion_results,
            "hallucinated_dishes": hallucinated_dishes,
            "meal_summary": meal_summary,
            "timing": {
                "vlm_latency_ms": round(vlm_latency_ms, 1),
                "detector_latency_ms": round(detector_latency_ms, 1),
                "total_latency_ms": round(total_latency_ms, 1)
            }
        }

    def render_overlay(
        self,
        img_np: np.ndarray,
        detected_portions: List[Dict[str, Any]],
        show_nutrition_tag: bool = True
    ) -> np.ndarray:
        """Vẽ bounding box nghệ thuật cùng nhãn món và calo trực tiếp lên ảnh."""
        vis_img = img_np.copy()
        h, w = vis_img.shape[:2]

        palette = [
            (46, 204, 113),   # Xanh lục
            (52, 152, 219),   # Xanh dương
            (231, 76, 60),    # Đỏ cam
            (241, 196, 15),   # Vàng chanh
            (155, 89, 182),   # Tím
            (230, 126, 34),   # Cam rực
            (26, 188, 156),   # Xanh ngọc
        ]

        for i, item in enumerate(detected_portions):
            box = item["box"]
            x1, y1, x2, y2 = map(int, box)
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)

            color = palette[i % len(palette)]
            name = item["name_vi"]
            cal = item["calories_kcal"]
            portion = item["portion_label"]
            conf = int(item["confidence"] * 100)

            # Vẽ bounding box dày 3px
            cv2.rectangle(vis_img, (x1, y1), (x2, y2), color, 3)

            # Chuẩn bị tag hiển thị
            if show_nutrition_tag:
                tag = f"{name} ({conf}%) | {cal} kcal [{portion}]"
            else:
                tag = f"{name} {conf}%"

            font_scale = 0.55
            thickness = 2
            (tw, th), baseline = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)

            # Vẽ nền cho text
            tag_y1 = max(0, y1 - th - 10)
            tag_y2 = y1
            cv2.rectangle(vis_img, (x1, tag_y1), (x1 + tw + 10, tag_y2), color, -1)
            cv2.putText(
                vis_img, tag, (x1 + 5, y1 - 6),
                cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness, cv2.LINE_AA
            )

        return vis_img


if __name__ == '__main__':
    # Test end-to-end pipeline
    test_img = '/home/atin/tuan/SoPSoP/grounding_data/vifood/images/val2017/srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg'
    analyzer = VLMGroundedFoodAnalyzer()
    print("\n--- Đang chạy phân tích end-to-end trên ảnh mẫu ---")
    results = analyzer.analyze_image(test_img, conf_thr=0.15)
    print("\n[Timing]:", json.dumps(results["timing"], indent=2))
    print("\n[VLM Meal Description]:", results["vlm_info"]["meal_description"])
    print("\n[VLM Health Assessment]:", results["vlm_info"]["health_assessment"])
    print("\n[Detected Portions]:", len(results["detected_portions"]))
    for p in results["detected_portions"]:
        print(f" - {p['name_vi']}: {p['calories_kcal']} kcal, P:{p['protein_g']}g, C:{p['carbs_g']}g, F:{p['fat_g']}g ({p['portion_label']}, Conf: {p['confidence']})")
    print("\n[Meal Summary]:", json.dumps(results["meal_summary"], ensure_ascii=False, indent=2))
