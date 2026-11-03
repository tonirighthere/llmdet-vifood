"""
Bố cục lấy từ box GT (luôn đúng với ảnh): vị trí lưới 3×3, kích thước tương đối, số lượng.
Mọi từ ở đây đã qua lint (không trùng tên lớp sau khi BERT bỏ dấu; tránh `bên cạnh`, `của`...).
"""
import collections

# (hàng, cột) -> cụm vị trí; cột 0 = trái, 2 = phải
POSITIONS = {
    (0, 0): 'góc trên bên trái', (0, 1): 'phía trên', (0, 2): 'góc trên bên phải',
    (1, 0): 'bên trái', (1, 1): 'chính giữa', (1, 2): 'bên phải',
    (2, 0): 'góc dưới bên trái', (2, 1): 'phía dưới', (2, 2): 'góc dưới bên phải',
}
COUNT_WORDS = {1: 'một', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm'}
SCATTERED = 'rải rác trên bàn'
LARGE_RATIO, SMALL_RATIO = 0.2, 0.02


def count_word(n):
    return COUNT_WORDS.get(n, 'nhiều')


def cell_of(bbox, width, height):
    x1, y1, x2, y2 = bbox
    cx, cy = (x1 + x2) / 2 / width, (y1 + y2) / 2 / height
    return min(int(cy * 3), 2), min(int(cx * 3), 2)


def flip_cell(cell):
    return cell[0], 2 - cell[1]


def size_word(ratio):
    if ratio >= LARGE_RATIO:
        return 'lớn'
    if ratio <= SMALL_RATIO:
        return 'nhỏ'
    return ''


class ClassGroup:
    """Các box cùng lớp trong một ảnh."""

    def __init__(self, label, name, boxes, width, height):
        self.label, self.name, self.boxes = label, name, boxes
        self.n = len(boxes)
        self.cells = list(dict.fromkeys(cell_of(b, width, height) for b in boxes))
        self.max_ratio = max((b[2] - b[0]) * (b[3] - b[1]) for b in boxes) / (width * height)

    def location(self, flip=False):
        """Cụm vị trí (không có giới từ) và cờ 'một ô duy nhất'."""
        cells = [flip_cell(c) for c in self.cells] if flip else self.cells
        if len(cells) == 1:
            return POSITIONS[cells[0]], True
        if len(cells) == 2:
            a, b = sorted(cells)
            return f'{POSITIONS[a]} và {POSITIONS[b]}', False
        return SCATTERED, False

    def size(self):
        return size_word(self.max_ratio) if self.n == 1 else ''


def group_instances(instances, class_names, width, height):
    """instances: list {'bbox', 'label'} -> list ClassGroup, lớp to nhất trước."""
    by_label = collections.OrderedDict()
    for inst in instances:
        by_label.setdefault(inst['label'], []).append(inst['bbox'])
    groups = [ClassGroup(l, class_names[l], bs, width, height) for l, bs in by_label.items()]
    groups.sort(key=lambda g: -g.max_ratio)
    return groups
