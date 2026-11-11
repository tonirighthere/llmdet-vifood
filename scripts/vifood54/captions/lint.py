"""
Lint caption grounding cho ViFood-54.

BERT của Grounding DINO (bert-base-uncased) viết thường + BỎ DẤU + WordPiece, nên
`của` → `cu ##a` trùng hẳn với lớp `cua`. Lint chạy trên chính token của BERT:

1. Mọi chỗ chuỗi token của một tên lớp xuất hiện (đúng ranh giới từ) phải nằm trong một
   span đã đăng ký. Span của lớp khác cũng được (`quay` trong `gà quay`, `canh` trong `bánh canh`).
2. Ngoài các span, không được có từ hương vị / cảm xúc (model không nhìn thấy được).
3. Mỗi span khớp tuyệt đối `caption[s:e] == phrase`, và `lower()` không đổi độ dài.
4. Số token BERT của caption ≤ max_tokens (phần còn lại của 256 dành cho negative).
"""
import re

# Từ / cụm không nhìn thấy được: hương vị, mùi, cảm giác khi ăn, cảm xúc, giá trị văn hóa
TASTE_WORDS = [
    'thơm', 'ngon', 'đậm đà', 'đậm vị', 'ngọt', 'cay', 'chua', 'mặn', 'béo', 'bùi', 'ngậy',
    'hương vị', 'vị', 'mùi', 'lừng', 'hấp dẫn', 'thèm', 'ấm cúng', 'quê nhà', 'truyền thống',
    'đặc sản', 'tinh hoa', 'nóng hổi', 'giòn', 'mềm', 'dai', 'dẻo', 'thanh mát', 'mát lạnh',
    'tươi ngon', 'đặc trưng', 'sum vầy', 'hài hòa',
]
# Cụm hợp lệ chứa từ trong danh sách trên (tên thành phần nhìn thấy được)
TASTE_ALLOW = ['cà chua']


def _word_re(w):
    return re.compile(r'(?<!\w)' + re.escape(w) + r'(?!\w)')


# Bản tiếng Anh (build_captions_en.py)
TASTE_WORDS_EN = [
    'delicious', 'tasty', 'yummy', 'flavor', 'flavour', 'flavorful', 'aroma', 'aromatic', 'fragrant', 'smell',
    'spicy', 'sweet', 'sour', 'salty', 'savory', 'bitter', 'rich', 'crispy', 'crunchy', 'tender', 'chewy', 'juicy',
    'soft', 'mouth-watering', 'appetizing', 'tempting', 'hot', 'warm', 'cold', 'cozy', 'homemade', 'traditional',
    'authentic', 'specialty', 'famous', 'favorite', 'perfect', 'beautiful', 'nice',
]
TASTE_ALLOW_EN = ['sweet potato', 'hot pot', 'hotpot']


class CaptionLinter:
    def __init__(self, tokenizer, class_names, max_tokens=160, taste_words=TASTE_WORDS, taste_allow=TASTE_ALLOW):
        self.tok = tokenizer
        self.max_tokens = max_tokens
        self.class_pieces = {n: tokenizer.tokenize(n) for n in class_names}
        self.taste_re = [(w, _word_re(w)) for w in taste_words]
        self.allow_re = [_word_re(w) for w in taste_allow]

    def tokens(self, text):
        enc = self.tok(text, add_special_tokens=False, return_offsets_mapping=True)
        return self.tok.convert_ids_to_tokens(enc['input_ids']), enc['offset_mapping']

    def n_tokens(self, text):
        return len(self.tok.tokenize(text))

    def check(self, caption, spans):
        """spans: list (start, end, phrase). Trả về list lỗi (rỗng = đạt)."""
        errors = []
        if len(caption.lower()) != len(caption):
            errors.append('lower() đổi độ dài caption')
        for s, e, phrase in spans:
            if caption[s:e] != phrase:
                errors.append(f'span lệch: [{s}:{e}]={caption[s:e]!r} != {phrase!r}')

        toks, offs = self.tokens(caption)
        if len(toks) > self.max_tokens:
            errors.append(f'quá dài: {len(toks)} > {self.max_tokens} token')

        def in_span(a, b):
            return any(s <= a and b <= e for s, e, _ in spans)

        for name, pieces in self.class_pieces.items():
            k = len(pieces)
            for i in range(len(toks) - k + 1):
                if toks[i:i + k] != pieces:
                    continue
                if toks[i].startswith('##') or (i + k < len(toks) and toks[i + k].startswith('##')):
                    continue  # không đúng ranh giới từ
                a, b = offs[i][0], offs[i + k - 1][1]
                if not in_span(a, b):
                    errors.append(f'token trùng tên lớp "{name}" ngoài span: {caption[a:b]!r} @{a}')

        masked = list(caption.lower())
        for s, e, _ in spans:
            masked[s:e] = ' ' * (e - s)
        masked = ''.join(masked)
        for r in self.allow_re:
            masked = r.sub(lambda m: ' ' * len(m.group()), masked)
        for w, r in self.taste_re:
            m = r.search(masked)
            if m:
                errors.append(f'từ không nhìn thấy được: {w!r} @{m.start()}')
        return errors
