#!/usr/bin/env python3
"""修复 pandoc 生成的代码块语言标记"""
import os
import re

DOCS = os.path.join(os.path.dirname(__file__), "src", "content", "docs")

# 映射表
STYLE_MAP = {
    'shell': 'bash',
    'python': 'python',
    'json': 'json',
    'stata': 'stata',
    'html': 'html',
    'text': 'text',
}

count = 0
for root, dirs, files in os.walk(DOCS):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        original = content

        # Fix: ``` {style="shell"}  ->  ```bash
        for style, lang in STYLE_MAP.items():
            content = content.replace(f'``` {{style="{style}"}}', f'```{lang}')

        # Fix: ``` {.JavaScript language="JavaScript"}  ->  ```javascript
        content = re.sub(r'``` \{\.\w+ language="(\w+)"\}',
                         lambda m: '```' + m.group(1).lower(), content)

        # Fix: ``` {.python}  ->  ```python
        content = re.sub(r'``` \{\.(\w+)\}',
                         lambda m: '```' + m.group(1), content)

        # Fix: ``` {verbatim} or ``` {verbatim,xxx}  ->  ```text
        content = re.sub(r'``` \{verbatim[^\}]*\}', '```text', content)

        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            count += 1
            print(f"  Fixed: {fname}")

print(f"\nTotal: {count} files fixed")
