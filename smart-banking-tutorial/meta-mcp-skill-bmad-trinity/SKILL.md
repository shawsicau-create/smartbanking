---
name: meta-mcp-skill-bmad-trinity
description: 当用户面对"AI如何赋能新业务/银行系统/智能应用"这类系统设计问题，或需要决定AI项目该用什么技术栈分工时使用。判断信号：用户提到"AI+业务"、"智能化改造"、"AI赋能"、选择MCP/Skill/BMAD组合、规划AI项目架构、为银行/金融/任意垂直行业设计AI智能系统。区别于单纯讲MCP或Skill的工具型skill，本skill解决的是"三者如何分工协同"的元架构问题。
---

# MCP + Skill + BMAD 三位一体框架

## R — 原文引用

> "构建银行业务智能系统，需要三个层面的能力协同——**连接**、**知识**和**方法**，分别由MCP、Skill和BMAD承载。BMAD定义'做什么'，Skill定义'怎么做'，MCP提供'能做什么'。"
> — 《智慧银行实验教程》ch01 §1.4

## I — 方法论骨架

把任意AI赋能业务系统拆成三层：

| 层 | 承载者 | 解决的问题 | 比喻 | 复杂度效应 |
|---|---|---|---|---|
| 连接层 | MCP | AI如何与世界交互 | 让AI有手脚 | N×M → N+M |
| 知识层 | Skill | AI如何拥有专业知识 | 让AI有专业脑 | 把组织记忆显性化 |
| 方法层 | BMAD | AI如何系统化做事 | 让AI有工作流 | 从碎片到闭环 |

**三者的递推关系**：
1. BMAD从业务需求出发，规划"要实现什么功能、达到什么标准"
2. Skill把功能分解为业务流程和操作步骤，编码为可执行脚本
3. MCP为Skill涉及的外部交互提供标准化连接

缺任何一层都会出问题：
- 没BMAD → AI东一榔头西一棒
- 没Skill → AI是通才但不懂业务
- 没MCP → AI只能"说话"不能"做事"

## A1 — 书中案例

**银行CRM系统开发**（ch07 §7.2）：
- BMAD定义：客户管理+产品推荐+风控审批+客服工单4大功能模块
- Skill编写：信贷审批Skill、反洗钱Skill、客户画像Skill、客服话术Skill
- MCP接入：Tushare数据MCP、Excel MCP、Playwright爬虫MCP、Word/PPT MCP

## A2 — 未来触发场景

**应触发**：
- "我想给XX业务做一个AI系统，该怎么分工？"
- "AI项目里MCP/Skill/BMAD什么时候用哪个？"
- "怎么评估一个AI应用的架构是否完整？"
- "为什么我的AI agent做事碎片化？"
- "金融/教育/医疗等垂直行业的AI项目架构设计"

**不应触发**（诱饵）：
- 单纯问"MCP怎么配置" → 用mcp-three-layer-architecture
- 单纯问"Skill怎么写" → 用skill-prompt-rewrite
- 单纯问"BMAD五阶段是什么" → 用bmad-five-phases

## E — 可执行步骤

1. **识别业务问题**：写下要解决的1个核心业务问题（如"客户贷款审批慢"）
2. **BMAD拆功能**：列出3-5个具体功能点（如"征信查询、产品匹配、额度计算、预审报告"）
3. **Skill设计**：每个功能点设计1个Skill，定义输入/输出/决策逻辑
4. **MCP盘点**：列出每个Skill需要的外部数据/系统，匹配现成MCP或计划自研
5. **完整性体检**：问自己三层是否都有——有方法无知识？有知识无连接？缺哪层就补哪层

## B — 边界与盲点

**不适用**：
- 纯对话型应用（如客服问答机器人）不需要BMAD
- 纯模型推理任务（如情感分析API）不需要MCP
- 一次性脚本任务（如数据清洗）不需要三层架构

**作者盲点**：书中对"小项目是否也需要三层"讨论不足。实践中：
- 小工具：只需Skill
- 中型应用：Skill + MCP
- 企业级系统：MCP + Skill + BMAD 全套

## 相关 skills

- [meta-bmad-five-phases](../meta-bmad-five-phases/SKILL.md) — BMAD详细五阶段
- [meta-mcp-three-layer-architecture](../meta-mcp-three-layer-architecture/SKILL.md) — MCP三层详解
- [flow-skill-prompt-rewrite](../flow-skill-prompt-rewrite/SKILL.md) — Skill编写规范
