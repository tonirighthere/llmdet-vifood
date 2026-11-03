_base_ = 'grounding_dino_swin_t_vifood54_ov_s1_od.py'

# Đánh giá OV generalized (prompt đủ 54 lớp) nhưng 8 lớp novel được gọi bằng `en`
# (tên tiếng Anh trong taxonomy). GT đổi tên tương ứng.
ov_dir = '../grounding_data/vifood54/annotations_ov/'
prompt_classes = ('bánh bèo', 'bánh bột lọc', 'bánh canh', 'bánh chưng', 'bánh cuốn', 'bánh căn', 'pyramid rice dumpling', 'bánh khọt', 'bánh mì', 'pia pastry', 'bánh tráng', 'bánh tét', 'bánh xèo', 'bánh đúc', 'bún bò Huế', 'bún tươi', 'bún mắm', 'bún riêu', 'bún thịt nướng', 'bún đậu mắm tôm', 'canh', 'cao lau noodles', 'cháo lòng', 'chả giò', 'cua', 'cá chiên', 'cơm chiên', 'broken rice', 'gà luộc', 'gỏi', 'gỏi cuốn', 'heo quay', 'hàu', 'hủ tiếu', 'lẩu', 'mì Quảng', 'mực', 'fermented pork', 'ngao sò', 'phở', 'rau sống', 'crab soup', 'thịt bò', 'rau luộc', 'tôm', 'xôi', 'sea snails', 'món ăn khác', 'rau xào', 'đồ chấm', 'gà quay', 'nem rán', 'món tráng miệng', 'fried dough sticks')
test_dataloader = dict(dataset=dict(metainfo=dict(classes=prompt_classes), ann_file=ov_dir + 'instances_test_en.json'))
test_evaluator = dict(ann_file=ov_dir + 'instances_test_en.json')
