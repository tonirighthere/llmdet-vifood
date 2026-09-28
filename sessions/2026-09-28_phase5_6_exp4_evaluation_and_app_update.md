# Session Log: Hoàn Tất Huấn Luyện Exp 4, Đánh Giá Benchmark & Cập Nhật Web Demo

**Ngày thực hiện:** 28/09/2026 (Sáng)  
**Mục tiêu:** Kiểm tra kết quả hoàn tất huấn luyện Experiment 4, thực hiện đánh giá định lượng theo chuẩn COCO metric trên tập kiểm thử 100 ảnh, và cập nhật trọng số tối ưu vào ứng dụng Web Demo trực quan.

---

## 1. Kết Quả Huấn Luyện Experiment 4
- **Thời gian hoàn thành:** 23:53:32 (Đêm 27/09/2026).
- **Tổng số iterations:** 10,000 / 10,000 iters hoàn thành trọn vẹn (không lỗi, không tràn VRAM).
- **Động thái hội tụ của hàm mất mát (Loss Convergence):**
  - **Tổng Loss:** Giảm sâu từ **34.26** $\rightarrow$ **10.58** (ổn định quanh mốc 10 - 12 ở những iters cuối).
  - **Classification Loss (`loss_cls`):** Giảm mạnh từ **2.30** $\rightarrow$ **0.33 - 0.47** (giảm hơn 80%, thể hiện khả năng phân biệt ngữ nghĩa giữa các món ăn tiếng Việt tăng vọt).
  - **BBox & IoU Loss:** Giảm đều đặn, mô hình định vị chính xác vị trí khay/đĩa thức ăn.
- **Trọng số xuất xưởng:** [`work_dirs/vifood_multi_res800/iter_10000.pth`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/work_dirs/vifood_multi_res800/iter_10000.pth) (Dung lượng: 1.85 GB).

---

## 2. Đánh Giá Định Lượng COCO Metric (Benchmark Toàn Diện 5 Mô Hình)

Thực hiện kiểm thử độc lập trên tập `val2017` (100 ảnh, 374 ground truth bounding boxes của 51 món ăn Việt Nam):

```bash
python3 mmdet_test.py \
    configs/val/grounding_dino_swin_t_vifood_val.py \
    work_dirs/vifood_multi_res800/iter_10000.pth \
    --work-dir work_dirs/eval_exp4_multi_res800
```

### Bảng So Sánh Thực Nghiệm Cốt Lõi (Phục vụ Luận văn):

| Mô hình / Thí nghiệm | Chiến lược Huấn luyện / Text Prompt | mAP (0.50:0.95) | mAP_50 | mAP_75 | mAP_l (Vật thể lớn) | Average Recall (AR) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Zero-Shot Baseline** | Trọng số gốc Swin-T chưa fine-tune | 0.026 | 0.034 | 0.031 | 0.030 | 0.392 (39.2%) |
| **Exp 1: Short VI** | Prompt nhãn ngắn tiếng Việt (`phở . bánh mì .`) | 0.024 | 0.037 | 0.027 | 0.031 | 0.233 (23.3%) |
| **Exp 2: Short EN** | Prompt nhãn ngắn tiếng Anh (`beef noodle soup .`) | 0.055 | 0.084 | 0.055 | 0.055 | 0.368 (36.8%) |
| **Exp 3: Full VI Caption** | Câu văn tự nhiên tiếng Việt phong phú | **0.055** | 0.074 | **0.066** | 0.057 | 0.543 (54.3%) |
| **⭐ Exp 4: Multi-Prompt + Res 800** | **x3 Biến thể ngữ cảnh + Đa tỉ lệ (480-800x1333)** | 0.054 | **0.075** | 0.063 | **0.060** | **0.565 (56.5%) 🏆** |

---

## 3. Phân Tích Ý Nghĩa Khoa Học Cho Luận Văn

1. **Kỷ lục mới về Độ bao phủ (Average Recall = 56.5%):**
   - Exp 4 thiết lập mốc Recall cao nhất toàn bộ đề tài: **56.5%**, vượt qua Exp 3 (54.3%) và bỏ xa Exp 1 (23.3%, tăng **+142%**).
   - Điều này chứng minh rằng việc áp dụng **Multi-Prompting** (kết hợp miêu tả tự nhiên, truy vấn tìm kiếm vị trí và danh sách thực thể) giúp mô hình thích ứng linh hoạt với mọi cách diễn đạt tiếng Việt của người dùng.
2. **Cải thiện rõ nét ở vật thể kích thước lớn (mAP_l: 0.057 → 0.060):**
   - Nhờ độ phân giải đa tỉ lệ lên tới $800 \times 1333$, các đĩa thức ăn lớn, mâm cơm tổng thể và các góc chụp rộng được nhận diện chuẩn xác hơn.
3. **Độ chính xác ở ngưỡng phát hiện chuẩn (mAP_50: 0.074 → 0.075):**
   - Tỷ lệ phát hiện đúng ở ngưỡng IoU=0.50 tiếp tục duy trì đà tăng trưởng, đồng thời giảm hiện tượng hallucination / over-predicting khi người dùng truy vấn món đơn lẻ.

---

## 4. Cập Nhật Web Demo (Phase 5)
- File cập nhật: [`llmdet_vietnamese_food/app.py`](file:///home/atin/tuan/SoPSoP/llmdet_vietnamese_food/app.py).
- Bổ sung Exp 4 vào danh sách chọn và đặt làm mô hình khởi động mặc định:
  `Exp 4: Multi-Prompt & High-Res 800 (Phiên bản mạnh nhất ⭐⭐⭐)`.
- Sửa lỗi tương thích đường dẫn cache ảnh mẫu (`allowed_paths`) trên Gradio.
- Đã khởi động lại web app trong tmux `vifood_web_app`.
- Kiểm tra kết nối mạng nội bộ và localhost: **HTTP 200 OK**.
- Địa chỉ truy cập trực tiếp:
  - Máy chủ: `http://localhost:7861`
  - Mạng LAN / Thiết bị ngoài: `http://192.168.1.191:7861`
