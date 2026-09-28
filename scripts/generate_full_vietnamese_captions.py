#!/usr/bin/env python3
"""
scripts/generate_full_vietnamese_captions.py
=============================================
Pha 3.5: Sinh caption tiếng Việt tự nhiên giàu ngữ cảnh cho Visual Grounding.

Chiến lược 2 tầng:
  1. Gemini API (nếu available) → caption đa dạng, giàu ngữ nghĩa
  2. Template engine nâng cao (fallback) → caption tự nhiên từ 50+ patterns

Output:
  - vifood_train_vg_vi_full.jsonl (900 mẫu)
  - vifood_val_vg_vi_full.jsonl (100 mẫu)
"""

import os
import sys
import json
import time
import re
import hashlib
import random
import urllib.request
import urllib.error

BASE_DIR = "/home/atin/tuan/SoPSoP"
ANN_DIR = os.path.join(BASE_DIR, "grounding_data", "vifood", "annotations")
CACHE_DIR = os.path.join(BASE_DIR, "grounding_data", "vifood", "cache")

# Input files
TRAIN_JSONL = os.path.join(ANN_DIR, "vifood_train_vg.jsonl")
VAL_JSONL = os.path.join(ANN_DIR, "vifood_val_vg.jsonl")

# Output files
TRAIN_OUT = os.path.join(ANN_DIR, "vifood_train_vg_vi_full.jsonl")
VAL_OUT = os.path.join(ANN_DIR, "vifood_val_vg_vi_full.jsonl")

# Cache
CAPTION_CACHE_FILE = os.path.join(CACHE_DIR, "gemini_full_vi_captions.json")

# Gemini API
API_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = "gemini-3.6-flash"

# ═══════════════════════════════════════════════════
# TỪ ĐIỂN 51 CLASS VỚI MÔ TẢ ĐẶC TRƯNG
# ═══════════════════════════════════════════════════

DISH_DESCRIPTIONS = {
    "bánh bèo": ["trắng mịn rắc tôm cháy vàng ruộm", "mềm dẻo phủ lớp tôm chấy thơm phức", "tròn nhỏ xinh xắn rắc nhân tôm giã nhuyễn"],
    "bánh bột lọc": ["trong suốt nhân tôm thịt dai mềm", "lớp vỏ trong veo bọc nhân tôm thịt đậm đà", "mềm dẻo đặc trưng Huế nhân tôm thịt thơm lừng"],
    "bánh canh": ["sợi to mềm trong nước dùng đậm đà", "nước dùng sánh ngọt với sợi bánh trắng mềm", "sợi bánh dày mềm mại trong nước lèo đậm vị"],
    "bánh chưng": ["vuông xanh lá dong nhân đậu xanh thịt heo", "gói lá dong vuông vức nhân đỗ xanh thịt mỡ", "truyền thống vuông vắn lớp nếp dẻo nhân đậu thịt"],
    "bánh cuốn": ["mỏng mịn cuốn thịt heo xay nấm mèo", "lớp bột mỏng như lụa cuốn nhân thịt thơm", "trắng muốt mịn màng cuốn nhân thịt nấm mộc nhĩ"],
    "bánh căn": ["nhỏ xinh giòn rụm nướng trên khuôn đất nung", "vàng giòn tròn nhỏ nướng khuôn nóng hổi", "giòn tan nướng trên bếp khuôn đất truyền thống"],
    "bánh giò": ["hình chóp gói lá chuối nhân thịt mộc nhĩ", "hình tam giác gói lá chuối thơm nhân thịt", "nóng hổi bọc lá chuối xanh nhân thịt bằm mộc nhĩ"],
    "bánh khọt": ["giòn vàng phủ tôm tươi ăn kèm rau sống", "vàng rộm tròn nhỏ đặt tôm tươi hồng trên mặt", "giòn xốp nướng khuôn phủ tôm tươi hấp dẫn"],
    "bánh mì": ["giòn tan nhân thịt pate rau sống đồ chua", "vỏ giòn ruột mềm kẹp đầy nhân thịt rau", "nóng hổi giòn rụm nhồi thịt chả pate đầy ắp"],
    "bánh pía": ["xốp nhiều lớp nhân sầu riêng đậu xanh trứng muối", "vỏ xốp lớp lớp nhân sầu riêng béo ngậy", "đặc sản Sóc Trăng vỏ xốp nhân đậu sầu riêng"],
    "bánh tráng": ["tròn mỏng giòn rắc hành phi mỡ hành", "mỏng giòn phủ hành phi thơm nức", "nướng giòn rụm rắc hành mỡ hấp dẫn"],
    "bánh tét": ["dài hình trụ gói lá chuối nhân đậu xanh", "hình trụ dài gói lá chuối xanh nhân đậu thịt", "dẻo thơm lớp nếp bọc nhân đậu xanh thịt mỡ"],
    "bánh xèo": ["vàng nghệ giòn rụm nhân tôm giá đỗ", "vàng óng giòn tan nhân tôm thịt giá đỗ", "giòn xốp vàng nghệ cuốn rau sống chấm nước mắm"],
    "bánh đúc": ["mềm mịn trắng ngà chan mắm thịt bằm", "trắng ngà mịn màng ăn kèm thịt bằm sốt", "mềm mát cắt miếng vuông chan nước thịt đậm đà"],
    "bún bò Huế": ["nước dùng cay nồng hương sả ớt đặc trưng xứ Huế", "đậm đà cay ngọt mùi sả ớt nồng nàn", "nước lèo đỏ au thơm sả ngọt xương hầm lâu"],
    "bún": ["sợi trắng tươi mềm mượt", "sợi tròn trắng muốt mềm mại", "tươi mát sợi nhỏ trắng tinh"],
    "bún mắm": ["nước dùng mắm cá đậm đà thơm lừng", "nước lèo mắm cá ngọt sâu hải sản phong phú", "đậm vị mắm đặc trưng miền Tây"],
    "bún riêu": ["nước dùng chua thanh với riêu cua đồng", "nước lèo cà chua chua ngọt với gạch cua béo", "thanh mát vị chua tự nhiên riêu cua đỏ thơm"],
    "bún thịt nướng": ["thịt nướng thơm phức trên lớp bún và rau thơm", "thịt nướng than hoa vàng ươm trên bún tươi rau sống", "thơm lừng thịt nướng sả ớt bày trên bún trắng rau thơm"],
    "bún đậu mắm tôm": ["đậu hũ chiên giòn chấm mắm tôm", "đậu phụ giòn vàng bên bún trắng chấm mắm tôm", "giòn rụm đậu chiên vàng ruộm kèm bún rau chấm mắm tôm"],
    "canh chua": ["nước dùng chua ngọt thanh mát với cá và thơm", "nước trong chua nhẹ thơm mùi me và thơm tươi", "thanh mát chua dịu với cá tươi rau thơm đầy màu sắc"],
    "cao lầu": ["sợi vàng dai đặc sản phố cổ Hội An", "sợi mì vàng dai ăn kèm thịt xá xíu đặc trưng Hội An", "đặc sản phố Hội sợi dai vàng óng với thịt heo và rau sống"],
    "cháo lòng": ["nóng hổi sánh mịn với lòng heo giòn sần sật", "sánh đặc thơm lừng hành phi điểm lòng heo tươi ngon", "nóng bốc khói mịn màng với lòng heo giòn dai đa dạng"],
    "chả": ["thơm ngon thái lát mỏng", "hồng nhạt mịn thái miếng vừa ăn", "thơm lừng cắt lát trình bày đẹp mắt"],
    "cua": ["tươi ngon vỏ đỏ au thịt ngọt chắc", "vỏ đỏ cam bóng bẩy thịt ngọt đầy đặn", "tươi sống hấp chín đỏ tươi thịt trắng ngọt"],
    "cá chiên": ["giòn vàng rụm thơm lừng", "chiên vàng giòn tan thơm mùi dầu nóng", "vàng ươm giòn rụm da cá giòn thịt cá mềm"],
    "cơm chiên": ["hạt tơi rời vàng óng ánh thơm mỡ hành", "vàng đều hạt tơi rời thơm nức mùi hành tỏi", "xào nóng hổi hạt cơm tơi xốp vàng đẹp mắt"],
    "cơm tấm": ["hạt tấm trắng dẻo kèm sườn nướng trứng ốp la", "hạt gạo tấm dẻo ngon kèm sườn nướng thơm phức", "đĩa cơm trắng nóng bên sườn nướng vàng ươm trứng ốp la"],
    "gà luộc": ["da vàng óng mượt thịt ngọt mềm", "da vàng bóng mịn thịt trắng ngọt thanh", "luộc chín vừa da vàng ươm thịt mềm ngọt tự nhiên"],
    "gỏi": ["rau tươi giòn trộn đều chua ngọt", "giòn sật đầy rau tươi trộn gia vị chua cay", "sắc màu rực rỡ với rau xanh tươi trộn vị chua ngọt hài hòa"],
    "gỏi cuốn": ["cuốn tôm thịt rau sống trong lớp bánh tráng mỏng", "tươi mát với tôm thịt rau cuốn trong bánh tráng trong", "lớp bánh tráng cuốn chặt tôm hồng thịt luộc rau thơm xanh"],
    "heo quay": ["da giòn vàng ruộm thịt mềm thấm gia vị", "lớp da giòn rụm vàng ươm thịt thấm đều gia vị", "da bì giòn tan vàng đỏ thịt bên trong mềm ngọt"],
    "hàu": ["tươi béo ngậy nướng mỡ hành", "nướng phô mai vàng ruộm béo ngậy", "tươi rói nướng than phủ mỡ hành thơm nức"],
    "hủ tiếu": ["sợi trong dai mềm trong nước dùng thanh ngọt", "sợi trắng trong dai giòn trong nước lèo xương hầm", "nước dùng trong veo ngọt thanh với sợi hủ tiếu dai mềm"],
    "lẩu": ["nước dùng sôi sùng sục đầy rau thịt hải sản", "bốc khói nghi ngút đầy rau xanh thịt tươi hải sản", "nước lèo sôi bùng bên cạnh đĩa rau thịt hải sản đa dạng"],
    "mì Quảng": ["sợi vàng nghệ nước dùng đậm đà đặc sản miền Trung", "sợi mì dẹt vàng nghệ chan nước dùng đậm vị", "đặc sản xứ Quảng sợi vàng ươm với nước dùng tôm thịt đậm đà"],
    "mực": ["tươi giòn dai xào tỏi ớt thơm lừng", "trắng giòn dai nướng thơm phức", "tươi ngon chế biến giòn sần sật hấp dẫn"],
    "nem chua": ["chua cay cuốn lá chuối hồng đào", "hồng nhạt chua dịu cuốn lá chuối xanh", "chua thanh cay nhẹ gói trong lá chuối tươi"],
    "ngao sò": ["tươi ngọt hấp sả ớt thơm nức", "vỏ mở tươi ngon hấp sả nóng hổi", "nước dùng ngọt thanh từ ngao tươi hấp sả gừng"],
    "phở": ["nước dùng trong veo thơm hồi quế ngọt thanh", "nước lèo trong ngọt thơm nồng quế hồi", "tô nóng hổi nước dùng thơm lừng hồi quế kèm thịt tái chín"],
    "rau sống": ["xanh mướt tươi giòn đủ loại rau thơm", "đĩa rau tươi xanh mướt đủ loại rau thơm đặc trưng", "tươi mát gồm xà lách húng quế kinh giới giá đỗ"],
    "súp cua": ["sánh mịn nóng hổi đầy thịt cua trứng cút", "sánh đặc nóng bốc khói với gạch cua trứng cút", "nóng hổi sánh mượt đầy thịt cua và trứng cút mềm"],
    "thịt bò": ["mềm ngọt xào lúc lắc đậm gia vị", "thái lát mềm thơm lừng gia vị tiêu đen", "tươi ngon chế biến đậm đà mềm mọng nước"],
    "rau luộc": ["xanh mướt chấm nước mắm tỏi ớt", "xanh non luộc chín vừa chấm nước chấm đậm đà", "mềm xanh tươi mát ăn kèm nước mắm pha"],
    "tôm": ["tươi ngon đỏ hồng thịt chắc ngọt", "hồng tươi uốn cong thịt ngọt chắc nịch", "tươi sống hấp chín đỏ au thịt trắng ngọt lịm"],
    "xôi xéo": ["vàng nghệ dẻo thơm phủ đậu xanh hành phi", "dẻo thơm vàng ươm rắc đậu xanh giã nhuyễn hành phi", "nếp dẻo vàng nghệ phủ đậu xanh tán và hành phi giòn"],
    "ốc": ["hấp sả ớt thơm nức mũi", "luộc nóng hổi chấm muối tiêu chanh", "nướng mỡ hành thơm lừng béo ngậy"],
    "món ăn khác": ["đa dạng đậm đà phong cách Việt", "truyền thống đặc trưng hương vị Việt Nam", "đặc sản truyền thống mang đậm bản sắc ẩm thực Việt"],
    "rau xào": ["xanh mướt xào tỏi thơm lừng", "xào nóng giòn mềm thơm mùi tỏi phi", "xanh tươi xào lửa lớn giòn ngon thơm phức"],
    "nước chấm": ["pha chua ngọt cay nồng", "trong vắt pha tỏi ớt chua ngọt đậm đà", "mắm pha chanh tỏi ớt đậm đà hòa quyện"],
    "gà quay": ["vàng ruộm giòn da thơm gia vị", "da giòn vàng rộm thịt mềm ngọt thấm gia vị", "nướng vàng đều da giòn tan thịt mềm thấm đẫm hương liệu"]
}

# ═══════════════════════════════════════════════════
# HỆ THỐNG TEMPLATE PHONG PHÚ (50+ patterns)
# ═══════════════════════════════════════════════════

# Mở đầu câu
OPENERS = [
    "Bữa ăn hôm nay nổi bật với",
    "Trên bàn ăn bày biện",
    "Mâm cơm Việt Nam đầy hấp dẫn với",
    "Bữa trưa ấm cúng gồm có",
    "Một góc bàn ăn gia đình với",
    "Bữa cơm gia đình thơm ngon với",
    "Mâm ăn truyền thống bao gồm",
    "Bữa ăn đậm chất Việt Nam với",
    "Trải dài trên bàn là",
    "Bữa tiệc nhỏ với những món đặc trưng gồm",
    "Mâm cỗ vừa dọn ra với",
    "Bữa cơm dân dã mà đầy đủ hương vị với",
    "Góc bàn ăn tràn ngập hương thơm của",
    "Một bữa ăn ngon miệng với",
    "Bữa cơm chiều sum vầy với",
]

# Nối giữa các món
CONNECTORS = [
    "bên cạnh là",
    "đi kèm với",
    "ăn kèm cùng",
    "dọn bên cạnh",
    "cùng với",
    "kết hợp cùng",
    "không thể thiếu",
    "hài hòa bên cạnh",
    "điểm thêm",
    "bổ sung bởi",
]

# Kết thúc câu
CLOSERS = [
    "tạo nên bức tranh ẩm thực Việt Nam đầy sắc màu.",
    "mang đến hương vị truyền thống đặc trưng.",
    "gợi nhớ hương vị quê nhà ấm áp.",
    "tất cả hòa quyện tạo nên bữa ăn ngon miệng.",
    "khiến ai nấy đều thèm thuồng.",
    "đúng chuẩn hương vị ẩm thực Việt Nam.",
    "làm cho bữa ăn thêm phần đặc sắc và hấp dẫn.",
    "mời gọi cả gia đình quây quần thưởng thức.",
    "đậm đà bản sắc ẩm thực dân tộc.",
    "tạo nên một bữa ăn trọn vẹn đầy hấp dẫn.",
    "thể hiện tinh hoa ẩm thực Việt Nam.",
    "hoàn hảo cho bữa cơm gia đình sum họp.",
]

# Từ nối bổ trợ
DISH_VERBS = [
    "được bày trí",
    "được dọn ra",
    "được bài trí",
    "nằm gọn gàng trên đĩa",
    "được sắp xếp đẹp mắt",
]


def get_desc(dish_name, seed=0):
    """Lấy mô tả cho một món, với seed để đa dạng hóa."""
    descs = DISH_DESCRIPTIONS.get(dish_name, ["đậm đà hương vị Việt", "thơm ngon truyền thống", "đặc trưng ẩm thực Việt Nam"])
    if isinstance(descs, str):
        return descs
    return descs[seed % len(descs)]


def generate_rich_template_caption(dishes, combo_key):
    """
    Sinh caption tự nhiên từ hệ thống template phong phú.
    Đảm bảo: tất cả tên món đều xuất hiện nguyên gốc trong caption.
    """
    rng = random.Random(hashlib.md5(combo_key.encode()).hexdigest())

    if len(dishes) == 1:
        d = dishes[0]
        desc = get_desc(d, rng.randint(0, 100))
        patterns = [
            f"Món {d} {desc} được bày trí gọn gàng trên bàn ăn, mang đậm hương vị ẩm thực truyền thống Việt Nam.",
            f"Trên bàn là phần {d} {desc}, một món ăn quen thuộc gợi nhớ bữa cơm gia đình ấm cúng.",
            f"Bữa ăn đơn giản mà ngon miệng với {d} {desc}, thể hiện nét tinh tế trong ẩm thực Việt.",
            f"Đĩa {d} {desc} nổi bật trên bàn ăn, hương thơm lan tỏa khiến ai cũng muốn thưởng thức.",
            f"Một phần {d} {desc} vừa được dọn ra, gợi lên hương vị đặc trưng của ẩm thực Việt Nam.",
            f"Góc bàn ăn thật hấp dẫn với phần {d} {desc}, mời gọi thực khách thưởng thức ngay.",
        ]
        return rng.choice(patterns)

    elif len(dishes) == 2:
        d0, d1 = dishes[0], dishes[1]
        desc0 = get_desc(d0, rng.randint(0, 100))
        desc1 = get_desc(d1, rng.randint(0, 100))
        conn = rng.choice(CONNECTORS)
        patterns = [
            f"Bữa ăn hôm nay có {d0} {desc0}, {conn} {d1} {desc1}, tạo nên sự kết hợp hài hòa đậm chất Việt Nam.",
            f"Trên bàn bày {d0} {desc0} cùng {d1} {desc1}, mang đến bữa ăn đậm chất truyền thống.",
            f"Mâm cơm ấm cúng với {d0} {desc0} và {d1} {desc1}, hương vị hòa quyện thật hấp dẫn.",
            f"Đĩa {d0} {desc0} {rng.choice(DISH_VERBS)} bên cạnh phần {d1} {desc1}, hoàn hảo cho bữa cơm gia đình.",
            f"Sự kết hợp giữa {d0} {desc0} và {d1} {desc1} tạo nên bữa ăn Việt Nam đầy hương vị.",
            f"Bữa cơm dân dã với {d0} {desc0}, {conn} {d1} {desc1}, đậm đà bản sắc ẩm thực dân tộc.",
        ]
        return rng.choice(patterns)

    elif len(dishes) == 3:
        d0, d1, d2 = dishes[0], dishes[1], dishes[2]
        desc0 = get_desc(d0, rng.randint(0, 100))
        desc1 = get_desc(d1, rng.randint(0, 100))
        desc2 = get_desc(d2, rng.randint(0, 100))
        opener = rng.choice(OPENERS)
        closer = rng.choice(CLOSERS)
        patterns = [
            f"{opener} {d0} {desc0}, {d1} {desc1} và {d2} {desc2}, {closer}",
            f"Bữa ăn phong phú gồm {d0} {desc0} bên cạnh {d1} {desc1}, thêm phần {d2} {desc2} {closer}",
            f"Mâm cơm bày biện {d0} {desc0}, kết hợp {d1} {desc1} cùng {d2} {desc2}, {closer}",
        ]
        return rng.choice(patterns)

    else:
        # 4+ món: ghép thành đoạn văn mạch lạc
        opener = rng.choice(OPENERS)
        closer = rng.choice(CLOSERS)

        parts = []
        for i, d in enumerate(dishes):
            desc = get_desc(d, rng.randint(0, 100))
            if i == 0:
                parts.append(f"{d} {desc}")
            elif i == len(dishes) - 1:
                parts.append(f"và {d} {desc}")
            else:
                if rng.random() < 0.3:
                    conn = rng.choice(CONNECTORS)
                    parts.append(f"{conn} {d} {desc}")
                else:
                    parts.append(f"{d} {desc}")

        dish_text = ", ".join(parts[:-1]) + " " + parts[-1]
        return f"{opener} {dish_text}, {closer}"


def call_gemini_api(prompt, max_retries=3, timeout=15):
    """Gọi Gemini API với retry. Trả về None nếu fail."""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={API_KEY}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 300}
    }).encode("utf-8")

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=timeout) as res:
                data = json.loads(res.read().decode("utf-8"))
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return text
        except urllib.error.HTTPError as e:
            if e.code == 429:
                wait = [10, 30, 60][min(attempt, 2)]
                print(f"   ⚠️ Rate limit 429, đợi {wait}s...")
                time.sleep(wait)
            else:
                return None
        except Exception:
            return None
    return None


def build_gemini_prompt(dishes):
    """Tạo prompt cho Gemini API."""
    dish_list_str = ", ".join(dishes)
    return f"""Bạn là chuyên gia ẩm thực Việt Nam. Hãy viết MỘT đoạn văn ngắn (2-3 câu, 40-80 từ) miêu tả bữa ăn gồm: {dish_list_str}.

YÊU CẦU:
1. Nhắc TẤT CẢ tên món ở dạng NGUYÊN GỐC chính xác: {dish_list_str}
2. Miêu tả đặc điểm, bày trí, màu sắc
3. Văn phong tự nhiên mạch lạc
4. KHÔNG thêm món khác, KHÔNG dấu ngoặc kép
5. Chỉ trả về đoạn văn, không tiêu đề"""


def verify_and_fix_caption(caption, dishes):
    """Verify + fix caption để đảm bảo tất cả tên món đều có mặt."""
    caption = caption.strip()
    caption = re.sub(r'[*_#]', '', caption)
    caption = re.sub(r'^\d+\.\s*', '', caption)
    caption = re.sub(r'^[-•]\s*', '', caption)
    caption = caption.strip()

    missing = [d for d in dishes if d not in caption]

    if not missing:
        if not caption.endswith(('.', '!', '?')):
            caption += '.'
        return caption, True

    # Chèn các món bị thiếu
    if not caption.endswith(('.', '!', '?', ',')):
        caption = caption.rstrip() + ','

    missing_parts = []
    for d in missing:
        desc = get_desc(d, hash(d) % 3)
        missing_parts.append(f"{d} {desc}")

    suffix = " cùng với " + " và ".join(missing_parts) + "."
    caption = caption.rstrip('.') + suffix

    return caption, False


def compute_tokens_positive(caption, dish_name):
    """Tìm character offset [start, end] ở word boundary."""
    search_start = 0
    while True:
        idx = caption.find(dish_name, search_start)
        if idx == -1:
            break

        # Kiểm tra word boundary
        before_ok = (idx == 0) or (not caption[idx - 1].isalpha())
        end_idx = idx + len(dish_name)
        after_ok = (end_idx >= len(caption)) or (not caption[end_idx].isalpha())

        if before_ok and after_ok:
            return [[idx, end_idx]]

        search_start = idx + 1

    # Fallback: simple find
    pos = caption.find(dish_name)
    if pos == -1:
        return []
    return [[pos, pos + len(dish_name)]]


def process_split(input_file, output_file, caption_cache, split_name, use_api=False):
    """Xử lý một split (train hoặc val)."""
    print(f"\n{'='*60}")
    print(f"📝 Xử lý {split_name}: {os.path.basename(input_file)}")
    print(f"{'='*60}")

    with open(input_file, 'r', encoding='utf-8') as f:
        samples = [json.loads(line) for line in f]

    print(f"📦 Đã nạp {len(samples)} mẫu")

    # Nhóm theo tổ hợp món
    combo_to_indices = {}
    for i, sample in enumerate(samples):
        dishes = []
        seen = set()
        for region in sample['grounding']['regions']:
            d = region['phrase']
            if d not in seen:
                dishes.append(d)
                seen.add(d)
        combo_key = " + ".join(sorted(dishes))
        if combo_key not in combo_to_indices:
            combo_to_indices[combo_key] = []
        combo_to_indices[combo_key].append((i, dishes))

    print(f"🎯 Tổng số tổ hợp món: {len(combo_to_indices)}")

    # Sinh caption cho combos chưa có
    missing_combos = {k: v[0][1] for k, v in combo_to_indices.items() if k not in caption_cache}
    cached_count = len(combo_to_indices) - len(missing_combos)
    print(f"📡 Cần sinh mới: {len(missing_combos)} | Đã cache: {cached_count}")

    if missing_combos:
        api_success = 0
        api_fail = 0
        template_used = 0

        for done, (combo_key, dishes) in enumerate(missing_combos.items(), 1):
            caption = None

            # Thử API nếu enabled
            if use_api:
                prompt = build_gemini_prompt(dishes)
                raw = call_gemini_api(prompt)
                if raw:
                    caption, all_found = verify_and_fix_caption(raw, dishes)
                    if all_found:
                        api_success += 1
                    else:
                        # API trả caption nhưng thiếu món → dùng template
                        caption = None

            # Fallback: Template engine
            if not caption:
                caption = generate_rich_template_caption(dishes, combo_key)
                caption, _ = verify_and_fix_caption(caption, dishes)
                template_used += 1

            caption_cache[combo_key] = caption

            if done % 20 == 0 or done == len(missing_combos):
                print(f"   ✅ {done}/{len(missing_combos)} (API: {api_success}, Template: {template_used})")

            if use_api:
                time.sleep(1.5)

        # Save cache
        os.makedirs(os.path.dirname(CAPTION_CACHE_FILE), exist_ok=True)
        with open(CAPTION_CACHE_FILE, 'w', encoding='utf-8') as f:
            json.dump(caption_cache, f, ensure_ascii=False, indent=2)
        print(f"💾 Cache saved: {CAPTION_CACHE_FILE}")

    # Xây dựng output
    print(f"⏳ Đóng gói ODVG JSONL...")
    output_samples = []
    token_errors = 0

    for i, sample in enumerate(samples):
        dishes = []
        seen = set()
        for region in sample['grounding']['regions']:
            d = region['phrase']
            if d not in seen:
                dishes.append(d)
                seen.add(d)

        combo_key = " + ".join(sorted(dishes))
        full_caption = caption_cache.get(combo_key, "")

        if not full_caption:
            full_caption = generate_rich_template_caption(dishes, combo_key)
            full_caption, _ = verify_and_fix_caption(full_caption, dishes)

        # Build regions
        new_regions = []
        for region in sample['grounding']['regions']:
            dish_name = region['phrase']
            tokens_pos = compute_tokens_positive(full_caption, dish_name)

            if not tokens_pos:
                token_errors += 1
                desc = get_desc(dish_name, 0)
                full_caption = full_caption.rstrip('.')
                full_caption += f", bên cạnh là {dish_name} {desc}."
                tokens_pos = compute_tokens_positive(full_caption, dish_name)

            new_regions.append({
                "bbox": region['bbox'],
                "phrase": dish_name,
                "tokens_positive": tokens_pos
            })

        conversations = [
            {"from": "human", "value": "<image>\nMô tả chi tiết bữa ăn trong hình."},
            {"from": "gpt", "value": full_caption}
        ]

        output_entry = {
            "filename": sample['filename'],
            "height": sample['height'],
            "width": sample['width'],
            "detection": sample['detection'],
            "grounding": {
                "caption": full_caption,
                "regions": new_regions
            },
            "conversations": conversations
        }
        output_samples.append(output_entry)

    # Write
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in output_samples:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"💾 Đã ghi {len(output_samples)} mẫu → {os.path.basename(output_file)}")
    if token_errors > 0:
        print(f"⚠️  {token_errors} trường hợp phải chèn thêm tên món")

    # Validation
    validate_output(output_file)

    return output_samples


def validate_output(jsonl_file):
    """Kiểm tra tokens_positive hợp lệ."""
    errors = 0
    total_regions = 0

    with open(jsonl_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            sample = json.loads(line)
            caption = sample['grounding']['caption']

            for region in sample['grounding']['regions']:
                total_regions += 1
                phrase = region['phrase']
                tps = region['tokens_positive']

                if not tps:
                    errors += 1
                    continue

                for start, end in tps:
                    if start < 0 or end > len(caption):
                        errors += 1
                        continue
                    extracted = caption[start:end]
                    if extracted != phrase:
                        errors += 1

    if errors == 0:
        print(f"   ✅ Tất cả {total_regions} regions đều hợp lệ!")
    else:
        print(f"   ⚠️  {errors}/{total_regions} regions có lỗi tokens_positive")


def main():
    print("=" * 60)
    print("⭐ PHA 3.5: SINH CAPTION TIẾNG VIỆT TỰ NHIÊN CHO GROUNDING")
    print("=" * 60)

    # Check if --api flag
    use_api = "--api" in sys.argv
    if use_api:
        print("🌐 Chế độ: Gemini API + Template fallback")
    else:
        print("📝 Chế độ: Template engine (nhanh, không cần API)")
        print("   Thêm flag --api để dùng Gemini API")

    print(f"Output: {os.path.basename(TRAIN_OUT)} + {os.path.basename(VAL_OUT)}")
    print()

    # Load cache
    caption_cache = {}
    if os.path.exists(CAPTION_CACHE_FILE):
        try:
            with open(CAPTION_CACHE_FILE, 'r', encoding='utf-8') as f:
                caption_cache = json.load(f)
            print(f"💾 Nạp {len(caption_cache)} caption từ cache.")
        except Exception:
            caption_cache = {}

    # Process
    process_split(TRAIN_JSONL, TRAIN_OUT, caption_cache, "TRAIN", use_api)
    process_split(VAL_JSONL, VAL_OUT, caption_cache, "VAL", use_api)

    # Show samples
    print(f"\n{'='*60}")
    print("📋 MẪU KẾT QUẢ (5 ảnh đầu tiên):")
    print(f"{'='*60}")

    with open(TRAIN_OUT, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i >= 5:
                break
            sample = json.loads(line)
            print(f"\n--- Ảnh {i+1}: {sample['filename'][:50]} ---")
            cap = sample['grounding']['caption']
            print(f"Caption ({len(cap)} chars): {cap}")
            for r in sample['grounding']['regions'][:3]:
                tp = r['tokens_positive']
                if tp:
                    extracted = cap[tp[0][0]:tp[0][1]]
                    print(f"  [{tp[0][0]}:{tp[0][1]}] '{r['phrase']}' → verify='{extracted}' {'✅' if extracted == r['phrase'] else '❌'}")

    # Stats
    print(f"\n{'='*60}")
    print("📊 THỐNG KÊ CAPTION:")
    with open(TRAIN_OUT, 'r', encoding='utf-8') as f:
        cap_lens = []
        for line in f:
            sample = json.loads(line)
            cap_lens.append(len(sample['grounding']['caption']))
        print(f"   Train: min={min(cap_lens)}, max={max(cap_lens)}, avg={sum(cap_lens)/len(cap_lens):.0f} chars")

    with open(VAL_OUT, 'r', encoding='utf-8') as f:
        cap_lens = []
        for line in f:
            sample = json.loads(line)
            cap_lens.append(len(sample['grounding']['caption']))
        print(f"   Val:   min={min(cap_lens)}, max={max(cap_lens)}, avg={sum(cap_lens)/len(cap_lens):.0f} chars")

    print(f"\n🎉 PHA 3.5 HOÀN TẤT!")
    print(f"\nBước tiếp:")
    print(f"  1. Config đã sẵn: configs/grounding_dino_swin_t_vifood_vi_full.py")
    print(f"  2. Train: python mmdet_train.py configs/grounding_dino_swin_t_vifood_vi_full.py --work-dir work_dirs/vifood_vi_full_1k --amp")


if __name__ == "__main__":
    main()
