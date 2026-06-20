#!/usr/bin/env python3
"""将 pandoc simple table 格式转换为 GFM 管道符表格格式

策略：逐文件扫描，检测 simple table 分隔行，提取整个表格块，
调用 pandoc -f markdown -t gfm 转换，替换回去。
不影响 frontmatter、callout 等其他内容。
"""

import os
import re
import subprocess
import glob

DOCS_DIR = os.path.join(os.path.dirname(__file__), "src", "content", "docs")

# simple table 分隔行：缩进 + 至少两列 --- 块
# 例: "  ---------- ---------- --------"
SEP_PATTERN = re.compile(r'^(\s+)-{2,}(\s+-{2,})+\s*$')

# simple table 数据行：有缩进，含非空白内容
# 但需要排除代码块内的内容
DATA_LINE_PATTERN = re.compile(r'^(\s{2,})\S')


def is_table_separator(line):
    """判断是否为 simple table 分隔行"""
    return bool(SEP_PATTERN.match(line))


def find_table_block(lines, sep_idx):
    """从分隔行位置出发，向前找表头，向后找数据行，返回 (start, end)"""
    # 向前找表头（直到空行或非缩进行）
    start = sep_idx
    while start > 0:
        prev = lines[start - 1]
        # 表头行应该有缩进且非空
        if prev.strip() == '' or not prev.startswith('  '):
            break
        # 避免无限回溯（最多5行表头）
        if sep_idx - start > 4:
            break
        start -= 1

    # 向后找数据行（直到空行或非缩进行）
    end = sep_idx + 1
    while end < len(lines):
        curr = lines[end]
        # 数据行应该有缩进且非空
        if curr.strip() == '' or not curr.startswith('  '):
            break
        # 排除另一个分隔行（下一个表格的分隔行）
        if is_table_separator(curr):
            break
        # 排除 callout 或其他特殊行
        if curr.strip().startswith(':::') or curr.strip().startswith(': '):
            break
        end += 1

    return start, end


def convert_table_with_pandoc(table_text):
    """用 pandoc 将 simple table 转换为 GFM pipe table"""
    try:
        result = subprocess.run(
            ['pandoc', '-f', 'markdown', '-t', 'gfm', '--wrap=none'],
            input=table_text,
            capture_output=True,
            text=True,
            timeout=10
        )
        if result.returncode == 0 and '|' in result.stdout:
            return result.stdout.rstrip('\n')
    except Exception as e:
        print(f"    pandoc 转换失败: {e}")
    return None


def process_file(filepath):
    """处理单个文件"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    # 标记需要转换的表格块
    replacements = []  # (start, end, new_text)

    i = 0
    while i < len(lines):
        if is_table_separator(lines[i]):
            start, end = find_table_block(lines, i)
            if end > start + 1:  # 至少有表头+分隔+1行数据
                table_text = '\n'.join(lines[start:end])
                converted = convert_table_with_pandoc(table_text)
                if converted:
                    replacements.append((start, end, converted))
                    i = end
                    continue
        i += 1

    if not replacements:
        return 0

    # 从后往前替换（避免索引偏移）
    for start, end, new_text in reversed(replacements):
        lines[start:end] = new_text.split('\n')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    return len(replacements)


def main():
    total = 0
    files_fixed = []

    for pattern in ['*.md', 'labs/*.md']:
        for filepath in sorted(glob.glob(os.path.join(DOCS_DIR, pattern))):
            count = process_file(filepath)
            if count > 0:
                rel = os.path.relpath(filepath, DOCS_DIR)
                print(f"  ✓ {rel}: {count} 个表格已转换")
                files_fixed.append(rel)
                total += count

    print(f"\n共转换 {total} 个表格（{len(files_fixed)} 个文件）")


if __name__ == '__main__':
    print("开始转换 pandoc simple table → GFM pipe table...\n")
    main()
    print("\n完成！")
