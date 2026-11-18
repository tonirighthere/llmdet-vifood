# Sinh caption v2 trên máy thuê Vast.ai (A100 PCIE 80 GB)

Mục tiêu: caption tiếng Anh chi tiết cho loss LLM (B5b, OV-W), bám nguyên tắc paper LLMDet (mục 3, Table 7):
tên món / vị trí / số lượng lấy từ nhãn; VLM mô tả từng món trên crop + bối cảnh; model khác kiểm chứng; bản Việt dịch
1:1 để người duyệt. Code: `scripts/vifood54/captions/caption_v2.py` (gọi vLLM, chạy theo lô bằng 32 yêu cầu song song).

Máy đã chọn (16/11/2026): **1× A100 PCIE 80 GB, Anh, offer #60219590, 0.872 USD/giờ** (độ tin cậy 98.3%, mạng ~9 Gbps,
ổ tối đa 148 GB, CUDA 13.1). Giá Vast đổi liên tục; hết máy này thì chọn A100 80 GB / RTX PRO 6000 96 GB khác, độ tin cậy ≥ 98%.

Ước tính (chưa đo; số thật in ra trong log mỗi 50 ảnh): cài đặt ~0.5 h · chạy thử ~1–1.5 h · chạy cả tập ~2–4 h
→ **~4–8 giờ ≈ 4–7 USD** + băng thông < 1 USD. Nạp 15 USD.

---

## 0. Chuẩn bị (máy nhóm, không tốn tiền)

1. **Code lên GitHub**: nhánh `truong/b5-en-v2` phải có `scripts/vifood54/captions/vast/` (máy thuê `git clone` nhánh này).
2. **Gói dữ liệu** — trên server của nhóm (nơi có ảnh và `annotations_en/*.jsonl`):
   ```bash
   git pull && bash scripts/vifood54/captions/vast/pack_for_caption.sh     # -> caption_pack.tar (ảnh train + annotation)
   ```
   Chỉ gói đúng 3138 ảnh train + `train_od.jsonl` + `taxonomy.json`, giữ nguyên đường dẫn. (Zip ảnh raw là không đủ:
   máy thuê cần `annotations_en/train_od.jsonl` để biết box và tên món.)
3. **Tài khoản Vast**: xác minh email, nạp 15 USD, thêm SSH public key của server nhóm ở *Keys* (để chép file thẳng
   server nhóm ↔ máy thuê).
4. **Hugging Face**: các model mặc định (Qwen3-VL, `google/gemma-4-12B-it`, giấy phép Apache 2.0) tải công khai, không cần
   token. Chỉ cần `HF_TOKEN` nếu đổi sang model có cổng điều khoản (vd. Gemma 3) hoặc bị giới hạn tốc độ tải.

## 1. Thuê máy

Sửa template **vLLM** của Vast (nút sửa template → lưu thành bản riêng), chỉ đổi các mục sau, còn lại giữ nguyên:

| Mục | Chọn |
| :--- | :--- |
| Template Name | `vifood-caption` |
| Image | giữ `vastai/vllm:v0.32.0-cuda-13.0` (vLLM mới, chạy được Qwen3-VL; máy hỗ trợ CUDA 13.1) |
| Ports | giữ nguyên (script dùng cổng nội bộ 9100/9101, không cần mở) |
| Env `VLLM_MODEL` | **xóa** (nếu không, máy tự tải + chạy Qwen3.5-9B, chiếm GPU). `setup.sh` vẫn tắt nó nếu còn chạy |
| Env `VLLM_ARGS` | xóa (chỉ dùng cho vLLM tự chạy của template) |
| Env khác (PORTAL_CONFIG, RAY_*, …) | giữ |
| **Không** thêm `HF_TOKEN` vào Env | token `export` trong terminal ở bước 2 |
| Launch Mode | Interactive shell server, SSH + tích *direct SSH* |
| On-start Script | chỉ để `entrypoint.sh` (xóa dòng `echo "--compilation-config ..."`) |
| Docker Repository Authentication | để trống |
| Container disk size | **140 GB** (máy #60219590 tối đa 148; 150 sẽ không thuê được) |
| Add recommended volume settings | **không** tích (volume tính phí riêng, sống sau khi Destroy) |
| Public / Private | **Private** |

Bấm **Create & Use** → quay lại trang Search, tìm offer #60219590 → **Rent** (On-Demand).

## 2. Cài đặt (~0.5 giờ)

Từ server nhóm (lấy `IP`, `PORT` ở nút *Connect* của instance):
```bash
scp -P <PORT> caption_pack.tar root@<IP>:/workspace/
scp -P <PORT> scripts/vifood54/captions/vast/setup.sh root@<IP>:/workspace/
ssh -p <PORT> root@<IP>
```
Hoặc, nếu gói đã nằm trên Google Drive (chia sẻ "bất kỳ ai có link"): bỏ lệnh `scp caption_pack.tar`, chỉ chép `setup.sh`,
rồi trên máy thuê `export PACK_URL="<link Drive>"` trước khi chạy `setup.sh` — máy thuê tự tải gói.

Trên máy thuê (nên chạy trong `tmux` để mất kết nối không dừng việc):
```bash
tmux new -s cap
export HF_TOKEN=hf_...            # token Read ở bước 0.4
bash /workspace/setup.sh          # clone repo, giải nén gói, kiểm tra vLLM, chạy test CPU, in GPU + ổ trống
cd /workspace/llmdet-vifood
```

## 3. Chạy thử 50 ảnh × 3 model (~1–1.5 giờ)

```bash
bash scripts/vifood54/captions/vast/run_pilot.sh
```
- Mô tả: `Qwen3-VL-8B` (mốc dưới) → `Qwen2.5-VL-72B-Instruct-AWQ` (gần cỡ paper) → `Qwen3-VL-32B` (ứng viên chính).
  Model nhỏ bị xóa khỏi ổ sau khi dùng; 32B được giữ cho bước 4.
- Kiểm chứng + dịch: `google/gemma-4-12B-it` (khác dòng với Qwen → kiểm chứng chéo có ý nghĩa).
- Ra `captions_pilot.tgz` (gồm `captions_v2/COMPARE.md`, `compare_scores.csv`). Chép về server nhóm:
  `scp -P <PORT> root@<IP>:/workspace/llmdet-vifood/captions_pilot.tgz .`

Nếu vLLM không nạp được Gemma 4 (log in đường dẫn file log): đặt `VERIFIER=` một model vLLM hỗ trợ, khác dòng Qwen, ví dụ
`google/gemma-3-12b-it` (cũng cần chấp nhận điều khoản) hoặc `OpenGVLab/InternVL3_5-8B`, rồi chạy lại — bước nào đã xong
sẽ được bỏ qua. Tên các repo model ở trên cần kiểm tra lại trên Hugging Face trước khi thuê.

**Chấm** (người, không cần GPU): mở `COMPARE.md`, đọc bản Việt [A]/[B]/[C] của từng ảnh, điền `compare_scores.csv`:
số câu sai, số chi tiết chung chung, điểm 1–5. Chấm xong trong ngày → để máy chạy (≈0.9 USD/giờ);
qua đêm → **Destroy** instance, hôm sau thuê lại và chạy lại bước 2.

Chọn model: ít câu sai nhất; hòa thì chọn model có nhiều chi tiết qua kiểm chứng / ảnh hơn.
Ngưỡng để chạy cả tập: ≥ 70 từ TB, < 1 câu sai / 10 caption.

## 4. Chạy cả tập train (~2–4 giờ)

```bash
DESCRIBER=Qwen/Qwen3-VL-32B-Instruct bash scripts/vifood54/captions/vast/run_full.sh
```
Log in tiến độ + thời gian còn lại mỗi 50 ảnh. Mất kết nối / dừng giữa chừng: chạy lại đúng lệnh, ảnh đã xong được bỏ qua.
Ra `captions_full.tgz`.

## 5. Kết thúc — làm ngay

```bash
scp -P <PORT> root@<IP>:/workspace/llmdet-vifood/captions_full.tgz .     # trên server nhóm
```
Rồi bấm **Destroy** instance trên Vast (Stop vẫn tính phí ổ). Kiểm tra số dư ở *Billing*.

## 6. Sau đó (server nhóm, không cần máy thuê)

```bash
tar -xzf captions_full.tgz                                       # -> grounding_data/vifood54/captions_v2/full_<model>/
C=scripts/vifood54/captions/caption_v2.py
python $C stats   --run full_Qwen3_VL_32B
python $C publish --run full_Qwen3_VL_32B                        # -> annotations_en/vlm_captions.jsonl
VIFOOD_LANG=en python scripts/vifood54/captions/review_captions.py --reviewer <tên>   # duyệt bản Việt, ghi số câu sai
VIFOOD_LANG=en python scripts/vifood54/captions/vlm_captions.py attach --suffix _lmm_v2
bash scripts/vifood54/run_b5_v2_en.sh b                          # B5b (HANDOFF T7)
```
Ưu tiên duyệt: ảnh bị gắn cờ → lớp hiếm / cặp dễ nhầm → 20% ngẫu nhiên. Commit thư mục `captions_v2/` (kết quả + bảng
chấm) để luận văn có số liệu so sánh model (tương ứng Table 7 của paper).
