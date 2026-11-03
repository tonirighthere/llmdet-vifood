# Thử VLM `google/gemma-4-12B-it` sửa thuộc tính caption (6 ảnh train)
- 14 lần gọi, TB 7.4s/lần, VRAM đỉnh 8.0 GB

## `banh_beo_multi_dish_00062.jpg`

- caption hiện tại: Chính giữa là một chén nhỏ bánh bèo, mặt bột trắng phẳng. Bên trái là một chén đồ chấm nhỏ, lẫn tỏi băm.

- **bánh bèo** (8.5s) · đựng: tô · đúng món: có
  - nhìn thấy: ['lớp bột trắng mỏng', 'rắc ruốc màu cam', 'điểm mỡ hành xanh', 'mặt bột trắng phẳng'] · bị loại: []
  - VLM thêm: nước chấm đỏ ✅; lót lá xanh ✅
- **đồ chấm** (7.7s) · đựng: chén · đúng món: có
  - nhìn thấy: ['nước màu nâu đỏ hoặc vàng', 'lát ớt đỏ nổi trên mặt'] · bị loại: ['lẫn tỏi băm']
  - VLM thêm: chất lỏng sệt ✅; màu đỏ sẫm ✅

## `srcB_646_jpg.rf.581478f1b6a076454483aefece62fc7c.jpg`

- caption hiện tại: Rải rác trên bàn có năm phần bánh khọt, xếp nhiều cái sát nhau. Hai đĩa rau sống nằm ở góc trên bên phải và chính giữa, nhiều loại lá. Phía trên là một chén đồ chấm nhỏ, nước màu nâu đỏ hoặc vàng, lẫn tỏi băm.

- **bánh khọt** (7.2s) · đựng: đĩa · đúng món: không
  - nhìn thấy: ['viền vàng nâu', 'xếp nhiều cái sát nhau'] · bị loại: ['bánh tròn nhỏ màu vàng', 'mặt bánh điểm nhân màu cam hồng']
  - VLM thêm: có tôm ❌ token trùng tên lớp "tôm" ngoài span: 'tôm' @22; rắc hành lá ✅
- **rau sống** (7.4s) · đựng: đĩa · đúng món: có
  - nhìn thấy: ['nhiều loại lá', 'lẫn giá đỗ trắng'] · bị loại: ['xếp đầy kín', 'lá xanh đậm và xanh nhạt']
  - VLM thêm: thái sợi dài ✅; màu trắng chủ đạo ✅
- **đồ chấm** (7.5s) · đựng: chén · đúng món: có
  - nhìn thấy: ['nước màu nâu đỏ hoặc vàng', 'lát ớt đỏ nổi trên mặt', 'lẫn tỏi băm'] · bị loại: []
  - VLM thêm: chén màu xanh ✅; nước có hạt ✅

## `banh_khot_detail_00070.jpg`

- caption hiện tại: Một đĩa rau sống nằm ở góc trên bên phải, xếp đầy kín. Rải rác trên bàn có nhiều chiếc bánh khọt, xếp nhiều cái sát nhau. Góc trên bên trái là một bát nhỏ đồ chấm, nước màu nâu đỏ hoặc vàng, lát ớt đỏ nổi trên mặt.

- **bánh khọt** (7.8s) · đựng: đĩa · đúng món: có
  - nhìn thấy: ['bánh tròn nhỏ màu vàng', 'viền vàng nâu', 'mặt bánh điểm nhân màu cam hồng', 'xếp nhiều cái sát nhau'] · bị loại: []
  - VLM thêm: tôm nguyên con ❌ token trùng tên lớp "tôm" ngoài span: 'tôm' @19; hành lá xanh ✅
- **rau sống** (7.2s) · đựng: tô · đúng món: có
  - nhìn thấy: ['nhiều loại lá', 'lá xanh đậm và xanh nhạt'] · bị loại: ['lẫn giá đỗ trắng', 'xếp đầy kín']
  - VLM thêm: có nước đọng ✅; mặt bàn đá ✅
- **đồ chấm** (7.3s) · đựng: chén · đúng món: có
  - nhìn thấy: ['nước màu nâu đỏ hoặc vàng', 'lẫn tỏi băm'] · bị loại: ['lát ớt đỏ nổi trên mặt']
  - VLM thêm: họa tiết xanh ✅; nước có váng ✅

## `heo_quay_detail_00008.jpg`

- caption hiện tại: Một rổ rau sống lớn nằm ở phía dưới, nhiều loại lá. Năm phần heo quay nằm rải rác trên bàn, bóng dầu, thái lát dày.

- **heo quay** (6.4s) · đựng: đĩa · đúng món: có
  - nhìn thấy: ['miếng thịt màu nâu đỏ', 'bề mặt cháy xém hoặc da vàng phồng', 'thái lát dày'] · bị loại: ['bóng dầu']
  - VLM thêm: thịt màu trắng ✅; lá xanh ✅
- **rau sống** (7.3s) · đựng: đĩa · đúng món: không
  - nhìn thấy: ['nhiều loại lá', 'lá xanh đậm và xanh nhạt'] · bị loại: ['lẫn giá đỗ trắng', 'xếp đầy kín']
  - VLM thêm: thịt có lớp da ✅; màu vàng cam ✅

## `srcB_209_jpg.rf.6d07cd0ae4e0488a8a6d8062d68ac3bf.jpg`

- caption hiện tại: Hai tô bún mắm nằm ở bên trái và bên phải, khoanh hải sản màu trắng và cam, lát thịt heo trên mặt. Phía trên là một đĩa rau sống, lẫn giá đỗ trắng.

- **bún mắm** (7.0s) · đựng: tô · đúng món: có
  - nhìn thấy: ['nước dùng màu nâu đục', 'khoanh hải sản màu trắng và cam', 'sợi nhỏ màu trắng'] · bị loại: ['lát thịt heo trên mặt']
  - VLM thêm: lá xanh ✅; ớt đỏ ✅
- **rau sống** (7.1s) · đựng: tô · đúng món: có
  - nhìn thấy: ['nhiều loại lá', 'lá xanh đậm và xanh nhạt'] · bị loại: ['lẫn giá đỗ trắng', 'xếp đầy kín']
  - VLM thêm: sợi màu nâu ✅; màu xanh lá ✅

## `srcB_32_jpg.rf.71931d4cfe7b31507c1d80682338aced.jpg`

- caption hiện tại: Hai tô bún bò Huế nằm ở bên trái và góc dưới bên phải, nước dùng màu đỏ cam có váng dầu, miếng thịt và khoanh giò heo. Một rổ rau sống nằm ở phía trên, lẫn giá đỗ trắng.

- **rau sống** (7.2s) · đựng: tô · đúng món: có
  - nhìn thấy: ['nhiều loại lá', 'lẫn giá đỗ trắng', 'lá xanh đậm và xanh nhạt'] · bị loại: ['xếp đầy kín']
  - VLM thêm: có nước dùng ✅; có thịt ✅
- **bún bò Huế** (7.5s) · đựng: tô · đúng món: có
  - nhìn thấy: ['nước dùng màu đỏ cam có váng dầu', 'sợi to tròn màu trắng', 'miếng thịt và khoanh giò heo'] · bị loại: ['lá xanh trên mặt']
  - VLM thêm: đũa gỗ ✅; hành lá xanh ✅

