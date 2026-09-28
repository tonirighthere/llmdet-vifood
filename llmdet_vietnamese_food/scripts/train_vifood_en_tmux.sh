#!/bin/bash
# ==============================================================================
# Script huấn luyện LLMDet ViFood-1K Thí nghiệm 2 (Tiếng Anh - Ablation Study)
# trong Tmux (Chống ngắt kết nối SSH)
# ==============================================================================

SESSION_NAME="vifood_en_train"
WORK_DIR="/home/atin/tuan/SoPSoP/llmdet_vietnamese_food/work_dirs/vifood_en_1k"
CONFIG_PATH="configs/grounding_dino_swin_t_vifood_en.py"

mkdir -p "$WORK_DIR"

tmux has-session -t "$SESSION_NAME" 2>/dev/null

if [ $? == 0 ]; then
    echo "⚠️ Tmux session '$SESSION_NAME' ĐANG CHẠY!"
    echo "👉 Để xem trực tiếp tiến trình, gõ: tmux attach -t $SESSION_NAME"
    echo "👉 Để dừng session, gõ: tmux kill-session -t $SESSION_NAME"
    exit 0
fi

echo "🚀 Đang khởi chạy training LLMDet Thí nghiệm 2 (Tiếng Anh) trong tmux session '$SESSION_NAME'..."

tmux new-session -d -s "$SESSION_NAME" "bash -c '
    export CUDA_VISIBLE_DEVICES=0
    export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
    export PYTHONPATH=/home/atin/tuan/SoPSoP/llmdet_vietnamese_food:\$PYTHONPATH
    cd /home/atin/tuan/SoPSoP/llmdet_vietnamese_food

    python3 mmdet_train.py \"$CONFIG_PATH\" \
        --work-dir \"$WORK_DIR\" \
        --amp \
        2>&1 | tee \"$WORK_DIR/train.log\"
    exec bash
'"

echo "=================================================================="
echo "✅ Huấn luyện Thí nghiệm 2 (Tiếng Anh) đã khởi chạy trong Tmux!"
echo "=================================================================="
echo "📌 Tên session  : $SESSION_NAME"
echo "📌 Log file     : $WORK_DIR/train.log"
echo "📌 Xem trực tiếp: tmux attach -t $SESSION_NAME"
echo "📌 Thoát ra     : Nhấn tổ hợp phím [Ctrl + B], sau đó nhấn phím [D]"
echo "=================================================================="
