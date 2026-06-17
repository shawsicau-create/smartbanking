#!/bin/bash
# 汉源花椒保险ABM实验 — 一键运行脚本
# 用法: bash start.sh

set -e
cd "$(dirname "$0")"

echo "============================================"
echo "  汉源花椒保险ABM实验 启动器"
echo "============================================"

# 检查并创建虚拟环境
if [ ! -d ".venv" ]; then
    echo "[1/3] 创建Python虚拟环境..."
    python3 -m venv .venv
fi

# 激活虚拟环境
source .venv/bin/activate

# 安装依赖
echo "[2/3] 安装依赖包..."
pip install -q -r requirements.txt

# 运行仿真
echo "[3/3] 运行汉源花椒保险ABM仿真..."
echo ""
python3 run.py

echo ""
echo "完成！请查看 results/ 目录。"
