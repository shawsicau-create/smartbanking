# 智慧银行实验教程——AI驱动的金融科技实践

四川农业大学经济学院 · 数字经济系 | 2026 春季学期

## 项目简介

《智慧银行实验教程——AI驱动的金融科技实践》教学资料仓库。本教程以 AI 编程工具（Qoder 等）为核心实验平台，系统讲授 **MCP + Skill + CLI** 技术栈在银行业务场景中的应用，通过 **BMAD 方法论** 驱动从需求到部署的全流程项目实践。

全书共 **8 章**，分为基础模块、进阶模块和综合模块三个层次，支持 16/32/48/64 学时四种教学方案灵活组合。

## 🌐 课程在线网站

> **在线阅读（含交互式目录、公式渲染、表格、实验手册）：** [https://smartbanking.edgeone.app](https://smartbanking.edgeone.app)

网站由 Astro + Starlight 构建，源码托管在 [CNB（xiaosicau/smartbanking）](https://cnb.cool/xiaosicau/smartbanking)，通过云原生流水线（`.cnb.yml`）自动部署到 EdgeOne Pages，每次 `git push` 后约 1-2 分钟自动更新。

## 文件结构

```
smartbanking/
├── 智慧银行实验教程chapters/             # 教程主体（自包含目录，可直接编译）
│   ├── 智慧银行实验教程.tex              # LaTeX 主文件
│   ├── 智慧银行实验教程.pdf              # 编译输出 PDF（253页）
│   ├── preface.tex                       # 前言（含教学路线图与能力矩阵）
│   ├── ch01.tex                          # 第1章 绪论
│   ├── ch02.tex                          # 第2章 环境搭建
│   ├── ch03.tex                          # 第3章 MCP协议
│   ├── ch04.tex                          # 第4章 Skill体系
│   ├── ch13.tex                          # 第5章 CLI工具实战
│   ├── ch07.tex                          # 第6章 金融数据分析与计量经济学
│   ├── ch06_comprehensive.tex            # 第7章 BMAD方法论与综合项目实践
│   ├── ch12.tex                          # 第8章 课程综合项目与创新实践
│   ├── appendix.tex                      # 附录 A–I
│   ├── references.bib                    # 参考文献
│   └── MCP服务配置参考手册.md            # MCP 配置独立参考文档
├── 实验讲义/                              # 配套实验讲义与操作指南
│   ├── BMAD-CRM系统开发实验手册.md        # 银行CRM系统12个完整实验
│   ├── 实验详细步骤 BMAD方法论实战.txt     # BMAD安装到开发全流程（651行）
│   ├── 实验详细步骤 BMAD代码云端部署.txt   # PinMe/EdgeOne部署实操（403行）
│   ├── 实验详细步骤 使用cnm同步项目库.txt   # 环境准备与CNB同步指南
│   ├── 本地大模型部署指南.md              # 本地 LLM 部署参考
│   └── mcp.json                          # MCP 服务配置文件
├── .agents/skills/                       # Qoder AI 技能配置
│   ├── consulting-frameworks/            # 咨询框架技能
│   ├── docx/                             # Word文档处理技能
│   ├── finance-expert/                   # 金融专家技能
│   ├── finance-news/                     # 金融新闻技能
│   ├── humanizer-zh/                     # 中文人文化写作技能
│   ├── mermaid-diagrams/                 # Mermaid图表技能
│   ├── openbb-finance/                   # OpenBB金融数据技能
│   └── xlsx/                             # Excel处理技能
├── qoder-skills-library/                 # 技能库（学术写作全流程）
└── .gitignore
```

## 教程章节概览

| 模块               | 章节  | 主题                                                  |
| ------------------ | ----- | ----------------------------------------------------- |
| **基础模块** | 第1章 | 绪论：AI驱动的银行数字化转型                          |
|                    | 第2章 | 开发环境搭建与AI协作基础                              |
|                    | 第3章 | MCP协议：让AI连接金融世界                             |
|                    | 第4章 | Skill体系：赋予AI金融专业能力                         |
|                    | 第5章 | CLI工具实战——AI辅助开发的命令行利器                 |
| **进阶模块** | 第6章 | 金融数据分析与计量经济学                              |
| **综合模块** | 第7章 | BMAD方法论与综合项目实践（含银行CRM系统12个完整实验） |
|                    | 第8章 | 课程综合项目与创新实践                                |

### 第7章特色：银行CRM系统完整开发实验

第7章以商业银行CRM系统为案例，通过 **12个递进式实验** 完整演示BMAD从需求到部署的全流程：

| 实验序号 | 实验名称                 | BMAD阶段 |
| :------: | ------------------------ | -------- |
|    1    | 安装BMAD框架             | 环境准备 |
|    2    | 创建产品需求文档（PRD）  | 需求分析 |
|    3    | 创建技术架构设计         | 架构设计 |
|    4    | 创建UX设计               | 交互设计 |
|    5    | 创建Epics和Stories       | 需求拆解 |
|    6    | Sprint规划               | 迭代规划 |
|    7    | Sprint 1——客户管理实现 | 代码实现 |
|    8    | Sprint 2-3——迭代开发   | 迭代开发 |
|    9    | 数据库适配与降级方案     | 工程实践 |
|    10    | 功能测试验证             | 质量保证 |
|    11    | 版本控制与CNB推送        | 版本管理 |
|    12    | EdgeOne Pages部署（前端） | 生产部署 |

## 附录目录

| 附录   | 主题                          |
| ------ | ----------------------------- |
| 附录 A | 完整环境配置手册              |
| 附录 B | MCP配置大全与故障排除         |
| 附录 C | Stata安装与联动配置           |
| 附录 D | 环境准备与CNB项目同步详细步骤 |
| 附录 E | CNB与GitHub命令速查           |
| 附录 F | 金融数据源汇总                |
| 附录 G | LaTeX论文排版模板             |
| 附录 H | 评分标准与交付规范            |
| 附录 I | 术语表                        |

## 技术栈

| 类别        | 技术                                                        |
| ----------- | ----------------------------------------------------------- |
| 文档排版    | LaTeX（XeLaTeX + ctexbook）                                 |
| AI 教学工具 | Qoder / Trae CN / Cursor 等 AI IDE                          |
| 工具协议    | MCP（Model Context Protocol）                               |
| AI 技能     | Skill 体系（8组专业技能）                                   |
| CLI 工具    | CNB CLI / Skills CLI / Claude Code / Codex                  |
| 项目方法论  | BMAD（Breakthrough Method of Agile AI-Driven Development）  |
| 数据分析    | Stata / Python（pandas, statsmodels）                       |
| 全栈开发    | React + Vite + Express + JWT                                |
| 部署平台    | EdgeOne Pages / CNB 云开发平台                                     |
| 版本控制    | Git + [CNB 云开发平台](https://cnb.cool/xiaosicau/smartbanking) |

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

编译完成后生成 `智慧银行实验教程.pdf`（253页）。

### 环境准备

详细的开发环境搭建步骤参见教程**附录 D**（环境准备与CNB项目同步详细步骤），主要包括：

1. 安装 Qoder / Trae CN 等 AI IDE
2. 安装 Python 3.12、Node.js LTS、Git 等基础运行时
3. 安装 CNB CLI 与 Skills 技能管理工具
4. 克隆课程仓库并同步到个人 CNB 空间

## 教学方案

本教程支持四种学时方案灵活组合：

| 方案   | 学时 | 覆盖章节             | 适用场景             |
| ------ | :--: | -------------------- | -------------------- |
| 入门版 |  16  | 第1-2、4-5、7章      | 短期培训、导论课程   |
| 精简版 |  32  | 第1-5、7章           | 金融科技概论实验环节 |
| 标准版 |  48  | 第1-8章全部          | 独立金融科技实验课程 |
| 完整版 |  64  | 第1-8章+附录深度实操 | 金融科技专业核心课程 |

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

### 1. Fork 项目

```bash
git clone https://cnb.cool/your-username/smartbanking.git
cd smartbanking
```

### 2. 创建分支

```bash
git checkout -b feature/新功能名称
```

### 3. 提交更改

```bash
git add .
git commit -m "feat: 添加新功能描述"
```

### 4. 推送并创建PR

```bash
git push origin feature/新功能名称
```

前往 [CNB 仓库](https://cnb.cool/xiaosicau/smartbanking) 创建 Pull Request。

### 提交信息规范

使用语义化提交信息：

- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `refactor:` 代码重构
- `chore:` 构建/工具相关

## 课程信息

- **教程版本**: v6.0（2026年春季，8章重构版）
- **PDF页数**: 253页
- **所属院系**: 四川农业大学经济学院 · 数字经济系
- **CNB 仓库**: https://cnb.cool/xiaosicau/smartbanking

## 相关文档

- [MCP服务配置参考手册](智慧银行实验教程chapters/MCP服务配置参考手册.md) - MCP服务配置
- [BMAD-CRM系统开发实验手册](实验讲义%20/BMAD-CRM系统开发实验手册.md) - 银行CRM完整开发指南
- [本地大模型部署指南](实验讲义%20/本地大模型部署指南.md) - 离线AI模型部署

## 许可证

本项目仅供教学使用。
