"""
Ghép caption grounding TIẾNG ANH cho một ảnh từ bố cục GT + thuộc tính hình thái (bản song song của builder.py).

- L1: liệt kê có số lượng và lượng từ ("A bowl of pho noodle soup, two small bowls of dipping sauce and a plate of
  fresh herbs and greens.")
- L2: mỗi lớp một câu: vị trí + số lượng + lượng từ + kích thước + tên + 1–2 thuộc tính
  ("In the center is a large bowl of pho noodle soup, flat white rice noodles, clear broth.")
- Vùng: "bowl of pho noodle soup, flat white rice noodles, clear broth" (caption mức vùng cho LMM).

Như builder.py: offset tên lớp ghi lúc ghép; mọi lựa chọn ngẫu nhiên nằm trong `plan` nên bản gốc và bản lật
trái↔phải chỉ khác từ chỉ vị trí. Thuộc tính lấy từ `attr_pool` của ảnh nếu có (thuộc tính VLM đã xác nhận trên ảnh
đó), không thì từ taxonomy.
"""
import random
import re

# (hàng, cột) -> cụm vị trí có giới từ; cột 0 = trái, 2 = phải
POSITIONS = {
    (0, 0): 'in the top left corner', (0, 1): 'at the top', (0, 2): 'in the top right corner',
    (1, 0): 'on the left', (1, 1): 'in the center', (1, 2): 'on the right',
    (2, 0): 'in the bottom left corner', (2, 1): 'at the bottom', (2, 2): 'in the bottom right corner',
}
SCATTERED = 'across the table'
COUNT_WORDS = {2: 'two', 3: 'three', 4: 'four', 5: 'five'}
SIZE_EN = {'lớn': 'large', 'nhỏ': 'small', '': ''}  # layout.size_word trả về từ VI

# Thuộc tính nói về dụng cụ đựng ('piled to fill the plate', 'spoon in the bowl', 'metal pot'): bỏ khi lượng từ đã chọn
# là dụng cụ khác ("a basket of ..., piled to fill the plate"). Lượng từ trung tính (serving, piece, slice) không mâu thuẫn.
_ATTR_CONTAINER = re.compile(r'\b(?:on|in|to fill) (?:a|the) (plate|bowl|basket|tray|pot)\b|^(?:bamboo )?(tray)\b|\b(pot)$|'
                             r'^large (pot)\b')
_UNIT_CONTAINER = re.compile(r'\b(plate|bowl|basket|tray|pot)s?$')


def container_conflict(unit, attr):
    m = _ATTR_CONTAINER.search(attr)
    u = _UNIT_CONTAINER.search(unit)
    return bool(m and u) and next(g for g in m.groups() if g) != u.group(1)


L1_PREFIXES = ['', 'The table has ', 'The image shows ', 'The meal includes ']
L2_TEMPLATES = ['loc_first', 'np_first', 'is']  # 'is' chỉ dùng khi lớp nằm trong một ô


def location_en(g, flip=False):
    """Cụm vị trí tiếng Anh (có giới từ) và cờ 'một ô duy nhất'; cùng logic ô lưới với ClassGroup.location."""
    cells = [(r, 2 - c) for r, c in g.cells] if flip else list(g.cells)
    if len(cells) == 1:
        return POSITIONS[cells[0]], True
    if len(cells) == 2:
        a, b = sorted(cells)
        return f'{POSITIONS[a]} and {POSITIONS[b]}', False
    return SCATTERED, False


def _article(word):
    return 'an' if word[:1].lower() in 'aeiou' else 'a'


def _cap(s):
    return s[:1].upper() + s[1:]


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


class CaptionBuilderEN:
    def __init__(self, bank, count_tokens, max_tokens=160):
        """bank: {tên EN: {'units': [(số ít, số nhiều)], 'multi_units': [...], 'attrs': [...]}};
        count_tokens: str -> số token BERT."""
        self.bank = bank
        self.count_tokens = count_tokens
        self.max_tokens = max_tokens

    # ── kế hoạch ngẫu nhiên ──
    def plan(self, groups, level, seed, attr_pool=None, unit_pool=None):
        """attr_pool: {tên EN: [thuộc tính]} của riêng ảnh này (VLM); lớp không có trong pool dùng taxonomy.
        unit_pool: {tên EN: (số ít, số nhiều)} dụng cụ đựng VLM thấy trên ảnh (chỉ áp cho lớp 1 box)."""
        rng = random.Random(seed)
        items = []
        for g in groups:
            v = self.bank[g.name]
            attrs = attr_pool[g.name] if attr_pool and g.name in attr_pool else v['attrs']
            units = v['units'] if g.n == 1 else v.get('multi_units') or v['units']
            # dụng cụ VLM thấy (box lớn nhất) chỉ dùng khi lớp có 1 box: nhiều box thường là nhiều miếng trên CÙNG một
            # đĩa ("five plates of ..." sai) -> giữ lượng từ số nhiều của taxonomy (slices, servings, pieces)
            unit = unit_pool[g.name] if unit_pool and g.name in unit_pool and g.n == 1 else rng.choice(units)
            attrs = [a for a in attrs if not container_conflict(unit[0], a)]
            k = min(len(attrs), rng.choice([1, 2]))
            items.append({
                'unit': unit,
                'attrs': rng.sample(attrs, k) if k else [],
                'template': rng.choice(L2_TEMPLATES if len(g.cells) == 1 else L2_TEMPLATES[:2]),
            })
        order = list(range(len(groups)))
        if level == 'L1':
            rng.shuffle(order)
        return {'level': level, 'prefix': rng.choice(L1_PREFIXES), 'items': items, 'order': order}

    # ── dựng câu ──
    def _np(self, t, g, it, with_size=True):
        """'a large bowl of pho noodle soup' / 'two small bowls of dipping sauce' (ghi span cho tên lớp)."""
        sing, plur = it['unit']
        # không nói kích thước khi lượng từ đã có 'small', hoặc với lớp không có hình thái chung
        size = SIZE_EN[g.size()] if with_size and 'small' not in sing and self.bank[g.name]['attrs'] else ''
        head = f'{size} {sing}' if size else sing
        if g.n == 1:
            t.add(f'{_article(head)} {head} of ')
        else:
            t.add(f'{COUNT_WORDS.get(g.n, "several")} {plur} of ')
        t.add_name(g.name, g.label)

    def _attrs(self, t, it):
        for a in it['attrs']:
            t.add(f', {a}')

    def render(self, groups, plan, flip=False):
        t = _Text()
        items = plan['items']
        if plan['level'] == 'L1':
            for j, i in enumerate(plan['order']):
                if j == 0:
                    t.add(plan['prefix'])
                elif j == len(plan['order']) - 1:
                    t.add(' and ')
                else:
                    t.add(', ')
                n0 = len(t.parts)
                self._np(t, groups[i], items[i], with_size=False)
                if j == 0 and not plan['prefix']:
                    t.parts[n0] = _cap(t.parts[n0])  # 'a bowl of ' -> 'A bowl of '
            t.add('.')
            return t.text(), t.spans

        for i in plan['order']:
            g, it = groups[i], items[i]
            loc, single = location_en(g, flip)
            verb = 'is' if g.n == 1 else 'are'
            if t.parts:
                t.add(' ')
            if it['template'] == 'is' and single:
                t.add(f'{_cap(loc)} {verb} ')
                self._np(t, g, it)
            elif it['template'] == 'np_first':
                n0 = len(t.parts)
                self._np(t, g, it)
                t.parts[n0] = _cap(t.parts[n0])
                t.add(f' {verb} scattered {loc}' if loc == SCATTERED else f' {verb} {loc}')
            else:
                t.add(f'{_cap(loc)} there {verb} ')
                self._np(t, g, it)
            self._attrs(t, it)
            t.add('.')
        return t.text(), t.spans

    def build(self, groups, level, seed, attr_pool=None, unit_pool=None):
        """Trả về (plan, caption, spans); L2 tự bớt thuộc tính nếu vượt ngân sách token."""
        plan = self.plan(groups, level, seed, attr_pool, unit_pool)
        text, spans = self.render(groups, plan)
        while self.count_tokens(text) > self.max_tokens:
            longest = max(plan['items'], key=lambda it: len(it['attrs']))
            if not longest['attrs']:
                break  # không bớt được nữa; lint sẽ loại
            longest['attrs'] = longest['attrs'][:-1]
            text, spans = self.render(groups, plan)
        return plan, text, spans

    def region_caption(self, name, attr_pool=None, unit_pool=None):
        v = self.bank[name]
        attrs = attr_pool[name] if attr_pool and name in attr_pool else v['attrs']
        unit = unit_pool[name][0] if unit_pool and name in unit_pool else v['units'][0][0]
        return ', '.join([f'{unit} of {name}'] + [a for a in attrs if not container_conflict(unit, a)][:2])
