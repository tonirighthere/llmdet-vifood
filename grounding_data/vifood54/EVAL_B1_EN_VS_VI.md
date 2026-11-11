# Đánh giá trên `instances_test.json` (414 ảnh, 1898 box, 54 lớp)

## Tổng

| Mô hình | mAP | 95% CI (bootstrap ảnh) | AP50 | AP75 | AP_s | AP_m | AP_l | AR@100 |
|---|---|---|---|---|---|---|---|---|
| B1_v2_VI | 0.315 | - | 0.394 | 0.357 | 0.604 | 0.301 | 0.324 | 0.808 |
| B1_EN | 0.384 | - | 0.475 | 0.433 | 0.584 | 0.368 | 0.396 | 0.827 |

## AP theo lớp (sắp theo AP của B1_EN, tăng dần)

| lớp | #GT test | B1_v2_VI AP / AP50 | B1_EN AP / AP50 |
|---|---|---|---|
| dessert | 12 | 0.016 / 0.017 | 0.003 / 0.003 |
| sliced beef | 11 | 0.004 / 0.005 | 0.015 / 0.018 |
| squid | 22 | 0.026 / 0.040 | 0.034 / 0.048 |
| grilled pork noodle bowl | 9 | 0.086 / 0.096 | 0.038 / 0.052 |
| boiled chicken | 11 | 0.124 / 0.142 | 0.087 / 0.100 |
| vietnamese pork ham | 40 | 0.087 / 0.105 | 0.107 / 0.136 |
| boiled vegetables | 8 | 0.130 / 0.150 | 0.129 / 0.157 |
| quang noodles | 24 | 0.284 / 0.347 | 0.210 / 0.292 |
| shrimp | 34 | 0.154 / 0.175 | 0.211 / 0.270 |
| clear vegetable soup | 14 | 0.055 / 0.063 | 0.213 / 0.254 |
| other dish | 65 | 0.172 / 0.237 | 0.220 / 0.280 |
| roast pork | 22 | 0.107 / 0.148 | 0.222 / 0.258 |
| rice vermicelli | 23 | 0.313 / 0.456 | 0.237 / 0.346 |
| hotpot | 5 | 0.004 / 0.006 | 0.237 / 0.245 |
| thick noodle soup | 12 | 0.260 / 0.296 | 0.245 / 0.276 |
| clams and scallops | 17 | 0.094 / 0.115 | 0.248 / 0.299 |
| fried spring rolls | 12 | 0.232 / 0.310 | 0.275 / 0.373 |
| hu tieu noodles | 30 | 0.166 / 0.199 | 0.282 / 0.354 |
| square rice cake | 59 | 0.179 / 0.277 | 0.297 / 0.496 |
| cao lau noodles | 29 | 0.166 / 0.216 | 0.301 / 0.384 |
| oyster | 33 | 0.118 / 0.141 | 0.309 / 0.362 |
| steamed rice rolls | 20 | 0.386 / 0.478 | 0.319 / 0.359 |
| sea snails | 20 | 0.332 / 0.387 | 0.319 / 0.386 |
| stir-fried vegetables | 11 | 0.076 / 0.103 | 0.348 / 0.388 |
| shredded salad | 10 | 0.035 / 0.048 | 0.352 / 0.440 |
| fried fish | 9 | 0.369 / 0.420 | 0.355 / 0.398 |
| fermented pork | 42 | 0.301 / 0.473 | 0.370 / 0.525 |
| fermented fish noodle soup | 20 | 0.189 / 0.217 | 0.376 / 0.420 |
| steamed savory cake | 59 | 0.342 / 0.380 | 0.382 / 0.438 |
| roasted chicken | 22 | 0.221 / 0.317 | 0.382 / 0.486 |
| crab noodle soup | 21 | 0.287 / 0.314 | 0.388 / 0.445 |
| mini savory pancakes | 42 | 0.317 / 0.375 | 0.405 / 0.461 |
| hue beef noodle soup | 23 | 0.291 / 0.394 | 0.420 / 0.535 |
| fresh spring rolls | 65 | 0.400 / 0.732 | 0.435 / 0.740 |
| fried dough sticks | 12 | 0.258 / 0.274 | 0.435 / 0.494 |
| sticky rice | 25 | 0.343 / 0.408 | 0.461 / 0.540 |
| crab soup | 11 | 0.673 / 0.807 | 0.492 / 0.601 |
| whole crab | 11 | 0.049 / 0.064 | 0.492 / 0.614 |
| sizzling crepe | 38 | 0.498 / 0.577 | 0.495 / 0.597 |
| steamed rice cakes | 71 | 0.569 / 0.808 | 0.500 / 0.758 |
| rice paper | 30 | 0.629 / 0.732 | 0.505 / 0.644 |
| pyramid rice dumpling | 15 | 0.301 / 0.421 | 0.522 / 0.704 |
| broken rice | 13 | 0.499 / 0.602 | 0.552 / 0.596 |
| tapioca dumplings | 66 | 0.537 / 0.792 | 0.579 / 0.820 |
| dipping sauce | 233 | 0.633 / 0.785 | 0.622 / 0.761 |
| baguette sandwich | 42 | 0.542 / 0.571 | 0.649 / 0.683 |
| fresh herbs and greens | 154 | 0.637 / 0.813 | 0.655 / 0.830 |
| cylindrical rice cake | 68 | 0.658 / 0.804 | 0.669 / 0.838 |
| mini crispy pancakes | 134 | 0.675 / 0.807 | 0.670 / 0.796 |
| tofu and noodle platter | 24 | 0.765 / 0.950 | 0.690 / 0.830 |
| pho noodle soup | 18 | 0.337 / 0.359 | 0.701 / 0.783 |
| fried rice | 19 | 0.734 / 0.857 | 0.723 / 0.852 |
| pia pastry | 33 | 0.724 / 0.946 | 0.751 / 0.958 |
| pork offal congee | 25 | 0.642 / 0.714 | 0.794 / 0.923 |

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
