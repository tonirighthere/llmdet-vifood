#!/usr/bin/env python3
"""
scripts/infer_vifood_2999_exp4_cvat.py
======================================
Infer labels for vifood_2999 dataset using Exp 4 (Multi-Prompt & High-Res 800)
and export in CVAT compatible format (YOLO 1.1, CVAT XML 1.1, COCO 1.0).

Features:
- Full 51 Vietnamese dish classes
- Multi-Prompting Grounding DINO Swin-T (Exp 4 checkpoint)
- Automatic checkpointing / caching to resume without loss
- High-efficiency inference pipeline with fast image loading
- Cross-class NMS to deduplicate redundant boxes on same food objects
- Packages into CVAT-compatible ZIP files:
  1. vifood_2999_labels_cvat.zip (YOLO 1.1 / Darknet format, matching vifood2.zip)
  2. vifood_2999_cvat_xml.zip (CVAT 1.1 XML format)
  3. vifood_2999_cvat_coco.zip (COCO 1.0 format)
"""

import os
import sys
import time
import json
import zipfile
import argparse
from xml.sax.saxutils import escape as xml_escape
import numpy as np
import cv2
import torch
from tqdm import tqdm

# Ensure LLMDET paths
WORKSPACE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LLMDET_DIR = os.path.join(WORKSPACE_DIR, 'llmdet_vietnamese_food')
sys.path.insert(0, LLMDET_DIR)
os.chdir(LLMDET_DIR)

from mmengine.registry import init_default_scope
init_default_scope('mmdet')
from mmdet.apis import init_detector, inference_detector
from mmdet.apis.inference import get_test_pipeline_cfg
from mmcv.transforms import Compose

# 51 Vietnamese Food Classes
CANONICAL_51_CLASSES = [
    'bánh bèo', 'bánh bột lọc', 'bánh canh', 'bánh chưng', 'bánh cuốn',
    'bánh căn', 'bánh giò', 'bánh khọt', 'bánh mì', 'bánh pía',
    'bánh tráng', 'bánh tét', 'bánh xèo', 'bánh đúc', 'bún bò Huế',
    'bún', 'bún mắm', 'bún riêu', 'bún thịt nướng', 'bún đậu mắm tôm',
    'canh chua', 'cao lầu', 'cháo lòng', 'chả', 'cua',
    'cá chiên', 'cơm chiên', 'cơm tấm', 'gà luộc', 'gỏi',
    'gỏi cuốn', 'heo quay', 'hàu', 'hủ tiếu', 'lẩu',
    'mì Quảng', 'mực', 'nem chua', 'ngao sò', 'phở',
    'rau sống', 'súp cua', 'thịt bò', 'rau luộc', 'tôm',
    'xôi xéo', 'ốc', 'món ăn khác', 'rau xào', 'nước chấm',
    'gà quay'
]

def nms(boxes, scores, iou_thr=0.6):
    """Greedy Non-Maximum Suppression."""
    if len(boxes) == 0:
        return []
    x1 = boxes[:, 0]
    y1 = boxes[:, 1]
    x2 = boxes[:, 2]
    y2 = boxes[:, 3]
    areas = (x2 - x1) * (y2 - y1)
    order = scores.argsort()[::-1]
    keep = []
    while order.size > 0:
        i = order[0]
        keep.append(i)
        xx1 = np.maximum(x1[i], x1[order[1:]])
        yy1 = np.maximum(y1[i], y1[order[1:]])
        xx2 = np.minimum(x2[i], x2[order[1:]])
        yy2 = np.minimum(y2[i], y2[order[1:]])
        w = np.maximum(0.0, xx2 - xx1)
        h = np.maximum(0.0, yy2 - yy1)
        inter = w * h
        union = areas[i] + areas[order[1:]] - inter
        ovr = inter / np.maximum(union, 1e-6)
        inds = np.where(ovr <= iou_thr)[0]
        order = order[inds + 1]
    return keep

def parse_args():
    parser = argparse.ArgumentParser(description="Infer Exp 4 labels for CVAT")
    parser.add_argument('--img-dir', type=str, default='/home/atin/tuan/SoPSoP/vifood_2999_extracted',
                        help='Directory with 2999 extracted images')
    parser.add_argument('--config', type=str, default='configs/val/grounding_dino_swin_t_vifood_val.py',
                        help='Model config path')
    parser.add_argument('--checkpoint', type=str, default='work_dirs/vifood_multi_res800/iter_10000.pth',
                        help='Exp 4 weights checkpoint path')
    parser.add_argument('--work-dir', type=str, default='/home/atin/tuan/SoPSoP/work_dirs/vifood_2999_cvat',
                        help='Output directory')
    parser.add_argument('--conf-thr', type=float, default=0.25,
                        help='Confidence threshold')
    parser.add_argument('--iou-thr', type=float, default=0.60,
                        help='Cross-class NMS IoU threshold')
    parser.add_argument('--device', type=str, default='cuda:0',
                        help='Device to run inference on')
    parser.add_argument('--force', action='store_true',
                        help='Force re-running model inference from scratch')
    return parser.parse_args()

def main():
    args = parse_args()
    print("=" * 70)
    print("🚀 BẮT ĐẦU SUY LUẬN NHÃN EXP 4 CHO TẬP VIFOOD 2.999 ẢNH (CVAT EXPORT)")
    print("=" * 70)
    print(f"📁 Thư mục ảnh đầu vào: {args.img_dir}")
    print(f"⚙️ Config: {args.config}")
    print(f"⚖️ Checkpoint: {args.checkpoint}")
    print(f"🎯 Ngưỡng Confidence: {args.conf_thr} | Ngưỡng NMS IoU: {args.iou_thr}")
    print(f"💻 Thiết bị: {args.device}")

    os.makedirs(args.work_dir, exist_ok=True)
    cache_path = os.path.join(args.work_dir, 'detections_cache.jsonl')

    # 1. Thu thập danh sách ảnh
    image_files = sorted([f for f in os.listdir(args.img_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    total_images = len(image_files)
    print(f"📷 Tổng số ảnh tìm thấy: {total_images}")
    if total_images == 0:
        print("❌ Không tìm thấy ảnh trong thư mục!")
        sys.exit(1)

    # 2. Đọc cache nếu có để hỗ trợ Resume
    cached_results = {}
    if args.force and os.path.exists(cache_path):
        print(f"🗑️ Flag --force được bật: Xóa cache cũ tại {cache_path}...")
        os.remove(cache_path)

    if os.path.exists(cache_path):
        print(f"🔄 Tìm thấy cache tại {cache_path}, đang nạp kết quả đã xử lý...")
        with open(cache_path, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    item = json.loads(line)
                    cached_results[item['file_name']] = item
        print(f"✅ Đã nạp {len(cached_results)} / {total_images} ảnh từ cache.")

    # 3. Khởi tạo mô hình Exp 4
    if len(cached_results) < total_images:
        print("\n⏳ Đang tải mô hình Exp 4 (Grounding DINO Swin-T Multi-Res800)...")
        t_load = time.time()
        model = init_detector(args.config, args.checkpoint, device=args.device)
        model.eval()
        print(f"✅ Tải mô hình thành công trong {time.time() - t_load:.2f}s!")

        # Tạo prompt gồm toàn bộ 51 classes
        prompt = " . ".join(CANONICAL_51_CLASSES) + " ."
        print(f"📝 Text Prompt (51 lớp món ăn): {prompt[:80]}... (Độ dài: {len(prompt)} ký tự)")

        # Mở cache để ghi tiếp
        cache_file = open(cache_path, 'a', encoding='utf-8')

        # Vòng lặp suy luận
        print(f"\n⚡ Tiến hành suy luận {total_images - len(cached_results)} ảnh còn lại...")
        t_start = time.time()
        processed_count = len(cached_results)
        step_times = []

        for idx, img_name in enumerate(image_files):
            if img_name in cached_results:
                continue

            img_path = os.path.join(args.img_dir, img_name)
            t0 = time.time()

            try:
                # Suy luận Grounding DINO
                with torch.inference_mode():
                    res = inference_detector(model, img_path, text_prompt=prompt, custom_entities=True)

                if hasattr(res, 'ori_shape'):
                    h, w = res.ori_shape[:2]
                else:
                    im_info = cv2.imread(img_path)
                    h, w = im_info.shape[:2]

                pred = res.pred_instances
                scores = pred.scores.cpu().numpy()
                boxes = pred.bboxes.cpu().numpy()
                labels = pred.labels.cpu().numpy()

                # Lọc theo confidence
                mask = scores >= args.conf_thr
                f_boxes = boxes[mask]
                f_scores = scores[mask]
                f_labels = labels[mask]

                # Áp dụng Cross-class NMS để loại bỏ box trùng lặp trên cùng một món
                final_boxes = []
                if len(f_boxes) > 0:
                    keep_indices = nms(f_boxes, f_scores, iou_thr=args.iou_thr)
                    for k_i in keep_indices:
                        cls_id = int(f_labels[k_i])
                        sc = float(f_scores[k_i])
                        box = [float(coord) for coord in f_boxes[k_i]]
                        final_boxes.append({
                            'class_id': cls_id,
                            'class_name': CANONICAL_51_CLASSES[cls_id] if cls_id < len(CANONICAL_51_CLASSES) else f"dish_{cls_id}",
                            'score': round(sc, 4),
                            'box_xyxy': [round(c, 2) for c in box]
                        })

                record = {
                    'file_name': img_name,
                    'width': int(w),
                    'height': int(h),
                    'boxes': final_boxes
                }
            except Exception as e:
                print(f"⚠️ Lỗi xử lý {img_name}: {e}")
                record = {
                    'file_name': img_name,
                    'width': 0,
                    'height': 0,
                    'boxes': []
                }
            cached_results[img_name] = record
            cache_file.write(json.dumps(record, ensure_ascii=False) + '\n')
            cache_file.flush()

            dt = time.time() - t0
            step_times.append(dt)
            processed_count += 1

            if processed_count % 50 == 0 or processed_count == total_images:
                avg_dt = np.mean(step_times[-50:]) if step_times else 0.5
                remain_imgs = total_images - processed_count
                eta_sec = remain_imgs * avg_dt
                eta_min = eta_sec / 60.0
                fps = 1.0 / avg_dt if avg_dt > 0 else 0
                print(f"[{processed_count}/{total_images}] ({processed_count/total_images*100:.1f}%) | "
                      f"Tốc độ: {fps:.1f} img/s | Box: {len(final_boxes)} | Còn lại: ~{eta_min:.1f} phút", flush=True)

        cache_file.close()
        print(f"\n🎉 Hoàn thành toàn bộ suy luận trong {time.time() - t_start:.2f}s!")
    else:
        print("\n✅ Tất cả 2.999 ảnh đã có kết quả suy luận trong cache!")

    # 4. Lọc theo ngưỡng conf_thr và Thống kê dữ liệu
    print("\n" + "=" * 70)
    print(f"📊 THỐNG KÊ KẾT QUẢ GÁN NHÃN VỚI CONFIDENCE >= {args.conf_thr}:")
    print("=" * 70)

    filtered_results = {}
    for f in image_files:
        rec = cached_results[f]
        filtered_results[f] = {
            'file_name': rec['file_name'],
            'width': rec['width'],
            'height': rec['height'],
            'boxes': [b for b in rec['boxes'] if b['score'] >= args.conf_thr]
        }

    total_boxes = sum(len(filtered_results[f]['boxes']) for f in image_files)
    box_counts = [len(filtered_results[f]['boxes']) for f in image_files]
    zero_box_imgs = sum(1 for c in box_counts if c == 0)
    
    class_counter = {c: 0 for c in CANONICAL_51_CLASSES}
    for f in image_files:
        for b in filtered_results[f]['boxes']:
            cname = b['class_name']
            class_counter[cname] = class_counter.get(cname, 0) + 1

    print(f"- Tổng số ảnh: {len(image_files):,}")
    print(f"- Tổng số bounding box phát hiện (conf >= {args.conf_thr}): {total_boxes:,}")
    print(f"- Trung bình box/ảnh: {total_boxes / len(image_files):.2f}")
    print(f"- Ảnh không có box nào: {zero_box_imgs} ({zero_box_imgs / len(image_files) * 100:.1f}%)")
    print(f"- Số box nhiều nhất trên 1 ảnh: {max(box_counts)}")
    print(f"- Số box ít nhất trên 1 ảnh: {min(box_counts)}")

    print("\n🔝 Top 15 món ăn xuất hiện nhiều nhất:")
    sorted_classes = sorted(class_counter.items(), key=lambda x: x[1], reverse=True)
    for rank, (cname, cnt) in enumerate(sorted_classes[:15], 1):
        print(f"  {rank:2d}. {cname:20s}: {cnt:5d} boxes ({cnt / max(total_boxes, 1) * 100:.1f}%)")

    # 5. Đóng gói Định dạng 1: CVAT YOLO 1.1 (Darknet)
    print("\n" + "=" * 70)
    print(f"📦 1. ĐÓNG GÓI ĐỊNH DẠNG CVAT YOLO 1.1 (conf >= {args.conf_thr})")
    print("=" * 70)
    yolo_dir = os.path.join(args.work_dir, 'cvat_yolo_1.1')
    yolo_obj_data_dir = os.path.join(yolo_dir, 'obj_train_data')
    os.makedirs(yolo_obj_data_dir, exist_ok=True)

    # File obj.names
    obj_names_path = os.path.join(yolo_dir, 'obj.names')
    with open(obj_names_path, 'w', encoding='utf-8') as f:
        for c in CANONICAL_51_CLASSES:
            f.write(c + '\n')

    # File obj.data
    obj_data_path = os.path.join(yolo_dir, 'obj.data')
    with open(obj_data_path, 'w', encoding='utf-8') as f:
        f.write(f"classes = {len(CANONICAL_51_CLASSES)}\n")
        f.write("train = data/train.txt\n")
        f.write("names = data/obj.names\n")
        f.write("backup = backup/\n")

    # File train.txt & các file nhãn txt trong obj_train_data/
    train_txt_path = os.path.join(yolo_dir, 'train.txt')
    with open(train_txt_path, 'w', encoding='utf-8') as train_f:
        for img_name in image_files:
            train_f.write(f"data/obj_train_data/{img_name}\n")
            stem = os.path.splitext(img_name)[0]
            label_file_path = os.path.join(yolo_obj_data_dir, f"{stem}.txt")
            
            rec = filtered_results[img_name]
            w, h = rec['width'], rec['height']
            with open(label_file_path, 'w', encoding='utf-8') as lbl_f:
                if w > 0 and h > 0:
                    for b in rec['boxes']:
                        cls_id = b['class_id']
                        x1, y1, x2, y2 = b['box_xyxy']
                        x1 = max(0.0, min(float(w), float(x1)))
                        y1 = max(0.0, min(float(h), float(y1)))
                        x2 = max(0.0, min(float(w), float(x2)))
                        y2 = max(0.0, min(float(h), float(y2)))
                        bw = x2 - x1
                        bh = y2 - y1
                        if bw <= 0 or bh <= 0:
                            continue
                        cx = x1 + bw / 2.0
                        cy = y1 + bh / 2.0
                        
                        norm_cx = cx / w
                        norm_cy = cy / h
                        norm_bw = bw / w
                        norm_bh = bh / h
                        lbl_f.write(f"{cls_id} {norm_cx:.6f} {norm_cy:.6f} {norm_bw:.6f} {norm_bh:.6f}\n")

    # Nén zip YOLO 1.1
    yolo_zip_path = os.path.join(WORKSPACE_DIR, 'vifood_2999_labels_cvat.zip')
    print(f"⏳ Đang nén file zip YOLO 1.1 ra: {yolo_zip_path} ...")
    with zipfile.ZipFile(yolo_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        zout.write(obj_names_path, 'obj.names')
        zout.write(obj_data_path, 'obj.data')
        zout.write(train_txt_path, 'train.txt')
        for img_name in image_files:
            stem = os.path.splitext(img_name)[0]
            txt_name = f"{stem}.txt"
            full_txt_path = os.path.join(yolo_obj_data_dir, txt_name)
            zout.write(full_txt_path, f"obj_train_data/{txt_name}")
    print(f"✅ Đã tạo thành công: {yolo_zip_path} ({os.path.getsize(yolo_zip_path) / 1024 / 1024:.2f} MB)")

    # 6. Đóng gói Định dạng 2: CVAT for images 1.1 XML
    print("\n" + "=" * 70)
    print(f"📦 2. ĐÓNG GÓI ĐỊNH DẠNG CVAT FOR IMAGES 1.1 XML (conf >= {args.conf_thr})")
    print("=" * 70)
    xml_path = os.path.join(args.work_dir, 'annotations.xml')
    print("⏳ Đang sinh file XML chuẩn CVAT 1.1...")
    with open(xml_path, 'w', encoding='utf-8') as xf:
        xf.write('<?xml version="1.0" encoding="utf-8"?>\n')
        xf.write('<annotations>\n')
        xf.write('  <version>1.1</version>\n')
        xf.write('  <meta>\n')
        xf.write('    <task>\n')
        xf.write('      <id>1</id>\n')
        xf.write('      <name>vifood_2999</name>\n')
        xf.write(f'      <size>{len(image_files)}</size>\n')
        xf.write('      <mode>annotation</mode>\n')
        xf.write('      <overlap>0</overlap>\n')
        xf.write('      <bugtracker></bugtracker>\n')
        xf.write('      <created>2026-10-01 00:00:00</created>\n')
        xf.write('      <updated>2026-10-01 00:00:00</updated>\n')
        xf.write('      <labels>\n')
        for c in CANONICAL_51_CLASSES:
            xf.write('        <label>\n')
            xf.write(f'          <name>{xml_escape(c)}</name>\n')
            xf.write('          <attributes></attributes>\n')
            xf.write('        </label>\n')
        xf.write('      </labels>\n')
        xf.write('    </task>\n')
        xf.write('  </meta>\n')

        for img_id, img_name in enumerate(image_files):
            rec = filtered_results[img_name]
            w, h = rec['width'], rec['height']
            xf.write(f'  <image id="{img_id}" name="{xml_escape(img_name)}" width="{w}" height="{h}">\n')
            for b in rec['boxes']:
                cname = xml_escape(b['class_name'])
                sc = b['score']
                x1, y1, x2, y2 = b['box_xyxy']
                xf.write(f'    <box label="{cname}" source="exp4" occluded="0" '
                         f'xtl="{x1:.1f}" ytl="{y1:.1f}" xbr="{x2:.1f}" ybr="{y2:.1f}" z_order="0" score="{sc:.4f}">\n')
                xf.write('    </box>\n')
            xf.write('  </image>\n')
        xf.write('</annotations>\n')

    cvat_xml_zip_path = os.path.join(WORKSPACE_DIR, 'vifood_2999_cvat_xml.zip')
    with zipfile.ZipFile(cvat_xml_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        zout.write(xml_path, 'annotations.xml')
    print(f"✅ Đã tạo thành công: {cvat_xml_zip_path} ({os.path.getsize(cvat_xml_zip_path) / 1024 / 1024:.2f} MB)")

    # 7. Đóng gói Định dạng 3: COCO 1.0 JSON
    print("\n" + "=" * 70)
    print(f"📦 3. ĐÓNG GÓI ĐỊNH DẠNG COCO 1.0 (conf >= {args.conf_thr})")
    print("=" * 70)
    coco_json_path = os.path.join(args.work_dir, 'instances_default.json')
    coco_categories = [{"id": i, "name": c, "supercategory": "food"} for i, c in enumerate(CANONICAL_51_CLASSES)]
    coco_images = []
    coco_annotations = []
    ann_id_counter = 1

    for img_id, img_name in enumerate(image_files, 1):
        rec = filtered_results[img_name]
        w, h = rec['width'], rec['height']
        coco_images.append({
            "id": img_id,
            "file_name": img_name,
            "width": w,
            "height": h
        })
        for b in rec['boxes']:
            cls_id = b['class_id']
            x1, y1, x2, y2 = b['box_xyxy']
            bw = max(0.0, x2 - x1)
            bh = max(0.0, y2 - y1)
            coco_annotations.append({
                "id": ann_id_counter,
                "image_id": img_id,
                "category_id": cls_id,
                "bbox": [round(x1, 2), round(y1, 2), round(bw, 2), round(bh, 2)],
                "area": round(bw * bh, 2),
                "score": b['score'],
                "iscrowd": 0
            })
            ann_id_counter += 1

    coco_data = {
        "info": {
            "description": f"ViFood 2999 Exp4 Inferred Labels for CVAT (conf >= {args.conf_thr})",
            "version": "1.0",
            "year": 2026,
            "contributor": "SoPSoP Team",
            "model": "Exp 4: Multi-Prompt & High-Res 800 (Grounding DINO Swin-T)"
        },
        "licenses": [],
        "categories": coco_categories,
        "images": coco_images,
        "annotations": coco_annotations
    }

    with open(coco_json_path, 'w', encoding='utf-8') as f:
        json.dump(coco_data, f, ensure_ascii=False, indent=2)

    coco_zip_path = os.path.join(WORKSPACE_DIR, 'vifood_2999_cvat_coco.zip')
    with zipfile.ZipFile(coco_zip_path, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
        zout.write(coco_json_path, 'instances_default.json')
    print(f"✅ Đã tạo thành công: {coco_zip_path} ({os.path.getsize(coco_zip_path) / 1024 / 1024:.2f} MB)")

    print("\n" + "=" * 70)
    print("✨ TOÀN BỘ QUÁ TRÌNH HOÀN TẤT THÀNH CÔNG RỰC RỠ!")
    print("=" * 70)
    print("📁 Danh sách file ZIP sẵn sàng để upload lên CVAT:")
    print(f"  1. [YOLO 1.1 (Chuẩn vifood2.zip)]: {yolo_zip_path}")
    print(f"  2. [CVAT for images 1.1 XML]:     {cvat_xml_zip_path}")
    print(f"  3. [COCO 1.0 JSON]:               {coco_zip_path}")

if __name__ == '__main__':
    main()
