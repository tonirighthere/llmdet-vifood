#!/usr/bin/env python3
"""
scripts/vifood54/captions/review_captions.py
============================================
Duyệt tay caption VLM (vlm_captions.jsonl) trước khi train LMM. Ảnh bị gắn cờ (flagged) hiện trước.
Mỗi thao tác ghi thêm một dòng vào captions_reviewed.jsonl (dòng sau ghi đè dòng trước),
nên tắt app giữa chừng không mất gì.

    python scripts/vifood54/captions/review_captions.py --reviewer ten --port 7863

Tiêu chí: caption chỉ tả cái nhìn thấy; đúng tên món, số lượng, vị trí, màu; không món nào ngoài box.
Sai nhỏ -> sửa rồi "Lưu bản sửa"; sai nhiều -> "Loại" (train sẽ dùng caption template L2).
"""
from __future__ import annotations

import argparse
import datetime
import json
import os

import gradio as gr
from PIL import Image, ImageDraw, ImageOps

from vlm_captions import ANN, RAW, REVIEWED, ROOT, read_jsonl


def load_queue(only_flagged: bool) -> list[dict]:
    reviewed = {r['filename'] for r in read_jsonl(REVIEWED)} if os.path.exists(REVIEWED) else set()
    rows = [r for r in read_jsonl(RAW) if r['filename'] not in reviewed]
    if only_flagged:
        rows = [r for r in rows if r['status'] == 'flagged']
    return sorted(rows, key=lambda r: r['status'] != 'flagged')


def render(row: dict, boxes: dict[str, list[dict]]) -> Image.Image:
    img = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, row['filename']))).convert('RGB')
    draw = ImageDraw.Draw(img)
    for inst in boxes.get(row['filename'], []):
        draw.rectangle(inst['bbox'], outline=(255, 64, 0), width=max(2, img.width // 300))
        draw.text((inst['bbox'][0] + 4, inst['bbox'][1] + 2), inst['category'], fill=(255, 255, 0))
    return img


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument('--reviewer', required=True)
    p.add_argument('--port', type=int, default=7863)
    p.add_argument('--only-flagged', action='store_true')
    args = p.parse_args()
    queue = load_queue(args.only_flagged)
    boxes = {r['filename']: r['detection']['instances']
             for r in read_jsonl(os.path.join(ANN, 'train_od.jsonl'))}  # VIFOOD_LANG=en -> nhãn EN

    def show(i: int):
        if i >= len(queue):
            return None, 'Hết ảnh cần duyệt.', '', '', i
        r = queue[i]
        info = f'**{i + 1}/{len(queue)}** · `{r["filename"]}` · {r["status"]}\n\nMón GT: {", ".join(r["gt"])}\n\n' + \
               '\n'.join(f'- {x}' for x in r['issues'])
        return render(r, boxes), info, r['caption'], r['raw'], i

    def save(i: int, caption: str, status: str):
        if i < len(queue):
            r = queue[i]
            if status == 'approved' and caption.strip() != r['caption']:
                status = 'edited'
            with open(REVIEWED, 'a', encoding='utf-8') as f:
                f.write(json.dumps({'filename': r['filename'], 'caption': caption.strip(), 'status': status,
                                    'reviewer': args.reviewer,
                                    'time': datetime.datetime.now().isoformat(timespec='seconds')},
                                   ensure_ascii=False) + '\n')
        return show(i + 1)

    with gr.Blocks(title='Duyệt caption VLM') as demo:
        idx = gr.State(0)
        with gr.Row():
            image = gr.Image(type='pil', label='Ảnh + box GT', height=560)
            with gr.Column():
                info = gr.Markdown()
                caption = gr.Textbox(label='Caption (sửa trực tiếp)', lines=10)
                raw = gr.Textbox(label='Bản gốc VLM (trước khi lọc)', lines=6, interactive=False)
                with gr.Row():
                    ok = gr.Button('Duyệt / Lưu bản sửa', variant='primary')
                    bad = gr.Button('Loại')
                    skip = gr.Button('Bỏ qua')
        outs = [image, info, caption, raw, idx]
        demo.load(lambda: show(0), outputs=outs)
        ok.click(lambda i, c: save(i, c, 'approved'), [idx, caption], outs)
        bad.click(lambda i, c: save(i, c, 'rejected'), [idx, caption], outs)
        skip.click(lambda i: show(i + 1), [idx], outs)
    demo.launch(server_name='0.0.0.0', server_port=args.port)


if __name__ == '__main__':
    main()
