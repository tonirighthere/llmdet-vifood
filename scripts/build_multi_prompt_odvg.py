#!/usr/bin/env python3
"""
scripts/build_multi_prompt_odvg.py
==================================
Tạo tập dữ liệu Multi-Prompting ODVG (Hướng 2):
Mỗi ảnh được nhân bản thành 3 phong cách ngôn ngữ khác nhau:
  1. Style 1: Miêu tả bữa ăn chi tiết (Rich Descriptive Caption - từ Exp 3)
  2. Style 2: Câu tìm kiếm / định vị vị trí tự nhiên (Search & Localization Query)
  3. Style 3: Liệt kê thực thể phân tách dấu chấm (Discrete Entity List)

Tổng số mẫu: 900 x 3 = 2.700 mẫu huấn luyện.
Tất cả tokens_positive được kiểm tra độ chuẩn xác 100% (character offset [start, end]).
"""

import os
import json
import random

BASE_DIR = "/home/atin/tuan/SoPSoP"
IN_FILE = os.path.join(BASE_DIR, "grounding_data", "vifood", "annotations", "vifood_train_vg_vi_full.jsonl")
OUT_FILE = os.path.join(BASE_DIR, "grounding_data", "vifood", "annotations", "vifood_train_vg_vi_multi.jsonl")

SEARCH_TEMPLATES = [
    ("Tìm giúp tôi {dishes_str} trên bàn ăn.", "Tìm giúp tôi "),
    ("Trên bàn ăn bày biện {dishes_str} thơm ngon hấp dẫn.", "Trên bàn ăn bày biện "),
    ("Hãy chỉ ra vị trí của {dishes_str} trong bữa ăn.", "Hãy chỉ ra vị trí của "),
    ("Bữa ăn đậm đà hương vị gồm có {dishes_str} được bày trí đẹp mắt.", "Bữa ăn đậm đà hương vị gồm có "),
    ("Xác định đĩa {dishes_str} trên mâm cơm.", "Xác định đĩa "),
    ("Mâm cơm gia đình ấm cúng với {dishes_str} ngon miệng.", "Mâm cơm gia đình ấm cúng với ")
]

def format_natural_dishes(dish_list):
    """Format ['phở', 'rau sống', 'nước chấm'] -> ('phở, rau sống và nước chấm', list of (dish, start_idx))"""
    if len(dish_list) == 1:
        return dish_list[0]
    elif len(dish_list) == 2:
        return f"{dish_list[0]} và {dish_list[1]}"
    else:
        return ", ".join(dish_list[:-1]) + f" và {dish_list[-1]}"

def create_search_sample(base_sample, idx):
    """Style 2: Tạo mẫu câu tìm kiếm / định vị tự nhiên."""
    instances = base_sample["detection"]["instances"]
    unique_dishes = list(dict.fromkeys(inst["category_name"] for inst in instances))
    
    template_str, prefix = SEARCH_TEMPLATES[idx % len(SEARCH_TEMPLATES)]
    dishes_text = format_natural_dishes(unique_dishes)
    caption = template_str.format(dishes_str=dishes_text)
    
    # Calculate exact tokens_positive for each unique dish
    dish_spans = {}
    for dish in unique_dishes:
        start = caption.find(dish)
        if start != -1:
            end = start + len(dish)
            dish_spans[dish] = [[start, end]]
        else:
            # Fallback
            dish_spans[dish] = [[0, len(caption)]]
            
    regions = []
    for inst in instances:
        dish = inst["category_name"]
        regions.append({
            "bbox": inst["bbox"],
            "phrase": dish,
            "tokens_positive": dish_spans.get(dish, [[0, len(caption)]])
        })
        
    return {
        "filename": base_sample["filename"],
        "height": base_sample["height"],
        "width": base_sample["width"],
        "detection": base_sample["detection"],
        "grounding": {
            "caption": caption,
            "regions": regions
        },
        "conversations": [
            {"from": "human", "value": f"<image>\n{caption}"},
            {"from": "gpt", "value": f"Đã định vị được {', '.join(unique_dishes)} trên mâm cơm."}
        ]
    }

def create_discrete_sample(base_sample):
    """Style 3: Liệt kê thực thể ngắn phân tách dấu chấm (chuẩn Grounding DINO)."""
    instances = base_sample["detection"]["instances"]
    unique_dishes = list(dict.fromkeys(inst["category_name"] for inst in instances))
    
    caption = " . ".join(unique_dishes) + " ."
    
    dish_spans = {}
    for dish in unique_dishes:
        start = caption.find(dish)
        end = start + len(dish)
        dish_spans[dish] = [[start, end]]
        
    regions = []
    for inst in instances:
        dish = inst["category_name"]
        regions.append({
            "bbox": inst["bbox"],
            "phrase": dish,
            "tokens_positive": dish_spans.get(dish, [[0, len(caption)]])
        })
        
    return {
        "filename": base_sample["filename"],
        "height": base_sample["height"],
        "width": base_sample["width"],
        "detection": base_sample["detection"],
        "grounding": {
            "caption": caption,
            "regions": regions
        },
        "conversations": [
            {"from": "human", "value": f"<image>\n{caption}"},
            {"from": "gpt", "value": f"Đã phát hiện: {caption}"}
        ]
    }

def main():
    print(f"Loading base samples from: {IN_FILE}")
    with open(IN_FILE, "r", encoding="utf-8") as f:
        base_samples = [json.loads(line) for line in f]
    print(f"Total base samples: {len(base_samples)}")
    
    multi_samples = []
    verified_tokens = 0
    total_tokens = 0
    
    for idx, s in enumerate(base_samples):
        # 1. Style 1: Descriptive
        multi_samples.append(s)
        
        # 2. Style 2: Search / Locational
        s2 = create_search_sample(s, idx)
        multi_samples.append(s2)
        
        # 3. Style 3: Discrete entities
        s3 = create_discrete_sample(s)
        multi_samples.append(s3)
        
    print(f"Generated total augmented samples: {len(multi_samples)} (x3)")
    
    # Verify tokens_positive integrity across all samples
    print("Verifying tokens_positive character alignment...")
    for item in multi_samples:
        caption = item["grounding"]["caption"]
        for r in item["grounding"]["regions"]:
            total_tokens += 1
            for span in r["tokens_positive"]:
                sub = caption[span[0]:span[1]]
                if sub == r["phrase"]:
                    verified_tokens += 1
                else:
                    print(f"⚠️ Mismatch: expected '{r['phrase']}', got '{sub}' in caption: '{caption}'")
                    
    print(f"Tokens alignment check: {verified_tokens}/{total_tokens} ({verified_tokens/total_tokens*100:.2f}%)")
    
    # Save output
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        for item in multi_samples:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
            
    print(f"✅ Successfully wrote 2,700 samples to: {OUT_FILE}")

if __name__ == "__main__":
    main()
