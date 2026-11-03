#!/usr/bin/env python3
"""
scripts/vifood54/check_tokenizer.py
===================================
Kiểm tra tên lớp tiếng Việt qua tokenizer BERT của Grounding DINO (bert-base-uncased:
lowercase + BỎ DẤU + WordPiece). Báo cáo:
  - số mảnh subword mỗi tên;
  - tên trùng / gần trùng (khác đúng 1 mảnh) sau khi bỏ dấu;
  - tên lồng trong tên khác (ví dụ quẩy -> 'quay' nằm trong 'gà quay');
  - từ thông dụng bị đọc thành tên lớp (của -> cua, cạnh -> canh...) — dùng cho lint caption.

    python scripts/vifood54/check_tokenizer.py
"""
import argparse
import itertools
import json
import os

from transformers import AutoTokenizer

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Từ thường gặp trong caption tiếng Việt cần kiểm tra
COMMON_WORDS = ['của', 'cạnh', 'gói', 'lâu', 'cả', 'cà', 'chà', 'bờ', 'óc', 'mức', 'mục', 'hậu',
                'phố', 'phó', 'quay', 'quầy', 'song', 'bùn', 'chào', 'đỏ', 'tốm', 'xởi', 'mì', 'mỡ']


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--tokenizer', default=os.path.join(ROOT, 'huggingface/bert-base-uncased'))
    p.add_argument('--taxonomy', default=os.path.join(ROOT, 'scripts/vifood54/taxonomy.json'))
    args = p.parse_args()

    tok = AutoTokenizer.from_pretrained(args.tokenizer)
    with open(args.taxonomy, encoding='utf-8') as f:
        names = [c['name'] for c in json.load(f)['classes']]
    pieces = {n: tok.tokenize(n) for n in names}

    print(f'Mảnh/tên: TB {sum(map(len, pieces.values())) / len(pieces):.1f}, '
          f'không bị cắt subword: {sum(not any(x.startswith("##") for x in v) for v in pieces.values())}/{len(names)}')

    by_seq = {}
    for n, v in pieces.items():
        by_seq.setdefault(tuple(v), []).append(n)
    print('Trùng hoàn toàn sau bỏ dấu:', [v for v in by_seq.values() if len(v) > 1] or 'không')

    print('Gần trùng (khác đúng 1 mảnh):')
    for a, b in itertools.combinations(names, 2):
        if len(pieces[a]) == len(pieces[b]) and sum(x != y for x, y in zip(pieces[a], pieces[b])) == 1:
            print(f'  {a} {pieces[a]}  ~  {b} {pieces[b]}')

    print('Tên lồng trong tên khác:')
    for a in names:
        for b in names:
            la = len(pieces[a])
            if a != b and la < len(pieces[b]) and any(
                    pieces[b][i:i + la] == pieces[a] for i in range(len(pieces[b]) - la + 1)):
                print(f'  {a} {pieces[a]}  ⊂  {b} {pieces[b]}')

    cls_of = {tuple(v): n for n, v in pieces.items()}
    hits = {w: cls_of[tuple(tok.tokenize(w))] for w in COMMON_WORDS
            if tuple(tok.tokenize(w)) in cls_of and cls_of[tuple(tok.tokenize(w))] != w}
    print('Từ thường bị đọc thành tên lớp:', hits)


if __name__ == '__main__':
    main()
