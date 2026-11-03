"""
Ghép caption grounding cho một ảnh từ bố cục GT + bộ thuộc tính hình thái.

- L1: cụm liệt kê có số lượng và lượng từ ("một tô phở, hai chén đồ chấm và một đĩa rau sống.")
- L2: mỗi lớp một câu: vị trí + số lượng + lượng từ + tên + kích thước + 1–2 thuộc tính.
- Vùng: "tô phở, sợi bánh dẹt trắng, nước dùng trong" (cho caption mức vùng của LMM).

Offset ký tự của tên lớp được ghi ngay lúc ghép (không dò lại bằng str.find).
Mọi lựa chọn ngẫu nhiên nằm trong `plan`, nên bản gốc và bản lật trái↔phải dùng
cùng lựa chọn, chỉ khác từ chỉ vị trí.
"""
import random

from layout import SCATTERED, count_word

L1_PREFIXES = ['', 'Trên bàn có ', 'Ảnh gồm ', 'Bữa ăn gồm ']
L2_TEMPLATES = ['loc_first', 'np_first', 'is']  # 'is' chỉ dùng khi lớp nằm trong một ô


class _Text:
    def __init__(self):
        self.parts, self.spans, self.pos = [], [], 0

    def add(self, s):
        self.parts.append(s)
        self.pos += len(s)

    def add_name(self, name, label):
        self.spans.append((self.pos, self.pos + len(name), name, label))
        self.add(name)

    def text(self):
        return ''.join(self.parts)


def _cap(s):
    return s[:1].upper() + s[1:]


class CaptionBuilder:
    def __init__(self, bank, count_tokens, max_tokens=160):
        """bank: {tên lớp: taxonomy[...]['visual']} (units, multi_units, attrs, definition); count_tokens: str -> số token BERT."""
        self.bank = bank
        self.count_tokens = count_tokens
        self.max_tokens = max_tokens

    # ── kế hoạch ngẫu nhiên ──
    def plan(self, groups, level, seed):
        rng = random.Random(seed)
        items = []
        for g in groups:
            v = self.bank[g.name]
            k = min(len(v['attrs']), rng.choice([1, 2]))
            items.append({
                'unit': rng.choice(v['units'] if g.n == 1 else v.get('multi_units', v['units'])),
                'attrs': rng.sample(v['attrs'], k) if k else [],
                'template': rng.choice(L2_TEMPLATES if len(g.cells) == 1 else L2_TEMPLATES[:2]),
            })
        order = list(range(len(groups)))
        if level == 'L1':
            rng.shuffle(order)
        return {'level': level, 'prefix': rng.choice(L1_PREFIXES), 'items': items, 'order': order}

    # ── dựng câu ──
    def _np(self, t, g, it, with_size=True):
        """'một tô phở lớn' (cụm danh từ, ghi span cho tên lớp)."""
        t.add(f'{count_word(g.n)} ')
        if it['unit']:
            t.add(f'{it["unit"]} ')
        t.add_name(g.name, g.label)
        # không nói kích thước khi lượng từ đã có 'nhỏ', hoặc với lớp không có hình thái chung
        size = g.size() if with_size and 'nhỏ' not in it['unit'] and self.bank[g.name]['attrs'] else ''
        if size:
            t.add(f' {size}')

    def _attrs(self, t, it):
        for a in it['attrs']:
            t.add(f', {a}')

    def render(self, groups, plan, flip=False):
        t = _Text()
        items = plan['items']
        if plan['level'] == 'L1':
            order = plan['order']
            for j, i in enumerate(order):
                if j == 0:
                    start = len(t.parts)
                    t.add(plan['prefix'])
                elif j == len(order) - 1:
                    t.add(' và ')
                else:
                    t.add(', ')
                self._np(t, groups[i], items[i], with_size=False)
                if j == 0 and not plan['prefix']:
                    t.parts[start + 1] = _cap(t.parts[start + 1])  # 'một' -> 'Một'
            t.add('.')
            return t.text(), t.spans

        for i in plan['order']:
            g, it = groups[i], items[i]
            loc, single = g.location(flip)
            loc_prep = loc if loc == SCATTERED else f'ở {loc}'
            if t.parts:
                t.add(' ')
            if it['template'] == 'is' and single:
                t.add(f'{_cap(loc)} là ')
                self._np(t, g, it)
                self._attrs(t, it)
            elif it['template'] == 'np_first':
                n0 = len(t.parts)
                self._np(t, g, it)
                t.parts[n0] = _cap(t.parts[n0])
                t.add(f' nằm {loc_prep}')
                self._attrs(t, it)
            else:
                t.add(f'{_cap(loc_prep)} có ')
                self._np(t, g, it)
                self._attrs(t, it)
            t.add('.')
        return t.text(), t.spans

    def build(self, groups, level, seed):
        """Trả về (plan, caption, spans); L2 tự bớt thuộc tính nếu vượt ngân sách token."""
        plan = self.plan(groups, level, seed)
        text, spans = self.render(groups, plan)
        while self.count_tokens(text) > self.max_tokens:
            longest = max(plan['items'], key=lambda it: len(it['attrs']))
            if not longest['attrs']:
                break  # không bớt được nữa; lint sẽ loại
            longest['attrs'] = longest['attrs'][:-1]
            text, spans = self.render(groups, plan)
        return plan, text, spans

    def region_caption(self, name):
        v = self.bank[name]
        unit = v['units'][0]
        head = f'{unit} {name}' if unit else name
        return ', '.join([head] + v['attrs'][:2])
