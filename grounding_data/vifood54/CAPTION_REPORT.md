# ViFood-54 — báo cáo caption hình thái (Pha 2)

- Biến thể / ảnh: ['L1', 'L1', 'L2', 'L2', 'L2', 'L2']; ngân sách 160 token BERT / caption
- `train_vg_cap_rfs.jsonl`: 4164 dòng (theo train_od_rfs)

| split | ảnh | ảnh có caption | biến thể lỗi lint | caption khác nhau / ảnh (TB) | token L1 TB / p95 / max | token L2 TB / p95 / max |
|---|---|---|---|---|---|---|
| train | 3138 | 3138 | 10/18828 | 5.89 | 21 / 44 / 92 | 65 / 147 / 160 |
| val | 404 | 404 | 8/2424 | 5.89 | 21 / 41 / 91 | 64 / 137 / 160 |
| test | 414 | 414 | 0/2484 | 5.88 | 21 / 44 / 81 | 63 / 150 / 160 |

## Lỗi lint (18 biến thể bị loại)

- quá dài: 36
- `11812228013829794785784325169194132278100652o-1599030488494561610147.jpg` L2: Ba đĩa rau sống nằm ở góc trên bên trái và bên trái. Phía trên là một con cua. Ba phần ngao sò nằm rải rác trên bàn. Một đĩa gà luộc nằm ở phía trên. Ở bên phải → ['quá dài: 173 > 160 token', 'quá dài: 173 > 160 token']
- `11812228013829794785784325169194132278100652o-1599030488494561610147.jpg` L2: Ở góc trên bên trái và bên trái có ba đĩa rau sống. Một con cua nằm ở phía trên. Ba phần ngao sò nằm rải rác trên bàn. Phía trên là một phần gà luộc. Ở bên phải → ['quá dài: 173 > 160 token', 'quá dài: 173 > 160 token']
- `11812228013829794785784325169194132278100652o-1599030488494561610147.jpg` L2: Ba đĩa rau sống nằm ở góc trên bên trái và bên trái. Một con cua nằm ở phía trên. Rải rác trên bàn có ba phần ngao sò. Phía trên là một đĩa gà luộc. Bên phải là → ['quá dài: 171 > 160 token', 'quá dài: 171 > 160 token']
- `11812228013829794785784325169194132278100652o-1599030488494561610147.jpg` L2: Ở góc trên bên trái và bên trái có ba đĩa rau sống. Một con cua nằm ở phía trên. Ba phần ngao sò nằm rải rác trên bàn. Phía trên là một đĩa gà luộc. Ở bên phải  → ['quá dài: 172 > 160 token', 'quá dài: 172 > 160 token']
- `9_a59070c3d5.jpg` L2: Ba đĩa rau sống nằm rải rác trên bàn. Ở chính giữa có một phần heo quay. Ở góc trên bên trái có một đĩa gỏi cuốn. Ở chính giữa có một phần bún thịt nướng. Bên p → ['quá dài: 164 > 160 token', 'quá dài: 164 > 160 token']
- `9_a59070c3d5.jpg` L2: Rải rác trên bàn có ba đĩa rau sống. Một đĩa heo quay nằm ở chính giữa. Ở góc trên bên trái có một phần gỏi cuốn. Ở chính giữa có một phần bún thịt nướng. Bên p → ['quá dài: 165 > 160 token', 'quá dài: 165 > 160 token']
- `images.jpg` L2: Một phần rau xào nằm ở góc dưới bên trái. Phía trên là một phần gà luộc. Một đĩa nem rán nằm ở góc dưới bên phải. Một phần chả giò nằm ở chính giữa. Bên phải là → ['quá dài: 165 > 160 token', 'quá dài: 165 > 160 token']
- `images.jpg` L2: Ở góc dưới bên trái có một đĩa rau xào. Ở phía trên có một đĩa gà luộc. Ở góc dưới bên phải có một đĩa nem rán. Một phần chả giò nằm ở chính giữa. Ở bên phải có → ['quá dài: 163 > 160 token', 'quá dài: 163 > 160 token']
- `images.jpg` L2: Ở góc dưới bên trái có một đĩa rau xào. Ở phía trên có một đĩa gà luộc. Ở góc dưới bên phải có một phần nem rán. Chính giữa là một đĩa chả giò. Bên phải là một  → ['quá dài: 165 > 160 token', 'quá dài: 165 > 160 token']
- `images.jpg` L2: Ở góc dưới bên trái có một đĩa rau xào. Một đĩa gà luộc nằm ở phía trên. Góc dưới bên phải là một phần nem rán. Ở chính giữa có một phần chả giò. Một phần gỏi n → ['quá dài: 165 > 160 token', 'quá dài: 165 > 160 token']

## 30 ví dụ ngẫu nhiên (train) để duyệt tay

- `srcB_426_jpg.rf.65f528c73ba0b8f6dc0dfb5c94db39ca.jpg` [L2] Ở góc dưới bên trái và góc dưới bên phải có hai bát bún mắm, lát thịt heo trên mặt, khoanh hải sản màu trắng và cam. Góc trên bên trái là một rổ rau sống, lá xanh đậm và xanh nhạt, nhiều loại lá. Ở góc trên bên phải có một phần rau luộc, màu xanh thẫm, lá rau bóng nước.
  - lật: Ở góc dưới bên trái và góc dưới bên phải có hai bát bún mắm, lát thịt heo trên mặt, khoanh hải sản màu trắng và cam. Góc trên bên phải là một rổ rau sống, lá xanh đậm và xanh nhạt, nhiều loại lá. Ở góc trên bên trái có một phần rau luộc, màu xanh thẫm, lá rau bóng nước.
- `banh_beo_detail_00037.jpg` [L1] Ảnh gồm nhiều chén nhỏ bánh bèo và một chén đồ chấm.
  - lật: Ảnh gồm nhiều chén nhỏ bánh bèo và một chén đồ chấm.
- `bun_rieu_multi_dish_00126.jpg` [L2] Rải rác trên bàn có bốn bát bún riêu, mảng riêu màu nâu vàng nổi trên mặt. Ở bên trái và bên phải có hai rổ rau sống, lá xanh đậm và xanh nhạt. Hai chén đồ chấm nằm ở phía trên và phía dưới, nước màu nâu đỏ hoặc vàng.
  - lật: Rải rác trên bàn có bốn bát bún riêu, mảng riêu màu nâu vàng nổi trên mặt. Ở bên trái và bên phải có hai rổ rau sống, lá xanh đậm và xanh nhạt. Hai chén đồ chấm nằm ở phía trên và phía dưới, nước màu nâu đỏ hoặc vàng.
- `cach-bay-mam-com-cung-gio-le-vat-van-khan-va-goi-y-mam-com-tipsnote-800x500-4.jpg` [L2] Chính giữa là một phần gà luộc, thịt trắng ở mặt cắt. Một đĩa gỏi nằm ở bên phải, rau củ thái sợi nhiều màu. Phía dưới là một đĩa nem rán, vỏ phồng rộp, cuốn dài màu vàng nâu. Rải rác trên bàn có năm món ăn khác. Ở chính giữa có một bát canh, có thìa trong bát. Ở bên phải có một đĩa xôi, rắc hành phi vàng, đắp thành đĩa hoặc nắm. Một chén đồ chấm nhỏ nằm ở bên phải, lẫn tỏi băm.
  - lật: Chính giữa là một phần gà luộc, thịt trắng ở mặt cắt. Một đĩa gỏi nằm ở bên trái, rau củ thái sợi nhiều màu. Phía dưới là một đĩa nem rán, vỏ phồng rộp, cuốn dài màu vàng nâu. Rải rác trên bàn có năm món ăn khác. Ở chính giữa có một bát canh, có thìa trong bát. Ở bên trái có một đĩa xôi, rắc hành phi vàng, đắp thành đĩa hoặc nắm. Một chén đồ chấm nhỏ nằm ở bên trái, lẫn tỏi băm.
- `images_100.jpg` [L2] Ở bên trái có một đĩa gà quay lớn, bề mặt bóng dầu, da màu nâu đỏ bóng. Góc dưới bên phải là một phần xôi lớn, rắc hành phi vàng, đắp thành đĩa hoặc nắm. Một đĩa rau sống nằm ở góc trên bên trái, lẫn giá đỗ trắng, lá xanh đậm và xanh nhạt. Một chén đồ chấm nhỏ nằm ở chính giữa, lát ớt đỏ nổi trên mặt.
  - lật: Ở bên phải có một đĩa gà quay lớn, bề mặt bóng dầu, da màu nâu đỏ bóng. Góc dưới bên trái là một phần xôi lớn, rắc hành phi vàng, đắp thành đĩa hoặc nắm. Một đĩa rau sống nằm ở góc trên bên phải, lẫn giá đỗ trắng, lá xanh đậm và xanh nhạt. Một chén đồ chấm nhỏ nằm ở chính giữa, lát ớt đỏ nổi trên mặt.
- `srcB_373_jpg.rf.d747f637423a639d9c2ea2e859237d56.jpg` [L2] Ở chính giữa và phía dưới có hai phần bánh khọt, xếp nhiều cái sát nhau, viền vàng nâu. Phía dưới là một đĩa rau sống, xếp đầy kín, lá xanh đậm và xanh nhạt. Ở góc dưới bên trái có một bát nhỏ đồ chấm, nước màu nâu đỏ hoặc vàng, lẫn tỏi băm.
  - lật: Ở chính giữa và phía dưới có hai phần bánh khọt, xếp nhiều cái sát nhau, viền vàng nâu. Phía dưới là một đĩa rau sống, xếp đầy kín, lá xanh đậm và xanh nhạt. Ở góc dưới bên phải có một bát nhỏ đồ chấm, nước màu nâu đỏ hoặc vàng, lẫn tỏi băm.
- `srcB_79_jpg.rf.1e60d23de4ebc9967f5007b7caa8a256.jpg` [L2] Rải rác trên bàn có nhiều chiếc bánh pía, in dấu chữ màu đỏ trên mặt, bánh tròn dẹt.
  - lật: Rải rác trên bàn có nhiều chiếc bánh pía, in dấu chữ màu đỏ trên mặt, bánh tròn dẹt.
- `hu_tieu_detail_00001.jpg` [L2] Ở chính giữa có một bát hủ tiếu lớn, lá xanh trên mặt, trứng cút trắng và lát thịt. Ở bên phải có một đĩa tôm, thân cong màu cam đỏ.
  - lật: Ở chính giữa có một bát hủ tiếu lớn, lá xanh trên mặt, trứng cút trắng và lát thịt. Ở bên trái có một đĩa tôm, thân cong màu cam đỏ.
- `images_-_2026-09-30T151011.160.jpg` [L2] Rải rác trên bàn có năm tô phở, sợi bánh dẹt trắng. Ở góc dưới bên phải có một đĩa rau sống, lẫn giá đỗ trắng. Hai bát nhỏ đồ chấm nằm ở góc trên bên phải và góc dưới bên trái, nước màu nâu đỏ hoặc vàng.
  - lật: Rải rác trên bàn có năm tô phở, sợi bánh dẹt trắng. Ở góc dưới bên trái có một đĩa rau sống, lẫn giá đỗ trắng. Hai bát nhỏ đồ chấm nằm ở góc trên bên trái và góc dưới bên phải, nước màu nâu đỏ hoặc vàng.
- `com_tam_detail_00013.jpg` [L2] Một phần cơm tấm lớn nằm ở chính giữa, hạt cơm trắng nhỏ, lát trứng hấp màu vàng. Chính giữa là một phần mực, thân màu trắng hồng, khoanh tròn hoặc nguyên con. Bên trái là một đĩa rau sống, xếp đầy kín. Ở bên phải có một bát nhỏ đồ chấm, lát ớt đỏ nổi trên mặt.
  - lật: Một phần cơm tấm lớn nằm ở chính giữa, hạt cơm trắng nhỏ, lát trứng hấp màu vàng. Chính giữa là một phần mực, thân màu trắng hồng, khoanh tròn hoặc nguyên con. Bên phải là một đĩa rau sống, xếp đầy kín. Ở bên trái có một bát nhỏ đồ chấm, lát ớt đỏ nổi trên mặt.
- `banh_uc_detail_00012.jpg` [L1] Một đĩa bánh đúc và một chén đồ chấm.
  - lật: Một đĩa bánh đúc và một chén đồ chấm.
- `ga_luoc_detail_00009.jpg` [L2] Nhiều phần gà luộc nằm rải rác trên bàn, thịt trắng ở mặt cắt, da màu vàng nhạt.
  - lật: Nhiều phần gà luộc nằm rải rác trên bàn, thịt trắng ở mặt cắt, da màu vàng nhạt.
- `chao_long_multi_dish_00148.jpg` [L2] Một tô cháo lòng lớn nằm ở góc dưới bên phải, mặt cháo đặc. Bên trái là một món ăn khác. Phía trên là một đĩa rau sống, xếp đầy kín. Phía dưới là một bát nhỏ đồ chấm, lẫn tỏi băm.
  - lật: Một tô cháo lòng lớn nằm ở góc dưới bên trái, mặt cháo đặc. Bên phải là một món ăn khác. Phía trên là một đĩa rau sống, xếp đầy kín. Phía dưới là một bát nhỏ đồ chấm, lẫn tỏi băm.
- `rau_xao_detail_00005.jpg` [L1] Một phần rau xào.
  - lật: Một phần rau xào.
- `bun_rieu_detail_00053.jpg` [L2] Một món ăn khác nằm ở góc trên bên trái. Góc dưới bên trái là một tô bún bò Huế lớn, sợi to tròn màu trắng, lá xanh trên mặt. Ở bên phải có một chén đồ chấm, lát ớt đỏ nổi trên mặt, nước màu nâu đỏ hoặc vàng.
  - lật: Một món ăn khác nằm ở góc trên bên phải. Góc dưới bên phải là một tô bún bò Huế lớn, sợi to tròn màu trắng, lá xanh trên mặt. Ở bên trái có một chén đồ chấm, lát ớt đỏ nổi trên mặt, nước màu nâu đỏ hoặc vàng.
- `xoi_xeo_detail_00024.jpg` [L2] Ở chính giữa có một đĩa xôi lớn, hạt nếp màu trắng hoặc vàng, đắp thành đĩa hoặc nắm.
  - lật: Ở chính giữa có một đĩa xôi lớn, hạt nếp màu trắng hoặc vàng, đắp thành đĩa hoặc nắm.
- `goi_multi_dish_00110.jpg` [L2] Ở chính giữa có một phần gỏi lớn, sợi cà rốt và ớt đỏ, rau củ thái sợi nhiều màu.
  - lật: Ở chính giữa có một phần gỏi lớn, sợi cà rốt và ớt đỏ, rau củ thái sợi nhiều màu.
- `banh_xeo_detail_00164.jpg` [L2] Một chiếc bánh xèo lớn nằm ở chính giữa, mép bánh vàng nâu. Góc trên bên phải là một chén đồ chấm, nước màu nâu đỏ hoặc vàng.
  - lật: Một chiếc bánh xèo lớn nằm ở chính giữa, mép bánh vàng nâu. Góc trên bên trái là một chén đồ chấm, nước màu nâu đỏ hoặc vàng.
- `srcB_922_jpg.rf.22c27bfdf3403b1e9116c4fe93cd1677.jpg` [L2] Ba tô bánh canh nằm rải rác trên bàn, nước dùng sánh, rắc hành lá xanh.
  - lật: Ba tô bánh canh nằm rải rác trên bàn, nước dùng sánh, rắc hành lá xanh.
- `srcA_H-011_jpg.rf.addf69245d81cf6c2805821b93e7b756.jpg` [L1] Ảnh gồm một đĩa bún tươi, bốn phần tôm, một phần mực, một phần thịt bò, một phần cua, hai tô canh và ba phần ngao sò.
  - lật: Ảnh gồm một đĩa bún tươi, bốn phần tôm, một phần mực, một phần thịt bò, một phần cua, hai tô canh và ba phần ngao sò.
- `hu_tieu_multi_dish_00291.jpg` [L2] Một tô hủ tiếu lớn nằm ở chính giữa, sợi nhỏ trong, trứng cút trắng và lát thịt. Một rổ rau sống nằm ở góc trên bên phải, lẫn giá đỗ trắng. Ở bên trái có một đĩa tôm, xếp nhiều con trên đĩa.
  - lật: Một tô hủ tiếu lớn nằm ở chính giữa, sợi nhỏ trong, trứng cút trắng và lát thịt. Một rổ rau sống nằm ở góc trên bên trái, lẫn giá đỗ trắng. Ở bên phải có một đĩa tôm, xếp nhiều con trên đĩa.
- `srcB_288_jpg.rf.45a50ac0ed4ce4da549561c19e23b79c.jpg` [L2] Năm chiếc bánh khọt nằm rải rác trên bàn, bánh tròn nhỏ màu vàng, viền vàng nâu.
  - lật: Năm chiếc bánh khọt nằm rải rác trên bàn, bánh tròn nhỏ màu vàng, viền vàng nâu.
- `srcB_401_jpg.rf.adf6bcb902194ecd719fd7e2e2528219.jpg` [L2] Rải rác trên bàn có nhiều phần bánh khọt, xếp nhiều cái sát nhau, bánh tròn nhỏ màu vàng.
  - lật: Rải rác trên bàn có nhiều phần bánh khọt, xếp nhiều cái sát nhau, bánh tròn nhỏ màu vàng.
- `srcC_77_jpg.rf.9f64d4c98894e3240d3507a7f421e336.jpg` [L2] Bên trái là một rổ rau sống lớn, xếp đầy kín, nhiều loại lá. Ở bên phải có một tô mì Quảng lớn, ít nước dùng màu cam, trứng cút và lạc rang. Góc trên bên phải là một phần bánh tráng, nướng phủ trứng và hành trên mặt.
  - lật: Bên phải là một rổ rau sống lớn, xếp đầy kín, nhiều loại lá. Ở bên trái có một tô mì Quảng lớn, ít nước dùng màu cam, trứng cút và lạc rang. Góc trên bên trái là một phần bánh tráng, nướng phủ trứng và hành trên mặt.
- `srcB_359_jpg.rf.1ee3ef370716c0d0fe94e3fab6f7eb2e.jpg` [L2] Ở bên trái và bên phải có hai chiếc bánh khọt, bánh tròn nhỏ màu vàng, viền vàng nâu.
  - lật: Ở bên trái và bên phải có hai chiếc bánh khọt, bánh tròn nhỏ màu vàng, viền vàng nâu.
- `banh_xeo_multi_dish_00086.jpg` [L1] Ảnh gồm hai bát nhỏ đồ chấm, hai rổ rau sống, bốn chiếc bánh xèo, một đĩa bún tươi và một món ăn khác.
  - lật: Ảnh gồm hai bát nhỏ đồ chấm, hai rổ rau sống, bốn chiếc bánh xèo, một đĩa bún tươi và một món ăn khác.
- `srcA_H-106_jpg.rf.698052f8fd2636c5c8bd9e8c9413fd11.jpg` [L2] Một phần món tráng miệng nằm ở góc dưới bên phải. Bên phải là một phần mực, khoanh tròn hoặc nguyên con.
  - lật: Một phần món tráng miệng nằm ở góc dưới bên trái. Bên trái là một phần mực, khoanh tròn hoặc nguyên con.
- `mon_an_khac_multi_dish_00101.jpg` [L2] Ở phía dưới có một phần gà luộc, chặt miếng xếp trên đĩa. Một món ăn khác nằm ở phía trên. Ở bên trái có một phần rau xào, xếp trên đĩa, rau xanh bóng dầu. Một phần xôi nằm ở bên phải, hạt nếp màu trắng hoặc vàng, rắc hành phi vàng. Bên trái là một đĩa thịt bò nhỏ, lát thịt màu nâu đỏ. Một bát nhỏ đồ chấm nằm ở chính giữa, lẫn tỏi băm.
  - lật: Ở phía dưới có một phần gà luộc, chặt miếng xếp trên đĩa. Một món ăn khác nằm ở phía trên. Ở bên phải có một phần rau xào, xếp trên đĩa, rau xanh bóng dầu. Một phần xôi nằm ở bên trái, hạt nếp màu trắng hoặc vàng, rắc hành phi vàng. Bên phải là một đĩa thịt bò nhỏ, lát thịt màu nâu đỏ. Một bát nhỏ đồ chấm nằm ở chính giữa, lẫn tỏi băm.
- `bun_rieu_detail_00031.jpg` [L2] Hai tô bún bò Huế nằm ở phía trên và phía dưới, lá xanh trên mặt, nước dùng màu đỏ cam có váng dầu. Bên phải là một đĩa rau sống, xếp đầy kín, lá xanh đậm và xanh nhạt. Bên trái là một chén đồ chấm, lẫn tỏi băm.
  - lật: Hai tô bún bò Huế nằm ở phía trên và phía dưới, lá xanh trên mặt, nước dùng màu đỏ cam có váng dầu. Bên trái là một đĩa rau sống, xếp đầy kín, lá xanh đậm và xanh nhạt. Bên phải là một chén đồ chấm, lẫn tỏi băm.
- `mon_an_khac_detail_00006.jpg` [L2] Một đĩa gỏi cuốn lớn nằm ở chính giữa, lộ màu hồng cam và lá xanh bên trong, cuộn dài hình trụ. Ở góc trên bên trái và bên trái có hai chén đồ chấm, lẫn tỏi băm, nước màu nâu đỏ hoặc vàng.
  - lật: Một đĩa gỏi cuốn lớn nằm ở chính giữa, lộ màu hồng cam và lá xanh bên trong, cuộn dài hình trụ. Ở góc trên bên phải và bên phải có hai chén đồ chấm, lẫn tỏi băm, nước màu nâu đỏ hoặc vàng.
