# Thử VLM `google/gemma-4-E4B-it` sửa thuộc tính caption (6 ảnh train)
- 14 lần gọi, TB 6.1s/lần, VRAM đỉnh 14.9 GB

## `banh_beo_multi_dish_00062.jpg`

- caption hiện tại: Chính giữa là một chén nhỏ bánh bèo, mặt bột trắng phẳng. Bên trái là một chén đồ chấm nhỏ, lẫn tỏi băm.

- **bánh bèo** (6.8s) · đựng: bát · đúng món: có
  - nhìn thấy: ['lớp bột trắng mỏng', 'rắc ruốc màu cam', 'điểm mỡ hành xanh'] · bị loại: ['mặt bột trắng phẳng']
  - VLM thêm: bánh hình bán nguyệt ✅; nước dùng vàng nhạt ✅
- **đồ chấm** (5.3s) · đựng: chén · đúng món: có
  - nhìn thấy: ['nước màu nâu đỏ hoặc vàng'] · bị loại: ['lát ớt đỏ nổi trên mặt', 'lẫn tỏi băm']
  - VLM thêm: chất lỏng sánh ✅; lát trắng bên cạnh ❌ token trùng tên lớp "canh" ngoài span: 'cạnh' @31

## `srcB_646_jpg.rf.581478f1b6a076454483aefece62fc7c.jpg`

- caption hiện tại: Rải rác trên bàn có năm phần bánh khọt, xếp nhiều cái sát nhau. Hai đĩa rau sống nằm ở góc trên bên phải và chính giữa, nhiều loại lá. Phía trên là một chén đồ chấm nhỏ, nước màu nâu đỏ hoặc vàng, lẫn tỏi băm.

- **bánh khọt** (6.2s) · đựng: đĩa · đúng món: có
  - nhìn thấy: ['bánh tròn nhỏ màu vàng', 'viền vàng nâu', 'mặt bánh điểm nhân màu cam hồng', 'xếp nhiều cái sát nhau'] · bị loại: []
  - VLM thêm: rắc rau thơm xanh ❌ từ không nhìn thấy được: 'thơm' @27; có lớp vỏ chiên ✅
- **rau sống** (6.2s) · đựng: đĩa · đúng món: có
  - nhìn thấy: ['nhiều loại lá', 'lẫn giá đỗ trắng', 'xếp đầy kín', 'lá xanh đậm và xanh nhạt'] · bị loại: []
  - VLM thêm: thanh trắng mỏng ✅; sợi trắng dài ✅
- **đồ chấm** (5.6s) · đựng: chén · đúng món: có
  - nhìn thấy: ['nước màu nâu đỏ hoặc vàng'] · bị loại: ['lát ớt đỏ nổi trên mặt', 'lẫn tỏi băm']
  - VLM thêm: hạt nhỏ li ti ✅; chất lỏng sẫm màu ✅

## `banh_khot_detail_00070.jpg`

- caption hiện tại: Một đĩa rau sống nằm ở góc trên bên phải, xếp đầy kín. Rải rác trên bàn có nhiều chiếc bánh khọt, xếp nhiều cái sát nhau. Góc trên bên trái là một bát nhỏ đồ chấm, nước màu nâu đỏ hoặc vàng, lát ớt đỏ nổi trên mặt.

- **bánh khọt** (6.5s) · đựng: đĩa · đúng món: không chắc
  - nhìn thấy: ['bánh tròn nhỏ màu vàng', 'viền vàng nâu', 'mặt bánh điểm nhân màu cam hồng', 'xếp nhiều cái sát nhau'] · bị loại: []
  - VLM thêm: nhân tôm màu cam ❌ token trùng tên lớp "tôm" ngoài span: 'tôm' @24; trang trí hành lá xanh ✅
- **rau sống** (5.9s) · đựng: tô · đúng món: không
  - nhìn thấy: ['nhiều loại lá', 'xếp đầy kín', 'lá xanh đậm và xanh nhạt'] · bị loại: ['lẫn giá đỗ trắng']
  - VLM thêm: lá có gân rõ ✅; màu xanh đa dạng ✅
- **đồ chấm** (5.4s) · đựng: chén · đúng món: có
  - nhìn thấy: ['nước màu nâu đỏ hoặc vàng'] · bị loại: ['lát ớt đỏ nổi trên mặt', 'lẫn tỏi băm']
  - VLM thêm: vài mảnh nhỏ nổi ✅; nước lỏng trong ✅

## `heo_quay_detail_00008.jpg`

- caption hiện tại: Một rổ rau sống lớn nằm ở phía dưới, nhiều loại lá. Năm phần heo quay nằm rải rác trên bàn, bóng dầu, thái lát dày.

- **heo quay** (6.0s) · đựng: đĩa · đúng món: có
  - nhìn thấy: ['miếng thịt màu nâu đỏ', 'bề mặt cháy xém hoặc da vàng phồng', 'thái lát dày'] · bị loại: ['bóng dầu']
  - VLM thêm: thịt trắng bên trong ✅; rau xanh trang trí ✅
- **rau sống** (5.5s) · đựng: đĩa · đúng món: không
  - nhìn thấy: ['nhiều loại lá', 'lá xanh đậm và xanh nhạt'] · bị loại: ['lẫn giá đỗ trắng', 'xếp đầy kín']
  - VLM thêm: thịt thái lát ✅; lá xanh tươi ✅

## `srcB_209_jpg.rf.6d07cd0ae4e0488a8a6d8062d68ac3bf.jpg`

- caption hiện tại: Hai tô bún mắm nằm ở bên trái và bên phải, khoanh hải sản màu trắng và cam, lát thịt heo trên mặt. Phía trên là một đĩa rau sống, lẫn giá đỗ trắng.

- **bún mắm** (6.0s) · đựng: tô · đúng món: không chắc
  - nhìn thấy: ['nước dùng màu nâu đục', 'khoanh hải sản màu trắng và cam', 'lát thịt heo trên mặt', 'sợi nhỏ màu trắng'] · bị loại: []
  - VLM thêm: lá xanh ✅; thịt miếng ✅
- **rau sống** (6.2s) · đựng: khay · đúng món: có
  - nhìn thấy: ['nhiều loại lá', 'lẫn giá đỗ trắng', 'xếp đầy kín', 'lá xanh đậm và xanh nhạt'] · bị loại: []
  - VLM thêm: sợi màu nâu ✅; trên bề mặt ✅

## `srcB_32_jpg.rf.71931d4cfe7b31507c1d80682338aced.jpg`

- caption hiện tại: Hai tô bún bò Huế nằm ở bên trái và góc dưới bên phải, nước dùng màu đỏ cam có váng dầu, miếng thịt và khoanh giò heo. Một rổ rau sống nằm ở phía trên, lẫn giá đỗ trắng.

- **rau sống** (5.8s) · đựng: đĩa · đúng món: có
  - nhìn thấy: ['nhiều loại lá', 'lẫn giá đỗ trắng', 'lá xanh đậm và xanh nhạt'] · bị loại: ['xếp đầy kín']
  - VLM thêm: lá xanh tươi ✅; giá đỗ trắng ✅
- **bún bò Huế** (6.4s) · đựng: tô · đúng món: không chắc
  - nhìn thấy: ['nước dùng màu đỏ cam có váng dầu', 'sợi to tròn màu trắng', 'miếng thịt và khoanh giò heo', 'lá xanh trên mặt'] · bị loại: []
  - VLM thêm: miếng đậu phụ trắng ✅; thanh tre/que gỗ ✅

