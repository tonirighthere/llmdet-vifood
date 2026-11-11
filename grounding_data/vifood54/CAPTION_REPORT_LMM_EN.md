# ViFood-54 — báo cáo caption hình thái TIẾNG ANH

- Biến thể / ảnh: ['L1', 'L1', 'L2', 'L2', 'L2', 'L2']; ngân sách 160 token BERT / caption
- `train_vg_cap_rfs.jsonl`: 4164 dòng (theo train_od_rfs)
- Thuộc tính VLM (train): 6977 lượt lớp-ảnh; giữ 17425/26699 thuộc tính taxonomy, thêm 11534 đặc điểm VLM (bản dịch có 3052 cụm), 1 lượt không còn thuộc tính, 2 lượt VLM lỗi (dùng taxonomy); lượng từ theo dụng cụ VLM thấy: 6250 lượt
- Cụm bị lint loại trước khi ghép: 223 ('red dipping sauce', 'orange-colored dipping sauce', 'brown-colored dipping sauce', 'sweet basil leaves', 'dipping sauce', 'red-colored dipping sauce', 'dipping sauce with chili', 'brown dipping sauce')

| split | ảnh | ảnh có caption | biến thể lỗi lint | caption khác nhau / ảnh (TB) | token L1 TB / p95 / max | token L2 TB / p95 / max |
|---|---|---|---|---|---|---|
| train | 3138 | 3138 | 0/18828 | 5.80 | 20 / 41 / 85 | 49 / 109 / 160 |
| val | 404 | 404 | 0/2424 | 5.87 | 20 / 39 / 89 | 52 / 113 / 160 |
| test | 414 | 414 | 0/2484 | 5.84 | 19 / 40 / 77 | 51 / 118 / 160 |

## Lỗi lint (0 biến thể bị loại)

- không có

## 30 ví dụ ngẫu nhiên (train) để duyệt tay

- `srcB_426_jpg.rf.65f528c73ba0b8f6dc0dfb5c94db39ca.jpg` [L2] Two bowls of fermented fish noodle soup are in the bottom left corner and in the bottom right corner, sprinkled green vegetables, thin white noodles. In the top left corner is a plate of fresh herbs and greens, dark and light green leaves. In the top right corner is a plate of boiled vegetables, long fiber shape, glossy wet leaves.
  - lật: Two bowls of fermented fish noodle soup are in the bottom left corner and in the bottom right corner, sprinkled green vegetables, thin white noodles. In the top right corner is a plate of fresh herbs and greens, dark and light green leaves. In the top left corner is a plate of boiled vegetables, long fiber shape, glossy wet leaves.
- `banh_beo_detail_00037.jpg` [L1] The image shows several small bowls of steamed rice cakes and a small bowl of dipping sauce.
  - lật: The image shows several small bowls of steamed rice cakes and a small bowl of dipping sauce.
- `bun_rieu_multi_dish_00126.jpg` [L2] Across the table there are four bowls of crab noodle soup, golden fried tofu pieces, yellow-brown crab paste floating on top. On the left and on the right there are two baskets of fresh herbs and greens, many kinds of leaves, leaves with veins. At the top and at the bottom there are two small bowls of dipping sauce, reddish-brown or yellow liquid, opaque water.
  - lật: Across the table there are four bowls of crab noodle soup, golden fried tofu pieces, yellow-brown crab paste floating on top. On the left and on the right there are two baskets of fresh herbs and greens, many kinds of leaves, leaves with veins. At the top and at the bottom there are two small bowls of dipping sauce, reddish-brown or yellow liquid, opaque water.
- `cach-bay-mam-com-cung-gio-le-vat-van-khan-va-goi-y-mam-com-tipsnote-800x500-4.jpg` [L2] A plate of boiled chicken is in the center, glossy skin layer, white meat at the cut faces. On the right is a plate of shredded salad, mixed with green leaves, round arrangement. A plate of fried spring rolls is at the bottom, cut into pieces. Across the table there are five servings of other dish. In the center there is a bowl of clear vegetable soup, white round balls. A plate of sticky rice is on the right, white or yellow glutinous rice grains. On the right there is a small bowl of dipping sauce, red chili slices floating on top.
  - lật: A plate of boiled chicken is in the center, glossy skin layer, white meat at the cut faces. On the left is a plate of shredded salad, mixed with green leaves, round arrangement. A plate of fried spring rolls is at the bottom, cut into pieces. Across the table there are five servings of other dish. In the center there is a bowl of clear vegetable soup, white round balls. A plate of sticky rice is on the left, white or yellow glutinous rice grains. On the left there is a small bowl of dipping sauce, red chili slices floating on top.
- `images_100.jpg` [L2] On the left there is a large tray of roasted chicken, oily shiny surface, many green vegetables. A large tray of sticky rice is in the bottom right corner, fibrous coating. A basket of fresh herbs and greens is in the top left corner, dark and light green leaves, many kinds of leaves. A small bowl of dipping sauce is in the center, red chili slices floating on top, reddish-brown or yellow liquid.
  - lật: On the right there is a large tray of roasted chicken, oily shiny surface, many green vegetables. A large tray of sticky rice is in the bottom left corner, fibrous coating. A basket of fresh herbs and greens is in the top right corner, dark and light green leaves, many kinds of leaves. A small bowl of dipping sauce is in the center, red chili slices floating on top, reddish-brown or yellow liquid.
- `srcB_373_jpg.rf.d747f637423a639d9c2ea2e859237d56.jpg` [L2] In the center and at the bottom there are two servings of mini crispy pancakes, flat round shape, vibrant yellow. At the bottom is a basket of fresh herbs and greens, leaves with veins. In the bottom left corner there is a bowl of dipping sauce, small seeds, reddish-brown or yellow liquid.
  - lật: In the center and at the bottom there are two servings of mini crispy pancakes, flat round shape, vibrant yellow. At the bottom is a basket of fresh herbs and greens, leaves with veins. In the bottom right corner there is a bowl of dipping sauce, small seeds, reddish-brown or yellow liquid.
- `srcB_79_jpg.rf.1e60d23de4ebc9967f5007b7caa8a256.jpg` [L2] Across the table there are several pieces of pia pastry, round shape.
  - lật: Across the table there are several pieces of pia pastry, round shape.
- `hu_tieu_detail_00001.jpg` [L2] In the center is a large bowl of hu tieu noodles, green leaves on top, white quail eggs and meat slices. On the right there is a serving of shrimp, clear broth.
  - lật: In the center is a large bowl of hu tieu noodles, green leaves on top, white quail eggs and meat slices. On the left there is a serving of shrimp, clear broth.
- `images_-_2026-09-30T151011.160.jpg` [L2] Across the table there are five bowls of pho noodle soup, meat with fat. In the bottom right corner there is a bowl of fresh herbs and greens, mixed with white bean sprouts. In the top right corner and in the bottom left corner there are two small bowls of dipping sauce, round shape.
  - lật: Across the table there are five bowls of pho noodle soup, meat with fat. In the bottom left corner there is a bowl of fresh herbs and greens, mixed with white bean sprouts. In the top left corner and in the bottom right corner there are two small bowls of dipping sauce, round shape.
- `com_tam_detail_00013.jpg` [L2] In the center is a large plate of broken rice, two spoons, small white rice grains. In the center is a plate of squid, long curled tentacles, cooked with onions. On the left is a plate of fresh herbs and greens, cucumber slices. A small bowl of dipping sauce is on the right, reddish-brown or yellow liquid.
  - lật: In the center is a large plate of broken rice, two spoons, small white rice grains. In the center is a plate of squid, long curled tentacles, cooked with onions. On the right is a plate of fresh herbs and greens, cucumber slices. A small bowl of dipping sauce is on the left, reddish-brown or yellow liquid.
- `banh_uc_detail_00012.jpg` [L1] The image shows a bowl of dipping sauce and a plate of steamed savory cake.
  - lật: The image shows a bowl of dipping sauce and a plate of steamed savory cake.
- `ga_luoc_detail_00009.jpg` [L2] Across the table there are several servings of boiled chicken, shiny skin.
  - lật: Across the table there are several servings of boiled chicken, shiny skin.
- `chao_long_multi_dish_00148.jpg` [L2] A large bowl of pork offal congee is in the bottom right corner, sprinkled with scallions and pepper. On the left is a serving of other dish. At the top there is a basket of fresh herbs and greens, many kinds of leaves. A small bowl of dipping sauce is at the bottom, reddish-brown or yellow liquid, viscous liquid.
  - lật: A large bowl of pork offal congee is in the bottom left corner, sprinkled with scallions and pepper. On the right is a serving of other dish. At the top there is a basket of fresh herbs and greens, many kinds of leaves. A small bowl of dipping sauce is at the bottom, reddish-brown or yellow liquid, viscous liquid.
- `rau_xao_detail_00005.jpg` [L1] The meal includes a plate of stir-fried vegetables.
  - lật: The meal includes a plate of stir-fried vegetables.
- `bun_rieu_detail_00053.jpg` [L2] A serving of other dish is in the top left corner. A large bowl of hue beef noodle soup is in the bottom left corner, orange-red broth with an oily film, green leaves on top. On the right there is a small bowl of dipping sauce, reddish-brown or yellow liquid, small air bubbles.
  - lật: A serving of other dish is in the top right corner. A large bowl of hue beef noodle soup is in the bottom right corner, orange-red broth with an oily film, green leaves on top. On the left there is a small bowl of dipping sauce, reddish-brown or yellow liquid, small air bubbles.
- `xoi_xeo_detail_00024.jpg` [L2] A large serving of sticky rice is in the center, sprinkled with golden fried shallots.
  - lật: A large serving of sticky rice is in the center, sprinkled with golden fried shallots.
- `goi_multi_dish_00110.jpg` [L2] In the center there is a large plate of shredded salad, patterned fabric, shredded carrot and red chili.
  - lật: In the center there is a large plate of shredded salad, patterned fabric, shredded carrot and red chili.
- `banh_xeo_detail_00164.jpg` [L2] In the center is a large tray of sizzling crepe, thin turmeric-yellow pancake. In the top right corner there is a bowl of dipping sauce, red chili slices floating on top, reddish-brown or yellow liquid.
  - lật: In the center is a large tray of sizzling crepe, thin turmeric-yellow pancake. In the top left corner there is a bowl of dipping sauce, red chili slices floating on top, reddish-brown or yellow liquid.
- `srcB_922_jpg.rf.22c27bfdf3403b1e9116c4fe93cd1677.jpg` [L2] Three bowls of thick noodle soup are scattered across the table, thick round opaque white noodles.
  - lật: Three bowls of thick noodle soup are scattered across the table, thick round opaque white noodles.
- `srcA_H-011_jpg.rf.addf69245d81cf6c2805821b93e7b756.jpg` [L1] A plate of rice vermicelli, a plate of sliced beef, four servings of shrimp, a plate of squid, three servings of clams and scallops, a serving of whole crab and two bowls of clear vegetable soup.
  - lật: A plate of rice vermicelli, a plate of sliced beef, four servings of shrimp, a plate of squid, three servings of clams and scallops, a serving of whole crab and two bowls of clear vegetable soup.
- `hu_tieu_multi_dish_00291.jpg` [L2] In the center is a large bowl of hu tieu noodles, thin translucent noodles, red chili. In the top right corner is a plate of fresh herbs and greens, white bean sprouts, mixed with white bean sprouts. On the left there is a plate of shrimp, long white strands.
  - lật: In the center is a large bowl of hu tieu noodles, thin translucent noodles, red chili. In the top left corner is a plate of fresh herbs and greens, white bean sprouts, mixed with white bean sprouts. On the right there is a plate of shrimp, long white strands.
- `srcB_288_jpg.rf.45a50ac0ed4ce4da549561c19e23b79c.jpg` [L2] Five servings of mini crispy pancakes are scattered across the table, golden-brown edges.
  - lật: Five servings of mini crispy pancakes are scattered across the table, golden-brown edges.
- `srcB_401_jpg.rf.adf6bcb902194ecd719fd7e2e2528219.jpg` [L2] Across the table there are several servings of mini crispy pancakes, has small green dots, golden-brown edges.
  - lật: Across the table there are several servings of mini crispy pancakes, has small green dots, golden-brown edges.
- `srcC_77_jpg.rf.9f64d4c98894e3240d3507a7f421e336.jpg` [L2] A large plate of fresh herbs and greens is on the left, densely piled, red text. A large bowl of quang noodles is on the right, scallions. In the top right corner is a plate of rice paper, grilled with egg and scallions on top.
  - lật: A large plate of fresh herbs and greens is on the right, densely piled, red text. A large bowl of quang noodles is on the left, scallions. In the top left corner is a plate of rice paper, grilled with egg and scallions on top.
- `srcB_359_jpg.rf.1ee3ef370716c0d0fe94e3fab6f7eb2e.jpg` [L2] Two servings of mini crispy pancakes are on the left and on the right, golden-brown edges.
  - lật: Two servings of mini crispy pancakes are on the left and on the right, golden-brown edges.
- `banh_xeo_multi_dish_00086.jpg` [L1] The image shows two baskets of fresh herbs and greens, a serving of other dish, a plate of rice vermicelli, two small bowls of dipping sauce and four servings of sizzling crepe.
  - lật: The image shows two baskets of fresh herbs and greens, a serving of other dish, a plate of rice vermicelli, two small bowls of dipping sauce and four servings of sizzling crepe.
- `srcA_H-106_jpg.rf.698052f8fd2636c5c8bd9e8c9413fd11.jpg` [L2] A serving of dessert is in the bottom right corner. On the right is a plate of squid, twisted shape.
  - lật: A serving of dessert is in the bottom left corner. On the left is a plate of squid, twisted shape.
- `mon_an_khac_multi_dish_00101.jpg` [L2] At the bottom is a plate of boiled chicken, white meat at the cut faces. At the top there is a serving of other dish. A plate of stir-fried vegetables is on the left, orange carrots, arranged on a plate. On the right is a serving of sticky rice, white or yellow glutinous rice grains. On the left is a small plate of sliced beef, thinly sliced, white fat marbling. In the center there is a small bowl of dipping sauce, sprinkle green onions.
  - lật: At the bottom is a plate of boiled chicken, white meat at the cut faces. At the top there is a serving of other dish. A plate of stir-fried vegetables is on the right, orange carrots, arranged on a plate. On the left is a serving of sticky rice, white or yellow glutinous rice grains. On the right is a small plate of sliced beef, thinly sliced, white fat marbling. In the center there is a small bowl of dipping sauce, sprinkle green onions.
- `bun_rieu_detail_00031.jpg` [L2] Two bowls of hue beef noodle soup are at the top and at the bottom, red tubers. A bowl of fresh herbs and greens is on the right, long brown strip. On the left is a bowl of dipping sauce, white seeds.
  - lật: Two bowls of hue beef noodle soup are at the top and at the bottom, red tubers. A bowl of fresh herbs and greens is on the left, long brown strip. On the right is a bowl of dipping sauce, white seeds.
- `mon_an_khac_detail_00006.jpg` [L2] In the center is a large plate of fresh spring rolls, long cylindrical rolls, pink-orange and green fillings showing inside. In the top left corner and on the left there are two small bowls of dipping sauce, reddish-brown or yellow liquid, brown orange.
  - lật: In the center is a large plate of fresh spring rolls, long cylindrical rolls, pink-orange and green fillings showing inside. In the top right corner and on the right there are two small bowls of dipping sauce, reddish-brown or yellow liquid, brown orange.
