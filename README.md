# SmartBank Agent：基于MCP+Skill+BMAD三位一体的金融科技实验教学智能体

> 四川农业大学经济学院 · 数字经济系 | 2026 春季学期

---

## 项目简介

本项目是面向金融学专业本科生的 **AI 工具实践教学生态系统**，包含教材、在线课程网站、AI 智能体、技能库四大核心模块。采用"低代码、高集成"技术路线——学生不需要从零编写 AI 程序，而是通过配置 IDE、接入 MCP 协议、编写 Skill 的方式，像搭积木一样组装出面向金融业务的智能系统。

全书共 **8 章 253 页**，分为基础模块、进阶模块和综合模块三个层次，支持 16/32/48/64 学时四种教学方案灵活组合。

## 🌐 课程在线网站

> **https://smartbanking.pages.dev**
>
> 含交互式文档、公式渲染、AI 智能体实时问答、金融数据查询

### 备用访问地址

| 平台 | 地址 | 说明 |
|------|------|------|
| Cloudflare Pages（主站） | https://smartbanking.pages.dev | 全球 CDN，推荐访问 |
| 阿里云 SWAS（备份站） | http://8.137.175.215 | 国内服务器，API 后端独立部署 |
| CNB 仓库 | https://cnb.cool/xiaosicau/smartbanking | 源码托管（公开仓库） |
| GitHub 仓库 | https://github.com/shawsicau-create/smartbanking | 镜像备份 |

- 网站由 **Astro + Starlight** 构建，部署在 **Cloudflare Pages**（全球 CDN + Serverless Functions）
- 源码托管在 [CNB（xiaosicau/smartbanking）](https://cnb.cool/xiaosicau/smartbanking)（公开仓库）
- 智能体后端由 Cloudflare Workers 驱动，接入 MiMo LLM + Tushare + World Bank 数据源

## 🤖 SmartBank Agent

课程网站内置的金融实验教学智能体，具备以下能力：

| 功能 | 说明 |
|------|------|
| 实时数据查询 | 通过 Tushare 查询 A 股行情、指数、宏观经济数据 |
| 全球金融对比 | 通过 World Bank API 获取跨国金融包容性指标 |
| 专业知识问答 | 基于教材内容的金融概念解释与案例分析 |
| BMAD 项目指导 | 引导学生完成 CRM 系统 12 个递进式实验 |

## 📘 教程 PDF

最新编译版本位于 `智慧银行实验教程chapters/智慧银行实验教程.pdf`（**253 页**）。

```bash
cd 智慧银行实验教程chapters/
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
biber "智慧银行实验教程"
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
```

## 文件结构

```
smartbanking/
├── 智慧银行实验教程chapters/             # 教程主体（LaTeX 源文件，可直接编译）
│   ├── 智慧银行实验教程.tex              # LaTeX 主文件
│   ├── 智慧银行实验教程.pdf              # 编译输出 PDF（253页）
│   ├── preface.tex                       # 前言（含教学路线图与能力矩阵）
│   ├── ch01.tex ~ ch12.tex              # 第1-8章 LaTeX 源文件
│   ├── appendix.tex                      # 附录 A–I
│   ├── references.bib                    # 参考文献
│   └── MCP服务配置参考手册.md            # MCP 配置独立参考文档
├── 实验讲义/                              # 配套实验讲义与操作指南
│   ├── BMAD-CRM系统开发实验手册.md        # 银行CRM系统12个完整实验
│   ├── 实验详细步骤 BMAD方法论实战.txt    # BMAD安装到开发全流程
│   ├── 实验详细步骤 BMAD代码云端部署.txt  # Cloudflare 部署实操
│   ├── 实验详细步骤 使用cnm同步项目库.txt # 环境准备与CNB同步指南
│   ├── 本地大模型部署指南.md              # 本地 LLM 部署参考
│   └── mcp.json                          # MCP 服务配置文件
├── webversion/                            # 在线网站源码（Astro + Starlight）
│   ├── src/                              # 内容源文件（MDX）与组件
│   ├── public/                           # 静态资源 + _worker.js（智能体后端）
│   ├── astro.config.mjs                  # Astro 配置（含 Starlight 侧边栏）
│   ├── package.json
│   └── dist/                             # 构建输出（用于 Cloudflare 部署）
├── .agents/skills/                       # Qoder AI 技能配置（课程内置）
│   ├── finance-expert/                   # 金融专家技能
│   ├── finance-news/                     # 金融新闻技能
│   ├── mermaid-diagrams/                 # Mermaid 图表技能
│   ├── openbb-finance/                   # OpenBB 金融数据技能
│   └── ...                               # 更多技能
├── qoder-skills-library/                 # 技能库（20 分类，学术写作全流程）
│   ├── 01-ideation/ ~ 20-messaging/     # 从选题到消息的完整技能矩阵
│   └── README.md
├── smart-banking-tutorial/               # 教材蒸馏产物：13 个可执行 AI Skill
│   ├── INDEX.md                          # 13 个 Skill 导航索引（学习路径 + 场景）
│   ├── GLOSSARY.md                       # 核心术语表
│   ├── DIGEST.md                         # 蒸馏总览与阅读建议
│   ├── BOOK_OVERVIEW.md / verified.md   # 原书概览与三重验证记录
│   ├── test-prompts.json                 # 52 个压力测试用例
│   ├── meta-*/                           # 元方法类 Skill（5 个）
│   ├── flow-*/                           # 流程类 Skill（3 个）
│   └── framework-*/ decision-*/         # 决策与批判类 Skill（5 个）
├── .env.example                          # 环境变量模板
├── wrangler.toml                         # Cloudflare Workers 配置
└── README.md
```

## 教程章节概览

| 模块               | 章节  | 主题                                                  |
| ------------------ | ----- | ----------------------------------------------------- |
| **基础模块** | 第1章 | 绪论：AI 驱动的银行数字化转型                          |
|                    | 第2章 | 开发环境搭建与 AI 协作基础                             |
|                    | 第3章 | MCP 协议：让 AI 连接金融世界                          |
|                    | 第4章 | Skill 体系：赋予 AI 金融专业能力                      |
|                    | 第5章 | CLI 工具实战——AI 辅助开发的命令行利器               |
| **进阶模块** | 第6章 | 金融数据分析与计量经济学                              |
| **综合模块** | 第7章 | BMAD 方法论与综合项目实践（含银行 CRM 系统 12 个完整实验） |
|                    | 第8章 | 课程综合项目与创新实践                                |

### 第7章特色：银行 CRM 系统完整开发实验

第7章以商业银行 CRM 系统为案例，通过 **12 个递进式实验** 完整演示 BMAD 从需求到部署的全流程：

| 实验序号 | 实验名称                  | BMAD 阶段  |
| :------: | ------------------------- | ---------- |
|    1     | 安装 BMAD 框架            | 环境准备   |
|    2     | 创建产品需求文档（PRD）   | 需求分析   |
|    3     | 创建技术架构设计          | 架构设计   |
|    4     | 创建 UX 设计              | 交互设计   |
|    5     | 创建 Epics 和 Stories     | 需求拆解   |
|    6     | Sprint 规划               | 迭代规划   |
|    7     | Sprint 1——客户管理实现  | 代码实现   |
|    8     | Sprint 2-3——迭代开发     | 迭代开发   |
|    9     | 数据库适配与降级方案      | 工程实践   |
|    10    | 功能测试验证              | 质量保证   |
|    11    | 版本控制与 CNB 推送       | 版本管理   |
|    12    | **Cloudflare Pages 部署**（前端） | 生产部署   |

## 技术栈

| 类别        | 技术                                                                |
| ----------- | ------------------------------------------------------------------- |
| 文档排版    | LaTeX（XeLaTeX + ctexbook）                                          |
| 教学网站    | Astro 6 + Starlight（Markdown 内容站 + Pagefind 全文搜索）          |
| AI 智能体   | Cloudflare Workers + MiMo LLM（OpenAI 兼容格式）                   |
| 金融数据源  | Tushare Pro（A 股）+ World Bank API（全球宏观）+ OECD              |
| AI 教学工具 | Qoder / Trae CN / Cursor 等 AI IDE                                   |
| 工具协议    | MCP（Model Context Protocol）                                       |
| AI 技能     | Skill 体系（8 组专业技能 + 20 分类技能库 + 13 个教材蒸馏 Skill）    |
| 项目方法论  | BMAD（Breakthrough Method of Agile AI-Driven Development）          |
| 数据分析    | Stata / Python（pandas, statsmodels）                               |
| 部署平台    | **Cloudflare Pages**（全球 CDN + Serverless Functions）+ **阿里云 SWAS**（国内备份站） |
| 版本控制    | Git + [CNB 云开发平台](https://cnb.cool/xiaosicau/smartbanking)     |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://cnb.cool/xiaosicau/smartbanking.git
cd smartbanking
```

### 2. 编译 PDF 教程

```bash
cd 智慧银行实验教程chapters/
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
biber "智慧银行实验教程"
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
```

### 3. 构建并本地预览在线网站

```bash
cd webversion/
pnpm install
pnpm build           # 产物输出到 dist/
pnpm preview         # 本地预览 http://localhost:4321
```

### 4. 部署到 Cloudflare Pages

```bash
# 前置条件：npm install -g wrangler && wrangler login
cd webversion/ && pnpm build
wrangler pages deploy dist --project-name=smartbanking
```

### 5. 环境准备

详细开发环境搭建步骤参见教程**附录 D**（环境准备与 CNB 项目同步详细步骤），主要包括：

1. 安装 Qoder / Trae CN 等 AI IDE
2. 安装 Python 3.12、Node.js LTS、Git 等基础运行时
3. 安装 CNB CLI 与 Skills 技能管理工具
4. 克隆课程仓库并同步到个人 CNB 空间

## 教学方案

本教程支持四种学时方案灵活组合：

| 方案   | 学时 | 覆盖章节                | 适用场景                  |
| ------ | :--: | ----------------------- | ------------------------- |
| 入门版 |  16  | 第 1-2、4-5、7 章       | 短期培训、导论课程        |
| 精简版 |  32  | 第 1-5、7 章            | 金融科技概论实验环节      |
| 标准版 |  48  | 第 1-8 章全部           | 独立金融科技实验课程      |
| 完整版 |  64  | 第 1-8 章+附录深度实操  | 金融科技专业核心课程      |

## 教学特色

- **双线并行**：全书贯穿 AI 工具线（IDE → MCP → Skill → BMAD）和金融业务线（零售银行 → 公司银行 → 风控 → 数据分析）
- **三层递进**：基础模块（认知）→ 进阶模块（应用）→ 综合模块（创造）
- **理论实操并重**：每章包含理论讲解 + 分步操作指引，确保"学了就能用"

## 课程信息

- **教程版本**: v6.0（2026 年春季，8 章重构版）
- **PDF 页数**: 253 页
- **所属院系**: 四川农业大学经济学院 · 数字经济系
- **CNB 仓库**: https://cnb.cool/xiaosicau/smartbanking
- **GitHub 仓库**: https://github.com/shawsicau-create/smartbanking
- **在线网站**: https://smartbanking.pages.dev
- **备用站点**: http://8.137.175.215（阿里云 SWAS）

## 教材蒸馏 Skill 库（smart-banking-tutorial/）

运用 RIA++ 方法论将《智慧银行实验教程》全书提炼为 **13 个可执行 AI Skill**，覆盖"AI+金融"的底层架构、执行流程与决策框架，均通过三重验证（跨域引用 / 预测力 / 独创性）。

| 类别 | 数量 | 代表 Skill |
|------|:----:|-----------|
| 元方法类（Meta） | 5 | MCP+Skill+BMAD 三位一体、BMAD 五阶段、AI 协作四模式、RTEII 提示词五原则、MCP 三层架构 |
| 流程类（Flow） | 3 | AI 协作闭环、金融实证 6 节点流水线、Skill 化提示词改写 |
| 决策与批判类 | 5 | 金融科技四阶段、AI 素养四维度、选题 F-N-F-T 四原则、金融 AI 应用矩阵、知识工程三范式 |

配套 `INDEX.md`（导航与场景推荐）、`GLOSSARY.md`（术语表）、`DIGEST.md`（阅读建议）、`test-prompts.json`（52 个压力测试用例）。详见 [smart-banking-tutorial/INDEX.md](smart-banking-tutorial/INDEX.md)。

## 相关文档

- [MCP 服务配置参考手册](智慧银行实验教程chapters/MCP服务配置参考手册.md)
- [BMAD-CRM 系统开发实验手册](实验讲义%20/BMAD-CRM系统开发实验手册.md)
- [本地大模型部署指南](实验讲义%20/本地大模型部署指南.md)
- [Cloudflare 部署指南](docs/cloudflare-pages-deploy.md)
- [教材蒸馏 Skill 库导航](smart-banking-tutorial/INDEX.md)

## 许可证

本项目仅供教学使用。
