import os, sys, time
sys.path.insert(0, '/home/atin/tuan/SoPSoP/llmdet_vietnamese_food')

import torch
from mmengine.registry import init_default_scope
init_default_scope('mmdet')
from mmdet.apis import init_detector, inference_detector

config_file = 'configs/val/grounding_dino_swin_t_vifood_val.py'
checkpoint_file = 'work_dirs/vifood_vi_full_1k/iter_10000.pth'

print("Initializing model for speed benchmark...")
model = init_detector(config_file, checkpoint_file, device='cuda:0')
img_path = '../grounding_data/vifood/images/val2017/srcB_602_jpg.rf.f8d3ff41f35382573abfdca91892f080.jpg'
prompt = "Bát phở bò nóng hổi ăn kèm đĩa rau sống và chén nước chấm."

# Warmup 5 runs
print("Warming up GPU (5 runs)...")
for _ in range(5):
    with torch.no_grad():
        _ = inference_detector(model, img_path, text_prompt=prompt, custom_entities=False)

torch.cuda.synchronize()

# Benchmark 30 runs
print("Benchmarking 30 runs...")
latencies = []
for i in range(30):
    t0 = time.perf_counter()
    with torch.no_grad():
        _ = inference_detector(model, img_path, text_prompt=prompt, custom_entities=False)
    torch.cuda.synchronize()
    latencies.append((time.perf_counter() - t0) * 1000)

avg_latency = sum(latencies) / len(latencies)
p50_latency = sorted(latencies)[len(latencies)//2]
min_latency = min(latencies)
max_latency = max(latencies)
fps = 1000.0 / avg_latency
vram_mb = torch.cuda.max_memory_allocated() / (1024 * 1024)

print("\n" + "="*50)
print("⚡ KẾT QUẢ BENCHMARK SUY LUẬN (INFERENCE PERFORMANCE)")
print("="*50)
print(f"Phần cứng:           NVIDIA GeForce RTX 3090 (24GB)")
print(f"Mô hình:             Grounding DINO Swin-T (Exp 3 Checkpoint)")
print(f"Độ trễ trung bình:   {avg_latency:.2f} ms")
print(f"Độ trễ trung vị P50: {p50_latency:.2f} ms")
print(f"Độ trễ tối thiểu:    {min_latency:.2f} ms")
print(f"Tốc độ khung hình:   {fps:.2f} FPS")
print(f"VRAM tiêu thụ:       {vram_mb:.1f} MB (~{vram_mb/1024:.2f} GB / 24 GB)")
print("="*50)
