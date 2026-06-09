# MCP服务配置参考手册

> 本文档汇总了《智慧银行实验教程》中使用的全部MCP服务及其配置方法。
> MCP（Model Context Protocol）是一种开放标准，通过三层架构（Client/Server/Tool）和JSON-RPC 2.0通信协议，实现AI与外部工具的标准化连接。

---

## 一、MCP服务总览

本教程共使用 **8组MCP服务**，分为4个功能组：

| 组别 | MCP名称 | 启动方式 | 主要能力 |
|------|---------|---------|---------|
| 浏览器组 | playwright | `npx @playwright/mcp@latest` | 操作Chromium/Firefox/WebKit，浏览器自动化 |
| 浏览器组 | chrome-devtools | `npx -y chrome-devtools-mcp@latest` | 调用Chrome DevTools（Lighthouse审计等） |
| 浏览器组 | fetch | `uvx mcp-server-fetch` | 直接抓取网页/JSON API |
| Office组 | excel | `npx --yes @negokaz/excel-mcp-server` | Excel读写、表格、格式、截图 |
| Office组 | word | `uvx --from office-word-mcp-server word_mcp_server` | Word读写、样式、目录、页码 |
| Office组 | ppt | `uvx --from office-powerpoint-mcp-server ppt_mcp_server` | PPT生成、模板、批量改稿 |
| 系统组 | WindowsMCP.Net | `Windows-MCP.Net.exe` | Windows原生UI操作（窗口/键鼠） |
| 数据分析组 | stata-mcp | `uvx stata-mcp` | 调用本机Stata进行计量回归分析 |

> **macOS注意**：WindowsMCP.Net仅支持Windows系统。macOS用户可跳过此MCP。

---

## 二、前置依赖安装

MCP服务依赖 Node.js（npx）和 Python（uvx）两个运行时：

```bash
# 1) 确认 Node.js >= v20、Python >= 3.10
node --version
python --version

# 2) 安装 uv（MCP服务如 fetch、word/ppt/stata-mcp 通过 uvx 启动）
pip install uv

# 3) 升级 pip / npm 到最新
python -m pip install --upgrade pip
npm install -g npm@latest

# 4) Windows用户额外安装 Windows-MCP.Net
dotnet tool install -g Windows-MCP.Net
```

---

## 三、配置文件路径

### Qoder

| 系统 | 路径 |
|------|------|
| Windows | `%APPDATA%\Qoder\SharedClientCache\extension\local\mcp.json` |
| macOS | `~/Library/Application Support/Qoder/SharedClientCache/extension/local/mcp.json` |

### TRAE CN

| 系统 | 路径 |
|------|------|
| Windows | `C:\Users\<用户名>\AppData\Roaming\Trae CN\User\mcp.json` |
| macOS | `~/Library/Application Support/Trae CN/User/mcp.json` |

---

## 四、完整 mcp.json 配置

将以下内容保存为 `mcp.json`（替换 `<用户名>` 为实际用户名）：

```json
{
  "mcpServers": {
    "fetch": {
      "command": "uvx",
      "args": ["mcp-server-fetch"]
    },
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    },
    "excel": {
      "command": "npx",
      "args": ["--yes", "@negokaz/excel-mcp-server"],
      "env": {
        "EXCEL_MCP_PAGING_CELLS_LIMIT": "10000"
      }
    },
    "word": {
      "command": "uvx",
      "args": ["--from", "office-word-mcp-server", "word_mcp_server"]
    },
    "ppt": {
      "command": "uvx",
      "args": ["--from", "office-powerpoint-mcp-server", "ppt_mcp_server"]
    },
    "WindowsMCP.Net": {
      "command": "C:\\Users\\<用户名>\\.dotnet\\tools\\Windows-MCP.Net.exe",
      "args": []
    },
    "stata-mcp": {
      "command": "uvx",
      "args": ["stata-mcp"],
      "env": {
        "STATA_PATH": "C:\\Program Files\\Stata18\\StataMP-64.exe",
        "MCP_STATA_LOGLEVEL": "INFO"
      }
    }
  }
}
```

### macOS Stata 路径

macOS 用户需将 `STATA_PATH` 修改为：

```json
"stata-mcp": {
  "command": "uvx",
  "args": ["stata-mcp"],
  "env": {
    "STATA_PATH": "/Applications/Stata/StataMP.app/Contents/MacOS/stata-mp",
    "MCP_STATA_LOGLEVEL": "INFO"
  }
}
```

### 配置字段说明

| 字段 | 含义 |
|------|------|
| `mcpServers` | 顶层对象，键 = MCP名称（自定义），值 = 启动配置 |
| `command` | 实际启动二进制（npx / uvx / .exe绝对路径） |
| `args` | 命令行参数，IDE启动时按数组顺序拼接 |
| `env` | 环境变量；放API Key、路径、限制参数 |
| `disabled` | 设为 `true` 时不加载该MCP |

---

## 五、各MCP服务详解

### 5.1 浏览器组

#### Playwright MCP

- **安装包**：`@playwright/mcp`
- **语言**：TypeScript
- **通信方式**：stdio
- **首次运行**需下载浏览器内核：`npx playwright install`

| 工具名 | 功能 |
|--------|------|
| `browser_navigate` | 导航到指定URL |
| `browser_click` | 点击页面元素 |
| `browser_fill` | 填写表单输入框 |
| `browser_screenshot` | 对当前页面截图 |
| `browser_evaluate` | 在页面上下文执行JavaScript |
| `browser_select_option` | 选择下拉菜单选项 |
| `browser_hover` | 鼠标悬停触发交互 |
| `browser_type` | 模拟键盘输入 |
| `browser_wait` | 等待元素出现或页面加载 |

**典型应用**：银行官网数据采集、业务流程监控、合规性验证。

#### Chrome DevTools MCP

- **安装包**：`chrome-devtools-mcp`
- **核心能力**：调用Lighthouse引擎对网页进行全方位审计

Lighthouse四维审计：

| 维度 | 关键指标 |
|------|---------|
| 性能（Performance） | FCP、LCP、CLS、FID |
| 可访问性（Accessibility） | 对比度、Alt文本、ARIA标签、键盘导航 |
| 最佳实践（Best Practices） | HTTPS使用、安全漏洞、浏览器错误 |
| SEO（搜索引擎优化） | 标题标签、Meta描述、结构化数据 |

#### Fetch MCP

- **安装包**：`mcp-server-fetch`
- **语言**：Python
- **本质**：AI驱动的HTTP客户端，自动构造HTTP请求并解析返回内容
- **适用场景**：金融API数据获取（汇率、利率、公告等）
- **局限**：不能处理需要JavaScript渲染的动态页面（此时应改用Playwright）

---

### 5.2 Office组

#### Excel MCP

- **安装包**：`@negokaz/excel-mcp-server`
- **环境变量**：`EXCEL_MCP_PAGING_CELLS_LIMIT=10000`

| 能力类别 | 具体功能 |
|---------|---------|
| 文件操作 | 创建/打开/保存/另存为Excel文件 |
| 数据读写 | 读取单元格、写入单元格、批量读写区域 |
| 格式设置 | 字体、颜色、边框、对齐方式、数字格式 |
| 公式计算 | 插入公式、自动计算、引用跨Sheet |
| 图表生成 | 柱状图、饼图、折线图、散点图 |
| Sheet管理 | 新建/重命名/删除/复制Sheet |
| 筛选排序 | 自动筛选、条件筛选、多列排序 |

**典型应用**：银行日报/周报/月报自动化、监管报表填充、客户分析报告。

#### Word MCP

- **安装包**：`office-word-mcp-server`
- **核心能力**：文档创建、样式设置、目录生成、页码插入
- **典型应用**：合规报告、客户函件、内部简报的标准化生成

#### PPT MCP

- **安装包**：`office-powerpoint-mcp-server`
- **核心能力**：基于模板生成PPT、批量修改幻灯片、插入图表
- **典型应用**：投研报告演示、银行年报简报

---

### 5.3 系统组

#### WindowsMCP.Net

- **安装方式**：`dotnet tool install -g Windows-MCP.Net`
- **仅支持 Windows**
- **核心能力**：Windows原生UI操作（窗口管理、键鼠模拟）
- **macOS替代**：可使用 `automation-mcp` 或 `macos-automator` MCP

---

### 5.4 数据分析组

#### Stata MCP

本教程介绍了两个Stata MCP方案：

##### 方案一：hanlulong/stata-mcp

| 项目 | 信息 |
|------|------|
| GitHub | https://github.com/hanlulong/stata-mcp |
| VS Code市场 | DeepEcon.stata-mcp |
| 要求 | Stata 17+ / UV包管理器 |
| 平台 | Windows / macOS / Linux |

**MCP工具清单**（3个）：
- `stata_run_selection` — 运行代码片段
- `stata_run_file` — 运行.do文件
- `stata_session` — 会话管理（list / destroy）

**端点地址**：

| 端点 | 协议 | 用途 |
|------|------|------|
| `http://localhost:4000/mcp-streamable` | Streamable HTTP | 首选（现代客户端） |
| `http://localhost:4000/mcp` | SSE | 旧版兼容 |
| `http://localhost:4000/health` | HTTP GET | 健康检查 |

**各客户端配置方式**：

| 客户端 | 配置方式 |
|--------|---------|
| Qoder / Claude Desktop | `"stata-mcp": {"command": "npx", "args": ["-y", "mcp-remote", "http://localhost:4000/mcp-streamable"]}` |
| Claude Code | `claude mcp add --transport http stata-mcp http://localhost:4000/mcp-streamable --scope user` |
| Cursor | `{"mcpServers": {"stata-mcp": {"url": "http://localhost:4000/mcp-streamable"}}}` |
| GitHub Copilot | `{"servers": {"stata-mcp": {"type": "http", "url": "http://localhost:4000/mcp-streamable"}}}` |

##### 方案二：SepineTam/mcp-for-stata

```bash
# 一键安装所有客户端
uvx stata-mcp install --all

# 环境检查
uvx stata-mcp doctor
```

| 特性 | hanlulong/stata-mcp | SepineTam/mcp-for-stata |
|------|---------------------|------------------------|
| 类型 | VS Code扩展（localhost HTTP） | 独立MCP Server + CLI |
| 执行方式 | IDE内嵌via localhost:4000 | do文件via subprocess |
| 安全机制 | — | Command Guard + RAM监控 |
| 最佳场景 | 在IDE中编写运行Stata | Agent驱动分析 |

##### Python替代方案

若无Stata环境，可用Python替代：

```python
import pandas as pd
import statsmodels.formula.api as smf

df = pd.read_stata("data/bank_panel.dta")
model = smf.ols("roe ~ npl_ratio + car + loan_growth + np.log(asset)",
                data=df).fit(cov_type="cluster",
                             cov_kwds={"groups": df["bank_id"]})
print(model.summary())
```

---

## 六、配置验证

修改 `mcp.json` 后，需**完全退出IDE**再重新打开（MCP配置只在启动时读取）。

验证步骤：

```bash
# 1) 终端验证基础工具
npx --version      # 确认npx可用
uvx --version      # 确认uvx可用

# 2) 在IDE Builder模式中输入以下提示词
请为我验证所有 MCP 服务的运行状态：
1. 测试 fetch 服务能否正常获取网页
2. 测试 excel 服务能否创建表格
3. 测试 playwright 服务能否启动浏览器
4. 输出完整的配置报告和服务状态
```

---

## 七、常见问题排查

| 现象 | 原因 | 解决方案 |
|------|------|---------|
| 找不到npx | Node.js未装或未加入PATH | 重装Node.js，勾选Add to PATH |
| 找不到uvx | 未装uv | `pip install uv` 或 `winget` 安装 |
| MCP工具不出现 | mcp.json语法错误 | 把整段JSON贴给AI检查格式 |
| playwright报错 | 首次运行需下载浏览器内核 | 执行 `npx playwright install` |
| stata-mcp报错 | STATA_PATH不正确 | 改为本机Stata实际安装路径 |
| 端口冲突（Stata） | 其他服务占用端口 | 修改 `stata-vscode.mcpServerPort` |
| MCP工具未刷新 | 同一会话中工具列表不更新 | 重启IDE/客户端 |
| JSON反斜杠问题 | JSON中反斜杠需转义 | 反斜杠写成 `\\` |

---

## 八、MCP组合编排模式

### 流水线模式（Pipeline）

按固定顺序依次执行，前一个MCP的输出作为后一个的输入：

```
Fetch → Excel → Word → PPT
(采集)  (处理)  (文档)  (演示)
```

### 并行模式（Parallel）

多个MCP同时执行独立任务，最后汇总：

```
Playwright ──→ 截图 + 审计数据
                  ↓ 汇总
Fetch ──────→ API数据    → Excel → 综合报告
```

### 条件分支模式（Conditional）

根据前一步结果决定后续调用哪个MCP：

```
Fetch → 数据格式判断
          ├── JSON格式 → 直接解析 → Excel
          └── HTML格式 → Playwright渲染 → 截图 → OCR → Excel
```

### 调用顺序原则

1. **数据先行**：Fetch/Playwright等采集类MCP最先执行
2. **处理居中**：Excel等数据处理MCP在采集之后、输出之前
3. **输出在后**：Word/PPT等文档生成MCP在数据处理完成后
4. **中间产物保存**：每一步输出保存为文件，确保步骤间解耦

---

## 九、MCP市场资源

| 市场 | 网址 | 说明 |
|------|------|------|
| 官方注册表 | https://github.com/modelcontextprotocol/servers | MCP协议作者维护 |
| Smithery | https://smithery.ai | 最活跃的第三方MCP市场，支持一键安装 |
| MCP.so | https://mcp.so | 中文友好的聚合站 |
| PulseMCP | https://www.pulsemcp.com | 含使用人数、更新频率排行 |
| Glama MCP Directory | https://glama.ai/mcp/servers | 服务器+客户端两个目录 |
| Awesome MCP Servers | https://github.com/punkpeye/awesome-mcp-servers | GitHub收集向list |
