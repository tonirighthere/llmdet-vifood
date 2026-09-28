#!/usr/bin/env python3
"""
scripts/download_weights.py
===========================
Tải các pretrained weights cần thiết cho LLMDet vào thư mục huggingface/:
1. bert-base-uncased (Text backbone)
2. my_llava-onevision-qwen2-0.5b-ov-2 (LMM backbone từ fushh7/LLMDet)
3. grounding_dino_swin-t_pretrain checkpoint từ OpenMMLab
"""

import os
import sys
import urllib.request
from huggingface_hub import snapshot_download

BASE_DIR = "/home/atin/tuan/SoPSoP"
HF_DIR = os.path.join(BASE_DIR, "huggingface")
BERT_DIR = os.path.join(HF_DIR, "bert-base-uncased")
LMM_DIR = os.path.join(HF_DIR, "my_llava-onevision-qwen2-0.5b-ov-2")
MM_GDINO_DIR = os.path.join(HF_DIR, "mm_grounding_dino")

GDINO_SWIN_T_URL = "https://download.openmmlab.com/mmdetection/v3.0/mm_grounding_dino/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det/grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth"
GDINO_CKPT_PATH = os.path.join(MM_GDINO_DIR, "grounding_dino_swin-t_pretrain_obj365_goldg_grit9m_v3det_20231204_095047-b448804b.pth")

def download_file_with_progress(url, dest_path):
    if os.path.exists(dest_path) and os.path.getsize(dest_path) > 100 * 1024 * 1024:
        print(f"✅ Đã có sẵn: {dest_path} ({os.path.getsize(dest_path) / (1024*1024):.1f} MB)")
        return

    print(f"⏳ Đang tải từ {url} -> {dest_path}...")
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    temp_path = dest_path + ".tmp"

    def reporthook(blocknum, blocksize, totalsize):
        readsofar = blocknum * blocksize
        if totalsize > 0:
            percent = readsofar * 100 / totalsize
            s = f"\r   Tiến độ: {readsofar / (1024*1024):.1f} MB / {totalsize / (1024*1024):.1f} MB ({percent:.1f}%)"
            sys.stdout.write(s)
            sys.stdout.flush()

    urllib.request.urlretrieve(url, temp_path, reporthook)
    os.rename(temp_path, dest_path)
    print(f"\n✅ Đã tải xong: {dest_path}")

def main():
    print("=" * 60)
    print("🚀 BƯỚC 3: TẢI PRETRAINED WEIGHTS CHO LLMDET")
    print("=" * 60)

    os.makedirs(HF_DIR, exist_ok=True)
    os.makedirs(MM_GDINO_DIR, exist_ok=True)

    # 1. Tải BERT
    print("\n📦 1/3: Kiểm tra / tải bert-base-uncased...")
    if not os.path.exists(os.path.join(BERT_DIR, "config.json")):
        snapshot_download(
            repo_id="google-bert/bert-base-uncased",
            local_dir=BERT_DIR,
            local_dir_use_symlinks=False
        )
        print(f"✅ Đã tải bert-base-uncased vào: {BERT_DIR}")
    else:
        print(f"✅ bert-base-uncased đã có sẵn tại: {BERT_DIR}")

    # 2. Tải my_llava-onevision-qwen2-0.5b-ov-2
    print("\n📦 2/3: Kiểm tra / tải my_llava-onevision-qwen2-0.5b-ov-2 từ fushh7/LLMDet...")
    if not os.path.exists(os.path.join(LMM_DIR, "config.json")) or not os.path.exists(os.path.join(LMM_DIR, "mm_projector2.bin")):
        snapshot_download(
            repo_id="fushh7/LLMDet",
            allow_patterns=["my_llava-onevision-qwen2-0.5b-ov-2/*"],
            local_dir=HF_DIR,
            local_dir_use_symlinks=False
        )
        print(f"✅ Đã tải LLaVA model vào: {LMM_DIR}")
    else:
        print(f"✅ my_llava-onevision-qwen2-0.5b-ov-2 đã có sẵn tại: {LMM_DIR}")

    # 3. Tải Grounding DINO Swin-T Checkpoint
    print("\n📦 3/3: Kiểm tra / tải checkpoint Grounding DINO Swin-T...")
    download_file_with_progress(GDINO_SWIN_T_URL, GDINO_CKPT_PATH)

    print("\n" + "=" * 60)
    print("🎉 TẤT CẢ PRETRAINED WEIGHTS ĐÃ SẴN SÀNG!")
    print("=" * 60)

if __name__ == "__main__":
    main()
