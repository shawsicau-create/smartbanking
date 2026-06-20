#!/usr/bin/env python3
"""将单行 $$公式$$ 转换为多行格式，使 remark-math 能正确识别为块级公式"""

import re
import os

DOCS_DIR = os.path.join(os.path.dirname(__file__), "src", "content", "docs")

# 匹配单行的 $$...$$ （行首到行尾，中间不含 $$）
PATTERN = re.compile(r'^\$\$(.+)\$\$$')


def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    changed = 0
    new_lines = []
    for line in lines:
        m = PATTERN.match(line.rstrip('\n'))
        if m:
            formula = m.group(1)
            # 转为多行格式
            new_lines.append('$$\n')
            new_lines.append(formula + '\n')
            new_lines.append('$$\n')
            changed += 1
        else:
            new_lines.append(line)

    if changed > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

    return changed


def main():
    total = 0
    for root, dirs, files in os.walk(DOCS_DIR):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            filepath = os.path.join(root, fname)
            count = fix_file(filepath)
            if count > 0:
                rel = os.path.relpath(filepath, DOCS_DIR)
                print(f"  ✓ {rel}: {count} 处块级公式已转换")
                total += count

    print(f"\n共转换 {total} 处")


if __name__ == '__main__':
    print("开始转换单行块级公式...\n")
    main()
    print("完成！")
