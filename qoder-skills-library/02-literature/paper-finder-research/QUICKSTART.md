# 快速开始指南

## 5 分钟快速上手

### 步骤 1：安装技能到 Skills Hub

#### 方法 A：通过 Skills Hub UI
1. 打开 Skills Hub 应用
2. 点击 "Add Skill" 按钮
3. 选择 "Local Folder" 标签
4. 浏览并选择 `paper-finder-research` 文件夹
5. 勾选要同步到的 AI 编码工具（如 Cursor、Claude Code、Qoder 等）
6. 点击 "Create" 完成安装

#### 方法 B：手动安装
将 `paper-finder-research` 文件夹复制到对应工具的技能目录：
- **Cursor**: `~/.cursor/skills/paper-finder-research`
- **Claude Code**: `~/.claude/skills/paper-finder-research`
- **Qoder**: `~/.qoder/skills/paper-finder-research`
- **其他工具**: 参考各工具的技能目录配置

---

### 步骤 2：第一次使用

打开您的 AI 编码助手（如 Cursor、Claude Code 等），输入：

```
使用 paper-finder-research 技能，研究主题是 "Transformer models in NLP"
```

或者更详细的调用：

```
使用 paper-finder-research 技能：
- 研究主题: "Deep learning for computer vision"
- 最大论文数: 20
- 年份范围: "2020-2024"
- 下载重要文献: true
```

---

### 步骤 3：查看输出

技能执行后，会在您的项目目录中生成：

```
project-root/
├── literature-review/
│   ├── review-[topic]-[date].md          # 📝 文献综述报告
│   ├── bibliography-[topic]-[date].bib   # 📚 BibTeX 引用
│   └── paper-list-[topic]-[date].json    # 📊 结构化数据
└── papers/
    ├── [Author]_[Year]_[keyword].pdf     # 📥 下载的论文
    └── ...
```

打开 `review-[topic]-[date].md` 即可查看完整的文献综述报告！

---

## 常见使用场景

### 🎓 场景 1：开始新研究项目
```
研究主题: "Federated learning privacy"
最大论文数: 25
```
**目的**: 快速了解领域现状和核心文献

### 📝 场景 2：撰写论文文献综述
```
研究主题: "Graph neural networks applications"
最大论文数: 30
年份范围: "2019-2024"
```
**目的**: 为论文 Related Work 章节收集材料

### 🔍 场景 3：追踪最新研究
```
研究主题: "Large language models optimization"
年份范围: "2023-2024"
最大论文数: 15
```
**目的**: 了解最新研究动态和趋势

---

## 核心功能一览

| 功能 | 说明 |
|------|------|
| 🔍 智能检索 | 使用 PaperFinder 进行语义搜索 |
| 📊 质量评估 | 基于引用数、期刊质量等多维度评估 |
| 📝 自动综述 | 生成结构化的文献综述报告 |
| 📥 PDF 下载 | 自动下载开放获取文献 |
| 📚 引用管理 | 生成 BibTeX 格式引用 |
| 🗂️ 智能分类 | 按基础、最新、方法等维度组织 |

---

## 参数快速参考

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| research_topic | string | **必需** | 研究主题或关键词 |
| max_papers | number | 20 | 要分析的最大论文数 |
| year_range | string | "2020-2024" | 年份范围 |
| download_important | boolean | true | 是否下载重要文献 |
| output_format | string | "markdown" | 输出格式（markdown/json）|

---

## 下一步

- 📖 查看 [完整使用示例](EXAMPLES.md) 了解更多场景
- 📘 阅读 [详细文档](README.md) 了解所有功能
- 🔧 根据需要调整参数进行个性化使用
- 💡 探索高级用法和最佳实践

---

## 需要帮助？

- 💬 查看 [常见问题](EXAMPLES.md#常见问题)
- 📧 提交问题反馈
- 🌟 给项目点星支持

---

**祝您研究顺利！开始您的第一次文献综述吧 🚀**