#!/usr/bin/env python3
"""
Chuyển đổi bộ dữ liệu ViFood-1K từ grounding caption Tiếng Việt sang Tiếng Anh
dựa trên bảng từ điển 51 món ăn (CLASS_TAXONOMY_51).
Tạo:
- vifood_train_vg_en.jsonl (900 mẫu train)
- vifood_val_vg_en.jsonl (100 mẫu val)
- instances_val_en.json (COCO format nhãn tiếng Anh)
"""

import os
import json
import copy

CLASS_TAXONOMY_51 = {
    "bánh bèo": ("steamed rice cakes", "savory steamed rice cakes topped with minced shrimp and scallion oil"),
    "bánh bột lọc": ("tapioca dumplings", "translucent tapioca dumplings filled with shrimp and pork"),
    "bánh canh": ("thick noodle soup", "Vietnamese thick noodle soup with savory broth"),
    "bánh chưng": ("square sticky rice cake", "traditional square sticky rice cake with mung beans and pork"),
    "bánh cuốn": ("steamed rice rolls", "thin steamed rice rolls stuffed with minced pork and wood-ear mushrooms"),
    "bánh căn": ("mini savory pancakes", "crispy small round rice pancakes cooked in clay molds"),
    "bánh giò": ("pyramid rice dumpling", "pyramid-shaped savory rice flour dumpling wrapped in banana leaves"),
    "bánh khọt": ("mini crispy pancakes", "savory mini crispy pancakes topped with shrimp"),
    "bánh mì": ("Vietnamese baguette", "crispy Vietnamese baguette sandwich filled with meats and pickled vegetables"),
    "bánh pía": ("pia pastry", "flaky pastry filled with durian, mung bean paste, and salted egg yolk"),
    "bánh tráng": ("rice paper", "Vietnamese rice paper sheets or grilled rice paper pizza"),
    "bánh tét": ("cylindrical rice cake", "cylindrical sticky rice cake wrapped in banana leaves"),
    "bánh xèo": ("sizzling crepe", "crispy Vietnamese yellow turmeric pancake with bean sprouts and pork"),
    "bánh đúc": ("steamed savory cake", "warm soft rice flour cake served with ground pork and sauce"),
    "bún bò Huế": ("Hue beef noodle soup", "spicy and aromatic Hue-style lemongrass beef noodle soup"),
    "bún": ("rice vermicelli", "fresh white Vietnamese rice vermicelli noodles"),
    "bún mắm": ("fermented fish noodle soup", "flavorful fermented seafood noodle soup"),
    "bún riêu": ("crab noodle soup", "tangy tomato and freshwater crab paste noodle soup"),
    "bún thịt nướng": ("grilled pork noodle bowl", "dry vermicelli bowl topped with lemongrass grilled pork and fresh herbs"),
    "bún đậu mắm tôm": ("tofu and noodle platter", "rice noodle platter served with fried tofu and shrimp paste"),
    "canh chua": ("sweet and sour soup", "Vietnamese tamarind sweet and sour soup with fish and pineapple"),
    "cao lầu": ("Cao Lau noodles", "Hoi An signature noodle dish with sliced pork and crispy crackers"),
    "cháo lòng": ("pork offal congee", "savory Vietnamese rice porridge with assorted pork offal"),
    "chả": ("Vietnamese sausage", "Vietnamese steamed pork roll or fried fish patties"),
    "cua": ("crab", "freshly cooked sea crab or crab claws"),
    "cá chiên": ("fried fish", "crispy golden deep-fried fish"),
    "cơm chiên": ("fried rice", "Vietnamese wok-fried rice with eggs and vegetables"),
    "cơm tấm": ("broken rice", "broken rice platter with grilled pork chop and meatloaf"),
    "gà luộc": ("boiled chicken", "tender poached chicken garnished with fresh lime leaves"),
    "gỏi": ("Vietnamese salad", "fresh shredded green papaya or cabbage salad with herbs"),
    "gỏi cuốn": ("fresh spring rolls", "fresh translucent rice paper spring rolls with shrimp and herbs"),
    "heo quay": ("roast pork", "crispy roasted pork belly with crackling golden skin"),
    "hàu": ("oyster", "fresh or grilled oysters topped with scallion oil"),
    "hủ tiếu": ("Hu Tieu noodles", "Southern Vietnamese clear pork noodle soup"),
    "lẩu": ("hotpot", "simmering hotpot broth with meats, seafood, and fresh vegetables"),
    "mì Quảng": ("Quang noodles", "turmeric noodles with concentrated savory broth, shrimp, and peanuts"),
    "mực": ("squid", "grilled or sauteed squid with chili and herbs"),
    "nem chua": ("fermented pork", "tangy cured fermented pork snacks with garlic and chili"),
    "ngao sò": ("clams and scallops", "steamed clams or grilled scallops with scallion oil"),
    "phở": ("Vietnamese Pho", "traditional Vietnamese beef or chicken noodle soup with fresh herbs"),
    "rau sống": ("fresh herbs and greens", "assorted fresh Vietnamese herbs, lettuce, and aromatic greens"),
    "súp cua": ("crab asparagus soup", "thick savory crab meat and egg drop soup"),
    "thịt bò": ("beef dish", "sauteed, grilled, or shaken tender beef dish"),
    "rau luộc": ("boiled vegetables", "boiled green vegetables served with dipping sauce"),
    "tôm": ("shrimp", "succulent steamed or grilled prawns"),
    "xôi xéo": ("turmeric sticky rice", "yellow sticky rice topped with mashed mung beans and fried shallots"),
    "ốc": ("sea snails", "savory sauteed or steamed sea snails with lemongrass"),
    "món ăn khác": ("other Vietnamese dish", "other traditional Vietnamese food dishes"),
    "rau xào": ("stir-fried vegetables", "garlic stir-fried green vegetables such as water spinach or bok choy"),
    "nước chấm": ("dipping sauce", "small bowl of seasoned Vietnamese dipping fish sauce or chili sauce"),
    "gà quay": ("roasted chicken", "golden roasted whole chicken or chicken drumsticks with savory herbs")
}

VI_TO_EN = {k: v[0] for k, v in CLASS_TAXONOMY_51.items()}

def convert_odvg_line(entry):
    new_entry = copy.deepcopy(entry)
    
    # 1. Trích xuất danh sách tên món tiếng Việt theo đúng thứ tự xuất hiện
    vn_regions = entry.get("grounding", {}).get("regions", [])
    vn_dishes_ordered = []
    for r in vn_regions:
        p = r.get("phrase", "")
        if p in VI_TO_EN and p not in vn_dishes_ordered:
            vn_dishes_ordered.append(p)
            
    # Nếu không có từ regions, parse từ caption
    if not vn_dishes_ordered:
        raw_cap = entry.get("grounding", {}).get("caption", "")
        parts = [p.strip() for p in raw_cap.split(".") if p.strip()]
        for p in parts:
            if p in VI_TO_EN and p not in vn_dishes_ordered:
                vn_dishes_ordered.append(p)

    # 2. Xây dựng English Grounding Caption
    en_dishes = [VI_TO_EN[d] for d in vn_dishes_ordered]
    if en_dishes:
        en_caption = " . ".join(en_dishes) + " ."
    else:
        en_caption = entry.get("grounding", {}).get("caption", "")

    # 3. Cập nhật regions với English phrase và exact tokens_positive
    new_regions = []
    for r in entry.get("grounding", {}).get("regions", []):
        vn_phrase = r.get("phrase", "")
        en_phrase = VI_TO_EN.get(vn_phrase, vn_phrase)
        
        start_idx = en_caption.find(en_phrase)
        if start_idx != -1:
            end_idx = start_idx + len(en_phrase)
            tok_pos = [[start_idx, end_idx]]
        else:
            tok_pos = []
            
        new_regions.append({
            "bbox": r["bbox"],
            "phrase": en_phrase,
            "tokens_positive": tok_pos
        })

    # 4. Cập nhật detection instances
    new_instances = []
    for inst in entry.get("detection", {}).get("instances", []):
        cat_vn = inst.get("category_name", "")
        cat_en = VI_TO_EN.get(cat_vn, cat_vn)
        new_instances.append({
            "bbox": inst["bbox"],
            "label": inst["label"],
            "category_name": cat_en
        })

    new_entry["detection"]["instances"] = new_instances
    new_entry["grounding"]["caption"] = en_caption
    new_entry["grounding"]["regions"] = new_regions
    new_entry["tags"] = en_caption
    
    return new_entry

def convert_file(in_path, out_path):
    print(f"Converting {in_path} -> {out_path}...")
    lines_out = []
    with open(in_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            entry = json.loads(line)
            en_entry = convert_odvg_line(entry)
            lines_out.append(json.dumps(en_entry, ensure_ascii=False) + "\n")
            
    with open(out_path, "w", encoding="utf-8") as f:
        f.writelines(lines_out)
    print(f"  Saved {len(lines_out)} lines to {out_path}")

def convert_coco_val(in_path, out_path):
    print(f"Converting COCO val {in_path} -> {out_path}...")
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    for cat in data.get("categories", []):
        vn_name = cat.get("name", "")
        if vn_name in VI_TO_EN:
            cat["name"] = VI_TO_EN[vn_name]
            
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Saved converted COCO val to {out_path}")

def main():
    base_dir = "/home/atin/tuan/SoPSoP/grounding_data/vifood/annotations"
    
    # 1. Train ODVG
    convert_file(
        os.path.join(base_dir, "vifood_train_vg.jsonl"),
        os.path.join(base_dir, "vifood_train_vg_en.jsonl")
    )
    
    # 2. Val ODVG
    convert_file(
        os.path.join(base_dir, "vifood_val_vg.jsonl"),
        os.path.join(base_dir, "vifood_val_vg_en.jsonl")
    )
    
    # 3. COCO Val
    convert_coco_val(
        os.path.join(base_dir, "instances_val.json"),
        os.path.join(base_dir, "instances_val_en.json")
    )
    
    print("\n✅ All English files created successfully!")

if __name__ == "__main__":
    main()
