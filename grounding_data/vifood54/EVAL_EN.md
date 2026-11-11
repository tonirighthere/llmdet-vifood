# Đánh giá trên `instances_test.json` (414 ảnh, 1898 box, 54 lớp)

## Tổng

| Mô hình | mAP | 95% CI (bootstrap ảnh) | AP50 | AP75 | AP_s | AP_m | AP_l | AR@100 |
|---|---|---|---|---|---|---|---|---|
| B1_v2_VI | 0.315 | - | 0.394 | 0.357 | 0.604 | 0.301 | 0.324 | 0.808 |
| B3b_VI | 0.323 | - | 0.405 | 0.366 | 0.284 | 0.303 | 0.333 | 0.816 |
| B1_EN | 0.384 | - | 0.475 | 0.433 | 0.584 | 0.368 | 0.396 | 0.827 |
| B3b_EN | 0.387 | - | 0.484 | 0.432 | 0.225 | 0.338 | 0.398 | 0.824 |

## AP theo lớp (sắp theo AP của B3b_EN, tăng dần)

| lớp | #GT test | B1_v2_VI AP / AP50 | B3b_VI AP / AP50 | B1_EN AP / AP50 | B3b_EN AP / AP50 |
|---|---|---|---|---|---|
| dessert | 12 | 0.016 / 0.017 | 0.017 / 0.018 | 0.003 / 0.003 | 0.002 / 0.002 |
| sliced beef | 11 | 0.004 / 0.005 | 0.003 / 0.004 | 0.015 / 0.018 | 0.004 / 0.006 |
| grilled pork noodle bowl | 9 | 0.086 / 0.096 | 0.041 / 0.046 | 0.038 / 0.052 | 0.027 / 0.037 |
| squid | 22 | 0.026 / 0.040 | 0.034 / 0.054 | 0.034 / 0.048 | 0.029 / 0.042 |
| boiled chicken | 11 | 0.124 / 0.142 | 0.062 / 0.079 | 0.087 / 0.100 | 0.079 / 0.091 |
| boiled vegetables | 8 | 0.130 / 0.150 | 0.115 / 0.133 | 0.129 / 0.157 | 0.096 / 0.122 |
| vietnamese pork ham | 40 | 0.087 / 0.105 | 0.068 / 0.085 | 0.107 / 0.136 | 0.153 / 0.196 |
| clams and scallops | 17 | 0.094 / 0.115 | 0.110 / 0.136 | 0.248 / 0.299 | 0.186 / 0.222 |
| other dish | 65 | 0.172 / 0.237 | 0.153 / 0.208 | 0.220 / 0.280 | 0.196 / 0.246 |
| roast pork | 22 | 0.107 / 0.148 | 0.121 / 0.149 | 0.222 / 0.258 | 0.200 / 0.228 |
| shrimp | 34 | 0.154 / 0.175 | 0.172 / 0.196 | 0.211 / 0.270 | 0.206 / 0.243 |
| quang noodles | 24 | 0.284 / 0.347 | 0.238 / 0.285 | 0.210 / 0.292 | 0.216 / 0.291 |
| hotpot | 5 | 0.004 / 0.006 | 0.007 / 0.010 | 0.237 / 0.245 | 0.227 / 0.230 |
| thick noodle soup | 12 | 0.260 / 0.296 | 0.279 / 0.349 | 0.245 / 0.276 | 0.248 / 0.283 |
| fried spring rolls | 12 | 0.232 / 0.310 | 0.222 / 0.346 | 0.275 / 0.373 | 0.259 / 0.351 |
| clear vegetable soup | 14 | 0.055 / 0.063 | 0.073 / 0.086 | 0.213 / 0.254 | 0.270 / 0.305 |
| hu tieu noodles | 30 | 0.166 / 0.199 | 0.126 / 0.156 | 0.282 / 0.354 | 0.275 / 0.336 |
| square rice cake | 59 | 0.179 / 0.277 | 0.193 / 0.303 | 0.297 / 0.496 | 0.278 / 0.494 |
| rice vermicelli | 23 | 0.313 / 0.456 | 0.295 / 0.417 | 0.237 / 0.346 | 0.279 / 0.363 |
| cao lau noodles | 29 | 0.166 / 0.216 | 0.202 / 0.263 | 0.301 / 0.384 | 0.315 / 0.400 |
| oyster | 33 | 0.118 / 0.141 | 0.123 / 0.150 | 0.309 / 0.362 | 0.325 / 0.403 |
| sea snails | 20 | 0.332 / 0.387 | 0.335 / 0.389 | 0.319 / 0.386 | 0.327 / 0.388 |
| stir-fried vegetables | 11 | 0.076 / 0.103 | 0.100 / 0.119 | 0.348 / 0.388 | 0.333 / 0.371 |
| fried fish | 9 | 0.369 / 0.420 | 0.388 / 0.438 | 0.355 / 0.398 | 0.336 / 0.375 |
| steamed rice rolls | 20 | 0.386 / 0.478 | 0.447 / 0.517 | 0.319 / 0.359 | 0.357 / 0.396 |
| fermented fish noodle soup | 20 | 0.189 / 0.217 | 0.166 / 0.189 | 0.376 / 0.420 | 0.358 / 0.399 |
| shredded salad | 10 | 0.035 / 0.048 | 0.063 / 0.083 | 0.352 / 0.440 | 0.370 / 0.460 |
| roasted chicken | 22 | 0.221 / 0.317 | 0.223 / 0.303 | 0.382 / 0.486 | 0.373 / 0.481 |
| crab noodle soup | 21 | 0.287 / 0.314 | 0.396 / 0.429 | 0.388 / 0.445 | 0.376 / 0.423 |
| steamed rice cakes | 71 | 0.569 / 0.808 | 0.493 / 0.730 | 0.500 / 0.758 | 0.387 / 0.830 |
| mini savory pancakes | 42 | 0.317 / 0.375 | 0.372 / 0.423 | 0.405 / 0.461 | 0.401 / 0.459 |
| hue beef noodle soup | 23 | 0.291 / 0.394 | 0.323 / 0.465 | 0.420 / 0.535 | 0.412 / 0.541 |
| fermented pork | 42 | 0.301 / 0.473 | 0.388 / 0.596 | 0.370 / 0.525 | 0.418 / 0.599 |
| fresh spring rolls | 65 | 0.400 / 0.732 | 0.411 / 0.727 | 0.435 / 0.740 | 0.418 / 0.748 |
| steamed savory cake | 59 | 0.342 / 0.380 | 0.357 / 0.388 | 0.382 / 0.438 | 0.431 / 0.480 |
| fried dough sticks | 12 | 0.258 / 0.274 | 0.242 / 0.274 | 0.435 / 0.494 | 0.440 / 0.497 |
| sizzling crepe | 38 | 0.498 / 0.577 | 0.503 / 0.602 | 0.495 / 0.597 | 0.486 / 0.602 |
| crab soup | 11 | 0.673 / 0.807 | 0.659 / 0.810 | 0.492 / 0.601 | 0.497 / 0.612 |
| sticky rice | 25 | 0.343 / 0.408 | 0.366 / 0.436 | 0.461 / 0.540 | 0.501 / 0.589 |
| broken rice | 13 | 0.499 / 0.602 | 0.433 / 0.530 | 0.552 / 0.596 | 0.502 / 0.588 |
| pyramid rice dumpling | 15 | 0.301 / 0.421 | 0.358 / 0.498 | 0.522 / 0.704 | 0.537 / 0.732 |
| rice paper | 30 | 0.629 / 0.732 | 0.640 / 0.745 | 0.505 / 0.644 | 0.569 / 0.710 |
| tapioca dumplings | 66 | 0.537 / 0.792 | 0.568 / 0.820 | 0.579 / 0.820 | 0.595 / 0.852 |
| dipping sauce | 233 | 0.633 / 0.785 | 0.632 / 0.769 | 0.622 / 0.761 | 0.604 / 0.733 |
| baguette sandwich | 42 | 0.542 / 0.571 | 0.537 / 0.566 | 0.649 / 0.683 | 0.608 / 0.640 |
| whole crab | 11 | 0.049 / 0.064 | 0.083 / 0.109 | 0.492 / 0.614 | 0.611 / 0.747 |
| fresh herbs and greens | 154 | 0.637 / 0.813 | 0.634 / 0.793 | 0.655 / 0.830 | 0.645 / 0.815 |
| mini crispy pancakes | 134 | 0.675 / 0.807 | 0.691 / 0.837 | 0.670 / 0.796 | 0.680 / 0.817 |
| cylindrical rice cake | 68 | 0.658 / 0.804 | 0.663 / 0.814 | 0.669 / 0.838 | 0.690 / 0.860 |
| pho noodle soup | 18 | 0.337 / 0.359 | 0.499 / 0.528 | 0.701 / 0.783 | 0.726 / 0.811 |
| fried rice | 19 | 0.734 / 0.857 | 0.740 / 0.869 | 0.723 / 0.852 | 0.739 / 0.857 |
| tofu and noodle platter | 24 | 0.765 / 0.950 | 0.715 / 0.887 | 0.690 / 0.830 | 0.743 / 0.898 |
| pia pastry | 33 | 0.724 / 0.946 | 0.732 / 0.963 | 0.751 / 0.958 | 0.760 / 0.971 |
| pork offal congee | 25 | 0.642 / 0.714 | 0.658 / 0.737 | 0.794 / 0.923 | 0.802 / 0.936 |

## B1_v2_VI: nhầm lẫn (score ≥ 0.3, IoU ≥ 0.5)

| GT | dự đoán thành | số box | % GT của lớp |
|---|---|---|---|
| square rice cake | cylindrical rice cake | 20 | 34% |
| fermented pork | fresh spring rolls | 11 | 26% |
| sticky rice | fried rice | 9 | 36% |
| clams and scallops | sea snails | 8 | 47% |
| hu tieu noodles | other dish | 7 | 23% |
| baguette sandwich | rice paper | 7 | 17% |
| sizzling crepe | baguette sandwich | 5 | 13% |
| oyster | sizzling crepe | 5 | 15% |
| fresh spring rolls | fried spring rolls | 5 | 8% |
| cylindrical rice cake | square rice cake | 5 | 7% |
| crab noodle soup | hue beef noodle soup | 5 | 24% |
| clear vegetable soup | dipping sauce | 5 | 36% |
| rice paper | sizzling crepe | 4 | 13% |
| pyramid rice dumpling | square rice cake | 4 | 27% |
| hu tieu noodles | pork offal congee | 4 | 13% |
| vietnamese pork ham | rice paper | 3 | 8% |
| stir-fried vegetables | boiled vegetables | 3 | 27% |
| steamed savory cake | steamed rice rolls | 3 | 5% |
| shredded salad | stir-fried vegetables | 3 | 30% |
| oyster | pyramid rice dumpling | 3 | 9% |

### B1_v2_VI: cặp theo dõi

| cặp | lý do | a→b | b→a | bỏ sót a | bỏ sót b |
|---|---|---|---|---|---|
| chả giò ↔ nem rán | giống hình | 0/40 | 0/12 | 34/40 | 6/12 |
| bánh căn ↔ bánh khọt | giống hình | 1/42 | 0/134 | 33/42 | 31/134 |
| bánh bèo ↔ bánh bột lọc | giống hình | 0/71 | 0/66 | 7/71 | 14/66 |
| gỏi ↔ gỏi cuốn | giống hình + lồng chữ | 0/10 | 0/65 | 6/10 | 12/65 |
| quẩy ↔ gà quay | dính chữ (quay) | 0/12 | 0/22 | 11/12 | 12/22 |
| quẩy ↔ heo quay | dính chữ (quay) | 1/12 | 0/22 | 11/12 | 15/22 |
| lẩu ↔ cao lầu | dính chữ (lau) | 0/5 | 0/29 | 3/5 | 22/29 |
| bánh căn ↔ bánh canh | dính chữ (can) | 0/42 | 0/12 | 33/42 | 1/12 |
| canh ↔ bánh canh | lồng chữ | 0/14 | 0/12 | 8/14 | 1/12 |
| cua ↔ súp cua | lồng chữ | 0/11 | 0/11 | 8/11 | 2/11 |
| tôm ↔ bún đậu mắm tôm | lồng chữ | 0/34 | 0/24 | 29/34 | 1/24 |
| cá chiên ↔ cơm chiên | gần trùng chữ | 0/9 | 0/19 | 3/9 | 1/19 |
| mực ↔ ốc | gần trùng chữ | 1/22 | 0/20 | 19/22 | 9/20 |
| lẩu ↔ tôm | gần trùng chữ | 0/5 | 0/34 | 3/5 | 29/34 |

## B3b_VI: nhầm lẫn (score ≥ 0.3, IoU ≥ 0.5)

| GT | dự đoán thành | số box | % GT của lớp |
|---|---|---|---|
| square rice cake | cylindrical rice cake | 20 | 34% |
| sticky rice | fried rice | 9 | 36% |
| fermented pork | fresh spring rolls | 9 | 21% |
| clams and scallops | sea snails | 8 | 47% |
| crab noodle soup | hue beef noodle soup | 6 | 29% |
| clear vegetable soup | dipping sauce | 6 | 43% |
| sizzling crepe | baguette sandwich | 5 | 13% |
| roasted chicken | fried fish | 5 | 23% |
| fresh spring rolls | fried spring rolls | 5 | 8% |
| sizzling crepe | rice paper | 4 | 11% |
| rice paper | sizzling crepe | 4 | 13% |
| pyramid rice dumpling | square rice cake | 4 | 27% |
| hue beef noodle soup | fermented fish noodle soup | 4 | 17% |
| hu tieu noodles | other dish | 4 | 13% |
| crab noodle soup | pork offal congee | 4 | 19% |
| baguette sandwich | rice paper | 4 | 10% |
| vietnamese pork ham | rice paper | 3 | 8% |
| stir-fried vegetables | boiled vegetables | 3 | 27% |
| roasted chicken | roast pork | 3 | 14% |
| oyster | pyramid rice dumpling | 3 | 9% |

### B3b_VI: cặp theo dõi

| cặp | lý do | a→b | b→a | bỏ sót a | bỏ sót b |
|---|---|---|---|---|---|
| chả giò ↔ nem rán | giống hình | 0/40 | 0/12 | 35/40 | 8/12 |
| bánh căn ↔ bánh khọt | giống hình | 0/42 | 0/134 | 31/42 | 34/134 |
| bánh bèo ↔ bánh bột lọc | giống hình | 0/71 | 0/66 | 18/71 | 14/66 |
| gỏi ↔ gỏi cuốn | giống hình + lồng chữ | 0/10 | 0/65 | 8/10 | 16/65 |
| quẩy ↔ gà quay | dính chữ (quay) | 0/12 | 0/22 | 12/12 | 11/22 |
| quẩy ↔ heo quay | dính chữ (quay) | 0/12 | 0/22 | 12/12 | 19/22 |
| lẩu ↔ cao lầu | dính chữ (lau) | 0/5 | 0/29 | 4/5 | 25/29 |
| bánh căn ↔ bánh canh | dính chữ (can) | 0/42 | 0/12 | 31/42 | 1/12 |
| canh ↔ bánh canh | lồng chữ | 0/14 | 0/12 | 6/14 | 1/12 |
| cua ↔ súp cua | lồng chữ | 0/11 | 0/11 | 8/11 | 2/11 |
| tôm ↔ bún đậu mắm tôm | lồng chữ | 0/34 | 0/24 | 28/34 | 5/24 |
| cá chiên ↔ cơm chiên | gần trùng chữ | 0/9 | 0/19 | 5/9 | 1/19 |
| mực ↔ ốc | gần trùng chữ | 0/22 | 0/20 | 22/22 | 10/20 |
| lẩu ↔ tôm | gần trùng chữ | 0/5 | 0/34 | 4/5 | 28/34 |

## B1_EN: nhầm lẫn (score ≥ 0.3, IoU ≥ 0.5)

| GT | dự đoán thành | số box | % GT của lớp |
|---|---|---|---|
| square rice cake | cylindrical rice cake | 17 | 29% |
| fermented pork | fresh spring rolls | 9 | 21% |
| clams and scallops | sea snails | 9 | 53% |
| steamed savory cake | steamed rice rolls | 8 | 14% |
| rice vermicelli | steamed rice rolls | 8 | 35% |
| quang noodles | cao lau noodles | 8 | 33% |
| cylindrical rice cake | square rice cake | 7 | 10% |
| cao lau noodles | quang noodles | 7 | 24% |
| sizzling crepe | cylindrical rice cake | 6 | 16% |
| mini crispy pancakes | oyster | 6 | 4% |
| hue beef noodle soup | crab noodle soup | 6 | 26% |
| thick noodle soup | crab soup | 5 | 42% |
| sticky rice | fried rice | 5 | 20% |
| rice paper | sizzling crepe | 5 | 17% |
| mini savory pancakes | baguette sandwich | 5 | 12% |
| fermented pork | square rice cake | 5 | 12% |
| tapioca dumplings | mini crispy pancakes | 4 | 6% |
| other dish | boiled chicken | 4 | 6% |
| grilled pork noodle bowl | steamed rice rolls | 4 | 44% |
| fresh spring rolls | steamed rice rolls | 4 | 6% |

### B1_EN: cặp theo dõi

| cặp | lý do | a→b | b→a | bỏ sót a | bỏ sót b |
|---|---|---|---|---|---|
| chả giò ↔ nem rán | giống hình | 0/40 | 0/12 | 36/40 | 6/12 |
| bánh căn ↔ bánh khọt | giống hình | 0/42 | 3/134 | 23/42 | 29/134 |
| bánh bèo ↔ bánh bột lọc | giống hình | 0/71 | 0/66 | 18/71 | 20/66 |
| gỏi ↔ gỏi cuốn | giống hình + lồng chữ | 0/10 | 0/65 | 4/10 | 6/65 |
| quẩy ↔ gà quay | dính chữ (quay) | 0/12 | 0/22 | 3/12 | 10/22 |
| quẩy ↔ heo quay | dính chữ (quay) | 0/12 | 0/22 | 3/12 | 8/22 |
| lẩu ↔ cao lầu | dính chữ (lau) | 0/5 | 0/29 | 2/5 | 6/29 |
| bánh căn ↔ bánh canh | dính chữ (can) | 0/42 | 0/12 | 23/42 | 0/12 |
| canh ↔ bánh canh | lồng chữ | 0/14 | 1/12 | 6/14 | 0/12 |
| cua ↔ súp cua | lồng chữ | 0/11 | 0/11 | 4/11 | 0/11 |
| tôm ↔ bún đậu mắm tôm | lồng chữ | 0/34 | 0/24 | 24/34 | 5/24 |
| cá chiên ↔ cơm chiên | gần trùng chữ | 0/9 | 0/19 | 3/9 | 2/19 |
| mực ↔ ốc | gần trùng chữ | 1/22 | 0/20 | 14/22 | 8/20 |
| lẩu ↔ tôm | gần trùng chữ | 0/5 | 0/34 | 2/5 | 24/34 |

## B3b_EN: nhầm lẫn (score ≥ 0.3, IoU ≥ 0.5)

| GT | dự đoán thành | số box | % GT của lớp |
|---|---|---|---|
| square rice cake | cylindrical rice cake | 18 | 31% |
| fermented pork | fresh spring rolls | 10 | 24% |
| quang noodles | cao lau noodles | 9 | 38% |
| cylindrical rice cake | square rice cake | 9 | 13% |
| clams and scallops | sea snails | 9 | 53% |
| thick noodle soup | crab noodle soup | 7 | 58% |
| rice vermicelli | steamed rice rolls | 7 | 30% |
| hue beef noodle soup | crab noodle soup | 7 | 30% |
| sizzling crepe | cylindrical rice cake | 6 | 16% |
| mini crispy pancakes | oyster | 6 | 4% |
| clear vegetable soup | dipping sauce | 6 | 43% |
| cao lau noodles | quang noodles | 6 | 21% |
| cao lau noodles | other dish | 6 | 21% |
| sticky rice | fried rice | 5 | 20% |
| rice paper | sizzling crepe | 5 | 17% |
| fermented pork | square rice cake | 5 | 12% |
| vietnamese pork ham | square rice cake | 4 | 10% |
| oyster | square rice cake | 4 | 12% |
| oyster | sea snails | 4 | 12% |
| other dish | boiled chicken | 4 | 6% |

### B3b_EN: cặp theo dõi

| cặp | lý do | a→b | b→a | bỏ sót a | bỏ sót b |
|---|---|---|---|---|---|
| chả giò ↔ nem rán | giống hình | 0/40 | 0/12 | 31/40 | 6/12 |
| bánh căn ↔ bánh khọt | giống hình | 0/42 | 3/134 | 27/42 | 29/134 |
| bánh bèo ↔ bánh bột lọc | giống hình | 0/71 | 0/66 | 19/71 | 22/66 |
| gỏi ↔ gỏi cuốn | giống hình + lồng chữ | 0/10 | 0/65 | 4/10 | 8/65 |
| quẩy ↔ gà quay | dính chữ (quay) | 0/12 | 0/22 | 4/12 | 11/22 |
| quẩy ↔ heo quay | dính chữ (quay) | 0/12 | 0/22 | 4/12 | 8/22 |
| lẩu ↔ cao lầu | dính chữ (lau) | 0/5 | 0/29 | 1/5 | 5/29 |
| bánh căn ↔ bánh canh | dính chữ (can) | 0/42 | 0/12 | 27/42 | 0/12 |
| canh ↔ bánh canh | lồng chữ | 0/14 | 1/12 | 4/14 | 0/12 |
| cua ↔ súp cua | lồng chữ | 0/11 | 0/11 | 4/11 | 0/11 |
| tôm ↔ bún đậu mắm tôm | lồng chữ | 0/34 | 0/24 | 24/34 | 10/24 |
| cá chiên ↔ cơm chiên | gần trùng chữ | 0/9 | 0/19 | 2/9 | 2/19 |
| mực ↔ ốc | gần trùng chữ | 1/22 | 0/20 | 13/22 | 6/20 |
| lẩu ↔ tôm | gần trùng chữ | 0/5 | 0/34 | 1/5 | 24/34 |
