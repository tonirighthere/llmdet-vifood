#!/usr/bin/env python3
"""
portion_estimator.py
====================
Module ước lượng kích thước khẩu phần (Portion Estimation) và tính toán
năng lượng (calories), protein, carbs, fat dựa trên diện tích Bounding Box.

Phương pháp:
  - Tính tỷ lệ diện tích Bounding Box so với tổng thể bức ảnh (Relative Area).
  - Phân loại khẩu phần theo nhóm thực phẩm (Món nước/tô, Món đĩa, Nước chấm, v.v.).
  - Điều chỉnh định lượng dinh dưỡng từ nutrition_vifood_51.json theo hệ số tỉ lệ.
"""

import os
import json
from typing import Dict, Any, Tuple, Optional, List

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
NUTRITION_PATH = os.path.join(CURRENT_DIR, 'nutrition_vifood_51.json')

with open(NUTRITION_PATH, 'r', encoding='utf-8') as f:
    NUTRITION_DB = json.load(f)

# Phân nhóm đặc thù món ăn để hiệu chỉnh ngưỡng diện tích
DIP_DISHES = {"nước chấm"}
BOWL_DISHES = {"phở", "bún", "bún bò Huế", "bún riêu", "bún mắm", "bánh canh", "hủ tiếu", "mì Quảng", "cháo lòng", "canh chua", "súp cua"}
SIDE_VEGGIES = {"rau sống", "rau luộc", "rau xào"}


class PortionEstimator:
    """Ước lượng khẩu phần và tính toán dinh dưỡng chi tiết."""

    def __init__(self, nutrition_db: Optional[Dict[str, Any]] = None):
        self.db = nutrition_db or NUTRITION_DB

    def estimate_portion(self, bbox: List[float], img_shape: Tuple[int, int], dish_key: str) -> Dict[str, Any]:
        """
        Ước lượng khẩu phần từ bounding box.

        Args:
            bbox: [x1, y1, x2, y2] tọa độ pixel
            img_shape: (height, width) của ảnh
            dish_key: tên món chuẩn trong nutrition DB (vd: 'bánh tráng', 'phở')

        Returns:
            dict chứa thông tin khẩu phần và dinh dưỡng đã được scale
        """
        img_h, img_w = img_shape[:2]
        img_area = max(float(img_h * img_w), 1.0)

        x1, y1, x2, y2 = bbox
        box_w = max(0.0, float(x2 - x1))
        box_h = max(0.0, float(y2 - y1))
        box_area = box_w * box_h
        relative_ratio = box_area / img_area
        relative_pct = round(relative_ratio * 100, 1)

        # Lấy thông tin gốc từ DB dinh dưỡng (nếu không có thì dùng fallback 'món ăn khác')
        canonical_key = dish_key.lower().strip()
        base_item = self.db.get(canonical_key, self.db.get('món ăn khác', {
            "name_vi": dish_key.title(),
            "name_en": dish_key,
            "serving": "1 phần tiêu chuẩn",
            "calories_kcal": 250,
            "protein_g": 10.0,
            "carbs_g": 30.0,
            "fat_g": 8.0,
            "category": "Món ăn chung",
            "note": ""
        }))

        # Xác định hệ số scale dựa trên đặc thù món và diện tích
        if canonical_key in DIP_DISHES:
            # Chén nước chấm luôn là 1 phần nhỏ chuẩn, ít khi tính khẩu phần khổng lồ
            if relative_ratio < 0.015:
                scale = 0.5
                label = "Nhỏ (ít chấm)"
            elif relative_ratio < 0.06:
                scale = 1.0
                label = "Tiêu chuẩn (1 chén)"
            else:
                scale = 1.5
                label = "Lớn (bát chấm chung)"

        elif canonical_key in BOWL_DISHES:
            # Món tô nước (phở, bún) thường chiếm diện tích lớn
            if relative_ratio < 0.08:
                scale = 0.6
                label = "Tô nhỏ"
            elif relative_ratio < 0.22:
                scale = 1.0
                label = "Tô vừa (chuẩn 1 người)"
            elif relative_ratio < 0.40:
                scale = 1.4
                label = "Tô lớn / Đặc biệt"
            else:
                scale = 1.8
                label = "Tô đại / Mâm lẩu"

        elif canonical_key in SIDE_VEGGIES:
            if relative_ratio < 0.05:
                scale = 0.6
                label = "Đĩa nhỏ ăn kèm"
            elif relative_ratio < 0.18:
                scale = 1.0
                label = "Đĩa vừa"
            else:
                scale = 1.5
                label = "Đĩa lớn / Rổ rau đầy"

        else:
            # Các món đĩa, bánh, cơm, thịt thông thường
            if relative_ratio < 0.04:
                scale = 0.5
                label = "Khẩu phần nhỏ"
            elif relative_ratio < 0.15:
                scale = 1.0
                label = "Khẩu phần vừa (chuẩn 1 người)"
            elif relative_ratio < 0.30:
                scale = 1.5
                label = "Khẩu phần lớn"
            else:
                scale = 2.0
                label = "Khẩu phần gia đình / Dùng chung"

        # Tính toán dinh dưỡng đã hiệu chỉnh
        base_cal = base_item.get("calories_kcal", 200)
        base_prot = base_item.get("protein_g", 10.0)
        base_carb = base_item.get("carbs_g", 25.0)
        base_fat = base_item.get("fat_g", 7.0)

        scaled_cal = round(base_cal * scale)
        scaled_prot = round(base_prot * scale, 1)
        scaled_carb = round(base_carb * scale, 1)
        scaled_fat = round(base_fat * scale, 1)

        return {
            "dish_key": canonical_key,
            "name_vi": base_item.get("name_vi", canonical_key.title()),
            "name_en": base_item.get("name_en", ""),
            "category": base_item.get("category", ""),
            "original_serving": base_item.get("serving", "1 phần"),
            "portion_label": label,
            "portion_scale": scale,
            "relative_area_pct": relative_pct,
            "calories_kcal": scaled_cal,
            "protein_g": scaled_prot,
            "carbs_g": scaled_carb,
            "fat_g": scaled_fat,
            "note": base_item.get("note", "")
        }

    def summarize_meal(self, detected_portions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Tổng hợp dinh dưỡng toàn bộ bữa ăn từ danh sách các phần phát hiện."""
        total_cal = sum(p["calories_kcal"] for p in detected_portions)
        total_prot = round(sum(p["protein_g"] for p in detected_portions), 1)
        total_carb = round(sum(p["carbs_g"] for p in detected_portions), 1)
        total_fat = round(sum(p["fat_g"] for p in detected_portions), 1)

        # Tính tỷ lệ phần trăm macro năng lượng
        # 1g Protein = 4 kcal, 1g Carb = 4 kcal, 1g Fat = 9 kcal
        cal_from_prot = total_prot * 4
        cal_from_carb = total_carb * 4
        cal_from_fat = total_fat * 9
        total_macro_cal = max(cal_from_prot + cal_from_carb + cal_from_fat, 1.0)

        prot_pct = round((cal_from_prot / total_macro_cal) * 100)
        carb_pct = round((cal_from_carb / total_macro_cal) * 100)
        fat_pct = round((cal_from_fat / total_macro_cal) * 100)

        # Đánh giá cân bằng dinh dưỡng
        advice = []
        if total_cal > 800:
            advice.append("⚠️ Bữa ăn có tổng calo khá cao (>800 kcal), thích hợp cho người vận động mạnh hoặc bữa chính no nê.")
        elif total_cal < 350 and total_cal > 0:
            advice.append("💡 Bữa ăn nhẹ hoặc ăn kiêng (<350 kcal), có thể bổ sung thêm năng lượng nếu cần làm việc nhiều.")

        if carb_pct > 60:
            advice.append("🍚 Tỷ lệ tinh bột chiếm đa số (>60%), nếu đang giảm cân hoặc kiểm soát đường huyết nên tăng cường rau xanh.")
        if prot_pct >= 25:
            advice.append("💪 Bữa ăn dồi dào chất đạm (>25% năng lượng), rất tốt cho việc phát triển cơ bắp và tạo cảm giác no lâu.")
        if fat_pct > 35:
            advice.append("🧈 Tỷ lệ chất béo cao (>35%), nên hạn chế các món chiên xào nhiều dầu mỡ.")

        if not advice:
            advice.append("✅ Bữa ăn có cơ cấu dinh dưỡng tương đối hài hòa và cân đối.")

        return {
            "total_items": len(detected_portions),
            "total_calories_kcal": total_cal,
            "total_protein_g": total_prot,
            "total_carbs_g": total_carb,
            "total_fat_g": total_fat,
            "macro_distribution": {
                "protein_pct": prot_pct,
                "carbs_pct": carb_pct,
                "fat_pct": fat_pct
            },
            "dietary_advice": " ".join(advice)
        }


if __name__ == '__main__':
    # Test portion estimator
    estimator = PortionEstimator()
    sample_box = [50, 50, 400, 350]
    sample_shape = (600, 600)
    result = estimator.estimate_portion(sample_box, sample_shape, 'bánh tráng')
    print("Test single portion estimation:")
    print(json.dumps(result, ensure_ascii=False, indent=2))

    summary = estimator.summarize_meal([result])
    print("\nTest meal summary:")
    print(json.dumps(summary, ensure_ascii=False, indent=2))
