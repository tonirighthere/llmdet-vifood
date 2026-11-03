#!/usr/bin/env python3
"""
app_vifood54.py
===============
Demo ViFood-54 (Pha 6): Grounding DINO Swin-T fine-tune trên 54 món Việt.

  Tab 1  Nhận diện 54 món + ước lượng dinh dưỡng (prompt đủ 54 tên lớp, như lúc đánh giá)
  Tab 2  Tìm món theo câu tiếng Việt ("tô phở ở bên trái và chén nước chấm có ớt")
  Tab 3  Kết quả thực nghiệm
  Tab 4  Từ điển 54 món & dinh dưỡng

    cd llmdet_vietnamese_food && python app_vifood54.py      # http://localhost:7862
"""
import json
import os
import sys
import time

import gradio as gr
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from mmengine.registry import init_default_scope  # noqa: E402

init_default_scope('mmdet')
import vifood54_core as core  # noqa: E402

NUTRITION = core.Nutrition()
DEFAULT_MODEL = next(iter(core.MODELS))
with open(os.path.join(HERE, 'demo_examples_vifood54.json'), encoding='utf-8') as f:
    EXAMPLES = [(os.path.join(core.ROOT, fn), classes, caption) for fn, classes, caption in json.load(f)]


# ───────────────────────────── HTML kết quả ─────────────────────────────

def nutrition_html(portions):
    if not portions:
        return "<div style='padding:16px;color:#64748b'>Không có món nào vượt ngưỡng tin cậy. Thử giảm ngưỡng.</div>"
    s = NUTRITION.summarize(portions)
    rows = ''.join(
        f"<tr><td><b>{p['name']}</b><br><small style='color:#64748b'>{p['name_en']}</small></td>"
        f"<td>{p['portion_label']} <small>(×{p['scale']}, {p['area_pct']}% ảnh)</small></td>"
        f"<td style='text-align:right'><b>{p['kcal']}</b>{' *' if p['estimated'] else ''}</td>"
        f"<td style='text-align:right'>{p['protein_g']}</td><td style='text-align:right'>{p['carbs_g']}</td>"
        f"<td style='text-align:right'>{p['fat_g']}</td><td style='text-align:right'>{p['score']:.2f}</td></tr>"
        for p in portions)
    note = ("<p style='font-size:0.8rem;color:#64748b'>* giá trị ước tính tham khảo. Khẩu phần suy từ diện tích box "
            "theo nhóm món (tô / đĩa / chén chấm / rau), không phải cân thật.</p>")
    return f"""
    <div style="font-family:system-ui,sans-serif">
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:12px">
        <div style="background:#fff7ed;border-radius:10px;padding:12px;text-align:center"><div>Năng lượng</div><div style="font-size:1.6rem;font-weight:800;color:#ea580c">{s['kcal']:.0f}</div><div>kcal</div></div>
        <div style="background:#f0fdf4;border-radius:10px;padding:12px;text-align:center"><div>Đạm</div><div style="font-size:1.6rem;font-weight:800;color:#16a34a">{s['protein_g']}</div><div>g ({s['pct']['protein']}%)</div></div>
        <div style="background:#fefce8;border-radius:10px;padding:12px;text-align:center"><div>Tinh bột</div><div style="font-size:1.6rem;font-weight:800;color:#ca8a04">{s['carbs_g']}</div><div>g ({s['pct']['carbs']}%)</div></div>
        <div style="background:#fef2f2;border-radius:10px;padding:12px;text-align:center"><div>Chất béo</div><div style="font-size:1.6rem;font-weight:800;color:#dc2626">{s['fat_g']}</div><div>g ({s['pct']['fat']}%)</div></div>
      </div>
      <table style="width:100%;border-collapse:collapse;font-size:0.9rem">
        <thead><tr style="background:#f1f5f9;text-align:left"><th>Món</th><th>Khẩu phần</th><th style="text-align:right">kcal</th>
        <th style="text-align:right">Đạm g</th><th style="text-align:right">Carb g</th><th style="text-align:right">Béo g</th><th style="text-align:right">Điểm</th></tr></thead>
        <tbody>{rows}</tbody>
      </table>{note}
    </div>"""


# ───────────────────────────── handlers ─────────────────────────────

def run_detect(image, thr, model_name):
    if image is None:
        return None, "<div style='color:#ef4444'>Hãy tải ảnh lên.</div>", ''
    t0 = time.time()
    items = core.detect(image, model_name, thr)
    ms = (time.time() - t0) * 1000
    portions = [dict(NUTRITION.portion(i['name'], i['box'], image.shape), score=i['score']) for i in items]
    vis = core.draw(image, items, [f"{i['name']} {i['score']:.2f}" for i in items])
    names = sorted({i['name'] for i in items})
    return vis, nutrition_html(portions), f"⏱️ {ms:.0f} ms · {len(items)} box · {len(names)} món: {', '.join(names) or '—'}"


def run_ground(image, sentence, thr, model_name):
    if image is None:
        return None, "Hãy tải ảnh lên.", ''
    if not sentence or not sentence.strip():
        return image, "Hãy nhập một câu có tên món.", ''
    t0 = time.time()
    ents, items = core.ground(image, model_name, sentence.strip(), thr)
    ms = (time.time() - t0) * 1000
    if not ents:
        known = ', '.join(core.CLASS_NAMES[:12])
        return image, (f"Không tìm thấy tên món nào trong câu. Câu cần có tên món trong 54 lớp hoặc tên gọi khác "
                       f"(ví dụ: {known}, ...)."), ''
    vis = core.draw(image, items, [f"{i['surface']} {i['score']:.2f}" for i in items])
    lines = ['| Cụm trong câu | Lớp | Box điểm cao nhất | Số box |', '|---|---|---|---|']
    for j, e in enumerate(ents):
        mine = [i for i in items if i['entity'] == j]
        top = f"{mine[0]['score']:.2f}" if mine else 'không tìm thấy'
        lines.append(f"| {e['surface']} | {e['name']} | {top} | {len(mine)} |")
    return vis, '\n'.join(lines), f"⏱️ {ms:.0f} ms · {len(ents)} cụm tên món trong câu"


# ───────────────────────────── nội dung tĩnh ─────────────────────────────

RESULTS_MD = """
## Kết quả trên tập test ViFood-54 (414 ảnh, 1898 box, 54 lớp)

| Mô hình | Huấn luyện | mAP | AP50 | Tìm món trong câu L2 (R@1) |
| :--- | :--- | :---: | :---: | :---: |
| B0 | checkpoint gốc, không fine-tune | 0.015 | 0.020 | 0.302 |
| B1-v2 | OD: tên lớp + negative | 0.315 | 0.394 | 0.363 |
| B3 | OD + caption hình thái, từ đầu | 0.220 | 0.279 | **0.774** |
| **B3b** | B1-v2 rồi fine-tune OD + caption | **0.323** | **0.405** | 0.663 |

- **Negative trong prompt** là yếu tố quyết định (0.015 → 0.315).
- **Caption hình thái** (vị trí, số lượng, lượng từ, thuộc tính nhìn thấy) giúp tìm món trong câu tự nhiên gần gấp đôi;
  fine-tune sau OD (B3b) giữ được mAP.
- **Từ hương vị** ("thơm ngon", "đậm đà"...) chèn vào câu không đổi kết quả (±0.01): model chỉ dựa vào cái nhìn thấy.
- **Open-vocabulary** (8 món không có trong train): AP_novel tốt nhất 0.082 (gọi bằng tên tiếng Anh), so với 0.419 khi
  có nhãn → món mới vẫn cần dữ liệu gán nhãn.

Chi tiết: `grounding_data/vifood54/EVAL_*.md`, `sessions/PLAN_VIFOOD54.md`.
"""


def dictionary_md():
    rows = []
    for c in core.TAXONOMY:
        e = NUTRITION.db[c['name']]
        rows.append(f"| **{c['name']}** | {c['en']} | {c['visual']['definition']} | {e['serving']} | "
                    f"{e['calories_kcal']}{' *' if e.get('estimated') else ''} | {e['protein_g']} | {e['carbs_g']} | {e['fat_g']} |")
    return ('| Món | Tiếng Anh | Nhận biết bằng mắt | Khẩu phần chuẩn | kcal | Đạm g | Carb g | Béo g |\n'
            '| :--- | :--- | :--- | :--- | ---: | ---: | ---: | ---: |\n' + '\n'.join(rows) +
            '\n\n\\* giá trị ước tính tham khảo (nem rán, quẩy, món tráng miệng).')


# ───────────────────────────── giao diện ─────────────────────────────

with gr.Blocks(title='ViFood-54 · Grounding & Dinh dưỡng', theme=gr.themes.Soft()) as demo:
    gr.Markdown('# 🍜 ViFood-54: nhận diện 54 món Việt, tìm món theo câu & ước lượng dinh dưỡng\n'
                'Grounding DINO Swin-T fine-tune trên ViFood-54 (B3b: OD + caption hình thái).')
    with gr.Tabs():
        with gr.TabItem('🍽️ Nhận diện 54 món'):
            with gr.Row():
                with gr.Column(scale=5):
                    d_img = gr.Image(type='numpy', label='Ảnh bữa ăn', sources=['upload', 'webcam', 'clipboard'])
                    with gr.Row():
                        d_thr = gr.Slider(0.1, 0.8, value=0.3, step=0.05, label='Ngưỡng tin cậy')
                        d_model = gr.Dropdown(list(core.MODELS), value=DEFAULT_MODEL, label='Mô hình')
                    d_btn = gr.Button('Nhận diện', variant='primary')
                    gr.Examples([[p, 0.3, DEFAULT_MODEL] for p, _, _ in EXAMPLES], [d_img, d_thr, d_model])
                with gr.Column(scale=7):
                    d_info = gr.Markdown()
                    d_out = gr.Image(type='numpy', label='Kết quả')
                    d_html = gr.HTML()
            d_btn.click(run_detect, [d_img, d_thr, d_model], [d_out, d_html, d_info])

        with gr.TabItem('💬 Tìm món theo câu'):
            gr.Markdown('Viết một câu có tên món (hoặc tên gọi khác như *nước chấm*, *giò lụa*, *nộm*). Model khoanh '
                        'box cho từng tên món trong câu, dùng cả ngữ cảnh vị trí, số lượng và đặc điểm nhìn thấy.')
            with gr.Row():
                with gr.Column(scale=5):
                    g_img = gr.Image(type='numpy', label='Ảnh bữa ăn', sources=['upload', 'webcam', 'clipboard'])
                    g_text = gr.Textbox(label='Câu mô tả', lines=3,
                                        value='Ở chính giữa có một tô phở, bên phải là chén nước chấm có lát ớt đỏ.')
                    with gr.Row():
                        g_thr = gr.Slider(0.1, 0.8, value=0.35, step=0.05, label='Ngưỡng cho box thêm')
                        g_model = gr.Dropdown(list(core.MODELS), value=DEFAULT_MODEL, label='Mô hình')
                    g_btn = gr.Button('Tìm theo câu', variant='primary')
                    gr.Examples([[p, cap, 0.35, DEFAULT_MODEL] for p, _, cap in EXAMPLES], [g_img, g_text, g_thr, g_model])
                with gr.Column(scale=7):
                    g_info = gr.Markdown()
                    g_out = gr.Image(type='numpy', label='Kết quả')
                    g_table = gr.Markdown()
            g_btn.click(run_ground, [g_img, g_text, g_thr, g_model], [g_out, g_table, g_info])

        with gr.TabItem('📊 Kết quả thực nghiệm'):
            gr.Markdown(RESULTS_MD)

        with gr.TabItem('📖 Từ điển 54 món'):
            gr.Markdown(dictionary_md())

if __name__ == '__main__':
    core.load_model(DEFAULT_MODEL)  # nạp sẵn model mặc định
    demo.launch(server_name='0.0.0.0', server_port=int(os.environ.get('PORT', 7862)),
                allowed_paths=[os.path.join(core.ROOT, 'grounding_data/vifood54/images'),
                               os.path.join(core.ROOT, 'vifood_2999_extracted')])
