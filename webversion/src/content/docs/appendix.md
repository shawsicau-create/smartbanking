---
title: '附录'
description: '环境配置速查、MCP服务器清单、Skill模板库、Prompt工程指南'
---

**适用场景**：本附录提供从零搭建完整AI辅助开发环境的详细指南，涵盖LaTeX排版、Node.js、Python、Git、AI IDE（Qoder）、AI CLI工具、MCP服务器等全部内容。已在实验一中完成基本环境搭建的同学，可参考本附录进行进阶配置。

## LaTeX排版环境（详细版）

### MiKTeX（Windows）

MiKTeX是Windows上最推荐的LaTeX发行版，支持按需自动安装宏包。

1.  访问<https://miktex.org/download>，下载Basic MiKTeX Installer（约230 MB）

2.  运行安装程序，选择\"Install for current user\"（无需管理员权限）

3.  安装路径默认为`%LOCALAPPDATA%\Programs\MiKTeX\`

4.  打开MiKTeX Console → Settings →\"Install missing packages\"设为Always

5.  Updates →\"Check for updates\"更新一次

安装后自动获得的工具：

| **工具** | **版本** | **用途**                               |
|:---------|:---------|:---------------------------------------|
| xelatex  | 4.16     | 中文论文必备（支持Unicode + 系统字体） |
| pdflatex | 4.23     | 英文论文编译                           |
| biber    | 2.21     | 现代参考文献处理（配合biblatex）       |
| latexmk  | —        | 自动化多轮编译                         |

### MacTeX（macOS）

MacTeX是TeX Live的macOS封装版，包含**全部**宏包（约7 GB）。

```bash
# 方式一：Homebrew（推荐）
brew install --cask mactex

# 方式二：清华CTAN镜像（国内速度快）
curl -L -o /tmp/mactex.pkg \
  "https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/mac/mactex/mactex-20260324.pkg"
sudo installer -pkg /tmp/mactex.pkg -target /

# 方式三：官网下载 .pkg
# 访问 https://www.tug.org/mactex/ 下载安装
```

**PATH配置（如终端找不到xelatex）：**

```bash
echo 'export PATH="/usr/local/texlive/2026/bin/universal-darwin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### 系统中文字体

| **平台** | **字体**                   | **LaTeX调用名**              |
|:---------|:---------------------------|:-----------------------------|
| Windows  | 宋体/黑体/楷体/仿宋        | SimSun/SimHei/KaiTi/FangSong |
| macOS    | 华文宋体/华文黑体/华文楷体 | STSong/STHeiti/STKaiti       |

:::note[提示]
使用`ctexart`文档类时，ctex宏包会**自动检测**操作系统并选择对应的中文字体，无需手动指定。
:::

### 推荐的LaTeX编辑器

| **编辑器**               | **平台**      | **特点**                           |
|:-------------------------|:--------------|:-----------------------------------|
| Qoder                    | Win/Mac/Linux | AI辅助写作，MCP集成，本课程首选    |
| TeXstudio                | Win/Mac/Linux | 免费，功能全面，适合初学者         |
| VS Code + LaTeX Workshop | Win/Mac/Linux | 轻量，实时预览，Git集成            |
| Overleaf                 | 在线          | 无需安装，协作方便，国内访问需加速 |

## AI IDE------Qoder

Qoder是一款基于VS Code架构的AI智能体编程平台，内置多模型支持。

1.  访问<https://qoder.com/download>，下载对应系统版本

2.  Windows双击安装；macOS拖拽到Applications

3.  首次启动后登录Qoder账号

**Qoder核心功能：**

| **功能**   | **说明**                                     |
|:-----------|:---------------------------------------------|
| 智能补全   | 上下文感知的代码自动补全                     |
| Agent对话  | 右侧面板与AI对话，可读写文件、运行命令       |
| MCP集成    | 内置MCP工具管理器，连接数据库、API、Office等 |
| Skill系统  | 加载SKILL.md文件赋予AI领域知识               |
| 多模型切换 | 支持GPT-4o、Claude Sonnet、DeepSeek等        |

## AI CLI工具

| **工具**    | **厂商**  | **安装命令**                         | **核心模型**  |
|:------------|:----------|:-------------------------------------|:--------------|
| QoderCLI    | Qoder AI  | `npm i -g @qoder-ai/qodercli`        | 多模型切换    |
| Claude Code | Anthropic | `npm i -g @anthropic-ai/claude-code` | Claude Sonnet |
| Codex CLI   | OpenAI    | `npm i -g @openai/codex`             | GPT-4o        |

## CC Switch------多账号管理

CC Switch是AI CLI多账号/多服务商管理工具，提供可视化界面统一管理Claude Code、Codex、Gemini CLI等7款工具的配置。

```bash
# macOS
brew install --cask cc-switch

# Windows：从GitHub Releases下载 .msi 安装
# https://github.com/farion1231/cc-switch/releases
```

核心功能：50+预置服务商一键切换、系统托盘快切、统一MCP管理、用量追踪、云端同步。

## OpenCLI与OpenClaw

**OpenCLI**------把网站变成命令行：

```bash
npm install -g @jackwener/opencli
opencli --version
opencli setup   # 验证Chrome扩展连接
```

**OpenClaw**------AI Skill包管理：

```bash
npm install -g openclaw
openclaw --version
openclaw install academic-paper-analysis
openclaw install arxiv
```

## MCP/Skill/CLI三种范式对比

| **维度** | **MCP**        | **Skill**        | **CLI**    |
|:---------|:---------------|:-----------------|:-----------|
| 本质     | 连接协议       | 领域知识文件     | Shell命令  |
| 类比     | USB-C接口      | 操作手册         | 万能遥控器 |
| 开发成本 | 高（写Server） | 低（写Markdown） | 零         |
| 适合场景 | 企业SaaS       | 知识沉淀复用     | 本地自动化 |

:::note[提示]
CLI（执行层）+ Skill（知识层）+ MCP（连接层）= 完整AI工具链。日常以CLI + Skill为主，MCP在需要跨系统数据连接时介入。
:::

## 完整安装检查清单

```bash
# LaTeX
xelatex --version
biber --version

# 运行时
node --version
npm --version
python --version
git --version

# AI CLI
qoder --version
claude --version
codex --version
opencli --version
openclaw --version
cnb --version
```

:::note[提示]
完整版本的AI开发环境配置讲义（含OpenMAIC、DeepTutor、所有安装细节与故障排除）可参见独立文档：`AI开发环境配置讲义_中文版.pdf`。
:::

# MCP配置大全与故障排除

## MCP服务器配置详解

MCP（Model Context Protocol）让AI助手能够访问外部数据源和工具。Qoder的MCP配置文件位于：

```text
# Windows
%APPDATA%\Qoder\SharedClientCache\extension\local\mcp.json
```

```text
# macOS
~/Library/Application Support/Qoder/SharedClientCache/extension/local/mcp.json
```

### 推荐配置的MCP服务器

| **服务名** | **启动命令**                    | **用途**      |
|:-----------|:--------------------------------|:--------------|
| fetch      | `uvx mcp-server-fetch`          | HTTP网页抓取  |
| playwright | `npx @playwright/mcp@latest`    | 浏览器自动化  |
| excel      | `npx @negokaz/excel-mcp-server` | Excel读写     |
| ppt        | `uvx ppt_mcp_server`            | PPT编辑       |
| word       | `uvx word_mcp_server`           | Word文档      |
| stata-mcp  | `uvx stata-mcp`                 | Stata统计分析 |

### 完整mcp.json参考配置

```json
{
  "mcpServers": {
```
"fetch": {
"command": "uvx",
"args": ["mcp-server-fetch"]
},
"playwright": {
"command": "npx",
"args": ["@playwright/mcp@latest"]
},
"excel": {
"command": "npx",
"args": ["@negokaz/excel-mcp-server"]
},
"ppt": {
"command": "uvx",
"args": ["ppt_mcp_server"]
},
"word": {
"command": "uvx",
"args": ["word_mcp_server"]
},
"stata-mcp": {
"command": "uvx",
"args": ["stata-mcp"],
"env": {
"STATA_PATH": "C:<br/>Program Files<br/>Stata18<br/>StataMP-64.exe",
"MCP_STATA_LOGLEVEL": "INFO"
}
}
```
  }
}
```

### 各平台路径说明

| **平台** | **mcp.json路径** |
|:---|:---|
| Qoder (Windows) | `%APPDATA%\Qoder\SharedClientCache\extension\local\mcp.json` |
| Qoder (macOS) | `~/Library/Application Support/Qoder/SharedClientCache/extension/local/mcp.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |

:::note[提示]
- 修改mcp.json后必须**完全退出IDE**再重启（任务栏右键退出，不只是关窗口）

- JSON中Windows路径的反斜杠必须写成`<br/>`

- macOS路径中的空格需注意转义
:::

## 常见问题排查

### IDE安装/登录问题

| **现象**          | **原因**          | **解决**                          |
|:------------------|:------------------|:----------------------------------|
| 启动闪退          | 显卡驱动/VC++缺失 | 装NVIDIA/Intel驱动；装VC++ Redist |
| 登录转圈          | 防火墙/代理拦截   | 系统代理放行；或切手机热点        |
| Builder不能建文件 | 未授权            | 文件 → 信任当前工作区             |

### Python/Node环境问题

- **多版本Python冲突**：优先Anaconda；`where python`看路径，环境变量上移Anaconda

- **pip install SSL错误**：`pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple`

- **npm install慢**：`npm config set registry https://registry.npmmirror.com`

- **TensorFlow装不上**：业绩预测有SARIMA即可得分，LSTM可选

### MCP类问题

- **找不到npx/uvx**：Node.js与uv都得装，且加入PATH。`pip install uv`装uv

- **mcp.json改完没生效**：必须**完全退出IDE**再重启（任务栏右键退出，不只是关窗口）

- **playwright报EPERM**：不要装在`C:\Program Files\`下；改用户目录

- **stata-mcp找不到Stata**：在env.STATA_PATH填本机Stata实际路径

- **word/ppt MCP启动慢**：首次uvx需联网下载，等1--3分钟

### Skill类问题

- **AI不识别Skill**：①升级IDE；②使用skill finder重新安装；③检查description是否含明确触发词

- **自写Skill不激活**：description写得太宽泛，AI不知何时调用------把场景写具体（如\"当用户提到X或Y时使用\"）

# Stata安装与联动配置

**适用场景**：实验中\"数据分析组\"使用stata-mcp跑计量回归时需要本机已安装Stata。无Stata的同学可改用Python（statsmodels）替代，但**强烈建议安装**以获得完整体验。

## Stata软件介绍

Stata是一款强大的统计分析软件，广泛应用于经济学、金融学、社会学等领域的实证研究。本课程实验中使用Stata进行计量经济学分析和数据处理，配合stata-mcp可让AI直接调起Stata内核跑OLS/reghdfe/esttab等命令。

## 获取方式

Stata为商业软件，请通过官方渠道获取合法授权：

:::note[正版获取途径]
- **官方网站**：访问 <https://www.stata.com> 购买正版授权
- **学生优惠**：Stata提供学生版（Graduate Plan），价格大幅低于商业版，详见 <https://www.stata.com/order/new/edu/graduate-plans/>
- **机构订阅**：部分高校已购买站点授权，可咨询学校图书馆或院系实验室
- **试用版**：可在官网申请免费的短期试用许可证
:::

:::caution[版权提示]
Stata为商业软件，受版权法保护。请务必通过上述正规渠道获取授权版本，**切勿使用来源不明的安装包**，以免面临法律风险和安全隐患（捆绑恶意软件等）。
:::

:::tip[无法获取Stata？]
若暂时无法获取Stata授权，可使用 Python（statsmodels / linearmodels）完成全部课程实验，详见下方「替代方案」。
:::

## 安装步骤

### Step 1 下载与安装

1.  从 Stata 官网下载对应操作系统的安装程序

2.  运行安装程序，安装路径建议保持默认：`C:\Program Files\Stata18\`

3.  安装类型选择**StataMP**（多核版，性能最佳）或**StataSE**

4.  一路Next完成安装

### Step 2 激活授权

启动 Stata 后，输入购买时获得的序列号和授权码完成激活。详见官方安装指南：<https://www.stata.com/install-guide/>

### Step 3 验证安装

打开PowerShell执行：

```bash
& "C:\Program Files\Stata18\StataMP-64.exe" -h
```

或直接双击桌面Stata图标，命令窗口输入：

```stata
sysuse auto, clear
summarize
```

能看到74条汽车数据的描述统计 = 安装成功。

## 与stata-mcp联动配置

stata-mcp有两种方案，分别对应不同的配置方式：

### 方案一：SepineTam/mcp-for-stata（独立Server，本课程默认）

本课程mcp.json使用的是SepineTam方案，它是独立的MCP Server，**无需IDE扩展**，直接通过subprocess调用Stata CLI：

```json
"stata-mcp": {
  "command": "uvx",
  "args": ["stata-mcp"],
  "env": {
```
"STATA_PATH": "C:<br/>Program Files<br/>Stata18<br/>StataMP-64.exe",
"MCP_STATA_LOGLEVEL": "INFO"
```
  }
}
```

**环境检查**（验证配置是否正确）：

```bash
# 检查 stata-mcp 是否能找到 Stata
uvx stata-mcp doctor
```

正常输出示例：

```text
stata-mcp v1.17.0 -- Doctor Report
[PASS] os: macOS (Darwin 25.3.0, arm64)
[PASS] python: 3.13.5
[PASS] uv: uv 0.11.13
[PASS] stata_cli: /usr/local/bin/stata-mp
[PASS] stata_execution: OK (0.1s)
[PASS] guard: enabled, loaded 27 rules
Summary: 12 passed, 0 failed
```

:::note[提示]
如安装的是SE版本，把StataMP-64.exe改为StataSE-64.exe；如安装路径不同，整段绝对路径也要相应修改。**注意JSON中反斜杠必须写成<br/><br/>**。
:::

### 方案二：hanlulong/stata-mcp（IDE扩展方案）

如果使用Qoder/VS Code/Cursor等支持扩展的IDE，可以选择安装`DeepEcon.stata-mcp`扩展。此方案的架构如下：

```text
┌─────────────────┐        HTTP         ┌──────────────────────┐
│  IDE (客户端)    │ ──mcp-remote──────▶ │  Stata MCP Server    │
│  mcp.json 配置   │                     │  localhost:4000      │
└─────────────────┘                     │  (由IDE扩展提供)      │
└──────────────────────┘
```

**Step 1：安装DeepEcon.stata-mcp扩展**（**关键步骤，不可跳过**）

```bash
# VS Code
code --install-extension DeepEcon.stata-mcp

# Cursor
cursor --install-extension DeepEcon.stata-mcp

# Qoder / Antigravity
# 在扩展市场搜索 "Stata MCP" 安装
```

或在IDE中：扩展视图（Ctrl+Shift+X / Cmd+Shift+X）→搜索\"Stata MCP\"→安装。

:::caution[警告]
此方案**必须先安装扩展**！扩展启动后才会在localhost:4000监听，否则mcp-remote无法连接，会报\"connection refused\"错误。安装成功后状态栏应显示\"Stata\"。
:::

**Step 2：配置mcp.json**（仅Qoder/Claude Desktop需要此配置）

```json
"stata-mcp": {
  "command": "npx",
  "args": ["-y", "mcp-remote", "http://localhost:4000/mcp-streamable"]
}
```

**Step 3：验证服务**

```bash
# 健康检查（扩展启动后执行）
curl -s http://localhost:4000/health
# 期望返回: {"status":"ok","service":"Stata MCP Server","version":"0.4.1","stata_available":true}
```

**端点说明**：

| **端点**                             | **协议**        | **用途**           |
|:-------------------------------------|:----------------|:-------------------|
| http://localhost:4000/mcp-streamable | Streamable HTTP | 首选（现代客户端） |
| http://localhost:4000/mcp            | SSE             | 旧版兼容           |
| http://localhost:4000/health         | HTTP GET        | 健康检查           |

### 两种方案选型建议

| **维度** | **SepineTam（本课程默认）** | **hanlulong（IDE扩展）** |
|:---|:---|:---|
| 是否需要IDE扩展 | 否 | 是（DeepEcon.stata-mcp） |
| 是否需要IDE窗口保持打开 | 否 | 是 |
| 安全机制 | Command Guard + RAM监控 | 无 |
| 安装难度 | pip install uv即可 | 需安装扩展 |
| 适合场景 | Agent驱动分析、CLI环境 | IDE内交互式编码 |

## 完整Stata MCP设置参考

以下设置适用于hanlulong/stata-mcp扩展方案，可在IDE设置中搜索\"Stata MCP\"修改：

| **设置项**                     | **说明**                   | **默认值** |
|:-------------------------------|:---------------------------|:-----------|
| stata-vscode.stataPath         | Stata安装路径              | 自动检测   |
| stata-vscode.stataEdition      | 版本（MP/SE/BE）           | mp         |
| stata-vscode.mcpServerPort     | MCP端口                    | 4000       |
| stata-vscode.autoStartServer   | 自动启动服务器             | true       |
| stata-vscode.multiSession      | 多会话并行                 | true       |
| stata-vscode.maxSessions       | 最大并发会话数             | 100        |
| stata-vscode.sessionTimeout    | 会话空闲超时（秒）         | 3600       |
| stata-vscode.resultDisplayMode | 输出模式（compact/full）   | compact    |
| stata-vscode.maxOutputTokens   | MCP输出最大token（0=无限） | 10000      |

:::note[提示]
Compact模式会过滤循环代码回显、程序定义块、命令回显和续行符、冗余消息如\"(N real changes made)\"，有助于减少AI的token消耗。
:::

## macOS安装说明

1.  下载macOS版Stata安装包（.dmg格式）

2.  双击.dmg文件，将Stata拖拽到Applications文件夹

3.  首次运行可能需要到「系统设置 → 隐私与安全性」中允许运行

4.  激活授权：按官方说明完成激活

**macOS Stata路径**：

```bash
/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp
```

macOS用户使用stata-mcp时：

- **SepineTam方案**：mcp.json中STATA_PATH设置为上述路径

- **hanlulong方案**：安装DeepEcon.stata-mcp扩展后，扩展会自动检测Stata路径

## 常见问题

| **现象** | **原因** | **解决** |
|:---|:---|:---|
| 安装时提示「Windows已保护您的电脑」 | SmartScreen误报 | 点击「更多信息」→「仍要运行」 |
| 启动报「License not found」 | 授权文件未正确放置 | 把stata.lic拷贝到C:<br/>Program Files<br/>Stata18<br/>根目录 |
| stata-mcp报「Stata not found」 | STATA_PATH路径写错或转义错 | 用PowerShell Test-Path验证 |
| 中文路径乱码 | 安装在中文目录下 | 卸载后重装到C:<br/>Program Files<br/>等纯英文路径 |
| 无法激活 | 授权码输入错误或过期 | 核对购买确认邮件中的序列号和授权码 |

## 替代方案（无法安装Stata时）

若实在无法安装Stata，可使用Python替代：

```python
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_stata("data/bank_panel.dta")
# 或 pd.read_excel

model = smf.ols("roe ~ npl_ratio + car + loan_growth + np.log(asset)",
```
data=df).fit(cov_type="cluster",
cov_kwds={"groups": df["bank_id"]})
```
print(model.summary())
```

并在实验报告中注明「采用Python statsmodels替代Stata」即可获得同等分数。

# 环境准备与CNB项目同步详细步骤

本附录帮助学生完成开发环境搭建，并将课程仓库同步到个人CNB空间。

## 安装 Trae CN

1.  访问 <https://www.trae.cn/ide/download>

2.  根据你的电脑系统选择对应版本下载：

```text
- Windows 用户：点击 Windows (x64) 下载
```

```text
- macOS 用户：点击 macOS (Apple Silicon) 下载
```

3.  安装完成后打开，首次启动选择「简体中文」

4.  使用手机号登录

## 安装基础运行时

winget 是 Windows 10/11 自带的包管理器。如果你的电脑上没有 winget，请使用下方「方式二」从官网下载安装。

**如何打开 PowerShell（管理员）**：右键点击屏幕左下角「开始」按钮 → 选择「终端(管理员)」或「Windows PowerShell(管理员)」

### 方式一：winget 一键安装（Windows 10/11 推荐）

在打开的 PowerShell（管理员）窗口中，逐条复制粘贴执行以下命令：

```bash
# 安装 Python 3.12
winget install --id Python.Python.3.12 -e --source winget

# 安装 Node.js LTS（长期支持版，不要选 Current）
winget install --id OpenJS.NodeJS.LTS -e --source winget

# 安装 Git
winget install --id Git.Git -e --source winget
```

### 方式二：官网下载安装（备选方案）

| **软件** | **下载地址** | **安装注意事项** |
|:---|:---|:---|
| Python 3.12 | <https://www.python.org/downloads/> | 务必勾选「Add Python to PATH」 |
| Node.js LTS | <https://nodejs.org/> | 选 LTS 版本，一路 Next |
| Git | <https://git-scm.com/download/win> | 务必勾选「Add Git to PATH」 |

### macOS 用户

如果终端提示 `brew: command not found`，说明尚未安装 Homebrew。先在终端执行：

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

然后安装所需软件：

```bash
brew install python@3.12 node git
```

:::caution[警告]
安装完成后，**必须关闭当前终端窗口，重新打开一个新终端**，才能识别 `python`、`node`、`git` 命令。
:::

## 安装 Python 包管理工具

前提：确保第二步中的三个软件已安装完成，并且已重启终端（关闭再重新打开）。

```bash
# 升级 pip
python -m pip install --upgrade pip

# 安装 uv（MCP 服务运行必需）
pip install uv -i https://pypi.tuna.tsinghua.edu.cn/simple

# 安装课程依赖库
pip install flask pandas openpyxl pypdf -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 安装 CNB CLI 与 Skills

前提：确保 `node --version` 有输出。如果报 `command not found`，回到第二步确认 Node.js 已安装并重启终端。

```bash
# 安装 CNB 命令行工具（管理仓库、组织等）
npm install @cnbcool/cnb-cli -g

# 安装 Skills 技能管理工具（实验三 Skill 体系的前置依赖）
npm install skills -g

# 添加 CNB Skill（增强 IDE 中的 AI 功能）
npx skills add https://cnb.cool/cnb/skills/cnb-skill.git --agent trae -y --copy
```

## 验证环境

在 Trae CN 终端（按 `Ctrl + ‘` 打开）中逐条执行：

```bash
python --version     # 应显示 3.12.x
node --version       # 应显示 v20.x 或更高
git --version        # 应显示 git version x.x
uvx --version        # 应显示版本号
cnb --version        # 应显示版本号
skills list          # 应显示已安装的技能列表（含 cnb-api 等）
```

如果某条命令报 `command not found`，说明该软件未正确安装或未加入 PATH。请回到对应步骤重新安装，然后重启终端再验证。

## CNB 项目同步

### 步骤 1：注册 CNB 账户并创建访问令牌

1.  浏览器打开 <https://cnb.cool>

2.  点击「注册」→ 微信扫码登录

3.  登录后，点击右上角头像 →「个人设置」→ 左侧菜单「访问令牌」

4.  在「令牌名」处填写：`smartbanking`

5.  授权范围设置（两种方式任选其一）：

```text
- 方式 A（推荐）：在「常见场景」区域勾选「Git 客户端凭据」
```

```text
- 方式 B：在下方「授权范围」中找到 repo-code → 选择「读写」
```

6.  点击页面底部「创建」按钮

7.  立即复制 Token

:::caution[警告]
Token 仅显示一次，关闭页面后无法再次查看！建议将 Token 粘贴到记事本或备忘录中保存。
:::

### 步骤 2：在 CNB 新建空仓库

1.  登录后点击页面左上角「+」按钮 → 选择「创建仓库」

2.  「仓库归属」改为你的个人命名空间（点击下拉框选择自己的用户名）

3.  「仓库名称」填写：`smartbanking`

4.  「公开性」选择：公开（默认即是公开）

5.  点击「创建」按钮

### 步骤 3：登录 CNB CLI

在 Trae CN 终端执行：

```bash
cnb login
```

终端会显示一个授权链接和一个 `user_code`（如 `bUp4WV3u`），并自动打开浏览器。

1.  终端显示链接后，浏览器会自动打开授权页面

2.  如果浏览器没有自动打开，手动复制终端中的链接到浏览器

3.  在授权页面确认 user_code 与终端显示的一致，点击「授权」

4.  终端显示登录成功信息即可

如果 `cnb login` 报错或超时，可以跳过此步骤，在步骤 6 中改用 Token URL 方式推送。

### 步骤 4：克隆课程仓库到本地

```bash
# 克隆教师仓库（完整课程资料）
git clone https://cnb.cool/xiaosicau/smartbanking.git smartbanking-work
cd smartbanking-work
```

### 步骤 5：配置 Git 用户信息

```bash
# 替换为你的真实姓名和邮箱（用于提交记录显示）
git config --global user.name "你的姓名"
git config --global user.email "你的邮箱@example.com"
```

### 步骤 6：关联并推送到你的 CNB 仓库

```bash
# 添加你自己的 CNB 仓库为远程地址
# 将 <你的用户名> 替换为你的 CNB 用户名
git remote add myrepo https://cnb.cool/<你的用户名>/smartbanking.git

# 推送所有代码到你的 CNB 仓库
git push myrepo main
```

如果步骤 3 中 `cnb login` 成功，此步骤无需再输入密码。

如果 `git push` 提示输入用户名密码或认证失败，改用以下命令：

```bash
# 将 <你的Token> 替换为步骤 1 保存的令牌
git remote set-url myrepo https://cnb:<你的Token>@cnb.cool/<你的用户名>/smartbanking.git
git push myrepo main
```

### 步骤 7：验证同步结果

打开浏览器访问 `https://cnb.cool/你的用户名/smartbanking`，确认页面显示以下目录结构：

```bash
smartbanking/
+-- .agents/                     # Qoder AI 技能配置
+-- 智慧银行实验教程chapters/    # 教程主体（12章 + 附录）
|   +-- 智慧银行实验教程.tex
|   +-- preface.tex ~ ch12.tex
|   +-- appendix.tex
|   +-- ...
+-- 实验讲义 /                   # 实验讲义文档
+-- .gitignore
+-- cnb-smartbanking.png
+-- README.md
```

## 附加练习：安装 PPT Master（AI 生成 PPT 工具）

PPT Master 是一个开源项目，可以用 AI 从任意文档生成原生可编辑的 PPT。

**项目地址**（任选其一，优先选国内镜像，速度快）：

- GitHub（官方）：<https://github.com/hugohe3/ppt-master>

- AtomGit（国内镜像）：<https://atomgit.com/hugohe3/ppt-master>

- Gitee AI（国内）：<https://ai.gitee.com/apps/66b932ba-9844-4184-adf6-aa567b2b8788>

**安装步骤**：

1.  克隆项目到本地（国内推荐用 AtomGit）：

```
```bash
# 方式 A（AtomGit 国内镜像，推荐）
git clone https://atomgit.com/hugohe3/ppt-master.git
```

```
# 方式 B（GitHub 官方）
git clone https://github.com/hugohe3/ppt-master.git
```
```

```text
也可以直接下载 ZIP 解压后进入目录。
```

2.  安装 Python 依赖：

```text
```bash
pip install -r requirements.txt
```
```

3.  验证安装：

```
```bash
python -c "import pptx; print('python-pptx 版本:', pptx.__version__)"
```
```

4.  浏览示例（可选）：打开 `examples/` 目录查看示例，或在线预览 <https://hugohe3.github.io/ppt-master/>

**使用方法**：在 Trae CN 中打开 ppt-master 项目，将源材料放入 `projects/` 目录，然后在 AI 对话中告诉它要把什么内容做成 PPT 即可。

## 验收清单

完成以下全部检查项，截图保存作为实验报告交付物：

|  **完成**   | **检查项**                      |
|:-----------:|:--------------------------------|
| $`\square`$ | Trae CN 已安装并登录            |
| $`\square`$ | `python --version` ≥ 3.10       |
| $`\square`$ | `node --version` ≥ v20          |
| $`\square`$ | `git --version` 有输出          |
| $`\square`$ | `cnb --version` 有输出          |
| $`\square`$ | `cnb login` 登录成功            |
| $`\square`$ | 项目已成功推送到自己的 CNB 仓库 |
| $`\square`$ | 在 CNB 网页能看到项目文件列表   |

## 常见问题速查

| **报错信息** | **原因** | **解决方法** |
|:---|:---|:---|
| `command not found` | 安装后未重启终端 | 关闭终端窗口，重新打开再试 |
| `cnb login` 超时 | 网络问题或 Token 错误 | 检查网络；或跳过 cnb login，在步骤6改用 Token URL |
| git push 要求输入密码 | cnb login 未生效 | 改用 Token URL 方式推送 |
| Authentication failed | Token 未复制完整或已过期 | 回步骤1重新创建令牌 |
| 403 Forbidden | 推送的是 origin（教师仓库） | 确认执行 `git push myrepo main` |
| updates were rejected | 自己的仓库已有内容 | 回步骤2删除仓库重建空仓库 |
| `skills add` 报错 | npm 镜像问题 | 执行 `npm config set registry https://registry.npmmirror.com` |
| `uvx: command not found` | uv 未安装 | 运行 `pip install uv` |
| Token 忘记保存 | Token 仅显示一次 | 回步骤1重新创建新令牌 |
| 中文文件名乱码 | 终端编码非 UTF-8 | Trae CN 设置中将终端编码改为 UTF-8 |

  : 常见问题速查

# CNB与GitHub命令速查

## 基础Git命令对比

CNB的基础Git命令与GitHub**完全相同**，因为它们都基于Git版本控制系统。

| **操作** | **Git命令**                  | **CNB中使用** |
|:---------|:-----------------------------|:--------------|
| 克隆仓库 | `git clone <url>`            | 相同          |
| 添加文件 | `git add <file>`             | 相同          |
| 提交     | `git commit -m "message"`    | 相同          |
| 推送     | `git push origin main`       | 相同          |
| 拉取     | `git pull origin main`       | 相同          |
| 分支管理 | `git branch`, `git checkout` | 相同          |

## CNB专属CLI命令

CNB提供了`cnb`命令行工具来管理平台资源：

```bash
# 登录/登出
cnb login
cnb logout

# 组织管理
cnb organizations list-top-groups
cnb organizations create-organization

# 仓库管理
cnb repositories list-repos
cnb repositories create-repo

# Issue和PR管理
cnb issues list-issues
cnb pulls list-pulls

# AI功能
cnb ai summarize-pr
```

## 仓库地址格式对比

**GitHub**：

```bash
https://github.com/用户名/仓库名.git
git@github.com:用户名/仓库名.git
```

**CNB**：

```bash
https://cnb.cool/组织名/仓库名.git
https://cnb:令牌@cnb.cool/组织名/仓库名.git  (带令牌认证)
```

:::note[提示]
- **Git核心命令**：完全一致，可使用熟悉的Git命令进行代码管理

- **平台管理命令**：CNB提供额外的`cnb` CLI来管理组织、仓库、Issue等

- **认证方式**：CNB使用访问令牌（Token）进行认证

如果你熟悉GitHub的使用，切换到CNB几乎没有学习成本！
:::

# 金融数据源汇总

本附录汇总课程实验中可能用到的金融数据源，包括免费和付费两大类。

## tushare Pro

tushare Pro是国内最流行的金融数据接口之一，提供A股、基金、期货、港股通等全品类数据。

**官网**：<https://tushare.pro>

**数据覆盖**：

| **数据类别** | **接口示例** | **说明** |
|:---|:---|:---|
| A股日线 | `daily()` | 沪深A股日线行情（开盘/收盘/最高/最低/成交量） |
| A股分钟线 | `pro.bar()` | 1分钟/5分钟线 |
| 财务数据 | `income()`, `balancesheet()` | 利润表、资产负债表等 |
| 基金净值 | `fund_nav()` | 开放式基金净值数据 |
| 期货数据 | `futures_daily()` | 商品期货日线行情 |
| 港股通 | `hk_hold()` | 港股通持股数据 |
| 宏观经济 | `cn_gdp()` | GDP、CPI等宏观数据 |

**安装与使用**：

```bash
pip install tushare
```

```python
import tushare as ts
pro = ts.pro_api('your_token')

# 获取贵州茅台日线数据
df = pro.daily(ts_code='600519.SH', start_date='20260101', end_date='20260608')

# 获取沪深300成分股
hs300 = pro.index_weight(index_code='399300.SZ')
```

:::note[提示]
tushare Pro采用积分制：注册送120积分，可访问基础数据；更高级的数据需要更多积分。获取积分的方式包括：完善个人信息、充值、分享文章等。课程实验所需的基础数据120积分即可满足。
:::

## akshare

akshare是免费开源的中国金融数据接口，无需注册和Token，适合初学者快速上手。

**官网**：<https://akshare.akfamily.xyz>

**安装与使用**：

```bash
pip install akshare
```

```python
import akshare as ak

# 获取A股实时行情
df = ak.stock_zh_a_spot_em()

# 获取个股历史数据
df = ak.stock_zh_a_hist(symbol="600519", period="daily",
```
start_date="20260101", end_date="20260608")
```

# 获取基金净值
df = ak.fund_open_fund_info_em(symbol="000001")

# 获取宏观数据
df = ak.macro_china_gdp()
```

**特点**：完全免费、无需注册、数据来源为东方财富等公开网站、更新频繁（几乎每周更新）。

## yfinance

yfinance是Yahoo Finance的Python接口，提供全球市场的股票、基金、指数、汇率等数据。

**安装与使用**：

```bash
pip install yfinance
```

```python
import yfinance as yf

# 获取苹果公司股票数据
aapl = yf.Ticker("AAPL")
df = aapl.history(period="1y")

# 获取沪深300ETF数据
df = yf.download("000300.SS", start="2026-01-01", end="2026-06-08")

# 获取美元兑人民币汇率
df = yf.download("CNY=X", period="6mo")
```

**特点**：全球市场覆盖、免费使用、适合国际比较分析。国内A股数据延迟约15分钟。

## FRED

FRED（Federal Reserve Economic Data）是美联储经济数据库，提供50万+美国及全球经济指标。

**官网**：<https://fred.stlouisfed.org>

```bash
pip install fredapi
```

```python
from fredapi import Fred
fred = Fred(api_key='your_key')

# 获取美国GDP
gdp = fred.get_series('GDP')

# 获取联邦基金利率
ffr = fred.get_series('FEDFUNDS')

# 获取CPI
cpi = fred.get_series('CPIAUCSL')
```

**特点**：数据权威、更新及时、免费API（需注册获取Key）。适合宏观经济研究和中美对比分析。

## Wind与CSMAR

**Wind**：万得金融数据终端，国内金融机构标配，数据最全最专业。年费数万元，一般学校图书馆有终端机可使用。

**CSMAR**：国泰安数据库，学术研究常用，涵盖中国上市公司财务、治理、交易等全维度数据。高校通常有机构订阅，可通过学校图书馆访问。

:::note[提示]
- 课程实验：优先使用tushare/akshare免费数据

- 毕业论文：申请学校图书馆的Wind/CSMAR访问权限

- 竞赛/科研项目：可通过导师申请专项数据经费
:::

## 各数据源对比

| **数据源**  | **覆盖市场** |   **费用**   | **A股深度** | **API质量** | **推荐度** |
|:------------|:-------------|:------------:|:-----------:|:-----------:|:----------:|
| tushare Pro | 中国         | 免费/积分制  |     高      |     优      |   ★★★★★    |
| akshare     | 中国         |     免费     |     中      |     良      |    ★★★★    |
| yfinance    | 全球         |     免费     |     低      |     良      |    ★★★     |
| FRED        | 美国/全球    |     免费     |     无      |     优      |    ★★★★    |
| Wind        | 全球         | 付费（昂贵） |    极高     |     优      |   ★★★★★    |
| CSMAR       | 中国         | 付费（机构） |    极高     |     良      |    ★★★★    |

  : 金融数据源对比

## OpenMAIC：AI辅助教学工具

**OpenMAIC**（Open Multi-Agent Interactive Classroom）是清华大学教育学院开发的开源AI教学平台，采用多智能体编排技术，可将任何主题一键转化为交互式课堂体验。

**官网**：<https://open.maic.chat>

**GitHub**：<https://github.com/THU-MAIC/OpenMAIC>（18.6k Stars）

### 核心功能

| **功能**   | **说明**                                           |
|:-----------|:---------------------------------------------------|
| AI教师讲解 | 自动生成课件，支持语音讲解、聚光灯和激光笔效果     |
| AI同学讨论 | 多智能体参与讨论，模拟真实课堂氛围                 |
| 随堂测验   | 自动生成单选/多选/简答题，AI实时评分反馈           |
| 交互式模拟 | 可操作的HTML模拟场景（3D可视化、流程模拟、小游戏） |
| 白板演示   | AI实时绘图讲解，支持公式推导、流程图绘制           |
| 项目制学习 | 学生选择角色，与AI协作完成结构化项目               |

  : OpenMAIC核心功能

### 快速上手

```bash
# 方式一：托管版（无需部署）
# 访问 https://open.maic.chat，注册后即可使用

# 方式二：本地部署
git clone https://github.com/THU-MAIC/OpenMAIC.git
cd OpenMAIC
pnpm install
cp .env.example .env.local
# 编辑 .env.local，填入至少一个API Key
pnpm dev
# 访问 http://localhost:3000
```

### 支持的AI模型

OpenMAIC支持多种AI模型提供商：

| **提供商** | **模型**        | **配置项**          |
|:-----------|:----------------|:--------------------|
| OpenAI     | GPT-5.5, GPT-4o | `OPENAI_API_KEY`    |
| Anthropic  | Claude Opus 4.8 | `ANTHROPIC_API_KEY` |
| Google     | Gemini 3 Flash  | `GOOGLE_API_KEY`    |
| 小米       | MiMo v2.5 Pro   | `XIAOMI_API_KEY`    |
| 智谱       | GLM-5.1         | `GLM_API_KEY`       |
| DeepSeek   | DeepSeek-V4     | `DEEPSEEK_API_KEY`  |
| 本地       | Ollama          | `OLLAMA_BASE_URL`   |

  : OpenMAIC支持的AI模型

### 导出格式

- **PowerPoint (.pptx)**：可编辑的课件，包含图片、图表和LaTeX公式

- **交互式HTML**：自包含网页，包含交互式模拟实验

- **课堂ZIP**：完整课堂导出（课件+媒体），可备份或分享

### 与本课程的结合

建议将OpenMAIC用于以下教学场景：

1.  **课前预习**：输入章节主题，生成预习课件，学生提前了解核心概念

2.  **课堂互动**：使用AI教师讲解+AI同学讨论，增强课堂参与度

3.  **课后复习**：生成随堂测验，巩固学习成果

4.  **项目展示**：为综合项目生成交互式演示，提升答辩效果

# LaTeX论文排版模板

## 课程实验报告模板

以下为本课程实验报告的LaTeX模板，可直接复制使用：

```html
\documentclass[12pt,a4paper]{ctexart}
\usepackage[margin=2.5cm]{geometry}
\usepackage{amsmath,amssymb}
\usepackage{graphicx}
\usepackage{float}
\usepackage{booktabs}
\usepackage{listings}
\usepackage{xcolor}
\usepackage[colorlinks=true,urlcolor=blue]{hyperref}

\title{智慧银行实验教程<br/>实验X：\{实验名称\}}
\author{姓名 \quad 学号 \quad 班级}
\date{\today}

\begin{document}
\maketitle

## 实验目的
% 描述本次实验的学习目标

## 实验环境
% 列出操作系统、IDE、语言版本等

## 实验步骤
### 步骤1：...
% 详细记录操作步骤，附截图

### 步骤2：...

## 实验结果
% 展示实验产出（截图/代码/数据）

## 问题与解决
% 记录遇到的问题及解决方法

## 实验心得
% 总结收获和不足

\end{document}
```

## 本科毕业论文模板简介

本科毕业论文一般采用学校提供的模板。如学校未提供，可参考以下基本结构：

```html
\documentclass[12pt,a4paper]{ctexbook}
\usepackage[top=2.5cm,bottom=2.5cm,left=3cm,right=3cm]{geometry}
\usepackage[backend=biber,style=gb7714-2015]{biblatex}
\addbibresource{references.bib}
% ... 其他宏包 ...

\begin{document}
\frontmatter
\maketitle
\tableofcontents

\mainmatter
# 绪论
## 研究背景与意义
## 文献综述
## 研究内容与方法

# 理论与方法
# 实验设计
# 结果与分析
# 结论与展望

\backmatter
\printbibliography
\end{document}
```

:::note[提示]
- 使用`gb7714-2015`参考文献格式，符合国标要求

- 图表编号自动管理：`\caption{...}` + `\label{...}`

- 交叉引用用`\ref{...}`，不手动写编号

- 编译顺序：xelatex → biber → xelatex → xelatex
:::

## 常用LaTeX技巧速查

| **需求**  | **LaTeX代码**                                           |
|:----------|:--------------------------------------------------------|
| 插入图片  | `\includegraphics[width=0.8\textwidth]{fig.png}`        |
| 插入表格  | 使用`booktabs`宏包的`\toprule`/`\midrule`/`\bottomrule` |
| 数学公式  | 行内`$...$`，行间`\[...\]`，编号`\begin{equation}`      |
| 引用文献  | `\textcite{key}`或`\parencite{key}`                     |
| 超链接    | `\url{https://...}`或`\href{url}{文字}`                 |
| 代码块    | `\begin{lstlisting}[style=shell] ... \end{lstlisting}`  |
| 分栏      | `\begin{multicols}{2}...\end{multicols}`                |
| 脚注      | `\footnote{脚注内容}`                                   |
| 加粗/斜体 | `**加粗**` / `*斜体*`                                   |
| 特殊符号  | 度数`$^\circ$C`，百分号`$\%$`，美元`$\$$`               |

  : LaTeX技巧速查

# 术语表

本术语表收录课程中涉及的60+核心术语，按拼音首字母排序，附中英对照及简要释义。

| **术语** | **英文** | **释义** |
|:---|:---|:---|
| **术语** | **英文** | **释义** |
| Agent | Autonomous Agent | 能自主感知环境、做出决策并执行动作的AI系统 |
| BMAD | Build-Measure-Analyze-Decide | 一种迭代式软件开发方法论 |
| CRM | Customer Relationship Management | 客户关系管理系统，用于管理客户交互和数据 |
| CTAN | Comprehensive TeX Archive Network | LaTeX宏包的全球分发网络 |
| DSL | Domain-Specific Language | 领域特定语言，为特定领域设计的专用语言 |
| ESG | Environmental, Social, Governance | 环境、社会、治理，企业可持续发展评估框架 |
| FAQ | Frequently Asked Questions | 常见问题解答 |
| FRED | Federal Reserve Economic Data | 美联储经济数据库 |
| FSM | Finite State Machine | 有限状态机，一种对话管理策略 |
| Git | — | 分布式版本控制系统 |
| GUI | Graphical User Interface | 图形用户界面 |
| IDE | Integrated Development Environment | 集成开发环境 |
| IVR | Interactive Voice Response | 交互式语音应答系统 |
| JSON | JavaScript Object Notation | 轻量级数据交换格式 |
| KPI | Key Performance Indicator | 关键绩效指标 |
| LaTeX | — | 学术排版系统，本课程用于论文写作 |
| LLM | Large Language Model | 大语言模型，如GPT-4、Claude等 |
| LSTM | Long Short-Term Memory | 长短期记忆网络，一种循环神经网络 |
| LPR | Loan Prime Rate | 贷款市场报价利率 |
| MCP | Model Context Protocol | 模型上下文协议，AI工具调用标准 |
| MVP | Minimum Viable Product | 最小可行产品 |
| NER | Named Entity Recognition | 命名实体识别 |
| NLP | Natural Language Processing | 自然语言处理 |
| NLG | Natural Language Generation | 自然语言生成 |
| NLU | Natural Language Understanding | 自然语言理解 |
| OLS | Ordinary Least Squares | 普通最小二乘法 |
| PR | Pull Request | 代码合并请求 |
| RAG | Retrieval-Augmented Generation | 检索增强生成 |
| SARIMA | Seasonal ARIMA | 季节性自回归移动平均模型 |
| SHAP | SHapley Additive exPlanations | 基于博弈论的模型解释方法 |
| Skill | — | 领域知识文件（SKILL.md），赋予AI专业能力 |
| WBS | Work Breakdown Structure | 工作分解结构 |
| XeLaTeX | — | 支持Unicode和系统字体的LaTeX引擎 |
| 按需安装 | On-demand Installation | MiKTeX特性，使用未安装宏包时自动下载 |
| 词嵌入 | Word Embedding | 将词语映射为低维向量的技术 |
| 对话框 | Dialogue Box | 聊天界面的消息展示区域 |
| 反洗钱 | Anti-Money Laundering (AML) | 防止不法资金通过金融系统合法化的监管要求 |
| 风险偏好 | Risk Appetite | 投资者对风险的承受意愿和能力 |
| 缝合怪 | Frankenstein | 指拼凑不同代码片段但不理解其原理的做法 |
| 幻觉 | Hallucination | AI生成看似合理但事实错误的内容 |
| 活期存款 | Demand Deposit | 随时可存取的银行存款 |
| 基金定投 | Regular Investment Plan | 定期定额投资基金的理财方式 |
| 框架填充 | Frame Filling | 一种对话管理策略，通过多轮收集槽位 |
| 跨行转账 | Interbank Transfer | 向其他银行账户转账 |
| 零售银行 | Retail Banking | 面向个人客户的银行服务 |
| 流动性 | Liquidity | 资产快速变现而不损失价值的能力 |
| 蒙特卡洛 | Monte Carlo | 通过随机模拟进行数值计算的方法 |
| 内幕交易 | Insider Trading | 利用非公开信息进行证券交易的违法行为 |
| 提示工程 | Prompt Engineering | 设计和优化AI输入提示的技术 |
| 刚性兑付 | Guaranteed Redemption | 金融机构承诺保本保收益的做法（已被禁止） |
| 商业计划书 | Business Plan | 描述商业机会和实施计划的文档 |
| 身份识别 | KYC (Know Your Customer) | 了解你的客户，银行客户身份识别义务 |
| 投资者适当性 | Investor Suitability | 确保推荐产品与客户风险承受能力匹配 |
| 脱敏 | Data Masking | 对敏感数据进行遮蔽处理，如6222\*\*\*\*1234 |
| 微调 | Fine-tuning | 在预训练模型基础上用特定数据继续训练 |
| 向量数据库 | Vector Database | 存储和检索向量嵌入的专用数据库 |
| 协议签署 | Agreement Signing | 客户确认产品条款的法律行为 |
| 意图识别 | Intent Classification | 判断用户话语所表达的意图类型 |
| 槽填充 | Slot Filling | 从用户话语中提取业务所需的结构化信息 |
| 知识图谱 | Knowledge Graph | 以实体和关系构建的结构化知识库 |
| 投资者适当性管理 | Suitability Management | 确保产品推荐与客户风险等级匹配的监管要求 |
| 资产证券化 | Securitization | 将资产转化为可交易证券的金融技术 |

  : 术语表
