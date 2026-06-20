#!/usr/bin/env python3
"""修复 pandoc 转换后残留的 LaTeX 属性和环境标记"""

import os
import re
import glob

DOCS_DIR = os.path.join(os.path.dirname(__file__), "src", "content", "docs")


def fix_unnumbered_attrs(content):
    """移除标题中的 {#id .unnumbered} 属性
    例: "## 一、编者前言 {#一编者前言 .unnumbered}" → "## 一、编者前言"
    """
    # 匹配标题行末尾的 {#... .unnumbered} 或 {#... .unnumbered ...}
    # 注意属性可能跨行，但通常是单行
    pattern = r'(\#{1,6}\s+.+?)\s*\{#[^}]*\.unnumbered[^}]*\}'
    content = re.sub(pattern, r'\1', content)
    return content


def fix_flushright_minipage(content):
    """修复 flushright/minipage 环境残留
    pandoc 将 \begin{flushright}\begin{minipage}...\end{minipage}\end{flushright}
    转换为 :::: flushright ::: minipage ... ::: ::::
    需要将其转换为右对齐的文本块
    """
    # 匹配 :::: flushright ::: minipage ... ::: :::: 模式
    pattern = r'::::\s*flushright\s*\n:::\s*minipage\s*\n(.*?)\n:::\s*\n::::'

    def replace_block(m):
        inner = m.group(1)
        # 将 \\ 转换为换行
        inner = inner.replace('\\\\', '\n')
        # 包裹在右对齐的 div 中
        return f'<div style="text-align: right;">\n\n{inner}\n\n</div>'

    content = re.sub(pattern, replace_block, content, flags=re.DOTALL)
    return content


def fix_other_residuals(content):
    """清理其他零散的 LaTeX/pandoc 残留"""
    # 清理残留的 \\\\ 在行尾（LaTeX 换行符）
    content = re.sub(r'\\\\\s*$', '', content, flags=re.MULTILINE)

    # 清理空的 fenced div（:::: ... ::::）
    # 匹配只有围栏没有内容的空块
    content = re.sub(r'::::?\s*\n::::?\s*\n', '', content)

    return content


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    content = fix_unnumbered_attrs(content)
    content = fix_flushright_minipage(content)
    content = fix_other_residuals(content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    fixed = []
    # 处理所有 .md 文件
    for pattern in ['*.md', 'labs/*.md']:
        for filepath in glob.glob(os.path.join(DOCS_DIR, pattern)):
            if process_file(filepath):
                name = os.path.relpath(filepath, DOCS_DIR)
                fixed.append(name)
                print(f"  ✓ 修复: {name}")

    if fixed:
        print(f"\n共修复 {len(fixed)} 个文件")
    else:
        print("\n所有文件均无问题，无需修复")


if __name__ == '__main__':
    print("开始修复 LaTeX 残留...\n")
    main()
    print("\n修复完成！")
