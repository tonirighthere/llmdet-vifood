import re
import json

with open('nutrition_vifood_51.json', 'r', encoding='utf-8') as f:
    NUTRITION_DB = json.load(f)

DISH_KEYS = sorted(list(NUTRITION_DB.keys()), key=lambda x: len(x), reverse=True)

RAW_PREFIXES = [
    "hãy tìm giúp tôi", "tìm giúp tôi", "hãy tìm cho tôi", "tìm cho tôi",
    "tìm kiếm", "hãy tìm", "tìm", "hãy chỉ ra", "chỉ ra", "chỉ giúp tôi",
    "cho tôi hỏi", "cho tôi xin", "cho tôi", "cho em", "ở đâu là", "ở đâu có",
    "xem có", "đâu là", "phát hiện", "detect", "tìm thấy", "xác định"
]
STOPWORDS_PREFIXES = sorted(RAW_PREFIXES, key=lambda x: len(x), reverse=True)

SPLIT_PATTERNS = [
    r'\s+và\s+', r'\s+với\s+', r'\s+cùng\s+', r'\s+kèm\s+', 
    r'\s+ăn kèm\s+', r'\s+lẫn\s+', r'[,;+]+', r'\s*\.\s*'
]

CONTAINER_WORDS = [
    "bát", "tô", "đĩa", "dĩa", "chén", "nồi", "mẹt", "ổ", "ly", "cốc", 
    "rổ", "miếng", "khúc", "phần", "suất", "gói", "đôi", "con", "cái"
]

ADJECTIVES = [
    "nóng hổi", "giòn rụm", "giòn tan", "thơm phức", "thơm lừng", 
    "xanh mướt", "ngon", "đầy đủ", "nóng", "chua ngọt", "nướng giòn", "hấp"
]

def parse_vietnamese_query(text):
    """
    Intelligently extracts individual food items from a natural Vietnamese sentence.
    Example: 'tìm tôm chiên và chả' -> ['tôm chiên', 'chả']
    Example: 'hãy tìm giúp tôi đĩa bánh tráng và tô bún bò Huế' -> ['bánh tráng', 'bún bò Huế']
    """
    clean_text = text.strip()
    
    # 1. Remove question / search prefixes
    lower_text = clean_text.lower()
    for prefix in STOPWORDS_PREFIXES:
        if lower_text.startswith(prefix):
            clean_text = clean_text[len(prefix):].strip()
            lower_text = clean_text.lower()
            break
            
    # 2. Split by conjunctions & punctuation
    pattern = '|'.join(SPLIT_PATTERNS)
    chunks = re.split(pattern, clean_text, flags=re.IGNORECASE)
    
    entities = []
    for chunk in chunks:
        c = chunk.strip().strip('.').strip(',')
        if not c or len(c) < 2:
            continue
            
        # Remove container words at beginning (e.g. "đĩa bánh cuốn" -> "bánh cuốn", "bát phở" -> "phở")
        words = c.split()
        if len(words) > 1 and words[0].lower() in CONTAINER_WORDS:
            c = " ".join(words[1:]).strip()
            
        # Clean adjective suffixes
        for adj in ADJECTIVES:
            if c.lower().endswith(adj):
                c = c[:-len(adj)].strip()
                
        # If the chunk directly contains one of our 51 known dishes, align with it
        matched_known = None
        for dish in DISH_KEYS:
            if dish.lower() in c.lower() or c.lower() in dish.lower():
                # Prefer the more specific / canonical term
                matched_known = c
                break
                
        if c and len(c) >= 2:
            entities.append(c)
            
    # Fallback: scan whole sentence for 51 dishes
    if len(entities) == 0:
        for dish in DISH_KEYS:
            if re.search(r'\b' + re.escape(dish) + r'\b', clean_text, re.IGNORECASE):
                entities.append(dish)
                
    # Remove duplicates preserving order
    unique_entities = []
    for e in entities:
        if e.lower() not in [u.lower() for u in unique_entities]:
            unique_entities.append(e)
            
    if not unique_entities:
        unique_entities = [text.strip()]
        
    formatted_prompt = " . ".join(unique_entities) + " ."
    return formatted_prompt, unique_entities

test_cases = [
    "tìm tôm chiên và chả",
    "hãy tìm giúp tôi đĩa bánh tráng và tô bún bò Huế",
    "bát phở bò nóng hổi ăn kèm đĩa rau sống và chén nước chấm",
    "tìm bánh mì, cơm tấm với gỏi cuốn",
    "tôm . chả ."
]

for tc in test_cases:
    fmt, ents = parse_vietnamese_query(tc)
    print(f"Input:     '{tc}'")
    print(f"Formatted: '{fmt}'")
    print(f"Entities:  {ents}\n")
