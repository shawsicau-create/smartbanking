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

## 自动化构建（CI/CD）

本项目配置了 GitHub Actions 自动化构建流程，每次提交代码时会自动编译PDF文件。

### 自动构建触发条件

- **Push 到 main/master 分支**：修改 `智慧银行实验教程chapters/` 目录下的文件时自动触发
- **Pull Request**：提交PR时自动构建并检查
- **手动触发**：在 GitHub Actions 页面手动运行

### 构建产物

- **PDF文件**：自动编译的 `智慧银行实验教程.pdf`
- **构建日志**：详细的编译过程记录
- **发布版本**：推送标签时自动创建 GitHub Release

### 创建发布版本

```bash
# 1. 更新版本号（在README.md中）
# 2. 提交更改
git add .
git commit -m "release: v5.1 新增第14章内容"

# 3. 创建标签
git tag v5.1

# 4. 推送标签
git push origin v5.1
```

系统会自动编译PDF并创建 GitHub Release。

## 本地构建工具（Makefile）

项目提供了 Makefile 简化本地编译流程：

### 常用命令

```bash
# 编译PDF
make pdf

# 清理编译文件
make clean

# 编译并打开PDF
make view

# 检查LaTeX语法
make check

# 统计字数
make wordcount

# 显示帮助
make help
```

### Makefile 优势

- **简化命令**：无需记忆复杂的xelatex编译流程
- **自动化处理**：自动处理多遍编译和参考文献
- **错误处理**：编译失败时提供清晰的错误信息
- **跨平台**：支持macOS、Linux、Windows（WSL）

## CI/CD 测试

项目提供了本地测试脚本，用于验证CI/CD配置：

```bash
# 运行CI/CD测试
./test-cicd.sh
```

测试脚本会：
1. 检查必要工具（xelatex、biber、make）
2. 清理旧的编译文件
3. 检查LaTeX语法
4. 编译PDF文件
5. 验证生成的PDF文件

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

### 1. Fork 项目

```bash
# 克隆你的Fork
git clone https://github.com/your-username/smartbanking-work.git
cd smartbanking-work
```

### 2. 创建分支

```bash
# 创建并切换到新分支
git checkout -b feature/新功能名称
```

### 3. 提交更改

```bash
# 添加更改
git add .

# 提交更改（使用语义化提交信息）
git commit -m "feat: 添加新功能描述"
```

### 4. 推送并创建PR

```bash
# 推送到你的Fork
git push origin feature/新功能名称

# 在GitHub上创建Pull Request
```

### 提交信息规范

使用语义化提交信息：
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工具相关

## 课程信息

- **教程版本**: v5.0（2026年春季）
- **所属院系**: 四川农业大学经济学院 · 数字经济系
- **CNB 仓库**: https://cnb.cool/xiaosicau/smartbanking

## 相关文档

- [CI/CD 配置说明](CI-CD-README.md) - 详细的自动化构建配置
- [本地大模型部署指南](本地大模型部署指南.md) - 离线AI模型部署
- [MCP服务配置参考手册](智慧银行实验教程chapters/MCP服务配置参考手册.md) - MCP服务配置

## 许可证

本项目仅供教学使用。
