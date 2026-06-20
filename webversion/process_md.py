#!/usr/bin/env python3
"""批量后处理 Markdown 文件：添加 frontmatter、替换容器、清理 LaTeX 残留"""

import os
import re

DOCS_DIR = os.path.join(os.path.dirname(__file__), "src", "content", "docs")

# 章节标题和描述映射
CHAPTER_META = {
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
CONTAINER_MAP = {
    r"::: theorybox": ":::tip[理论要点]",
    r"::: notebox": ":::note[提示]",
    r"::: warningbox": ":::caution[警告]",
    r"::: casebox": ":::note[案例研究]",
    r"::: practicebox": ":::tip[实操步骤]",
    r"::: exercisebox": ":::danger[练习]",
}

# LaTeX 残留清理
LATEX_CLEANUP = [
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


def process_file(filepath, slug):
    """处理单个 Markdown 文件"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 获取元数据
    if slug in CHAPTER_META:
        title, description = CHAPTER_META[slug]
    else:
        title = slug
        description = ""

    # 替换容器
    for old, new in CONTAINER_MAP.items():
        content = content.replace(old, new)

    # 清理 LaTeX 残留
    for pattern, replacement in LATEX_CLEANUP:
        content = re.sub(pattern, replacement, content)

    # 移除第一行如果已经是标题行（pandoc 会生成 # 标题）
    lines = content.split("\n")
    if lines and lines[0].startswith("# ") and not content.startswith("---"):
        # 移除原始标题行，用 frontmatter 中的 title 替代
        content = "\n".join(lines[1:])

    # 添加 frontmatter
    frontmatter = f"""---
title: '{title}'
description: '{description}'
---

"""
    content = frontmatter + content.strip() + "\n"

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return title


def main():
    processed = []
    for root, dirs, files in os.walk(DOCS_DIR):
        for fname in sorted(files):
            if not fname.endswith(".md") and not fname.endswith(".mdx"):
                continue
            filepath = os.path.join(root, fname)
            # 计算 slug（相对于 docs 目录，去掉 .md 扩展名）
            rel_path = os.path.relpath(filepath, DOCS_DIR)
            slug = os.path.splitext(rel_path)[0]

            # 跳过 index.mdx
            if slug == "index":
                continue

            title = process_file(filepath, slug)
            processed.append((slug, title, filepath))
            print(f"  ✓ {slug}: {title}")

    print(f"\n共处理 {len(processed)} 个文件")


if __name__ == "__main__":
    print("开始批量后处理 Markdown 文件...\n")
    main()
    print("\n处理完成！")
