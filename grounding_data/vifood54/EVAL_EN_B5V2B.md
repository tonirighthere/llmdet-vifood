# Đánh giá trên `instances_test.json` (414 ảnh, 1898 box, 54 lớp)

## Tổng

| Mô hình | mAP | 95% CI (bootstrap ảnh) | AP50 | AP75 | AP_s | AP_m | AP_l | AR@100 |
|---|---|---|---|---|---|---|---|---|
| B1_EN | 0.384 | 0.369–0.431 | 0.475 | 0.433 | 0.584 | 0.368 | 0.396 | 0.827 |
| B3b_EN | 0.387 | 0.374–0.434 | 0.484 | 0.432 | 0.225 | 0.338 | 0.398 | 0.824 |
| B5b_best | 0.389 | 0.376–0.435 | 0.484 | 0.436 | 0.218 | 0.346 | 0.400 | 0.828 |
| B5b_last | 0.388 | 0.375–0.435 | 0.484 | 0.433 | 0.218 | 0.342 | 0.400 | 0.827 |

## So ghép cặp với B3b_EN (bootstrap 300 lần, cùng mẫu ảnh)

| Mô hình | ΔmAP (điểm) | 95% CI của Δ | P(Δ > 0) | Kết luận |
|---|---|---|---|---|
| B1_EN | -0.003 | -0.012 … +0.005 | 0.28 | chưa phân biệt được |
| B5b_best | +0.002 | -0.004 … +0.007 | 0.75 | chưa phân biệt được |
| B5b_last | +0.001 | -0.004 … +0.005 | 0.63 | chưa phân biệt được |

## AP theo tần suất lớp (số ảnh train) — tương ứng APr / APc / APf của LVIS

| Nhóm | số lớp | B1_EN AP / AP50 | B3b_EN AP / AP50 | B5b_best AP / AP50 | B5b_last AP / AP50 |
|---|---|---|---|---|---|
| hiếm (≤60 ảnh train) | 13 | 0.295 / 0.371 | 0.300 / 0.379 | 0.298 / 0.374 | 0.296 / 0.371 |
| thường | 33 | 0.403 / 0.495 | 0.406 / 0.507 | 0.409 / 0.509 | 0.409 / 0.510 |
| phổ biến (≥151) | 8 | 0.449 / 0.559 | 0.450 / 0.557 | 0.454 / 0.563 | 0.453 / 0.562 |

## AP theo lớp (sắp theo AP của B5b_last, tăng dần)

| lớp | #GT test | B1_EN AP / AP50 | B3b_EN AP / AP50 | B5b_best AP / AP50 | B5b_last AP / AP50 |
|---|---|---|---|---|---|
| dessert | 12 | 0.003 / 0.003 | 0.002 / 0.002 | 0.002 / 0.003 | 0.002 / 0.003 |
| sliced beef | 11 | 0.015 / 0.018 | 0.004 / 0.006 | 0.003 / 0.005 | 0.004 / 0.006 |
| grilled pork noodle bowl | 9 | 0.038 / 0.052 | 0.027 / 0.037 | 0.030 / 0.041 | 0.030 / 0.041 |
| squid | 22 | 0.034 / 0.048 | 0.029 / 0.042 | 0.032 / 0.046 | 0.032 / 0.047 |
| boiled chicken | 11 | 0.087 / 0.100 | 0.079 / 0.091 | 0.083 / 0.096 | 0.087 / 0.100 |
| boiled vegetables | 8 | 0.129 / 0.157 | 0.099 / 0.126 | 0.104 / 0.130 | 0.099 / 0.127 |
| vietnamese pork ham | 40 | 0.107 / 0.136 | 0.153 / 0.196 | 0.150 / 0.185 | 0.151 / 0.185 |
| other dish | 65 | 0.219 / 0.280 | 0.196 / 0.246 | 0.185 / 0.237 | 0.185 / 0.237 |
| clams and scallops | 17 | 0.248 / 0.299 | 0.186 / 0.222 | 0.209 / 0.251 | 0.205 / 0.247 |
| roast pork | 22 | 0.222 / 0.258 | 0.200 / 0.228 | 0.203 / 0.231 | 0.208 / 0.236 |
| shrimp | 34 | 0.211 / 0.270 | 0.206 / 0.243 | 0.207 / 0.246 | 0.210 / 0.249 |
| quang noodles | 24 | 0.210 / 0.292 | 0.216 / 0.291 | 0.240 / 0.327 | 0.225 / 0.305 |
| hotpot | 5 | 0.237 / 0.245 | 0.227 / 0.230 | 0.231 / 0.235 | 0.231 / 0.235 |
| thick noodle soup | 12 | 0.245 / 0.276 | 0.248 / 0.283 | 0.250 / 0.287 | 0.233 / 0.267 |
| fried spring rolls | 12 | 0.275 / 0.373 | 0.259 / 0.351 | 0.240 / 0.321 | 0.240 / 0.322 |
| clear vegetable soup | 14 | 0.213 / 0.254 | 0.270 / 0.305 | 0.257 / 0.291 | 0.265 / 0.301 |
| hu tieu noodles | 30 | 0.284 / 0.357 | 0.275 / 0.336 | 0.255 / 0.313 | 0.269 / 0.330 |
| rice vermicelli | 23 | 0.237 / 0.346 | 0.278 / 0.363 | 0.275 / 0.381 | 0.271 / 0.369 |
| square rice cake | 59 | 0.297 / 0.496 | 0.278 / 0.494 | 0.276 / 0.464 | 0.275 / 0.463 |
| cao lau noodles | 29 | 0.301 / 0.384 | 0.315 / 0.400 | 0.314 / 0.401 | 0.320 / 0.406 |
| sea snails | 20 | 0.319 / 0.385 | 0.327 / 0.388 | 0.331 / 0.394 | 0.331 / 0.400 |
| stir-fried vegetables | 11 | 0.348 / 0.388 | 0.333 / 0.371 | 0.340 / 0.378 | 0.338 / 0.375 |
| oyster | 33 | 0.309 / 0.362 | 0.325 / 0.403 | 0.333 / 0.406 | 0.340 / 0.414 |
| fried fish | 9 | 0.355 / 0.398 | 0.336 / 0.375 | 0.346 / 0.389 | 0.348 / 0.391 |
| steamed rice rolls | 20 | 0.319 / 0.359 | 0.357 / 0.396 | 0.363 / 0.407 | 0.365 / 0.408 |
| fermented fish noodle soup | 20 | 0.376 / 0.420 | 0.358 / 0.399 | 0.365 / 0.405 | 0.366 / 0.406 |
| roasted chicken | 22 | 0.382 / 0.486 | 0.373 / 0.481 | 0.377 / 0.483 | 0.369 / 0.473 |
| shredded salad | 10 | 0.352 / 0.440 | 0.370 / 0.460 | 0.367 / 0.438 | 0.369 / 0.441 |
| steamed rice cakes | 71 | 0.500 / 0.758 | 0.387 / 0.830 | 0.395 / 0.839 | 0.387 / 0.833 |
| crab noodle soup | 21 | 0.388 / 0.445 | 0.376 / 0.424 | 0.390 / 0.453 | 0.392 / 0.457 |
| mini savory pancakes | 42 | 0.405 / 0.461 | 0.401 / 0.459 | 0.395 / 0.447 | 0.400 / 0.452 |
| fermented pork | 42 | 0.370 / 0.525 | 0.418 / 0.600 | 0.402 / 0.579 | 0.405 / 0.577 |
| fresh spring rolls | 65 | 0.435 / 0.740 | 0.418 / 0.748 | 0.408 / 0.737 | 0.408 / 0.732 |
| steamed savory cake | 59 | 0.382 / 0.438 | 0.431 / 0.480 | 0.435 / 0.483 | 0.435 / 0.483 |
| fried dough sticks | 12 | 0.435 / 0.494 | 0.440 / 0.497 | 0.444 / 0.503 | 0.437 / 0.499 |
| hue beef noodle soup | 23 | 0.420 / 0.535 | 0.412 / 0.541 | 0.441 / 0.579 | 0.438 / 0.582 |
| crab soup | 11 | 0.492 / 0.601 | 0.497 / 0.612 | 0.503 / 0.620 | 0.477 / 0.584 |
| sizzling crepe | 38 | 0.495 / 0.597 | 0.486 / 0.602 | 0.504 / 0.612 | 0.505 / 0.625 |
| broken rice | 13 | 0.552 / 0.596 | 0.502 / 0.588 | 0.502 / 0.572 | 0.515 / 0.587 |
| sticky rice | 25 | 0.461 / 0.540 | 0.501 / 0.589 | 0.529 / 0.615 | 0.521 / 0.606 |
| whole crab | 11 | 0.492 / 0.614 | 0.611 / 0.747 | 0.547 / 0.672 | 0.550 / 0.675 |
| pyramid rice dumpling | 15 | 0.522 / 0.704 | 0.537 / 0.732 | 0.565 / 0.745 | 0.553 / 0.745 |
| rice paper | 30 | 0.505 / 0.644 | 0.569 / 0.710 | 0.572 / 0.720 | 0.575 / 0.723 |
| tapioca dumplings | 66 | 0.578 / 0.818 | 0.595 / 0.852 | 0.596 / 0.852 | 0.597 / 0.851 |
| dipping sauce | 233 | 0.622 / 0.761 | 0.604 / 0.733 | 0.602 / 0.727 | 0.603 / 0.729 |
| baguette sandwich | 42 | 0.649 / 0.683 | 0.608 / 0.640 | 0.613 / 0.647 | 0.609 / 0.642 |
| fresh herbs and greens | 154 | 0.655 / 0.830 | 0.645 / 0.815 | 0.642 / 0.815 | 0.640 / 0.815 |
| cylindrical rice cake | 68 | 0.669 / 0.838 | 0.690 / 0.860 | 0.678 / 0.847 | 0.679 / 0.848 |
| mini crispy pancakes | 134 | 0.670 / 0.795 | 0.680 / 0.817 | 0.682 / 0.816 | 0.679 / 0.816 |
| pho noodle soup | 18 | 0.701 / 0.783 | 0.726 / 0.811 | 0.720 / 0.806 | 0.727 / 0.815 |
| fried rice | 19 | 0.723 / 0.852 | 0.739 / 0.857 | 0.744 / 0.857 | 0.744 / 0.859 |
| tofu and noodle platter | 24 | 0.689 / 0.829 | 0.743 / 0.898 | 0.748 / 0.904 | 0.747 / 0.903 |
| pia pastry | 33 | 0.751 / 0.958 | 0.760 / 0.971 | 0.762 / 0.972 | 0.764 / 0.973 |
| pork offal congee | 25 | 0.794 / 0.923 | 0.802 / 0.936 | 0.801 / 0.937 | 0.803 / 0.940 |

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

## B5b_best: nhầm lẫn (score ≥ 0.3, IoU ≥ 0.5)

| GT | dự đoán thành | số box | % GT của lớp |
|---|---|---|---|
| square rice cake | cylindrical rice cake | 16 | 27% |
| cylindrical rice cake | square rice cake | 10 | 15% |
| quang noodles | cao lau noodles | 9 | 38% |
| fermented pork | fresh spring rolls | 9 | 21% |
| clams and scallops | sea snails | 8 | 47% |
| sizzling crepe | cylindrical rice cake | 6 | 16% |
| rice vermicelli | steamed rice rolls | 6 | 26% |
| oyster | square rice cake | 6 | 18% |
| mini crispy pancakes | oyster | 6 | 4% |
| hu tieu noodles | pho noodle soup | 6 | 20% |
| clear vegetable soup | dipping sauce | 6 | 43% |
| cao lau noodles | quang noodles | 6 | 21% |
| thick noodle soup | crab noodle soup | 5 | 42% |
| sticky rice | fried rice | 5 | 20% |
| fermented pork | square rice cake | 5 | 12% |
| cao lau noodles | other dish | 5 | 17% |
| rice paper | sizzling crepe | 4 | 13% |
| oyster | sea snails | 4 | 12% |
| other dish | boiled chicken | 4 | 6% |
| hue beef noodle soup | crab noodle soup | 4 | 17% |

### B5b_best: cặp theo dõi

| cặp | lý do | a→b | b→a | bỏ sót a | bỏ sót b |
|---|---|---|---|---|---|
| chả giò ↔ nem rán | giống hình | 0/40 | 0/12 | 32/40 | 6/12 |
| bánh căn ↔ bánh khọt | giống hình | 0/42 | 3/134 | 27/42 | 28/134 |
| bánh bèo ↔ bánh bột lọc | giống hình | 0/71 | 0/66 | 19/71 | 24/66 |
| gỏi ↔ gỏi cuốn | giống hình + lồng chữ | 0/10 | 0/65 | 4/10 | 9/65 |
| quẩy ↔ gà quay | dính chữ (quay) | 0/12 | 0/22 | 3/12 | 11/22 |
| quẩy ↔ heo quay | dính chữ (quay) | 0/12 | 0/22 | 3/12 | 8/22 |
| lẩu ↔ cao lầu | dính chữ (lau) | 0/5 | 0/29 | 1/5 | 6/29 |
| bánh căn ↔ bánh canh | dính chữ (can) | 0/42 | 0/12 | 27/42 | 0/12 |
| canh ↔ bánh canh | lồng chữ | 0/14 | 1/12 | 4/14 | 0/12 |
| cua ↔ súp cua | lồng chữ | 0/11 | 0/11 | 4/11 | 1/11 |
| tôm ↔ bún đậu mắm tôm | lồng chữ | 0/34 | 0/24 | 25/34 | 9/24 |
| cá chiên ↔ cơm chiên | gần trùng chữ | 0/9 | 0/19 | 1/9 | 2/19 |
| mực ↔ ốc | gần trùng chữ | 1/22 | 0/20 | 15/22 | 7/20 |
| lẩu ↔ tôm | gần trùng chữ | 0/5 | 0/34 | 1/5 | 25/34 |

## B5b_last: nhầm lẫn (score ≥ 0.3, IoU ≥ 0.5)

| GT | dự đoán thành | số box | % GT của lớp |
|---|---|---|---|
| square rice cake | cylindrical rice cake | 16 | 27% |
| quang noodles | cao lau noodles | 9 | 38% |
| fermented pork | fresh spring rolls | 9 | 21% |
| cylindrical rice cake | square rice cake | 9 | 13% |
| clams and scallops | sea snails | 8 | 47% |
| rice vermicelli | steamed rice rolls | 7 | 30% |
| sizzling crepe | cylindrical rice cake | 6 | 16% |
| mini crispy pancakes | oyster | 6 | 4% |
| clear vegetable soup | dipping sauce | 6 | 43% |
| cao lau noodles | quang noodles | 6 | 21% |
| thick noodle soup | crab noodle soup | 5 | 42% |
| sticky rice | fried rice | 5 | 20% |
| oyster | square rice cake | 5 | 15% |
| hue beef noodle soup | crab noodle soup | 5 | 22% |
| hu tieu noodles | pho noodle soup | 5 | 17% |
| fermented pork | square rice cake | 5 | 12% |
| cao lau noodles | other dish | 5 | 17% |
| rice paper | sizzling crepe | 4 | 13% |
| oyster | sea snails | 4 | 12% |
| other dish | boiled chicken | 4 | 6% |

### B5b_last: cặp theo dõi

| cặp | lý do | a→b | b→a | bỏ sót a | bỏ sót b |
|---|---|---|---|---|---|
| chả giò ↔ nem rán | giống hình | 0/40 | 0/12 | 32/40 | 6/12 |
| bánh căn ↔ bánh khọt | giống hình | 0/42 | 3/134 | 29/42 | 28/134 |
| bánh bèo ↔ bánh bột lọc | giống hình | 0/71 | 0/66 | 19/71 | 24/66 |
| gỏi ↔ gỏi cuốn | giống hình + lồng chữ | 0/10 | 0/65 | 4/10 | 9/65 |
| quẩy ↔ gà quay | dính chữ (quay) | 0/12 | 0/22 | 3/12 | 12/22 |
| quẩy ↔ heo quay | dính chữ (quay) | 0/12 | 0/22 | 3/12 | 8/22 |
| lẩu ↔ cao lầu | dính chữ (lau) | 0/5 | 0/29 | 1/5 | 6/29 |
| bánh căn ↔ bánh canh | dính chữ (can) | 0/42 | 0/12 | 29/42 | 0/12 |
| canh ↔ bánh canh | lồng chữ | 0/14 | 1/12 | 4/14 | 0/12 |
| cua ↔ súp cua | lồng chữ | 0/11 | 0/11 | 4/11 | 0/11 |
| tôm ↔ bún đậu mắm tôm | lồng chữ | 0/34 | 0/24 | 24/34 | 10/24 |
| cá chiên ↔ cơm chiên | gần trùng chữ | 0/9 | 0/19 | 1/9 | 2/19 |
| mực ↔ ốc | gần trùng chữ | 1/22 | 0/20 | 13/22 | 6/20 |
| lẩu ↔ tôm | gần trùng chữ | 0/5 | 0/34 | 1/5 | 24/34 |
