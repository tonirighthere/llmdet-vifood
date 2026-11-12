#!/usr/bin/env python3
"""
vifood54_core.py
================
Lõi suy luận cho demo ViFood-54 (Pha 6), tách khỏi giao diện để test được:

- `detect(img, model, thr)`        prompt đủ 54 tên lớp (giống lúc đánh giá COCO)
- `ground(img, model, sentence)`   tìm món theo câu tiếng Việt: tên lớp / tên gọi khác trong câu được
                                   ghi tokens_positive, model khoanh box cho từng cụm (như eval_grounding)
- `Nutrition`                      dinh dưỡng theo nutrition_vifood54.json, hệ số khẩu phần theo nhóm món
                                   trong taxonomy (món nước, nước chấm, rau, món đĩa) và diện tích box
- `draw(img, items)`               vẽ box + nhãn tiếng Việt có dấu (PIL, không dùng cv2.putText)

Taxonomy (`scripts/vifood54/taxonomy.json`) là nguồn tên lớp, tên gọi khác và nhóm món.
"""
import json
import os
import re
import sys

import numpy as np
import torch
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TAXONOMY_PATH = os.path.join(ROOT, 'scripts/vifood54/taxonomy.json')
NUTRITION_PATH = os.path.join(HERE, 'nutrition_vifood54.json')
CONFIG = os.path.join(HERE, 'configs/grounding_dino_swin_t_vifood54_b1_od.py')        # prompt tên Việt
CONFIG_EN = os.path.join(HERE, 'configs/grounding_dino_swin_t_vifood54_b1_od_en.py')  # prompt tên Anh
FONT_PATH = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

sys.path.insert(0, os.path.join(ROOT, 'scripts/vifood54/captions'))
from en_names import PROMPT_EN  # noqa: E402  tên lớp Việt -> tên Anh đưa vào BERT (mô hình *-EN)

# Giao diện, taxonomy và dinh dưỡng luôn dùng tên Việt. Mô hình `lang='en'` chỉ khác ở chuỗi đưa vào BERT:
# detect() / ground() tự đổi tên Việt -> tên Anh (PROMPT_EN) rồi trả kết quả theo tên Việt.
_W = os.path.join(HERE, 'work_dirs')
_ALL_MODELS = {
    'B3b-EN: OD + caption, prompt tiếng Anh (tốt nhất)': dict(
        ckpt=os.path.join(_W, 'vifood54_b3b_ft_en/best_coco_bbox_mAP_iter_7000.pth'), config=CONFIG_EN, lang='en'),
    'B1-EN: OD + negative, prompt tiếng Anh': dict(
        ckpt=os.path.join(_W, 'vifood54_b1_od_en/best_coco_bbox_mAP_iter_16000.pth'), config=CONFIG_EN, lang='en'),
    'B3b: OD + caption hình thái (tiếng Việt)': dict(
        ckpt=os.path.join(_W, 'vifood54_b3b_ft/best_coco_bbox_mAP_iter_6000.pth'), config=CONFIG, lang='vi'),
    'B1-v2: OD + negative (tiếng Việt)': dict(
        ckpt=os.path.join(_W, 'vifood54_b1_od_v2/best_coco_bbox_mAP_iter_16000.pth'), config=CONFIG, lang='vi'),
    'B0: zero-shot (chưa fine-tune)': dict(
        ckpt=os.path.join(ROOT, 'huggingface/mm_grounding_dino/'
                                'grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth'),
        config=CONFIG, lang='vi'),
}
# chỉ hiện mô hình có checkpoint trên máy này (thứ tự trên = thứ tự ưu tiên làm mặc định)
MODELS = {k: v for k, v in _ALL_MODELS.items() if os.path.exists(v['ckpt'])} or _ALL_MODELS


def is_en(model_name):
    return MODELS[model_name]['lang'] == 'en'


with open(TAXONOMY_PATH, encoding='utf-8') as f:
    TAXONOMY = json.load(f)['classes']
CLASS_NAMES = [c['name'] for c in TAXONOMY]
BY_NAME = {c['name']: c for c in TAXONOMY}

# tên lớp + tên gọi khác -> tên lớp; khớp cụm dài trước ('bún bò Huế' trước 'bún')
_SURFACE = {}
for c in TAXONOMY:
    for s in [c['name']] + c['aliases']:
        _SURFACE.setdefault(s.lower(), c['name'])
_SURFACE_RE = re.compile(
    r'(?<!\w)(' + '|'.join(re.escape(s) for s in sorted(_SURFACE, key=len, reverse=True)) + r')(?!\w)',
    re.IGNORECASE)


# ───────────────────────────── model ─────────────────────────────

_LOADED = {}


def load_model(name):
    if name not in _LOADED:
        from mmdet.apis import init_detector
        from mmengine.dataset import Compose
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        model = init_detector(MODELS[name]['config'], MODELS[name]['ckpt'], device=device)
        steps = [dict(t) for t in model.cfg.test_dataloader.dataset.pipeline if t['type'] != 'LoadAnnotations']
        steps[0] = dict(type='LoadImageFromNDArray')
        steps[-1]['meta_keys'] = ('img_id', 'img_path', 'ori_shape', 'img_shape', 'scale_factor',
                                  'text', 'custom_entities', 'tokens_positive')
        _LOADED[name] = (model, Compose(steps))
    return _LOADED[name]


def _run(model_name, img_rgb, text, tokens_positive=None):
    from mmengine.dataset import pseudo_collate
    model, pipeline = load_model(model_name)
    data = dict(img=np.ascontiguousarray(img_rgb[:, :, ::-1]), img_id=0, text=text,
                custom_entities=tokens_positive is None)
    if tokens_positive is not None:
        data['tokens_positive'] = tokens_positive
    with torch.no_grad():
        pred = model.test_step(pseudo_collate([pipeline(data)]))[0].pred_instances
    return pred.bboxes.cpu().numpy(), pred.scores.cpu().numpy(), pred.labels.cpu().numpy()


def _nms(items, iou_thr=0.55):
    kept = []
    for it in sorted(items, key=lambda x: -x['score']):
        if all(it['name'] != k['name'] or _iou(it['box'], k['box']) <= iou_thr for k in kept):
            kept.append(it)
    return kept


def _iou(a, b):
    ix = max(0.0, min(a[2], b[2]) - max(a[0], b[0]))
    iy = max(0.0, min(a[3], b[3]) - max(a[1], b[1]))
    inter = ix * iy
    u = (a[2] - a[0]) * (a[3] - a[1]) + (b[2] - b[0]) * (b[3] - b[1]) - inter
    return inter / u if u > 0 else 0.0


def detect(img_rgb, model_name, thr=0.3, classes=None, return_best=False):
    """Nhận diện với prompt là `classes` (tên Việt; mặc định đủ 54 lớp, giống lúc đánh giá).
    -> list {'name', 'box', 'score'}; return_best thêm dict tên lớp -> điểm box cao nhất."""
    classes = list(classes or CLASS_NAMES)
    prompt = [PROMPT_EN[c] for c in classes] if is_en(model_name) else classes
    boxes, scores, labels = _run(model_name, img_rgb, tuple(prompt))
    best = {}
    for s, l in zip(scores, labels):
        best[classes[int(l)]] = max(best.get(classes[int(l)], 0.0), float(s))
    items = _nms([{'name': classes[int(l)], 'box': [float(v) for v in b], 'score': float(s)}
                  for b, s, l in zip(boxes, scores, labels) if s >= thr])
    return (items, best) if return_best else items


def detect_open(img_rgb, model_name, extra, known_items, thr=0.3, max_names=5):
    """Món NGOÀI 54 lớp do VLM gọi tên (thử nghiệm từ vựng mở). extra: list {'name_vi', 'name_en'}.
    Prompt chỉ gồm các tên mới (mô hình EN dùng name_en) nên không có lớp đã học để cạnh tranh -> bỏ box trùng
    (IoU > 0.5) với món đã nhận diện. -> list {'name' (tên Việt VLM đặt), 'box', 'score', 'open': True}."""
    extra = [e for e in extra if e.get('name_vi') and (e.get('name_en') or not is_en(model_name))][:max_names]
    if not extra:
        return []
    prompt = [e['name_en'].lower() if is_en(model_name) else e['name_vi'] for e in extra]
    boxes, scores, labels = _run(model_name, img_rgb, tuple(prompt))
    items = _nms([{'name': extra[int(l)]['name_vi'], 'box': [float(v) for v in b], 'score': float(s), 'open': True}
                  for b, s, l in zip(boxes, scores, labels) if s >= thr])
    return [it for it in items if all(_iou(it['box'], k['box']) <= 0.5 for k in known_items)]


def parse_sentence(sentence):
    """Tìm tên lớp / tên gọi khác trong câu. -> list {'surface', 'name', 'span'} theo thứ tự xuất hiện."""
    out = []
    for m in _SURFACE_RE.finditer(sentence):
        out.append({'surface': m.group(0), 'name': _SURFACE[m.group(0).lower()], 'span': [m.start(), m.end()]})
    return out


def ground(img_rgb, model_name, sentence, thr=0.3):
    """Tìm món theo câu. Mỗi cụm tên món là một entity; luôn trả box điểm cao nhất của entity
    (nếu ≥ 0.1) và thêm các box khác ≥ thr. -> (entities, items)."""
    ents = parse_sentence(sentence)
    if not ents:
        return [], []
    if is_en(model_name):
        # Mô hình EN không đọc được câu tiếng Việt: prompt = tên Anh của từng cụm tên món trong câu
        # ("pho noodle soup. dipping sauce."), mỗi cụm một entity. (R@1 chỉ-tên của B3b-EN: 0.859.)
        text, spans = '', []
        for e in ents:
            name = PROMPT_EN[e['name']]
            spans.append([[len(text), len(text) + len(name)]])
            text += name + '. '
        text = text.strip()
    else:
        text = sentence if sentence.rstrip().endswith('.') else sentence.rstrip() + '.'
        spans = [[e['span']] for e in ents]
    boxes, scores, labels = _run(model_name, img_rgb, text, spans)
    items = []
    for j, e in enumerate(ents):
        idx = np.where(labels == j)[0]
        idx = idx[np.argsort(-scores[idx])]
        for rank, k in enumerate(idx):
            if (rank == 0 and scores[k] >= 0.1) or scores[k] >= thr:
                items.append({'name': e['name'], 'surface': e['surface'], 'entity': j,
                              'box': [float(v) for v in boxes[k]], 'score': float(scores[k]), 'top1': rank == 0})
    return ents, _nms(items)


# ───────────────────────────── dinh dưỡng ─────────────────────────────

class Nutrition:
    """Dinh dưỡng 1 khẩu phần chuẩn × hệ số theo diện tích box và nhóm món."""

    # (ngưỡng tỉ lệ diện tích, hệ số, nhãn) theo thứ tự tăng dần
    SCALES = {
        'bowl': [(0.08, 0.6, 'Tô nhỏ'), (0.22, 1.0, 'Tô vừa'), (0.40, 1.4, 'Tô lớn'), (9, 1.8, 'Tô đại / nồi')],
        'dip': [(0.015, 0.5, 'Chén nhỏ'), (0.06, 1.0, '1 chén'), (9, 1.5, 'Bát chấm chung')],
        'side': [(0.05, 0.6, 'Đĩa nhỏ'), (0.18, 1.0, 'Đĩa vừa'), (9, 1.5, 'Đĩa / rổ lớn')],
        'plate': [(0.04, 0.5, 'Phần nhỏ'), (0.15, 1.0, 'Phần vừa'), (0.30, 1.5, 'Phần lớn'), (9, 2.0, 'Phần dùng chung')],
    }

    def __init__(self, path=NUTRITION_PATH):
        with open(path, encoding='utf-8') as f:
            self.db = json.load(f)['dishes']

    @staticmethod
    def kind(name):
        c = BY_NAME[name]
        if c['group'] == 'sauce':
            return 'dip'
        if c['supercategory'] in ('noodle_soup', 'soup_pot') or name == 'cháo lòng':
            return 'bowl'
        if c['supercategory'] == 'vegetable':
            return 'side'
        return 'plate'

    def portion(self, name, box, img_shape):
        h, w = img_shape[:2]
        ratio = max(0.0, box[2] - box[0]) * max(0.0, box[3] - box[1]) / max(1.0, h * w)
        scale, label = next((s, l) for t, s, l in self.SCALES[self.kind(name)] if ratio < t)
        e = self.db[name]
        return {
            'name': name, 'name_vi': e['name_vi'], 'name_en': e['name_en'], 'serving': e['serving'],
            'portion_label': label, 'scale': scale, 'area_pct': round(ratio * 100, 1),
            'kcal': round(e['calories_kcal'] * scale), 'protein_g': round(e['protein_g'] * scale, 1),
            'carbs_g': round(e['carbs_g'] * scale, 1), 'fat_g': round(e['fat_g'] * scale, 1),
            'estimated': e.get('estimated', False),
            'allergens': e.get('allergens', []),  # bản nháp theo thành phần điển hình, xem _notes của file dinh dưỡng
        }

    @staticmethod
    def summarize(portions):
        tot = {k: round(sum(p[k] for p in portions), 1) for k in ('kcal', 'protein_g', 'carbs_g', 'fat_g')}
        cal = {'protein': tot['protein_g'] * 4, 'carbs': tot['carbs_g'] * 4, 'fat': tot['fat_g'] * 9}
        s = max(sum(cal.values()), 1.0)
        tot['pct'] = {k: round(v / s * 100) for k, v in cal.items()}
        tot['allergens'] = {}  # chất gây dị ứng -> các món chứa nó
        for p in portions:
            for a in p.get('allergens', []):
                tot['allergens'].setdefault(a, [])
                if p['name'] not in tot['allergens'][a]:
                    tot['allergens'][a].append(p['name'])
        return tot


# ───────────────────────────── vẽ ─────────────────────────────

COLORS = [(46, 204, 113), (52, 152, 219), (231, 76, 60), (241, 196, 15), (155, 89, 182),
          (230, 126, 34), (26, 188, 156), (236, 72, 153)]


def draw(img_rgb, items, labels):
    """items: list có 'box'; labels: chuỗi nhãn cùng thứ tự. Màu theo tên lớp."""
    im = Image.fromarray(img_rgb).convert('RGB')
    d = ImageDraw.Draw(im)
    size = max(14, im.width // 45)
    font = ImageFont.truetype(FONT_PATH, size) if os.path.exists(FONT_PATH) else ImageFont.load_default()
    for it, text in zip(items, labels):
        color = COLORS[(CLASS_NAMES.index(it['name']) if it['name'] in BY_NAME else len(it['name'])) % len(COLORS)]
        x1, y1, x2, y2 = it['box']
        d.rectangle([x1, y1, x2, y2], outline=color, width=max(2, im.width // 300))
        tb = d.textbbox((x1, y1), text, font=font)
        ty = y1 - (tb[3] - tb[1]) - 6 if y1 - (tb[3] - tb[1]) - 6 > 0 else y1
        d.rectangle([x1, ty, x1 + tb[2] - tb[0] + 8, ty + tb[3] - tb[1] + 6], fill=color)
        d.text((x1 + 4, ty + 2), text, fill=(255, 255, 255), font=font)
    return np.array(im)
