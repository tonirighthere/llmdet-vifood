# HƯỚNG DẪN CHI TIẾT MÃ NGUỒN CƠ SỞ LLMDET VÀ QUY TRÌNH FINE-TUNING NHẬN DIỆN MÓN ĂN VIỆT NAM

---

## PHẦN 1: TỔNG QUAN VỀ CẤU TRÚC THƯ MỤC VÀ TỆP MÃ NGUỒN (PROJECT ARCHITECTURE MAP)

Cấu trúc tổng thể của dự án **LLMDet**:

```text
LLMDet/
├── configs/                         # Thư mục chứa các file cấu hình (Config files)
│   ├── grounding_dino_swin_t.py      # Config cho bản Swin-Tiny (Mô hình chuẩn dùng train/test)
│   ├── grounding_dino_swin_b.py      # Config cho bản Swin-Base (Mô hình lớn hơn, mAP cao hơn)
│   ├── grounding_dino_swin_l.py      # Config cho bản Swin-Large (Mô hình lớn nhất)
│   ├── grounding_dino_swin_t_only_p5.py # Config tối ưu chỉ dùng Feature map P5 cho LLM
│   ├── val/                         # Các config đánh giá trên LVIS, COCO, ODinW, RefExp
│   └── _base_/                      # Cấu hình nền tảng (datasets, schedules, runtime)
│
├── mmdet/                           # Thư mục cốt lõi của Detector (dựa trên MMDetection v3)
│   ├── models/
│   │   ├── detectors/
│   │   │   └── grounding_dino.py    # [QUAN TRỌNG] Class GroundingDINO chính tích hợp LMM
│   │   ├── dense_heads/
│   │   │   └── grounding_dino_head.py # BBox Regression & Focal Loss/Contrastive Loss
│   │   ├── backbones/               # Swin Transformer & ResNet backbones
│   │   └── language_models/         # BERT Transformer text encoder wrapper
│   ├── datasets/
│   │   ├── odvg.py                  # [QUAN TRỌNG] Dataset loader đọc định dạng JSONL (OD & VG)
│   │   ├── coco.py / lvis.py        # Dataset loaders tiêu chuẩn COCO / LVIS
│   │   └── transforms/              # Pipeline biến đổi ảnh & mẫu hóa nhãn (RandomSamplingNegPos2)
│   └── apis/
│       └── det_inferencer.py        # Interface suy luận cao cấp DetInferencer
│
├── llava/                           # Thư mục chứa kiến trúc MLLM (LLaVA-Qwen2)
│   ├── model/
│   │   ├── language_model/llava_qwen.py # Class LLaVA kết hợp Qwen2 LMM
│   │   └── multimodal_projector/        # Lớp chiếu Feature Map sang hidden space của LLM
│   ├── train/                       # Module huấn luyện LLaVA Trainer
│   └── eval/                        # Kịch bản đánh giá các benchmark đa phương thức
│
├── hf_model/                        # Thư mục phục vụ đóng gói và chuyển đổi sang HuggingFace
│   ├── modeling_grounding_dino.py   # Implementation Grounding DINO tương thích chuẩn HF Transformers
│   ├── convert_grounding_dino_to_hf.py # Script convert checkpoint .pth (MMDet) sang .safetensors (HF)
│   └── demo_hf.py                   # Script demo chạy với thư viện transformers
│
├── ram/                             # Module Recognize Anything Model (RAM / Tag2Text)
│   └── models/                      # Các mô hình sinh tag tự động (ViT, Swin, Tag2Text)
│
├── weights/                         # Thư mục lưu mô hình local dạng HuggingFace
│   ├── model.safetensors            # Trọng số mô hình HF
│   ├── config.json                  # Cấu hình kiến trúc HF
│   └── tokenizer_config.json        # Cấu hình Tokenizer
│
├── images/                          # Thư mục chứa ảnh thử nghiệm demo
├── scripts/                         # Các shell script huấn luyện DeepSpeed (my_pretrain.sh, zero3.json...)
├── hf_demo.py                       # [QUAN TRỌNG] Script suy luận nhanh Zero-shot với HuggingFace
├── image_demo.py                    # [QUAN TRỌNG] Script suy luận MMDetection DetInferencer
├── mmdet_train.py / dist_train.sh   # [QUAN TRỌNG] Script chạy huấn luyện mô hình (Single/Multi-GPU)
├── mmdet_test.py / dist_test.sh     # [QUAN TRỌNG] Script chạy kiểm thử / đánh giá mAP
└── train.py                         # Script huấn luyện MLLM LLaVA co-training
```

---

## PHẦN 2: CHI TIẾT TÁC DỤNG VÀ CHỨC NĂNG CÁC FILE CHÍNH (FILE-BY-FILE GUIDE)

### 1. Nhóm File Suy luận & Demo (Inference & Demo Scripts)

#### 📄 `hf_demo.py`
* **Tác dụng**: Chạy suy luận nhanh Zero-Shot Object Detection bằng thư viện `transformers` của HuggingFace từ thư mục weights local (`./weights`).
* **Cách hoạt động**:
  ```python
  # 1. Load processor & model từ local folder ./weights
  processor = AutoProcessor.from_pretrained("./weights")
  model = AutoModelForZeroShotObjectDetection.from_pretrained("./weights").to(device)

  # 2. Đưa ảnh và prompt văn bản tiếng Anh vào
  inputs = processor(images=image, text=[["spring rolls"]], return_tensors="pt")

  # 3. Chạy suy luận (không tốn GPU cho LLM vì đã tách LLM)
  outputs = model(**inputs)

  # 4. Post-processing lọc score > 0.3 và vẽ Bounding Box
  results = processor.post_process_grounded_object_detection(outputs, threshold=0.3, ...)
  ```
* **Khi nào can thiệp**: Khi cần làm ứng dụng web nhẹ, API suy luận nhanh không cần MMDetection.

#### 📄 `image_demo.py`
* **Tác dụng**: Chạy suy luận chuyên sâu dựa trên MMDetection `DetInferencer`.
* **Tham số quan trọng**:
  * `--texts`: Nhập prompt văn bản (VD: `'spring rolls .'` hoặc `'$: lvis'`).
  * `-c` (`--custom-entities`): Bật chế độ tùy chỉnh từ khóa danh mục.
  * `-p` (`--tokens-positive`): Chỉ định vị trí từ khóa quan tâm trong câu (dùng cho Referential Expression / Phrase Grounding).
  * `-s` (`--chunked-size`): Cắt nhỏ danh sách từ khóa nếu có hàng trăm danh mục.

---

### 2. Nhóm File Huấn luyện & Đánh giá (Training & Testing Scripts)

#### 📄 `mmdet_train.py` & `dist_train.sh`
* **Tác dụng**: Script chính để fine-tune hoặc huấn luyện mô hình Grounding DINO / LLMDet.
* **Cách hoạt động**: Đọc file config (ví dụ `configs/grounding_dino_swin_t.py`), khởi tạo `Runner` từ MMEngine, thiết lập tự động scale learning rate (`auto_scale_lr`), bật Mixed Precision (`--amp`), và khởi chạy vòng lặp huấn luyện `IterBasedTrainLoop`.
* **Cú pháp chạy**:
  ```bash
  # Train 1 GPU
  python mmdet_train.py configs/grounding_dino_swin_t.py --work-dir work_dirs/vifood --amp

  # Train Multi-GPU (VD: 4 GPUs)
  bash dist_train.sh configs/grounding_dino_swin_t.py 4 --amp
  ```

#### 📄 `mmdet_test.py` & `dist_test.sh`
* **Tác dụng**: Đánh giá mô hình đã huấn luyện trên tập kiểm thử (Validation / Test Set) để tính chỉ số mAP / AP50 / Fixed AP.

---

### 3. Nhóm File Cấu hình (Configuration Files in `configs/`)

#### 📄 `configs/grounding_dino_swin_t.py`
Đây là file cấu hình quan trọng nhất bạn sẽ dùng làm khuôn mẫu để tạo file config fine-tune món ăn Việt Nam (`configs/grounding_dino_swin_t_vifood.py`).

* **Cấu trúc các khối quan trọng**:
  1. `model`: Khai báo loại mô hình `type='GroundingDINO'`, đường dẫn LMM (`lmm=lmm_path`), đường dẫn BERT (`language_model`), tỉ lệ loss (`lmm_region_loss_weight`, `lmm_image_loss_weight`), số lớp LoRA (`lora_r=128`).
  2. `train_pipeline`: Chuỗi tiền xử lý dữ liệu: `LoadImageFromFile` $\rightarrow$ `RandomChoiceResize` $\rightarrow$ `RandomSamplingNegPos2` (mẫu hóa từ khóa dương/âm) $\rightarrow$ `PackDetInputs`.
  3. `train_dataloader`: Định nghĩa tập dataset huấn luyện `ODVGDataset` (kết hợp COCO, Flickr30k, GQA, V3Det...).
  4. `optim_wrapper`: Khai báo Optimizer (`AdamW`, `lr=0.0001`), gradient clipping và phân chia learning rate (`lr_mult=0.1` cho backbone).
  5. `param_scheduler`: Bộ điều phối tốc độ học (`LinearLR` warmup 1000 iter đầu + `MultiStepLR`).

---

### 4. Nhóm File Kiến trúc Mô hình (Model Architecture in `mmdet/models/`)

#### 📄 `mmdet/models/detectors/grounding_dino.py` (Class `GroundingDINO`)
* **Tác dụng**: Lớp mô hình chính kết hợp giữa Detector (DINO) + Text Encoder (BERT) + Large Multimodal Model (LLaVA-Qwen2).
* **Các phương thức quan trọng**:
  * `__init__()`: Khởi tạo các module Swin Backbone, BERT Language Model, LMM Qwen2, LMM connectors (projectors), LoRA layers.
  * `forward_encoder()` & `forward_decoder()`: Chạy biến đổi đặc trưng đa tỉ lệ qua Deformable Transformer Encoder/Decoder.
  * `loss()`: Tính tổng các hàm mất mát ($L_{focal} + L_{l1} + L_{giou} + L_{lmm\_image} + L_{lmm\_region}$).
  * `predict()`: Luồng suy luận dự đoán Bounding Box và gán tên lớp tương ứng với prompt văn bản đầu vào.

#### 📄 `mmdet/datasets/odvg.py` (Class `ODVGDataset`)
* **Tác dụng**: Bộ đọc dữ liệu định dạng JSONL (hỗ trợ cả bài toán Object Detection `actual_dataset_mode='OD'` và Visual Grounding `actual_dataset_mode='VG'`).

---

## PHẦN 3: HƯỚNG DẪN ĐỊNH DẠNG DATASET MÓN ĂN VIỆT NAM (ODVG JSONL FORMAT)

Dữ liệu để fine-tune LLMDet được tổ chức theo cấu trúc thư mục sau:

```text
grounding_data/
└── vifood/
    ├── images/
    │   ├── train2017/           # Thư mục chứa toàn bộ ảnh huấn luyện
    │   │   ├── buacom_001.jpg
    │   │   ├── buacom_002.jpg
    │   │   └── ...
    │   └── val2017/             # Thư mục chứa toàn bộ ảnh kiểm thử
    └── annotations/
        ├── vifood_train_vg.jsonl  # [QUAN TRỌNG] File nhãn huấn luyện dạng JSONL
        └── vifood_val.json        # File nhãn kiểm thử dạng COCO JSON
```

### 1. Cấu trúc chi tiết file `vifood_train_vg.jsonl` (Chuẩn ODVG Format)
Mỗi dòng trong file `.jsonl` là 1 chuỗi JSON hoàn chỉnh đại diện cho **1 bức ảnh**:

#### Mẫu 1: Nhãn dạng Visual Grounding (VG Mode - Khuyên dùng)
```json
{
  "filename": "train2017/buacom_001.jpg",
  "height": 800,
  "width": 1200,
  "detection": {
    "instances": [
      {
        "bbox": [983.33, 412.89, 1146.46, 503.29],
        "label": "nem_ran",
        "text": "a crispy vietnamese fried spring roll"
      },
      {
        "bbox": [966.01, 378.71, 1115.48, 446.9],
        "label": "nem_ran",
        "text": "a crispy vietnamese fried spring roll"
      },
      {
        "bbox": [320.5, 150.0, 750.2, 520.8],
        "label": "dia_nem_ran",
        "text": "a plate of vietnamese fried spring rolls with dipping sauce"
      },
      {
        "bbox": [480.0, 200.5, 780.4, 450.0],
        "label": "thit_kho_to",
        "text": "a clay pot of vietnamese braised pork belly"
      }
    ]
  }
}
```

* **Lưu ý quan trọng về Bounding Box**:
  * Tọa độ Bounding Box có dạng `[x1, y1, x2, y2]` (Góc trên-trái và Góc dưới-phải pixel).
  * **Khoanh vùng đa cấp độ (Multi-granularity)**: Nên gán nhãn cả từng chiếc nem đơn lẻ (`nem_ran`) VÀ khoanh toàn bộ đĩa nem (`dia_nem_ran`) để mô hình hiểu được cả 2 mức độ truy vấn người dùng!

---

## PHẦN 4: HƯỚNG DẪN TỪNG BƯỚC CAN THIỆP & FINE-TUNING LLMDET

### Bước 1: Tạo file Config custom `configs/grounding_dino_swin_t_vifood.py`
Tạo file config mới và chỉnh sửa các đường dẫn dữ liệu:

```python
_base_ = ['./grounding_dino_swin_t.py']

# 1. Đường dẫn dataset món ăn Việt Nam
vifood_train_dataset = dict(
    type='ODVGDataset',
    data_root='../grounding_data/vifood/',
    ann_file='annotations/vifood_train_vg.jsonl',
    data_prefix=dict(img='images/'),
    pipeline={{_base_.train_pipeline}},
    return_classes=True,
    actual_dataset_mode='VG',
    backend_args=None)

# 2. Cập nhật Dataloader
train_dataloader = dict(
    batch_size=4,
    num_workers=4,
    dataset=dict(
        _delete_=True,
        type='ConcatDataset',
        datasets=[vifood_train_dataset]
    )
)

# 3. Đường dẫn lưu checkpoint & max_iter
max_iter = 20000
train_cfg = dict(max_iters=max_iter, val_interval=2000)
work_dir = './work_dirs/grounding_dino_swin_t_vifood'

# 4. Trọng số nạp ban đầu (Pretrained Checkpoint)
load_from = '../huggingface/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth'
```

### Bước 2: Khởi chạy huấn luyện Fine-tuning
Chạy lệnh trong terminal:
```bash
python mmdet_train.py configs/grounding_dino_swin_t_vifood.py --work-dir work_dirs/grounding_dino_swin_t_vifood --amp
```

### Bước 3: Đóng gói sang định dạng HuggingFace để chạy `hf_demo.py`
Sau khi train xong, dùng script `hf_model/mmdet2groundingdino_swint.py` để convert checkpoint `.pth` trong `work_dirs/` sang `.safetensors` lưu vào thư mục `./weights`:

```bash
python hf_model/mmdet2groundingdino_swint.py \
    configs/grounding_dino_swin_t_vifood.py \
    work_dirs/grounding_dino_swin_t_vifood/iter_20000.pth \
    --save-path ./weights
```

---
*Tài liệu tổng hợp mã nguồn được biên soạn dành cho dự án Đồ án Tốt nghiệp LLMDet Vietnamese Food Grounding.*
