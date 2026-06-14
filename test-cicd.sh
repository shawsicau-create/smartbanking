#!/bin/bash
# CI/CD 测试脚本
# 用于本地测试GitHub Actions构建流程

set -e  # 遇到错误立即退出

echo "=== 智慧银行实验教程 CI/CD 测试 ==="
echo ""

# 检查必要工具
echo "1. 检查必要工具..."
command -v xelatex >/dev/null 2>&1 || { echo "错误: 未找到xelatex"; exit 1; }
command -v biber >/dev/null 2>&1 || { echo "错误: 未找到biber"; exit 1; }
command -v make >/dev/null 2>&1 || { echo "错误: 未找到make"; exit 1; }
echo "   ✓ 工具检查通过"

# 清理旧文件
echo ""
echo "2. 清理旧文件..."
make clean
echo "   ✓ 清理完成"

# 检查LaTeX语法
echo ""
echo "3. 检查LaTeX语法..."
make check
echo "   ✓ 语法检查通过"

# 编译PDF
echo ""
echo "4. 编译PDF文件..."
make pdf
echo "   ✓ PDF编译成功"

# 验证PDF文件
echo ""
echo "5. 验证PDF文件..."
if [ -f "智慧银行实验教程chapters/智慧银行实验教程.pdf" ]; then
    echo "   ✓ PDF文件存在"
    echo "   文件大小: $(du -h "智慧银行实验教程chapters/智慧银行实验教程.pdf" | cut -f1)"
else
    echo "   ✗ PDF文件不存在"
    exit 1
fi

echo ""
echo "=== 测试完成 ==="
echo "所有检查通过！CI/CD配置应该可以正常工作。"
