# 智慧银行实验教程

四川农业大学经济学院 · 数字经济系 | 2026 春季学期

## 项目简介

《智慧银行实验教程——AI驱动的金融科技实践》教学资料仓库。本教程以 AI 编程工具（Qoder 等）为核心实验平台，系统讲授 AI IDE + MCP + Skill 技术栈在银行业务场景中的应用，涵盖智能客服、风控建模、数据分析、全栈开发等实践内容。

## 文件结构

```
smartbanking/
├── 智慧银行实验教程chapters/          # 教程主体（自包含目录，可直接编译）
│   ├── 智慧银行实验教程.tex            # LaTeX 主文件
│   ├── 智慧银行实验教程.pdf            # 编译输出 PDF（379页）
│   ├── preface.tex                    # 前言
│   ├── ch01.tex – ch13.tex            # 第1–13章
│   ├── appendix.tex                   # 附录 A–I
│   ├── references.bib                 # 参考文献
│   └── MCP服务配置参考手册.md          # MCP 配置独立参考文档
├── 实验讲义/                           # 实验讲义（v4.0）
│   ├── 智慧银行实验讲义_v4.0.tex
│   ├── 智慧银行实验讲义_v4.0.pdf
│   └── 实验详细步骤 使用cnm同步项目库.txt  # 环境准备与CNB同步操作指南
├── papers_digital_finance/             # 数字金融研究文献集（9篇）
├── .agents/skills/                     # Qoder AI 技能配置
│   ├── consulting-frameworks/         # 咨询框架技能
│   ├── docx/                          # Word文档处理技能
│   ├── finance-expert/                # 金融专家技能
│   ├── finance-news/                  # 金融新闻技能
│   ├── humanizer-zh/                  # 中文人文化写作技能
│   ├── mermaid-diagrams/              # Mermaid图表技能
│   └── xlsx/                          # Excel处理技能
├── mcp.json                            # MCP 服务配置文件
├── mino                                # Mino 配置
├── 本地大模型部署指南.md               # 本地 LLM 部署参考
└── .gitignore
```

## 教程章节概览

| 模块 | 章节 | 主题 |
|------|------|------|
| **基础模块** | 第1章 | 绪论：AI驱动的银行数字化转型 |
| | 第2章 | 开发环境搭建与AI协作基础 |
| | 第3章 | MCP协议：让AI连接金融世界 |
| | 第4章 | Skill体系：赋予AI金融专业能力 |
| **进阶模块** | 第5章 | 银行零售业务智能化 |
| | 第6章 | 银行公司业务与风控建模 |
| | 第7章 | 金融数据分析与计量经济学 |
| | 第8章 | 金融舆情分析与智能投研 |
| **综合模块** | 第9章 | BMAD方法论与AI驱动开发 |
| | 第10章 | 银行CRM系统全栈开发 |
| | 第11章 | 银行智能客服系统开发 |
| | 第12章 | 课程综合项目与创新实践 |
| **实战模块** | 第13章 | CLI工具实战——AI辅助开发的命令行利器 |

## 附录目录

| 附录 | 主题 |
|------|------|
| 附录 A | 完整环境配置手册 |
| 附录 B | MCP配置大全与故障排除 |
| 附录 C | Stata安装与联动配置 |
| 附录 D | 环境准备与CNB项目同步详细步骤 |
| 附录 E | CNB与GitHub命令速查 |
| 附录 F | 金融数据源汇总 |
| 附录 G | LaTeX论文排版模板 |
| 附录 H | 评分标准与交付规范 |
| 附录 I | 术语表 |

## 技术栈

| 类别 | 技术 |
|------|------|
| 文档排版 | LaTeX（XeLaTeX + ctexbook） |
| AI 教学工具 | Qoder / Trae CN / Cursor 等 AI IDE |
| 工具协议 | MCP（Model Context Protocol）8组服务 |
| 数据分析 | Stata / Python（pandas, statsmodels） |
| 版本控制 | Git + [CNB 云开发平台](https://cnb.cool/xiaosicau/smartbanking) |

## 快速开始

### 克隆仓库

```bash
git clone https://cnb.cool/xiaosicau/smartbanking.git smartbanking-work
cd smartbanking-work
```

### 编译教程

在 `智慧银行实验教程chapters/` 目录下执行：

```bash
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
biber "智慧银行实验教程"
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
```

### 环境准备

详细的开发环境搭建步骤参见**附录 D**（环境准备与CNB项目同步详细步骤），主要包括：

1. 安装 Trae CN / Qoder 等 AI IDE
2. 安装 Python 3.12、Node.js LTS、Git 等基础运行时
3. 安装 CNB CLI 与 Skills 技能管理工具
4. 克隆课程仓库并同步到个人 CNB 空间

## 课程信息

- **教程版本**: v5.0（2026年春季）
- **所属院系**: 四川农业大学经济学院 · 数字经济系
- **CNB 仓库**: https://cnb.cool/xiaosicau/smartbanking

## 许可证

本项目仅供教学使用。
