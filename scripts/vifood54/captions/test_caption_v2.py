#!/usr/bin/env python3
"""Test phần CPU của caption_v2.py (không cần GPU / VLM):  python scripts/vifood54/captions/test_caption_v2.py"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import caption_v2 as C  # noqa: E402  (đặt VIFOOD_LANG=en)

CLASSES = C.load_taxonomy()
ID = {c['name']: c['id'] for c in CLASSES}
FILT = C.CaptionFilter(CLASSES)


def make_row():
    pho, herbs, sauce = ID['pho noodle soup'], ID['fresh herbs and greens'], ID['dipping sauce']
    inst = [{'bbox': [100, 150, 500, 550], 'label': pho}, {'bbox': [600, 100, 900, 350], 'label': herbs},
            {'bbox': [650, 500, 750, 590], 'label': sauce}, {'bbox': [800, 500, 900, 590], 'label': sauce}]
    row = {'filename': 'x.jpg', 'width': 1000, 'height': 600, 'detection': {'instances': inst}}
    desc = {'filename': 'x.jpg', 'model': 'A', 'dishes': {
        str(pho): {'container': 'bowl', 'colors': ['clear brown broth', 'white flat noodles'],
                   'components': ['sliced green onions', 'thin beef slices', 'purple unicorn horn'],
                   'arrangement': 'topped with herbs', 'box': inst[0]['bbox']},
        str(herbs): {'container': 'basket', 'colors': ['dark green leaves'], 'components': ['white bean sprouts'],
                     'arrangement': '', 'box': inst[1]['bbox']},
        str(sauce): {'error': 'json'}},
        'scene': {'surface': 'dark wooden table', 'utensils': ['wooden chopsticks'], 'other_objects': ['glass of water'],
                  'background': ''}}
    ver = {'filename': 'x.jpg', 'model': 'B', 'dishes': {
        str(pho): {'clear brown broth': True, 'white flat noodles': True, 'sliced green onions': True,
                   'thin beef slices': True, 'purple unicorn horn': False, 'topped with herbs': True},
        str(herbs): {'dark green leaves': True, 'white bean sprouts': False}},
        'scene': {'dark wooden table': True, 'wooden chopsticks': True, 'glass of water': False}}
    return row, desc, ver


def test_compose():
    row, desc, ver = make_row()
    r = C.compose_row(row, desc, ver, CLASSES, FILT, 140)
    cap = r['caption']
    assert 'unicorn' not in cap and 'bean sprouts' not in cap and 'glass of water' not in cap, cap  # bị kiểm chứng loại
    assert 'a large bowl of pho noodle soup' in cap and 'two small bowls of dipping sauce' in cap, cap
    assert 'The pho noodle soup is to the left of the fresh herbs and greens.' in cap, cap
    assert set(r['gt']) == FILT.dishes_in(cap)
    assert r['n_claim'] == 11 and r['n_kept'] == 8, (r['n_claim'], r['n_kept'])
    assert any('lỗi JSON' in i for i in r['issues']) and r['status'] == 'flagged'
    assert all(s.endswith('.') for s in r['sentences']) and ' '.join(r['sentences']) == cap
    return r


def test_cleaner():
    cl = C.PhraseCleaner(CLASSES)
    assert cl.clean(' Sliced Green Onions. ') == 'sliced green onions'
    assert cl.clean('delicious golden crust') is None            # hương vị
    assert cl.clean('probably fish sauce') is None                # suy đoán
    assert cl.clean('side of dipping sauce') is None              # tên món
    assert cl.clean('a b c d e f g h i') is None and cl.clean(None) is None and cl.clean('none') is None
    assert cl.clean_list(['red chili', 'red chili', 5, 'lime wedge'], 5) == ['red chili', 'lime wedge']


def test_translate_protect():
    r = test_compose()
    name_vi = {c['name']: c['name_vi'] for c in CLASSES}
    masked, table = C.protect(r['sentences'], name_vi, FILT)
    assert 'pho noodle soup' not in ' '.join(masked) and '[[0]]' in masked[0], masked
    assert 'phở' in table and 'rau sống' in table and 'đồ chấm' in table
    assert C.restore(['Ở giữa có một tô [[0]].'], table) == [f'Ở giữa có một tô {table[0]}.']
    assert C.restore(['[[9]]'], table) is None

    class Fake:  # model giả: trả đúng số câu, giữ placeholder
        def ask(self, images, text, max_new_tokens=0):
            lines = [l.split('. ', 1)[1] for l in text.splitlines() if l[:1].isdigit()]
            return json.dumps(['VI: ' + l for l in lines], ensure_ascii=False)

    vi = C.translate_row(Fake(), r['sentences'], name_vi, FILT)
    assert vi and len(vi) == len(r['sentences']) and 'phở' in vi[0], vi

    class Bad(Fake):  # làm mất placeholder -> phải bị từ chối
        def ask(self, images, text, max_new_tokens=0):
            return json.dumps(['x'] * len([l for l in text.splitlines() if l[:1].isdigit()]))

    assert C.translate_row(Bad(), r['sentences'], name_vi, FILT) is None


if __name__ == '__main__':
    for name, fn in list(globals().items()):
        if name.startswith('test_'):
            fn()
            print('ok', name)
    print(test_compose()['caption'])
