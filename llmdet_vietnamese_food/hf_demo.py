import torch
from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor
from PIL import Image, ImageDraw

# 1. Khai báo thiết bị và đường dẫn tới thư mục weights bạn vừa tải
model_path = "./weights"
device = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Đang tải mô hình lên thiết bị: {device}...")
# Load processor và model trực tiếp từ thư mục local
processor = AutoProcessor.from_pretrained(model_path)
model = AutoModelForZeroShotObjectDetection.from_pretrained(model_path).to(device)

# 2. Chuẩn bị ảnh đầu vào và câu lệnh
image_path = "images/buacomVN2.jpg"
image = Image.open(image_path).convert("RGB")
text_labels = [["spring rolls"]] # Yêu cầu mô hình tìm 'quả táo'

print(f"Đang phân tích ảnh: {image_path} với từ khóa: {text_labels}")
inputs = processor(images=image, text=text_labels, return_tensors="pt", padding=True).to(device)

# 3. Chạy suy luận (Inference) - Lưu ý: Lúc này LLM không tham gia, chỉ có Backbone chạy
with torch.no_grad():
    outputs = model(**inputs)

# 4. Xử lý kết quả đầu ra (Lọc các box có độ tự tin > 0.3)
results = processor.post_process_grounded_object_detection(
    outputs,
    threshold=0.3,
    target_sizes=[(image.size[1], image.size[0])]
)[0]

# 5. Vẽ Bounding Box lên ảnh và lưu kết quả
draw = ImageDraw.Draw(image)
for box, score, label in zip(results["boxes"], results["scores"], results["labels"]):
    # Làm tròn tọa độ và điểm số
    box = [round(i, 2) for i in box.tolist()]
    confidence = round(score.item(), 2)
    
    print(f"Phát hiện: '{label}' (Độ tự tin: {confidence}) tại tọa độ {box}")
    
    # Vẽ khung chữ nhật màu đỏ, viền dày 3 pixel
    draw.rectangle(box, outline="red", width=3)
    # Gắn nhãn text lên góc box
    draw.text((box[0], box[1] - 10), f"{label}: {confidence}", fill="red")

output_path = "demo_result.jpg"
image.save(output_path)
print(f"Đã lưu ảnh kết quả thành công tại: {output_path}")