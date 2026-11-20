# Open-vocabulary trên test ViFood-54

- Novel (8): pyramid rice dumpling, pia pastry, cao lau noodles, broken rice, fermented pork, crab soup, sea snails, fried dough sticks
- Base: 46 lớp. Prompt test đủ 54 tên (generalized): lớp novel phải thắng cả lớp base trong prompt.
- `*` = đã thấy lớp novel khi train (không phải OV, chỉ để làm trần trên).

| Mô hình | mAP (54) | AP_base | AP_novel | AP50_novel | AR@100_novel |
|---|---|---|---|---|---|
| B0_EN | 0.084 | 0.093 | 0.031 | 0.037 | 0.556 |
| OV_S1_EN | 0.330 | 0.372 | 0.090 | 0.108 | 0.743 |
| OV_W_EN | 0.335 | 0.378 | 0.089 | 0.108 | 0.735 |
| B3b_EN* | 0.387 | 0.372 | 0.475 | 0.599 | 0.825 |

## AP theo lớp novel (AP / AP50)

| lớp | B0_EN | OV_S1_EN | OV_W_EN | B3b_EN* |
|---|---|---|---|---|
| pyramid rice dumpling | 0.002 / 0.003 | 0.013 / 0.017 | 0.011 / 0.014 | 0.537 / 0.732 |
| pia pastry | 0.025 / 0.034 | 0.073 / 0.095 | 0.086 / 0.109 | 0.760 / 0.971 |
| cao lau noodles | 0.042 / 0.056 | 0.235 / 0.303 | 0.233 / 0.302 | 0.315 / 0.400 |
| broken rice | 0.002 / 0.004 | 0.009 / 0.011 | 0.011 / 0.013 | 0.502 / 0.588 |
| fermented pork | 0.000 / 0.000 | 0.003 / 0.004 | 0.000 / 0.000 | 0.418 / 0.600 |
| crab soup | 0.011 / 0.014 | 0.053 / 0.064 | 0.079 / 0.097 | 0.497 / 0.612 |
| sea snails | 0.010 / 0.012 | 0.079 / 0.094 | 0.071 / 0.087 | 0.327 / 0.388 |
| fried dough sticks | 0.156 / 0.170 | 0.251 / 0.277 | 0.218 / 0.238 | 0.440 / 0.497 |
