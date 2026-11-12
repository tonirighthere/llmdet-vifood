#!/usr/bin/env python3
"""
scripts/crop_dataset_boxes.py
=============================
Cắt các bounding box từ tập ảnh và nhãn theo tọa độ YOLO,
xếp vào thư mục theo 54 món ăn (class) để người dùng kiểm tra trực quan.

Hỗ trợ:
- Source 1: vifood (images: grounding_data/vifood54/images/vifood, labels: crops_review/labels/vifood)
- Source 2: vifood2999 (images: vifood_2999_extracted, labels: crops_review/labels/vifood2999)
- Tự động chuẩn hóa EXIF orientation giống CVAT/mmcv.
- Lưu metadata JSON và classes.json phục vụ Web UI và sync tool.
"""

import os
import sys
import json
import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REVIEW_DIR = os.path.join(ROOT, "crops_review")
CROPS_DIR = os.path.join(REVIEW_DIR, "crops")
MANIFEST_PATH = os.path.join(REVIEW_DIR, "manifest.json")
CLASSES_PATH = os.path.join(REVIEW_DIR, "classes.json")

def load_classes():
    names_file = os.path.join(REVIEW_DIR, "labels", "vifood", "obj.names")
    if not os.path.exists(names_file):
        raise FileNotFoundError(f"Không tìm thấy {names_file}")
    with open(names_file, "r", encoding="utf-8") as f:
        classes = [line.strip() for line in f if line.strip()]
    return classes

def get_class_folder_name(cid, cname):
    return f"{cid:02d}_{cname}"

def process_single_image(args_tuple):
    source, stem, img_fname, img_rel_path, label_rel_path, classes, crops_dir = args_tuple
    abs_img_path = os.path.join(ROOT, img_rel_path)
    abs_label_path = os.path.join(ROOT, label_rel_path)

    if not os.path.exists(abs_img_path) or not os.path.exists(abs_label_path):
        return []

    with open(abs_label_path, "r", encoding="utf-8") as f:
        label_lines = [l.strip() for l in f if l.strip()]

    if not label_lines:
        return []

    try:
        with Image.open(abs_img_path) as im:
            im = ImageOps.exif_transpose(im)
            im_w, im_h = im.size
            im_rgb = im.convert("RGB")
    except Exception as e:
        print(f"Lỗi mở ảnh {abs_img_path}: {e}", file=sys.stderr)
        return []

    records = []
    for box_idx, line in enumerate(label_lines):
        parts = line.split()
        if len(parts) < 5:
            continue
        try:
            cid = int(parts[0])
            cx, cy, bw, bh = map(float, parts[1:5])
        except ValueError:
            continue

        if cid < 0 or cid >= len(classes):
            continue

        cname = classes[cid]
        folder_name = get_class_folder_name(cid, cname)

        # Tọa độ pixel (clamped)
        x1 = max(0, int(round((cx - bw / 2.0) * im_w)))
        y1 = max(0, int(round((cy - bh / 2.0) * im_h)))
        x2 = min(im_w, int(round((cx + bw / 2.0) * im_w)))
        y2 = min(im_h, int(round((cy + bh / 2.0) * im_h)))

        # Đảm bảo box có kích thước tối thiểu 1 pixel
        if x2 <= x1:
            x2 = min(im_w, x1 + 1)
        if y2 <= y1:
            y2 = min(im_h, y1 + 1)

        crop_img = im_rgb.crop((x1, y1, x2, y2))

        crop_filename = f"{source}__{stem}__box{box_idx}.jpg"
        crop_rel_path = os.path.join("crops_review", "crops", folder_name, crop_filename)
        abs_crop_path = os.path.join(ROOT, crop_rel_path)

        try:
            crop_img.save(abs_crop_path, format="JPEG", quality=90)
        except Exception as e:
            print(f"Lỗi lưu crop {abs_crop_path}: {e}", file=sys.stderr)
            continue

        crop_id = f"{source}__{stem}__box{box_idx}"
        records.append({
            "crop_id": crop_id,
            "crop_filename": crop_filename,
            "source": source,
            "img_stem": stem,
            "img_filename": img_fname,
            "img_rel_path": img_rel_path,
            "label_rel_path": label_rel_path,
            "box_idx": box_idx,
            "class_id": cid,
            "class_name": cname,
            "orig_class_id": cid,
            "orig_class_name": cname,
            "cx": cx, "cy": cy, "bw": bw, "bh": bh,
            "x1": x1, "y1": y1, "x2": x2, "y2": y2,
            "img_w": im_w, "img_h": im_h,
            "crop_rel_path": crop_rel_path,
            "is_deleted": 0,
            "updated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        })

    return records

def main():
    parser = argparse.ArgumentParser(description="Crop bounding boxes by class for review")
    parser.add_argument("--workers", type=int, default=16, help="Số worker song song")
    parser.add_argument("--limit", type=int, default=0, help="Giới hạn số ảnh xử lý (0 = tất cả)")
    args = parser.parse_args()

    classes = load_classes()
    print(f"==> Đã tải {len(classes)} classes từ obj.names")

    # Tạo trước các thư mục theo món
    os.makedirs(CROPS_DIR, exist_ok=True)
    trash_dir = os.path.join(CROPS_DIR, "_trash")
    os.makedirs(trash_dir, exist_ok=True)

    classes_meta = []
    for cid, cname in enumerate(classes):
        folder_name = get_class_folder_name(cid, cname)
        folder = os.path.join(CROPS_DIR, folder_name)
        os.makedirs(folder, exist_ok=True)
        classes_meta.append({"id": cid, "name": cname, "folder": folder_name})

    with open(CLASSES_PATH, "w", encoding="utf-8") as f:
        json.dump(classes_meta, f, ensure_ascii=False, indent=2)

    # Thu thập danh sách ảnh từ 2 nguồn
    sources_config = [
        ("vifood", "grounding_data/vifood54/images/vifood", "crops_review/labels/vifood/train.txt", "crops_review/labels/vifood/obj_train_data"),
        ("vifood2999", "vifood_2999_extracted", "crops_review/labels/vifood2999/train.txt", "crops_review/labels/vifood2999/obj_train_data")
    ]

    tasks = []
    for src_name, img_dir, train_txt, label_dir in sources_config:
        abs_train = os.path.join(ROOT, train_txt)
        with open(abs_train, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        for line in lines:
            img_fname = os.path.basename(line)
            stem = os.path.splitext(img_fname)[0]
            img_rel = os.path.join(img_dir, img_fname)
            lbl_rel = os.path.join(label_dir, f"{stem}.txt")
            tasks.append((src_name, stem, img_fname, img_rel, lbl_rel, classes, CROPS_DIR))

    if args.limit > 0:
        tasks = tasks[:args.limit]

    total_images = len(tasks)
    print(f"==> Bắt đầu cắt box cho {total_images} ảnh với {args.workers} workers...")

    start_time = time.time()
    manifest_map = {}
    processed_count = 0
    total_boxes = 0

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(process_single_image, t): t for t in tasks}
        for future in as_completed(futures):
            res = future.result()
            if res:
                for r in res:
                    manifest_map[r["crop_id"]] = r
                total_boxes += len(res)

            processed_count += 1
            if processed_count % 200 == 0 or processed_count == total_images:
                elapsed = time.time() - start_time
                speed = processed_count / elapsed if elapsed > 0 else 0
                print(f"    [{processed_count}/{total_images} ảnh] Đã cắt {total_boxes} boxes ({speed:.1f} ảnh/giây)...")

    # Ghi manifest JSON
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest_map, f, ensure_ascii=False, indent=2)

    total_time = time.time() - start_time
    print(f"\n Hoàn tất! Đã cắt tổng cộng {total_boxes} boxes từ {total_images} ảnh trong {total_time:.1f} giây.")
    print(f" Thư mục ảnh đã cắt: {CROPS_DIR}")
    print(f" Manifest JSON tại: {MANIFEST_PATH}")
    print(f" Classes JSON tại: {CLASSES_PATH}")

if __name__ == "__main__":
    main()
