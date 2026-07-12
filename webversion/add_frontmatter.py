#!/usr/bin/env python3
"""
为新转换的Markdown文件添加frontmatter
"""

import os
from pathlib import Path

# 章节标题和描述映射
chapter_meta = {
    "ch02": ("第2章 环境搭建", "IDE安装配置、MCP服务器接入、Skill模板部署的完整实操指南"),
    "ch03": ("第3章 MCP协议", "MCP架构原理、服务器开发、银行业务数据接入"),
    "ch04": ("第4章 Skill体系", "Skill编写规范、金融Skill实例、调试与优化"),
    "ch05": ("第5章 CLI工具实战", "CLI工具生态、CNB/Skills CLI、AI编程助手"),
    "ch06": ("第6章 金融数据分析与计量经济学", "金融数据处理、面板回归、时间序列、因果推断"),
    "ch07": ("第7章 BMAD方法论与综合项目实践", "BMAD五阶段、CRM完整开发12个实验、智能客服、EdgeOne Pages部署"),
    "ch08": ("第8章 课程综合项目与创新实践", "项目选题、团队管理、答辩、竞赛指南"),
}

docs_dir = Path(
    "/Users/xiaoshiishun/微云同步助手(275531137)/当前工作/期末成绩处理 国际金融 智慧银行/智慧银行讲义 成绩 学生报告/webversion/src/content/docs")

for slug, (title, description) in chapter_meta.items():
    filepath = docs_dir / f"{slug}.md"
    if filepath.exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查是否已有frontmatter
        if not content.startswith('---'):
            # 添加frontmatter
            frontmatter = f"""---
title: '{title}'
description: '{description}'
---

"""
            content = frontmatter + content

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"✓ Added frontmatter to {slug}.md")
        else:
            print(f"  {slug}.md already has frontmatter")
