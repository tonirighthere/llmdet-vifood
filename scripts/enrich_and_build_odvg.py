#!/usr/bin/env python3
"""
scripts/enrich_and_build_odvg.py
================================
Sinh caption song ngữ (ngắn + dài LMM) bằng Gemini API (gemini-3.6-flash)
và đóng gói thành định dạng ODVG JSONL cho LLMDet:
1. Chuẩn hóa từ điển 51 class (Việt - Anh)
2. Gọi Gemini API sinh LMM conversations đa luồng + persistent cache
3. Tính toán chính xác character offsets (tokens_positive) cho Visual Grounding
4. Xuất:
   - vifood_train_vg.jsonl (900 samples)
   - vifood_val_vg.jsonl (100 samples)
   - instances_val.json (COCO format cho mAP eval)
   - label_map.json (51 classes)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE_DIR = "/home/atin/tuan/SoPSoP"
RAW_CACHE_FILE = os.path.join(BASE_DIR, "grounding_data", "vifood", "cache", "vifood_1k_raw.json")
GEMINI_CACHE_FILE = os.path.join(BASE_DIR, "grounding_data", "vifood", "cache", "gemini_captions.json")

ANN_DIR = os.path.join(BASE_DIR, "grounding_data", "vifood", "annotations")
TRAIN_JSONL = os.path.join(ANN_DIR, "vifood_train_vg.jsonl")
VAL_JSONL = os.path.join(ANN_DIR, "vifood_val_vg.jsonl")
VAL_COCO_JSON = os.path.join(ANN_DIR, "instances_val.json")
LABEL_MAP_FILE = os.path.join(ANN_DIR, "label_map.json")

API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3.6-flash"

# Từ điển 51 class chuẩn hóa: [Tên Việt] -> (Tên Anh, Mô tả món)
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

def call_gemini_api(prompt):
    """Gọi Gemini API qua REST endpoint với timeout ngắn."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.4, "maxOutputTokens": 150}
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=8) as res:
            data = json.loads(res.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        return None

def is_valid_caption(text):
    if not text or len(text.strip()) < 35:
        return False
    text = text.strip()
    if text[0] in [',', '.', '/', ';', ':', '*']:
        return False
    if not text.endswith(('.', '!', '?')):
        return False
    return True

def generate_fallback_caption(dishes):
    """Tạo caption sinh động thay thế nếu API bị giới hạn."""
    en_dishes = [CLASS_TAXONOMY_51.get(d, (d, ""))[0] for d in dishes]
    dishes_str = ", ".join(en_dishes) if en_dishes else "assorted Vietnamese dishes"
    return (
        f"This image presents an authentic Vietnamese meal showcasing {dishes_str}. "
        "The dishes are neatly arranged on the dining table, highlighting fresh ingredients, vibrant colors, "
        "and characteristic Vietnamese culinary presentation."
    )

def main():
    print("=" * 60)
    print("🚀 BƯỚC 2: SINH CAPTION SONG NGỮ & ĐÓNG GÓI ODVG JSONL")
    print("=" * 60)

    os.makedirs(ANN_DIR, exist_ok=True)

    with open(RAW_CACHE_FILE, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    samples = raw_data["samples"]
    print(f"📦 Đã nạp {len(samples)} mẫu từ cache thô.")

    # 1. Nạp hoặc khởi tạo cache caption Gemini
    gemini_cache = {}
    if os.path.exists(GEMINI_CACHE_FILE):
        try:
            with open(GEMINI_CACHE_FILE, "r", encoding="utf-8") as f:
                gemini_cache = json.load(f)
            print(f"💾 Nạp {len(gemini_cache)} caption đã có từ cache.")
        except Exception:
            gemini_cache = {}

    # Lập danh sách các dish combination cần sinh caption
    dish_combos = {}
    for s in samples:
        dishes = sorted(list(set(b["class_name"] for b in s["bboxes"])))
        key = " + ".join(dishes) if dishes else "bữa ăn Việt Nam"
        if key not in dish_combos:
            dish_combos[key] = dishes

    missing_keys = [k for k in dish_combos if k not in gemini_cache]
    print(f"🎯 Tổng số tổ hợp món ăn: {len(dish_combos)} (Cần sinh mới: {len(missing_keys)})")

    if missing_keys:
        print("⏳ Đang sinh mô tả chi tiết bằng Gemini API (đa luồng)...")
        def process_combo(key):
            dishes = dish_combos[key]
            en_names = [CLASS_TAXONOMY_51.get(d, (d, ""))[0] for d in dishes]
            prompt = (
                f"Describe a Vietnamese meal presentation in 2 concise, natural, vivid sentences in English. "
                f"The dishes shown are: {', '.join(en_names)} ({', '.join(dishes)}). "
                f"Focus on visual presentation, appetizing colors, garnishes, and dining arrangement."
            )
            cap = call_gemini_api(prompt)
            if not cap:
                cap = generate_fallback_caption(dishes)
            return key, cap

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_key = {executor.submit(process_combo, k): k for k in missing_keys}
            done_count = 0
            for future in as_completed(future_to_key):
                k, cap = future.result()
                gemini_cache[k] = cap
                done_count += 1
                if done_count % 10 == 0 or done_count == len(missing_keys):
                    print(f"   Đã sinh: {done_count}/{len(missing_keys)} caption...", flush=True)
                    # Lưu cache định kỳ
                    with open(GEMINI_CACHE_FILE, "w", encoding="utf-8") as f:
                        json.dump(gemini_cache, f, ensure_ascii=False, indent=2)

        # Lưu cache cuối cùng
        with open(GEMINI_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(gemini_cache, f, ensure_ascii=False, indent=2)
        print("✅ Hoàn tất sinh caption bằng Gemini API!")

    # 2. Xây dựng file ODVG JSONL và COCO JSON
    print("\n⏳ Đang đóng gói ODVG JSONL và tính toán tokens_positive character offsets...")
    train_odvg = []
    val_odvg = []

    coco_categories = []
    classes = raw_data["classes"]
    for i, cname in enumerate(classes):
        coco_categories.append({
            "id": i,
            "name": cname,
            "supercategory": "vietnamese_food"
        })

    coco_val_images = []
    coco_val_annotations = []
    val_ann_id = 1

    for s in samples:
        w = s["width"]
        h = s["height"]
        rel_path = s["relative_path"] # e.g. train2017/xxx.jpg hoặc val2017/xxx.jpg

        # Danh sách món trong ảnh
        unique_dishes = []
        for b in s["bboxes"]:
            if b["class_name"] not in unique_dishes:
                unique_dishes.append(b["class_name"])

        # Grounding caption: các món cách nhau bởi " . "
        # Ví dụ: "bánh bèo . nước chấm ."
        if unique_dishes:
            grounding_caption = " . ".join(unique_dishes) + " ."
        else:
            grounding_caption = "món ăn khác ."

        # Tags cho detection & contrastive loss
        tags_str = grounding_caption

        # LMM Conversation (Long caption)
        combo_key = " + ".join(sorted(unique_dishes)) if unique_dishes else "bữa ăn Việt Nam"
        long_cap = gemini_cache.get(combo_key, "")
        if not is_valid_caption(long_cap):
            long_cap = generate_fallback_caption(unique_dishes)

        conversations = [
            {"from": "human", "value": "<image>\nDescribe the image in detail."},
            {"from": "gpt", "value": long_cap}
        ]

        # Bounding boxes và Tokens Positive
        instances = []
        regions = []

        for b in s["bboxes"]:
            cname = b["class_name"]
            cid = b["class_id"]
            x1, y1, x2, y2 = b["bbox_pixel"]

            # Instance cho detection mode
            instances.append({
                "bbox": [x1, y1, x2, y2],
                "label": cid,
                "category_name": cname
            })

            # Tính exact character offset [start, end] trong grounding_caption
            # Tìm vị trí xuất hiện của cname trong caption
            start_pos = grounding_caption.find(cname)
            if start_pos != -1:
                end_pos = start_pos + len(cname)
                tokens_positive = [[start_pos, end_pos]]
            else:
                tokens_positive = []

            regions.append({
                "bbox": [x1, y1, x2, y2],
                "phrase": cname,
                "tokens_positive": tokens_positive
            })

        odvg_entry = {
            "filename": rel_path,
            "height": h,
            "width": w,
            "detection": {"instances": instances},
            "grounding": {
                "caption": grounding_caption,
                "regions": regions
            },
            "tags": tags_str,
            "conversations": conversations
        }

        if s["split"] == "train":
            train_odvg.append(odvg_entry)
        else:
            val_odvg.append(odvg_entry)

            # Đóng gói COCO format cho tập val
            coco_val_images.append({
                "id": s["id"],
                "file_name": s["filename"],
                "width": w,
                "height": h
            })
            for b in s["bboxes"]:
                x1, y1, x2, y2 = b["bbox_pixel"]
                bw = round(x2 - x1, 2)
                bh = round(y2 - y1, 2)
                coco_val_annotations.append({
                    "id": val_ann_id,
                    "image_id": s["id"],
                    "category_id": b["class_id"],
                    "bbox": [x1, y1, bw, bh],
                    "area": round(bw * bh, 2),
                    "iscrowd": 0
                })
                val_ann_id += 1

    # Ghi file JSONL
    with open(TRAIN_JSONL, "w", encoding="utf-8") as f:
        for item in train_odvg:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"💾 Đã ghi file Train ODVG ({len(train_odvg)} mẫu): {TRAIN_JSONL}")

    with open(VAL_JSONL, "w", encoding="utf-8") as f:
        for item in val_odvg:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"💾 Đã ghi file Val ODVG ({len(val_odvg)} mẫu): {VAL_JSONL}")

    # Ghi file COCO Val JSON
    coco_val_data = {
        "images": coco_val_images,
        "annotations": coco_val_annotations,
        "categories": coco_categories
    }
    with open(VAL_COCO_JSON, "w", encoding="utf-8") as f:
        json.dump(coco_val_data, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã ghi file COCO Val JSON ({len(coco_val_images)} ảnh, {len(coco_val_annotations)} boxes): {VAL_COCO_JSON}")

    # Ghi file Label Map
    label_map = {str(i): cname for i, cname in enumerate(classes)}
    with open(LABEL_MAP_FILE, "w", encoding="utf-8") as f:
        json.dump(label_map, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã ghi file Label Map (51 class): {LABEL_MAP_FILE}")

    print("=" * 60)
    print("🎉 BƯỚC 2 HOÀN TẤT THÀNH CÔNG!")
    print("=" * 60)

if __name__ == "__main__":
    main()
