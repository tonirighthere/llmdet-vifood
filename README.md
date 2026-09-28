# 🍜 LLMDet ViFood: Vietnamese Food Visual Grounding & Nutrition AI

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![PyTorch 2.10](https://img.shields.io/badge/PyTorch-2.10-orange.svg)](https://pytorch.org/)
[![MMDetection](https://img.shields.io/badge/MMDetection-3.3.0-green.svg)](https://github.com/open-mmlab/mmdetection)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

> **Hệ Thống Định Vị Món Ăn Việt Nam Bằng Ngôn Ngữ Tự Nhiên & Ước Tính Dinh Dưỡng**  
> Nghiên cứu và thực nghiệm mô hình thị giác - ngôn ngữ **Grounding DINO (Swin-T + BERT)** thích ứng trên tập dữ liệu **ViFood-51** (51 món ăn Việt Nam truyền thống).

---

## 📌 Điểm Nổi Bật Của Dự Án

- **Vượt qua Rào cản Ngôn ngữ (Cross-Lingual Grounding):** Giải quyết triệt để vấn đề BERT bias tiếng Anh thông qua kỹ thuật **Rich Vietnamese Captions** và **Multi-Prompting** (x3 ngữ cảnh), nâng độ phủ **Recall từ 23.3% lên 56.5% (+142%)**.
- **Bộ Dữ Liệu ViFood-1K Chuẩn Hóa:** 1,000 mâm cơm Việt Nam phân giải cao được gán nhãn 51 món ăn, đóng gói chuẩn định dạng ODVG (Object Detection in Visual Grounding) với 12,084 token spans positive khớp 100%.
- **Huấn Luyện Đa Tỉ Lệ (Multi-Scale Res 800x1333):** Mở rộng không gian đặc trưng giúp phát hiện chuẩn xác từ các chi tiết nhỏ (sợi bún, rau thơm) đến các đĩa lớn, mâm cơm tổng thể.
- **Tích Hợp Module Dinh Dưỡng Tự Động:** Cơ sở dữ liệu chuẩn hóa 51 món ăn gồm Calo (kcal), Đạm (g), Tinh bột (g), Chất béo (g) và cảnh báo sức khỏe.
- **Ứng Dụng Web Demo Tương Tác:** Giao diện Gradio trực quan hỗ trợ phân tích ngôn ngữ tự nhiên tiếng Việt thông minh (`Smart NLP Parser`).

---

## 📊 Bảng Kết Quả Thực Nghiệm Benchmark (COCO Metric)

Đánh giá độc lập trên tập kiểm thử 100 ảnh validation (`instances_val.json`):

| Mô hình / Thí nghiệm | Chiến lược Text Prompt | mAP (0.50:0.95) | mAP_50 | mAP_75 | mAP_l (Vật thể lớn) | Average Recall (AR) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Zero-Shot Baseline** | Trọng số gốc Swin-T chưa fine-tune | 0.026 | 0.034 | 0.031 | 0.030 | 0.392 (39.2%) |
| **Exp 1: Short VI** | Prompt nhãn ngắn tiếng Việt (`phở . bánh mì .`) | 0.024 | 0.037 | 0.027 | 0.031 | 0.233 (23.3%) |
| **Exp 2: Short EN** | Prompt nhãn ngắn tiếng Anh (`pho . bread .`) | 0.055 | 0.084 | 0.055 | 0.055 | 0.368 (36.8%) |
| **Exp 3: Full VI Caption** | Câu miêu tả tự nhiên tiếng Việt phong phú | **0.055** | 0.074 | **0.066** | 0.057 | 0.543 (54.3%) |
| **⭐ Exp 4: Multi-Prompt + Res 800** | **x3 Biến thể ngữ cảnh + Đa tỉ lệ (480-800x1333)** | 0.054 | **0.075** | 0.063 | **0.060** | **0.565 (56.5%) 🏆** |

---

## 🗂 Cấu Trúc Dự Án

```bash
├── grounding_data/               # Dữ liệu gán nhãn Visual Grounding
│   └── vifood/annotations/       # Instances JSON & ODVG JSONL (train/val)
├── llmdet_vietnamese_food/       # Mã nguồn chính của hệ thống
│   ├── app.py                    # Ứng dụng Web Demo AI & Phân tích Dinh Dưỡng
│   ├── configs/                  # File cấu hình MMDetection & Grounding DINO
│   ├── mmdet/                    # Lõi thư viện MMDetection tùy biến
│   ├── nutrition_vifood_51.json  # Cơ sở dữ liệu dinh dưỡng 51 món ăn
│   ├── mmdet_train.py            # Script khởi chạy huấn luyện
│   └── mmdet_test.py             # Script chạy đánh giá benchmark định lượng
├── scripts/                      # Bộ công cụ sinh dữ liệu & tiền xử lý
│   ├── build_multi_prompt_odvg.py# Sinh x3 multi-prompt ODVG
│   ├── enrich_and_build_odvg.py  # Sinh Dual-Caption & tính token spans
│   └── prepare_vifood_1k.py      # Trích xuất và phân chia tập ViFood-1K
├── sessions/                     # Toàn bộ 16 Session Logs chi tiết từng ngày
│   ├── README.md                 # Mục lục các phiên làm việc
│   └── PLAN_NEXT_STEPS.md        # Kế hoạch mở rộng nghiên cứu
├── .gitignore                    # Loại trừ weights nặng (>100MB) & cache
└── README.md
```

---

## 🚀 Hướng Dẫn Cài Đặt & Sử Dụng

### 1. Khởi tạo môi trường
```bash
conda create -n vifood python=3.11 -y
conda activate vifood

# Cài đặt PyTorch và MMDetection dependencies
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
pip install openmim
mim install mmengine "mmcv>=2.0.0"
pip install transformers timm gradio opencv-python Pillow
```

### 2. Chạy Ứng Dụng Web Demo
```bash
cd llmdet_vietnamese_food
python app.py
```
Truy cập tại: `http://localhost:7861`

### 3. Huấn luyện Mô hình
```bash
python mmdet_train.py \
    configs/grounding_dino_swin_t_vifood_multi_res800.py \
    --work-dir work_dirs/vifood_multi_res800 \
    --amp
```

### 4. Đánh giá Định lượng Benchmark (COCO Metric)
```bash
python mmdet_test.py \
    configs/val/grounding_dino_swin_t_vifood_val.py \
    work_dirs/vifood_multi_res800/iter_10000.pth \
    --work-dir work_dirs/eval_exp4_multi_res800
```

---

## 📜 Tài Liệu Học Thuật & Luận Văn
Toàn bộ nhật ký thí nghiệm chi tiết phục vụ viết các chương Luận văn tốt nghiệp được lưu trữ trong thư mục [`sessions/`](sessions/README.md).
