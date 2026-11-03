_base_ = 'grounding_dino_swin_t_vifood54_ov_s1_od.py'

# Đánh giá OV generalized (prompt đủ 54 lớp) nhưng 8 lớp novel được gọi bằng `desc`
# (tên tiếng Việt + thuộc tính hình thái đầu tiên trong taxonomy). GT đổi tên tương ứng.
ov_dir = '../grounding_data/vifood54/annotations_ov/'
prompt_classes = ('bánh bèo', 'bánh bột lọc', 'bánh canh', 'bánh chưng', 'bánh cuốn', 'bánh căn', 'bánh giò hình chóp', 'bánh khọt', 'bánh mì', 'bánh pía tròn dẹt', 'bánh tráng', 'bánh tét', 'bánh xèo', 'bánh đúc', 'bún bò Huế', 'bún tươi', 'bún mắm', 'bún riêu', 'bún thịt nướng', 'bún đậu mắm tôm', 'canh', 'cao lầu sợi vàng', 'cháo lòng', 'chả giò', 'cua', 'cá chiên', 'cơm chiên', 'cơm tấm hạt nhỏ', 'gà luộc', 'gỏi', 'gỏi cuốn', 'heo quay', 'hàu', 'hủ tiếu', 'lẩu', 'mì Quảng', 'mực', 'nem chua bọc lá', 'ngao sò', 'phở', 'rau sống', 'súp cua súp sánh', 'thịt bò', 'rau luộc', 'tôm', 'xôi', 'ốc vỏ xoắn', 'món ăn khác', 'rau xào', 'đồ chấm', 'gà quay', 'nem rán', 'món tráng miệng', 'quẩy thanh chiên')
test_dataloader = dict(dataset=dict(metainfo=dict(classes=prompt_classes), ann_file=ov_dir + 'instances_test_desc.json'))
test_evaluator = dict(ann_file=ov_dir + 'instances_test_desc.json')
