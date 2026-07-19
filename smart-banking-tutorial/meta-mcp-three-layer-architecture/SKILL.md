---
name: meta-mcp-three-layer-architecture
description: 当用户需要理解、设计、配置或排查MCP（Model Context Protocol）系统时使用，尤其是面对"为什么MCP比传统API更适合AI"、"MCP三层架构怎么搭"、"MCP生命周期怎么走"、"如何给AI接入外部工具/数据"这类问题。判断信号：用户提到"MCP"、"Model Context Protocol"、"给AI接工具"、"AI调外部API"、"JSON-RPC"、"MCP Server配置"、"AI agent连数据库"、设计AI工具系统。区别于讲具体MCP服务器配置的工具型skill，本skill解决的是MCP架构原理的元问题。
---

# MCP 三层架构与 JSON-RPC 生命周期

## R — 原文引用

> "MCP（Model Context Protocol）是一种让AI模型与外部工具、数据源、API标准化通信的协议。它把AI与世界的交互抽象为三层——**Host（宿主）/ Client（客户端）/ Server（服务端）**，通过JSON-RPC 2.0消息格式完成'发现-调用-返回'的完整生命周期。相比传统API，MCP让AI'自己决定调用什么'，而不是人预先写死调用逻辑。"
> — 《智慧银行实验教程》ch03 §3.1

## I — 方法论骨架

### 三层架构

| 层 | 角色 | 类比 | 典型实现 |
|---|---|---|---|
| **Host 宿主** | AI所在的应用 | 大脑所在的身体 | Claude Desktop、Cursor、自研agent |
| **Client 客户端** | Host内的MCP适配器 | 神经末梢 | Host内置或插件 |
| **Server 服务端** | 暴露工具/数据 | 手脚+感官 | Tushare MCP、Excel MCP、Playwright MCP |

### JSON-RPC 生命周期（6步）

```
1. initialize       Host→Server  协商版本和能力
2. tools/list       Host→Server  "你有哪些工具？"
3. tools/call       Host→Server  AI决定调用某工具（含参数）
4. 执行             Server内部   调用真实API/数据库
5. 结果返回         Server→Host  JSON-RPC response
6. AI整合           Host内部     把工具结果喂回模型，生成最终回答
```

### MCP vs 传统API

| 维度 | 传统API | MCP |
|---|---|---|
| 调用决策 | 人写死代码逻辑 | AI根据语义自主决定 |
| 接入成本 | 每个API单独适配 | 标准协议，N×M → N+M |
| 发现机制 | 无（需文档） | tools/list 自动发现 |
| 参数构造 | 人工hardcode | AI根据schema生成 |

## A1 — 书中案例

**银行数据接入MCP化**（ch03 §3.3）：
- 传统做法：写Python脚本调Tushare API，hardcode参数，AI只能看结果
- MCP化：配置Tushare MCP Server → Host通过tools/list发现"查股价、查财报、查宏观数据"等工具 → AI根据用户问题自主决定调哪个、传什么参数
- 效果：同一个agent能回答"分析茅台最近3年财报"、"对比四大行ROE"、"查2024年CPI走势"等任意组合问题，无需改代码

## A2 — 未来触发场景

**应触发**：
- "怎么让AI调用外部API/数据库"
- "MCP是什么/为什么比API好"
- "MCP Server怎么写/配置"
- "AI agent怎么连接工具"
- "JSON-RPC生命周期是什么"
- "为什么我的AI不能自主查数据"

**不应触发**（诱饵）：
- 单纯问"某个MCP Server怎么装" → 工具配置教程
- 单纯问"REST和RPC区别" → 通用协议对比
- 问"API怎么设计" → 用meta-mcp-skill-bmad-trinity

## E — 可执行步骤

1. **盘点外部依赖**：列出AI需要访问的所有外部系统（数据库、API、文件、SaaS）
2. **找现成MCP**：到MCP市场/官方仓库搜索——通常80%常见场景（数据库、Office、浏览器、天气、股票）已有现成Server
3. **配置Host**：在Host的mcp-config.json里挂载Server，填入认证信息
4. **验证发现**：启动Host，让AI执行"列出所有可用工具"，确认tools/list返回预期工具
5. **测试调用**：让AI执行3-5个典型任务，观察tools/call参数是否合理、结果是否正确
6. **设计回退**：对每个关键工具定义失败回退（如API限流时降级到本地缓存）

## B — 边界与盲点

**不适用**：
- 纯对话型应用（不需要外部数据）
- 高频实时场景（MCP的JSON-RPC开销比直连API大）
- 极简脚本（一次性调用，MCP化收益小于成本）

**作者盲点**：书中对"MCP的安全治理"讨论不足。实践中：
- MCP Server能访问什么数据必须严格白名单
- 敏感操作（转账、删除、修改）必须加二次人工确认
- Server日志要完整审计，防止AI误操作或被注入攻击
- 生产环境建议加rate limit和异常调用检测

## 相关 skills

- [meta-mcp-skill-bmad-trinity](../meta-mcp-skill-bmad-trinity/SKILL.md) — MCP在三位一体中的连接层定位
- [framework-finance-ai-application-matrix](../framework-finance-ai-application-matrix/SKILL.md) — 金融场景该接入哪些MCP
- [flow-six-node-skill-pipeline](../flow-six-node-skill-pipeline/SKILL.md) — Skill流水线中的数据节点通常由MCP承载
