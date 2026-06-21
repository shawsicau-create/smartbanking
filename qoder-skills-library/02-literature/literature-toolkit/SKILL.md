---
name: literature-toolkit
description: "Academic literature CLI: search, parse, and analyze research papers."
workflow_stage: literature
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - literature
  - analysis
  - parser
  - search
---

# Literature Toolkit

## Purpose

学术文献分析工具包，提供命令行接口(CLI)用于搜索、解析和分科学术论文。包含分析器(analyzer)、解析器(parsers)和指针搜索(zhizhen_search)模块。

## When to Use

- 需要对学术文献进行批量解析和分析时使用
- 需要搜索和筛选相关论文时触发
- 触发词: "文献工具"、"literature toolkit"、"论文解析"

## Instructions

### Step 1: Install and Configure

```bash
cd literature-toolkit
pip install -e .
```

### Step 2: Search Papers

使用zhizhen_search模块搜索相关论文:
```bash
python zhizhen_search.py --query "structural equation modeling" --max-results 20
```

### Step 3: Parse and Analyze

使用parsers和analyzer模块解析论文内容:
```bash
python cli.py analyze --input papers/ --output results/
```

## Example Prompts

- "解析这篇PDF论文的核心论点和方法论"
- "搜索SEM相关的最新文献"
- "批量分析10篇论文的引用网络"

## Requirements

### Software
- Python 3.10+

### Packages
- `pdfplumber`, `scholarly`, `pandas`

## Best Practices

1. 批量操作前先测试单篇论文解析
2. 保存中间结果避免重复解析
3. 标注论文来源和质量等级

## Common Pitfalls

- ❌ PDF解析失败时未处理异常
- ❌ 搜索结果未去重
- ❌ 忽略论文发表年份的时效性

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library