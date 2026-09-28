import json
from collections import defaultdict

with open('../grounding_data/vifood/annotations/instances_val.json') as f:
    val_data = json.load(f)

cat_map = {c['id']: c['name'] for c in val_data['categories']}
img_map = {img['id']: img['file_name'] for img in val_data['images']}

img_cats = defaultdict(list)
for ann in val_data['annotations']:
    img_cats[ann['image_id']].append(cat_map[ann['category_id']])

interesting_dishes = ['bánh mì', 'phở', 'bún bò Huế', 'bánh tráng', 'gỏi cuốn', 'bánh xèo', 'cơm tấm']
found = {}
for img_id, cats in img_cats.items():
    for dish in interesting_dishes:
        if dish in cats and dish not in found:
            found[dish] = (img_map[img_id], list(set(cats)))

for dish, (img, all_cats) in found.items():
    print(f"Dish [{dish}]: {img} -> All items: {all_cats}")
