# 智慧银行实验教程——AI驱动的金融科技实践

> 四川农业大学经济学院 · 数字经济系 | 2026 春季学期

---

## 项目简介

《智慧银行实验教程——AI驱动的金融科技实践》教学资料仓库。本教程以 AI 编程工具（Qoder 等）为核心实验平台，系统讲授 **MCP + Skill + CLI** 技术栈在银行业务场景中的应用，通过 **BMAD 方法论** 驱动从需求到部署的全流程项目实践。

全书共 **8 章**，分为基础模块、进阶模块和综合模块三个层次，支持 16/32/48/64 学时四种教学方案灵活组合。

## 🌐 课程在线网站

> **在线阅读（含交互式目录、公式渲染、表格、实验手册）：**
> [https://smartbanking-wmacgcua.edgeone.run](https://smartbanking-wmacgcua.edgeone.run)

- 网站由 **Astro + Starlight** 构建
- 源码托管在 [CNB（xiaosicau/smartbanking）](https://cnb.cool/xiaosicau/smartbanking)
- 通过 `.cnb.yml` 云原生流水线自动部署到 **EdgeOne Pages**
- 每次 `git push` 后约 1-2 分钟自动更新

> 🌐 **GitHub Pages 镜像**：[https://shawsicau-create.github.io/smartbanking/](https://shawsicau-create.github.io/smartbanking/)（海外访问，GitHub Actions 自动部署）

> ⚠️ **中国大陆用户访问提示**：本项目部署在 EdgeOne Pages 的 Global 区域。如在中国大陆网络下访问出现 401 UNAUTHORIZED，请到 [EdgeOne 控制台](https://console.cloud.tencent.com/edgeone/pages) 项目设置中启用"中国大陆加速"，然后重新部署。

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
│   ├── 实验详细步骤 BMAD方法论实战.txt    # BMAD安装到开发全流程
│   ├── 实验详细步骤 BMAD代码云端部署.txt  # EdgeOne 部署实操
│   ├── 实验详细步骤 CNB流水线自动部署到EdgeOne.md
│   ├── 实验详细步骤 使用cnm同步项目库.txt # 环境准备与CNB同步指南
│   ├── 本地大模型部署指南.md              # 本地 LLM 部署参考
│   └── mcp.json                          # MCP 服务配置文件
├── webversion/                            # 在线网站源码（Astro + Starlight）
│   ├── src/content/docs/                 # Markdown 内容源
│   ├── astro.config.mjs                  # Astro 配置（含 Starlight 侧边栏）
│   ├── package.json
│   └── dist/                             # 构建输出（用于 EdgeOne 部署）
├── .agents/skills/                       # Qoder AI 技能配置
│   ├── consulting-frameworks/            # 咨询框架技能
│   ├── docx/                             # Word 文档处理技能
│   ├── finance-expert/                   # 金融专家技能
│   ├── finance-news/                     # 金融新闻技能
│   ├── humanizer-zh/                     # 中文人文化写作技能
│   ├── mermaid-diagrams/                 # Mermaid 图表技能
│   ├── openbb-finance/                   # OpenBB 金融数据技能
│   └── xlsx/                             # Excel 处理技能
├── qoder-skills-library/                 # 技能库（学术写作全流程）
├── .cnb.yml                              # CNB 云原生流水线配置
├── .env.example                          # 环境变量模板
├── .gitignore
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
|    12    | **EdgeOne Pages 部署**（前端） | 生产部署   |

## 附录目录

| 附录   | 主题                          |
| ------ | ----------------------------- |
| 附录 A | 完整环境配置手册              |
| 附录 B | MCP 配置大全与故障排除         |
| 附录 C | Stata 安装与联动配置           |
| 附录 D | 环境准备与 CNB 项目同步详细步骤 |
| 附录 E | CNB 与 GitHub 命令速查        |
| 附录 F | 金融数据源汇总                |
| 附录 G | LaTeX 论文排版模板            |
| 附录 H | 评分标准与交付规范            |
| 附录 I | 术语表                        |

## 技术栈

| 类别        | 技术                                                                |
| ----------- | ------------------------------------------------------------------- |
| 文档排版    | LaTeX（XeLaTeX + ctexbook）                                          |
| 教学网站    | Astro 6 + Starlight（Markdown 内容站 + Pagefind 全文搜索）          |
| AI 教学工具 | Qoder / Trae CN / Cursor 等 AI IDE                                   |
| 工具协议    | MCP（Model Context Protocol）                                       |
| AI 技能     | Skill 体系（8 组专业技能）                                          |
| CLI 工具    | CNB CLI / Skills CLI / Claude Code / Codex / EdgeOne CLI           |
| 项目方法论  | BMAD（Breakthrough Method of Agile AI-Driven Development）          |
| 数据分析    | Stata / Python（pandas, statsmodels）                               |
| 全栈开发    | React + Vite + Express + JWT                                        |
| 部署平台    | **EdgeOne Pages**（腾讯云全球 CDN）+ CNB 云开发平台               |
| 版本控制    | Git + [CNB 云开发平台](https://cnb.cool/xiaosicau/smartbanking)     |

## 快速开始

### 1. 克隆仓库

```bash
git clone https://cnb.cool/xiaosicau/smartbanking.git smartbanking-work
cd smartbanking-work
```

### 2. 编译 PDF 教程

```bash
cd 智慧银行实验教程chapters/
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
biber "智慧银行实验教程"
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
```

编译完成后生成 `智慧银行实验教程.pdf`（253 页）。

### 3. 构建并本地预览在线网站

```bash
cd webversion/
pnpm install
pnpm build           # 产物输出到 dist/
pnpm preview         # 本地预览 http://localhost:4321
```

### 4. 部署在线网站到 EdgeOne Pages

#### 前置条件

- 全局安装 EdgeOne CLI：`npm install -g edgeone`
- 获取 API Token：访问 [https://pages.edgeone.ai/document/api-token](https://pages.edgeone.ai/document/api-token)
- 在项目根目录创建 `.env` 文件（已加入 `.gitignore`）：
  ```bash
  EDGEONE_PAGES_API_TOKEN=your_token_here
  ```

#### 一键部署

```bash
cd webversion/
source ../.env
npx edgeone makers deploy ./dist -n smartbanking -t $EDGEONE_PAGES_API_TOKEN
```

部署成功后会返回形如 `https://smartbanking-wmacgcua.edgeone.run` 的访问链接。

> ⚠️ **中国大陆访问**：默认部署到 Global（MLC excluded）区域，国内访问会被拦截。需在 [EdgeOne 控制台](https://console.cloud.tencent.com/edgeone/pages) 启用"中国大陆加速"。

### 5. 自动部署（CI/CD）

推送代码即自动部署。`.cnb.yml` 已配置完整流水线：

```yaml
main:
  push:
    - name: deploy-webversion-to-edgeone
      docker:
        image: node:22
      imports:
        - https://cnb.cool/xiaosicau/secrets/-/blob/main/edgeone.yml
      stages:
        - 安装 pnpm
        - 安装依赖（pnpm install）
        - 构建网站（pnpm build）
        - 部署到 EdgeOne Pages
```

密钥仓库 `xiaosicau/secrets` 需包含 `edgeone.yml`：

```yaml
EDGEONE_PAGES_API_TOKEN: "your_token_here"
```

### 6. 环境准备

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

### 4. 推送并创建 PR

```bash
git push origin feature/新功能名称
```

前往 [CNB 仓库](https://cnb.cool/xiaosicau/smartbanking) 创建 Pull Request。

### 提交信息规范

使用语义化提交信息：

- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `refactor:` 代码重构
- `chore:` 构建/工具相关
- `style:` 格式调整

## 课程信息

- **教程版本**: v6.0（2026 年春季，8 章重构版）
- **PDF 页数**: 253 页
- **所属院系**: 四川农业大学经济学院 · 数字经济系
- **CNB 仓库**: https://cnb.cool/xiaosicau/smartbanking
- **GitHub 仓库**: https://github.com/shawsicau-create/smartbanking
- **在线网站**: https://smartbanking-wmacgcua.edgeone.run
- **GitHub Pages**: https://shawsicau-create.github.io/smartbanking/

## 相关文档

- [MCP 服务配置参考手册](智慧银行实验教程chapters/MCP服务配置参考手册.md) - MCP 服务配置
- [BMAD-CRM 系统开发实验手册](实验讲义%20/BMAD-CRM系统开发实验手册.md) - 银行 CRM 完整开发指南
- [本地大模型部署指南](实验讲义%20/本地大模型部署指南.md) - 离线 AI 模型部署
- [EdgeOne 流水线部署指南](实验讲义%20/实验详细步骤%20CNB流水线自动部署到EdgeOne.md) - 自动部署实战

## 许可证

本项目仅供教学使用。