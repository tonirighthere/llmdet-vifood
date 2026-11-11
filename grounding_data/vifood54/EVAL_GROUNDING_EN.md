# Grounding câu tự nhiên trên test ViFood-54 (inference)

- 414 ảnh test; prompt chỉ chứa lớp có mặt; 1 entity = 1 lớp trong câu. IoU ≥ 0.5.
- R@1: box điểm cao nhất của entity đúng; R@n: tỉ lệ box GT tìm được bằng n box điểm cao nhất (n = số box GT của lớp).
- Số entity: names 942, L1 1884, L2 3768, L2_taste 3768

| Mô hình | names R@1 | L1 R@1 | L2 R@1 | L2_taste R@1 | names R@n | L1 R@n | L2 R@n | L2_taste R@n |
|---|---|---|---|---|---|---|---|---|
| B1_EN | 0.860 | 0.716 | 0.612 | 0.641 | 0.846 | 0.686 | 0.616 | 0.630 |
| B3b_EN | 0.859 | 0.808 | 0.830 | 0.827 | 0.850 | 0.798 | 0.813 | 0.807 |

## R@1 theo lớp: L2 so với names (lớp ≥ 5 entity test)

| lớp | B1_EN names / L2 / L2_taste | B3b_EN names / L2 / L2_taste |
|---|---|---|
| dipping sauce | 0.92 / 0.60 / 0.61 | 0.92 / 0.89 / 0.90 |
| fresh herbs and greens | 0.93 / 0.66 / 0.77 | 0.92 / 0.89 / 0.90 |
| other dish | 0.62 / 0.46 / 0.47 | 0.68 / 0.57 / 0.58 |
| mini crispy pancakes | 0.91 / 0.54 / 0.54 | 0.91 / 0.88 / 0.87 |
| quang noodles | 0.95 / 0.80 / 0.84 | 1.00 / 0.95 / 0.97 |
| shrimp | 0.67 / 0.62 / 0.63 | 0.76 / 0.62 / 0.61 |
| sizzling crepe | 1.00 / 0.95 / 0.93 | 1.00 / 0.99 / 0.99 |
| rice paper | 1.00 / 0.47 / 0.61 | 1.00 / 1.00 / 1.00 |
| cylindrical rice cake | 1.00 / 0.33 / 0.36 | 1.00 / 0.97 / 0.96 |
| vietnamese pork ham | 0.67 / 0.32 / 0.32 | 0.61 / 0.62 / 0.57 |
| pork offal congee | 1.00 / 0.75 / 0.63 | 1.00 / 1.00 / 0.97 |
| roast pork | 0.94 / 0.77 / 0.81 | 0.88 / 0.97 / 0.98 |
| fresh spring rolls | 0.88 / 0.56 / 0.67 | 0.94 / 0.91 / 0.88 |
| sticky rice | 0.94 / 0.81 / 0.83 | 0.88 / 0.86 / 0.86 |
| baguette sandwich | 0.93 / 0.53 / 0.60 | 0.93 / 0.85 / 0.90 |
| rice vermicelli | 1.00 / 0.42 / 0.40 | 1.00 / 0.80 / 0.80 |
| cao lau noodles | 1.00 / 0.65 / 0.57 | 1.00 / 0.98 / 0.95 |
| pho noodle soup | 1.00 / 0.92 / 0.93 | 1.00 / 1.00 / 1.00 |
| fried rice | 1.00 / 0.93 / 0.97 | 1.00 / 1.00 / 1.00 |
| crab noodle soup | 1.00 / 0.69 / 0.73 | 1.00 / 1.00 / 1.00 |
| hue beef noodle soup | 1.00 / 0.75 / 0.77 | 0.92 / 1.00 / 1.00 |
| clear vegetable soup | 0.85 / 0.54 / 0.52 | 0.77 / 0.73 / 0.73 |
| oyster | 0.83 / 0.62 / 0.54 | 0.75 / 0.73 / 0.67 |
| tapioca dumplings | 0.67 / 0.46 / 0.65 | 0.67 / 0.83 / 0.83 |
| tofu and noodle platter | 1.00 / 0.83 / 0.92 | 1.00 / 0.92 / 0.94 |
| roasted chicken | 0.83 / 0.69 / 0.71 | 0.83 / 0.75 / 0.79 |
| sea snails | 0.73 / 0.50 / 0.52 | 0.73 / 0.59 / 0.61 |
| mini savory pancakes | 0.73 / 0.57 / 0.68 | 0.73 / 0.64 / 0.68 |
| broken rice | 0.27 / 0.77 / 0.73 | 0.27 / 0.52 / 0.43 |
| hu tieu noodles | 1.00 / 0.80 / 0.86 | 1.00 / 0.91 / 0.93 |
| squid | 0.30 / 0.35 / 0.33 | 0.30 / 0.35 / 0.35 |
| stir-fried vegetables | 0.70 / 0.47 / 0.45 | 0.60 / 0.70 / 0.68 |
| fried dough sticks | 1.00 / 0.90 / 0.95 | 1.00 / 0.97 / 1.00 |
| steamed rice cakes | 0.70 / 0.20 / 0.20 | 0.60 / 0.80 / 0.72 |
| steamed rice rolls | 0.70 / 0.80 / 0.80 | 0.70 / 0.75 / 0.75 |
| shredded salad | 0.67 / 0.61 / 0.58 | 0.78 / 0.67 / 0.58 |
| fried fish | 0.67 / 0.81 / 0.81 | 0.89 / 0.86 / 0.86 |
| boiled chicken | 0.78 / 0.61 / 0.56 | 0.67 / 0.42 / 0.47 |
| pyramid rice dumpling | 1.00 / 0.78 / 0.75 | 0.89 / 0.81 / 0.89 |
| dessert | 0.00 / 0.09 / 0.12 | 0.25 / 0.34 / 0.28 |
| pia pastry | 1.00 / 0.28 / 0.44 | 1.00 / 0.97 / 1.00 |
| square rice cake | 0.88 / 0.41 / 0.47 | 0.88 / 0.88 / 0.81 |
| fried spring rolls | 0.75 / 0.28 / 0.25 | 0.75 / 0.56 / 0.47 |
| thick noodle soup | 0.88 / 0.66 / 0.69 | 0.88 / 0.88 / 0.88 |
| boiled vegetables | 0.75 / 0.47 / 0.44 | 0.75 / 0.66 / 0.59 |
| whole crab | 0.86 / 0.79 / 0.82 | 0.86 / 0.79 / 0.82 |
| clams and scallops | 0.71 / 0.46 / 0.43 | 0.71 / 0.39 / 0.36 |
| fermented pork | 0.86 / 0.54 / 0.50 | 0.86 / 0.79 / 0.79 |
| grilled pork noodle bowl | 0.57 / 0.50 / 0.54 | 0.57 / 0.54 / 0.50 |
| fermented fish noodle soup | 1.00 / 0.71 / 0.82 | 1.00 / 1.00 / 1.00 |
| steamed savory cake | 0.71 / 0.25 / 0.25 | 0.71 / 0.71 / 0.68 |
| crab soup | 1.00 / 0.86 / 0.86 | 1.00 / 1.00 / 1.00 |
| sliced beef | 0.86 / 0.57 / 0.57 | 0.71 / 0.86 / 0.86 |
| hotpot | 0.60 / 0.65 / 0.70 | 0.60 / 0.60 / 0.70 |
