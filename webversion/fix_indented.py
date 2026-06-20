#!/usr/bin/env python3
"""
修复 Markdown 文件中 4 空格缩进的框线/ASCII 内容：
1. 识别连续的 4 空格缩进行块
2. 如果块包含框线字符（┌│├─）→ 包裹在 ```text 代码块中
3. 如果块是 Tab 分隔的对齐文本 → 转换为 GFM 管道符表格
"""
import re
import sys
import os

def is_box_char(text):
    """检查是否包含 Unicode 框线字符"""
    return bool(re.search(r'[┌┐└┘│├┤┬┴┼─━═]', text))

def is_code_like(text):
    """检查是否是代码（JSON/编程语言）"""
    code_indicators = ['{', '}', '"', '=', 'function', 'const', 'return', 'import', '//', '/*']
    stripped = text.strip()
    return any(ind in stripped for ind in code_indicators) or stripped.endswith(';')

def is_gfm_table(text):
    """检查是否已经是GFM表格格式"""
    return text.strip().startswith('|')

def tab_to_gfm(lines):
    """将Tab/多空格对齐的文本转为GFM管道符表格"""
    result = []
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # Split on 2+ consecutive spaces or single tab
        cells = re.split(r'\t|  +', stripped)
        cells = [c.strip() for c in cells if c.strip()]
        if len(cells) >= 2:
            result.append('| ' + ' | '.join(cells) + ' |')
        else:
            result.append(stripped)
    return result

def fix_indented_blocks(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    output = []
    i = 0
    changes = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this line starts a 4-space indented block
        if line.startswith('    ') and not line.strip().startswith('|'):
            # Collect all consecutive indented lines
            block = []
            while i < len(lines) and lines[i].startswith('    ') and lines[i].strip():
                block.append(lines[i])
                i += 1
            
            # Analyze the block
            block_text = '\n'.join(block)
            block_content = [b.strip() for b in block]
            
            if is_box_char(block_text):
                # ASCII art / diagram → wrap in code block
                output.append('```text\n')
                for b in block_content:
                    output.append(b + '\n')
                output.append('```\n')
                changes += 1
            elif is_code_like(block_text):
                # Code → wrap in code block
                # Detect language
                lang = ''
                if '"name"' in block_text and '"arguments"' in block_text:
                    lang = 'json'
                elif 'function' in block_text or 'const ' in block_text:
                    lang = 'javascript'
                output.append(f'```{lang}\n' if lang else '```\n')
                for b in block_content:
                    output.append(b + '\n')
                output.append('```\n')
                changes += 1
            else:
                # Try to convert to GFM table
                gfm_lines = tab_to_gfm(block)
                if len(gfm_lines) >= 2 and '|' in gfm_lines[0]:
                    # It's a table - add separator after header
                    output.append(gfm_lines[0] + '\n')
                    # Generate separator
                    cols = gfm_lines[0].count('|') - 1
                    output.append('|' + '---|' * cols + '\n')
                    for gl in gfm_lines[1:]:
                        output.append(gl + '\n')
                    changes += 1
                else:
                    # Fallback: wrap in code block
                    output.append('```text\n')
                    for gl in gfm_lines:
                        output.append(gl + '\n')
                    output.append('```\n')
                    changes += 1
            
            # Skip any trailing blank line that was part of the block
            continue
        else:
            output.append(line)
            i += 1
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(output)
    
    return changes

if __name__ == '__main__':
    docs_dir = os.path.join(os.path.dirname(__file__), '..', 'src', 'content', 'docs')
    targets = sys.argv[1:] if len(sys.argv) > 1 else ['ch01.md', 'ch03.md']
    
    for fname in targets:
        fpath = os.path.join(docs_dir, fname)
        if not os.path.exists(fpath):
            print(f"  跳过 {fname} (不存在)")
            continue
        changes = fix_indented_blocks(fpath)
        print(f"  {fname}: 修复 {changes} 处缩进块")
