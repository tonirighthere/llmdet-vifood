# So sánh caption v2 giữa các model (50 ảnh chung)

| Run | Model mô tả + kiểm chứng | Số từ TB | Chi tiết nêu / qua kiểm chứng | Tỉ lệ bị loại | Chi tiết qua kiểm chứng / ảnh | Ảnh bị gắn cờ |
|---|---|---|---|---|---|---|
| pilot_Qwen3_VL_8B | Qwen/Qwen3-VL-8B-Instruct + google/gemma-4-12B-it | 130 | 1611 / 1409 | 13% | 28.2 | 13 |
| pilot_Qwen2.5_VL_72B | Qwen/Qwen2.5-VL-72B-Instruct-AWQ + google/gemma-4-12B-it | 131 | 1597 / 1247 | 22% | 24.9 | 12 |
| pilot_Qwen3_VL_32B | Qwen/Qwen3-VL-32B-Instruct + google/gemma-4-12B-it | 133 | 2105 / 1895 | 10% | 37.9 | 14 |

Người chấm: đọc bản tiếng Việt (bản Anh để đối chiếu), điền `compare_scores.csv`: số câu SAI so với ảnh, số chi tiết CHUNG CHUNG (vd "green leaves" thay vì gọi đúng loại rau), điểm tổng 1–5. Thứ tự các run trong từng ảnh được giữ cố định; nên chấm mà không nhìn tên run.

## `srcA_H-000_jpg.rf.9b3c0354b6ea79e39d868d5d71f49079.jpg`

Món (nhãn): cylindrical rice cake, dipping sauce, fresh herbs and greens, fried spring rolls, rice vermicelli, steamed rice cakes

**[A]** (139 từ, 38/45 chi tiết)

> Ở phía trên có một giỏ rau sống. Nó cho thấy khăn trải bàn màu đỏ, lá xanh và lá xanh. Nó được đặt trên bề mặt màu đỏ. Ở giữa và ở phía dưới có ba bát nhỏ bánh bèo. Chúng cho thấy bánh gạo trắng, hành lá xanh và ruốc màu cam. Chúng được phủ hành lá xanh lên trên. Ở giữa có một đĩa nem rán. Nó cho thấy các cuộn màu nâu vàng, khăn trải bàn màu đỏ và các cuộn dài. Nó được sắp xếp trên một chiếc đĩa. Ở bên trái và bên phải có hai phần bún tươi. Chúng cho thấy mì trắng, vành màu xanh và khăn trải bàn màu đỏ. Ở bên phải có một đĩa bánh tét. Nó cho thấy vành màu xanh trên đĩa, bề mặt đĩa màu trắng và các món đồ gói màu xanh. Nó được đặt trên đĩa với các que.

<sub>EN: At the top there is a basket of fresh herbs and greens. It shows red tablecloth, green leaves and green leaves. It is placed on red surface. In the center and at the bottom there are three small bowls of steamed rice cakes. They show white rice cakes, green scallions and orange floss. They are topped with green scallions. In the center there is a plate of fried spring rolls. It shows golden-brown rolls, red tablecloth and long rolls. It is arranged on a plate. On the left and on the right there are two servings of rice vermicelli. They show white noodles, blue rim and red tablecloth. On the right there is a plate of cylindrical rice cake. It shows blue rim on plate, white plate surface and green wrapped items. It is placed on plate with sticks.</sub>

**[B]** (138 từ, 26/41 chi tiết)

> Ở phía trên có một đĩa rau sống. Nó cho thấy rau lá xanh và rau lá xanh. Nó được đặt trên bề mặt màu đỏ. Ở giữa và ở phía dưới có ba bát nhỏ bánh bèo. Chúng cho thấy bánh mỏng màu trắng, lớp phủ màu cam và đồ trang trí màu xanh. Chúng được đặt trên bàn. Ở giữa có một đĩa nem rán. Nó cho thấy các cuộn màu nâu vàng. Ở bên trái và bên phải có hai phần bún tươi. Chúng cho thấy bún trắng, đồ trang trí màu xanh và bún trắng. Chúng được đặt trên đĩa. Ở bên phải có một phần bánh tét. Nó cho thấy lá chuối xanh và gói lá chuối. Băng qua bàn có ba bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ.

<sub>EN: At the top there is a plate of fresh herbs and greens. It shows green leafy vegetables and green leafy vegetables. It is placed on red surface. In the center and at the bottom there are three small bowls of steamed rice cakes. They show white thin cakes, orange topping and green garnish. They are placed on table. In the center there is a plate of fried spring rolls. It shows golden brown rolls. On the left and on the right there are two servings of rice vermicelli. They show white rice noodles, green garnish and white noodles. They are placed on plate. On the right there is a serving of cylindrical rice cake. It shows green banana leaves and banana leaf wrapping. Across the table there are three small bowls of dipping sauce. They show reddish-brown liquid.</sub>

**[C]** (137 từ, 47/55 chi tiết)

> Ở phía trên có một giỏ rau sống. Nó cho thấy lá xanh, khăn trải bàn đỏ và rau xanh. Ở giữa và ở dưới cùng có ba bát nhỏ bánh bèo. Chúng cho thấy lớp phủ màu nâu vàng, thảo mộc xanh và bánh gạo hình tam giác. Chúng được sắp xếp chồng lên nhau. Ở giữa có một đĩa nem rán. Nó cho thấy các cuộn màu nâu vàng, vành đĩa đa sắc và các cuộn chiên dài. Nó được sắp xếp thành một hàng. Ở bên trái và bên phải có hai phần bún tươi. Chúng cho thấy mì trắng, thảo mộc xanh và nước sốt nâu đậm. Ở bên phải có một đĩa bánh tét. Nó cho thấy lá chuối xanh, sợi trắng và đĩa xanh trắng. Nó được sắp xếp theo hình tròn.

<sub>EN: At the top there is a basket of fresh herbs and greens. It shows green leaves, red tablecloth and green leafy vegetables. In the center and at the bottom there are three small bowls of steamed rice cakes. They show golden brown topping, green herbs and triangular rice cakes. They are arranged in overlapping pieces. In the center there is a plate of fried spring rolls. It shows golden-brown rolls, multicolored plate rim and long fried rolls. It is arranged in a row. On the left and on the right there are two servings of rice vermicelli. They show white noodles, green herbs and dark brown sauce. On the right there is a plate of cylindrical rice cake. It shows green banana leaves, white strings and blue and white plate. It is arranged in a circular pattern.</sub>

## `srcA_H-001_jpg.rf.ea49db583598a718178ea42e637ab5ac.jpg`

Món (nhãn): other dish, shredded salad, squid

**[A]** (100 từ, 17/23 chi tiết)

> Phía bên kia bàn có năm phần món ăn khác. Phía bên kia bàn có ba phần gỏi. Chúng cho thấy rau xanh, đĩa trắng, ớt đỏ, ớt đỏ và rau xanh. Chúng được sắp xếp theo hình xoắn ốc. Ở góc dưới bên phải có một đĩa mực. Nó cho thấy đĩa trắng, sốt đỏ, đồ trang trí xanh, ớt đỏ thái nhỏ và bắp cải bào. Nó được trang trí với rau mùi tây. Các món ăn khác nằm ở bên trái của các gỏi. Các gỏi nằm phía trên các mực. Cũng có thể thấy: thìa gỗ, miếng chanh và máy xay tiêu.

<sub>EN: Across the table there are five servings of other dish. Across the table there are three servings of shredded salad. They show green leafy vegetables, white plate, red chili peppers, red chili peppers and green leafy vegetables. They are arranged in spiral pattern. In the bottom right corner there is a plate of squid. It shows white plate, red sauce, green garnish, chopped red peppers and shredded cabbage. It is garnished with parsley. The other dish are to the left of the shredded salad. The shredded salad are above the squid. Also visible: wooden spoon, lime wedge and pepper grinder.</sub>

**[B]** (115 từ, 16/20 chi tiết)

> Phía bên kia bàn có năm phần món ăn khác. Phía bên kia bàn có ba phần gỏi. Chúng cho thấy rau xanh, các hình xoắn ốc màu trắng, các lát xoắn ốc màu trắng, rau xanh và các lát ớt đỏ. Chúng được sắp xếp theo hình tròn. Ở góc dưới bên phải có một đĩa mực. Nó cho thấy nền sốt đỏ, trang trí bằng rau mùi xanh, ớt chuông đỏ, rau mùi xanh và bắp cải bào. Nó được đặt trên giường. Các món ăn khác nằm ở bên trái của các gỏi. Các gỏi nằm phía trên mực. Các món ăn được đặt trên một chiếc bàn gỗ sáng màu. Cũng có thể thấy: bát trắng nhỏ, lát chanh xanh và quả ớt đỏ.

<sub>EN: Across the table there are five servings of other dish. Across the table there are three servings of shredded salad. They show green leafy vegetables, white spiral shapes, sliced white spirals, green leafy vegetables and red chili slices. They are arranged in circular pattern. In the bottom right corner there is a plate of squid. It shows red sauce base, green parsley garnish, red bell peppers, green parsley and shredded cabbage. It is placed on bed. The other dish are to the left of the shredded salad. The shredded salad are above the squid. The dishes are set on a light wooden table. Also visible: small white bowl, green lime wedge and red chili pepper.</sub>

**[C]** (121 từ, 19/23 chi tiết)

> Phía bên kia bàn có năm phần món ăn khác. Phía bên kia bàn có ba phần gỏi. Chúng cho thấy các lát cuộn màu nâu nhạt, phần lá xanh, dải ớt đỏ, các lát cuộn thịt hoặc nội tạng và rau xanh. Chúng được sắp xếp theo hình tròn. Ở góc dưới bên phải có một đĩa mực. Nó cho thấy các miếng cà chua đỏ, đồ trang trí lá xanh, các miếng cà chua đỏ, đồ trang trí lá xanh và phần phủ màu vàng bào sợi. Nó được xếp thành một đống trên đĩa. Các món ăn khác nằm ở bên trái của các gỏi. Các gỏi nằm phía trên mực. Cũng có thể nhìn thấy: thìa gỗ, bát trắng nhỏ, đĩa hoa văn xanh trắng, miếng chanh và chai gốm màu nâu.

<sub>EN: Across the table there are five servings of other dish. Across the table there are three servings of shredded salad. They show light brown rolled slices, green leafy top, red chili strips, rolled slices of meat or offal and green leafy vegetables. They are arranged in circular pattern. In the bottom right corner there is a plate of squid. It shows red tomato pieces, green leafy garnish, red tomato pieces, green leafy garnish and shredded yellow topping. It is arranged in a pile on plate. The other dish are to the left of the shredded salad. The shredded salad are above the squid. Also visible: wooden spoon, small white bowls, blue and white patterned plate, lime wedge and brown ceramic bottle.</sub>

## `srcA_H-002_jpg.rf.631ea2c0aadeaba32633fa07445d6ec4.jpg`

Món (nhãn): dipping sauce, fresh herbs and greens, fried fish, pork offal congee

**[A]** (140 từ, 26/28 chi tiết)

> Ở giữa có một bát lớn cháo lòng. Nó cho thấy bát màu be nhạt, thảo mộc xanh và nước dùng trắng. Nó được phủ lên trên bằng thảo mộc xanh. Ở góc trên bên phải có một bát nhỏ cá chiên. Nó cho thấy nước dùng màu nâu nhạt, phần lá xanh và phần lá xanh. Ở góc trên bên trái có một bát rau sống. Nó cho thấy lá xanh, ớt đỏ và bàn màu nâu. Ở bên trái có một bát nhỏ đồ chấm. Nó cho thấy bát viền xanh, chất lỏng màu đỏ và các miếng trắng băm nhỏ. cháo lòng nằm bên dưới cá chiên. cá chiên nằm ở bên phải của rau sống. Các món ăn được đặt trên một chiếc bàn gỗ tối màu. Cũng có thể thấy: bát xanh trắng, chiếu tre và vải xanh.

<sub>EN: In the center there is a large bowl of pork offal congee. It shows light beige bowl, green herbs and white broth. It is topped with green herbs. In the top right corner there is a small bowl of fried fish. It shows light brown broth, green leafy tops and green leafy tops. In the top left corner there is a bowl of fresh herbs and greens. It shows green leaves, red chilies and brown table. On the left there is a small bowl of dipping sauce. It shows blue rimmed bowl, reddish liquid and minced white pieces. The pork offal congee is below the fried fish. The fried fish is to the right of the fresh herbs and greens. The dishes are set on a dark wooden table. Also visible: blue and white bowl, bamboo mat and blue cloth.</sub>

**[B]** (136 từ, 23/27 chi tiết)

> Ở giữa có một bát lớn cháo lòng. Nó cho thấy lớp nền kem màu trắng, đồ trang trí lá xanh và những miếng tròn nhỏ. Nó được trang trí với thảo mộc tươi. Ở góc trên bên phải có một bát nhỏ cá chiên. Nó cho thấy đồ trang trí lá xanh, lát thịt màu nâu và rau xanh. Nó được đặt cạnh thịt. Ở góc trên bên trái có một bát rau sống. Nó cho thấy rau xanh, ớt đỏ và rau xanh. Ở bên trái có một bát nhỏ đồ chấm. Nó cho thấy chất lỏng màu nâu đỏ, vành bát màu trắng và những miếng tỏi băm. Nó được đặt trong bát nhỏ. cháo lòng ở dưới cá chiên. cá chiên ở bên phải của rau sống.

<sub>EN: In the center there is a large bowl of pork offal congee. It shows white creamy base, green leafy garnish and small round pieces. It is garnished with fresh herbs. In the top right corner there is a small bowl of fried fish. It shows green leafy garnish, brown meat slice and leafy greens. It is placed beside meat. In the top left corner there is a bowl of fresh herbs and greens. It shows green leafy vegetables, red chili peppers and green leafy vegetables. On the left there is a small bowl of dipping sauce. It shows reddish brown liquid, white bowl rim and minced garlic pieces. It is placed in small bowl. The pork offal congee is below the fried fish. The fried fish is to the right of the fresh herbs and greens.</sub>

**[C]** (130 từ, 33/40 chi tiết)

> Ở giữa có một bát lớn cháo lòng. Nó cho thấy cháo màu nâu xám, thảo mộc xanh và các miếng nội tạng trắng. Nó được phủ lên trên bằng thảo mộc và nội tạng. Ở góc trên bên phải có một bát cá chiên. Nó cho thấy da cá màu nâu nhạt, thảo mộc xanh và xương cá. Nó được sắp xếp trong bát với thảo mộc. Ở góc trên bên trái có một bát rau sống. Nó cho thấy các loại thảo mộc lá xanh, ớt đỏ và các loại thảo mộc lá xanh. Nó được sắp xếp trong một chiếc bát. Ở bên trái có một bát nhỏ đồ chấm. Nó cho thấy chất lỏng màu nâu đỏ, vành bát màu xanh và trắng và các đốm trắng trong chất lỏng. Nó được rải trong chất lỏng. cháo lòng nằm bên dưới cá chiên.

<sub>EN: In the center there is a large bowl of pork offal congee. It shows gray-brown porridge, green herbs and white offal pieces. It is topped with herbs and offal. In the top right corner there is a bowl of fried fish. It shows light brown fish skin, green herbs and fish bones. It is arranged in bowl with herbs. In the top left corner there is a bowl of fresh herbs and greens. It shows green leafy herbs, red chili peppers and green leafy herbs. It is arranged in a bowl. On the left there is a small bowl of dipping sauce. It shows reddish-brown liquid, blue and white bowl rim and white specks in liquid. It is scattered in liquid. The pork offal congee is below the fried fish.</sub>

## `srcA_H-004_jpg.rf.e18f567c3afed2cb3f17491dac4ab805.jpg`

Món (nhãn): other dish, sliced beef, squid, stir-fried vegetables

**[A]** (133 từ, 20/25 chi tiết)

> Ở góc dưới bên phải có một đĩa thịt bò. Nó cho thấy các loại rau xanh, thịt thái lát màu nâu đỏ và rau xanh. Nó được xào với rau. Ở phía dưới có một đĩa mực. Nó cho thấy các miếng dứa vàng, rau xanh và các miếng ớt chuông đỏ. Chúng được trộn lẫn với nhau trong bát. Ở góc trên bên trái và ở phía trên có hai phần món ăn khác. Ở góc trên bên phải và ở góc dưới bên trái có hai phần rau xào. Chúng cho thấy vành bát màu nâu nhạt, nấm thái lát và hành lá thái lát. Chúng được trộn lẫn với nhau trong bát. thịt bò nằm ở bên phải của mực. mực nằm bên dưới món ăn khác. Phông nền cho thấy một chiếc chiếu đan màu trắng.

<sub>EN: In the bottom right corner there is a plate of sliced beef. It shows green leafy vegetables, reddish-brown meat slices and green leafy vegetables. It is stir-fried with vegetables. At the bottom there is a plate of squid. It shows yellow pineapple chunks, green leafy vegetables and red bell pepper pieces. It is mixed together in bowl. In the top left corner and at the top there are two servings of other dish. In the top right corner and in the bottom left corner there are two servings of stir-fried vegetables. They show light brown bowl rim, sliced mushrooms and sliced green onions. They are mixed together in bowl. The sliced beef is to the right of the squid. The squid is below the other dish. The background shows a white woven mat.</sub>

**[B]** (128 từ, 20/23 chi tiết)

> Ở góc dưới bên phải có một đĩa thịt bò. Nó cho thấy những lát thịt màu nâu đỏ, rau xanh và rau xanh. Nó được rắc lên trên. Ở phía dưới có một đĩa mực. Nó cho thấy rau xanh, những miếng dứa vàng và những miếng dứa. Chúng được trộn lẫn với nhau một cách ngẫu nhiên. Ở góc trên bên trái và ở phía trên có hai phần món ăn khác. Ở góc trên bên phải và ở góc dưới bên trái có hai phần rau xào. Chúng cho thấy những dải thịt màu nâu, giá đỗ và những dải thịt. Chúng được trộn lẫn với nhau. thịt bò nằm ở bên phải của mực. mực nằm bên dưới món ăn khác. Cũng có thể thấy: vải trang trí màu đỏ và đĩa gốm trắng.

<sub>EN: In the bottom right corner there is a plate of sliced beef. It shows reddish-brown meat slices, green leafy vegetables and green leafy vegetables. It is scattered on top. At the bottom there is a plate of squid. It shows green leafy vegetables, yellow pineapple chunks and pineapple pieces. It is mixed together casually. In the top left corner and at the top there are two servings of other dish. In the top right corner and in the bottom left corner there are two servings of stir-fried vegetables. They show brown meat strips, bean sprouts and meat strips. They are mixed together. The sliced beef is to the right of the squid. The squid is below the other dish. Also visible: red decorative cloth and white ceramic plate.</sub>

**[C]** (127 từ, 24/29 chi tiết)

> Ở góc dưới bên phải có một đĩa thịt bò. Nó cho thấy thịt màu nâu đỏ, rau xanh và những lát ớt đỏ. Nó được rắc lên trên rau xanh. Ở phía dưới có một đĩa mực. Nó cho thấy dứa vàng, ớt chuông đỏ và những miếng dứa. Nó được rắc với thảo mộc ở trên cùng. Ở góc trên bên trái và ở phía trên có hai phần món ăn khác. Ở góc trên bên phải và ở góc dưới bên trái có hai phần rau xào. Chúng cho thấy giá đỗ trắng, nấm nâu và hành lá xanh. Chúng được trộn lẫn với nhau trong bát. thịt bò nằm ở bên phải của mực. mực nằm bên dưới món ăn khác. Cũng có thể thấy: đĩa gốm trắng.

<sub>EN: In the bottom right corner there is a plate of sliced beef. It shows reddish-brown meat, green leafy vegetables and red chili slices. It is scattered over leafy greens. At the bottom there is a plate of squid. It shows yellow pineapple, red bell pepper and pineapple chunks. It is scattered with herbs on top. In the top left corner and at the top there are two servings of other dish. In the top right corner and in the bottom left corner there are two servings of stir-fried vegetables. They show white bean sprouts, brown mushrooms and green scallions. They are mixed together in bowl. The sliced beef is to the right of the squid. The squid is below the other dish. Also visible: white ceramic plate.</sub>

## `srcA_H-005_jpg.rf.e3e8712d94597b542a6bfe28d7aae471.jpg`

Món (nhãn): clams and scallops, other dish, roast pork, roasted chicken, shredded salad

**[A]** (130 từ, 23/27 chi tiết)

> Ở góc dưới bên phải có một phần món ăn khác. Ở góc trên bên phải có một đĩa lớn gỏi. Nó cho thấy đĩa màu xanh lá cây nhạt, nước sốt màu nâu và hành lá. Nó được trộn lẫn với nhau. Ở góc trên bên trái có một đĩa gà quay. Nó cho thấy lớp da màu nâu đỏ, đĩa trắng và đồ trang trí màu xanh lá cây. Nó được sắp xếp trên đĩa. Ở bên trái có một bát ngao sò. Nó cho thấy vỏ màu trắng, măng màu vàng và vỏ động vật hai mảnh vỏ đang mở. Nó được sắp xếp trong một chiếc bát. Ở góc dưới bên trái có một đĩa heo quay. Nó cho thấy thịt màu nâu đỏ, các lát thịt dày và ớt đỏ băm nhỏ. Nó được sắp xếp trên một chiếc đĩa. món ăn khác nằm bên dưới gỏi.

<sub>EN: In the bottom right corner there is a serving of other dish. In the top right corner there is a large plate of shredded salad. It shows light green plate, brown sauce and green onions. It is mixed together. In the top left corner there is a plate of roasted chicken. It shows reddish-brown skin, white plate and green garnish. It is arranged on plate. On the left there is a bowl of clams and scallops. It shows white shells, yellow bamboo shoots and open bivalve shells. It is arranged in a bowl. In the bottom left corner there is a plate of roast pork. It shows reddish-brown meat, thick meat slices and chopped red chili. It is arranged on a plate. The other dish is below the shredded salad.</sub>

**[B]** (138 từ, 19/30 chi tiết)

> Ở góc dưới bên phải có một phần món ăn khác. Ở góc trên bên phải có một đĩa lớn gỏi. Nó cho thấy đồ trang trí màu xanh, hành lá băm và hành tây. Nó được trộn với nhau một cách lỏng lẻo. Ở góc trên bên trái có một đĩa gà quay. Nó cho thấy cá màu nâu vàng và chanh xanh. Nó được chiên và phục vụ. Ở bên trái có một bát ngao sò. Nó cho thấy vỏ sò trắng và vỏ sò đang mở. Ở góc dưới bên trái có một đĩa heo quay. Nó cho thấy các miếng màu nâu vàng, đồ trang trí màu xanh và các miếng thịt chiên. Nó được trang trí với rau mùi tây. món ăn khác nằm bên dưới gỏi. gỏi nằm ở bên phải của gà quay. Cũng có thể nhìn thấy: đồ trang trí màu xanh và ớt đỏ.

<sub>EN: In the bottom right corner there is a serving of other dish. In the top right corner there is a large plate of shredded salad. It shows green garnish, chopped green onions and onions. It is tossed together loosely. In the top left corner there is a plate of roasted chicken. It shows golden brown fish and green lime. It is fried and served. On the left there is a bowl of clams and scallops. It shows white clam shells and open clam shells. In the bottom left corner there is a plate of roast pork. It shows golden brown pieces, green garnish and fried meat pieces. It is garnished with parsley. The other dish is below the shredded salad. The shredded salad is to the right of the roasted chicken. Also visible: green garnish and red pepper.</sub>

**[C]** (140 từ, 34/44 chi tiết)

> Ở góc dưới bên phải có một phần món ăn khác. Ở góc trên bên phải có một đĩa lớn gỏi. Nó cho thấy các loại thảo mộc xanh, các dải màu vàng và thảo mộc xanh. Nó được chất đống trên đĩa. Ở góc trên bên trái có một đĩa gà quay. Nó cho thấy lớp da màu nâu đỏ, các miếng chiên màu nâu vàng và chanh xanh. Nó được sắp xếp trên đĩa với chanh và thảo mộc. Ở bên trái có một bát ngao sò. Nó cho thấy các vỏ màu xám trắng, thịt nghêu trắng và đồ trang trí tròn màu đỏ. Nó được sắp xếp trong bát với rau và đồ trang trí. Ở góc dưới bên trái có một đĩa heo quay. Nó cho thấy các miếng màu nâu vàng, các miếng ớt đỏ và thảo mộc xanh. Nó được sắp xếp trên lá xanh. món ăn khác nằm bên dưới gỏi.

<sub>EN: In the bottom right corner there is a serving of other dish. In the top right corner there is a large plate of shredded salad. It shows green herbs, yellowish strips and green herbs. It is piled on plate. In the top left corner there is a plate of roasted chicken. It shows reddish-brown skin, golden brown fried pieces and green lime. It is arranged on plate with lime and herbs. On the left there is a bowl of clams and scallops. It shows gray-white shells, white clam meat and red round garnish. It is arranged in a bowl with vegetables and garnish. In the bottom left corner there is a plate of roast pork. It shows golden brown pieces, red chili pieces and green herbs. It is arranged on green leaf. The other dish is below the shredded salad.</sub>

## `srcA_H-006_jpg.rf.1d5bd3939a43c39859dacc3b2806beeb.jpg`

Món (nhãn): dipping sauce, other dish, shredded salad, sliced beef, whole crab

**[A]** (135 từ, 31/32 chi tiết)

> Ở góc trên bên phải có một đĩa gỏi. Nó cho thấy đĩa trắng, lá xanh và cà rốt cam. Nó được trộn lẫn với nhau. Ở góc trên bên trái có một phần món ăn khác. Ở phía dưới có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, bề mặt đĩa trắng và càng cua. Nó được đặt nguyên con trên đĩa. Ở góc dưới bên phải có một phần thịt bò. Nó cho thấy lá xà lách xanh, ớt đỏ và lát hành tây trắng. Nó được đặt trên lớp xà lách. Ở giữa có một bát nhỏ đồ chấm. Nó cho thấy chất lỏng màu nâu đỏ, bát trắng và lát ớt đỏ. gỏi nằm ở bên phải của món ăn khác. món ăn khác nằm ở phía trên của cua.

<sub>EN: In the top right corner there is a plate of shredded salad. It shows white plate, green leaves and orange carrots. It is mixed together. In the top left corner there is a serving of other dish. At the bottom there is a plate of whole crab. It shows red-orange crab shell, white plate surface and crab claws. It is placed whole on plate. In the bottom right corner there is a serving of sliced beef. It shows green lettuce leaves, red chili peppers and white onion slices. It is placed on lettuce bed. In the center there is a small bowl of dipping sauce. It shows reddish brown liquid, white bowl and red chili slices. The shredded salad is to the right of the other dish. The other dish is above the whole crab.</sub>

**[B]** (136 từ, 29/32 chi tiết)

> Ở góc trên bên phải có một đĩa gỏi. Nó cho thấy các phần lá xanh, các phần bào màu cam và các mẩu rắc màu nâu. Nó được trộn lẫn với nhau một cách lỏng lẻo. Ở góc trên bên trái có một phần món ăn khác. Ở phía dưới có một phần cua. Nó cho thấy cua màu cam đỏ, đĩa trắng và càng cua. Ở góc dưới bên phải có một đĩa thịt bò. Nó cho thấy các lát thịt màu nâu đỏ, lá xà lách xanh và các lát hành tây trắng. Nó được đặt trên xà lách. Ở giữa có một bát nhỏ đồ chấm. Nó cho thấy chất lỏng màu nâu đỏ, các lát ớt đỏ và các miếng màu trắng. Nó được đặt ở giữa. gỏi nằm ở bên phải của món ăn khác. món ăn khác nằm phía trên cua.

<sub>EN: In the top right corner there is a plate of shredded salad. It shows green leafy parts, orange shredded parts and brown sprinkle bits. It is mixed together loosely. In the top left corner there is a serving of other dish. At the bottom there is a serving of whole crab. It shows red orange crab, white plate and crab claws. In the bottom right corner there is a plate of sliced beef. It shows reddish-brown meat slices, green lettuce leaves and white onion slices. It is placed on lettuce. In the center there is a small bowl of dipping sauce. It shows reddish brown liquid, red chili slices and white pieces. It is placed in center. The shredded salad is to the right of the other dish. The other dish is above the whole crab.</sub>

**[C]** (135 từ, 41/41 chi tiết)

> Ở góc trên bên phải có một đĩa gỏi. Nó cho thấy các loại rau xanh, cà rốt bào sợi màu cam và lạc rang màu nâu. Nó được trộn lẫn với nhau trên đĩa. Ở góc trên bên trái có một phần món ăn khác. Ở phía dưới có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, đĩa trắng và các lát cà chua đỏ. Nó được sắp xếp trên đĩa trắng. Ở góc dưới bên phải có một đĩa thịt bò. Nó cho thấy các lát thịt màu nâu đỏ, lớp nền rau xanh và ớt đỏ. Nó được sắp xếp trên lớp nền rau. Ở giữa có một bát nhỏ đồ chấm. Nó cho thấy chất lỏng màu nâu đỏ, các miếng trắng và các mảnh đỏ. Nó được rải trong chất lỏng. gỏi nằm ở bên phải của món ăn khác.

<sub>EN: In the top right corner there is a plate of shredded salad. It shows green leafy vegetables, orange shredded carrots and brown roasted peanuts. It is mixed together on plate. In the top left corner there is a serving of other dish. At the bottom there is a plate of whole crab. It shows red-orange crab shell, white plate and red tomato slices. It is arranged on white plate. In the bottom right corner there is a plate of sliced beef. It shows reddish-brown meat slices, green leafy base and red chili peppers. It is arranged on leafy base. In the center there is a small bowl of dipping sauce. It shows reddish-brown liquid, white chunks and red pieces. It is scattered in liquid. The shredded salad is to the right of the other dish.</sub>

## `srcA_H-007_jpg.rf.0ca84175a22c721dfa8dcfc528442bec.jpg`

Món (nhãn): clams and scallops, dipping sauce, fresh herbs and greens, shrimp, squid, whole crab

**[A]** (132 từ, 32/35 chi tiết)

> Ở góc dưới bên phải có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, bàn gỗ màu nâu đậm và đồ trang trí màu xanh lá cây. Nó được đặt nguyên con trên đĩa. Ở bên trái và bên phải có hai phần ngao sò. Chúng cho thấy đĩa thủy tinh trong suốt, bàn gỗ màu nâu và vỏ động vật hai mảnh đang mở. Ở giữa có một đĩa tôm. Nó cho thấy bề mặt đĩa màu trắng, đồ trang trí màu xanh lá cây và các miếng chanh vàng. Nó được sắp xếp thành hàng trên đĩa. Ở phía dưới có một đĩa mực. Nó cho thấy thảo mộc xanh, thảo mộc xanh và các lát gừng vàng. Nó được thái lát và sắp xếp trên đĩa. Ở phía dưới có một đĩa rau sống. Nó cho thấy lá xanh, giá đỗ trắng và nước sốt đỏ.

<sub>EN: In the bottom right corner there is a plate of whole crab. It shows red-orange crab shell, dark brown wooden table and green garnish. It is placed whole on plate. On the left and on the right there are two servings of clams and scallops. They show clear glass plate, brown wooden table and open bivalve shells. In the center there is a plate of shrimp. It shows white plate surface, green garnish and yellow lemon wedges. It is arranged in rows on plate. At the bottom there is a plate of squid. It shows green herbs, green herbs and yellow ginger slices. It is sliced and arranged on plate. At the bottom there is a plate of fresh herbs and greens. It shows green leaves, white bean sprouts and red sauce.</sub>

**[B]** (137 từ, 31/38 chi tiết)

> Ở góc dưới bên phải có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, bề mặt đĩa màu trắng và càng cua. Nó được đặt nguyên vẹn trên đó. Ở bên trái và bên phải có hai phần ngao sò. Chúng cho thấy đĩa kim loại màu bạc, thịt nghêu trắng và các đốm thảo mộc xanh. Ở giữa có một đĩa tôm. Nó cho thấy lá thảo mộc xanh và các lát chanh. Nó được xếp ngay ngắn. Ở phía dưới có một đĩa mực. Nó cho thấy các loại thảo mộc xanh. Nó được đặt trên đĩa trắng. Ở phía dưới có một đĩa rau sống. Nó cho thấy rau xanh, giá đỗ trắng và rau xanh. Nó được đặt trên đĩa trắng. Ở phía dưới có một bát nhỏ đồ chấm.

<sub>EN: In the bottom right corner there is a plate of whole crab. It shows red-orange crab shell, white plate surface and crab claws. It is placed whole on. On the left and on the right there are two servings of clams and scallops. They show silver metallic plate, white clam meat and green herb specks. In the center there is a plate of shrimp. It shows green herb leaves and lemon slices. It is lined up neatly. At the bottom there is a plate of squid. It shows green herbs. It is placed on white plate. At the bottom there is a plate of fresh herbs and greens. It shows green leafy vegetables, white bean sprouts and green leafy vegetables. It is placed on white plate. At the bottom there is a small bowl of dipping sauce.</sub>

**[C]** (137 từ, 48/51 chi tiết)

> Ở góc dưới bên phải có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, phần đế lá xanh và những chiếc chân dài xòe ra. Nó được đặt nguyên con trên đĩa. Ở bên trái và bên phải có hai phần ngao sò. Chúng cho thấy vỏ màu xám trắng, thảo mộc xanh và phần phủ màu nâu. Chúng được sắp xếp theo hình tròn. Ở giữa có một đĩa tôm. Nó cho thấy vỏ bóng loáng, thảo mộc xanh và thảo mộc xanh. Nó được sắp xếp thành hàng trên đĩa. Ở phía dưới có một đĩa mực. Nó cho thấy sốt đỏ, thảo mộc xanh và thảo mộc xanh. Nó được sắp xếp với thảo mộc và sốt. Ở phía dưới có một đĩa rau sống. Nó cho thấy lá xanh, giá đỗ trắng và sốt đỏ. Nó được sắp xếp trên đĩa.

<sub>EN: In the bottom right corner there is a plate of whole crab. It shows red-orange crab shell, green leafy base and long spread legs. It is placed whole on plate. On the left and on the right there are two servings of clams and scallops. They show gray-white shells, green herbs and brown topping. They are arranged in circular pattern. In the center there is a plate of shrimp. It shows shiny shells, green herbs and green herbs. It is arranged in rows on plate. At the bottom there is a plate of squid. It shows red sauce, green herbs and green herbs. It is arranged with herbs and sauce. At the bottom there is a plate of fresh herbs and greens. It shows green leaves, white bean sprouts and red sauce. It is arranged on plate.</sub>

## `srcA_H-008_jpg.rf.3defe255e39d813c40cbcee01e6a63ca.jpg`

Món (nhãn): clams and scallops, dipping sauce, other dish, oyster, sea snails, shrimp, squid

**[A]** (132 từ, 31/34 chi tiết)

> Ở giữa có một đĩa ngao sò. Nó cho thấy nước dùng màu nâu trong, vành đĩa màu trắng và các vỏ động vật hai mảnh vỏ đang mở. Nó được sắp xếp trong chất lỏng nông. Ở bên phải có một phần món ăn khác. Ở góc trên bên trái và bên phải có hai phần hàu. Chúng cho thấy đĩa màu trắng, rau xanh và rau xanh. Chúng được đặt trên đĩa trắng. Ở góc dưới bên trái có một đĩa mực. Nó cho thấy đồ trang trí lá xanh và đồ trang trí lá xanh. Nó được sắp xếp trên lớp nền lá. Ở bên trái có một đĩa tôm. Nó cho thấy các miếng chiên màu nâu vàng, lát chanh vàng và các miếng chiên. Nó được sắp xếp trên một chiếc đĩa. Bên kia bàn có bốn phần ốc.

<sub>EN: In the center there is a plate of clams and scallops. It shows clear brown broth, white plate rim and open bivalve shells. It is arranged in shallow liquid. On the right there is a serving of other dish. In the top left corner and on the right there are two servings of oyster. They show white plate, green vegetables and green vegetables. They are placed on white plate. In the bottom left corner there is a plate of squid. It shows green leafy garnish and green leafy garnish. It is arranged on leafy base. On the left there is a plate of shrimp. It shows golden brown fried pieces, yellow lemon slice and fried pieces. It is arranged on a plate. Across the table there are four servings of sea snails.</sub>

**[B]** (134 từ, 24/32 chi tiết)

> Ở giữa có một đĩa ngao sò. Nó cho thấy vỏ sò trắng và vỏ sò mở. Nó được đặt trên đĩa. Ở bên phải có một phần món ăn khác. Ở góc trên bên trái và bên phải có hai phần hàu. Chúng cho thấy thảo mộc xanh và thảo mộc xanh. Chúng được đặt trên đĩa. Ở góc dưới bên trái có một đĩa mực. Nó cho thấy thảo mộc xanh, xúc tu xoăn và thảo mộc xanh. Nó được đặt trên đĩa. Ở bên trái có một đĩa tôm. Nó cho thấy các miếng màu nâu vàng, đĩa trắng và các miếng thức ăn chiên. Nó được đặt trên đĩa. Băng qua bàn có bốn phần ốc. Chúng cho thấy rau xanh, vỏ nâu xoắn và rau xanh.

<sub>EN: In the center there is a plate of clams and scallops. It shows white clam shells and open clam shells. It is placed on plate. On the right there is a serving of other dish. In the top left corner and on the right there are two servings of oyster. They show green herbs and green herbs. They are placed on plate. In the bottom left corner there is a plate of squid. It shows green herbs, curled tentacles and green herbs. It is placed on plate. On the left there is a plate of shrimp. It shows golden brown pieces, white plate and fried food pieces. It is placed on plate. Across the table there are four servings of sea snails. They show green leafy vegetables, spiral brown shells and green leafy vegetables.</sub>

**[C]** (135 từ, 40/44 chi tiết)

> Ở giữa có một đĩa ngao sò. Nó cho thấy những vỏ sò màu xám trắng, nước dùng màu nâu và thảo mộc xanh. Ở bên phải có một phần món ăn khác. Ở góc trên bên trái và bên phải có hai phần hàu. Chúng cho thấy vỏ xám thô, lớp phủ màu nâu vàng và lớp phủ màu nâu vàng. Chúng được sắp xếp trên đĩa trắng. Ở góc dưới bên trái có một đĩa mực. Nó cho thấy lá xanh, xúc tu xoăn và lá xanh. Nó được sắp xếp trên lá xanh. Ở bên trái có một đĩa tôm. Nó cho thấy những miếng chiên màu nâu vàng, lát chanh vàng và đĩa trắng. Nó được chất đống trên đĩa. Băng qua bàn có bốn phần ốc. Chúng cho thấy vỏ màu nâu, đồ trang trí lá xanh và lát cam.

<sub>EN: In the center there is a plate of clams and scallops. It shows gray-white shells, brown broth and green herbs. On the right there is a serving of other dish. In the top left corner and on the right there are two servings of oyster. They show rough gray shell, golden brown topping and golden brown topping. They are arranged on white plate. In the bottom left corner there is a plate of squid. It shows green leaf, curled tentacles and green leaf. It is arranged on green leaf. On the left there is a plate of shrimp. It shows golden brown fried pieces, yellow lime slice and white plate. It is piled on plate. Across the table there are four servings of sea snails. They show brown shells, green leafy garnish and orange slice.</sub>

## `srcA_H-009_jpg.rf.11f9e6fee8ea6f1016167ae8495e9227.jpg`

Món (nhãn): clams and scallops, shrimp, squid

**[A]** (138 từ, 21/24 chi tiết)

> Ở giữa có một đĩa lớn tôm. Nó cho thấy đĩa hoa văn xanh và những nhánh ngò tươi. Nó được sắp xếp trên một chiếc đĩa. Ở góc trên bên phải có một đĩa mực. Nó cho thấy vành hoa văn xanh, lớp vỏ vàng nâu, hải sản nướng, thảo mộc xanh tươi và dưa chuột thái lát. Nó được sắp xếp trên một chiếc đĩa. Ở góc trên bên trái có một đĩa ngao sò. Nó cho thấy nước sốt đỏ, vành xanh, vỏ động vật hai mảnh vỏ đang mở, lá xanh và bát nhỏ. Nó được phục vụ với bát bên cạnh. tôm nằm bên dưới mực. mực nằm ở bên phải của ngao sò. Các món ăn được đặt trên bề mặt bếp kim loại. Cũng có thể thấy: các đĩa hoa văn xanh, bát nhỏ, thảo mộc xanh trang trí và bát gốm trắng. Phông nền cho thấy một khu vực nấu ăn ngoài trời.

<sub>EN: In the center there is a large plate of shrimp. It shows blue patterned plate and fresh cilantro sprigs. It is arranged on a plate. In the top right corner there is a plate of squid. It shows blue patterned rim, golden brown crust, grilled seafood, fresh green herbs and sliced cucumber. It is arranged on a plate. In the top left corner there is a plate of clams and scallops. It shows red sauce, blue rim, open bivalve shells, green leaf and small bowl. It is served with side bowl. The shrimp is below the squid. The squid is to the right of the clams and scallops. The dishes are set on a metallic stovetop surface. Also visible: blue patterned plates, small bowls, green herbs garnish and white ceramic bowl. The background shows an outdoor cooking area.</sub>

**[B]** (128 từ, 21/24 chi tiết)

> Ở giữa có một phần tôm lớn. Nó cho thấy những chiếc anten dài, rau trang trí màu xanh và các nguyên liệu thái nhỏ. Nó được sắp xếp trên đĩa. Ở góc trên bên phải có một đĩa mực. Nó cho thấy lớp vỏ màu nâu vàng, các miếng hải sản nướng, rau trang trí lá xanh, lạc thái nhỏ và các lát dưa chuột. Nó được đặt trên đĩa có hoa văn. Ở góc trên bên trái có một đĩa ngao sò. Nó cho thấy vỏ sò trắng, nền sốt đỏ, vỏ sò mở, bát trắng nhỏ và lá thảo mộc xanh. Nó được trải đều trên đĩa. tôm nằm bên dưới mực. mực nằm bên phải của ngao sò. Các món ăn được đặt trên những chiếc đĩa hoa văn màu xanh. Cũng có thể thấy: rau trang trí lá xanh và bát trắng nhỏ.

<sub>EN: In the center there is a large serving of shrimp. It shows long antennae, green garnish and chopped ingredients. It is arranged on plate. In the top right corner there is a plate of squid. It shows golden brown crust, grilled seafood pieces, green leafy garnish, chopped peanuts and cucumber slices. It is placed on patterned plate. In the top left corner there is a plate of clams and scallops. It shows white clam shells, red sauce base, open clam shells, small white bowl and green herb leaves. It is spread across plate. The shrimp is below the squid. The squid is to the right of the clams and scallops. The dishes are set on a blue patterned plates. Also visible: green leafy garnish and small white bowl.</sub>

**[C]** (130 từ, 23/29 chi tiết)

> Ở giữa có một đĩa lớn tôm. Nó cho thấy lát chanh, thảo mộc xanh và bát nhỏ với nước sốt. Nó được sắp xếp trên một chiếc đĩa có hoa văn màu xanh. Ở góc trên bên phải có một đĩa mực. Nó cho thấy đĩa hoa văn xanh trắng, thịt nướng màu nâu vàng, thảo mộc lá xanh, các miếng thịt nướng và thảo mộc lá xanh. Nó được sắp xếp trên một chiếc đĩa có hoa văn. Ở góc trên bên trái có một đĩa ngao sò. Nó cho thấy đĩa hoa văn xanh trắng, nước sốt màu nâu đỏ, lá xanh, vỏ động vật hai mảnh mở và lá xanh. Nó được sắp xếp trên một chiếc đĩa. tôm nằm bên dưới mực. mực nằm ở bên phải của ngao sò. Các món ăn được đặt trên một chiếc bàn kim loại tối màu.

<sub>EN: In the center there is a large plate of shrimp. It shows lime wedge, green herbs and small bowl with sauce. It is arranged on a blue patterned plate. In the top right corner there is a plate of squid. It shows blue and white patterned plate, golden brown grilled meat, green leafy herb, grilled meat pieces and green leafy herb. It is arranged on a patterned plate. In the top left corner there is a plate of clams and scallops. It shows blue and white patterned plate, reddish-brown sauce, green leaf, open bivalve shells and green leaf. It is arranged on a plate. The shrimp is below the squid. The squid is to the right of the clams and scallops. The dishes are set on a dark metal table.</sub>

## `srcA_H-010_jpg.rf.f664af26ba9a8df4b9f165eaed8c18c8.jpg`

Món (nhãn): dessert, dipping sauce, fresh herbs and greens, shrimp, squid, stir-fried vegetables, whole crab

**[A]** (139 từ, 36/42 chi tiết)

> Ở bên trái có một đĩa cua. Nó cho thấy đĩa viền xanh, vỏ cua màu cam và càng cua. Nó được đặt nguyên con trên đĩa. Ở phía dưới có một đĩa tôm. Nó cho thấy đĩa viền xanh, hành tây thái lát và rau màu trắng. Nó được sắp xếp trên đĩa. Ở bên phải có một đĩa rau xào. Nó cho thấy viền hoa văn xanh, bề mặt đĩa trắng và những dải ớt đỏ. Nó được trộn lẫn với nhau trên đĩa. Ở góc trên bên trái có một phần món tráng miệng. Ở phía trên có một đĩa mực. Nó cho thấy hải sản màu trắng hồng, thảo mộc xanh và viền đĩa trắng. Nó được sắp xếp trên đĩa với đồ trang trí. Ở bên phải có một đĩa rau sống. Nó cho thấy lá xanh, giá đỗ trắng và nước sốt đỏ.

<sub>EN: On the left there is a plate of whole crab. It shows blue rimmed plate, orange crab shell and crab claws. It is placed whole on plate. At the bottom there is a plate of shrimp. It shows blue rimmed plate, sliced onions and white vegetables. It is arranged on a plate. On the right there is a plate of stir-fried vegetables. It shows blue patterned rim, white plate surface and red chili strips. It is mixed together on plate. In the top left corner there is a serving of dessert. At the top there is a plate of squid. It shows pinkish-white seafood, green herbs and white plate rim. It is arranged on plate with garnish. On the right there is a plate of fresh herbs and greens. It shows green leaves, white bean sprouts and red sauce.</sub>

**[B]** (137 từ, 28/39 chi tiết)

> Ở bên trái có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, vành đĩa màu trắng và càng cua. Nó được đặt nguyên vẹn trên đó. Ở phía dưới có một đĩa tôm. Nó cho thấy các lát hành tây trắng, lát hành tây và hành lá. Nó được đặt trên đĩa. Ở bên phải có một đĩa rau xào. Nó cho thấy ớt đỏ thái lát, ớt đỏ thái lát và các miếng hành tây trắng. Chúng được trộn lẫn với nhau một cách lỏng lẻo. Ở góc trên bên trái có một phần món tráng miệng. Ở phía trên có một đĩa mực. Nó cho thấy rau xanh, rau xanh và các miếng dưa chuột băm nhỏ. Ở bên phải có một đĩa rau sống. Nó cho thấy các loại thảo mộc lá xanh, thảo mộc lá xanh và các lát dưa chuột. Nó được đặt ở trên cùng.

<sub>EN: On the left there is a plate of whole crab. It shows red-orange crab shell, white plate rim and crab claws. It is placed whole on. At the bottom there is a plate of shrimp. It shows white onion slices, onion slices and green onions. It is placed on plate. On the right there is a plate of stir-fried vegetables. It shows red sliced peppers, sliced red peppers and white onion pieces. It is mixed together loosely. In the top left corner there is a serving of dessert. At the top there is a plate of squid. It shows green leafy vegetables, green leafy vegetables and chopped cucumber pieces. On the right there is a plate of fresh herbs and greens. It shows green leafy herbs, green leafy herbs and cucumber slices. It is placed on top.</sub>

**[C]** (134 từ, 46/52 chi tiết)

> Ở bên trái có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, đĩa màu xanh và trắng và những lát dưa chuột xanh. Nó được đặt nguyên con trên đĩa. Ở phía dưới có một đĩa tôm. Nó cho thấy những lát hành tây trắng, hành lá xanh và những lát hành tây. Nó được sắp xếp trên một chiếc đĩa. Ở bên phải có một đĩa rau xào. Nó cho thấy đĩa có hoa văn xanh trắng, những dải ớt đỏ và hành lá xanh. Nó được trộn lẫn với nhau trên đĩa. Ở góc trên bên trái có một phần món tráng miệng. Ở phía trên có một đĩa mực. Nó cho thấy các loại thảo mộc xanh, ớt đỏ băm và các loại thảo mộc xanh. Nó được sắp xếp với thảo mộc và ớt ở bên cạnh. Ở bên phải có một đĩa rau sống.

<sub>EN: On the left there is a plate of whole crab. It shows red-orange crab shell, blue and white plate and green cucumber slices. It is placed whole on plate. At the bottom there is a plate of shrimp. It shows white onion slices, green scallions and onion slices. It is arranged on a plate. On the right there is a plate of stir-fried vegetables. It shows blue and white patterned plate, red chili strips and green scallions. It is mixed together on plate. In the top left corner there is a serving of dessert. At the top there is a plate of squid. It shows green herbs, red chili flakes and green herbs. It is arranged with herbs and chili on side. On the right there is a plate of fresh herbs and greens.</sub>

## `srcA_H-011_jpg.rf.addf69245d81cf6c2805821b93e7b756.jpg`

Món (nhãn): clams and scallops, clear vegetable soup, rice vermicelli, shrimp, sliced beef, squid, whole crab

**[A]** (140 từ, 41/45 chi tiết)

> Ở góc dưới bên trái và ở góc dưới bên phải có hai bát canh. Chúng cho thấy nước dùng màu cam, hành lá và hành lá. Bên kia bàn có bốn phần tôm. Chúng cho thấy lá xà lách xanh, xà lách và những vỏ sò trắng nhỏ. Chúng được sắp xếp trên lớp xà lách. Ở góc trên bên phải có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, lá xà lách xanh và cua với càng. Nó được đặt nguyên con trên đĩa. Ở bên phải có một đĩa bún tươi. Nó cho thấy nước dùng màu nâu trong, mì trắng và mì trắng. Nó được đặt trên một chiếc đĩa. Ở góc trên bên trái có một đĩa thịt bò. Nó cho thấy hoa trang trí màu cam, lá xà lách xanh và vành đĩa màu trắng. Nó được sắp xếp trên đĩa với đồ trang trí.

<sub>EN: In the bottom left corner and in the bottom right corner there are two bowls of clear vegetable soup. They show orange broth, green onions and green onions. Across the table there are four servings of shrimp. They show green lettuce leaves, lettuce and small white shells. They are arranged on lettuce bed. In the top right corner there is a plate of whole crab. It shows red-orange crab shell, green lettuce leaves and crab with claws. It is placed whole on plate. On the right there is a plate of rice vermicelli. It shows clear brown broth, white noodles and white noodles. It is placed on a plate. In the top left corner there is a plate of sliced beef. It shows orange flower garnish, green lettuce leaf and white plate rim. It is arranged on plate with garnish.</sub>

**[B]** (139 từ, 30/47 chi tiết)

> Ở góc dưới bên trái và ở góc dưới bên phải có hai bát canh. Chúng cho thấy nước dùng đỏ, rau xanh và rau xanh. Bên kia bàn có bốn phần tôm. Chúng cho thấy lá xà lách xanh, lá xà lách và những viên tròn nhỏ màu trắng. Chúng được đặt trên xà lách. Ở góc trên bên phải có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, rau xanh và càng cua. Ở bên phải có một bát bún tươi. Nó cho thấy sợi mì trắng mỏng, rau xanh và sợi mì trắng mỏng. Ở góc trên bên trái có một đĩa thịt bò. Nó cho thấy những lát thịt màu nâu đỏ, hoa trang trí màu vàng và lá xà lách xanh. Nó được đặt trên đĩa trang trí. Bên kia bàn có ba phần ngao sò.

<sub>EN: In the bottom left corner and in the bottom right corner there are two bowls of clear vegetable soup. They show red broth, green vegetables and green vegetables. Across the table there are four servings of shrimp. They show green lettuce leaves, lettuce leaves and small white balls. They are placed on lettuce. In the top right corner there is a plate of whole crab. It shows red-orange crab shell, green leafy vegetables and crab claws. On the right there is a bowl of rice vermicelli. It shows white thin noodles, green leafy vegetable and white thin noodles. In the top left corner there is a plate of sliced beef. It shows reddish-brown meat slices, yellow flower decoration and green lettuce leaves. It is placed on decorative plate. Across the table there are three servings of clams and scallops.</sub>

**[C]** (133 từ, 61/62 chi tiết)

> Ở góc dưới bên trái và ở góc dưới bên phải có hai bát canh. Chúng cho thấy nước dùng màu cam đỏ, thảo mộc xanh và mì trắng. Chúng được rắc hành lá xanh. Bên kia bàn có bốn phần tôm. Chúng cho thấy lá xà lách xanh, vỏ tôm hùm màu xám đậm và tôm hùm với vỏ phân đoạn. Chúng được sắp xếp trên lớp xà lách. Ở góc trên bên phải có một đĩa cua. Nó cho thấy vỏ cua màu cam đỏ, rau xanh và đồ trang trí hình hoa màu cam. Nó được đặt nguyên vẹn trên lớp rau. Ở bên phải có một đĩa bún tươi. Nó cho thấy mì trắng, đồ trang trí lá xanh và chất lỏng màu nâu đậm. Nó được xếp chồng trên đĩa. Ở góc trên bên trái có một đĩa thịt bò.

<sub>EN: In the bottom left corner and in the bottom right corner there are two bowls of clear vegetable soup. They show orange-red broth, green herbs and white noodles. They are scattered with green onions. Across the table there are four servings of shrimp. They show green lettuce leaves, dark gray lobster shell and lobster with segmented shell. They are arranged on bed of lettuce. In the top right corner there is a plate of whole crab. It shows red-orange crab shell, green leafy vegetables and orange flower-like garnish. It is placed whole on leafy base. On the right there is a plate of rice vermicelli. It shows white noodles, green leafy garnish and dark brown liquid. It is stacked on plate. In the top left corner there is a plate of sliced beef.</sub>

## `srcA_H-012_jpg.rf.20093064d338224b22dab43c00197317.jpg`

Món (nhãn): fresh herbs and greens, hotpot, pho noodle soup, sliced beef, whole crab

**[A]** (129 từ, 33/37 chi tiết)

> Ở bên trái có một đĩa thịt bò. Nó cho thấy đĩa trắng, đồ trang trí màu xanh lá và đồ trang trí màu cam. Nó được phục vụ trên đĩa trắng. Ở bên phải có một đĩa rau sống. Nó cho thấy lá xanh, bàn gỗ và rau xanh. Nó được chất cao trên đĩa. Ở phía trên có một nồi lẩu. Nó cho thấy nước dùng màu cam, chân cua đỏ và rau xanh. Nó được phục vụ trong nồi kim loại. Ở góc dưới bên phải có một đĩa phở. Nó cho thấy mì màu nâu nhạt, đồ trang trí lá xanh và mì dẹt. Ở phía dưới có một nồi cua. Nó cho thấy vỏ cua màu đỏ cam, nồi màu nâu đậm và càng cua. Nó được đặt nguyên con trong nồi.

<sub>EN: On the left there is a plate of sliced beef. It shows white plate, green garnish and orange garnish. It is served on white plate. On the right there is a plate of fresh herbs and greens. It shows green leaves, wooden table and green leafy vegetables. It is piled high on plate. At the top there is a pot of hotpot. It shows orange broth, red crab legs and green vegetables. It is served in metal pot. In the bottom right corner there is a plate of pho noodle soup. It shows light brown noodles, green leafy garnish and flat noodles. At the bottom there is a pot of whole crab. It shows red-orange crab shell, dark brown pot and crab claws. It is placed whole in pot.</sub>

**[B]** (133 từ, 27/36 chi tiết)

> Ở bên trái có một đĩa thịt bò. Nó cho thấy những lát thịt màu nâu đỏ, hành lá thái nhỏ và hoa đỏ trang trí. Nó được phục vụ trên đĩa dài. Ở bên phải có một đĩa rau sống. Nó cho thấy rau xanh, mì trắng và rau xanh. Ở phía trên có một nồi lẩu. Nó cho thấy nước dùng màu đỏ, các phần lá xanh và miếng càng tôm hùm. Nó được luộc trong nước dùng. Ở góc dưới bên phải có một đĩa phở. Nó cho thấy mì màu vàng nhạt, rau xanh và mì vàng dẹt. Nó được đặt trên đĩa trắng. Ở phía dưới có một nồi cua. Nó cho thấy vỏ cua màu đỏ cam, càng cua và chân cua. Nó được đặt nguyên con bên trong.

<sub>EN: On the left there is a plate of sliced beef. It shows reddish-brown meat slices, chopped green onions and red flower garnish. It is served on long plate. On the right there is a plate of fresh herbs and greens. It shows green leafy vegetables, white noodles and green leafy vegetables. At the top there is a pot of hotpot. It shows red broth liquid, green leafy parts and lobster claw piece. It is boiled in broth. In the bottom right corner there is a plate of pho noodle soup. It shows pale yellow noodles, green leafy vegetable and flat yellow noodles. It is placed on white plate. At the bottom there is a pot of whole crab. It shows red-orange crab shell, crab claws and crab legs. It is placed whole inside.</sub>

**[C]** (128 từ, 46/50 chi tiết)

> Ở bên trái có một đĩa thịt bò. Nó cho thấy những lát thịt màu nâu đỏ, thảo mộc xanh và đồ trang trí màu cam. Nó được sắp xếp trên đĩa trắng. Ở bên phải có một giỏ rau sống. Nó cho thấy lá xanh, bề mặt gỗ màu nâu và đĩa trắng. Ở phía trên có một nồi lẩu. Nó cho thấy nước dùng màu nâu trong, đuôi tôm hùm đỏ và thảo mộc xanh. Nó đang nổi trong nước dùng. Ở góc dưới bên phải có một đĩa phở. Nó cho thấy mì màu nâu nhạt, đĩa trắng và lá xanh. Nó được chất đống trên đĩa. Ở phía dưới có một bát cua. Nó cho thấy vỏ cua màu đỏ cam, bát màu nâu đậm và thảo mộc xanh. Nó được đặt nguyên con trong bát.

<sub>EN: On the left there is a plate of sliced beef. It shows reddish-brown meat slices, green herbs and orange garnish. It is arranged on white plate. On the right there is a basket of fresh herbs and greens. It shows green leaves, brown wooden surface and white plate. At the top there is a pot of hotpot. It shows clear brown broth, red lobster tail and green herbs. It is floating in broth. In the bottom right corner there is a plate of pho noodle soup. It shows light brown noodles, white plate and green leaf. It is piled on plate. At the bottom there is a bowl of whole crab. It shows red-orange crab shell, dark brown bowl and green herbs. It is placed whole in bowl.</sub>

## `srcA_H-015_jpg.rf.00f392b7bb318b7e5c118695b0ffa87c.jpg`

Món (nhãn): baguette sandwich, fresh herbs and greens, hotpot, other dish, rice vermicelli, shrimp, whole crab

**[A]** (130 từ, 32/36 chi tiết)

> Ở giữa có một nồi lẩu. Nó cho thấy nước dùng màu nâu trong, các miếng cà chua đỏ và các miếng rau xanh. Ở góc trên bên trái và ở góc dưới bên trái có hai đĩa rau sống. Chúng cho thấy rau lá xanh, rau lá xanh và thìa kim loại. Ở góc dưới bên trái có một đĩa bún tươi. Nó cho thấy mì trắng, bề mặt gỗ màu nâu và mì trắng. Ở bên phải có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, đồ trang trí màu xanh và đồ trang trí màu xanh. Nó được đặt nguyên con trên đĩa. Ở giữa và ở góc dưới bên phải có hai phần tôm. Chúng cho thấy lá xà lách xanh, xà lách và đồ trang trí cà rốt. Chúng được sắp xếp trên một chiếc đĩa.

<sub>EN: In the center there is a pot of hotpot. It shows clear brown broth, red tomato pieces and green vegetable pieces. In the top left corner and in the bottom left corner there are two plates of fresh herbs and greens. They show green leafy vegetables, green leafy vegetables and metal spoon. In the bottom left corner there is a plate of rice vermicelli. It shows white noodles, brown wooden surface and white noodles. On the right there is a plate of whole crab. It shows red-orange crab shell, green garnish and green garnish. It is placed whole on plate. In the center and in the bottom right corner there are two servings of shrimp. They show green lettuce leaves, lettuce and carrot garnish. They are arranged on a plate.</sub>

**[B]** (140 từ, 34/41 chi tiết)

> Ở giữa có một nồi lẩu. Nó cho thấy nước dùng màu nâu trong, những miếng cà chua đỏ và rau xanh. Nó được đặt xung quanh nồi trung tâm. Ở góc trên bên trái và ở góc dưới bên trái có hai đĩa rau sống. Chúng cho thấy rau xanh, rau xanh và thìa kim loại. Ở góc dưới bên trái có một đĩa bún tươi. Nó cho thấy sợi mì trắng mỏng, mì trắng mỏng và rau trang trí xanh. Nó được đặt ở giữa. Ở bên phải có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, rau trang trí xanh và càng cua. Ở giữa và ở góc dưới bên phải có hai phần tôm. Chúng cho thấy rau trang trí xanh, lá xanh và lát ớt đỏ. Chúng được đặt trên đĩa trắng.

<sub>EN: In the center there is a pot of hotpot. It shows clear brown broth, red tomato pieces and green leafy vegetables. It is placed around central pot. In the top left corner and in the bottom left corner there are two plates of fresh herbs and greens. They show green leafy vegetables, green leafy vegetables and metal spoon. In the bottom left corner there is a plate of rice vermicelli. It shows white thin noodles, thin white noodles and green leaf garnish. It is placed in center. On the right there is a plate of whole crab. It shows red-orange crab shell, green leafy garnish and crab claws. In the center and in the bottom right corner there are two servings of shrimp. They show green leaf garnish, green leaf and red chili slice. They are placed on white plate.</sub>

**[C]** (132 từ, 50/53 chi tiết)

> Ở giữa có một nồi lẩu. Nó cho thấy nước dùng màu nâu trong, những miếng cà chua đỏ và rau xanh. Nó đang nổi trong nước dùng. Ở góc trên bên trái và ở góc dưới bên trái có hai đĩa rau sống. Chúng cho thấy rau xanh, thìa bạc và rau xanh. Chúng nằm rải rác trên đĩa. Ở góc dưới bên trái có một đĩa bún tươi. Nó cho thấy mì trắng, bề mặt gỗ màu nâu và lá xanh. Nó được xếp chồng lên đĩa. Ở bên phải có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, rau trang trí màu xanh và hoa trang trí màu cam. Nó được đặt nguyên con trên đĩa. Ở giữa và ở góc dưới bên phải có hai phần tôm.

<sub>EN: In the center there is a pot of hotpot. It shows clear brown broth, red tomato pieces and green leafy vegetables. It is floating in broth. In the top left corner and in the bottom left corner there are two plates of fresh herbs and greens. They show green leafy vegetables, silver spoon and green leafy vegetables. They are scattered on plate. In the bottom left corner there is a plate of rice vermicelli. It shows white noodles, brown wooden surface and green leaf. It is piled on plate. On the right there is a plate of whole crab. It shows red-orange crab shell, green leafy garnish and orange flower garnish. It is placed whole on plate. In the center and in the bottom right corner there are two servings of shrimp.</sub>

## `srcA_H-016_jpg.rf.18183470157653a32c75009531aa6a75.jpg`

Món (nhãn): clams and scallops, dipping sauce, squid

**[A]** (111 từ, 17/20 chi tiết)

> Ở bên phải có một đĩa lớn ngao sò. Nó cho thấy đĩa trắng, thảo mộc xanh, vỏ động vật hai mảnh vỏ đang mở, thảo mộc xanh và hạt nâu. Nó được sắp xếp trên một chiếc đĩa. Ở bên trái có một đĩa lớn mực. Nó cho thấy đĩa trắng, lát dưa chuột xanh, ớt đỏ, dưa chuột thái lát và ớt đỏ. Nó được sắp xếp trên đĩa với đồ trang trí. Ở góc trên bên trái có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ và chất lỏng màu nâu đỏ. ngao sò nằm ở bên phải của mực. mực nằm bên dưới đồ chấm. Các món ăn được đặt trên một chiếc bàn kim loại.

<sub>EN: On the right there is a large plate of clams and scallops. It shows white plate, green herbs, open bivalve shells, green herbs and brown seeds. It is arranged on a plate. On the left there is a large plate of squid. It shows white plate, green cucumber slices, red chili, sliced cucumber and red chili. It is arranged on plate with garnish. In the top left corner there are two small bowls of dipping sauce. They show reddish brown liquid and reddish brown liquid. The clams and scallops is to the right of the squid. The squid is below the dipping sauce. The dishes are set on a metallic table.</sub>

**[B]** (125 từ, 19/20 chi tiết)

> Ở bên phải có một đĩa lớn ngao sò. Nó cho thấy vỏ sò trắng, nhân màu vàng, sò mở, nhân màu vàng và các loại hạt nhỏ. Nó được đặt trên đĩa. Ở bên trái có một đĩa lớn mực. Nó cho thấy dưa chuột thái lát màu xanh, hành lá thái lát và các lát dưa chuột. Nó được trang trí với rau củ. Ở góc trên bên trái có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, chất rắn màu trắng, chất rắn màu trắng và chất lỏng. Chúng được đặt cạnh nhau. ngao sò nằm ở bên phải của mực. mực nằm bên dưới đồ chấm. Các món ăn được đặt trên một bề mặt màu xám kim loại. Cũng có thể thấy: đĩa gốm trắng, bát trắng nhỏ và nồi kim loại.

<sub>EN: On the right there is a large plate of clams and scallops. It shows white clam shells, yellow filling, open clams, yellow filling and small nuts. It is placed on plate. On the left there is a large plate of squid. It shows green sliced cucumber, sliced green onions and cucumber slices. It is garnished with vegetables. In the top left corner there are two small bowls of dipping sauce. They show reddish brown liquid, white solid, white solid and liquid. They are placed beside each other. The clams and scallops is to the right of the squid. The squid is below the dipping sauce. The dishes are set on a metallic gray surface. Also visible: white ceramic plates, small white bowls and metal pot.</sub>

**[C]** (122 từ, 21/22 chi tiết)

> Ở bên phải có một đĩa lớn ngao sò. Nó cho thấy các vỏ sò màu xám trắng, thảo mộc xanh, nhân màu vàng nhạt, vỏ động vật hai mảnh vỏ đang mở và thảo mộc. Nó được sắp xếp thành một cụm. Ở bên trái có một đĩa lớn mực. Nó cho thấy các lát dưa chuột xanh, sợi hành tây trắng, lát dưa chuột, sợi hành lá xanh và sợi hành tây trắng. Nó được sắp xếp trên đĩa với đồ trang trí. Ở góc trên bên trái có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, một muỗng nhỏ màu trắng, chất lỏng màu nâu đỏ và một muỗng nhỏ màu trắng. Chúng được đặt trong bát nhỏ. ngao sò nằm ở bên phải của mực. mực nằm bên dưới đồ chấm. Các món ăn được đặt trên một chiếc bàn màu xám kim loại.

<sub>EN: On the right there is a large plate of clams and scallops. It shows gray-white shells, green herbs, yellowish filling, open bivalve shells and herbs. It is arranged in a cluster. On the left there is a large plate of squid. It shows green cucumber slices, white onion strips, cucumber slices, green onion strips and white onion strips. It is arranged on plate with garnish. In the top left corner there are two small bowls of dipping sauce. They show reddish-brown liquid, white dollop, reddish-brown liquid and white dollop. They are placed in small bowl. The clams and scallops is to the right of the squid. The squid is below the dipping sauce. The dishes are set on a metallic gray table.</sub>

## `srcA_H-018_jpg.rf.8484d42fe04261c18857c5ec1a24242d.jpg`

Món (nhãn): clams and scallops, fresh herbs and greens, shrimp, whole crab

**[A]** (137 từ, 24/26 chi tiết)

> Ở góc trên bên trái và ở phía dưới có hai phần cua. Chúng cho thấy vỏ cua màu đỏ cam, lá mùi tây xanh và ớt chuông đỏ. Chúng được đặt nguyên vẹn trên đĩa. Bên kia bàn có ba đĩa rau sống. Chúng cho thấy các loại thảo mộc lá xanh. Ở góc trên bên phải và ở bên phải có hai phần ngao sò. Chúng cho thấy bắp ngô vàng, xúc xích đỏ và cà rốt cam. Chúng được sắp xếp trong một chiếc bát màu đen. Ở giữa và ở góc dưới bên trái có hai phần tôm. Chúng cho thấy các loài giáp xác màu đỏ tươi, đồ trang trí lá xanh và các loài giáp xác. Chúng được tập trung trong bát. Các cua nằm bên dưới các rau sống. Các rau sống nằm bên trên các ngao sò.

<sub>EN: In the top left corner and at the bottom there are two servings of whole crab. They show red-orange crab shell, green parsley leaves and red bell pepper. They are placed whole on plate. Across the table there are three plates of fresh herbs and greens. They show green leafy herbs. In the top right corner and on the right there are two servings of clams and scallops. They show yellow corn on cob, red sausage and orange carrot. They are arranged in a black bowl. In the center and in the bottom left corner there are two servings of shrimp. They show bright red crustaceans, green leafy garnish and crustaceans. They are clustered in bowl. The whole crab are below the fresh herbs and greens. The fresh herbs and greens are above the clams and scallops.</sub>

**[B]** (134 từ, 25/31 chi tiết)

> Ở góc trên bên trái và ở phía dưới có hai phần cua. Chúng cho thấy vỏ cua màu đỏ cam, rau trang trí lá xanh và chân cua trải ra. Chúng được đặt nguyên vẹn ở giữa. Bên kia bàn có ba đĩa rau sống. Chúng cho thấy lá mùi tây xanh, bắp và nấm kim châm. Chúng được trang trí với mùi tây. Ở góc trên bên phải và ở bên phải có hai phần ngao sò. Chúng cho thấy thịt nghêu trắng, vỏ nghêu mở và bắp. Chúng được đặt sát nhau. Ở giữa và ở góc dưới bên trái có hai phần tôm. Chúng cho thấy mùi tây xanh, râu dài và vỏ bóng. Chúng được đặt sát nhau. Các cua nằm bên dưới các rau sống.

<sub>EN: In the top left corner and at the bottom there are two servings of whole crab. They show red-orange crab shell, green leafy garnish and crab legs spread. They are placed whole centrally. Across the table there are three plates of fresh herbs and greens. They show green parsley leaves, corn on cob and enoki mushrooms. They are garnished with parsley. In the top right corner and on the right there are two servings of clams and scallops. They show white clam meat, open clam shells and corn on cob. They are placed together closely. In the center and in the bottom left corner there are two servings of shrimp. They show green parsley, long antennae and shiny shells. They are placed together closely. The whole crab are below the fresh herbs and greens.</sub>

**[C]** (137 từ, 30/34 chi tiết)

> Ở góc trên bên trái và ở phía dưới có hai phần cua. Chúng cho thấy vỏ cua màu đỏ cam, rau mùi xanh và lát chanh vàng. Chúng được đặt nguyên vẹn trên đĩa. Bên kia bàn có ba đĩa rau sống. Chúng cho thấy các loại thảo mộc lá xanh, chanh vàng và các loại thảo mộc lá xanh. Chúng được sắp xếp trong các bát riêng biệt. Ở góc trên bên phải và ở bên phải có hai phần ngao sò. Chúng cho thấy ngô vàng, xúc xích đỏ và cà rốt cam. Chúng được sắp xếp trong một chiếc bát. Ở giữa và ở góc dưới bên trái có hai phần tôm. Chúng cho thấy vỏ màu đỏ tươi, đồ trang trí lá xanh đậm và vật thể nền màu vàng. Chúng được chất đống trong bát. Các cua nằm bên dưới các rau sống.

<sub>EN: In the top left corner and at the bottom there are two servings of whole crab. They show red-orange crab shell, green parsley and yellow lemon wedge. They are placed whole on plate. Across the table there are three plates of fresh herbs and greens. They show green leafy herbs, yellow lemon and green leafy herbs. They are arranged in separate bowls. In the top right corner and on the right there are two servings of clams and scallops. They show yellow corn, red sausage and orange carrot. They are arranged in a bowl. In the center and in the bottom left corner there are two servings of shrimp. They show bright red shells, dark green leafy garnish and yellow background object. They are piled in bowl. The whole crab are below the fresh herbs and greens.</sub>

## `srcA_H-021_jpg.rf.769476f327ba7ba7c4e0750c400ca24e.jpg`

Món (nhãn): clams and scallops, dipping sauce, other dish, oyster, sea snails, shrimp, squid, whole crab

**[A]** (140 từ, 35/42 chi tiết)

> Bên kia bàn có bốn phần tôm. Chúng cho thấy bề mặt đĩa trắng, lá xà lách xanh và lá xà lách. Chúng được sắp xếp trên đĩa trắng. Ở bên trái và bên phải có ba phần cua. Chúng cho thấy vỏ cua màu đỏ cam, mặt bàn gỗ màu nâu và càng cua. Chúng được đặt nguyên con trên đĩa. Bên kia bàn có bốn phần ngao sò. Chúng cho thấy đĩa trắng, bề mặt gỗ màu nâu và thảo mộc xanh. Chúng được sắp xếp trên đĩa. Ở góc trên bên phải và bên phải có hai phần hàu. Chúng cho thấy đĩa trắng, bề mặt gỗ màu nâu và sò điệp trong vỏ. Chúng được sắp xếp trên đĩa. Bên kia bàn có ba phần ốc. Chúng cho thấy các lát ớt chuông đỏ, thảo mộc xanh và vỏ màu nâu. Chúng được rải trên đĩa.

<sub>EN: Across the table there are four servings of shrimp. They show white plate surface, green lettuce leaves and lettuce leaves. They are arranged on white plate. On the left and on the right there are three servings of whole crab. They show red-orange crab shell, brown wooden table and crab claws. They are placed whole on plate. Across the table there are four servings of clams and scallops. They show white plate, brown wooden surface and green herbs. They are arranged on plate. In the top right corner and on the right there are two servings of oyster. They show white plate, brown wooden surface and scallops in shells. They are arranged on plate. Across the table there are three servings of sea snails. They show red bell pepper slices, green herbs and brown shells. They are scattered on plate.</sub>

**[B]** (136 từ, 35/41 chi tiết)

> Bên kia bàn có bốn phần tôm. Chúng cho thấy những thân màu cam cong, râu dài và nhiều cái được sắp xếp. Chúng được đặt trên đĩa. Ở bên trái và bên phải có ba phần cua. Chúng cho thấy vỏ cua màu đỏ cam, bề mặt đĩa trắng và càng cua. Chúng được trải khắp đĩa. Bên kia bàn có bốn phần ngao sò. Chúng cho thấy rau thơm trang trí màu xanh, thịt có thể nhìn thấy bên trong và rau thơm xanh băm nhỏ. Chúng được đặt trên đĩa trắng. Ở góc trên bên phải và bên phải có hai phần hàu. Chúng cho thấy đĩa gốm trắng, rau trang trí màu xanh và rau trang trí màu xanh. Chúng được đặt trên đĩa trắng. Bên kia bàn có ba phần ốc. Chúng cho thấy vỏ đốm nâu, ớt thái lát màu đỏ và vỏ đốm nâu.

<sub>EN: Across the table there are four servings of shrimp. They show curved orange bodies, long antennae and many arranged. They are placed on plate. On the left and on the right there are three servings of whole crab. They show red-orange crab shell, white plate surface and crab claws. They are spread across plate. Across the table there are four servings of clams and scallops. They show green herb garnish, visible meat inside and chopped green herbs. They are placed on white plate. In the top right corner and on the right there are two servings of oyster. They show white ceramic plate, green garnish and green garnish. They are placed on white plate. Across the table there are three servings of sea snails. They show brown spotted shells, red sliced peppers and spotted brown shells.</sub>

**[C]** (134 từ, 41/54 chi tiết)

> Bên kia bàn có bốn phần tôm. Chúng có lớp vỏ màu nâu vàng, xà lách xanh và lá xà lách xanh. Chúng được sắp xếp trên một chiếc đĩa trắng. Ở bên trái và bên phải có ba phần cua. Chúng có vỏ cua màu đỏ cam, đĩa trắng và bàn gỗ màu nâu. Chúng được đặt nguyên con trên đĩa. Bên kia bàn có bốn phần ngao sò. Chúng có thảo mộc xanh, thịt màu hồng và thảo mộc xanh. Ở góc trên bên phải và bên phải có hai phần hàu. Chúng có lớp phủ xanh, lớp phủ xanh và đĩa trắng. Chúng được sắp xếp thành một cụm. Bên kia bàn có ba phần ốc. Chúng có vỏ đốm nâu, ớt thái lát màu đỏ và thảo mộc lá xanh. Chúng được rải trên đĩa.

<sub>EN: Across the table there are four servings of shrimp. They show golden-brown coating, green lettuce and green lettuce leaves. They are arranged on a white plate. On the left and on the right there are three servings of whole crab. They show red-orange crab shell, white plate and brown wooden table. They are placed whole on plate. Across the table there are four servings of clams and scallops. They show green herbs, pinkish meat and green herbs. In the top right corner and on the right there are two servings of oyster. They show green topping, green topping and white plate. They are arranged in a cluster. Across the table there are three servings of sea snails. They show brown spotted shells, red sliced peppers and green leafy herbs. They are scattered on plate.</sub>

## `srcA_H-022_jpg.rf.5ce347c46f0a08d3306e956dd27448f8.jpg`

Món (nhãn): clams and scallops, dipping sauce, other dish, oyster, shrimp, sliced beef, squid, whole crab

**[A]** (135 từ, 40/45 chi tiết)

> Ở giữa có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, đĩa trắng và càng cua. Nó được đặt nguyên con trên đĩa. Bên kia bàn có ba phần món ăn khác. Ở góc trên bên trái và ở phía dưới có hai phần ngao sò. Chúng cho thấy đĩa trắng, bàn màu nâu và vỏ động vật hai mảnh đang mở. Chúng được sắp xếp trên đĩa trắng. Ở bên trái có một đĩa hàu. Nó cho thấy đĩa trắng và nước sốt màu xanh lá cây. Nó được sắp xếp theo hình tròn. Ở bên phải có hai phần mực. Chúng cho thấy thịt màu trắng hồng, thịt thái lát mỏng và ớt xanh. Chúng được sắp xếp trên một chiếc đĩa trắng. Ở góc trên bên trái và ở góc trên bên phải có ba phần thịt bò.

<sub>EN: In the center there is a plate of whole crab. It shows red-orange crab shell, white plate and crab claws. It is placed whole on plate. Across the table there are three servings of other dish. In the top left corner and at the bottom there are two servings of clams and scallops. They show white plate, brown table and open bivalve shells. They are arranged on white plate. On the left there is a plate of oyster. It shows white plate and green sauce. It is arranged in a circle. On the right there are two servings of squid. They show pinkish-white meat, thinly sliced meat and green chili. They are arranged on a white plate. In the top left corner and in the top right corner there are three servings of sliced beef.</sub>

**[B]** (138 từ, 36/44 chi tiết)

> Ở giữa có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, hạt vừng trắng và càng cua. Nó trải đều khắp đĩa. Trên bàn có ba phần món ăn khác. Ở góc trên bên trái và ở phía dưới có hai phần ngao sò. Chúng cho thấy vỏ sò trắng, lòng đỏ trứng vàng và vỏ sò mở. Chúng được đặt trên đĩa trắng. Ở bên trái có một đĩa hàu. Nó cho thấy vỏ màu xám trắng, đồ trang trí màu xanh lá và vỏ sò nửa. Nó được đặt trên đĩa. Ở bên phải có hai phần mực. Chúng cho thấy thảo mộc xanh, thảo mộc xanh và lát ớt đỏ. Chúng được đặt trên đĩa trắng. Ở góc trên bên trái và ở góc trên bên phải có ba phần thịt bò.

<sub>EN: In the center there is a plate of whole crab. It shows red-orange crab shell, white sesame seeds and crab claws. It is spread across plate. Across the table there are three servings of other dish. In the top left corner and at the bottom there are two servings of clams and scallops. They show white clam shells, yellow egg yolk and open clam shells. They are placed on white plate. On the left there is a plate of oyster. It shows gray white shells, green garnish and half shells. It is placed on plate. On the right there are two servings of squid. They show green herbs, green herbs and red chili slices. They are placed on white plate. In the top left corner and in the top right corner there are three servings of sliced beef.</sub>

**[C]** (139 từ, 51/56 chi tiết)

> Ở giữa có một đĩa cua. Nó cho thấy vỏ cua màu cam đỏ, đĩa trắng và mặt bàn màu nâu. Nó được đặt nguyên con trên đĩa. Bên kia bàn có ba phần món ăn khác. Ở góc trên bên trái và ở phía dưới có hai phần ngao sò. Chúng cho thấy vỏ màu xám trắng, thịt màu vàng nhạt và lá xanh. Chúng được sắp xếp thành một đống. Bên trái có một đĩa hàu. Nó cho thấy vỏ xám thô, nước sốt màu xanh lá nhạt và đồ trang trí màu xanh lá. Nó được sắp xếp theo hình tròn. Bên phải có hai phần mực. Chúng cho thấy ớt đỏ, hành lá và các miếng ớt đỏ. Chúng được sắp xếp thành một đống. Ở góc trên bên trái và ở góc trên bên phải có ba phần thịt bò.

<sub>EN: In the center there is a plate of whole crab. It shows red-orange crab shell, white plate and brown table surface. It is placed whole on plate. Across the table there are three servings of other dish. In the top left corner and at the bottom there are two servings of clams and scallops. They show gray-white shells, yellowish meat and green leaf. They are arranged in a pile. On the left there is a plate of oyster. It shows rough gray shell, light green sauce and green garnish. It is arranged in a circular pattern. On the right there are two servings of squid. They show red pepper, green onion and red pepper pieces. They are arranged in a pile. In the top left corner and in the top right corner there are three servings of sliced beef.</sub>

## `srcA_H-024_jpg.rf.b8fa91a975acf0d5afbf222989aaf9cd.jpg`

Món (nhãn): fresh herbs and greens, hotpot, other dish, oyster, sea snails

**[A]** (139 từ, 30/31 chi tiết)

> Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy bề mặt gỗ màu nâu nhạt, rau xanh và giá đỗ trắng. Nó được phủ lên trên bằng giá đỗ. Ở góc trên bên phải có một đĩa hàu. Nó cho thấy đĩa trắng, vỏ màu xám và lá xanh. Nó được sắp xếp thành hình tròn. Ở bên trái có một nồi lẩu. Nó cho thấy các loại thảo mộc xanh nổi lên, ớt đỏ có thể nhìn thấy và bề mặt nước dùng sẫm màu. Đó là các nguyên liệu nổi trong nước dùng. Ở góc trên bên trái và bên phải có hai phần món ăn khác. Ở góc dưới bên phải có một nồi ốc. Nó cho thấy chất lỏng màu trắng kem, thảo mộc xanh và ốc với vỏ xoắn ốc. Nó đang nổi trong chất lỏng. rau sống nằm bên dưới hàu.

<sub>EN: In the bottom left corner there is a plate of fresh herbs and greens. It shows light brown wooden surface, green leafy vegetables and white bean sprouts. It is topped with bean sprouts. In the top right corner there is a plate of oyster. It shows white plate, gray shells and green leaves. It is arranged in circle. On the left there is a pot of hotpot. It shows green herbs floating, red peppers visible and dark broth surface. It is ingredients floating in broth. In the top left corner and on the right there are two servings of other dish. In the bottom right corner there is a pot of sea snails. It shows white creamy liquid, green herbs and snails with spiral shells. It is floating in liquid. The fresh herbs and greens is below the oyster.</sub>

**[B]** (132 từ, 23/29 chi tiết)

> Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy những lá xà lách xanh, giá đỗ và lá xà lách. Chúng được trộn lẫn với nhau một cách lỏng lẻo. Ở góc trên bên phải có một đĩa hàu. Nó cho thấy những vỏ sò màu xám trắng, lớp phủ thảo mộc xanh và những nửa vỏ sò. Nó được đặt theo hình tròn. Ở bên trái có một nồi lẩu. Nó cho thấy thảo mộc xanh đậm, ớt thái lát đỏ và ớt đỏ thái lát. Nó đang nổi trên bề mặt. Ở góc trên bên trái và bên phải có hai phần món ăn khác. Ở góc dưới bên phải có một bát ốc. Nó cho thấy nước dùng kem màu trắng, vỏ sò đốm nâu và lát ớt đỏ. rau sống nằm bên dưới hàu.

<sub>EN: In the bottom left corner there is a plate of fresh herbs and greens. It shows green lettuce leaves, bean sprouts and lettuce leaves. It is mixed together loosely. In the top right corner there is a plate of oyster. It shows gray white shells, green herb topping and half shells. It is placed in circular pattern. On the left there is a pot of hotpot. It shows dark green herbs, red sliced peppers and sliced red peppers. It is floating on surface. In the top left corner and on the right there are two servings of other dish. In the bottom right corner there is a bowl of sea snails. It shows white creamy broth, brown spotted shells and red chili slices. The fresh herbs and greens is below the oyster.</sub>

**[C]** (132 từ, 32/35 chi tiết)

> Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy rau xanh, mì màu nâu nhạt và rau xanh. Nó được rải trên rau xanh. Ở góc trên bên phải có một đĩa hàu. Nó cho thấy rau thơm xanh, vỏ màu xám đậm và rau thơm trang trí. Nó được sắp xếp theo hình tròn. Ở bên trái có một nồi lẩu. Nó cho thấy rau thơm xanh, lát ớt đỏ và nước dùng trong. Nó đang nổi trong nước dùng. Ở góc trên bên trái và bên phải có hai phần món ăn khác. Ở góc dưới bên phải có một bát ốc. Nó cho thấy vỏ xoắn màu nâu có đốm, nước dùng kem trắng và ớt đỏ thái lát. Nó được rải trong nước dùng.

<sub>EN: In the bottom left corner there is a plate of fresh herbs and greens. It shows green leafy vegetables, light brown noodles and green leafy vegetables. It is scattered over leafy greens. In the top right corner there is a plate of oyster. It shows green herb topping, dark gray shell and green herb garnish. It is arranged in circular pattern. On the left there is a pot of hotpot. It shows green herbs, red chili slices and clear broth. It is floating in broth. In the top left corner and on the right there are two servings of other dish. In the bottom right corner there is a bowl of sea snails. It shows spiral brown shells with spots, white creamy broth and red sliced peppers. It is scattered in broth.</sub>

## `srcA_H-054_jpg.rf.74b133dfd4da6998306da8505d0221f4.jpg`

Món (nhãn): fresh herbs and greens, hotpot, pho noodle soup, sliced beef, vietnamese pork ham

**[A]** (139 từ, 33/36 chi tiết)

> Ở góc trên bên trái có một đĩa lớn rau sống. Nó cho thấy các loại rau xanh, nấm kim châm trắng và thịt viên nướng màu nâu. Nó được sắp xếp trên một chiếc đĩa. Ở góc trên bên phải có một nồi lẩu. Nó cho thấy nước dùng màu nâu trong, rau xanh và cà chua đỏ. Ở phía dưới có một đĩa phở. Nó cho thấy đĩa trắng, mì màu vàng nhạt và mì trắng dẹt. Ở góc dưới bên trái có một đĩa chả giò. Nó cho thấy thịt sống thái lát, thịt viên nướng và rau xanh. Ở giữa có một đĩa thịt bò. Nó cho thấy các lát thịt màu nâu đỏ, vân mỡ trắng và trứng trắng. Nó được sắp xếp trên một chiếc đĩa. rau sống nằm ở bên trái của lẩu.

<sub>EN: In the top left corner there is a large plate of fresh herbs and greens. It shows green leafy vegetables, white enoki mushrooms and brown grilled meatballs. It is arranged on a plate. In the top right corner there is a pot of hotpot. It shows clear brown broth, green vegetables and red tomatoes. At the bottom there is a plate of pho noodle soup. It shows white plate, light yellow noodles and flat white noodles. In the bottom left corner there is a plate of vietnamese pork ham. It shows sliced raw meat, grilled meatballs and green leafy vegetables. In the center there is a plate of sliced beef. It shows reddish-brown meat slices, white fat marbling and white eggs. It is arranged on a plate. The fresh herbs and greens is to the left of the hotpot.</sub>

**[B]** (135 từ, 34/40 chi tiết)

> Ở góc trên bên trái có một đĩa lớn rau sống. Nó cho thấy trứng trắng, lá xanh và trứng trắng. Nó được đặt cùng nhau gọn gàng. Ở góc trên bên phải có một nồi lẩu. Nó cho thấy nước dùng màu nâu trong, vỏ cà chua đỏ và cà chua thái lát. Nó nổi trên bề mặt. Ở phía dưới có một bát phở. Nó cho thấy mì màu vàng nhạt, đĩa trắng và mì trắng dẹt. Nó được đặt trên đĩa trắng. Ở góc dưới bên trái có một đĩa chả giò. Nó cho thấy thịt thái lát màu hồng, các món chiên màu nâu và thịt hồng thái lát. Nó được đặt trên đĩa trắng. Ở giữa có một phần thịt bò. Nó cho thấy thịt thái lát màu nâu đỏ, vân mỡ trắng và mì.

<sub>EN: In the top left corner there is a large plate of fresh herbs and greens. It shows white eggs, green leaves and white eggs. It is placed together neatly. In the top right corner there is a pot of hotpot. It shows clear brown broth, red tomato skin and sliced tomatoes. It is floated on surface. At the bottom there is a bowl of pho noodle soup. It shows pale yellow noodles, white plate and flat white noodles. It is placed on white plate. In the bottom left corner there is a plate of vietnamese pork ham. It shows pink sliced meat, brown fried items and sliced pink meat. It is placed on white plate. In the center there is a serving of sliced beef. It shows reddish-brown sliced meat, white fat marbling and noodles.</sub>

**[C]** (136 từ, 40/50 chi tiết)

> Ở góc trên bên trái có một đĩa lớn rau sống. Nó cho thấy các loại rau xanh, nấm kim châm trắng và các loại rau xanh. Nó được sắp xếp thành một đống. Ở góc trên bên phải có một nồi lẩu. Nó cho thấy nước dùng màu nâu trong, ớt đỏ và hành lá thái lát. Nó đang nổi trong nước dùng. Ở phía dưới có một đĩa phở. Nó cho thấy mì màu vàng nhạt, đĩa trắng và thịt màu hồng. Nó được chất đống trên đĩa. Ở góc dưới bên trái có một đĩa chả giò. Nó cho thấy thịt màu hồng nhạt, thịt viên màu nâu và thảo mộc xanh. Nó được sắp xếp thành các hàng. Ở giữa có một đĩa thịt bò. Nó cho thấy các lát thịt màu nâu đỏ, vân mỡ trắng và thịt thái lát.

<sub>EN: In the top left corner there is a large plate of fresh herbs and greens. It shows green leafy vegetables, white enoki mushrooms and green leafy vegetables. It is arranged in a pile. In the top right corner there is a pot of hotpot. It shows clear brown broth, red chili peppers and sliced green onions. It is floating in broth. At the bottom there is a plate of pho noodle soup. It shows pale yellow noodles, white plate and pink meat. It is piled on plate. In the bottom left corner there is a plate of vietnamese pork ham. It shows light pink meat, brown meatballs and green herbs. It is arranged in rows. In the center there is a plate of sliced beef. It shows reddish-brown meat slices, white fat marbling and sliced meat.</sub>

## `srcA_H-055_jpg.rf.f273f108c4a6c72344454413a0714600.jpg`

Món (nhãn): fresh spring rolls, fried spring rolls, mini crispy pancakes, other dish, pho noodle soup, roast pork, sizzling crepe, stir-fried vegetables

**[A]** (138 từ, 42/48 chi tiết)

> Ở bên trái có một bát heo quay. Nó cho thấy lát chanh vàng, thịt lợn thái lát và lát chanh. Đó là thịt lợn thái lát được xếp ở phía trên. Ở bên phải có một đĩa nem rán. Nó cho thấy các cuộn màu nâu vàng, thảo mộc xanh và đĩa trắng. Nó được sắp xếp trên một chiếc đĩa. Ở giữa có một đĩa rau xào. Nó cho thấy rau xanh, tỏi phi vàng và rau lá xanh. Nó được trộn với tỏi phi. Ở phía trên có một phần món ăn khác. Ở góc trên bên trái và ở phía dưới có hai bát phở. Chúng cho thấy nước dùng màu nâu trong, thảo mộc xanh và mì trắng. Ở góc trên bên phải có một miếng bánh xèo. Nó cho thấy bánh xèo màu vàng kim, lá xanh và bánh xèo gấp lại.

<sub>EN: On the left there is a bowl of roast pork. It shows yellow lime wedge, sliced pork and lime wedge. It is sliced pork arranged on top. On the right there is a plate of fried spring rolls. It shows golden-brown rolls, green herbs and white plate. It is arranged on a plate. In the center there is a plate of stir-fried vegetables. It shows green vegetables, golden fried garlic and green leafy vegetables. It is mixed with fried garlic. At the top there is a serving of other dish. In the top left corner and at the bottom there are two bowls of pho noodle soup. They show clear brown broth, green herbs and white noodles. In the top right corner there is a piece of sizzling crepe. It shows golden-yellow crepe, green leaf and folded crepe.</sub>

**[B]** (139 từ, 36/43 chi tiết)

> Ở bên trái có một bát heo quay. Nó cho thấy xà lách xanh, một miếng chanh vàng và các lát ớt đỏ. Nó được cắt thành những lát dày. Ở bên phải có một đĩa nem rán. Nó cho thấy các cuộn màu nâu vàng, lá trang trí màu xanh và các cuộn màu nâu vàng. Ở giữa có một đĩa rau xào. Nó cho thấy các loại rau bóng loáng màu xanh, tỏi băm trắng và các loại rau dài màu xanh. Ở phía trên có một phần món ăn khác. Ở góc trên bên trái và ở phía dưới có hai bát phở. Chúng cho thấy nước dùng trong, thảo mộc xanh và các lát thịt mỏng. Chúng được đặt trong nước dùng. Ở góc trên bên phải có một khay tre bánh xèo. Nó cho thấy bánh crepe màu vàng kim, lá trang trí màu xanh và bánh crepe mỏng được gấp lại.

<sub>EN: On the left there is a bowl of roast pork. It shows green lettuce, yellow lime wedge and red chili slices. It is cut into thick slices. On the right there is a plate of fried spring rolls. It shows golden brown rolls, green garnish leaves and golden brown rolls. In the center there is a plate of stir-fried vegetables. It shows green glossy vegetables, white chopped garlic and long green vegetables. At the top there is a serving of other dish. In the top left corner and at the bottom there are two bowls of pho noodle soup. They show clear broth, green herbs and thin meat slices. They are placed in broth. In the top right corner there is a bamboo tray of sizzling crepe. It shows golden yellow crepe, green leafy garnish and folded thin crepe.</sub>

**[C]** (138 từ, 54/64 chi tiết)

> Ở bên trái có một bát heo quay. Nó cho thấy xà lách xanh, chanh xanh nhạt và thịt thái lát. Nó được sắp xếp trong một chiếc bát. Ở bên phải có một đĩa nem rán. Nó cho thấy các cuộn màu nâu vàng, rau mùi xanh và ớt đỏ thái lát. Nó được sắp xếp trên một chiếc đĩa. Ở giữa có một đĩa rau xào. Nó cho thấy rau xanh tươi, tỏi vàng và các mẩu tỏi chiên. Nó được rắc tỏi lên trên. Ở phía trên có một phần món ăn khác. Ở góc trên bên trái và ở phía dưới có hai bát phở. Chúng cho thấy nước dùng trong, rau thơm xanh và thịt nâu. Chúng được phủ lên trên bằng rau thơm và hành lá. Ở góc trên bên phải có một miếng bánh xèo.

<sub>EN: On the left there is a bowl of roast pork. It shows green lettuce, light green lime and sliced meat. It is arranged in a bowl. On the right there is a plate of fried spring rolls. It shows golden-brown rolls, green cilantro and red chili slices. It is arranged on a plate. In the center there is a plate of stir-fried vegetables. It shows bright green vegetables, golden brown garlic and fried garlic bits. It is scattered with garlic on top. At the top there is a serving of other dish. In the top left corner and at the bottom there are two bowls of pho noodle soup. They show clear broth, green herbs and brown meat. They are topped with herbs and green onions. In the top right corner there is a piece of sizzling crepe.</sub>

## `srcA_H-056_jpg.rf.f997bd3ec2b4386711e5dc36a9f548bb.jpg`

Món (nhãn): mini crispy pancakes, sizzling crepe

**[A]** (92 từ, 17/22 chi tiết)

> Ở bên phải có một miếng bánh xèo. Nó cho thấy bánh crepe vàng, lá xanh, lá xanh và bát trắng nhỏ. Nó được xếp chồng lên lá. Ở giữa có một phần bánh khọt. Nó cho thấy bánh pancake vàng, sốt cam, bánh tròn nhỏ, thảo mộc xanh và nhân trắng. Nó được đóng gói sát nhau. bánh xèo nằm ở bên phải của bánh khọt. Các món ăn được đặt trên một chiếc bàn gỗ tối màu. Cũng có thể thấy: thìa kim loại và túi nilon. Phông nền cho thấy nội thất nhà hàng bị làm mờ.

<sub>EN: On the right there is a piece of sizzling crepe. It shows yellow crepe, green leaf, green leaf and small white bowl. It is stacked on leaf. In the center there is a serving of mini crispy pancakes. It shows yellow pancakes, orange sauce, small round cakes, green herbs and white filling. It is packed closely together. The sizzling crepe is to the right of the mini crispy pancakes. The dishes are set on a dark wooden table. Also visible: metal spoon and plastic bags. The background shows a blurred restaurant interior.</sub>

**[B]** (101 từ, 16/19 chi tiết)

> Ở bên phải có một phần bánh xèo. Nó cho thấy bánh crepe mỏng màu vàng, rau lá xanh, rau lá xanh và món ăn kèm tròn nhỏ. Nó được xếp chồng lên trên. Ở giữa có một phần bánh khọt. Nó cho thấy bánh tròn màu vàng, rau trang trí lá xanh, bánh tròn màu vàng và rau trang trí lá xanh. Chúng được đóng gói sát nhau. bánh xèo nằm ở bên phải của bánh khọt. Các món ăn được đặt trên một chiếc bàn gỗ tối màu. Cũng có thể thấy: thìa kim loại, túi nhựa, bát trắng và đĩa xanh. Phông nền cho thấy nội thất nhà hàng bị làm mờ.

<sub>EN: On the right there is a piece of sizzling crepe. It shows yellow thin crepe, green leafy vegetable, green leafy vegetable and small round side dish. It is stacked on top. In the center there is a serving of mini crispy pancakes. It shows yellow round cakes, green leafy garnish, round yellow cakes and green leafy garnish. It is packed closely together. The sizzling crepe is to the right of the mini crispy pancakes. The dishes are set on a dark wooden table. Also visible: metal spoon, plastic bags, white bowls and green plate. The background shows a blurred restaurant interior.</sub>

**[C]** (111 từ, 21/27 chi tiết)

> Ở bên phải có một khay bánh xèo. Nó cho thấy bánh crepe màu vàng, thảo mộc xanh, bánh crepe màu vàng, thảo mộc xanh và bát trắng. Nó được xếp chồng và gấp lại. Ở giữa có một khay bánh khọt. Nó cho thấy bánh màu vàng đậm, bánh tròn nhỏ, đồ trang trí lá xanh, vật phẩm gấp màu vàng và bát nhỏ với chất lỏng. Nó được đóng gói sát nhau. bánh xèo nằm ở bên phải của bánh khọt. Các món ăn được đặt trên một chiếc bàn gỗ tối màu. Cũng có thể thấy: đũa đỏ và trắng, thìa kim loại, ấm trà gốm trắng, bát trắng nhỏ, đĩa lá chuối xanh và giấy bọc nhựa. Phông nền cho thấy nội thất nhà hàng bị làm mờ.

<sub>EN: On the right there is a tray of sizzling crepe. It shows yellow crepes, green herbs, yellow crepes, green herbs and white bowl. It is stacked and folded. In the center there is a tray of mini crispy pancakes. It shows deep-yellow cakes, small round cakes, green leafy garnish, yellow folded item and small bowl with liquid. It is packed closely together. The sizzling crepe is to the right of the mini crispy pancakes. The dishes are set on a dark wooden table. Also visible: red and white chopsticks, metal spoon, white ceramic teapots, small white bowls, green banana leaf plate and plastic-wrapped paper. The background shows a blurred restaurant interior.</sub>

## `srcA_H-057_jpg.rf.a89b838b13e83e2b7719faa06395ceb5.jpg`

Món (nhãn): fresh herbs and greens, other dish, roast pork, roasted chicken, sliced beef

**[A]** (132 từ, 31/34 chi tiết)

> Ở bên phải có một khay gà quay. Nó cho thấy hộp nhựa trong suốt, da gà màu nâu vàng và các miếng thịt gà. Nó được sắp xếp thành các hàng. Ở giữa có một phần heo quay. Nó cho thấy thịt màu nâu đỏ, giá đỗ trắng và nước sốt màu nâu đậm. Đó là thịt thái lát xếp cao. Ở góc trên bên phải và góc dưới bên trái có hai phần món ăn khác. Ở bên trái có một đĩa rau sống. Nó cho thấy rau xanh đậm, giá đỗ trắng và bàn gỗ màu nâu nhạt. Nó được đặt trong khay đen. Ở phía dưới có một phần thịt bò. Nó cho thấy các lát thịt màu nâu đỏ, rau xanh và khay trắng. Nó được đặt cạnh nhau.

<sub>EN: On the right there is a tray of roasted chicken. It shows clear plastic container, golden brown chicken skin and chicken pieces. It is arranged in rows. In the center there is a serving of roast pork. It shows reddish-brown meat, white bean sprouts and dark brown sauce. It is sliced meat piled high. In the top right corner and in the bottom left corner there are two servings of other dish. On the left there is a plate of fresh herbs and greens. It shows dark green leafy greens, white bean sprouts and light brown wooden table. It is placed in black tray. At the bottom there is a serving of sliced beef. It shows reddish brown meat slices, green leafy vegetables and white tray. It is placed side by side.</sub>

**[B]** (134 từ, 22/28 chi tiết)

> Ở bên phải có một phần gà quay. Nó cho thấy da gà màu nâu đỏ, các miếng gà và rau xanh. Nó được xếp thành từng lớp. Ở giữa có một phần heo quay. Nó cho thấy phần thịt băm bên trên và sợi mì trắng thái nhỏ. Nó được cắt thành những lát dày. Ở góc trên bên phải và góc dưới bên trái có hai phần món ăn khác. Ở bên trái có một khay rau sống. Nó cho thấy rau xanh, giá đỗ trắng và rau xanh. Nó được đặt trên khay. Ở phía dưới có một phần thịt bò. Nó cho thấy các lát thịt màu nâu đỏ, rau trang trí xanh và lá xanh. Nó được đặt ở phía trên. gà quay nằm ở bên phải của heo quay.

<sub>EN: On the right there is a serving of roasted chicken. It shows reddish-brown chicken skin, chicken pieces and green vegetables. It is stacked in layers. In the center there is a serving of roast pork. It shows minced meat topping and shredded white noodles. It is cut into thick slices. In the top right corner and in the bottom left corner there are two servings of other dish. On the left there is a tray of fresh herbs and greens. It shows green leafy vegetables, white bean sprouts and green leafy vegetables. It is placed on tray. At the bottom there is a serving of sliced beef. It shows reddish-brown meat slices, green leafy garnish and green leaves. It is placed on top. The roasted chicken is to the right of the roast pork.</sub>

**[C]** (139 từ, 37/39 chi tiết)

> Ở bên phải có một khay gà quay. Nó cho thấy da màu nâu đỏ, lá màu xanh đậm và các miếng thịt gà. Nó được sắp xếp thành các hàng. Ở giữa có một phần heo quay. Nó cho thấy thịt màu nâu đỏ, thịt màu nâu nhạt và giá đỗ trắng. Nó được sắp xếp thành các lớp. Ở góc trên bên phải và góc dưới bên trái có hai phần món ăn khác. Ở bên trái có một khay rau sống. Nó cho thấy rau xanh, giá đỗ trắng và thực phẩm thái lát màu nâu nhạt. Nó được sắp xếp thành các lớp. Ở phía dưới có một khay thịt bò. Nó cho thấy thịt màu nâu đỏ, vân mỡ trắng và rau xanh. Nó được sắp xếp với rau xanh ở trên cùng. gà quay nằm ở bên phải của heo quay.

<sub>EN: On the right there is a tray of roasted chicken. It shows reddish-brown skin, dark green leaf and chicken pieces. It is arranged in rows. In the center there is a serving of roast pork. It shows reddish-brown meat, light brown meat and white bean sprouts. It is arranged in layers. In the top right corner and in the bottom left corner there are two servings of other dish. On the left there is a tray of fresh herbs and greens. It shows green leafy vegetables, white bean sprouts and light brown sliced food. It is arranged in layers. At the bottom there is a tray of sliced beef. It shows reddish-brown meat, white fat marbling and green leafy vegetables. It is arranged with leafy greens on top. The roasted chicken is to the right of the roast pork.</sub>

## `srcA_H-058_jpg.rf.75fb94eb91407b97c4f210a2cdbaa9c7.jpg`

Món (nhãn): fresh herbs and greens, fried spring rolls, grilled pork noodle bowl, rice vermicelli

**[A]** (132 từ, 23/27 chi tiết)

> Ở góc trên bên trái có một đĩa rau sống. Nó cho thấy lá xanh và lá xanh. Bên kia bàn có ba bát bún thịt nướng. Chúng cho thấy nước dùng màu nâu đậm, thịt màu nâu nhạt và rau trang trí màu xanh. Ở góc trên bên phải và bên trái có hai phần bún tươi. Chúng cho thấy mì trắng, bàn màu nâu nhạt và mì trắng. Ở giữa có một đĩa nem rán. Nó cho thấy các miếng chiên màu nâu vàng, đĩa trắng và các miếng chiên. Nó được sắp xếp trên một chiếc đĩa. rau sống ở phía trên bún thịt nướng. bún thịt nướng ở bên phải của bún tươi. Các món ăn được đặt trên một chiếc bàn gỗ sáng màu.

<sub>EN: In the top left corner there is a plate of fresh herbs and greens. It shows green leaves and green leaves. Across the table there are three bowls of grilled pork noodle bowl. They show dark brown broth, light brown meat and green leafy garnish. In the top right corner and on the left there are two servings of rice vermicelli. They show white noodles, light brown table and white noodles. In the center there is a plate of fried spring rolls. It shows golden-brown fried pieces, white plate and fried pieces. It is arranged on a plate. The fresh herbs and greens is above the grilled pork noodle bowl. The grilled pork noodle bowl are to the right of the rice vermicelli. The dishes are set on a light wooden table.</sub>

**[B]** (131 từ, 22/28 chi tiết)

> Ở góc trên bên trái có một đĩa rau sống. Nó cho thấy rau xanh, nước dùng màu nâu và rau xanh. Nó được đặt trên các đĩa riêng biệt. Bên kia bàn có ba bát bún thịt nướng. Chúng cho thấy thịt màu nâu đậm, rong biển xanh và các miếng thịt. Chúng được đặt trong nước dùng. Ở góc trên bên phải và bên trái có hai phần bún tươi. Chúng cho thấy những sợi trắng mỏng, những sợi trắng mỏng và nhãn chữ màu đỏ. Chúng được xếp chồng lỏng lẻo với nhau. Ở giữa có một đĩa nem rán. Nó cho thấy các miếng màu nâu vàng, các miếng đồ chiên và lá xà lách xanh. Nó được đặt trên đĩa. rau sống ở phía trên bún thịt nướng.

<sub>EN: In the top left corner there is a plate of fresh herbs and greens. It shows green leafy vegetables, brown broth and green leafy vegetables. It is placed on separate plates. Across the table there are three bowls of grilled pork noodle bowl. They show dark brown meat, green seaweed and meat pieces. They are placed in broth. In the top right corner and on the left there are two servings of rice vermicelli. They show white thin strands, white thin strands and red text label. They are piled loosely together. In the center there is a plate of fried spring rolls. It shows golden brown pieces, fried food pieces and green lettuce leaves. It is placed on plate. The fresh herbs and greens is above the grilled pork noodle bowl.</sub>

**[C]** (133 từ, 34/38 chi tiết)

> Ở góc trên bên trái có một đĩa rau sống. Nó cho thấy các loại thảo mộc lá xanh, thịt nâu trong bát và các loại thảo mộc lá xanh. Nó được sắp xếp trên một chiếc đĩa. Bên kia bàn có ba bát bún thịt nướng. Chúng cho thấy thịt nâu đậm, rong biển xanh và cà rốt cam. Chúng được đặt trong nước dùng. Ở góc trên bên phải và bên trái có hai phần bún tươi. Chúng cho thấy mì trắng, bề mặt bàn màu nâu nhạt và mì sợi trắng. Chúng được xếp lỏng lẻo trên đĩa. Ở giữa có một đĩa nem rán. Nó cho thấy các miếng chiên màu nâu vàng, đĩa trắng và rau lá xanh. Nó được xếp chồng lên đĩa. rau sống nằm phía trên bún thịt nướng.

<sub>EN: In the top left corner there is a plate of fresh herbs and greens. It shows green leafy herbs, brown meat in bowl and green leafy herbs. It is arranged on a plate. Across the table there are three bowls of grilled pork noodle bowl. They show dark brown meat, green seaweed and orange carrot. They are placed in broth. In the top right corner and on the left there are two servings of rice vermicelli. They show white noodles, light brown table surface and white thin noodles. They are piled loosely on plate. In the center there is a plate of fried spring rolls. It shows golden-brown fried pieces, white plate and green leafy vegetable. It is stacked on plate. The fresh herbs and greens is above the grilled pork noodle bowl.</sub>

## `srcA_H-059_jpg.rf.3128112cdb6a77ead07b57a03f81ffb3.jpg`

Món (nhãn): dipping sauce, fresh herbs and greens, fried spring rolls, grilled pork noodle bowl, rice vermicelli

**[A]** (136 từ, 26/28 chi tiết)

> Ở phía dưới có một đĩa lớn rau sống. Nó cho thấy lá xanh, lá tím và lá xanh. Bên kia bàn có ba bát bún thịt nướng. Chúng cho thấy vành bát màu trắng, thịt màu nâu đậm và các miếng thịt. Ở góc trên bên phải có một đĩa nem rán. Nó cho thấy các cuốn chiên màu nâu vàng, vành đĩa màu trắng và các cuốn chiên. Nó được sắp xếp trên một chiếc đĩa. Ở góc trên bên trái có một đĩa bún tươi. Nó cho thấy mì trắng, nước dùng màu nâu nhạt và mì trắng. Ở góc trên bên trái có một bát nhỏ đồ chấm. Nó cho thấy nước dùng trong, bát trắng và củ cải trắng thái lát. rau sống nằm ở bên phải của bún thịt nướng.

<sub>EN: At the bottom there is a large plate of fresh herbs and greens. It shows green leaves, purple leaves and green leaves. Across the table there are three bowls of grilled pork noodle bowl. They show white bowl rim, dark brown meat and chunks of meat. In the top right corner there is a plate of fried spring rolls. It shows golden-brown fried rolls, white plate rim and fried rolls. It is arranged on a plate. In the top left corner there is a plate of rice vermicelli. It shows white noodles, light brown broth and white noodles. In the top left corner there is a small bowl of dipping sauce. It shows clear broth, white bowl and sliced white radish. The fresh herbs and greens is to the right of the grilled pork noodle bowl.</sub>

**[B]** (131 từ, 30/37 chi tiết)

> Ở phía dưới có một đĩa lớn rau sống. Nó cho thấy rau lá xanh, rau lá tím và rau lá xanh. Chúng được trộn lẫn với nhau một cách lỏng lẻo. Băng qua bàn có ba bát bún thịt nướng. Chúng cho thấy thịt màu nâu đậm, thịt nướng miếng và rau trang trí xanh. Chúng được đặt ở giữa. Ở góc trên bên phải có một phần nem rán. Nó cho thấy các món chiên màu nâu vàng, ớt đỏ và các miếng thức ăn chiên. Nó được đặt trên đĩa trắng. Ở góc trên bên trái có một đĩa bún tươi. Nó cho thấy bún trắng, nước sốt nâu và bún trắng. Nó được đặt trong các hộp riêng biệt. Ở góc trên bên trái có một bát đồ chấm.

<sub>EN: At the bottom there is a large plate of fresh herbs and greens. It shows green leafy vegetables, purple leafy vegetables and green leafy vegetables. It is mixed together loosely. Across the table there are three bowls of grilled pork noodle bowl. They show dark brown meat, grilled meat chunks and green garnish. They are placed in center. In the top right corner there is a serving of fried spring rolls. It shows golden brown fried items, red chili peppers and fried food pieces. It is placed on white plate. In the top left corner there is a plate of rice vermicelli. It shows white rice noodles, brown sauce and white rice noodles. It is placed on separate containers. In the top left corner there is a bowl of dipping sauce.</sub>

**[C]** (136 từ, 47/48 chi tiết)

> Ở phía dưới có một đĩa lớn rau sống. Nó cho thấy các loại thảo mộc lá xanh, lá màu tím và xà lách xanh nhạt. Chúng được trộn lẫn với nhau trên đĩa. Bên kia bàn có ba bát bún thịt nướng. Chúng cho thấy thịt màu nâu đậm, nước dùng màu nâu nhạt và bát màu trắng. Chúng được sắp xếp trong bát. Ở góc trên bên phải có một đĩa nem rán. Nó cho thấy các cuộn màu nâu vàng, nước sốt màu nâu đậm và ớt đỏ. Nó được xếp chồng lên trên đĩa. Ở góc trên bên trái có một đĩa bún tươi. Nó cho thấy mì trắng, nước dùng màu nâu và nước dùng màu vàng nhạt. Nó được đặt riêng biệt trên đĩa. Ở góc trên bên trái có một bát đồ chấm. Nó cho thấy các miếng màu vàng nhạt, lát cam và bát màu trắng.

<sub>EN: At the bottom there is a large plate of fresh herbs and greens. It shows green leafy herbs, purple leaves and light green lettuce. It is mixed together on plate. Across the table there are three bowls of grilled pork noodle bowl. They show dark-brown meat, light brown broth and white bowl. They are arranged in a bowl. In the top right corner there is a plate of fried spring rolls. It shows golden-brown rolls, dark brown sauce and red chili peppers. It is stacked on plate. In the top left corner there is a plate of rice vermicelli. It shows white noodles, brown broth and yellowish broth. It is separately placed on plate. In the top left corner there is a bowl of dipping sauce. It shows pale yellow pieces, orange slices and white bowl.</sub>

## `srcA_H-060_jpg.rf.ca5bcfe42edf39cd81fc095f699a59a3.jpg`

Món (nhãn): dipping sauce, fried rice, hotpot, other dish, roast pork, stir-fried vegetables

**[A]** (136 từ, 31/33 chi tiết)

> Ở giữa có một nồi lẩu. Nó cho thấy nước dùng màu cam, thảo mộc xanh và thảo mộc xanh. Ở góc trên bên trái có một phần món ăn khác. Ở góc dưới bên phải có một phần heo quay. Nó cho thấy thịt màu nâu đỏ, rau mùi xanh và bàn gỗ sáng màu. Đó là thịt thái lát được sắp xếp trên đĩa. Ở góc trên bên phải và ở phía dưới có hai phần cơm chiên. Chúng cho thấy đống cơm màu nâu đậm, đồ trang trí lá xanh và các miếng ớt đỏ. Chúng được vun ở giữa, trang trí ở các bên. Ở phía trên có một đĩa rau xào. Nó cho thấy rau xanh, nước sốt màu nâu nhạt và các mảnh nhỏ màu đỏ. Chúng được trộn lẫn với nhau. Ở góc trên bên trái và ở giữa có hai bát nhỏ đồ chấm.

<sub>EN: In the center there is a pot of hotpot. It shows orange broth, green herbs and green herbs. In the top left corner there is a serving of other dish. In the bottom right corner there is a serving of roast pork. It shows reddish-brown meat, green cilantro and light wooden table. It is sliced meat arranged on plate. In the top right corner and at the bottom there are two servings of fried rice. They show dark brown rice mound, green leaf garnish and red chili pieces. They are mounded center, garnished sides. At the top there is a plate of stir-fried vegetables. It shows green vegetables, light brown sauce and small red pieces. It is mixed together. In the top left corner and in the center there are two small bowls of dipping sauce.</sub>

**[B]** (137 từ, 29/36 chi tiết)

> Ở giữa có một nồi lẩu. Nó cho thấy nước dùng màu đỏ, các loại thảo mộc lá xanh và rau xanh. Nó được đặt ở giữa. Ở góc trên bên trái có một phần món ăn khác. Ở góc dưới bên phải có một phần heo quay. Nó cho thấy các lát thịt màu nâu đỏ, lá ngò xanh và bún trắng. Ở góc trên bên phải và ở phía dưới có hai phần cơm chiên. Chúng cho thấy gạo màu nâu đậm, đồ trang trí lá xanh và viên gạo nâu. Chúng được tạo hình thành đống. Ở phía trên có một đĩa rau xào. Nó cho thấy các phần lá xanh, dầu màu vàng và rau xanh thái nhỏ. Ở góc trên bên trái và ở giữa có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ.

<sub>EN: In the center there is a pot of hotpot. It shows red broth liquid, green leafy herbs and leafy green herbs. It is placed in center. In the top left corner there is a serving of other dish. In the bottom right corner there is a serving of roast pork. It shows reddish-brown meat slices, green cilantro leaves and white rice noodles. In the top right corner and at the bottom there are two servings of fried rice. They show dark brown rice, green leaf garnish and brown rice ball. They are shaped into mound. At the top there is a plate of stir-fried vegetables. It shows green leafy parts, yellowish oil and chopped green vegetables. In the top left corner and in the center there are two small bowls of dipping sauce. They show reddish-brown liquid.</sub>

**[C]** (139 từ, 47/49 chi tiết)

> Ở giữa có một nồi lẩu. Nó cho thấy nước dùng màu đỏ cam, thảo mộc xanh và những miếng màu trắng. Nó được trang trí với thảo mộc xanh. Ở góc trên bên trái có một phần món ăn khác. Ở góc dưới bên phải có một khay heo quay. Nó cho thấy thịt màu nâu đỏ, thảo mộc xanh và nước sốt sẫm màu. Nó được sắp xếp trong một chiếc khay. Ở góc trên bên phải và ở phía dưới có hai phần cơm chiên. Chúng cho thấy cơm màu xám đậm, ớt đỏ và những lát dưa chuột xanh. Chúng được sắp xếp xung quanh một đống ở giữa. Ở phía trên có một bát rau xào. Nó cho thấy rau xanh, chất lỏng màu nâu và những đốm đỏ. Nó được cắt thành từng miếng. Ở góc trên bên trái và ở giữa có hai bát nhỏ đồ chấm.

<sub>EN: In the center there is a pot of hotpot. It shows orange-red broth, green herbs and white chunks. It is garnished with green herbs. In the top left corner there is a serving of other dish. In the bottom right corner there is a tray of roast pork. It shows reddish-brown meat, green herb and dark sauce. It is arranged in a tray. In the top right corner and at the bottom there are two servings of fried rice. They show dark gray rice, red chili peppers and green cucumber slices. They are arranged around a central mound. At the top there is a bowl of stir-fried vegetables. It shows green vegetables, brownish liquid and red specks. It is cut into pieces. In the top left corner and in the center there are two small bowls of dipping sauce.</sub>

## `srcA_H-061_jpeg.rf.f092b7e45120195bd76fed8db8bceea9.jpg`

Món (nhãn): clear vegetable soup, other dish, shredded salad, shrimp, squid, stir-fried vegetables

**[A]** (132 từ, 35/36 chi tiết)

> Ở góc trên bên phải và ở góc dưới bên trái có hai phần món ăn khác. Ở bên phải và ở phía dưới có hai bát canh. Chúng cho thấy nước dùng đỏ, sủi cảo trắng và rau xanh. Ở góc trên bên trái có một đĩa mực. Nó cho thấy nước sốt đỏ sẫm, thịt nâu nhạt và các miếng thịt đã nấu chín. Nó được phục vụ trên đĩa hình chữ nhật. Ở phía trên có một đĩa tôm. Nó cho thấy nước sốt đỏ, xà lách xanh và rau xà lách. Nó được sắp xếp trên lớp xà lách. Ở bên trái có một đĩa gỏi. Nó cho thấy rau củ bào sợi màu cam, đĩa trắng và rau củ bào sợi màu cam. Nó được đặt trên một chiếc đĩa trắng. Ở giữa có một bát rau xào.

<sub>EN: In the top right corner and in the bottom left corner there are two servings of other dish. On the right and at the bottom there are two bowls of clear vegetable soup. They show red broth, white dumplings and green vegetables. In the top left corner there is a plate of squid. It shows dark red sauce, light brown meat and cooked meat pieces. It is served on rectangular plate. At the top there is a plate of shrimp. It shows red sauce, green lettuce and lettuce. It is arranged on lettuce bed. On the left there is a plate of shredded salad. It shows orange shredded vegetables, white plate and shredded orange vegetables. It is placed on a white plate. In the center there is a bowl of stir-fried vegetables.</sub>

**[B]** (134 từ, 30/35 chi tiết)

> Ở góc trên bên phải và ở góc dưới bên trái có hai phần món ăn khác. Ở bên phải và ở phía dưới có hai bát canh. Chúng cho thấy các miếng cà chua đỏ, các viên tròn màu trắng và các miếng cà chua đỏ. Chúng được đặt trong nước dùng. Ở góc trên bên trái có một đĩa mực. Nó cho thấy rau lá xanh, các xúc tu xoăn và nước sốt chấm. Ở phía trên có một đĩa tôm. Nó cho thấy các lá xà lách xanh, các lá xà lách xanh và thìa kim loại. Nó được đặt trên đĩa trắng. Ở bên trái có một đĩa gỏi. Nó cho thấy các sợi bào màu vàng kim, các miếng nấu chín màu trắng và các sợi bào màu vàng. Nó được trộn lẫn với nhau không đều. Ở giữa có một bát rau xào.

<sub>EN: In the top right corner and in the bottom left corner there are two servings of other dish. On the right and at the bottom there are two bowls of clear vegetable soup. They show red tomato pieces, white round balls and red tomato pieces. They are placed in broth. In the top left corner there is a plate of squid. It shows green leafy vegetable, curled tentacles and dip sauce. At the top there is a plate of shrimp. It shows green lettuce leaves, green lettuce leaves and metal spoon. It is placed on white plate. On the left there is a plate of shredded salad. It shows golden shredded strands, white cooked pieces and shredded yellow strands. It is mixed together unevenly. In the center there is a bowl of stir-fried vegetables.</sub>

**[C]** (135 từ, 44/48 chi tiết)

> Ở góc trên bên phải và ở góc dưới bên trái có hai phần món ăn khác. Ở bên phải và ở phía dưới có hai bát canh. Chúng cho thấy nước dùng đỏ, các miếng tròn màu trắng và các khối màu cam. Chúng nằm rải rác trong nước dùng. Ở góc trên bên trái có một đĩa mực. Nó cho thấy thịt màu nâu, thảo mộc xanh và nước sốt đỏ sẫm. Nó được sắp xếp trên đĩa trắng. Ở phía trên có một đĩa tôm. Nó cho thấy xà lách xanh, nước sốt đỏ và xà lách. Nó được sắp xếp trên một lớp xà lách. Ở bên trái có một đĩa gỏi. Nó cho thấy rau thái sợi màu cam, đĩa trắng và thìa kim loại. Nó nằm rải rác trên đĩa. Ở giữa có một bát rau xào.

<sub>EN: In the top right corner and in the bottom left corner there are two servings of other dish. On the right and at the bottom there are two bowls of clear vegetable soup. They show red broth, white round pieces and orange cubes. They are scattered in broth. In the top left corner there is a plate of squid. It shows brown meat, green herbs and dark red sauce. It is arranged on white plate. At the top there is a plate of shrimp. It shows green lettuce, red sauce and lettuce. It is arranged on a bed of lettuce. On the left there is a plate of shredded salad. It shows orange shredded vegetables, white plate and metal spoon. It is scattered on plate. In the center there is a bowl of stir-fried vegetables.</sub>

## `srcA_H-062_jpg.rf.c5f656b07561d51b7dc9dcd4a52139a3.jpg`

Món (nhãn): boiled vegetables, clear vegetable soup, fried fish, other dish, stir-fried vegetables

**[A]** (129 từ, 21/27 chi tiết)

> Ở bên trái và ở phía dưới có hai phần món ăn khác. Ở góc trên bên trái có một đĩa cá chiên. Nó cho thấy nước dùng màu nâu trong, thảo mộc xanh và cá nguyên con. Ở phía trên có hai phần rau xào. Chúng cho thấy rau xanh, ngô vàng và đĩa trắng. Chúng được trộn lẫn với nhau. Ở bên phải có một bát canh. Nó cho thấy nước dùng màu vàng nhạt, bát trắng và đũa đen. Ở bên phải có một đĩa rau luộc. Nó cho thấy rau và thìa. Các món ăn khác nằm bên dưới các cá chiên. cá chiên nằm ở bên trái của rau xào. Các món ăn được đặt trên một chiếc khăn trải bàn màu đỏ. Cũng có thể nhìn thấy: thìa kim loại và điện thoại di động.

<sub>EN: On the left and at the bottom there are two servings of other dish. In the top left corner there is a plate of fried fish. It shows clear brown broth, green herbs and whole fish. At the top there are two servings of stir-fried vegetables. They show green vegetables, yellow corn and white plate. They are mixed together. On the right there is a bowl of clear vegetable soup. It shows light yellow broth, white bowl and black chopsticks. On the right there is a plate of boiled vegetables. It shows vegetables and spoon. The other dish are below the fried fish. The fried fish is to the left of the stir-fried vegetables. The dishes are set on a red tablecloth. Also visible: metal spoon and mobile phone.</sub>

**[B]** (140 từ, 22/29 chi tiết)

> Ở bên trái và ở phía dưới có hai phần món ăn khác. Ở góc trên bên trái có một phần cá chiên. Nó cho thấy thìa kim loại màu bạc, thịt cá màu trắng và thân cá nguyên con. Nó được đặt trên đĩa trắng. Ở phía trên có hai phần rau xào. Chúng cho thấy đậu hà lan xanh, ngô vàng và đậu hà lan xanh. Chúng được trộn đều với nhau. Ở bên phải có một bát canh. Nó cho thấy nước dùng màu xanh trong, bát trắng và các nguyên liệu thái nhỏ. Nó được đặt trên bàn. Ở bên phải có một bát rau luộc. Nó cho thấy rau màu xanh đậm và thìa kim loại. Các món ăn khác nằm bên dưới các cá chiên. cá chiên nằm ở bên trái của rau xào. Các món ăn được đặt trên khăn trải bàn có hoa văn màu đỏ.

<sub>EN: On the left and at the bottom there are two servings of other dish. In the top left corner there is a serving of fried fish. It shows silver metal spoon, white fish flesh and whole fish body. It is placed on white plate. At the top there are two servings of stir-fried vegetables. They show green peas, yellow corn and green peas. They are mixed together evenly. On the right there is a bowl of clear vegetable soup. It shows clear green broth, white bowl and chopped ingredients. It is placed on table. On the right there is a bowl of boiled vegetables. It shows dark green vegetables and metal spoon. The other dish are below the fried fish. The fried fish is to the left of the stir-fried vegetables. The dishes are set on a red patterned tablecloth.</sub>

**[C]** (132 từ, 34/40 chi tiết)

> Ở bên trái và ở phía dưới có hai phần món ăn khác. Ở góc trên bên trái có một đĩa cá chiên. Nó cho thấy nước sốt đỏ sẫm, thảo mộc xanh và thìa bạc. Nó được đặt trên đĩa bầu dục màu trắng. Ở phía trên có hai phần rau xào. Chúng cho thấy đậu hà lan xanh, ngô vàng và đậu hà lan xanh. Chúng được rải trên đĩa. Ở bên phải có một bát canh. Nó cho thấy nước dùng vàng trong, thảo mộc xanh và đũa đen. Nó được đặt ngang qua bát. Ở bên phải có một bát rau luộc. Nó cho thấy rau xanh đậm, thìa bạc và bát trắng. Các món ăn khác nằm bên dưới cá chiên. cá chiên nằm ở bên trái của rau xào.

<sub>EN: On the left and at the bottom there are two servings of other dish. In the top left corner there is a plate of fried fish. It shows dark red sauce, green herbs and silver spoon. It is placed on white oval plate. At the top there are two servings of stir-fried vegetables. They show green peas, yellow corn and green peas. They are scattered on plate. On the right there is a bowl of clear vegetable soup. It shows clear yellow broth, green herbs and black chopsticks. It is placed across bowl. On the right there is a bowl of boiled vegetables. It shows dark green vegetables, silver spoon and white bowl. The other dish are below the fried fish. The fried fish is to the left of the stir-fried vegetables.</sub>

## `srcA_H-065_jpg.rf.481fa6a339309292dd846ee202f95836.jpg`

Món (nhãn): fried rice, other dish, roasted chicken, stir-fried vegetables

**[A]** (128 từ, 28/34 chi tiết)

> Ở phía trên và bên phải có hai phần rau xào. Chúng cho thấy đĩa trắng với hoa văn xanh, rau xanh và hành lá thái lát. Chúng được trộn lẫn với nhau. Bên kia bàn có ba phần món ăn khác. Ở bên trái có một đĩa cơm chiên. Nó cho thấy đĩa trắng với hoa văn xanh, đậu hà lan xanh và hạt gạo. Nó được chất thành đống trên đĩa. Ở góc trên bên phải có một đĩa gà quay. Nó cho thấy da gà màu nâu đỏ, bông cải xanh và lát ớt chuông vàng. Nó được sắp xếp trên một chiếc đĩa trắng. Các rau xào nằm ở bên phải của các món ăn khác. Các món ăn khác nằm bên dưới cơm chiên. Các món ăn được đặt trên một chiếc bàn mặt kính tròn.

<sub>EN: At the top and on the right there are two servings of stir-fried vegetables. They show white plate with blue pattern, green vegetables and sliced green onions. They are mixed together. Across the table there are three servings of other dish. On the left there is a plate of fried rice. It shows white plate with blue pattern, green peas and rice grains. It is mounded on plate. In the top right corner there is a plate of roasted chicken. It shows reddish-brown chicken skin, green broccoli florets and yellow bell pepper slice. It is arranged on a white plate. The stir-fried vegetables are to the right of the other dish. The other dish are below the fried rice. The dishes are set on a round glass-top table.</sub>

**[B]** (132 từ, 22/28 chi tiết)

> Ở phía trên và bên phải có hai phần rau xào. Chúng cho thấy các miếng thịt nâu, các dải rau xanh và thịt thái lát. Bên kia bàn có ba phần món ăn khác. Ở bên trái có một đĩa cơm chiên. Nó cho thấy đậu hà lan xanh, cà rốt cam và đậu hà lan xanh. Nó được chất thành đống trên đĩa. Ở góc trên bên phải có một đĩa gà quay. Nó cho thấy các miếng gà màu nâu đỏ, các bông súp lơ xanh và các miếng gà. Nó được đặt trên đĩa. Các rau xào nằm ở bên phải của các món ăn khác. Các món ăn khác nằm bên dưới cơm chiên. Các món ăn được đặt trên một chiếc bàn màu xanh lá cây nhạt. Cũng có thể thấy: thìa kim loại, cốc nước và các chai gia vị. Phông nền cho thấy cách sắp xếp bàn ăn trong nhà hàng.

<sub>EN: At the top and on the right there are two servings of stir-fried vegetables. They show brown meat pieces, green vegetable strips and sliced meat. Across the table there are three servings of other dish. On the left there is a plate of fried rice. It shows green peas, orange carrots and green peas. It is mounded on plate. In the top right corner there is a plate of roasted chicken. It shows reddish-brown chicken pieces, green broccoli florets and chicken pieces. It is placed on plate. The stir-fried vegetables are to the right of the other dish. The other dish are below the fried rice. The dishes are set on a light green table. Also visible: metal spoons, glass of water and condiment bottles. The background shows a restaurant table setting.</sub>

**[C]** (128 từ, 32/36 chi tiết)

> Ở phía trên và bên phải có hai phần rau xào. Chúng cho thấy nước sốt nâu, rau xanh và hành tây trắng. Chúng được trộn lẫn với nhau thành một đống. Bên kia bàn có ba phần món ăn khác. Ở bên trái có một đĩa cơm chiên. Nó cho thấy đậu hà lan xanh, các miếng cà rốt cam và hạt gạo. Nó được chất thành đống ở giữa đĩa. Ở góc trên bên phải có một đĩa gà quay. Nó cho thấy da gà màu nâu đỏ, bông cải xanh và ớt chuông vàng. Nó được sắp xếp với rau củ xung quanh thịt gà. Các rau xào nằm ở bên phải của các món ăn khác. Các món ăn khác nằm bên dưới cơm chiên. Các món ăn được đặt trên một chiếc bàn kính tròn với các tấm lót hoa.

<sub>EN: At the top and on the right there are two servings of stir-fried vegetables. They show brown sauce, green vegetables and white onions. They are mixed together in a pile. Across the table there are three servings of other dish. On the left there is a plate of fried rice. It shows green peas, orange carrot pieces and rice grains. It is mounded in center of plate. In the top right corner there is a plate of roasted chicken. It shows reddish-brown chicken skin, green broccoli and yellow bell pepper. It is arranged with vegetables around chicken. The stir-fried vegetables are to the right of the other dish. The other dish are below the fried rice. The dishes are set on a round glass table with floral placemats.</sub>

## `srcA_H-069_jpg.rf.8b2b6df86d40620e2197288c0c893d85.jpg`

Món (nhãn): dessert, dipping sauce, fermented pork, fresh herbs and greens, sizzling crepe

**[A]** (134 từ, 20/26 chi tiết)

> Ở góc dưới bên trái có một đĩa lớn bánh xèo. Nó cho thấy bánh crepe màu vàng, thảo mộc xanh và nước sốt màu nâu. Nó được thái lát và sắp xếp trên đĩa. Ở góc trên bên phải có một phần món tráng miệng. Ở góc dưới bên phải có một đĩa rau sống. Nó cho thấy đĩa màu xanh sáng, lá màu xanh đậm và rau xanh. Ở góc trên bên trái có một đĩa nem chua. Nó cho thấy vành đĩa hoa văn màu xanh dương và xiên gỗ. Nó được sắp xếp trên đĩa. Ở góc trên bên phải và ở bên phải có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, rau trang trí màu xanh và thìa kim loại. bánh xèo nằm bên dưới món tráng miệng. món tráng miệng nằm bên trên rau sống.

<sub>EN: In the bottom left corner there is a large plate of sizzling crepe. It shows yellow crepe, green herbs and brown sauce. It is sliced and arranged on plate. In the top right corner there is a serving of dessert. In the bottom right corner there is a plate of fresh herbs and greens. It shows bright green plate, dark green leaves and green leafy vegetables. In the top left corner there is a plate of fermented pork. It shows blue patterned rim and wooden skewers. It is arranged on plate. In the top right corner and on the right there are two small bowls of dipping sauce. They show reddish-brown liquid, green leafy garnish and metal spoon. The sizzling crepe is below the dessert. The dessert is above the fresh herbs and greens.</sub>

**[B]** (134 từ, 23/28 chi tiết)

> Ở góc dưới bên trái có một đĩa lớn bánh xèo. Nó cho thấy bề mặt bánh crepe màu vàng, các cạnh màu nâu vàng và các nửa bánh crepe được gấp lại. Nó được gấp thành hình bán nguyệt. Ở góc trên bên phải có một phần món tráng miệng. Ở góc dưới bên phải có một đĩa rau sống. Nó cho thấy các loại rau xanh, đĩa màu vàng và các loại rau xanh. Nó được chất đống trên đĩa. Ở góc trên bên trái có một đĩa nem chua. Nó cho thấy thịt nướng màu nâu, vành đĩa màu trắng và các miếng thịt xiên. Nó được đặt trên đĩa. Ở góc trên bên phải và ở bên phải có hai bát nhỏ đồ chấm. Chúng cho thấy xà lách xanh. Chúng được đặt trên bề mặt màu trắng. bánh xèo nằm bên dưới món tráng miệng.

<sub>EN: In the bottom left corner there is a large plate of sizzling crepe. It shows yellow crepe surface, golden brown edges and folded crepe halves. It is folded into half-moon. In the top right corner there is a serving of dessert. In the bottom right corner there is a plate of fresh herbs and greens. It shows green leafy vegetables, yellow plate and green leafy vegetables. It is piled on plate. In the top left corner there is a plate of fermented pork. It shows brown grilled meat, white plate rim and skewered meat pieces. It is placed on plate. In the top right corner and on the right there are two small bowls of dipping sauce. They show green lettuce. They are placed on white surface. The sizzling crepe is below the dessert.</sub>

**[C]** (140 từ, 32/38 chi tiết)

> Ở góc dưới bên trái có một đĩa lớn bánh xèo. Nó cho thấy bánh crepe màu vàng, các cạnh màu nâu vàng và thảo mộc xanh. Nó được cắt thành từng miếng. Ở góc trên bên phải có một phần món tráng miệng. Ở góc dưới bên phải có một bát rau sống. Nó cho thấy những chiếc lá xanh tươi, bát màu vàng và nước sốt màu nâu. Nó được rải trong bát. Ở góc trên bên trái có một đĩa nem chua. Nó cho thấy thịt màu nâu vàng, đĩa có hoa văn xanh trắng và những chiếc que gỗ màu nâu nhạt. Nó được xếp thẳng đứng trên đĩa. Ở góc trên bên phải và ở bên phải có hai bát nhỏ đồ chấm. Chúng cho thấy nước sốt màu nâu đỏ, vành bát màu trắng và thìa kim loại. Chúng được múc một phần bằng thìa. bánh xèo nằm bên dưới món tráng miệng.

<sub>EN: In the bottom left corner there is a large plate of sizzling crepe. It shows yellow crepe, golden-brown edges and green herbs. It is cut into pieces. In the top right corner there is a serving of dessert. In the bottom right corner there is a bowl of fresh herbs and greens. It shows bright green leaves, yellow bowl and brown sauce. It is scattered in bowl. In the top left corner there is a plate of fermented pork. It shows golden brown meat, blue and white patterned plate and light brown wooden sticks. It is arranged upright on plate. In the top right corner and on the right there are two small bowls of dipping sauce. They show reddish-brown sauce, white bowl rim and metal spoon. They are partially scooped with spoon. The sizzling crepe is below the dessert.</sub>

## `srcA_H-072_jpg.rf.a4bcd49c31dc7685cacadbc1312f3c70.jpg`

Món (nhãn): fresh herbs and greens, other dish, stir-fried vegetables

**[A]** (113 từ, 16/18 chi tiết)

> Ở góc dưới bên phải có một phần món ăn khác. Ở giữa có một đĩa rau xào. Nó cho thấy rau xanh, bọt trắng trên bia, rau xanh, tỏi phi và ớt đỏ. Nó được trộn với tỏi phi. Ở góc dưới bên phải có một đĩa rau sống. Nó cho thấy lá xanh và lá xanh. món ăn khác nằm bên dưới rau xào. rau xào nằm bên trái của rau sống. Các món ăn được đặt trên một chiếc bàn nhựa màu đỏ. Cũng có thể thấy: đũa gỗ, cốc thủy tinh, bát trắng và khăn giấy. Phông nền cho thấy một vỉa hè ngoài trời.

<sub>EN: In the bottom right corner there is a serving of other dish. In the center there is a plate of stir-fried vegetables. It shows green leafy vegetables, white foam on beer, green leafy vegetables, fried garlic and red chili. It is mixed with fried garlic. In the bottom right corner there is a plate of fresh herbs and greens. It shows green leaves and green leaves. The other dish is below the stir-fried vegetables. The stir-fried vegetables is to the left of the fresh herbs and greens. The dishes are set on a red plastic table. Also visible: wooden chopsticks, glass mugs, white bowls and paper napkins. The background shows an outdoor pavement.</sub>

**[B]** (121 từ, 16/19 chi tiết)

> Ở góc dưới bên phải có một phần món ăn khác. Ở giữa có một đĩa rau xào. Nó cho thấy các loại rau lá xanh, các miếng tỏi trắng, các phần lá xanh, các miếng tỏi trắng và lát ớt đỏ. Ở góc dưới bên phải có một đĩa rau sống. Nó cho thấy các loại rau thơm lá xanh, các loại rau thơm lá xanh và món chiên. Nó được đặt trên đĩa. món ăn khác nằm bên dưới rau xào. rau xào nằm ở bên trái của rau sống. Các món ăn được đặt trên một chiếc bàn nhựa màu đỏ. Cũng có thể thấy: đũa gỗ, bát trắng, cốc thủy tinh, khăn ăn trắng và bát nhỏ màu xanh lá cây. Phông nền cho thấy một khu vực chỗ ngồi ngoài trời.

<sub>EN: In the bottom right corner there is a serving of other dish. In the center there is a plate of stir-fried vegetables. It shows green leafy vegetables, white garlic pieces, green leafy parts, white garlic pieces and red chili slice. In the bottom right corner there is a plate of fresh herbs and greens. It shows green leafy herbs, green leafy herbs and fried item. It is placed on plate. The other dish is below the stir-fried vegetables. The stir-fried vegetables is to the left of the fresh herbs and greens. The dishes are set on a red plastic table. Also visible: wooden chopsticks, white bowls, glass mugs, white napkin and small green bowl. The background shows an outdoor seating area.</sub>

**[C]** (133 từ, 23/24 chi tiết)

> Ở góc dưới bên phải có một phần món ăn khác. Ở giữa có một đĩa rau xào. Nó cho thấy các loại rau lá xanh đậm, ớt đỏ thái lát, các miếng chiên màu nâu nhạt, rau lá xanh đậm và ớt đỏ thái lát. Nó được trộn lẫn với nhau trên đĩa. Ở góc dưới bên phải có một đĩa rau sống. Nó cho thấy lá ngò xanh, thức ăn chiên màu nâu, cạnh bát màu trắng, lá ngò và thức ăn chiên. Nó được đặt cạnh thức ăn chiên. món ăn khác nằm bên dưới rau xào. rau xào nằm bên trái của rau sống. Các món ăn được đặt trên một chiếc bàn nhựa màu đỏ. Cũng có thể thấy: đũa gỗ, cốc thủy tinh đựng bia, bát gốm trắng, khăn giấy và bát gốm màu xanh lá cây.

<sub>EN: In the bottom right corner there is a serving of other dish. In the center there is a plate of stir-fried vegetables. It shows dark green leafy vegetables, red sliced chili, light brown fried pieces, dark green leafy vegetables and red chili slices. It is mixed together on plate. In the bottom right corner there is a plate of fresh herbs and greens. It shows green cilantro leaves, brown fried food, white bowl edge, cilantro leaves and fried food. It is placed next to fried food. The other dish is below the stir-fried vegetables. The stir-fried vegetables is to the left of the fresh herbs and greens. The dishes are set on a red plastic table. Also visible: wooden chopsticks, glass mugs with beer, white ceramic bowls, paper napkins and green ceramic bowl.</sub>

## `srcA_H-074_jpg.rf.9dbc799b63f1f4b8ce44b48d4a374981.jpg`

Món (nhãn): clams and scallops, dipping sauce, fried fish, oyster, sea snails, whole crab

**[A]** (135 từ, 42/44 chi tiết)

> Ở giữa có một phần cá chiên. Nó cho thấy lớp giấy bạc sáng bóng, da cá màu nâu vàng và cá nguyên con với vây. Nó được phục vụ trên giấy gói bạc. Ở bên phải và phía dưới có hai phần ngao sò. Chúng cho thấy đồ trang trí lá xanh, nửa vỏ sò trắng và khăn trải bàn màu đỏ. Chúng được đặt trên rau xanh. Bên kia bàn có ba phần ốc. Chúng cho thấy đĩa trắng, khăn trải bàn màu đỏ và thảo mộc xanh. Chúng được rải trên đĩa. Ở góc trên bên phải có một đĩa hàu. Nó cho thấy đĩa trắng, vỏ sò màu xám và lá xanh. Nó được sắp xếp trên một chiếc đĩa. Ở góc trên bên trái có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, đồ trang trí lá xanh và đồ trang trí lá xanh.

<sub>EN: In the center there is a serving of fried fish. It shows shiny silver foil, golden-brown fish skin and whole fish with fins. It is served on foil wrapper. On the right and at the bottom there are two servings of clams and scallops. They show green leafy garnish, white shell halves and red tablecloth. They are placed on leafy greens. Across the table there are three servings of sea snails. They show white plate, red tablecloth and green herbs. They are scattered on plate. In the top right corner there is a plate of oyster. It shows white plate, gray shell and green leaves. It is arranged on a plate. In the top left corner there is a plate of whole crab. It shows red-orange crab shell, green leaf garnish and green leaf garnish.</sub>

**[B]** (138 từ, 41/45 chi tiết)

> Ở giữa có một đĩa cá chiên. Nó cho thấy cá màu nâu vàng, thảo mộc xanh và cá nguyên con. Nó được gói trong giấy bạc. Ở bên phải và phía dưới có hai phần ngao sò. Chúng cho thấy vỏ màu trắng xám, đồ trang trí lá xanh và vỏ động vật hai mảnh đang mở. Chúng được đặt trên lá. Băng qua bàn có ba phần ốc. Chúng cho thấy vỏ đốm nâu, thảo mộc xanh và vỏ xoắn màu nâu. Chúng nằm rải rác trên bề mặt. Ở góc trên bên phải có một đĩa hàu. Nó cho thấy hàu màu xám trắng, thảo mộc xanh và hàu màu xám trắng. Nó được đặt trên đĩa. Ở góc trên bên trái có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, bề mặt đĩa trắng và chân cua. Nó được đặt nguyên con lên trên.

<sub>EN: In the center there is a plate of fried fish. It shows golden brown fish, green herbs and whole fish. It is wrapped in foil. On the right and at the bottom there are two servings of clams and scallops. They show white gray shells, green leafy garnish and open bivalve shells. They are placed on leaves. Across the table there are three servings of sea snails. They show brown spotted shells, green herbs and spiral brown shells. They are scattered across surface. In the top right corner there is a plate of oyster. It shows gray white oysters, green herbs and gray white oysters. It is placed on plate. In the top left corner there is a plate of whole crab. It shows red-orange crab shell, white plate surface and crab legs. It is placed whole on.</sub>

**[C]** (139 từ, 53/55 chi tiết)

> Ở giữa có một khay cá chiên. Nó cho thấy lớp da cá màu nâu vàng, thảo mộc xanh và những miếng ớt đỏ. Nó được gói trong giấy nhôm. Ở bên phải và phía dưới có hai phần ngao sò. Chúng cho thấy lớp vỏ màu xám trắng, lá xanh và đồ trang trí màu cam. Chúng được sắp xếp trên đĩa với lá. Bên kia bàn có ba phần ốc. Chúng cho thấy lớp vỏ màu nâu, thảo mộc xanh và sốt đỏ. Chúng được rải trên đĩa. Ở góc trên bên phải có một đĩa hàu. Nó cho thấy đồ trang trí lá xanh, đồ trang trí lá xanh và các loại hạt băm nhỏ. Nó được sắp xếp trên đĩa trắng. Ở góc trên bên trái có một đĩa cua. Nó cho thấy vỏ cua màu đỏ cam, đồ trang trí lá xanh và đĩa trắng. Nó được đặt nguyên con trên đĩa.

<sub>EN: In the center there is a tray of fried fish. It shows golden-brown fish skin, green herbs and red chili pieces. It is wrapped in aluminum foil. On the right and at the bottom there are two servings of clams and scallops. They show gray-white shells, green leaves and orange garnish. They are arranged on plate with leaves. Across the table there are three servings of sea snails. They show brown shells, green herbs and red sauce. They are scattered on plate. In the top right corner there is a plate of oyster. It shows green leafy garnish, green leafy garnish and chopped nuts. It is arranged on white plate. In the top left corner there is a plate of whole crab. It shows red-orange crab shell, green leafy garnish and white plate. It is placed whole on plate.</sub>

## `srcA_H-075_jpg.rf.9400412ba2beba18a3a5f6a385d1cc8a.jpg`

Món (nhãn): boiled vegetables, dipping sauce, fresh herbs and greens, other dish, shredded salad, vietnamese pork ham

**[A]** (135 từ, 34/43 chi tiết)

> Ở phía dưới có một đĩa rau sống. Nó cho thấy những chiếc lá xanh đậm, gỗ màu nâu nhạt và rau xanh. Nó được sắp xếp trên một chiếc đĩa. Ở phía dưới có một đĩa chả giò. Nó cho thấy chiếc đĩa màu nâu đậm, thịt màu hồng nhạt và những chiếc lá xanh. Đó là thịt thái lát được sắp xếp trên đĩa. Ở bên trái có một phần món ăn khác. Ở bên phải có một đĩa gỏi. Nó cho thấy những chiếc lá xà lách xanh, rau thái sợi màu trắng và những sợi cà rốt màu cam. Nó được trộn trên đĩa. Ở phía trên có một đĩa rau luộc. Nó cho thấy lá xanh đậm, những lát cà rốt màu cam và dưa lưới màu xanh nhạt. Nó được sắp xếp gọn gàng trên đĩa. Ở chính giữa có một bát nhỏ đồ chấm.

<sub>EN: At the bottom there is a plate of fresh herbs and greens. It shows dark green leaves, light brown wood and green leafy vegetables. It is arranged on a plate. At the bottom there is a plate of vietnamese pork ham. It shows dark brown plate, light pink meat and green leaves. It is sliced meat arranged on plate. On the left there is a serving of other dish. On the right there is a plate of shredded salad. It shows green lettuce leaves, white shredded vegetables and orange carrot strands. It is mixed on plate. At the top there is a plate of boiled vegetables. It shows dark green leaf, orange carrot slices and light green melon. It is neatly arranged on plate. In the center there is a small bowl of dipping sauce.</sub>

**[B]** (138 từ, 29/39 chi tiết)

> Ở phía dưới có một đĩa rau sống. Nó cho thấy các loại rau xanh, thảo mộc lá xanh và các miếng thịt thái lát. Nó được đặt ở phía trên. Ở phía dưới có một phần chả giò. Nó cho thấy các lát thịt màu hồng, rau trang trí lá xanh và các cuộn thịt thái lát. Nó được cắt thành từng lát. Ở bên trái có một phần món ăn khác. Ở bên phải có một bát gỏi. Nó cho thấy các phần lá xanh, các phần trắng bào sợi và các phần trắng bào sợi. Nó được trộn lẫn với nhau một cách lỏng lẻo. Ở phía trên có một đĩa rau luộc. Nó cho thấy các lá xanh đậm, rau màu vàng nhạt và rau màu vàng nhạt thái lát. Nó được đặt cùng nhau một cách gọn gàng. Ở chính giữa có một bát nhỏ đồ chấm. Nó cho thấy chất lỏng màu nâu đỏ.

<sub>EN: At the bottom there is a plate of fresh herbs and greens. It shows green leafy greens, green leafy herbs and sliced meat pieces. It is placed on top. At the bottom there is a serving of vietnamese pork ham. It shows pinkish meat slices, green leafy garnish and sliced meat rolls. It is cut into slices. On the left there is a serving of other dish. On the right there is a bowl of shredded salad. It shows green leafy parts, white shredded parts and shredded white parts. It is mixed together loosely. At the top there is a plate of boiled vegetables. It shows dark green leaves, pale yellow vegetable and sliced pale yellow vegetable. It is neatly placed together. In the center there is a small bowl of dipping sauce. It shows reddish brown liquid.</sub>

**[C]** (139 từ, 40/49 chi tiết)

> Ở phía dưới có một giỏ rau sống. Nó cho thấy lá xanh, thân màu tím và rau lá xanh. Ở phía dưới có một phần chả giò. Nó cho thấy các lát thịt lợn màu hồng nhạt, rau lá xanh và nước sốt màu cam. Nó được sắp xếp theo hình tròn. Ở bên trái có một phần món ăn khác. Ở bên phải có một bát gỏi. Nó cho thấy rau lá xanh, rau thái sợi màu trắng và cà rốt thái sợi màu cam. Nó được phủ lên trên bằng rau thái sợi. Ở phía trên có một bát rau luộc. Nó cho thấy các lát cà rốt màu cam, các miếng dưa chuột màu xanh nhạt và lá màu xanh đậm. Nó được sắp xếp gọn gàng trong bát. Ở giữa có một bát nhỏ đồ chấm. Nó cho thấy chất lỏng màu cam đỏ, các đốm màu nâu nhạt và chất lỏng.

<sub>EN: At the bottom there is a basket of fresh herbs and greens. It shows green leaves, purple stems and green leafy vegetables. At the bottom there is a serving of vietnamese pork ham. It shows light pink pork slices, green leafy vegetables and orange sauce. It is arranged in a circular pattern. On the left there is a serving of other dish. On the right there is a bowl of shredded salad. It shows green leafy vegetables, white shredded vegetables and orange shredded carrots. It is topped with shredded vegetables. At the top there is a bowl of boiled vegetables. It shows orange carrot slices, light green cucumber pieces and dark green leaf. It is neatly arranged in bowl. In the center there is a small bowl of dipping sauce. It shows reddish-orange liquid, light brown specks and liquid.</sub>

## `srcA_H-079_jpg.rf.ad000b97d9d37e95de0ffaf79b71954d.jpg`

Món (nhãn): clams and scallops, fresh herbs and greens, fried fish, tofu and noodle platter

**[A]** (132 từ, 31/31 chi tiết)

> Ở bên phải có một giỏ lớn rau sống. Nó cho thấy các loại rau lá xanh, giá đỗ trắng và cánh hoa vàng. Nó được trộn với giá đỗ. Ở phía dưới có một bát ngao sò. Nó cho thấy bề mặt gỗ màu nâu nhạt, vành bát bằng kim loại và các vỏ sò hai mảnh đang mở. Nó được trộn lẫn với nhau trong bát. Ở bên trái có một khay tre đựng bún đậu mắm tôm. Nó cho thấy các loại rau lá xanh, mì trắng và thịt đỏ. Ở giữa có một đĩa cá chiên. Nó cho thấy thịt màu hồng, thảo mộc xanh và các lát thịt mỏng. rau sống nằm ở bên phải của ngao sò. ngao sò nằm ở bên phải của bún đậu mắm tôm.

<sub>EN: On the right there is a large basket of fresh herbs and greens. It shows green leafy vegetables, white bean sprouts and yellow flower petals. It is mixed with bean sprouts. At the bottom there is a bowl of clams and scallops. It shows light brown wooden surface, metallic bowl rim and open bivalve shells. It is mixed together in bowl. On the left there is a bamboo tray of tofu and noodle platter. It shows green leafy vegetables, white noodles and red meat. In the center there is a plate of fried fish. It shows pinkish meat, green herbs and thin meat slices. The fresh herbs and greens is to the right of the clams and scallops. The clams and scallops is to the right of the tofu and noodle platter.</sub>

**[B]** (138 từ, 22/34 chi tiết)

> Ở bên phải có một đĩa lớn rau sống. Nó cho thấy các loại rau xanh, giá đỗ trắng và cánh hoa vàng. Ở phía dưới có một bát ngao sò. Nó cho thấy vỏ sò trắng, thân thảo mộc xanh và các loại thảo mộc xanh nhỏ. Ở bên trái có một khay tre đựng bún đậu mắm tôm. Ở giữa có một bát cá chiên. Nó cho thấy thịt đỏ hồng, rau xanh và thịt thái lát mỏng. Nó được đặt ở phía trên. rau sống nằm ở bên phải của ngao sò. ngao sò nằm ở bên phải của bún đậu mắm tôm. Các món ăn được đặt trên một chiếc bàn gỗ sáng màu. Cũng có thể thấy: thìa kim loại, đũa gỗ, ly bia và bát sứ trắng.

<sub>EN: On the right there is a large plate of fresh herbs and greens. It shows green leafy vegetables, white bean sprouts and yellow flower petals. At the bottom there is a bowl of clams and scallops. It shows white clam shells, green herb stems and small green herbs. On the left there is a bamboo tray of tofu and noodle platter. In the center there is a bowl of fried fish. It shows pinkish red meat, green leafy vegetables and thinly sliced meat. It is placed on top. The fresh herbs and greens is to the right of the clams and scallops. The clams and scallops is to the right of the tofu and noodle platter. The dishes are set on a light wooden table. Also visible: metal spoon, wooden chopsticks, glass of beer and white ceramic bowl.</sub>

**[C]** (137 từ, 41/44 chi tiết)

> Ở bên phải có một giỏ lớn rau sống. Nó cho thấy các loại thảo mộc lá xanh, cánh hoa vàng và giá đỗ trắng. Nó được sắp xếp thành từng lớp. Ở dưới cùng có một bát ngao sò. Nó cho thấy các loại vỏ màu xám trắng, thảo mộc xanh và gỗ màu nâu nhạt. Nó được rắc thảo mộc ở phía trên. Ở bên trái có một khay tre đựng bún đậu mắm tôm. Nó cho thấy các loại thảo mộc lá xanh, thịt đỏ và các dải trắng trong suốt. Ở giữa có một đĩa cá chiên. Nó cho thấy thịt màu đỏ hồng, thảo mộc xanh và đĩa bạc. Nó được sắp xếp với thảo mộc ở phía trên. rau sống nằm ở bên phải của ngao sò. ngao sò nằm ở bên phải của bún đậu mắm tôm.

<sub>EN: On the right there is a large basket of fresh herbs and greens. It shows green leafy herbs, yellow flower petals and white bean sprouts. It is arranged in layers. At the bottom there is a bowl of clams and scallops. It shows gray-white shells, green herbs and light brown wood. It is scattered with herbs on top. On the left there is a bamboo tray of tofu and noodle platter. It shows green leafy herbs, red meat and white translucent strips. In the center there is a plate of fried fish. It shows pinkish red meat, green herbs and silver plate. It is arranged with herbs on top. The fresh herbs and greens is to the right of the clams and scallops. The clams and scallops is to the right of the tofu and noodle platter.</sub>

## `srcA_H-081_jpg.rf.92fa432607cd8a8dde03fedff94c3543.jpg`

Món (nhãn): clear vegetable soup, fresh herbs and greens, tofu and noodle platter, vietnamese pork ham

**[A]** (127 từ, 19/27 chi tiết)

> Ở phía trên và ở giữa có hai bát canh. Chúng cho thấy nước dùng màu vàng, lá xanh và rau xanh. Ở góc dưới bên phải có một đĩa rau sống. Nó cho thấy lá xanh và lá xanh. Ở bên trái có một đĩa chả giò. Nó cho thấy thảo mộc xanh và nước dùng màu vàng. Ở phía trên có một đĩa bún đậu mắm tôm. Nó cho thấy đậu phụ chiên vàng, thảo mộc xanh và các miếng đậu phụ chiên. Nó được xếp chồng lên đĩa. Các canh nằm ở bên trái của rau sống. rau sống nằm ở bên phải của chả giò. Các món ăn được đặt trên một chiếc bàn gỗ.

<sub>EN: At the top and in the center there are two bowls of clear vegetable soup. They show yellow broth, green leaves and leafy greens. In the bottom right corner there is a plate of fresh herbs and greens. It shows green leaves and green leaves. On the left there is a plate of vietnamese pork ham. It shows green herbs and yellow broth. At the top there is a plate of tofu and noodle platter. It shows golden fried tofu, green herbs and fried tofu pieces. It is piled on plate. The clear vegetable soup are to the left of the fresh herbs and greens. The fresh herbs and greens is to the right of the vietnamese pork ham. The dishes are set on a wooden table.</sub>

**[B]** (130 từ, 25/31 chi tiết)

> Ở phía trên và ở giữa có hai bát canh. Chúng cho thấy nước dùng màu vàng, lá xanh và rau xanh. Chúng được đặt ở giữa. Ở góc dưới bên phải có một đĩa rau sống. Nó cho thấy rau xanh và rau xanh. Nó được đặt trên đĩa trắng. Ở bên trái có một phần chả giò. Nó cho thấy nước dùng màu vàng nhạt, lá xanh đậm và nước dùng màu vàng. Nó được đặt trên đĩa trắng. Ở phía trên có một đĩa bún đậu mắm tôm. Nó cho thấy các miếng chiên vàng, rau thơm băm nhỏ và các miếng thức ăn chiên. Nó được đặt trên đĩa. Các canh nằm ở bên trái của rau sống.

<sub>EN: At the top and in the center there are two bowls of clear vegetable soup. They show yellowish broth, green leaves and leafy greens. They are placed in center. In the bottom right corner there is a plate of fresh herbs and greens. It shows green leafy vegetables and green leafy vegetables. It is placed on white plate. On the left there is a serving of vietnamese pork ham. It shows light yellow broth, dark green leaf and yellow soup base. It is placed on white plate. At the top there is a plate of tofu and noodle platter. It shows golden fried pieces, green chopped herbs and fried food pieces. It is placed on plate. The clear vegetable soup are to the left of the fresh herbs and greens.</sub>

**[C]** (128 từ, 40/41 chi tiết)

> Ở phía trên và ở giữa có hai bát canh. Chúng cho thấy nước dùng màu vàng, rau xanh và những miếng thịt màu nâu. Chúng được phủ lên trên bằng rau xanh tươi. Ở góc dưới bên phải có một đĩa rau sống. Nó cho thấy những chiếc lá xanh, những cuống màu xanh đậm và vành bát màu trắng. Nó được rải trên đĩa. Ở bên trái có một đĩa chả giò. Nó cho thấy da cá màu xám đậm và trắng, nước dùng màu vàng và thảo mộc xanh. Ở phía trên có một đĩa bún đậu mắm tôm. Nó cho thấy những miếng chiên màu vàng kim, thảo mộc băm nhỏ màu xanh và đĩa màu trắng. Nó được chất đống trên đĩa. Các canh nằm ở bên trái của rau sống.

<sub>EN: At the top and in the center there are two bowls of clear vegetable soup. They show yellow broth, green leafy vegetables and brown meat pieces. They are topped with fresh greens. In the bottom right corner there is a plate of fresh herbs and greens. It shows green leaves, dark green stems and white bowl edge. It is scattered on plate. On the left there is a plate of vietnamese pork ham. It shows dark gray and white fish skin, yellow broth and green herbs. At the top there is a plate of tofu and noodle platter. It shows golden fried pieces, green chopped herbs and white plate. It is piled on plate. The clear vegetable soup are to the left of the fresh herbs and greens.</sub>

## `srcA_H-082_jpg.rf.d77ff3db67402ca4131ff83ec079923c.jpg`

Món (nhãn): clear vegetable soup, fresh herbs and greens, other dish, shredded salad, stir-fried vegetables

**[A]** (140 từ, 28/32 chi tiết)

> Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy những lá xà lách xanh, lá xà lách tím và lá xà lách. Chúng được trộn lẫn với nhau trên đĩa. Ở giữa có một đĩa gỏi. Nó cho thấy những lá xà lách xanh, rau thái sợi và lá xà lách. Nó được trộn trên lớp nền xà lách. Ở bên phải có một phần món ăn khác. Ở góc dưới bên phải có một đĩa rau xào. Nó cho thấy rau xanh bóng, đũa màu nâu nhạt và rau lá xanh. Nó được trộn với tỏi phi. Ở bên trái có một bát canh. Nó cho thấy nước dùng màu nâu nhạt, bát trắng và cà chua đỏ thái nhỏ. rau sống nằm bên dưới gỏi. gỏi nằm ở bên trái của món ăn khác.

<sub>EN: In the bottom left corner there is a plate of fresh herbs and greens. It shows green lettuce leaves, purple lettuce leaves and lettuce leaves. It is mixed together on plate. In the center there is a plate of shredded salad. It shows green lettuce leaves, shredded vegetables and lettuce leaves. It is mixed on lettuce base. On the right there is a serving of other dish. In the bottom right corner there is a plate of stir-fried vegetables. It shows glossy green vegetables, light brown chopsticks and green leafy vegetables. It is mixed with fried garlic. On the left there is a bowl of clear vegetable soup. It shows light brown broth, white bowl and chopped red tomatoes. The fresh herbs and greens is below the shredded salad. The shredded salad is to the left of the other dish.</sub>

**[B]** (139 từ, 22/31 chi tiết)

> Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy rau lá xanh, rau lá xanh và rau lá tím. Nó được trộn lẫn với nhau một cách lỏng lẻo. Ở giữa có một đĩa gỏi. Nó cho thấy lớp nền lá xanh, hỗn hợp sợi màu nâu và rau thái sợi. Nó được trộn lẫn với nhau một cách hào phóng. Ở bên phải có một phần món ăn khác. Ở góc dưới bên phải có một bát rau xào. Nó cho thấy rau lá xanh, rau xanh thái nhỏ và những mẩu tỏi phi. Ở bên trái có một bát canh. Nó cho thấy nước sốt màu đỏ nâu, cà chua thái nhỏ và những miếng thịt. Nó được chất lên trên. rau sống nằm bên dưới gỏi. gỏi nằm ở bên trái của món ăn khác.

<sub>EN: In the bottom left corner there is a plate of fresh herbs and greens. It shows green leafy vegetables, green leafy vegetables and purple leafy vegetables. It is mixed together loosely. In the center there is a plate of shredded salad. It shows green leafy base, brown shredded mix and shredded vegetables. It is mixed together generously. On the right there is a serving of other dish. In the bottom right corner there is a bowl of stir-fried vegetables. It shows green leafy vegetables, chopped green vegetables and fried garlic bits. On the left there is a bowl of clear vegetable soup. It shows brownish red sauce, chopped tomatoes and chunks of meat. It is piled on top. The fresh herbs and greens is below the shredded salad. The shredded salad is to the left of the other dish.</sub>

**[C]** (135 từ, 41/44 chi tiết)

> Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy các loại rau lá xanh, rau lá tím và đĩa trắng. Nó được rải trên đĩa. Ở giữa có một đĩa gỏi. Nó cho thấy các lá xà lách xanh, phần phủ bào màu nâu và chất lỏng màu xanh trong suốt. Nó được sắp xếp trên một lớp xà lách. Ở bên phải có một phần món ăn khác. Ở góc dưới bên phải có một đĩa rau xào. Nó cho thấy các loại rau màu xanh đậm, tỏi màu nâu nhạt và đũa trắng. Nó được rải trên đĩa. Ở bên trái có một bát canh. Nó cho thấy nước dùng màu nâu, các miếng cà chua đỏ và thảo mộc xanh. Nó được trộn lẫn với nhau trong bát. rau sống nằm bên dưới gỏi.

<sub>EN: In the bottom left corner there is a plate of fresh herbs and greens. It shows green leafy vegetables, purple leafy vegetables and white plate. It is scattered on plate. In the center there is a plate of shredded salad. It shows green lettuce leaves, brown shredded topping and clear green liquid. It is arranged on a bed of lettuce. On the right there is a serving of other dish. In the bottom right corner there is a plate of stir-fried vegetables. It shows dark green vegetables, light brown garlic and white chopsticks. It is scattered on plate. On the left there is a bowl of clear vegetable soup. It shows brown broth, red tomato pieces and green herbs. It is mixed together in bowl. The fresh herbs and greens is below the shredded salad.</sub>

## `srcA_H-083_jpg.rf.b3de1d6e084faf84ebcd534fd7bafbe2.jpg`

Món (nhãn): clams and scallops, other dish, shredded salad

**[A]** (115 từ, 18/20 chi tiết)

> Ở phía dưới có một phần món ăn khác. Ở bên phải có một đĩa gỏi. Nó cho thấy vành hoa màu hồng, rau thái sợi màu vàng, lá xanh, rau thái sợi màu vàng và lá xanh. Nó được trang trí với lá xanh. Ở giữa có một nồi ngao sò. Nó cho thấy nồi gốm màu nâu đậm, vỏ màu be nhạt và vỏ động vật hai mảnh vỏ đang mở. món ăn khác nằm ở bên trái của gỏi. gỏi nằm ở bên phải của ngao sò. Các món ăn được đặt trên một chiếc bàn kim loại. Cũng có thể thấy: bát màu xanh lá cây, đũa, chai bia, cốc, xe máy và vạch kẻ đường. Phông nền cho thấy một con phố vào ban đêm.

<sub>EN: At the bottom there is a serving of other dish. On the right there is a plate of shredded salad. It shows pink floral rim, yellow shredded vegetables, green leaves, shredded yellow vegetables and green leaves. It is garnished with green leaves. In the center there is a pot of clams and scallops. It shows dark brown ceramic pot, light beige shells and open bivalve shells. The other dish is to the left of the shredded salad. The shredded salad is to the right of the clams and scallops. The dishes are set on a metal table. Also visible: green bowls, chopsticks, beer bottles, glass, motorcycle and crosswalk. The background shows a street at night.</sub>

**[B]** (121 từ, 15/18 chi tiết)

> Ở phía dưới có một phần món ăn khác. Ở bên phải có một đĩa gỏi. Nó cho thấy vành đĩa màu trắng, các phần lá xanh, rau củ màu vàng thái sợi, các phần lá xanh và các mảnh nhỏ màu nâu. Nó được trộn lẫn với nhau một cách ngẫu nhiên. Ở giữa có một nồi ngao sò. Nó cho thấy các vỏ màu xám trắng và vỏ sò đang mở. Nó được đặt trong nước dùng. món ăn khác nằm ở bên trái của gỏi. gỏi nằm ở bên phải của ngao sò. Các món ăn được đặt trên một chiếc bàn nhựa màu đen. Cũng có thể thấy: đũa gỗ, ly bia, ghế nhựa màu xanh và chai thủy tinh màu nâu. Phía sau cho thấy một con phố với vạch kẻ đường.

<sub>EN: At the bottom there is a serving of other dish. On the right there is a plate of shredded salad. It shows white plate rim, green leafy parts, shredded yellow vegetables, green leafy parts and small brown pieces. It is mixed together casually. In the center there is a pot of clams and scallops. It shows gray white shells and open clam shells. It is placed in broth. The other dish is to the left of the shredded salad. The shredded salad is to the right of the clams and scallops. The dishes are set on a black plastic table. Also visible: wooden chopsticks, glass of beer, blue plastic chair and brown glass bottle. The background shows a street with crosswalk.</sub>

**[C]** (137 từ, 20/22 chi tiết)

> Ở phía dưới có một phần món ăn khác. Ở bên phải có một đĩa gỏi. Nó cho thấy đĩa hoa văn hồng, rau củ bào sợi màu vàng, thảo mộc lá xanh, rau củ bào sợi màu vàng và thảo mộc lá xanh. Nó được rắc với đồ trang trí ở trên cùng. Ở giữa có một bát ngao sò. Nó cho thấy vỏ sò trắng xám, nước dùng nhạt, vành bát màu sẫm, vỏ động vật hai mảnh vỏ đang mở và thịt vỏ bên trong. Nó được sắp xếp trong một chiếc bát. món ăn khác nằm ở bên trái của gỏi. gỏi nằm ở bên phải của ngao sò. Các món ăn được đặt trên một chiếc bàn kim loại màu sẫm. Cũng có thể thấy: đũa nhựa màu xanh lá cây, chai bia màu nâu, cốc thủy tinh trong suốt đựng bia và bát nhựa màu xanh lá cây. Phông nền cho thấy một con phố với vạch kẻ đường và xe tay ga đang đỗ.

<sub>EN: At the bottom there is a serving of other dish. On the right there is a plate of shredded salad. It shows pink floral plate, yellow shredded vegetables, green leafy herbs, shredded yellow vegetables and green leafy herbs. It is scattered with garnish on top. In the center there is a bowl of clams and scallops. It shows gray-white shells, light broth, dark rim of bowl, open bivalve shells and shell meat inside. It is arranged in a bowl. The other dish is to the left of the shredded salad. The shredded salad is to the right of the clams and scallops. The dishes are set on a dark metal table. Also visible: green plastic chopsticks, brown beer bottles, clear glass with beer and green plastic bowls. The background shows a street with crosswalk and parked scooter.</sub>

## `srcA_H-087_jpg.rf.20c859222fadf4d429c9115ca05b0f40.jpg`

Món (nhãn): boiled chicken, boiled vegetables, clear vegetable soup, dipping sauce, stir-fried vegetables, vietnamese pork ham

**[A]** (135 từ, 27/35 chi tiết)

> Ở góc dưới bên phải có một đĩa rau luộc. Nó cho thấy đĩa trắng, các miếng cà rốt màu cam và các miếng rau màu xanh lá cây nhạt. Ở phía dưới có một đĩa gà luộc. Nó cho thấy da gà màu vàng nhạt và rau thơm trang trí màu xanh lá cây. Ở giữa có một đĩa rau xào. Nó cho thấy rau xanh, ớt đỏ và rau xanh. Chúng được trộn lẫn với nhau. Ở bên trái và ở góc dưới bên trái có hai bát canh. Chúng cho thấy nước dùng màu xanh lá cây nhạt, bát trắng và rau xanh. Ở bên trái và ở góc dưới bên trái có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, bát trắng và đũa. Ở giữa và bên phải có hai phần chả giò.

<sub>EN: In the bottom right corner there is a plate of boiled vegetables. It shows white plate, orange carrot pieces and light green vegetable pieces. At the bottom there is a plate of boiled chicken. It shows pale yellow chicken skin and green herb garnish. In the center there is a plate of stir-fried vegetables. It shows green vegetables, red peppers and green vegetables. It is mixed together. On the left and in the bottom left corner there are two bowls of clear vegetable soup. They show light green broth, white bowl and leafy green vegetable. On the left and in the bottom left corner there are two small bowls of dipping sauce. They show reddish-brown liquid, white bowl and chopsticks. In the center and on the right there are two servings of vietnamese pork ham.</sub>

**[B]** (139 từ, 27/42 chi tiết)

> Ở góc dưới bên phải có một đĩa rau luộc. Nó cho thấy những miếng cà rốt màu cam và những miếng khoai tây màu trắng. Nó được đặt gọn gàng cùng nhau. Ở phía dưới có một đĩa gà luộc. Nó cho thấy lớp da màu vàng nhạt, thịt trắng bên trong và một nhánh thảo mộc xanh. Nó được đặt trên đĩa trắng. Ở giữa có một đĩa rau xào. Nó cho thấy bề mặt đĩa trắng, các phần lá xanh và những miếng cà chua đỏ. Chúng được trộn lẫn với nhau một cách lỏng lẻo. Ở bên trái và ở góc dưới bên trái có hai bát canh. Chúng cho thấy nước dùng trong, lá xanh và các miếng thịt. Chúng được đặt trong nước dùng. Ở bên trái và ở góc dưới bên trái có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ. Chúng được đặt ở giữa.

<sub>EN: In the bottom right corner there is a plate of boiled vegetables. It shows orange carrot pieces and white potato chunks. It is neatly placed together. At the bottom there is a plate of boiled chicken. It shows pale yellow skin, white meat inside and green herb sprig. It is placed on white plate. In the center there is a plate of stir-fried vegetables. It shows white plate surface, green leafy parts and red tomato pieces. It is mixed together loosely. On the left and in the bottom left corner there are two bowls of clear vegetable soup. They show clear broth, green leaves and meat pieces. They are placed in broth. On the left and in the bottom left corner there are two small bowls of dipping sauce. They show reddish brown liquid. They are placed in center.</sub>

**[C]** (134 từ, 49/55 chi tiết)

> Ở góc dưới bên phải có một bát rau luộc. Nó cho thấy những miếng cà rốt màu cam, những miếng củ cải trắng và những miếng nấm màu nâu. Nó được sắp xếp trong một chiếc bát. Ở phía dưới có một đĩa gà luộc. Nó cho thấy da gà màu vàng nhạt, thịt gà trắng và một chiếc lon màu cam. Nó được cắt thành từng miếng. Ở giữa có một bát rau xào. Nó cho thấy rau xanh, những miếng màu đỏ và những miếng màu trắng. Nó được trộn lẫn với nhau trong bát. Ở bên trái và ở góc dưới bên trái có hai bát canh. Chúng cho thấy nước dùng màu xanh trong, thịt màu nâu nhạt và rau lá xanh. Chúng được ngập một phần trong nước dùng. Ở bên trái và ở góc dưới bên trái có hai bát nhỏ đồ chấm.

<sub>EN: In the bottom right corner there is a bowl of boiled vegetables. It shows orange carrot pieces, white radish pieces and brown mushroom pieces. It is arranged in a bowl. At the bottom there is a plate of boiled chicken. It shows pale yellow chicken skin, white chicken meat and orange can. It is cut into pieces. In the center there is a bowl of stir-fried vegetables. It shows green vegetables, red pieces and white pieces. It is mixed together in bowl. On the left and in the bottom left corner there are two bowls of clear vegetable soup. They show clear green broth, light brown meat and green leafy vegetable. They are partially submerged in broth. On the left and in the bottom left corner there are two small bowls of dipping sauce.</sub>

## `srcA_H-091_jpg.rf.d704ecfc7e1aae4897ee65a7a96444ef.jpg`

Món (nhãn): dipping sauce, fresh herbs and greens, roast pork, squid, stir-fried vegetables

**[A]** (131 từ, 36/39 chi tiết)

> Ở bên phải có một đĩa mực. Nó cho thấy các loại thảo mộc xanh, cốc thủy tinh trong suốt và các loại thảo mộc xanh. Nó được sắp xếp trên một chiếc đĩa trắng. Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy các loại lá xanh, nước sốt màu nâu nhạt và các loại lá xanh. Nó được đặt trên một chiếc đĩa trắng. Ở giữa có một đĩa heo quay. Nó cho thấy thịt màu nâu đỏ, đĩa trắng và thịt thái lát. Nó được sắp xếp trên đĩa. Ở phía trên và bên trái có hai phần rau xào. Chúng cho thấy nước sốt đỏ, xà lách xanh và xà lách. Chúng được phục vụ trên lớp xà lách. Bên kia bàn có bốn bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, bát trắng và bát nhỏ.

<sub>EN: On the right there is a plate of squid. It shows green herbs, clear glass cup and green herbs. It is arranged on a white plate. In the bottom left corner there is a plate of fresh herbs and greens. It shows green leaves, light brown sauce and green leaves. It is placed on a white plate. In the center there is a plate of roast pork. It shows reddish brown meat, white plate and sliced meat. It is arranged on plate. At the top and on the left there are two servings of stir-fried vegetables. They show red sauce, green lettuce and lettuce. They are served on bed of lettuce. Across the table there are four small bowls of dipping sauce. They show reddish-brown liquid, white bowl and small bowl.</sub>

**[B]** (130 từ, 28/35 chi tiết)

> Ở bên phải có một đĩa mực. Nó cho thấy các loại rau lá xanh, thảo mộc xanh và ớt đỏ. Nó được đặt trên đĩa trắng. Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy các loại thảo mộc lá xanh, thảo mộc lá xanh và món chiên màu vàng. Nó được đặt trên đĩa trắng. Ở giữa có một đĩa heo quay. Nó cho thấy các lát thịt màu nâu đỏ, các lát dưa chuột xanh và thịt thái lát. Ở phía trên và bên trái có hai phần rau xào. Chúng cho thấy nước sốt đỏ bên cạnh, rau trang trí lá xanh và hỗn hợp rau thái nhỏ. Chúng được trộn lẫn với nhau không đều. Băng qua bàn có bốn bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ. Chúng được đặt trong bát nhỏ.

<sub>EN: On the right there is a plate of squid. It shows green leafy vegetables, green herbs and red chili. It is placed on white plate. In the bottom left corner there is a plate of fresh herbs and greens. It shows green leafy herbs, green leafy herbs and yellow fried item. It is placed on white plate. In the center there is a plate of roast pork. It shows reddish-brown meat slices, green cucumber slices and sliced meat. At the top and on the left there are two servings of stir-fried vegetables. They show red sauce side, green leaf garnish and chopped vegetables mix. They are mixed together unevenly. Across the table there are four small bowls of dipping sauce. They show reddish-brown liquid. They are placed in small bowl.</sub>

**[C]** (139 từ, 37/42 chi tiết)

> Ở bên phải có một đĩa mực. Nó cho thấy các loại thảo mộc xanh, lát ớt đỏ và thảo mộc xanh. Nó được sắp xếp với thảo mộc và rau củ. Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy lá xanh, các miếng chiên màu nâu nhạt và lá xanh. Nó được sắp xếp trên đĩa. Ở giữa có một đĩa heo quay. Nó cho thấy thịt màu nâu đỏ, đồ trang trí lá xanh và các lát dưa chuột màu xanh nhạt. Nó được sắp xếp trên đĩa với đồ trang trí. Ở phía trên và bên trái có hai phần rau xào. Chúng cho thấy nước sốt đỏ, xà lách xanh và cà rốt cam. Băng qua bàn có bốn bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, bát trắng và chất lỏng. mực nằm ở bên phải của rau sống.

<sub>EN: On the right there is a plate of squid. It shows green herbs, red chili slices and green herbs. It is arranged with herbs and vegetables. In the bottom left corner there is a plate of fresh herbs and greens. It shows green leaves, light brown fried pieces and green leaves. It is arranged on plate. In the center there is a plate of roast pork. It shows reddish-brown meat, green leafy garnish and light green cucumber slices. It is arranged on plate with garnishes. At the top and on the left there are two servings of stir-fried vegetables. They show red sauce, green lettuce and orange carrot. Across the table there are four small bowls of dipping sauce. They show reddish-brown liquid, white bowl and liquid. The squid is to the right of the fresh herbs and greens.</sub>

## `srcA_H-092_jpg.rf.4d0a05771177aa044833f53250bea7c4.jpg`

Món (nhãn): dessert, dipping sauce, fresh herbs and greens, fried rice, other dish, squid, tofu and noodle platter

**[A]** (133 từ, 26/37 chi tiết)

> Ở giữa có một phần món tráng miệng. Ở góc dưới bên trái có một đĩa rau sống. Nó cho thấy những lá xà lách xanh, lá xà lách và ớt đỏ. Ở bên trái có một đĩa bún đậu mắm tôm. Nó cho thấy đậu phụ chiên, lá xanh và bát nhỏ. Nó được đặt trên một chiếc đĩa trắng. Ở bên phải có một đĩa mực. Nó cho thấy đĩa trắng, rau xanh và cà rốt cam. Nó được trộn với rau. Ở phía trên có một phần món ăn khác. Ở góc dưới bên phải có một đĩa cơm chiên. Nó cho thấy những hạt gạo màu nâu nhạt, hạt gạo và đũa. Nó được vun thành đống ở giữa. Ở phía dưới có một bát nhỏ đồ chấm.

<sub>EN: In the center there is a serving of dessert. In the bottom left corner there is a plate of fresh herbs and greens. It shows green lettuce leaves, lettuce leaves and red chili peppers. On the left there is a plate of tofu and noodle platter. It shows fried tofu, green leaves and small bowl. It is placed on a white plate. On the right there is a plate of squid. It shows white plate, green vegetables and orange carrot. It is mixed with vegetables. At the top there is a serving of other dish. In the bottom right corner there is a plate of fried rice. It shows light brown rice grains, rice grains and chopsticks. It is mounded in center. At the bottom there is a small bowl of dipping sauce.</sub>

**[B]** (139 từ, 21/36 chi tiết)

> Ở giữa có một phần món tráng miệng. Ở góc dưới bên trái có một bát rau sống. Nó cho thấy rau xanh, rau xanh và lát ớt đỏ. Ở bên trái có một khay tre đựng bún đậu mắm tôm. Nó cho thấy đậu phụ chiên vàng, lá xanh và các miếng đậu phụ chiên. Nó được đặt trên đĩa. Ở bên phải có một đĩa mực. Nó cho thấy rau xanh và lát cà rốt. Nó được đặt trên đĩa trắng. Ở phía trên có một phần món ăn khác. Ở góc dưới bên phải có một đĩa cơm chiên. Nó được chất thành đống trên đĩa. Ở phía dưới có một bát nhỏ đồ chấm. Nó cho thấy chất lỏng màu nâu đỏ và lát ớt đỏ. Nó được đặt trong bát nhỏ.

<sub>EN: In the center there is a serving of dessert. In the bottom left corner there is a bowl of fresh herbs and greens. It shows green leafy vegetables, green leafy vegetables and red chili slices. On the left there is a bamboo tray of tofu and noodle platter. It shows golden fried tofu, green leaves and fried tofu pieces. It is placed on plate. On the right there is a plate of squid. It shows green leafy vegetables and carrot slices. It is placed on white plate. At the top there is a serving of other dish. In the bottom right corner there is a plate of fried rice. It is mounded on plate. At the bottom there is a small bowl of dipping sauce. It shows reddish-brown liquid and red chili slices. It is placed in small bowl.</sub>

**[C]** (136 từ, 39/45 chi tiết)

> Ở giữa có một phần món tráng miệng. Ở góc dưới bên trái có một bát rau sống. Nó cho thấy các loại rau lá màu xanh nhạt, ớt đỏ và xà lách xanh thái sợi. Ở bên trái có một đĩa bún đậu mắm tôm. Nó cho thấy đậu phụ chiên vàng, lá xanh và nước sốt sẫm màu. Nó được sắp xếp trên một chiếc đĩa trắng. Ở bên phải có một đĩa mực. Nó cho thấy các loại thảo mộc xanh, cà rốt cam và các loại thảo mộc xanh. Nó được rải trên đĩa. Ở phía trên có một phần món ăn khác. Ở góc dưới bên phải có một đĩa cơm chiên. Nó cho thấy các hạt gạo màu nâu nhạt, hạt gạo và đũa. Nó được vun thành đống ở giữa. Ở phía dưới có một bát nhỏ đồ chấm.

<sub>EN: In the center there is a serving of dessert. In the bottom left corner there is a bowl of fresh herbs and greens. It shows light green leafy vegetables, red chili peppers and shredded green lettuce. On the left there is a plate of tofu and noodle platter. It shows golden fried tofu, green leaves and dark sauce. It is arranged on a white plate. On the right there is a plate of squid. It shows green herbs, orange carrot and green herbs. It is scattered on plate. At the top there is a serving of other dish. In the bottom right corner there is a plate of fried rice. It shows light brown rice grains, rice grains and chopsticks. It is mounded in center. At the bottom there is a small bowl of dipping sauce.</sub>

## `srcA_H-093_jpg.rf.785ee9cabd391da6cd0100e276cc7a66.jpg`

Món (nhãn): roasted chicken, stir-fried vegetables, tofu and noodle platter

**[A]** (140 từ, 22/27 chi tiết)

> Ở góc dưới bên phải có một đĩa rau xào. Nó cho thấy rau xanh, đĩa trắng, rau xanh và tỏi phi. Nó được trộn lẫn với nhau. Ở bên phải có một đĩa gà quay. Nó cho thấy da gà màu nâu đỏ, rau trang trí xanh, các miếng gà và rau trang trí xanh. Nó được sắp xếp trên một chiếc đĩa trắng. Ở giữa có một khay tre đựng bún đậu mắm tôm. Nó cho thấy rau xanh, đậu phụ chiên vàng, rau xanh, đậu phụ chiên vàng và bát nhỏ. rau xào nằm bên dưới gà quay. gà quay nằm ở bên phải của bún đậu mắm tôm. Các món ăn được đặt trên mặt bàn đá granite lốm đốm. Cũng có thể thấy: đũa gỗ, cốc thủy tinh, hộp màu xanh, bát trắng và nắp chai màu đỏ. Phông nền cho thấy những người đang ngồi tại bàn.

<sub>EN: In the bottom right corner there is a plate of stir-fried vegetables. It shows green vegetables, white plate, green vegetables and fried garlic. It is mixed together. On the right there is a plate of roasted chicken. It shows reddish-brown chicken skin, green leafy garnish, chicken pieces and green leafy garnish. It is arranged on a white plate. In the center there is a bamboo tray of tofu and noodle platter. It shows green leafy vegetables, golden fried tofu, green leafy vegetables, golden fried tofu and small bowl. The stir-fried vegetables is below the roasted chicken. The roasted chicken is to the right of the tofu and noodle platter. The dishes are set on a speckled granite countertop. Also visible: wooden chopsticks, glass cups, blue container, white bowls and red bottle cap. The background shows a people sitting at table.</sub>

**[B]** (136 từ, 20/27 chi tiết)

> Ở góc dưới bên phải có một đĩa rau xào. Nó cho thấy các loại rau xanh, những miếng tỏi trắng, vụn tỏi chiên và dầu thực vật. Chúng được trộn lẫn với nhau một cách lỏng lẻo. Ở bên phải có một đĩa gà quay. Nó cho thấy da gà màu nâu đỏ, rau trang trí màu xanh, các miếng gà, rau xanh và nước sốt màu nâu. Nó được đặt trên đĩa. Ở giữa có một khay tre đựng bún đậu mắm tôm. Nó cho thấy đậu phụ chiên vàng, các loại rau xanh, các miếng đậu phụ chiên và rau xanh. rau xào nằm bên dưới gà quay. gà quay nằm ở bên phải của bún đậu mắm tôm. Các món ăn được đặt trên mặt bàn đá cẩm thạch. Cũng có thể thấy: đũa gỗ, ly bia và đĩa lá xanh. Phông nền cho thấy mọi người đang ngồi xung quanh.

<sub>EN: In the bottom right corner there is a plate of stir-fried vegetables. It shows green leafy vegetables, white garlic pieces, fried garlic bits and vegetable oil. It is mixed together loosely. On the right there is a plate of roasted chicken. It shows reddish-brown chicken skin, green leafy garnish, chicken pieces, leafy greens and brown sauce. It is placed on plate. In the center there is a bamboo tray of tofu and noodle platter. It shows golden fried tofu, green leafy vegetables, fried tofu pieces and leafy greens. The stir-fried vegetables is below the roasted chicken. The roasted chicken is to the right of the tofu and noodle platter. The dishes are set on a marble table top. Also visible: wooden chopsticks, glass of beer and green leaf plate. The background shows a people sitting around.</sub>

**[C]** (139 từ, 29/33 chi tiết)

> Ở góc dưới bên phải có một đĩa rau xào. Nó cho thấy các loại rau màu xanh đậm, các miếng tỏi trắng, dầu màu xanh nhạt, rau lá xanh và tỏi thái lát. Nó được trộn lẫn với nhau trên đĩa. Ở bên phải có một đĩa gà quay. Nó cho thấy lớp da màu nâu đỏ, lá màu xanh đậm, thịt màu nâu nhạt, các miếng gà và lá màu xanh đậm. Nó được sắp xếp trên đĩa với lá ở phía trên. Ở giữa có một khay tre đựng bún đậu mắm tôm. Nó cho thấy các loại rau lá xanh, đậu phụ chiên vàng, các loại rau lá xanh, đậu phụ chiên vàng và một bát nước sốt nhỏ. Nó được sắp xếp trên lá chuối. rau xào nằm bên dưới gà quay. gà quay nằm ở bên phải của bún đậu mắm tôm. Các món ăn được đặt trên một chiếc bàn đá lốm đốm màu xám.

<sub>EN: In the bottom right corner there is a plate of stir-fried vegetables. It shows dark green vegetables, white garlic pieces, light green oil, green leafy vegetables and sliced garlic. It is mixed together on plate. On the right there is a plate of roasted chicken. It shows reddish-brown skin, dark green leaves, light brown meat, chicken pieces and dark green leaves. It is arranged on plate with leaves on top. In the center there is a bamboo tray of tofu and noodle platter. It shows green leafy vegetables, golden fried tofu, green leafy vegetables, golden fried tofu and small bowl of sauce. It is arranged on banana leaf. The stir-fried vegetables is below the roasted chicken. The roasted chicken is to the right of the tofu and noodle platter. The dishes are set on a gray speckled stone table.</sub>

## `srcA_H-094_jpg.rf.b4a1639633e42d3c4865b3033f3e07c5.jpg`

Món (nhãn): dipping sauce, other dish, stir-fried vegetables

**[A]** (118 từ, 13/15 chi tiết)

> Ở phía dưới có một đĩa rau xào. Nó cho thấy các loại rau màu xanh đậm, các miếng tỏi trắng, mặt bàn màu nâu nhạt và các miếng tỏi trắng. Chúng được trộn lẫn với nhau trên đĩa. Ở góc trên bên trái và bên phải có hai phần món ăn khác. Ở bên trái và ở giữa có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ. rau xào nằm bên dưới món ăn khác. món ăn khác nằm ở bên phải của đồ chấm. Các món ăn được đặt trên một chiếc bàn gỗ sáng màu. Cũng có thể thấy: đũa đen, ly bia tuborg, ly uống nước trong suốt, cốc giấy trắng và hộp nhựa màu đỏ. Phông nền cho thấy nội thất nhà hàng bị làm mờ.

<sub>EN: At the bottom there is a plate of stir-fried vegetables. It shows dark green vegetables, white garlic pieces, light brown table and white garlic pieces. It is mixed together on plate. In the top left corner and on the right there are two servings of other dish. On the left and in the center there are two small bowls of dipping sauce. They show reddish-brown liquid. The stir-fried vegetables is below the other dish. The other dish are to the right of the dipping sauce. The dishes are set on a light wooden table. Also visible: black chopsticks, tuborg beer glass, clear drinking glass, white paper cup and red plastic container. The background shows a blurred restaurant interior.</sub>

**[B]** (109 từ, 10/16 chi tiết)

> Ở phía dưới có một đĩa rau xào. Nó cho thấy các loại rau xanh, những miếng tỏi trắng, rau xanh và tỏi băm. Ở góc trên bên trái và bên phải có hai phần món ăn khác. Ở bên trái và ở giữa có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ. Chúng được đặt trong bát nhỏ. rau xào nằm bên dưới món ăn khác. món ăn khác nằm ở bên phải của đồ chấm. Các món ăn được đặt trên một chiếc bàn gỗ sáng màu. Cũng có thể thấy: đũa đen và bát gốm trắng. Phông nền cho thấy một không gian trong nhà không rõ ràng.

<sub>EN: At the bottom there is a plate of stir-fried vegetables. It shows green leafy vegetables, white garlic pieces, green leafy vegetables and chopped garlic. In the top left corner and on the right there are two servings of other dish. On the left and in the center there are two small bowls of dipping sauce. They show reddish brown liquid. They are placed in small bowl. The stir-fried vegetables is below the other dish. The other dish are to the right of the dipping sauce. The dishes are set on a light wooden table. Also visible: black chopsticks and white ceramic bowl. The background shows an indistinct indoor space.</sub>

**[C]** (126 từ, 19/21 chi tiết)

> Ở phía dưới có một đĩa rau xào. Nó cho thấy các loại rau màu xanh đậm, các miếng tỏi trắng, bề mặt bàn màu nâu nhạt, các loại rau lá xanh bóng và các miếng tỏi trắng. Nó được rải trên đĩa. Ở góc trên bên trái và bên phải có hai phần món ăn khác. Ở bên trái và ở giữa có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, mặt trong bát màu trắng, chất lỏng và bát nhỏ. rau xào nằm bên dưới món ăn khác. món ăn khác nằm ở bên phải của đồ chấm. Các món ăn được đặt trên một chiếc bàn gỗ sáng màu. Cũng có thể thấy: đũa đen, ly bia, các bát nhỏ, cốc giấy và thực đơn màu đỏ. Phông nền cho thấy nội thất nhà hàng bị làm mờ.

<sub>EN: At the bottom there is a plate of stir-fried vegetables. It shows dark green vegetables, white garlic pieces, light brown table surface, glossy green leafy vegetables and white garlic pieces. It is scattered on plate. In the top left corner and on the right there are two servings of other dish. On the left and in the center there are two small bowls of dipping sauce. They show reddish-brown liquid, white bowl interior, liquid and small bowl. The stir-fried vegetables is below the other dish. The other dish are to the right of the dipping sauce. The dishes are set on a light wooden table. Also visible: black chopsticks, glass of beer, small bowls, paper cup and red menu. The background shows a blurred restaurant interior.</sub>

## `srcA_H-096_jpeg.rf.b46f6427a8e55ba8b2e0f5ab39efbe2d.jpg`

Món (nhãn): sea snails, shrimp, squid, stir-fried vegetables

**[A]** (138 từ, 26/32 chi tiết)

> Ở góc dưới bên phải có một đĩa mực. Nó cho thấy lớp giấy bạc sáng bóng, rau xanh và nước sốt màu cam. Nó được trộn lẫn với nhau trong giấy bạc. Bên kia bàn có ba phần ốc. Chúng cho thấy lá húng quế xanh và lá húng quế. Ở giữa có một bát tôm. Nó cho thấy nước dùng màu nâu đậm và thảo mộc xanh. Nó được sắp xếp trong một chiếc bát. Ở giữa có một khay rau xào. Nó cho thấy khay màu nâu đậm, rau xanh và rau xanh. Nó được trộn lẫn với nhau. mực nằm ở bên phải của ốc. ốc nằm ở bên dưới tôm. Các món ăn được đặt trên một chiếc bàn gỗ màu tối. Cũng có thể thấy: cốc nước, lon nhôm, chai màu xanh và bát màu trắng. Phông nền cho thấy nội thất nhà hàng bị làm mờ.

<sub>EN: In the bottom right corner there is a plate of squid. It shows shiny silver foil, green leafy vegetables and orange sauce. It is mixed together in foil. Across the table there are three servings of sea snails. They show green basil leaves and basil leaves. In the center there is a bowl of shrimp. It shows dark brown broth and green herbs. It is arranged in a bowl. In the center there is a tray of stir-fried vegetables. It shows dark brown tray, green vegetables and green vegetables. It is mixed together. The squid is to the right of the sea snails. The sea snails are below the shrimp. The dishes are set on a dark wooden table. Also visible: glass of water, aluminum can, green bottle and white bowls. The background shows a blurred restaurant interior.</sub>

**[B]** (139 từ, 19/26 chi tiết)

> Ở góc dưới bên phải có một đĩa mực. Nó cho thấy các loại rau lá xanh, rau xanh và các lát cà rốt màu cam. Nó được đặt trên giấy bạc. Bên kia bàn có ba phần ốc. Chúng cho thấy lớp sốt màu nâu, vỏ xoắn màu trắng và rau trang trí màu xanh. Chúng được đặt xung quanh phần sốt ở giữa. Ở giữa có một bát tôm. Nó cho thấy bát màu đen. Nó được đặt sát nhau. Ở giữa có một khay rau xào. Nó cho thấy các loại rau bóng loáng màu xanh, rau xanh và sốt ớt đỏ. Chúng được trộn lẫn với nhau. mực nằm ở bên phải của ốc. Các ốc nằm bên dưới tôm. Các món ăn được đặt trên một chiếc bàn gỗ tối màu. Cũng có thể thấy: ly nước và giấy bạc. Phông nền cho thấy nội thất nhà hàng bị làm mờ.

<sub>EN: In the bottom right corner there is a plate of squid. It shows green leafy vegetables, leafy greens and orange carrot slices. It is placed on foil. Across the table there are three servings of sea snails. They show brown sauce base, white spiral shells and green leafy garnish. They are placed around central sauce. In the center there is a bowl of shrimp. It shows black bowl. It is placed together closely. In the center there is a tray of stir-fried vegetables. It shows green glossy vegetables, green vegetables and red chili sauce. It is mixed together. The squid is to the right of the sea snails. The sea snails are below the shrimp. The dishes are set on a dark wooden table. Also visible: glass of water and aluminum foil. The background shows a blurred restaurant interior.</sub>

**[C]** (135 từ, 35/38 chi tiết)

> Ở góc dưới bên phải có một bát mực. Nó cho thấy rau xanh, sốt cam và rau xanh. Nó được gói trong giấy nhôm. Bên kia bàn có ba phần ốc. Chúng cho thấy sốt nâu, vỏ trắng và lá xanh. Chúng được sắp xếp trong sốt với lá ở trên cùng. Ở giữa có một bát tôm. Nó cho thấy nước dùng nâu đậm, thảo mộc xanh và nước dùng. Nó được sắp xếp trong bát với nước dùng. Ở giữa có một đĩa rau xào. Nó cho thấy rau xanh, tỏi chiên vàng và sốt đỏ đậm. Nó được trộn lẫn với nhau trên đĩa. mực nằm ở bên phải của ốc. ốc nằm ở dưới tôm. Các món ăn được đặt trên một chiếc bàn gỗ tối màu.

<sub>EN: In the bottom right corner there is a bowl of squid. It shows green leafy vegetables, orange sauce and green leafy vegetables. It is wrapped in aluminum foil. Across the table there are three servings of sea snails. They show brown sauce, white shells and green leaves. They are arranged in sauce with leaves on top. In the center there is a bowl of shrimp. It shows dark brown broth, green herbs and broth. It is arranged in a bowl with broth. In the center there is a plate of stir-fried vegetables. It shows green vegetables, golden fried garlic and dark red sauce. It is mixed together on plate. The squid is to the right of the sea snails. The sea snails are below the shrimp. The dishes are set on a dark wooden table.</sub>

## `srcA_H-097_jpg.rf.f354f9faa5111d2d576f9c605a3a7045.jpg`

Món (nhãn): dipping sauce, other dish, tofu and noodle platter

**[A]** (101 từ, 12/13 chi tiết)

> Ở bên trái có một phần món ăn khác. Ở góc dưới bên phải có một đĩa bún đậu mắm tôm. Nó cho thấy đậu phụ chiên vàng, lá xanh, đậu phụ cắt khối và lá xanh. Ở giữa và ở phía dưới có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, bát trắng, lát ớt đỏ và các đốm trắng nhỏ. món ăn khác nằm ở bên trái của bún đậu mắm tôm. bún đậu mắm tôm nằm ở bên phải của đồ chấm. Cũng có thể thấy: đũa gỗ, cốc thủy tinh màu xanh, khăn giấy và bát trắng.

<sub>EN: On the left there is a serving of other dish. In the bottom right corner there is a plate of tofu and noodle platter. It shows golden fried tofu, green leaves, cubed tofu and green leaves. In the center and at the bottom there are two small bowls of dipping sauce. They show reddish-brown liquid, white bowl, red chili slices and small white specks. The other dish is to the left of the tofu and noodle platter. The tofu and noodle platter is to the right of the dipping sauce. Also visible: wooden chopsticks, green glass, paper napkins and white bowls.</sub>

**[B]** (114 từ, 13/14 chi tiết)

> Ở bên trái có một phần món ăn khác. Ở góc dưới bên phải có một khay tre đựng bún đậu mắm tôm. Nó cho thấy đậu phụ chiên vàng, rau trang trí xanh, đậu phụ chiên khối và rau trang trí xanh. Nó được đặt trên đĩa trắng. Ở giữa và ở phía dưới có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, lát ớt đỏ và tỏi băm. Chúng được đặt ở giữa. món ăn khác nằm ở bên trái của bún đậu mắm tôm. bún đậu mắm tôm nằm ở bên phải của đồ chấm. Cũng có thể thấy: đũa gỗ, cốc nước, bát trắng và khăn giấy.

<sub>EN: On the left there is a serving of other dish. In the bottom right corner there is a bamboo tray of tofu and noodle platter. It shows golden fried tofu, green leafy garnish, fried tofu cubes and green leafy garnish. It is placed on white plate. In the center and at the bottom there are two small bowls of dipping sauce. They show reddish-brown liquid, red chili slices and minced garlic. They are placed in center. The other dish is to the left of the tofu and noodle platter. The tofu and noodle platter is to the right of the dipping sauce. Also visible: wooden chopsticks, glass of water, white bowls and paper napkins.</sub>

**[C]** (137 từ, 22/23 chi tiết)

> Ở bên trái có một phần món ăn khác. Ở góc dưới bên phải có một đĩa bún đậu mắm tôm. Nó cho thấy đậu phụ chiên vàng, lá xanh, đĩa trắng, các khối đậu phụ chiên và lá xanh. Nó được sắp xếp trên đĩa. Ở giữa và ở phía dưới có hai bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, lát ớt đỏ, các đốm trắng, chất lỏng màu nâu đỏ và lát ớt đỏ. Chúng đang nổi trong chất lỏng. món ăn khác nằm ở bên trái của bún đậu mắm tôm. bún đậu mắm tôm nằm ở bên phải của đồ chấm. Các món ăn được đặt trên một chiếc bàn màu nâu đỏ sẫm. Cũng có thể thấy: đũa gỗ, ly đồ uống màu xanh, bát gốm trắng, khăn giấy và gói gia vị. Phông nền cho thấy bối cảnh trong nhà bị làm mờ.

<sub>EN: On the left there is a serving of other dish. In the bottom right corner there is a plate of tofu and noodle platter. It shows golden fried tofu, green leaf, white plate, fried tofu cubes and green leaf. It is arranged on plate. In the center and at the bottom there are two small bowls of dipping sauce. They show reddish-brown liquid, red chili slices, white specks, reddish-brown liquid and red chili slices. They are floating in liquid. The other dish is to the left of the tofu and noodle platter. The tofu and noodle platter is to the right of the dipping sauce. The dishes are set on a dark reddish-brown table. Also visible: wooden chopsticks, glass of green drink, white ceramic bowls, paper napkins and packaged condiment. The background shows a blurred indoor setting.</sub>

## `srcA_H-099_jpg.rf.03f5e9ef6d44778186328703b60486f6.jpg`

Món (nhãn): fried fish, oyster, shrimp, stir-fried vegetables

**[A]** (131 từ, 23/27 chi tiết)

> Ở phía dưới có một đĩa rau xào. Nó cho thấy những cây măng tây xanh, đĩa màu be nhạt và những cây măng tây. Nó được sắp xếp thành một hàng. Ở giữa có một đĩa cá chiên. Nó cho thấy cá nguyên con với lớp da vàng, đồ trang trí lá xanh và những chiếc bát nhỏ màu đen. Nó được sắp xếp trên một chiếc đĩa trắng. Ở bên trái có một khay tre đựng hàu. Nó cho thấy lớp phủ màu nâu vàng, vỏ màu xám và lớp phủ màu vàng. Ở bên phải có một đĩa tôm. Nó cho thấy đồ trang trí lá xanh, đồ trang trí lá xanh và bát nhỏ màu tối. Nó được sắp xếp trên một chiếc đĩa. rau xào nằm bên dưới cá chiên. cá chiên nằm ở bên phải của hàu. Các món ăn được đặt trên một chiếc bàn gỗ.

<sub>EN: At the bottom there is a plate of stir-fried vegetables. It shows green asparagus spears, light beige plate and asparagus spears. It is arranged in a row. In the center there is a plate of fried fish. It shows whole fish with golden skin, green leafy garnish and small black bowls. It is arranged on a white plate. On the left there is a bamboo tray of oyster. It shows golden brown topping, gray shell and golden topping. On the right there is a plate of shrimp. It shows green leaf garnish, green leaf garnish and small dark bowl. It is arranged on a plate. The stir-fried vegetables is below the fried fish. The fried fish is to the right of the oyster. The dishes are set on a wooden table.</sub>

**[B]** (133 từ, 24/29 chi tiết)

> Ở phía dưới có một đĩa rau xào. Nó cho thấy các nhánh măng tây xanh, nhánh măng tây và các miếng tỏi chiên. Nó được đặt trên đĩa. Ở giữa có một đĩa cá chiên. Nó cho thấy cá màu nâu vàng, lá xà lách xanh và thân cá nguyên con. Nó được đặt trên đĩa trắng. Ở bên trái có một phần hàu. Nó cho thấy các con hàu màu xám trắng, thảo mộc xanh và các con hàu màu xám trắng. Nó được đặt trên vỏ sò. Ở bên phải có một đĩa tôm. Nó được đặt trên đĩa. rau xào nằm bên dưới cá chiên. cá chiên nằm ở bên phải của hàu. Cũng có thể thấy: khay phục vụ bằng gỗ, ly bia, giấy gói bằng nhôm và bát nhỏ màu đen. Phông nền cho thấy nội thất nhà hàng bị làm mờ.

<sub>EN: At the bottom there is a plate of stir-fried vegetables. It shows green asparagus spears, asparagus spears and fried garlic pieces. It is placed on plate. In the center there is a plate of fried fish. It shows golden brown fish, green lettuce leaves and whole fish body. It is placed on white plate. On the left there is a serving of oyster. It shows gray white oysters, green herbs and gray white oysters. It is placed on shells. On the right there is a plate of shrimp. It is placed on plate. The stir-fried vegetables is below the fried fish. The fried fish is to the right of the oyster. Also visible: wooden serving board, glass of beer, aluminum foil wrapper and black small bowl. The background shows a blurred restaurant interior.</sub>

**[C]** (132 từ, 35/39 chi tiết)

> Ở phía dưới có một đĩa rau xào. Nó cho thấy măng tây xanh, các miếng màu cam và đĩa trắng. Ở giữa có một đĩa cá chiên. Nó cho thấy da cá màu nâu vàng, xà lách xanh và cá nướng màu nâu đậm. Nó được sắp xếp với xà lách và các món ăn kèm. Ở bên trái có một đĩa hàu. Nó cho thấy vỏ xám thô, lớp phủ màu vàng và lớp phủ màu vàng. Nó được sắp xếp trên đĩa với đũa. Ở bên phải có một đĩa tôm. Nó cho thấy các vết nướng cháy sẫm, đồ trang trí lá xanh và đồ trang trí lá xanh. Nó được sắp xếp trên đĩa với đồ trang trí. rau xào nằm bên dưới cá chiên. cá chiên nằm ở bên phải của hàu. Các món ăn được đặt trên một chiếc bàn gỗ sáng màu.

<sub>EN: At the bottom there is a plate of stir-fried vegetables. It shows green asparagus, orange pieces and white plate. In the center there is a plate of fried fish. It shows golden-brown fish skin, green lettuce and dark brown grilled fish. It is arranged with lettuce and side dishes. On the left there is a plate of oyster. It shows rough gray shell, yellow topping and yellow topping. It is arranged on a plate with chopsticks. On the right there is a plate of shrimp. It shows dark charred grill marks, green leafy garnish and green leafy garnish. It is arranged on plate with garnish. The stir-fried vegetables is below the fried fish. The fried fish is to the right of the oyster. The dishes are set on a light wooden table.</sub>

## `srcA_H-100_jpg.rf.ff29a738f059f7e704f6c3860e027757.jpg`

Món (nhãn): clear vegetable soup, fried fish, roast pork, sliced beef

**[A]** (132 từ, 32/36 chi tiết)

> Ở bên phải có một đĩa thịt bò. Nó cho thấy bàn gỗ màu nâu nhạt, vành đĩa trắng và những lát thịt mỏng. Nó được phục vụ trên đĩa bầu dục. Ở phía trên và ở giữa có hai phần heo quay. Chúng cho thấy thịt màu nâu đỏ, hành tây trắng và xà lách xanh. Chúng là những lát cà chua được sắp xếp xung quanh. Ở góc trên bên trái có một đĩa cá chiên. Nó cho thấy nước sốt đỏ trên cá, lá xà lách xanh và hành lá ở trên cùng. Nó được phục vụ với các món ăn kèm. Ở phía trên có một bát canh. Nó cho thấy rau lá xanh, rau xanh và những lát ớt đỏ. thịt bò nằm ở bên phải của heo quay. heo quay nằm ở bên dưới cá chiên.

<sub>EN: On the right there is a plate of sliced beef. It shows light brown wooden table, white plate rim and thin meat slices. It is served on oval plate. At the top and in the center there are two servings of roast pork. They show reddish-brown meat, white onions and green lettuce. They are sliced tomatoes arranged around. In the top left corner there is a plate of fried fish. It shows red sauce on fish, green lettuce leaves and green onions on top. It is served with side dishes. At the top there is a bowl of clear vegetable soup. It shows green leafy vegetables, leafy green vegetables and red chili slices. The sliced beef is to the right of the roast pork. The roast pork are below the fried fish.</sub>

**[B]** (138 từ, 29/34 chi tiết)

> Ở bên phải có một phần thịt bò. Nó cho thấy những lát thịt màu nâu đỏ, rau lá xanh và rau xanh. Nó được trộn với rau. Ở phía trên và ở giữa có hai phần heo quay. Chúng cho thấy những miếng thịt màu nâu đỏ, cà chua thái lát và hành tây. Chúng được đặt trên đĩa trắng. Ở góc trên bên trái có một phần cá chiên. Nó cho thấy cá màu nâu vàng, rau lá xanh và cá nguyên con. Nó được đặt trên đĩa trắng. Ở phía trên có một bát canh. Nó cho thấy rau lá xanh, nước dùng trong và rau xanh. Nó được đặt trong bát. thịt bò nằm ở bên phải của heo quay. heo quay nằm ở bên dưới cá chiên. Các món ăn được đặt trên một chiếc bàn gỗ màu nâu.

<sub>EN: On the right there is a serving of sliced beef. It shows reddish-brown meat slices, green leafy vegetables and green vegetables. It is mixed with vegetables. At the top and in the center there are two servings of roast pork. They show reddish-brown meat pieces, sliced tomatoes and onions. They are placed on white plate. In the top left corner there is a serving of fried fish. It shows golden brown fish, green leafy vegetable and whole fish. It is placed on white plate. At the top there is a bowl of clear vegetable soup. It shows green leafy vegetables, clear broth and leafy greens. It is placed in bowl. The sliced beef is to the right of the roast pork. The roast pork are below the fried fish. The dishes are set on a brown wooden table.</sub>

**[C]** (138 từ, 39/43 chi tiết)

> Ở bên phải có một đĩa thịt bò. Nó cho thấy những lát thịt màu nâu đỏ, rau lá màu xanh đậm và nước dùng màu vàng nhạt. Nó được sắp xếp trên một chiếc đĩa hình bầu dục màu trắng. Ở phía trên và ở giữa có hai phần heo quay. Chúng cho thấy thịt màu nâu đỏ, lát hành tây vàng và lát cà chua đỏ. Chúng được sắp xếp trên một chiếc đĩa. Ở góc trên bên trái có một đĩa cá chiên. Nó cho thấy nước sốt đỏ, thảo mộc xanh và da cá trắng. Nó được đặt trên đĩa với đồ trang trí. Ở phía trên có một bát canh. Nó cho thấy nước dùng màu xanh trong, rau lá xanh và lát ớt đỏ. Nó đang nổi trong nước dùng. thịt bò nằm ở bên phải của heo quay. heo quay nằm ở bên dưới cá chiên.

<sub>EN: On the right there is a plate of sliced beef. It shows reddish-brown meat slices, dark green leafy vegetables and light yellow broth. It is arranged on a white oval plate. At the top and in the center there are two servings of roast pork. They show reddish-brown meat, yellow onion slices and red tomato slices. They are arranged on a plate. In the top left corner there is a plate of fried fish. It shows red sauce, green herbs and white fish skin. It is placed on plate with garnish. At the top there is a bowl of clear vegetable soup. It shows clear green broth, green leafy vegetables and red chili slices. It is floating in broth. The sliced beef is to the right of the roast pork. The roast pork are below the fried fish.</sub>

## `srcA_H-103_jpg.rf.01c49d87932e274c27afb1a7a03b89cf.jpg`

Món (nhãn): boiled chicken, boiled vegetables, fried fish, other dish, roast pork, shredded salad, shrimp, sticky rice, vietnamese pork ham

**[A]** (139 từ, 48/53 chi tiết)

> Ở phía dưới có một đĩa gà luộc. Nó cho thấy da gà màu vàng nhạt, đồ trang trí màu xanh lá và đồ trang trí màu cam. Nó được sắp xếp trên một chiếc đĩa. Ở góc dưới bên trái có một đĩa rau luộc. Nó cho thấy rau màu xanh đậm bóng loáng, cà rốt cắt thanh màu cam và rau thái lát màu xanh nhạt. Nó là bông cải xanh ở giữa được bao quanh bởi các lát cắt. Ở giữa có một đĩa tôm. Nó cho thấy lớp vỏ màu nâu vàng, đĩa màu trắng và đồ trang trí màu xanh lá. Nó được sắp xếp thành các hàng. Ở bên phải có một đĩa heo quay. Nó cho thấy thịt màu nâu đỏ, rau mùi màu xanh lá và bánh mì màu nâu vàng. Nó là thịt thái lát được trang trí với rau mùi. Ở bên trái có một đĩa cá chiên. Nó cho thấy lớp giấy bạc bọc, bề mặt đĩa màu trắng và cá có da. Nó được bọc trong giấy bạc trên đĩa.

<sub>EN: At the bottom there is a plate of boiled chicken. It shows pale yellow chicken skin, green garnish and orange garnish. It is arranged on a plate. In the bottom left corner there is a plate of boiled vegetables. It shows glossy dark green vegetables, orange carrot sticks and light green sliced vegetables. It is centered broccoli surrounded by slices. In the center there is a plate of shrimp. It shows golden brown crust, white plate and green garnish. It is arranged in rows. On the right there is a plate of roast pork. It shows reddish-brown meat, green parsley and golden-brown buns. It is sliced meat garnished with parsley. On the left there is a plate of fried fish. It shows silver foil wrapping, white plate surface and fish with skin. It is wrapped in foil on plate.</sub>

**[B]** (132 từ, 40/57 chi tiết)

> Ở phía dưới có một đĩa gà luộc. Nó cho thấy lớp da màu vàng nhạt, lá trang trí màu xanh lá cây và những lát cà rốt màu cam. Ở góc dưới bên trái có một đĩa rau luộc. Nó cho thấy bông cải xanh đậm, những thanh cà rốt màu cam và dưa chuột màu xanh nhạt. Nó được sắp xếp gọn gàng xung quanh. Ở giữa có một đĩa tôm. Nó cho thấy các món chiên màu nâu vàng và bắp cải bào sợi. Ở bên phải có một đĩa heo quay. Nó cho thấy các miếng thịt màu nâu đỏ, cành mùi tây xanh và các miếng thịt. Nó được trang trí với mùi tây. Ở bên trái có một phần cá chiên. Nó cho thấy lớp giấy bạc màu bạc, cá bên trong giấy bạc và các loại thảo mộc xanh ở gần đó. Nó được gói trong giấy bạc. Ở bên phải có một phần món ăn khác.

<sub>EN: At the bottom there is a plate of boiled chicken. It shows pale yellow skin, green garnish leaves and orange carrot slices. In the bottom left corner there is a plate of boiled vegetables. It shows dark green broccoli, orange carrot sticks and pale green cucumber. It is neatly arranged around. In the center there is a plate of shrimp. It shows golden brown fried items and shredded cabbage. On the right there is a plate of roast pork. It shows reddish-brown meat pieces, green parsley sprig and meat pieces. It is garnished with parsley. On the left there is a serving of fried fish. It shows silver foil wrapping, fish inside foil and green herbs nearby. It is wrapped in foil. On the right there is a serving of other dish.</sub>

**[C]** (140 từ, 71/76 chi tiết)

> Ở phía dưới có một đĩa gà luộc. Nó cho thấy da gà màu vàng nhạt, thảo mộc xanh và thảo mộc xanh. Nó được sắp xếp trên một chiếc đĩa trắng. Ở góc dưới bên trái có một đĩa rau luộc. Nó cho thấy bông cải xanh đậm, lát dưa chuột xanh nhạt và lát cà rốt màu cam. Nó được sắp xếp theo hình tròn. Ở giữa có một đĩa tôm. Nó cho thấy lớp vỏ chiên màu nâu vàng, phần đế sợi màu vàng nhạt và đĩa trắng. Nó được sắp xếp thành hàng trên đĩa. Ở bên phải có một đĩa heo quay. Nó cho thấy thịt màu nâu đỏ, thảo mộc xanh và các vật phẩm tròn màu vàng. Nó được sắp xếp trên đĩa trắng. Ở bên trái có một phần cá chiên. Nó cho thấy da cá màu nâu vàng, giấy bạc màu bạc sáng và thảo mộc xanh. Nó được gói trong giấy bạc.

<sub>EN: At the bottom there is a plate of boiled chicken. It shows pale yellow chicken skin, green herbs and green herbs. It is arranged on a white plate. In the bottom left corner there is a plate of boiled vegetables. It shows dark green broccoli, light green cucumber slices and orange carrot slices. It is arranged in circular pattern. In the center there is a plate of shrimp. It shows golden brown fried coating, light yellow shredded base and white plate. It is arranged in rows on plate. On the right there is a plate of roast pork. It shows reddish-brown meat, green herbs and golden round items. It is arranged on white plate. On the left there is a serving of fried fish. It shows golden-brown fish skin, shiny silver foil and green herbs. It is wrapped in foil.</sub>

## `srcA_H-104_jpg.rf.abe716729a666f55b468cbe93ad7a06a.jpg`

Món (nhãn): clear vegetable soup, dipping sauce, fresh herbs and greens, shrimp, squid

**[A]** (140 từ, 25/30 chi tiết)

> Ở bên trái có một đĩa tôm. Nó cho thấy bề mặt đĩa trắng, râu và vỏ. Nó được sắp xếp trên một chiếc đĩa. Ở bên phải có một bát rau sống. Nó cho thấy lá màu xanh nhạt, bát trắng và rau lá xanh. Ở góc trên bên trái có một bát canh. Nó cho thấy nước dùng màu nâu trong, các miếng rau màu đỏ và thìa kim loại. Ở giữa có một đĩa mực. Nó cho thấy rau mùi xanh, rau mùi và bát nhỏ. Nó được sắp xếp trên đĩa với bát. Băng qua bàn có bốn bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ và bát màu be nhạt. tôm nằm ở bên trái của rau sống. rau sống nằm ở bên phải của canh.

<sub>EN: On the left there is a plate of shrimp. It shows white plate surface, antennae and shells. It is arranged on a plate. On the right there is a bowl of fresh herbs and greens. It shows light green leaves, white bowl and green leafy vegetables. In the top left corner there is a bowl of clear vegetable soup. It shows clear brown broth, red vegetable pieces and metal spoon. In the center there is a plate of squid. It shows green parsley, parsley and small bowl. It is arranged on plate with bowl. Across the table there are four small bowls of dipping sauce. They show reddish brown liquid and light beige bowl. The shrimp is to the left of the fresh herbs and greens. The fresh herbs and greens is to the right of the clear vegetable soup.</sub>

**[B]** (140 từ, 22/30 chi tiết)

> Ở bên trái có một đĩa tôm. Nó cho thấy đĩa trắng và râu dài. Nó được sắp xếp trên đĩa. Ở bên phải có một bát rau sống. Nó cho thấy rau xanh, giá đỗ trắng và rau xanh. Chúng được trộn lẫn với nhau lỏng lẻo. Ở góc trên bên trái có một bát canh. Nó cho thấy nước dùng màu nâu trong, lát ớt đỏ và lát ớt đỏ. Ở giữa có một đĩa mực. Nó cho thấy bát nhỏ. Nó được đặt trên đĩa. Băng qua bàn có bốn bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ. Chúng được đặt ở giữa. tôm nằm ở bên trái của rau sống. rau sống nằm ở bên phải của canh.

<sub>EN: On the left there is a plate of shrimp. It shows white plate and long antennae. It is arranged on plate. On the right there is a bowl of fresh herbs and greens. It shows green leafy vegetables, white bean sprouts and green leafy vegetables. It is mixed together loosely. In the top left corner there is a bowl of clear vegetable soup. It shows clear brown broth, red chili slice and red chili slice. In the center there is a plate of squid. It shows small bowl. It is placed on plate. Across the table there are four small bowls of dipping sauce. They show reddish brown liquid. They are placed in center. The shrimp is to the left of the fresh herbs and greens. The fresh herbs and greens is to the right of the clear vegetable soup.</sub>

**[C]** (132 từ, 33/34 chi tiết)

> Ở bên trái có một đĩa tôm. Nó cho thấy những chiếc vỏ bóng loáng, đĩa trắng và những chiếc vỏ bóng loáng. Nó được sắp xếp trên đĩa. Ở bên phải có một bát rau sống. Nó cho thấy rau xanh, giá đỗ trắng và rau xanh. Nó được trộn lẫn với nhau. Ở góc trên bên trái có một bát canh. Nó cho thấy nước dùng màu nâu trong, các miếng rau màu đỏ và thìa kim loại. Nó được đặt trong bát. Ở giữa có một đĩa mực. Nó cho thấy thảo mộc xanh, thảo mộc xanh và chất lỏng màu nâu trong bát nhỏ. Nó được rải trên đĩa. Băng qua bàn có bốn bát nhỏ đồ chấm. Chúng cho thấy chất lỏng màu nâu đỏ, vành bát màu be nhạt và chất lỏng. Chúng được chứa trong bát.

<sub>EN: On the left there is a plate of shrimp. It shows shiny shells, white plate and shiny shells. It is arranged on plate. On the right there is a bowl of fresh herbs and greens. It shows green leafy vegetables, white bean sprouts and green leafy vegetables. It is mixed together. In the top left corner there is a bowl of clear vegetable soup. It shows clear brown broth, red vegetable pieces and metal spoon. It is placed in bowl. In the center there is a plate of squid. It shows green herbs, green herbs and brownish liquid in small bowl. It is scattered on plate. Across the table there are four small bowls of dipping sauce. They show reddish-brown liquid, light beige bowl rim and liquid. They are contained in bowl.</sub>

## `srcA_H-106_jpg.rf.698052f8fd2636c5c8bd9e8c9413fd11.jpg`

Món (nhãn): dessert, squid

**[A]** (69 từ, 12/12 chi tiết)

> Ở góc dưới bên phải có một phần món tráng miệng. Ở bên phải có một đĩa mực. Nó cho thấy đĩa trắng, khăn trải bàn đỏ, xúc tu xoăn và đũa. Nó được phục vụ trên một chiếc đĩa. món tráng miệng nằm bên dưới mực. Các món ăn được đặt trên một chiếc bàn màu đỏ. Cũng có thể thấy: đũa gỗ, chai nước, cốc màu xanh lá cây, hộp màu xanh dương và lọ thủy tinh. Phông nền cho thấy một vỉa hè lát đá cuội.

<sub>EN: In the bottom right corner there is a serving of dessert. On the right there is a plate of squid. It shows white plate, red tablecloth, curled tentacles and chopsticks. It is served on a plate. The dessert is below the squid. The dishes are set on a red table. Also visible: wooden chopsticks, water bottle, green cup, blue container and glass jar. The background shows a cobblestone pavement.</sub>

**[B]** (64 từ, 8/8 chi tiết)

> Ở góc dưới bên phải có một phần món tráng miệng. Ở bên phải có một đĩa mực. Nó cho thấy những chiếc xúc tu xoăn. Nó được đặt trên đĩa. món tráng miệng nằm bên dưới mực. Các món ăn được đặt trên một chiếc bàn nhựa màu đỏ. Cũng có thể thấy: đũa gỗ, chai nước nhựa, cốc nhựa màu xanh lá cây và lọ thủy tinh. Phông nền cho thấy một khu vực ngoài trời được lát gạch.

<sub>EN: In the bottom right corner there is a serving of dessert. On the right there is a plate of squid. It shows curled tentacles. It is placed on plate. The dessert is below the squid. The dishes are set on a red plastic table. Also visible: wooden chopsticks, plastic water bottle, green plastic cup and glass jar. The background shows a paved outdoor area.</sub>

**[C]** (80 từ, 13/14 chi tiết)

> Ở góc dưới bên phải có một phần món tráng miệng. Ở bên phải có một đĩa mực. Nó cho thấy các cạnh màu nâu vàng, đĩa trắng, xúc tu xoăn, đũa và mặt bàn màu đỏ. Nó nằm rải rác trên đĩa. món tráng miệng nằm bên dưới mực. Các món ăn được đặt trên một chiếc bàn gỗ màu đỏ. Cũng có thể thấy: đũa gỗ, cốc nhựa màu xanh lá cây, chai nhựa trong suốt, hộp nhựa màu xanh dương và một chiếc ly nhỏ với chất lỏng màu cam. Phông nền cho thấy một vỉa hè bằng đá màu xám.

<sub>EN: In the bottom right corner there is a serving of dessert. On the right there is a plate of squid. It shows golden brown edges, white plate, curled tentacles, chopsticks and red table surface. It is scattered on plate. The dessert is below the squid. The dishes are set on a red wooden table. Also visible: wooden chopsticks, green plastic cup, clear plastic bottle, blue plastic container and small glass with orange liquid. The background shows a gray stone pavement.</sub>

## `srcA_H-107_jpg.rf.ac91f6b82a5cc4eb351cea86640e9122.jpg`

Món (nhãn): boiled vegetables, dessert, dipping sauce, other dish, roasted chicken, shredded salad, sticky rice, stir-fried vegetables, whole crab

**[A]** (133 từ, 48/51 chi tiết)

> Ở bên trái có một phần cua. Nó cho thấy những con côn trùng màu nâu đậm, bát màu trắng và gạo tím. Ở giữa có một đĩa rau luộc. Nó cho thấy rau màu xanh đậm, đũa gỗ màu nâu nhạt và rau màu xanh đậm bóng loáng. Nó được sắp xếp gọn gàng trên đĩa. Ở phía trên có một phần gà quay. Nó cho thấy da gà màu nâu đỏ, lá xanh và các miếng gà. Nó được đặt trên lá chuối. Ở bên trái có một đĩa xôi. Nó cho thấy những hạt gạo tím, đĩa trắng và lá xanh. Nó được phục vụ trên một chiếc đĩa. Ở góc trên bên phải có một đĩa rau xào. Nó cho thấy đế lá xanh, bề mặt gỗ màu nâu nhạt và tay đang cầm đũa. Nó được trộn trên bề mặt lá.

<sub>EN: On the left there is a serving of whole crab. It shows dark brown insects, white bowl and purple rice. In the center there is a plate of boiled vegetables. It shows dark green vegetables, light brown wooden chopsticks and glossy dark green vegetables. It is neatly arranged on plate. At the top there is a serving of roasted chicken. It shows reddish-brown chicken skin, green leaf and chicken pieces. It is placed on banana leaf. On the left there is a plate of sticky rice. It shows purple rice grains, white plate and green leaf. It is served on a plate. In the top right corner there is a plate of stir-fried vegetables. It shows green leaf base, light brown wooden surface and hand holding chopsticks. It is mixed on leaf surface.</sub>

**[B]** (130 từ, 38/48 chi tiết)

> Ở bên trái có một đĩa cua. Nó cho thấy những con côn trùng màu nâu sẫm, rau xanh và những con côn trùng nhỏ màu sẫm. Ở giữa có một đĩa rau luộc. Nó cho thấy rau màu xanh đậm, rau màu xanh đậm và những miếng ớt đỏ. Ở phía trên có một phần gà quay. Nó cho thấy da gà màu nâu đỏ, rau lá xanh và những miếng thịt gà. Nó được đặt trên lá. Ở bên trái có một đĩa xôi. Nó cho thấy lá xanh, gạo tím và lá xanh. Nó được đặt trên lá xanh. Ở góc trên bên phải có một đĩa rau xào. Nó cho thấy đế lá xanh, phần phủ màu nâu thái sợi và đế lá xanh. Ở góc trên bên trái có một đĩa gỏi.

<sub>EN: On the left there is a plate of whole crab. It shows dark brown insects, green vegetables and small dark insects. In the center there is a plate of boiled vegetables. It shows dark green vegetables, dark green vegetables and red chili pieces. At the top there is a serving of roasted chicken. It shows reddish-brown chicken skin, green leafy vegetables and chicken pieces. It is placed on leaf. On the left there is a plate of sticky rice. It shows green leaf, purple rice and green leaf. It is placed on green leaf. In the top right corner there is a plate of stir-fried vegetables. It shows green leaf base, shredded brown topping and green leaf base. In the top left corner there is a plate of shredded salad.</sub>

**[C]** (136 từ, 61/63 chi tiết)

> Ở bên trái có một phần cua. Nó cho thấy côn trùng chiên màu nâu đậm, lá xanh và những miếng ớt đỏ. Nó được rải trên lá. Ở giữa có một đĩa rau luộc. Nó cho thấy rau màu xanh đậm bóng, thân màu xanh nhạt và bát trắng. Nó được sắp xếp gọn gàng trên đĩa. Ở phía trên có một phần gà quay. Nó cho thấy da gà màu nâu đỏ, rau xanh và nước sốt màu nâu nhạt. Nó được sắp xếp trên lá chuối. Ở bên trái có một đĩa xôi. Nó cho thấy gạo tím, phần phủ sợi màu nâu nhạt và nguyên liệu khô màu nâu đậm. Nó được vun thành đống trên đĩa. Ở góc trên bên phải có một đĩa rau xào. Nó cho thấy rau xanh, nguyên liệu sợi màu nâu nhạt và thảo mộc màu xanh đậm.

<sub>EN: On the left there is a serving of whole crab. It shows dark brown fried insects, green leaf and red chili pieces. It is scattered on leaf. In the center there is a plate of boiled vegetables. It shows glossy dark green vegetables, light green stems and white bowl. It is neatly arranged on plate. At the top there is a serving of roasted chicken. It shows reddish-brown chicken skin, green leafy vegetables and light brown sauce. It is arranged on banana leaf. On the left there is a plate of sticky rice. It shows purple rice, light brown shredded topping and dark brown dried ingredient. It is mounded on plate. In the top right corner there is a plate of stir-fried vegetables. It shows green leafy vegetables, light brown shredded ingredient and dark green herbs.</sub>

## `srcA_H-108_JPG.rf.ffcece842962ecf19bb574144c2afb18.jpg`

Món (nhãn): dessert, dipping sauce, other dish, pork offal congee, roast pork, sticky rice, stir-fried vegetables

**[A]** (134 từ, 37/41 chi tiết)

> Trên bàn có năm phần xôi. Chúng cho thấy cụm gạo trắng, cụm gạo đỏ và cụm gạo xanh. Chúng được sắp xếp thành những đống đầy màu sắc. Ở bên trái có một phần món ăn khác. Ở bên phải có một bát cháo lòng. Nó cho thấy vành hoa văn xanh trắng, nước dùng xanh nhạt và thìa trắng. Ở góc trên bên phải có một phần món tráng miệng. Ở bên phải và ở phía dưới có hai phần rau xào. Chúng cho thấy vành hoa văn xanh, rau xanh và hoa trang trí màu cam. Chúng được đặt ở giữa với đồ trang trí xung quanh. Ở bên phải có một đĩa heo quay. Nó cho thấy vành hoa văn xanh trắng, bề mặt thịt màu nâu đỏ và thịt thái lát. Nó được cắt thành những lát dày.

<sub>EN: Across the table there are five servings of sticky rice. They show white rice cluster, red rice cluster and blue rice cluster. They are arranged in colorful piles. On the left there is a serving of other dish. On the right there is a bowl of pork offal congee. It shows blue and white patterned rim, light green broth and white spoon. In the top right corner there is a serving of dessert. On the right and at the bottom there are two servings of stir-fried vegetables. They show blue patterned rim, green leafy vegetables and orange flower garnish. They are centered with garnish around. On the right there is a plate of roast pork. It shows blue and white patterned rim, reddish-brown meat surface and sliced meat. It is cut into thick slices.</sub>

**[B]** (131 từ, 26/32 chi tiết)

> Trên bàn có năm phần xôi. Chúng cho thấy các loại thảo mộc xanh và những chiếc bát trắng nhỏ. Chúng được nhóm lại trên lá. Ở bên trái có một phần món ăn khác. Ở bên phải có một bát cháo lòng. Nó cho thấy súp kem trắng, các mẩu lá xanh và rau xanh. Nó được bao quanh bởi các món ăn kèm. Ở góc trên bên phải có một phần món tráng miệng. Ở bên phải và ở phía dưới có hai phần rau xào. Chúng cho thấy thành phần lá xanh, rau xanh thái nhỏ và các mẩu tỏi phi. Chúng được trộn đều với nhau. Ở bên phải có một đĩa heo quay. Nó cho thấy các lát thịt màu nâu đỏ, các cạnh bề mặt cháy xém và các miếng thịt thái lát. Nó được cắt thành những lát dày.

<sub>EN: Across the table there are five servings of sticky rice. They show green herbs and small white bowls. They are grouped on leaf. On the left there is a serving of other dish. On the right there is a bowl of pork offal congee. It shows white creamy soup, green leafy bits and leafy greens. It is surrounded by side dishes. In the top right corner there is a serving of dessert. On the right and at the bottom there are two servings of stir-fried vegetables. They show green leafy contents, chopped green vegetables and fried garlic bits. They are mixed together evenly. On the right there is a plate of roast pork. It shows reddish-brown meat slices, charred surface edges and sliced meat pieces. It is cut into thick slices.</sub>

**[C]** (135 từ, 46/49 chi tiết)

> Trên bàn có năm phần xôi. Chúng cho thấy gạo trắng, gạo đỏ và gạo xanh. Chúng được xếp thành đống trên lá. Ở bên trái có một phần món ăn khác. Ở bên phải có một bát cháo lòng. Nó cho thấy nước dùng màu xanh lá nhạt, bát trắng với hoa văn xanh và các miếng lá xanh. Nó được đặt trên lá xanh. Ở góc trên bên phải có một phần món tráng miệng. Ở bên phải và ở dưới cùng có hai phần rau xào. Chúng cho thấy rau xanh băm nhỏ, đồ trang trí hình hoa màu cam và đĩa hoa văn xanh trắng. Chúng được sắp xếp theo hình tròn. Ở bên phải có một đĩa heo quay. Nó cho thấy thịt màu nâu đỏ, đĩa hoa văn xanh trắng và đồ trang trí màu cam.

<sub>EN: Across the table there are five servings of sticky rice. They show white rice, red rice and blue rice. They are arranged in mounds on leaf. On the left there is a serving of other dish. On the right there is a bowl of pork offal congee. It shows light green broth, white bowl with blue pattern and green leafy pieces. It is placed on green leaf. In the top right corner there is a serving of dessert. On the right and at the bottom there are two servings of stir-fried vegetables. They show green chopped vegetables, orange flower-shaped garnish and blue and white patterned plate. They are arranged in a circular pattern. On the right there is a plate of roast pork. It shows reddish-brown meat, blue and white patterned plate and orange garnish.</sub>

