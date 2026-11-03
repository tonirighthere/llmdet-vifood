"""Unit test bộ sinh caption: python -m pytest scripts/vifood54/captions/test_captions.py -q"""
import json
import os
import random

import pytest
from transformers import AutoTokenizer

from builder import CaptionBuilder
from layout import group_instances
from lint import CaptionLinter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
TAX = json.load(open(os.path.join(HERE, '..', 'taxonomy.json'), encoding='utf-8'))['classes']
NAMES = [c['name'] for c in TAX]
BANK = {c['name']: c['visual'] for c in TAX}
ID = {n: i for i, n in enumerate(NAMES)}


@pytest.fixture(scope='module')
def linter():
    tok = AutoTokenizer.from_pretrained(os.path.join(ROOT, 'huggingface/bert-base-uncased'))
    return CaptionLinter(tok, NAMES, max_tokens=160)


@pytest.fixture(scope='module')
def builder(linter):
    return CaptionBuilder(BANK, linter.n_tokens, 160)


def span(cap, name):
    s = cap.index(name)
    return (s, s + len(name), name)


def test_cua_vs_cua_accent(linter):
    cap = 'Một bát súp cua của nhà hàng.'
    errs = linter.check(cap, [span(cap, 'súp cua')])
    assert any('"cua"' in e and 'của' in e for e in errs)  # 'của' -> 'cu ##a' = lớp cua
    cap2 = 'Một bát súp cua.'
    assert linter.check(cap2, [span(cap2, 'súp cua')]) == []  # 'cua' nằm trong span 'súp cua'


def test_canh_vs_canh_accent(linter):
    cap = 'Một tô bánh canh kế bên chén đồ chấm.'
    assert linter.check(cap, [span(cap, 'bánh canh'), span(cap, 'đồ chấm')]) == []
    cap2 = 'Một tô bánh canh bên cạnh chén đồ chấm.'
    errs = linter.check(cap2, [span(cap2, 'bánh canh'), span(cap2, 'đồ chấm')])
    assert any('cạnh' in e for e in errs)


def test_bun_tuoi_and_bun_rieu(linter):
    cap = 'Một đĩa bún tươi và một tô bún riêu.'
    assert linter.check(cap, [span(cap, 'bún tươi'), span(cap, 'bún riêu')]) == []


def test_unregistered_class_mention(linter):
    cap = 'Một chén bánh bèo rắc tôm.'
    assert any('"tôm"' in e for e in linter.check(cap, [span(cap, 'bánh bèo')]))


def test_taste_words(linter):
    cap = 'Một đĩa nem chua thơm ngon, lát cà chua đỏ.'
    errs = linter.check(cap, [span(cap, 'nem chua')])
    assert any("'thơm'" in e for e in errs) and any("'ngon'" in e for e in errs)
    assert not any("'chua'" in e for e in errs)  # 'nem chua' (span) và 'cà chua' hợp lệ


def test_bank_passes_lint(linter):
    for n, v in BANK.items():
        for u in v['units'] + v.get('multi_units', []):
            for a in v['attrs'] or ['']:
                cap = f'một {u} {n}, {a}.'.replace('  ', ' ')
                assert linter.check(cap, [span(cap, n)]) == [], (n, cap)


def test_definitions_and_cues_pass_lint(linter):
    # định nghĩa: không tên lớp khác, không hương vị; cue: không hương vị (được nhắc tên lớp kia)
    for c in TAX:
        d = c['visual']['definition']
        assert linter.check(d, []) == [], (c['name'], d)
        for o in c['confusable_with']:
            errs = [e for e in linter.check(o['cue'], []) if 'không nhìn thấy' in e]
            assert errs == [], (c['name'], o)


def _random_instances(rng, n_boxes, w=800, h=600):
    out = []
    for _ in range(n_boxes):
        x, y = rng.uniform(0, w - 60), rng.uniform(0, h - 60)
        out.append({'bbox': [x, y, x + rng.uniform(20, 200), y + rng.uniform(20, 200)], 'label': rng.randrange(len(NAMES))})
    return out


@pytest.mark.parametrize('n_boxes', [1, 3, 8, 32])
@pytest.mark.parametrize('level', ['L1', 'L2'])
def test_builder_spans_flip_budget(linter, builder, n_boxes, level):
    rng = random.Random(n_boxes)
    insts = _random_instances(rng, n_boxes)
    groups = group_instances(insts, NAMES, 800, 600)
    plan, cap, spans = builder.build(groups, level, seed=7)
    fcap, fspans = builder.render(groups, plan, flip=True)
    assert {s[3] for s in spans} == {g.label for g in groups}  # mọi lớp đều được nhắc
    for c, sp in ((cap, spans), (fcap, fspans)):
        for s, e, name, _ in sp:
            assert c[s:e] == name
        assert c[0].isupper()
    if level == 'L2' and n_boxes <= 8:
        assert linter.check(cap, [s[:3] for s in spans]) == []
        assert linter.check(fcap, [s[:3] for s in fspans]) == []


def test_flip_swaps_left_right(builder):
    insts = [{'bbox': [10, 250, 100, 350], 'label': ID['phở']}]  # ô giữa-trái
    groups = group_instances(insts, NAMES, 900, 600)
    plan, cap, _ = builder.build(groups, 'L2', seed=1)
    fcap, _ = builder.render(groups, plan, flip=True)
    assert 'trái' in cap and 'phải' not in cap
    assert 'phải' in fcap and 'trái' not in fcap
