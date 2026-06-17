# PaperFinder 文献综述助手

一个智能文献综述技能，使用 Allen AI 的 PaperFinder 进行学术文献检索、分析和下载。

## 功能特性

- 🔍 **智能检索**: 使用 PaperFinder 进行语义化文献搜索
- 📊 **质量评估**: 根据引用数、期刊影响力等评估论文重要性
- 📝 **综述生成**: 自动生成结构化的文献综述报告
- 📥 **自动下载**: 从 arXiv 等开放获取源下载重要文献
- 📚 **引用管理**: 生成 BibTeX 格式的引用信息

## 快速开始

### 使用方法

在支持的 AI 编码助手中（如 Claude Code、Cursor、Qoder 等），使用以下方式调用技能：

```
使用 paper-finder-research 技能，研究主题是 "Transformer models in NLP"
```

或提供更详细的参数：

```
使用 paper-finder-research 技能：
- 研究主题: "Few-shot learning methods"
- 最大论文数: 25
- 年份范围: "2020-2024"
- 下载重要文献: true
```

### 参数说明

- **research_topic** (必需): 研究主题或关键词
- **max_papers** (可选): 要分析的最大论文数量，默认 20
- **year_range** (可选): 年份范围，默认 "2020-2024"
- **download_important** (可选): 是否自动下载重要文献，默认 true
- **output_format** (可选): 输出格式，支持 "markdown" 或 "json"

## 输出说明

技能会在您的项目目录中创建以下文件结构：

```
project-root/
├── literature-review/
│   ├── review-[topic]-[date].md          # 文献综述报告
│   ├── bibliography-[topic]-[date].bib   # BibTeX 引用文件
│   └── paper-list-[topic]-[date].json    # 结构化论文列表
└── papers/
    ├── Smith_2024_transformer.pdf        # 下载的 PDF 文件
    ├── Zhang_2023_attention.pdf
    └── ...
```

### 综述报告包含

1. **研究背景与概述** - 领域现状和主要挑战
2. **核心文献分析** - 基础理论、最新进展、方法对比
3. **研究趋势与热点** - 当前研究方向
4. **关键文献列表** - 按重要性排序的论文清单
5. **研究空白与未来方向** - 未来研究机会
6. **引用信息** - 完整的 BibTeX 引用

## 使用场景

### 场景 1：开始新研究项目
```
研究主题: "Graph neural networks for drug discovery"
目的: 了解领域现状，识别关键文献
```

### 场景 2：撰写文献综述章节
```
研究主题: "Federated learning privacy preservation"
目的: 为论文撰写系统的文献综述
```

### 场景 3：追踪最新进展
```
研究主题: "Large language models optimization"
年份范围: "2023-2024"
目的: 了解最新研究动态
```

## 技能优势

✅ **全自动化**: 从检索到综述生成一键完成
✅ **智能筛选**: 自动评估论文质量和相关性
✅ **结构化输出**: 生成格式规范的综述报告
✅ **引用管理**: 自动生成 BibTeX 引用文件
✅ **开放获取**: 自动下载可用的 PDF 文献

## 注意事项

- 📖 PDF 下载仅限于开放获取来源（如 arXiv）
- 🔒 付费论文需要通过机构订阅或作者联系获取
- ⏱️ 大规模文献综述可能需要较长时间
- 🌐 需要网络连接以访问 PaperFinder 和文献数据库

## 技术规格

- **版本**: 1.0.0
- **类型**: Agent 型技能
- **难度**: 中级
- **最低要求**: Claude Code 1.0.0+
- **支持平台**: macOS, Linux, Windows

## 安装到 Skills Hub

如果您正在使用 Skills Hub 管理技能：

1. 将 `paper-finder-research` 文件夹放入您的技能目录
2. 在 Skills Hub 中导入该技能
3. 选择要同步到的 AI 编码工具
4. 开始使用！

或者通过 Git URL 导入：
```
# 如果将技能推送到 Git 仓库
在 Skills Hub 中选择 "Add Skill" > "Git Repository"
输入仓库 URL
```

## 许可证

MIT License - 自由使用和修改

## 作者

Research Assistant

## 反馈与改进

欢迎提出建议和改进意见！