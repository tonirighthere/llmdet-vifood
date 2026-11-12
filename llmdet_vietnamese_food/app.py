#!/usr/bin/env python3
"""
app.py
======
[LEGACY — ViFood-51, Exp 1-4] Không chạy được trên repo hiện tại: cần `vlm_discovery.py` (không có trong git) và
trọng số Exp 4. Demo đang dùng là `app_vifood54.py` (54 lớp, mô hình EN, Gemini, dinh dưỡng + dị ứng).

Hệ Thống Smart Vietnamese Food AI:
  - Tab 1 (🤖 AI Tự Động): VLM-Guided Discovery (Zero-Prompt), phát hiện tự động,
    định vị chính xác bằng Grounding DINO, ước lượng khẩu phần & tính dinh dưỡng bữa ăn.
  - Tab 2 (✍️ Nhập Thủ Công): Grounding DINO với câu tìm kiếm tùy biến tiếng Việt.
  - Tab 3 (📊 Benchmark): Báo cáo thực nghiệm khoa học 4 mô hình (COCO metric).
  - Tab 4 (📖 Từ Điển 51 Món): Cơ sở tri thức dinh dưỡng chuẩn ViFood.
"""

import os
import sys
import time
import json
import re
import cv2
import numpy as np
import torch
from PIL import Image
import gradio as gr

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from mmengine.registry import init_default_scope
init_default_scope('mmdet')
from mmdet.apis import init_detector, inference_detector

from vlm_discovery import VLMFoodDiscoverer, CANONICAL_51_DISHES
from portion_estimator import PortionEstimator
from vlm_grounding_pipeline import VLMGroundedFoodAnalyzer

# Base paths
BASE_DIR = CURRENT_DIR
CONFIG_VAL_PATH = os.path.join(BASE_DIR, 'configs/val/grounding_dino_swin_t_vifood_val.py')
NUTRITION_PATH = os.path.join(BASE_DIR, 'nutrition_vifood_51.json')
EXAMPLE_DIR = "/home/atin/tuan/SoPSoP/grounding_data/vifood/images/val2017"

MODEL_CONFIGS = {
    "Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)": {
        "config": CONFIG_VAL_PATH,
        "weights": os.path.join(BASE_DIR, 'work_dirs/vifood_multi_res800/iter_10000.pth'),
        "description": "Mô hình thế hệ mới nhất: Tăng cường x3 Multi-Prompting tiếng Việt kết hợp huấn luyện đa tỉ lệ High-Res 800x1333. Đạt kỷ lục Average Recall 56.5%, mAP_50 7.5%."
    },
    "Exp 3: Full VI Caption Grounding (Đóng góp cốt lõi ⭐)": {
        "config": CONFIG_VAL_PATH,
        "weights": os.path.join(BASE_DIR, 'work_dirs/vifood_vi_full_1k/iter_10000.pth'),
        "description": "Mô hình Visual Grounding huấn luyện trên câu miêu tả tự nhiên tiếng Việt phong phú. Đạt Recall 54.3%, mAP_75: 0.066 (+144%)."
    },
    "Exp 1: Short VI Prompt": {
        "config": CONFIG_VAL_PATH,
        "weights": os.path.join(BASE_DIR, 'work_dirs/vifood_1k/iter_10000.pth'),
        "description": "Mô hình fine-tune trên nhãn tiếng Việt ngắn ngăn cách bởi dấu chấm ('phở . bánh mì .')."
    },
    "Zero-Shot Baseline (Pretrained)": {
        "config": CONFIG_VAL_PATH,
        "weights": '/home/atin/tuan/SoPSoP/huggingface/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth',
        "description": "Mô hình Swin-T gốc chưa fine-tune trên dữ liệu món ăn Việt Nam."
    }
}

# Load Nutrition Database
with open(NUTRITION_PATH, 'r', encoding='utf-8') as f:
    NUTRITION_DB = json.load(f)

DISH_KEYS = sorted(list(NUTRITION_DB.keys()), key=lambda x: len(x), reverse=True)

# Khởi tạo pipeline components
PORTION_ESTIMATOR = PortionEstimator(NUTRITION_DB)
VLM_DISCOVERER = VLMFoodDiscoverer()

LOADED_MODELS = {}

def get_model(model_name):
    if model_name not in LOADED_MODELS:
        meta = MODEL_CONFIGS[model_name]
        print(f"[App] Đang tải model: {model_name} từ {meta['weights']} ...")
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        model = init_detector(meta['config'], meta['weights'], device=device)
        LOADED_MODELS[model_name] = model
        print("[App] Model tải thành công!")
    return LOADED_MODELS[model_name]

# Warmup model mặc định Exp 4
try:
    get_model("Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)")
except Exception as e:
    print(f"[App] Cảnh báo khởi động model mặc định: {e}")

# Các quy tắc bóc tách câu tiếng Việt cho chế độ thủ công
STOP_WORDS = ["tìm", "chỉ", "ra", "xem", "cho", "tôi", "ở", "đâu", "đĩa", "bát", "tô", "phần", "nồi", "ly", "cốc", "chén", "các", "những", "cái", "ổ", "miếng", "con"]
CONTAINER_WORDS = ["đĩa", "dĩa", "bát", "tô", "phần", "nồi", "chén", "rổ", "khay", "ổ", "ly", "cốc"]
ADJECTIVES = ["nóng hổi", "thơm ngon", "giòn rụm", "vàng ươm", "chua ngọt", "đậm đà", "hấp dẫn", "nóng", "ngon", "giòn", "vàng"]

def parse_vietnamese_query(text):
    """Bóc tách thực thể món ăn từ câu tự nhiên tiếng Việt."""
    if not text:
        return "", []
    clean_text = text.strip()
    clauses = re.split(r'[,;]|\bvà\b|\bcùng\b|\bvới\b|\bkèm\b|\bbên cạnh\b|\bvới lại\b', clean_text, flags=re.IGNORECASE)
    entities = []
    for c in clauses:
        c = c.strip()
        if not c:
            continue
        for sw in STOP_WORDS:
            pattern = r'^\b' + re.escape(sw) + r'\b\s*'
            c = re.sub(pattern, '', c, flags=re.IGNORECASE).strip()
        words = c.split()
        if len(words) > 1 and words[0].lower() in CONTAINER_WORDS:
            c = " ".join(words[1:]).strip()
        for adj in ADJECTIVES:
            if c.lower().endswith(adj):
                c = c[:-len(adj)].strip()
        if c and len(c) >= 2:
            entities.append(c)
    if len(entities) == 0:
        for dish in DISH_KEYS:
            if re.search(r'\b' + re.escape(dish) + r'\b', clean_text, re.IGNORECASE):
                entities.append(dish)
    unique_entities = []
    for e in entities:
        if e.lower() not in [u.lower() for u in unique_entities]:
            unique_entities.append(e)
    if not unique_entities:
        unique_entities = [text.strip()]
    formatted_prompt = " . ".join(unique_entities) + " ."
    return formatted_prompt, unique_entities

def draw_visualizations(img_np, detected_boxes, portion_estimator):
    """Vẽ bounding box và tag dinh dưỡng nghệ thuật."""
    vis_img = img_np.copy()
    h, w = vis_img.shape[:2]
    colors = [
        (46, 204, 113),   # Xanh lục
        (52, 152, 219),   # Xanh dương
        (231, 76, 60),    # Đỏ cam
        (241, 196, 15),   # Vàng chanh
        (155, 89, 182),   # Tím
        (230, 126, 34),   # Cam rực
        (26, 188, 156),   # Xanh ngọc
    ]
    portion_items = []
    for i, item in enumerate(detected_boxes):
        box = item["box"]
        score = item["score"]
        name = item["label_name"]
        x1, y1, x2, y2 = map(int, box)
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        portion_info = portion_estimator.estimate_portion(
            bbox=[x1, y1, x2, y2],
            img_shape=(h, w),
            dish_key=name
        )
        portion_info["confidence"] = round(float(score), 3)
        portion_info["box"] = [x1, y1, x2, y2]
        portion_items.append(portion_info)
        color = colors[i % len(colors)]
        cv2.rectangle(vis_img, (x1, y1), (x2, y2), color, 3)
        conf_pct = int(score * 100)
        cal = portion_info["calories_kcal"]
        tag = f"{portion_info['name_vi']} ({conf_pct}%) | {cal}kcal [{portion_info['portion_label']}]"
        font_scale = 0.55
        thickness = 2
        (tw, th), baseline = cv2.getTextSize(tag, cv2.FONT_HERSHEY_SIMPLEX, font_scale, thickness)
        tag_y1 = max(0, y1 - th - 10)
        tag_y2 = y1
        cv2.rectangle(vis_img, (x1, tag_y1), (x1 + tw + 10, tag_y2), color, -1)
        cv2.putText(vis_img, tag, (x1 + 5, y1 - 6), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)
    return vis_img, portion_items

def apply_nms(detected_boxes, iou_thr=0.55):
    """NMS deduplication."""
    if not detected_boxes:
        return []
    sorted_boxes = sorted(detected_boxes, key=lambda x: x["score"], reverse=True)
    kept = []
    for b in sorted_boxes:
        box1 = b["box"]
        overlap = False
        for k in kept:
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

def render_html_dashboard(meal_summary, portion_items, vlm_info=None, hallucinated_dishes=None):
    """Tạo giao diện HTML hiện đại, chuẩn UI/UX cho kết quả dinh dưỡng."""
    cal = meal_summary.get("total_calories_kcal", 0)
    prot = meal_summary.get("total_protein_g", 0)
    carb = meal_summary.get("total_carbs_g", 0)
    fat = meal_summary.get("total_fat_g", 0)
    macros = meal_summary.get("macro_distribution", {"protein_pct": 0, "carbs_pct": 0, "fat_pct": 0})
    advice = meal_summary.get("dietary_advice", "")

    # VLM context block
    vlm_html = ""
    if vlm_info:
        meal_desc = vlm_info.get("meal_description", "")
        health_ass = vlm_info.get("health_assessment", "")
        cached_badge = '<span style="background: #27ae60; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">Cache VLM</span>' if vlm_info.get("cached") else '<span style="background: #2980b9; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem;">Gemini Live</span>'
        vlm_html = f"""
        <div style="background: #f8fafc; border-left: 4px solid #3b82f6; border-radius: 8px; padding: 14px 18px; margin-bottom: 18px;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <span style="font-weight: 700; color: #1e3a8a; font-size: 1rem;">🤖 Góc Nhìn VLM (Vision-Language AI)</span>
                {cached_badge}
            </div>
            <p style="margin: 0 0 8px 0; color: #334155; font-size: 0.95rem; line-height: 1.5;"><strong>🍽️ Mô tả bữa ăn:</strong> {meal_desc}</p>
            {f'<p style="margin: 0; color: #475569; font-size: 0.9rem; line-height: 1.5;"><strong>🩺 Đánh giá sức khỏe:</strong> {health_ass}</p>' if health_ass else ''}
        </div>
        """

    # Anti-Hallucination block
    hallucination_html = ""
    if hallucinated_dishes and len(hallucinated_dishes) > 0:
        badges = " ".join([f'<span style="background:#fee2e2; color:#991b1b; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem; margin-right: 4px;">{d}</span>' for d in hallucinated_dishes])
        hallucination_html = f"""
        <div style="background: #fff7ed; border-left: 4px solid #f97316; border-radius: 8px; padding: 10px 14px; margin-bottom: 16px; font-size: 0.88rem; color: #9a3412;">
            🛡️ <strong>Lọc ảo giác 2 tầng (Anti-Hallucination):</strong> VLM có gợi ý nhưng Detector không tìm thấy box khớp: {badges} <em>(Đã tự động loại bỏ để tránh cộng thừa calo)</em>
        </div>
        """
    elif vlm_info:
        hallucination_html = """
        <div style="background: #f0fdf4; border-left: 4px solid #22c55e; border-radius: 8px; padding: 8px 14px; margin-bottom: 16px; font-size: 0.88rem; color: #166534;">
            🛡️ <strong>Xác thực 2 tầng:</strong> Toàn bộ các món ăn được phát hiện đều đã được Grounding DINO kiểm chứng và định vị chính xác.
        </div>
        """

    # Macro distribution bar
    p_pct = macros.get("protein_pct", 0)
    c_pct = macros.get("carbs_pct", 0)
    f_pct = macros.get("fat_pct", 0)

    # Table of detected portions
    rows = ""
    for item in portion_items:
        rows += f"""
        <tr style="border-bottom: 1px solid #e2e8f0;">
            <td style="padding: 10px; font-weight: 600; color: #0f172a;">{item['name_vi']}<br><span style="font-size: 0.75rem; color: #64748b;">{item.get('name_en', '')}</span></td>
            <td style="padding: 10px; text-align: center;"><span style="background:#e0f2fe; color:#0369a1; padding: 3px 8px; border-radius: 6px; font-size: 0.82rem; font-weight: 600;">{item['portion_label']}</span></td>
            <td style="padding: 10px; text-align: center; color: #475569;">{item.get('relative_area_pct', 0)}%</td>
            <td style="padding: 10px; text-align: right; font-weight: 700; color: #ea580c;">{item['calories_kcal']}</td>
            <td style="padding: 10px; text-align: right; color: #16a34a;">{item['protein_g']}g</td>
            <td style="padding: 10px; text-align: right; color: #ca8a04;">{item['carbs_g']}g</td>
            <td style="padding: 10px; text-align: right; color: #dc2626;">{item['fat_g']}g</td>
            <td style="padding: 10px; text-align: center;"><span style="background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.8rem; font-weight: 600;">{int(item['confidence']*100)}%</span></td>
        </tr>
        """

    if not rows:
        rows = '<tr><td colspan="8" style="padding: 20px; text-align: center; color: #94a3b8;">Không phát hiện thấy món ăn nào vượt qua ngưỡng tin cậy. Hãy thử giảm ngưỡng xuống 0.15.</td></tr>'

    html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        {vlm_html}
        {hallucination_html}

        <!-- Macro 4 Cards Grid -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 16px;">
            <div style="background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%); border: 1px solid #fed7aa; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.85rem; color: #9a3412; font-weight: 600; text-transform: uppercase;">⚡ Năng Lượng</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #ea580c; margin: 4px 0;">{cal}</div>
                <div style="font-size: 0.8rem; color: #c2410c;">kcal</div>
            </div>
            <div style="background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%); border: 1px solid #bbf7d0; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.85rem; color: #166534; font-weight: 600; text-transform: uppercase;">🥩 Đạm (Protein)</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #16a34a; margin: 4px 0;">{prot}</div>
                <div style="font-size: 0.8rem; color: #15803d;">gam ({p_pct}%)</div>
            </div>
            <div style="background: linear-gradient(135deg, #fefce8 0%, #fef9c3 100%); border: 1px solid #fef08a; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.85rem; color: #854d0e; font-weight: 600; text-transform: uppercase;">🍚 Tinh Bột (Carbs)</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #ca8a04; margin: 4px 0;">{carb}</div>
                <div style="font-size: 0.8rem; color: #a16207;">gam ({c_pct}%)</div>
            </div>
            <div style="background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border: 1px solid #fecaca; border-radius: 10px; padding: 14px; text-align: center;">
                <div style="font-size: 0.85rem; color: #991b1b; font-weight: 600; text-transform: uppercase;">🥑 Chất Béo (Fat)</div>
                <div style="font-size: 1.8rem; font-weight: 800; color: #dc2626; margin: 4px 0;">{fat}</div>
                <div style="font-size: 0.8rem; color: #b91c1c;">gam ({f_pct}%)</div>
            </div>
        </div>

        <!-- Macro Distribution Stacked Bar -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 18px; margin-bottom: 16px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.85rem; font-weight: 600; margin-bottom: 8px;">
                <span>Cơ cấu calo đa lượng (Macronutrients)</span>
                <span>Đạm: {p_pct}% | Tinh bột: {c_pct}% | Béo: {f_pct}%</span>
            </div>
            <div style="display: flex; height: 16px; border-radius: 8px; overflow: hidden; background: #e2e8f0;">
                <div style="width: {p_pct}%; background: #16a34a;" title="Protein: {p_pct}%"></div>
                <div style="width: {c_pct}%; background: #ca8a04;" title="Carbs: {c_pct}%"></div>
                <div style="width: {f_pct}%; background: #dc2626;" title="Fat: {f_pct}%"></div>
            </div>
            <div style="margin-top: 10px; font-size: 0.88rem; color: #334155; line-height: 1.4;">
                {advice}
            </div>
        </div>

        <!-- Table of Detected Items -->
        <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 10px; overflow: hidden;">
            <div style="padding: 12px 16px; background: #f8fafc; border-bottom: 1px solid #e2e8f0; font-weight: 700; color: #1e293b;">
                📋 Danh Sách Khẩu Phần Chi Tiết ({len(portion_items)} phần phát hiện)
            </div>
            <table style="width: 100%; border-collapse: collapse; font-size: 0.9rem;">
                <thead>
                    <tr style="background: #f1f5f9; color: #475569; text-align: left;">
                        <th style="padding: 10px;">Món Ăn</th>
                        <th style="padding: 10px; text-align: center;">Khẩu Phần</th>
                        <th style="padding: 10px; text-align: center;">Diện Tích Box</th>
                        <th style="padding: 10px; text-align: right;">Calo</th>
                        <th style="padding: 10px; text-align: right;">Đạm</th>
                        <th style="padding: 10px; text-align: right;">Carb</th>
                        <th style="padding: 10px; text-align: right;">Béo</th>
                        <th style="padding: 10px; text-align: center;">Confidence</th>
                    </tr>
                </thead>
                <tbody>
                    {rows}
                </tbody>
            </table>
        </div>
    </div>
    """
    return html

# ════════════════════════════════════════════════════════════════
# CORE INFERENCE FUNCTIONS
# ════════════════════════════════════════════════════════════════

def auto_vlm_predict(image, conf_thr, model_choice, api_key_override=""):
    """Pipeline Tab 1: AI Tự Động (VLM-guided Zero-Prompt)."""
    if image is None:
        return None, "<div style='padding:20px; color:#ef4444;'>⚠️ Vui lòng tải ảnh lên hoặc chụp ảnh từ camera.</div>", "⏱️ Chưa có ảnh đầu vào."

    if api_key_override and api_key_override.strip():
        VLM_DISCOVERER.set_api_key(api_key_override.strip())

    t0 = time.time()
    pil_img = Image.fromarray(image).convert('RGB') if isinstance(image, np.ndarray) else image.convert('RGB')
    img_np = np.array(pil_img)
    img_h, img_w = img_np.shape[:2]
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    # 1. VLM Discovery
    t_vlm_0 = time.time()
    vlm_info = VLM_DISCOVERER.discover_dishes(pil_img, use_cache=True)
    vlm_latency_ms = (time.time() - t_vlm_0) * 1000
    canonical = vlm_info.get("canonical_dishes", [])
    known_dishes = [d for d in canonical if d in CANONICAL_51_DISHES]
    prompt_dishes = known_dishes if known_dishes else canonical[:4]
    if not prompt_dishes:
        prompt_dishes = ["món ăn"]
    detector_prompt = " . ".join(prompt_dishes) + " ."

    # 2. Grounding DINO Detection
    model = get_model(model_choice)
    t_det_0 = time.time()
    with torch.no_grad():
        result = inference_detector(model, img_bgr, text_prompt=detector_prompt, custom_entities=True)
    detector_latency_ms = (time.time() - t_det_0) * 1000

    pred = result.pred_instances
    mask = pred.scores >= conf_thr
    boxes = pred.bboxes[mask].cpu().numpy()
    scores = pred.scores[mask].cpu().numpy()
    labels = pred.labels[mask].cpu().numpy()
    label_names_all = getattr(pred, 'label_names', None)

    detected_boxes = []
    for i, (box, score) in enumerate(zip(boxes, scores)):
        if label_names_all is not None and i < len(label_names_all):
            label_name = label_names_all[i]
        else:
            idx = int(labels[i])
            label_name = canonical[idx] if idx < len(canonical) else f"dish_{idx}"
        detected_boxes.append({
            "box": [float(c) for c in box],
            "score": float(score),
            "label_name": label_name
        })

    # NMS Deduplication
    detected_boxes = apply_nms(detected_boxes, iou_thr=0.55)

    # 3. Portion Estimation & Visualization
    vis_img, portion_items = draw_visualizations(img_np, detected_boxes, PORTION_ESTIMATOR)

    # 4. Anti-Hallucination Check
    verified_dishes_set = {p["dish_key"].lower() for p in portion_items}
    hallucinated_dishes = []
    for d in vlm_info.get("canonical_dishes", []):
        if not any(d.lower() in v or v in d.lower() for v in verified_dishes_set):
            hallucinated_dishes.append(d)

    # 5. Summarize Meal
    meal_summary = PORTION_ESTIMATOR.summarize_meal(portion_items)

    total_latency_ms = (time.time() - t0) * 1000
    fps = 1000.0 / total_latency_ms if total_latency_ms > 0 else 0

    timing_badge = f"""
    ⏱️ **Độ trễ toàn trình:** `{total_latency_ms:.1f} ms` ({fps:.1f} FPS) | VLM: `{vlm_latency_ms:.1f} ms` | Detector: `{detector_latency_ms:.1f} ms` | Đã nhận diện: `{len(portion_items)} món`
    """

    dashboard_html = render_html_dashboard(
        meal_summary=meal_summary,
        portion_items=portion_items,
        vlm_info=vlm_info,
        hallucinated_dishes=hallucinated_dishes
    )

    return vis_img, dashboard_html, timing_badge

def manual_predict(image, text_prompt, conf_thr, model_choice, smart_parse):
    """Pipeline Tab 2: Nhập prompt thủ công theo từ khóa / câu mô tả."""
    if image is None:
        return None, "<div style='padding:20px; color:#ef4444;'>⚠️ Vui lòng tải ảnh lên.</div>", "⏱️ Chưa có ảnh đầu vào."

    if not text_prompt or text_prompt.strip() == "":
        text_prompt = "phở . bánh mì . bánh tráng . bún bò Huế . cơm tấm . gỏi cuốn . bánh xèo ."

    prompt_clean = text_prompt.strip()
    if smart_parse:
        formatted_prompt, entities = parse_vietnamese_query(prompt_clean)
        prompt_to_model = formatted_prompt
    else:
        entities = [p.strip() for p in prompt_clean.split('.') if p.strip()]
        prompt_to_model = prompt_clean

    t0 = time.time()
    pil_img = Image.fromarray(image).convert('RGB') if isinstance(image, np.ndarray) else image.convert('RGB')
    img_np = np.array(pil_img)
    img_h, img_w = img_np.shape[:2]
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    model = get_model(model_choice)
    t_det_0 = time.time()
    with torch.no_grad():
        result = inference_detector(model, img_bgr, text_prompt=prompt_to_model, custom_entities=True)
    det_latency_ms = (time.time() - t_det_0) * 1000

    pred = result.pred_instances
    mask = pred.scores >= conf_thr
    boxes = pred.bboxes[mask].cpu().numpy()
    scores = pred.scores[mask].cpu().numpy()
    labels = pred.labels[mask].cpu().numpy()
    label_names_all = getattr(pred, 'label_names', None)

    detected_boxes = []
    for i, (box, score) in enumerate(zip(boxes, scores)):
        if label_names_all is not None and i < len(label_names_all):
            label_name = label_names_all[i]
        else:
            idx = int(labels[i])
            label_name = entities[idx] if idx < len(entities) else f"dish_{idx}"
        detected_boxes.append({
            "box": [float(c) for c in box],
            "score": float(score),
            "label_name": label_name
        })

    detected_boxes = apply_nms(detected_boxes, iou_thr=0.55)
    vis_img, portion_items = draw_visualizations(img_np, detected_boxes, PORTION_ESTIMATOR)
    meal_summary = PORTION_ESTIMATOR.summarize_meal(portion_items)

    total_latency_ms = (time.time() - t0) * 1000
    fps = 1000.0 / total_latency_ms if total_latency_ms > 0 else 0

    timing_badge = f"""
    ⏱️ **Độ trễ Detector:** `{det_latency_ms:.1f} ms` ({fps:.1f} FPS) | Món bóc tách từ prompt: `{'`, `'.join(entities)}` | Đã nhận diện: `{len(portion_items)} món`
    """

    vlm_dummy = {
        "meal_description": f"Chế độ tìm kiếm thủ công theo prompt: '{text_prompt}'",
        "health_assessment": "",
        "cached": False
    }

    dashboard_html = render_html_dashboard(
        meal_summary=meal_summary,
        portion_items=portion_items,
        vlm_info=vlm_dummy,
        hallucinated_dishes=[]
    )

    return vis_img, dashboard_html, timing_badge


# ════════════════════════════════════════════════════════════════
# GRADIO UI DEFINITION
# ════════════════════════════════════════════════════════════════

CUSTOM_CSS = """
.container { max-width: 1320px; margin: auto; }
.header-box { text-align: center; padding: 24px 20px; background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 50%, #0369a1 100%); color: white; border-radius: 14px; margin-bottom: 20px; box-shadow: 0 6px 20px rgba(0,0,0,0.15); }
.header-box h1 { font-size: 2.3rem; font-weight: 800; margin-bottom: 8px; color: #ffffff; letter-spacing: -0.5px; }
.header-box p { font-size: 1.1rem; opacity: 0.92; margin: 0; }
.badge-group { display: flex; justify-content: center; gap: 8px; flex-wrap: wrap; margin-top: 12px; }
.badge-item { display: inline-block; padding: 4px 14px; background: rgba(255,255,255,0.18); border-radius: 20px; font-size: 0.85rem; font-weight: 600; color: #f1f5f9; backdrop-filter: blur(4px); }
"""

EXAMPLES_TAB1 = [
    [os.path.join(EXAMPLE_DIR, "srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg"), 0.20, "Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)"],
    [os.path.join(EXAMPLE_DIR, "srcB_604_jpg.rf.1b4975927ccb1b3dd003d7fc87d94ee5.jpg"), 0.20, "Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)"],
    [os.path.join(EXAMPLE_DIR, "srcB_62_jpg.rf.0d726dfcf5c7acfda31cac058481f3a8.jpg"), 0.20, "Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)"],
    [os.path.join(EXAMPLE_DIR, "srcB_604_jpg.rf.8acf9d99c36a035ab7805852cdb7b856.jpg"), 0.20, "Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)"],
]

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue", secondary_hue="emerald"), css=CUSTOM_CSS, title="ViFood AI - VLM Grounding & Nutrition") as demo:
    with gr.Column(elem_classes="container"):
        # Header
        gr.HTML("""
        <div class="header-box">
            <h1>🍜 Smart Vietnamese Food AI</h1>
            <p>Hệ Thống Tự Động Khám Phá Món Ăn Bằng VLM, Định Vị Visual Grounding & Ước Lượng Dinh Dưỡng</p>
            <div class="badge-group">
                <span class="badge-item">🤖 Gemini VLM Auto-Discovery (Zero-Prompt)</span>
                <span class="badge-item">🎯 Grounding DINO Swin-T Exp 4 (Recall 56.5%)</span>
                <span class="badge-item">🥗 Portion Estimator & Nutrition DB 51 Món</span>
                <span class="badge-item">🛡️ Anti-Hallucination 2 Tầng</span>
            </div>
        </div>
        """)

        with gr.Tabs():
            # ──────────────────────────────────────────────────────────
            # TAB 1: AI TỰ ĐỘNG (VLM-GUIDED ZERO-PROMPT)
            # ──────────────────────────────────────────────────────────
            with gr.TabItem("🤖 AI Tự Động Khám Phá (Zero-Prompt ⭐)"):
                with gr.Row():
                    # Cột trái: Tải ảnh
                    with gr.Column(scale=5):
                        t1_input_img = gr.Image(
                            type="numpy",
                            label="1. Tải ảnh hoặc Chụp trực tiếp từ Camera",
                            sources=["upload", "webcam", "clipboard"]
                        )
                        with gr.Row():
                            t1_conf_slider = gr.Slider(
                                minimum=0.10, maximum=0.80, value=0.20, step=0.05,
                                label="Ngưỡng Tin Cậy Detector (Confidence)"
                            )
                            t1_model_dropdown = gr.Dropdown(
                                choices=list(MODEL_CONFIGS.keys()),
                                value="Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)",
                                label="Mô Hình Detector"
                            )
                        with gr.Accordion("⚙️ Cấu Hình API Key VLM (Tùy chọn)", open=False):
                            t1_api_key_input = gr.Textbox(
                                label="Google Gemini API Key",
                                placeholder="Key mặc định đã được cấu hình sẵn. Chỉ nhập nếu muốn dùng key riêng.",
                                type="password",
                                value=""
                            )
                        t1_detect_btn = gr.Button("✨ AI TỰ ĐỘNG KHÁM PHÁ & PHÂN TÍCH", variant="primary", size="lg")

                        gr.Markdown("### 🖼️ Ảnh Mẫu Kiểm Thử Tự Động:")
                        gr.Examples(
                            examples=EXAMPLES_TAB1,
                            inputs=[t1_input_img, t1_conf_slider, t1_model_dropdown],
                            label="Click để nạp nhanh ảnh mẫu:",
                            cache_examples=False
                        )

                    # Cột phải: Kết quả trực quan
                    with gr.Column(scale=7):
                        t1_perf_output = gr.Markdown("⏱️ *Chờ ảnh đầu vào...*")
                        t1_output_img = gr.Image(type="numpy", label="Ảnh Kết Quả Định Vị (Visual Grounding)")
                        t1_dashboard_output = gr.HTML("<div style='color:#64748b; padding:20px; text-align:center;'>Bảng phân tích dinh dưỡng đa lượng sẽ hiển thị tại đây sau khi AI nhận diện.</div>")

            # ──────────────────────────────────────────────────────────
            # TAB 2: NHẬP PROMPT THỦ CÔNG
            # ──────────────────────────────────────────────────────────
            with gr.TabItem("✍️ Nhập Prompt Thủ Công"):
                with gr.Row():
                    with gr.Column(scale=5):
                        t2_input_img = gr.Image(type="numpy", label="1. Tải Ảnh Mâm Cơm", sources=["upload", "clipboard"])
                        t2_prompt_input = gr.Textbox(
                            label="2. Câu Tìm Kiếm / Mô Tả Tiếng Việt",
                            placeholder="Ví dụ: 'tìm tôm chiên và chả' hoặc 'đĩa bánh tráng nướng'...",
                            value="tìm đĩa bánh tráng",
                            lines=2
                        )
                        t2_smart_parse = gr.Checkbox(
                            value=True,
                            label="✨ Tự động bóc tách thực thể món ăn từ câu tiếng Việt tự nhiên"
                        )
                        with gr.Accordion("💡 Phím tắt Prompt nhanh", open=False):
                            with gr.Row():
                                btn_pho = gr.Button("🍜 Phở & Rau sống", size="sm")
                                btn_banhxeo = gr.Button("🥞 Bánh xèo & Khọt", size="sm")
                                btn_comtam = gr.Button("🍛 Cơm tấm sườn", size="sm")
                                btn_banhmi = gr.Button("🥖 Bánh mì", size="sm")
                        with gr.Row():
                            t2_conf_slider = gr.Slider(minimum=0.10, maximum=0.80, value=0.25, step=0.05, label="Ngưỡng Tin Cậy")
                            t2_model_dropdown = gr.Dropdown(
                                choices=list(MODEL_CONFIGS.keys()),
                                value="Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)",
                                label="Mô Hình"
                            )
                        t2_detect_btn = gr.Button("🚀 ĐỊNH VỊ THEO PROMPT", variant="primary", size="lg")

                    with gr.Column(scale=7):
                        t2_perf_output = gr.Markdown("⏱️ *Sẵn sàng xử lý...*")
                        t2_output_img = gr.Image(type="numpy", label="Ảnh Kết Quả")
                        t2_dashboard_output = gr.HTML("<div style='color:#64748b; padding:20px; text-align:center;'>Kết quả dinh dưỡng theo prompt thủ công sẽ xuất hiện tại đây.</div>")

            # ──────────────────────────────────────────────────────────
            # TAB 3: BÁO CÁO THỰC NGHIỆM KHOA HỌC
            # ──────────────────────────────────────────────────────────
            with gr.TabItem("📊 Báo Cáo Thực Nghiệm (Luận Văn)"):
                gr.Markdown("""
## 🏆 BẢNG SO SÁNH HIỆU NĂNG 4 MÔ HÌNH TRÊN TẬP VALIDATION CHUẨN COCO METRIC
*(100 ảnh validation độc lập, 374 nhãn ground-truth, 51 lớp món ăn Việt Nam)*

| Mô hình / Thí nghiệm | Dạng Prompt Huấn Luyện | mAP (0.50:0.95) | mAP_50 | mAP_75 | mAP_m | Average Recall (AR) | Ý nghĩa Khoa học |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Zero-Shot Baseline** | Pretrained Swin-T gốc | 0.026 | 0.034 | 0.031 | 0.017 | 0.392 | Đối sánh ban đầu |
| **Exp 1: Short VI** | Nhãn ngắn tiếng Việt (`"phở . bánh mì ."`) | 0.024 | 0.037 | 0.027 | **0.224** | 0.233 | Thiếu ngữ cảnh miêu tả |
| **Exp 2: Short EN** | Nhãn ngắn tiếng Anh (`"Vietnamese Pho ."`) | 0.055 | 0.084 | 0.055 | 0.102 | 0.368 | Đo Cross-lingual gap |
| **Exp 3: Full VI** | Câu tự nhiên tiếng Việt phong phú | **0.055** | **0.074** | **0.066** | **0.199** | **0.543** | Đóng góp cốt lõi (+133% Recall) |
| **Exp 4: Multi-Res 800** | Multi-Prompt x3 + Đa tỉ lệ 800x1333 | **0.054** | **0.075** | **0.060** | **0.218** | **0.565** | **Kỷ lục Average Recall 56.5%** |

---

### 🔬 3 Đóng Góp Nổi Bật Cho Đề Tài:
1. **Pipeline VLM-guided Grounding (Mới)**: Loại bỏ sự phụ thuộc vào text prompt người dùng. VLM tự nhận diện ngữ nghĩa món ăn, truyền sang Grounding DINO để định vị pixel-level chính xác, kết hợp cơ chế kiểm chứng 2 tầng chống ảo giác (Anti-Hallucination).
2. **Kỷ lục Average Recall 56.5%**: Sự kết hợp giữa Multi-Prompting tiếng Việt và phân giải High-Res 800x1333 giúp độ bao phủ món ăn đạt đỉnh cao nhất từ trước đến nay.
3. **Smart Nutrition Analysis**: Tự động ước lượng khẩu phần (Nhỏ/Vừa/Lớn) từ diện tích Bounding Box và tính toán tổng năng lượng, cơ cấu đạm/tinh bột/chất béo cho toàn bữa ăn.
""")

            # ──────────────────────────────────────────────────────────
            # TAB 4: TỪ ĐIỂN 51 MÓN ĂN & DINH DƯỠNG
            # ──────────────────────────────────────────────────────────
            with gr.TabItem("📖 Từ Điển 51 Món Dinh Dưỡng"):
                gr.Markdown("### 🥗 Cơ sở tri thức dinh dưỡng chuẩn của 51 món ăn Việt Nam:")
                db_rows = []
                for k, v in NUTRITION_DB.items():
                    db_rows.append(
                        f"| **{v['name_vi']}** | *{v['name_en']}* | `{v['category']}` | {v['serving']} | **{v['calories_kcal']}** | {v['protein_g']}g | {v['carbs_g']}g | {v['fat_g']}g | {v['note']} |"
                    )
                db_table = "\n".join(db_rows)
                gr.Markdown(f"""
| Tên Món Ăn | Tên Tiếng Anh | Phân loại | Khẩu phần chuẩn | Năng lượng (kcal) | Đạm | Tinh bột | Béo | Ghi chú văn hóa |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: | :--- |
{db_table}
""")

    # Event handlers
    t1_detect_btn.click(
        fn=auto_vlm_predict,
        inputs=[t1_input_img, t1_conf_slider, t1_model_dropdown, t1_api_key_input],
        outputs=[t1_output_img, t1_dashboard_output, t1_perf_output]
    )

    t2_detect_btn.click(
        fn=manual_predict,
        inputs=[t2_input_img, t2_prompt_input, t2_conf_slider, t2_model_dropdown, t2_smart_parse],
        outputs=[t2_output_img, t2_dashboard_output, t2_perf_output]
    )

    btn_pho.click(lambda: "Bát phở bò thơm lừng với nước dùng quế hồi và đĩa rau sống xanh mướt.", None, t2_prompt_input)
    btn_banhxeo.click(lambda: "Đĩa bánh xèo vàng giòn rụm bên cạnh bánh khọt tôm tươi và rổ rau sống.", None, t2_prompt_input)
    btn_comtam.click(lambda: "Dĩa cơm tấm sườn nướng mỡ hành thơm phức và chả trứng hấp.", None, t2_prompt_input)
    btn_banhmi.click(lambda: "Ổ bánh mì kẹp thịt giòn rụm với pate và đồ chua.", None, t2_prompt_input)

if __name__ == "__main__":
    print("[App] Khởi động Smart Vietnamese Food AI trên port 7861...")
    demo.launch(
        server_name="0.0.0.0",
        server_port=7861,
        share=False,
        allowed_paths=[
            '/home/atin/tuan/SoPSoP/grounding_data/vifood/images',
            '/home/atin/tuan/SoPSoP/grounding_data/vifood/images/val2017'
        ]
    )
