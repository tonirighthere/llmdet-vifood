_base_ = 'grounding_dino_swin_t_vifood54_ov_s1_od.py'

# Đánh giá OV chuẩn: prompt CHỈ gồm 8 tên lớp novel (không cạnh tranh với tên base).
ov_dir = '../grounding_data/vifood54/annotations_ov/'
novel_classes = ('bánh giò', 'bánh pía', 'cao lầu', 'cơm tấm', 'nem chua', 'súp cua', 'ốc', 'quẩy')
test_dataloader = dict(dataset=dict(metainfo=dict(classes=novel_classes),
                                    ann_file=ov_dir + 'instances_test_novel.json'))
test_evaluator = dict(ann_file=ov_dir + 'instances_test_novel.json')
