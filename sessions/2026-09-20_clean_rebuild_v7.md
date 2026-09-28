# NHẬT KÝ PHIÊN LÀM VIỆC: 20/09/2026 – 21/09/2026
## Chủ đề: Hoàn thiện Pipeline Clean Rebuild v7 & Hợp nhất Phân cấp

---

### 1. Thông tin chung
* **Thời gian**: 20/09/2026 – 21/09/2026
* **Mục tiêu**: Xây dựng thuật toán lọc sạch toàn bộ bounding box AI kém chất lượng, hợp nhất phân cấp nhãn và kiểm soát số lượng mẫu cân bằng.
* **Người thực hiện**: [Họ và tên của bạn]

---

### 2. Thuật toán và Cải tiến Kỹ thuật
* **Phát triển script cốt lõi**: `vietnamese-food-dataset/scripts/build_dataset_v7.py` (627 dòng code).
* **Các cơ chế kỹ thuật được áp dụng**:
  1. **Hierarchical Merging (Hợp nhất có phân cấp)**:
     - Gộp tất cả họ tôm (tôm hùm, tôm sú, tôm càng, tôm tít, gỏi tôm...) thành một lớp chung duy nhất: `"tôm"`.
     - Phân định rạch ròi 3 phân lớp hải sản vỏ cứng vốn hay bị gộp ẩu: `"ốc"`, `"ngao sò"` và `"hàu"`.
     - Đại diện hóa nhóm món: `"cá kho tộ"` (đại diện món cá), `"gà luộc"` (đại diện món gà), `"thịt bò"` (gộp bò lúc lắc, bò nướng, bò kho...).
  2. **Candidate Pruning**: Loại bỏ 100% các bounding box có cờ `is_candidate=True` hoặc độ tin cậy thấp do các script AI tự động trước đó gán vào.
  3. **Cap Boxes per Class**: Đặt trần `MAX_BOXES_PER_CLASS = 500` để ngăn các lớp quá phổ biến (như cơm, rau) áp đảo hoàn toàn các lớp khác trong quá trình tính loss.

---

### 3. Kết quả đạt được
* Bộ nhãn được tinh gọn thành **35 - 43 lớp món ăn cốt lõi**, sạch sẽ, không còn nhãn rác.
* Xuất file metadata và các file định dạng COCO chuẩn tại `vietnamese-food-dataset/data/exports/v7/`.
* Đóng gói tập dữ liệu sạch `vietnamese_food_dataset_1962.zip` (133 MB).

---

### 4. Ghi chú cho Báo cáo Luận văn
> *Nội dung này là điểm sáng trong **Chương 3 (Thu thập & Tiền xử lý dữ liệu)**: Chứng minh được phương pháp xử lý mất cân bằng lớp (Class Imbalance) và lọc nhiễu nhãn (Label Noise Filtering).*
