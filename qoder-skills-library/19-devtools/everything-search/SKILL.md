---
name: everything-search
description: Fast file system search using Everything SDK for Windows or spotlight/find for macOS to locate research files and data.
workflow_stage: data
compatibility:
  - claude-code
  - cursor
  - codex
author: Qoder Skills Library
version: 1.0.0
tags:
  - devtools
  - search
  - file-system
  - utility
---

# Everything Search

## Purpose

使用Everything SDK(Windows)或spotlight/find(macOS)进行快速文件系统搜索，快速定位研究文件和数据。

## When to Use

- 需要快速搜索本地文件系统时使用
- 定位特定数据文件或代码时触发
- 触发词："搜索文件"、"找文件"、"everything"

## Instructions

### Step 1
确认搜索目标：文件名/内容/类型/日期
### Step 2
构建搜索查询：关键词+文件类型+路径过滤
### Step 3
执行搜索并按相关性排序结果
### Step 4
对结果做摘要和分类
### Step 5
提供最相关文件的路径和简介

## Example Prompts

- "搜索所有.dta数据文件"
- "找到包含'sem'关键词的.do文件"
- "定位最近修改的LaTeX文件"

## Requirements

### Software
- Python 3.10+ or appropriate runtime

## Best Practices

1. **组合多个搜索条件缩小范围**
2. **使用文件类型过滤**
3. **标注搜索结果的可信度**

## Common Pitfalls

- ❌ 搜索条件过于宽泛导致结果太多
- ❌ 忽视文件版本差异
- ❌ 不验证搜索结果的完整性

## Changelog

### v1.0.0
- Initial release from Qoder Skills Library
