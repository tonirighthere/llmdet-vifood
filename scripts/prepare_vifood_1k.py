#!/usr/bin/env python3
"""
scripts/prepare_vifood_1k.py
============================
Trích xuất 1.000 ảnh đầu tiên từ vifood2.zip:
- Đọc 1.000 dòng đầu tiên từ train.txt (bắt đầu từ srcA_H-000...)
- Đọc file annotation YOLO tương ứng từ obj_train_data/
- Đọc obj.names (51 class, bao gồm rau xào, nước chấm, gà quay)
- Lấy ảnh từ vietnamese-food-dataset/data/raw/roboflow_food_v6/
- Chia 900 train / 100 val
- Lưu ảnh vào grounding_data/vifood/images/train2017 và val2017
- Tạo metadata thô grounding_data/vifood/cache/vifood_1k_raw.json
"""

import os
import sys
import zipfile
import json
import shutil
from PIL import Image

BASE_DIR = "/home/atin/tuan/SoPSoP"
ZIP_PATH = os.path.join(BASE_DIR, "vifood2.zip")
RAW_IMG_DIR = os.path.join(BASE_DIR, "vietnamese-food-dataset", "data", "raw", "roboflow_food_v6")

OUT_DATA_DIR = os.path.join(BASE_DIR, "grounding_data", "vifood")
OUT_TRAIN_DIR = os.path.join(OUT_DATA_DIR, "images", "train2017")
OUT_VAL_DIR = os.path.join(OUT_DATA_DIR, "images", "val2017")
OUT_CACHE_DIR = os.path.join(OUT_DATA_DIR, "cache")
OUT_ANN_DIR = os.path.join(OUT_DATA_DIR, "annotations")

def main():
    print("=" * 60)
    print("🚀 BƯỚC 1: TRÍCH XUẤT 1.000 ẢNH ĐẦU TIÊN TỪ VIFOOD2.ZIP")
    print("=" * 60)

    # 1. Tạo các thư mục đầu ra
    for p in [OUT_TRAIN_DIR, OUT_VAL_DIR, OUT_CACHE_DIR, OUT_ANN_DIR]:
        os.makedirs(p, exist_ok=True)

    if not os.path.exists(ZIP_PATH):
        print(f"❌ Không tìm thấy file zip: {ZIP_PATH}")
        sys.exit(1)

    with zipfile.ZipFile(ZIP_PATH, 'r') as zf:
        # Đọc obj.names
        names_content = zf.read("obj.names").decode("utf-8").strip()
        classes = [line.strip() for line in names_content.splitlines() if line.strip()]
        print(f"📋 Danh sách classes ({len(classes)} classes):")
        for i, c in enumerate(classes):
            print(f"   [{i:2d}] {c}")

        # Đọc train.txt
        train_lines = zf.read("train.txt").decode("utf-8").strip().splitlines()
        print(f"\n📄 Tổng số dòng trong train.txt: {len(train_lines)}")

        # Lấy 1.000 ảnh đầu tiên
        target_lines = train_lines[:1000]
        print(f"🎯 Lấy 1.000 ảnh đầu tiên (từ dòng 0 đến 999):")
        print(f"   Ảnh đầu: {target_lines[0]}")
        print(f"   Ảnh cuối: {target_lines[-1]}")

        # Chuẩn bị dữ liệu
        all_samples = []
        missing_images = 0
        total_boxes = 0
        class_distribution = {c: 0 for c in classes}

        print("\n⏳ Đang xử lý annotations và sao chép ảnh...")
        for idx, line in enumerate(target_lines):
            # Ví dụ: data/obj_train_data/srcA_H-000_jpg.rf.9b3c0354b6ea79e39d868d5d71f49079.jpg
            line = line.strip()
            if not line:
                continue

            base_name = os.path.basename(line) # srcA_H-000_jpg.rf....jpg
            stem = os.path.splitext(base_name)[0] # srcA_H-000_jpg.rf...

            # Tìm file ảnh gốc trên disk
            raw_img_path = os.path.join(RAW_IMG_DIR, base_name)
            if not os.path.exists(raw_img_path):
                missing_images += 1
                print(f"⚠️ Thiếu ảnh: {raw_img_path}")
                continue

            # Đọc kích thước ảnh
            with Image.open(raw_img_path) as img:
                w, h = img.size

            # Đọc annotation txt từ zip
            ann_zip_path = f"obj_train_data/{stem}.txt"
            bboxes = []
            if ann_zip_path in zf.namelist():
                ann_text = zf.read(ann_zip_path).decode("utf-8").strip()
                for ann_line in ann_text.splitlines():
                    parts = ann_line.strip().split()
                    if len(parts) >= 5:
                        cls_id = int(parts[0])
                        cx = float(parts[1])
                        cy = float(parts[2])
                        bw = float(parts[3])
                        bh = float(parts[4])

                        # Chuyển đổi sang pixel [x1, y1, x2, y2]
                        x1 = max(0.0, min((cx - bw / 2.0) * w, float(w - 1)))
                        y1 = max(0.0, min((cy - bh / 2.0) * h, float(h - 1)))
                        x2 = max(x1 + 1.0, min((cx + bw / 2.0) * w, float(w)))
                        y2 = max(y1 + 1.0, min((cy + bh / 2.0) * h, float(h)))

                        cls_name = classes[cls_id] if cls_id < len(classes) else "món ăn khác"
                        class_distribution[cls_name] += 1
                        total_boxes += 1

                        bboxes.append({
                            "class_id": cls_id,
                            "class_name": cls_name,
                            "bbox_yolo": [cx, cy, bw, bh],
                            "bbox_pixel": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)]
                        })

            # Chia train (900) vs val (100)
            is_val = (idx >= 900)
            split_dir = OUT_VAL_DIR if is_val else OUT_TRAIN_DIR
            dest_img_path = os.path.join(split_dir, base_name)

            # Sao chép ảnh
            if not os.path.exists(dest_img_path):
                shutil.copy2(raw_img_path, dest_img_path)

            all_samples.append({
                "id": idx,
                "split": "val" if is_val else "train",
                "filename": base_name,
                "relative_path": f"train2017/{base_name}" if not is_val else f"val2017/{base_name}",
                "width": w,
                "height": h,
                "bboxes": bboxes
            })

            if (idx + 1) % 200 == 0 or (idx + 1) == len(target_lines):
                print(f"   Đã xử lý: {idx + 1}/{len(target_lines)} ảnh...")

    print(f"\n✅ Đã xử lý thành công {len(all_samples)} ảnh (Thiếu: {missing_images})")
    print(f"📦 Tổng số Bounding Box: {total_boxes}")
    train_count = sum(1 for s in all_samples if s["split"] == "train")
    val_count = sum(1 for s in all_samples if s["split"] == "val")
    print(f"📊 Phân chia: {train_count} ảnh Train (images/train2017) | {val_count} ảnh Val (images/val2017)")

    # Lưu metadata thô
    out_raw_json = os.path.join(OUT_CACHE_DIR, "vifood_1k_raw.json")
    with open(out_raw_json, "w", encoding="utf-8") as f:
        json.dump({
            "classes": classes,
            "total_images": len(all_samples),
            "total_boxes": total_boxes,
            "samples": all_samples
        }, f, ensure_ascii=False, indent=2)
    print(f"💾 Đã lưu metadata thô tại: {out_raw_json}")

    # In thống kê top class
    print("\n📈 Thống kê Top 15 Class phổ biến nhất trong 1.000 ảnh:")
    sorted_cls = sorted(class_distribution.items(), key=lambda x: x[1], reverse=True)
    for cname, cnt in sorted_cls[:15]:
        print(f"   {cname:25s}: {cnt:4d} boxes")

    print("=" * 60)
    print("🎉 BƯỚC 1 HOÀN TẤT THÀNH CÔNG!")
    print("=" * 60)

if __name__ == "__main__":
    main()
