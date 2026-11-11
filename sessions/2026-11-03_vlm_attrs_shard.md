# 03/11 — VLM (Gemma 4 12B) lấy thuộc tính nhìn thấy cho caption train, chia 2 nửa

Mục tiêu: caption hình thái của train khớp ảnh hơn. VLM không viết lại caption (sẽ mất span, có thể thêm món không có
box); với mỗi lớp trong ảnh, cắt box lớn nhất và hỏi thuộc tính ứng viên nào trong taxonomy thật sự nhìn thấy, thêm tối
đa 2 đặc điểm (qua lint), dụng cụ đựng, có đúng món không. Builder sau đó ghép lại caption, span vẫn chính xác.

## Khối lượng
| Tập | Ảnh | Crop (lớp có thuộc tính) | Gemma 12B 4-bit (7.4 s/crop) |
| :--- | ---: | ---: | ---: |
| train | 3138 | 6979 | ~14.3 h |
| val | 404 | 894 | ~1.8 h (chưa chạy, không cần cho huấn luyện) |

Chia 2 shard theo thứ tự filename (ảnh thứ i → shard i % 2) để mỗi nửa trải đều các nguồn ảnh:
shard 0 = 1569 ảnh / 3477 crop (~7.1 h), shard 1 = phần còn lại.

## Script
`scripts/vifood54/captions/vlm_attrs.py` (dùng lại PROMPT/crop/parse_json của `vlm_pilot.py`):
- ghi `grounding_data/vifood54/vlm_attrs/train_gemma-4-12B-it_shard{k}of2.jsonl`, một dòng/ảnh, ghi ngay sau mỗi ảnh;
- chạy lại cùng lệnh thì bỏ qua ảnh đã có (dừng giữa chừng không mất việc);
- crop lỗi được ghi `error`, không dừng cả đêm.

Chạy thử 3 ảnh (14 crop): 7.4 s/crop, JSON đọc được 14/14, VRAM ~9 GB (app 7862 vẫn chạy cùng GPU).

## Đang chạy (tối 03/11)
```bash
tmux attach -t vlm_attrs        # log: grounding_data/vifood54/vlm_attrs/log_shard0of2.txt
```
Nửa sau (đêm sau), cùng lệnh, đổi `--shard 1`:
```bash
HF_HUB_OFFLINE=1 ~/miniconda/envs/gemma_env/bin/python -u scripts/vifood54/captions/vlm_attrs.py \
    --shard 1 --num-shards 2 --model google/gemma-4-12B-it --load-4bit
```

## Việc tiếp theo
- Đọc kết quả shard 0: tỉ lệ `match = không` (có thể là nhãn sai, đưa đi soát), thuộc tính bị loại nhiều nhất.
- Builder đọc `vlm_attrs/*.jsonl`: ảnh có kết quả VLM thì dùng `visible` + `extra` thay cho thuộc tính mặc định của lớp;
  ảnh chưa có giữ caption cũ → có thể train thử B3b với nửa đầu trước khi có nửa sau.

## Kết quả shard 0 (xong sáng 04/11)
- 1569 ảnh, 3477 crop, 7.5 s/crop (7.2 h), lỗi 1 (JSON).
- `match`: có 2906 (84%), không 388 (11%), không chắc 182 (5%).
- Thuộc tính ứng viên giữ lại 65% (8654/13304); 26 crop không giữ thuộc tính nào. Đặc điểm thêm: 6597 qua lint,
  355 bị loại (chủ yếu nhắc "tôm", "rau thơm/rau sống" — trùng tên lớp).
- Thuộc tính mặc định hay sai: `rau sống · xếp đầy kín` bị loại 91% (n=517), `bánh tráng · lá bánh mỏng tròn` 99%,
  `xôi · hạt nếp dính thành khối` 96%, `cháo lòng · mặt cháo đặc` 100%, các thuộc tính cách nấu ("xào với sả và ớt",
  "xào với hành tây") >89% → caption template hiện tại khẳng định nhiều thứ không có trong ảnh.
- `match = không` theo lớp: chả giò 100%, cơm tấm 44%, bánh đúc 35%, bánh giò 34%, bánh căn 33%, bánh tét 28%.
  Soát tay 4 crop/lớp: cơm tấm 3/4 đúng là nhãn sai (cơm gà chiên, cơm gà vàng, cơm chiên tôm); chả giò, bánh căn,
  bánh tét gần như toàn VLM sai (giò lụa bị hiểu theo nghĩa "chả giò" = nem rán miền Nam; bánh tét lá cẩm/gấc; bánh căn
  có trứng cút). → `match` chỉ dùng để gợi ý soát nhãn, không tự bỏ nhãn.
- Đặc điểm thêm hay là dụng cụ/nền ("thìa kim loại", "đũa gỗ") → builder nên lọc theo danh sách từ dụng cụ/nền.

## Shard 1 (bắt đầu 08/11 ~22:05)
- Cache HF bị dọn (~05/11) → mất trọng số Gemma; tải lại `hf download google/gemma-4-12B-it` (không cần token,
  ~6.5 phút, ~87 MB/s). Ổ `/` còn ~25 GB sau khi tải.
- Chạy trong tmux `vlm_attrs1`: tải xong tự chạy lệnh shard 1 ở trên. Log tải `vlm_attrs/log_download.txt`,
  log chạy `vlm_attrs/log_shard1of2.txt` (cuối có `EXIT <code>`). 1569 ảnh / 3502 crop, dự kiến ~7.3 h.
- Ra `vlm_attrs/train_gemma-4-12B-it_shard1of2.jsonl`; script resume được nếu bị ngắt (chạy lại cùng lệnh).

## Kết quả shard 1 (xong 09/11 ~05:19, `EXIT 0`)
- 1569 ảnh, 3502 crop, 7.43 s/crop (7.2 h), lỗi 1 (JSON). Tmux `vlm_attrs1` đã tự đóng, GPU trả lại.
- `match`: có 2926 (84%), không 406 (12%), không chắc 169 (5%) — gần như y hệt shard 0.
- Thuộc tính ứng viên giữ lại 65% (8771/13395); 19 crop không giữ thuộc tính nào. Đặc điểm thêm 6595 qua lint
  (653 trong đó là dụng cụ/nền theo regex `NOT_FOOD`), 407 bị loại (vẫn chủ yếu "tôm …", "rau thơm xanh").
- `match = không` theo lớp: chả giò 100%, bánh căn 67% (shard 0: 33%), bánh giò 39%, bánh khọt 35%, bánh tét 33%,
  bánh chưng 32%, bánh bột lọc 32%, mì Quảng 30%, bún thịt nướng 30%, cơm tấm 25%.

## Gộp cả train (3138 ảnh / 6979 crop, 14.5 h GPU)
- `match`: có 84%, không 11% (794 crop), không chắc 5%. Lỗi 2 crop.
- Giữ 65% thuộc tính ứng viên (17425/26699). Thêm 13192 đặc điểm (1337 là dụng cụ/nền → lọc khi build).
- Thuộc tính template sai ổn định ở cả 2 nửa (loại ≥89%, n≥30): `bánh tráng · lá bánh mỏng tròn` 99%,
  `cháo lòng · mặt cháo đặc` 99%, `rau luộc · rau xanh đậm luộc chín` 98%, `ốc · xào với sả và ớt` 98%,
  `xôi · hạt nếp dính thành khối` 96%, `bánh tráng · bẻ thành miếng nhỏ` 93%, `bánh giò · hình chóp` 92%,
  `ngao sò · nằm trong nước dùng có sả` 91%, `thịt bò · xào với hành tây` 91%, `rau sống · xếp đầy kín` 90% (n=1040),
  `chả giò · lá chuối xanh bọc ngoài` 89%, `mực · xào với hành và ớt` 89% → nên sửa/bỏ trong taxonomy chứ không chỉ
  thay theo từng ảnh.
- `match = không` theo lớp (gộp): chả giò 100% (VLM hiểu nhầm, đã soát), bánh căn 48%, bánh giò 37%, cơm tấm 35%,
  bánh tét 30%, bánh khọt 29%, bánh đúc 28%, mì Quảng 24%, bánh chưng 24%, bún thịt nướng 22%.
  Lớp mới nổi ở shard 1 cần soát tay: bánh khọt (nghi lẫn bánh ít), mì Quảng, bánh bột lọc.
