---
name: meta-bmad-five-phases
description: 当用户要用AI驱动开发一个中小型软件项目（MVP/原型/教学实验/个人项目），需要从模糊想法到可运行代码的端到端工作流时使用。判断信号：用户提到"做XX系统"、"开发XX原型"、"AI写代码"、"BMAD"、"PRD"、"Sprint"、"我有个想法想做出来"、需要从需求到交付全流程、对1人+AI完成项目感兴趣。区别于传统敏捷/Scrum方法论skill，本skill强调AI扮演多角色的BMAD专属范式。
---

# BMAD 五阶段方法论（B-M-A-D-V）

## R — 原文引用

> "BMAD（Breakthrough Method of Agile AI-Driven Development）是一种AI驱动的敏捷开发方法论，其核心理念是：**让AI扮演不同角色完成专业工作，人类负责决策与审核**。这种方法将程序员的定位从'代码编写者'提升为'AI团队管理者'。"
> — 《智慧银行实验教程》ch07 §7.1

## I — 方法论骨架

五阶段顺序推进，每阶段AI扮演一个角色：

| 字母 | 阶段 | AI角色 | 产出物 | 输出目录 |
|---|---|---|---|---|
| **B**rainstorm | 分析/构思 | Analyst（Mary） | 10-20个创意 | `_bmad-output/brainstorming/` |
| **M**odel | 规划/设计 | PM（John） | PRD（含FR-1等功能编号） | `_bmad-output/planning-artifacts/prd.md` |
| **A**rchitect | 方案细化 | Architect（Winston）+UX（Sally） | architecture.md + Epic/Story拆分 | `_bmad-output/` |
| **D**evelop | 实施/交付 | Developer（Amelia） | 可运行代码（红-绿-重构） | 源码仓库 |
| **V**erify | 验证/反馈 | QA | 三层对抗式审查报告 | sprint-status.yaml |

**关键节奏**：
- B-M阶段用Chat模式（发散）
- A-D阶段用Builder模式（执行）
- V阶段用SOLO或独立Agent（盲测）
- 每个Sprint闭环反馈下一个B

## A1 — 书中案例

**银行CRM系统12个实验**（ch07 §7.2）：
- B阶段：脑暴20+功能点，收敛到4大模块
- M阶段：写PRD含FR-1到FR-28功能需求
- A阶段：技术选型Flask+SQLite，拆分6个Epic
- D阶段：12个Sprint迭代开发，每Sprint完成1-3个Story
- V阶段：盲点猎人+边界猎人+验收审计三层审查

## A2 — 未来触发场景

**应触发**：
- "我想用AI做一个XX系统/MVP/原型"
- "BMAD五阶段怎么走？"
- "AI写代码的完整流程是什么？"
- "从需求到部署的AI驱动开发"
- "1个人+AI完成项目的方法"
- "PRD/Epic/Story/Sprint在AI开发中怎么用"

**不应触发**（诱饵）：
- "传统敏捷Scrum怎么做" → 通用Scrum指南
- "PRD模板" → 通用PRD写作
- "怎么写单元测试" → TDD方法论

## E — 可执行步骤

1. **B阶段（脑暴，30-60分钟）**：在AI IDE的Chat模式描述业务背景和目标用户，让AI扮演Analyst，使用"脑倾泻"+逆向思维+跨领域类比，产出10-20个创意，保存到`_bmad-output/brainstorming/ideas.md`
2. **M阶段（PRD，60-90分钟）**：切换到AI以PM身份对话，逐节讨论：产品愿景、目标用户、核心功能（按优先级P0/P1/P2）、用户旅程、非功能需求、KPI。每个需求编FR-N号，产出`prd.md`
3. **A阶段（架构+Epic，60分钟）**：AI扮演Architect讨论技术选型（框架/数据库/部署），再拆分PRD→Epic→Story→Task。每个Story用"As a... I want... So that..."格式，验收标准用Given/When/Then
4. **D阶段（开发，2小时-数天）**：AI生成`sprint-status.yaml`跟踪状态（backlog→ready-for-dev→in-progress→review→done），按"红-绿-重构"TDD循环逐Story实施
5. **V阶段（验证，1-2小时）**：三层对抗式审查——盲点猎人（找bug）+边界猎人（遍历边界）+验收审计（对照标准）。问题按Critical/High/Medium/Low分级
6. **闭环反馈**：把V阶段发现的问题作为下一个B阶段的输入

## B — 边界与盲点

**适合**：
- 中小型项目原型开发（<4周）
- MVP验证（能否1周出最小可用版本）
- 教学实验、个人项目、技术方案可行性验证

**不适合**：
- 高安全要求的核心银行系统（需严格审计）
- 大型团队协作（需成熟项目管理）
- 可靠性极高的生产系统（如交易、支付）

**作者盲点**：从MVP到生产级系统的迁移路径未充分讨论。实践中需要补充：
- 代码审计与重构
- 安全加固（鉴权、加密、审计日志）
- 性能优化（数据库索引、缓存、限流）
- 监控告警（APM、日志聚合、健康检查）

## 相关 skills

- [meta-mcp-skill-bmad-trinity](../meta-mcp-skill-bmad-trinity/SKILL.md) — BMAD在三位一体中的定位
- [decision-project-topic-four-principles](../decision-project-topic-four-principles/SKILL.md) — B阶段前的选题决策
- [meta-ai-collaboration-four-modes](../meta-ai-collaboration-four-modes/SKILL.md) — 各阶段该用哪种AI模式
