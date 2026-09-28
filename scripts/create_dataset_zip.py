#!/usr/bin/env python3
"""
scripts/create_dataset_zip.py
=============================
Đóng gói dataset CHỈ GỒM 1.962 ảnh đạt chuẩn + nhãn:
- Đã loại bỏ hoàn toàn 38 ảnh kém chất lượng không có nhãn
- Nguồn ảnh: vietnamese-food-dataset/data/raw/roboflow_food_v6 (lấy đúng 1.962 ảnh)
- Nguồn nhãn: vifood2.zip (1.962 nhãn YOLO/Darknet, 51 classes)
- Định dạng chuẩn:
  + YOLOv5 / YOLOv8 / YOLOv11 (images/, labels/, data.yaml)
  + Darknet (obj.names, obj.data, obj_train_data/, train.txt)
  + COCO 1.0 (annotations_coco.json)
  + README.md tài liệu chi tiết
"""

import os
import sys
import glob
import json
import zipfile
from PIL import Image

BASE_DIR = "/home/atin/tuan/SoPSoP"
RAW_IMG_DIR = os.path.join(BASE_DIR, "vietnamese-food-dataset", "data", "raw", "roboflow_food_v6")
LABEL_ZIP_PATH = os.path.join(BASE_DIR, "vifood2.zip")
OUTPUT_ZIP_PATH = os.path.join(BASE_DIR, "vietnamese_food_dataset_1962.zip")

def main():
    print("=" * 60)
    print("📦 BẮT ĐẦU ĐÓNG GÓI DATASET 1.962 ẢNH + LABELS (CLEAN QUALITY)")
    print("=" * 60)

    # 1. Kiểm tra ảnh thô
    raw_images = sorted(glob.glob(os.path.join(RAW_IMG_DIR, "*")))
    print(f"📷 Tìm thấy {len(raw_images)} file ảnh trong {RAW_IMG_DIR}")
    if len(raw_images) == 0:
        print("❌ Không tìm thấy ảnh!")
        sys.exit(1)

    raw_img_map = {os.path.basename(p): p for p in raw_images}

    # 2. Đọc nhãn từ vifood2.zip
    if not os.path.exists(LABEL_ZIP_PATH):
        print(f"❌ Không tìm thấy file nhãn: {LABEL_ZIP_PATH}")
        sys.exit(1)

    with zipfile.ZipFile(LABEL_ZIP_PATH, 'r') as zf_in:
        names_content = zf_in.read("obj.names").decode("utf-8").strip()
        classes = [line.strip() for line in names_content.splitlines() if line.strip()]
        print(f"📋 Số lượng class: {len(classes)}")

        obj_data_content = zf_in.read("obj.data").decode("utf-8") if "obj.data" in zf_in.namelist() else ""
        
        # Lấy tất cả file nhãn txt
        label_files = [f for f in zf_in.namelist() if f.startswith("obj_train_data/") and f.endswith(".txt")]
        print(f"🏷️  Số lượng file nhãn: {len(label_files)}")

        # Lưu nội dung các file nhãn {stem: content}
        labels_dict = {}
        for lf in label_files:
            stem = os.path.splitext(os.path.basename(lf))[0]
            labels_dict[stem] = zf_in.read(lf).decode("utf-8")

    # 3. Chỉ chọn các ảnh có nhãn (loại bỏ hoàn toàn 38 ảnh không nhãn)
    labeled_images = []
    skipped_images = []

    for img_name in sorted(raw_img_map.keys()):
        stem = os.path.splitext(img_name)[0]
        if stem in labels_dict:
            labeled_images.append(img_name)
        else:
            skipped_images.append(img_name)

    print(f"✅ Ảnh được đóng gói: {len(labeled_images)} ảnh")
    print(f"🚫 Ảnh bị loại bỏ (chất lượng kém): {len(skipped_images)} ảnh")
    assert len(labeled_images) == 1962, f"Kỳ vọng 1962 ảnh, thực tế có {len(labeled_images)} ảnh"

    # 4. Tạo metadata & COCO JSON
    print("\n⏳ Đang sinh metadata và cấu trúc COCO 1.0...")
    coco_images = []
    coco_annotations = []
    ann_id_counter = 1
    total_boxes = 0

    coco_categories = [{"id": i, "name": c, "supercategory": "food"} for i, c in enumerate(classes)]

    for img_id, img_name in enumerate(labeled_images, 1):
        img_path = raw_img_map[img_name]
        stem = os.path.splitext(img_name)[0]

        with Image.open(img_path) as im:
            w, h = im.size

        coco_images.append({
            "id": img_id,
            "file_name": f"images/{img_name}",
            "width": w,
            "height": h
        })

        lbl_content = labels_dict[stem].strip()
        if lbl_content:
            for line in lbl_content.splitlines():
                parts = line.strip().split()
                if len(parts) >= 5:
                    cls_id = int(parts[0])
                    cx = float(parts[1])
                    cy = float(parts[2])
                    bw = float(parts[3])
                    bh = float(parts[4])

                    x_min = max(0.0, (cx - bw / 2.0) * w)
                    y_min = max(0.0, (cy - bh / 2.0) * h)
                    box_w = min(float(w) - x_min, bw * w)
                    box_h = min(float(h) - y_min, bh * h)

                    coco_annotations.append({
                        "id": ann_id_counter,
                        "image_id": img_id,
                        "category_id": cls_id,
                        "bbox": [round(x_min, 2), round(y_min, 2), round(box_w, 2), round(box_h, 2)],
                        "area": round(box_w * box_h, 2),
                        "iscrowd": 0
                    })
                    ann_id_counter += 1
                    total_boxes += 1

    coco_data = {
        "info": {
            "description": "Vietnamese Food Dataset (1,962 Curated Images + Labels)",
            "version": "1.0",
            "year": 2026,
            "contributor": "SoPSoP Team",
            "note": "Dataset chuẩn hóa gồm đúng 1.962 ảnh chất lượng cao và nhãn bounding box (đã loại bỏ các ảnh kém chất lượng)."
        },
        "licenses": [],
        "categories": coco_categories,
        "images": coco_images,
        "annotations": coco_annotations
    }

    # 5. README.md
    readme_content = f"""# Vietnamese Food Dataset (1,962 Images + Labels)

Tập dữ liệu chuẩn hóa gồm đúng 1.962 ảnh món ăn Việt Nam chất lượng cao và nhãn bounding box (đã loại bỏ toàn bộ ảnh chất lượng kém / không đạt chuẩn).

---

## 📊 Thống Kê Tổng Quan

- **Tổng số ảnh**: 1.962 ảnh
- **Tổng số file nhãn**: 1.962 file (.txt tương ứng từng ảnh)
- **Tổng số bounding box**: {total_boxes} boxes
- **Số lớp đối tượng (Classes)**: {len(classes)} lớp món ăn Việt Nam

---

## 📁 Cấu Trúc Thư Mục Trong File Zip

```
vietnamese_food_dataset/
├── images/                       # Chứa đúng 1.962 ảnh (.jpg)
├── labels/                       # 1.962 file nhãn YOLO (.txt)
├── obj_train_data/               # 1.962 file nhãn định dạng Darknet / CVAT
├── train.txt                     # Danh sách 1.962 ảnh dùng để huấn luyện
├── classes.txt                   # Danh sách 51 tên class món ăn
├── obj.names                     # Danh sách class định dạng Darknet
├── obj.data                      # Cấu hình Darknet
├── data.yaml                     # Cấu hình huấn luyện cho Ultralytics YOLO (v5/v8/v11)
├── annotations_coco.json         # File nhãn COCO 1.0 (cho MMDetection, Detectron2, CVAT)
└── README.md                     # Tài liệu hướng dẫn
```

---

## 🚀 Hướng Dẫn Sử Dụng

### 1. Huấn luyện với Ultralytics YOLO (v8 / v11)
File `data.yaml` đã được thiết lập sẵn:
```python
from ultralytics import YOLO

model = YOLO('yolov8n.pt')
model.train(data='data.yaml', epochs=100, imgsz=640)
```

### 2. Huấn luyện với Darknet
Sử dụng: `obj.data`, `obj.names`, `train.txt`

### 3. Huấn luyện với MMDetection / Detectron2 / PyTorch
Sử dụng: `annotations_coco.json` và thư mục ảnh `images/`

---

## 📋 Danh Sách {len(classes)} Lớp Món Ăn
{chr(10).join([f"{i}. {c}" for i, c in enumerate(classes)])}
"""

    # 6. data.yaml
    yaml_names_block = "\n".join([f"  {i}: '{c}'" for i, c in enumerate(classes)])
    data_yaml_content = f"""# YOLOv5/v8/v11 Dataset Configuration
path: .
train: train.txt
val: train.txt

nc: {len(classes)}
names:
{yaml_names_block}
"""

    # 7. Danh sách file txt
    train_txt = "\n".join([f"images/{img}" for img in labeled_images]) + "\n"
    classes_txt = "\n".join(classes) + "\n"

    # 8. Tạo file ZIP
    print(f"\n📦 Đang nén file zip tại: {OUTPUT_ZIP_PATH} ...")
    if os.path.exists(OUTPUT_ZIP_PATH):
        os.remove(OUTPUT_ZIP_PATH)

    with zipfile.ZipFile(OUTPUT_ZIP_PATH, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf_out:
        # A. Thêm các file metadata & config
        print("  - Thêm README.md, data.yaml, classes.txt, obj.names, obj.data, train.txt...")
        zf_out.writestr("vietnamese_food_dataset/README.md", readme_content)
        zf_out.writestr("vietnamese_food_dataset/data.yaml", data_yaml_content)
        zf_out.writestr("vietnamese_food_dataset/classes.txt", classes_txt)
        zf_out.writestr("vietnamese_food_dataset/obj.names", classes_txt)
        zf_out.writestr("vietnamese_food_dataset/obj.data", obj_data_content)
        zf_out.writestr("vietnamese_food_dataset/train.txt", train_txt)
        
        # B. Thêm file COCO json
        print("  - Thêm annotations_coco.json...")
        zf_out.writestr("vietnamese_food_dataset/annotations_coco.json", json.dumps(coco_data, ensure_ascii=False, indent=2))

        # C. Thêm labels/ và obj_train_data/ (đúng 1962 files)
        print(f"  - Thêm {len(labeled_images)} file nhãn vào labels/ và obj_train_data/...")
        for img_name in labeled_images:
            stem = os.path.splitext(img_name)[0]
            content = labels_dict[stem]
            zf_out.writestr(f"vietnamese_food_dataset/labels/{stem}.txt", content)
            zf_out.writestr(f"vietnamese_food_dataset/obj_train_data/{stem}.txt", content)

        # D. Thêm ĐÚNG 1.962 file ảnh vào images/
        print(f"  - Thêm đúng 1.962 ảnh vào images/...")
        for i, img_name in enumerate(labeled_images, 1):
            img_path = raw_img_map[img_name]
            zf_out.write(img_path, arcname=f"vietnamese_food_dataset/images/{img_name}")
            if i % 400 == 0 or i == len(labeled_images):
                print(f"    Đã nén: {i}/{len(labeled_images)} ảnh...")

    size_mb = os.path.getsize(OUTPUT_ZIP_PATH) / (1024 * 1024)
    print("=" * 60)
    print(f"🎉 HOÀN TẤT THÀNH CÔNG!")
    print(f"📁 Đường dẫn file ZIP: {OUTPUT_ZIP_PATH}")
    print(f"📦 Kích thước file: {size_mb:.2f} MB")
    print("=" * 60)

if __name__ == "__main__":
    main()
