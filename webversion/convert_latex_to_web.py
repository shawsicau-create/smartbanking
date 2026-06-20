#!/usr/bin/env python3
"""
LaTeX到Web统一转换脚本
整合所有fix_*.py脚本的功能，提供统一的转换管道
"""

import os
import re
import subprocess
import sys
from pathlib import Path
from typing import List, Tuple, Optional


class LatexToWebConverter:
    """LaTeX到Web转换器"""
    
    def __init__(self, docs_dir: str = None):
        """初始化转换器"""
        if docs_dir is None:
            docs_dir = os.path.join(os.path.dirname(__file__), "src", "content", "docs")
        self.docs_dir = Path(docs_dir)
        
        # 章节标题和描述映射
        self.chapter_meta = {
            "preface": ("前言", "智慧银行实验教程前言——编者前言、教学路线图与能力矩阵"),
            "ch01": ("第1章 绪论：AI驱动的银行数字化转型", "银行业数字化转型全景、AI应用矩阵、大语言模型与Agent范式、MCP+Skill+BMAD方法论框架"),
            "ch02": ("第2章 环境搭建", "IDE安装配置、MCP服务器接入、Skill模板部署的完整实操指南"),
            "ch03": ("第3章 MCP协议", "MCP架构原理、服务器开发、银行业务数据接入"),
            "ch04": ("第4章 Skill体系", "Skill编写规范、金融Skill实例、调试与优化"),
            "ch05": ("第5章 CLI工具实战", "CLI工具生态、CNB/Skills CLI、AI编程助手"),
            "ch06": ("第6章 金融数据分析与计量经济学", "金融数据处理、面板回归、时间序列、因果推断"),
            "ch07": ("第7章 BMAD方法论与综合项目实践", "BMAD五阶段、CRM完整开发12个实验、智能客服、Vercel部署"),
            "ch08": ("第8章 课程综合项目与创新实践", "项目选题、团队管理、答辩、竞赛指南"),
            "appendix": ("附录", "环境配置速查、MCP服务器清单、Skill模板库、Prompt工程指南"),
            "labs/bmad-crm": ("BMAD-CRM系统开发实验手册", "从零到部署的完整全栈工程实战指南"),
            "labs/local-llm-deploy": ("本地大模型部署指南", "macOS Apple Silicon 部署 oMLX + Chatbox 本地大模型"),
            "labs/bmad-deploy": ("BMAD代码云端部署", "BMAD项目部署到 Vercel 的详细步骤"),
            "labs/bmad-practice": ("BMAD方法论实战", "BMAD方法论实战操作详细步骤"),
            "labs/cnb-sync": ("使用CNB同步项目库", "使用 CNB 平台同步和管理项目代码库"),
        }
        
        # 容器映射
        self.container_map = {
            r"::: theorybox": ":::tip[理论要点]",
            r"::: notebox": ":::note[提示]",
            r"::: warningbox": ":::caution[警告]",
            r"::: casebox": ":::note[案例研究]",
            r"::: practicebox": ":::tip[实操步骤]",
            r"::: exercisebox": ":::danger[练习]",
        }
        
        # LaTeX 残留清理
        self.latex_cleanup = [
            (r"\$\\rightarrow\$", "→"),
            (r"\$\\leftarrow\$", "←"),
            (r"\$\\leftrightarrow\$", "↔"),
            (r"\$\\Rightarrow\$", "⇒"),
            (r"\$\\geq\$", "≥"),
            (r"\$\\leq\$", "≤"),
            (r"\$\\neq\$", "≠"),
            (r"\$\\times\$", "×"),
            (r"\$\\pm\$", "±"),
            (r"\$\\approx\$", "≈"),
            (r"\$\\alpha\$", "α"),
            (r"\$\\beta\$", "β"),
            (r"\$\\gamma\$", "γ"),
            (r"\$\\delta\$", "δ"),
            (r"\$\\sigma\$", "σ"),
            (r"\$\\mu\$", "μ"),
            (r"\$\\lambda\$", "λ"),
            (r"\$\\pi\$", "π"),
            (r"\$\\infty\$", "∞"),
            (r"\$\\sum\$", "∑"),
            (r"\$\\hat\{([^}]+)\}\$", r"\1̂"),
            (r"\\\\", "<br/>"),
            (r"\[@([^\]]+)\]", r"[\1]"),  # pandoc citation → bracket
            (r"\\textbf\{([^}]+)\}", r"**\1**"),
            (r"\\textit\{([^}]+)\}", r"*\1*"),
            (r"\\emph\{([^}]+)\}", r"*\1*"),
            (r"\\chapter\*?\{([^}]+)\}", r"# \1"),
            (r"\\section\*?\{([^}]+)\}", r"## \1"),
            (r"\\subsection\*?\{([^}]+)\}", r"### \1"),
            (r"\\keyterms\{", "**关键术语：**"),
            (r"\\chapteroverview\{", ""),
            (r"\\begin\{enumerate\}", "1. "),
            (r"\\end\{enumerate\}", ""),
            (r"\\begin\{itemize\}", "• "),
            (r"\\end\{itemize\}", ""),
            (r"\\item\s+", ""),
        ]
    
    def fix_tables(self, content: str) -> str:
        """修复表格格式"""
        # 检查是否包含simple table
        if re.search(r'^\s*\|.*\|.*\|', content, re.MULTILINE):
            try:
                # 使用pandoc转换表格
                result = subprocess.run(
                    ['pandoc', '-f', 'markdown', '-t', 'gfm', '--columns=1000'],
                    input=content,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                if result.returncode == 0:
                    return result.stdout
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        return content
    
    def fix_codeblocks(self, content: str) -> str:
        """修复代码块格式"""
        # 修复未闭合的代码块
        lines = content.split('\n')
        in_codeblock = False
        codeblock_lang = None
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith('```'):
                if not in_codeblock:
                    in_codeblock = True
                    codeblock_lang = stripped[3:].strip()
                else:
                    in_codeblock = False
                    codeblock_lang = None
        
        # 如果代码块未闭合，在末尾添加闭合标记
        if in_codeblock:
            lines.append('```')
        
        return '\n'.join(lines)
    
    def fix_block_math(self, content: str) -> str:
        """修复块级数学公式"""
        # 确保数学公式前后有空行
        content = re.sub(r'([^\n])\n(\$\$)', r'\1\n\n\2', content)
        content = re.sub(r'(\$\$)\n([^\n])', r'\1\n\n\2', content)
        
        # 修复未闭合的数学公式
        if content.count('$$') % 2 != 0:
            content += '\n$$'
        
        return content
    
    def fix_indented(self, content: str) -> str:
        """修复缩进格式"""
        lines = content.split('\n')
        fixed_lines = []
        
        for line in lines:
            # 移除行尾空格
            line = line.rstrip()
            
            # 修复混合缩进（制表符和空格）
            if line.startswith('\t'):
                line = '    ' + line[1:]
            
            fixed_lines.append(line)
        
        return '\n'.join(fixed_lines)
    
    def fix_latex_residual(self, content: str) -> str:
        """清理LaTeX残留"""
        for pattern, replacement in self.latex_cleanup:
            content = re.sub(pattern, replacement, content)
        return content
    
    def add_frontmatter(self, content: str, slug: str) -> str:
        """添加frontmatter"""
        if slug in self.chapter_meta:
            title, description = self.chapter_meta[slug]
        else:
            title = slug
            description = ""
        
        # 移除第一行如果已经是标题行
        lines = content.split('\n')
        if lines and lines[0].startswith('# ') and not content.startswith('---'):
            content = '\n'.join(lines[1:])
        
        # 添加frontmatter
        frontmatter = f"""---
title: '{title}'
description: '{description}'
---

"""
        return frontmatter + content.strip() + '\n'
    
    def replace_containers(self, content: str) -> str:
        """替换容器语法"""
        for old, new in self.container_map.items():
            content = content.replace(old, new)
        return content
    
    def convert_file(self, filepath: Path, slug: str) -> Tuple[str, bool]:
        """转换单个文件"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 应用所有修复
            content = self.fix_tables(content)
            content = self.fix_codeblocks(content)
            content = self.fix_block_math(content)
            content = self.fix_indented(content)
            content = self.fix_latex_residual(content)
            content = self.replace_containers(content)
            content = self.add_frontmatter(content, slug)
            
            # 写回文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return slug, True
            
        except Exception as e:
            print(f"  ✗ {slug}: {str(e)}")
            return slug, False
    
    def convert_all(self) -> List[Tuple[str, bool]]:
        """转换所有文件"""
        results = []
        
        for root, dirs, files in os.walk(self.docs_dir):
            for fname in sorted(files):
                if not fname.endswith('.md') and not fname.endswith('.mdx'):
                    continue
                
                filepath = Path(root) / fname
                rel_path = filepath.relative_to(self.docs_dir)
                slug = str(rel_path.with_suffix(''))
                
                # 跳过 index.mdx
                if slug == 'index':
                    continue
                
                slug, success = self.convert_file(filepath, slug)
                results.append((slug, success))
                
                if success:
                    print(f"  ✓ {slug}")
        
        return results
    
    def validate_conversion(self) -> List[str]:
        """验证转换结果"""
        errors = []
        
        for root, dirs, files in os.walk(self.docs_dir):
            for fname in sorted(files):
                if not fname.endswith('.md') and not fname.endswith('.mdx'):
                    continue
                
                filepath = Path(root) / fname
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # 检查frontmatter
                    if not content.startswith('---'):
                        errors.append(f"{fname}: 缺少frontmatter")
                    
                    # 检查LaTeX残留
                    latex_patterns = [
                        r'\\textbf\{',
                        r'\\textit\{',
                        r'\\emph\{',
                        r'\\chapter\{',
                        r'\\section\{',
                        r'\\subsection\{',
                    ]
                    
                    for pattern in latex_patterns:
                        if re.search(pattern, content):
                            errors.append(f"{fname}: 包含LaTeX残留: {pattern}")
                            break
                    
                    # 检查未闭合的代码块
                    if content.count('```') % 2 != 0:
                        errors.append(f"{fname}: 代码块未闭合")
                    
                    # 检查未闭合的数学公式
                    if content.count('$$') % 2 != 0:
                        errors.append(f"{fname}: 数学公式未闭合")
                
                except Exception as e:
                    errors.append(f"{fname}: 读取失败: {str(e)}")
        
        return errors


def main():
    """主函数"""
    print("LaTeX到Web统一转换脚本")
    print("=" * 50)
    
    converter = LatexToWebConverter()
    
    # 转换所有文件
    print("\n开始转换文件...")
    results = converter.convert_all()
    
    # 统计结果
    success_count = sum(1 for _, success in results if success)
    fail_count = sum(1 for _, success in results if not success)
    
    print(f"\n转换完成: {success_count} 成功, {fail_count} 失败")
    
    # 验证转换结果
    print("\n验证转换结果...")
    errors = converter.validate_conversion()
    
    if errors:
        print(f"发现 {len(errors)} 个问题:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("所有文件验证通过！")
    
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
