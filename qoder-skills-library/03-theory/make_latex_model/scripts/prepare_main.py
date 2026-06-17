#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
main.tex 预处理工具

自动注释掉 main.tex 中的 \\input{} 行，保留标题结构，
用于生成仅包含标题的 PDF 进行像素级对比。

使用方法:
    # 预处理（注释 input 行）
    python scripts/prepare_main.py projects/NSFC_Young/main.tex

    # 恢复（取消注释）
    python scripts/prepare_main.py projects/NSFC_Young/main.tex --restore

    # 指定备份目录
    python scripts/prepare_main.py projects/NSFC_Young/main.tex --backup-dir projects/NSFC_Young/.make_latex_model/backup

    # 预览模式（不修改文件）
    python scripts/prepare_main.py projects/NSFC_Young/main.tex --dry-run

    # 调试：为像素级对齐插入“空白占位”（仅对被注释的 extraTex 输入）
    python scripts/prepare_main.py projects/NSFC_Young/main.tex --add-placeholders
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime
from typing import Tuple, List, Optional


def find_input_lines(content: str) -> List[Tuple[int, str]]:
    """
    查找所有 \\input{} 行

    Args:
        content: 文件内容

    Returns:
        [(行号, 行内容), ...] 列表
    """
    input_pattern = re.compile(r'^(\s*)\\input\{([^}]+)\}', re.MULTILINE)
    lines = content.split('\n')
    results = []

    for i, line in enumerate(lines, 1):
        if input_pattern.match(line):
            results.append((i, line))

    return results


def comment_input_lines(content: str, add_placeholders: bool = False) -> Tuple[str, int]:
    """
    注释掉所有 \\input{} 行

    Args:
        content: 原始文件内容
        add_placeholders: 是否在被注释的 extraTex 输入处插入“空白占位”（用于像素对齐调试）

    Returns:
        (修改后的内容, 修改的行数)
    """
    lines = content.split('\n')
    modified_count = 0

    # 匹配 \input{} 行（未被注释的）
    input_pattern = re.compile(r'^(\s*)\\input\{([^}]+)\}')

    out_lines: List[str] = []
    for line in lines:
        match = input_pattern.match(line)
        if not match or line.strip().startswith('%'):
            out_lines.append(line)
            continue

        # Keep the style config in place; otherwise the prepared document won't compile.
        input_target = match.group(2).strip()
        input_target_norm = input_target.replace('\\', '/')
        if input_target_norm.endswith('/@config.tex') or input_target_norm.endswith('@config.tex'):
            out_lines.append(line)
            continue

        indent = match.group(1)
        out_lines.append(f"{indent}% [PREPARE_MAIN_COMMENTED] {line.strip()}")
        modified_count += 1

        # 为像素级对比保留“空白占位”：只对 extraTex 正文段落插入 1 行空白
        # （Word 模板通常在各提纲标题后留一个空段落用于填写）
        if add_placeholders and input_target_norm.startswith("extraTex/"):
            out_lines.append(f"{indent}\\vspace*{{\\baselineskip}} % [PREPARE_MAIN_PLACEHOLDER]")

    return '\n'.join(out_lines), modified_count


def restore_input_lines(content: str) -> Tuple[str, int]:
    """
    恢复被注释的 \\input{} 行

    Args:
        content: 文件内容

    Returns:
        (修改后的内容, 恢复的行数)
    """
    lines = content.split('\n')
    restored_count = 0

    # 匹配带有标记的注释行
    comment_pattern = re.compile(r'^(\s*)% \[PREPARE_MAIN_COMMENTED\] (.+)$')

    out_lines: List[str] = []
    for line in lines:
        if "[PREPARE_MAIN_PLACEHOLDER]" in line:
            continue
        match = comment_pattern.match(line)
        if match:
            indent = match.group(1)
            original_content = match.group(2)
            out_lines.append(f"{indent}{original_content}")
            restored_count += 1
        else:
            out_lines.append(line)

    return '\n'.join(out_lines), restored_count


def is_prepared(content: str) -> bool:
    """
    检查文件是否已被预处理

    Args:
        content: 文件内容

    Returns:
        是否已预处理
    """
    return '[PREPARE_MAIN_COMMENTED]' in content


def create_backup(file_path: Path, backup_dir: Optional[Path] = None) -> Path:
    """
    创建备份文件

    Args:
        file_path: 原文件路径
        backup_dir: 备份目录（可选）

    Returns:
        备份文件路径
    """
    # 本地备份
    local_backup = file_path.with_suffix('.tex.bak')
    shutil.copy2(file_path, local_backup)

    # 如果指定了备份目录，也复制一份
    if backup_dir:
        backup_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        remote_backup = backup_dir / f"main_{timestamp}.tex.bak"
        shutil.copy2(file_path, remote_backup)

    return local_backup


def extract_section_structure(content: str) -> List[dict]:
    """
    提取文档的章节结构（用于报告）

    Args:
        content: 文件内容

    Returns:
        章节结构列表
    """
    sections = []

    # 匹配各级标题
    section_pattern = re.compile(
        r'^(\s*)\\(section|subsection|subsubsection)\{([^}]+)\}',
        re.MULTILINE
    )

    for match in section_pattern.finditer(content):
        level = match.group(2)
        title = match.group(3)
        sections.append({
            'level': level,
            'title': title[:50] + ('...' if len(title) > 50 else ''),
        })

    return sections


def main():
    parser = argparse.ArgumentParser(
        description="main.tex 预处理工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
    # 预处理（注释 input 行）
    python prepare_main.py projects/NSFC_Young/main.tex

    # 恢复（取消注释）
    python prepare_main.py projects/NSFC_Young/main.tex --restore

    # 预览模式
    python prepare_main.py projects/NSFC_Young/main.tex --dry-run
        """
    )

    parser.add_argument("main_tex", type=Path, help="main.tex 文件路径")
    parser.add_argument("--restore", "-r", action="store_true",
                       help="恢复被注释的 input 行")
    parser.add_argument("--backup-dir", type=Path,
                       help="备份目录（除了本地备份外）")
    parser.add_argument("--dry-run", "-n", action="store_true",
                       help="预览模式，不实际修改文件")
    parser.add_argument("--force", "-f", action="store_true",
                       help="强制执行，不检查当前状态")
    parser.add_argument("--add-placeholders", action="store_true",
                       help="为像素对齐调试插入空白占位（仅在预处理模式生效）")

    args = parser.parse_args()

    # 检查文件存在
    if not args.main_tex.exists():
        print(f"❌ 错误: 文件不存在: {args.main_tex}")
        sys.exit(1)

    # 读取文件
    content = args.main_tex.read_text(encoding='utf-8')

    print(f"\n{'='*60}")
    print(f"main.tex 预处理工具")
    print(f"{'='*60}")
    print(f"文件: {args.main_tex}")
    print(f"模式: {'恢复' if args.restore else '预处理'}")
    print(f"预览: {'是' if args.dry_run else '否'}")
    if not args.restore:
        print(f"占位: {'是' if args.add_placeholders else '否'}")

    # 检查当前状态
    prepared = is_prepared(content)
    print(f"\n当前状态: {'已预处理' if prepared else '原始状态'}")

    if args.restore:
        # 恢复模式
        if not prepared and not args.force:
            print("⚠️  文件未被预处理，无需恢复")
            print("💡 使用 --force 强制执行")
            sys.exit(0)

        new_content, count = restore_input_lines(content)
        action = "恢复"
    else:
        # 预处理模式
        if prepared and not args.force:
            print("⚠️  文件已被预处理，请先恢复")
            print("💡 使用 --restore 恢复，或 --force 强制执行")
            sys.exit(0)

        # 显示将被注释的行
        input_lines = find_input_lines(content)
        print(f"\n找到 {len(input_lines)} 个 \\input{{}} 行:")
        for line_num, line_content in input_lines[:5]:
            print(f"  第 {line_num} 行: {line_content.strip()[:60]}...")
        if len(input_lines) > 5:
            print(f"  ... 还有 {len(input_lines) - 5} 行")

        new_content, count = comment_input_lines(content, add_placeholders=args.add_placeholders)
        action = "注释"

    # 显示章节结构
    sections = extract_section_structure(content)
    if sections:
        print(f"\n保留的章节结构 ({len(sections)} 个):")
        for sec in sections[:5]:
            indent = "  " if sec['level'] == 'section' else "    "
            print(f"{indent}\\{sec['level']}{{{sec['title']}}}")
        if len(sections) > 5:
            print(f"  ... 还有 {len(sections) - 5} 个章节")

    if args.dry_run:
        print(f"\n🔍 预览模式: 将{action} {count} 行")
        print("💡 移除 --dry-run 以实际执行")
    else:
        # 创建备份
        if not args.restore:
            backup_path = create_backup(args.main_tex, args.backup_dir)
            print(f"\n📦 备份已创建: {backup_path}")
            if args.backup_dir:
                print(f"📦 远程备份: {args.backup_dir}")

        # 写入文件
        args.main_tex.write_text(new_content, encoding='utf-8')
        print(f"\n✅ 已{action} {count} 行")

    print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
