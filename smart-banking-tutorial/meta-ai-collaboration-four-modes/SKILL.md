---
name: meta-ai-collaboration-four-modes
description: 当用户面对"该用什么方式跟AI协作完成任务"这类模式选择问题，或在做项目时犹豫用IDE/Chat/Builder/SOLO哪种模式时使用。判断信号：用户提到"AI怎么用"、"哪种AI工具适合XX任务"、"Cursor/Claude/Devin怎么选"、"AI自主性该多高"、"AI协作模式"、规划AI使用策略、对AI工具选型困惑。区别于单纯讲某款工具的教程，本skill解决的是"四模式分工决策"的元问题。
---

# AI 协作四模式（IDE/Chat/Builder/SOLO）

## R — 原文引用

> "根据AI的自主性程度和与人类协作的紧密度，可以把AI协作模式分为四类：**IDE模式**（人在环里）、**Chat模式**（人主导对话）、**Builder模式**（AI主导执行）、**SOLO模式**（AI自主完成）。不同复杂度和风险等级的任务应选择不同模式。"
> — 《智慧银行实验教程》ch02 §2.5

## I — 方法论骨架

四模式按"AI自主性↑、人类控制↓"排列：

| 模式 | 自主性 | 人类角色 | 适用任务 | 风险等级 | 典型工具 |
|---|---|---|---|---|---|
| **IDE** | 低（人在环里） | 实时审阅每一行 | 写代码、改bug、精细操作 | 低 | Cursor、Windsurf |
| **Chat** | 中低（人主导） | 引导对话方向 | 头脑风暴、学习、分析 | 低 | ChatGPT、Claude对话 |
| **Builder** | 中高（AI主导） | 给目标+审结果 | 端到端开发、批量任务 | 中 | Devin、Lovable |
| **SOLO** | 高（AI自主） | 仅启动+收尾 | 重复性、探索性任务 | 高 | AutoGPT、BabyAGI |

**核心权衡公式**：
> 自主性 ↑ = 效率 ↑ × 不可控性 ↑
> 选择原则：**风险与自主性反向匹配**——高 stakes 用 IDE/Chat，低 stakes 用 Builder/SOLO。

## A1 — 书中案例

**银行CRM开发全周期**（ch07 §7.2）模式切换：
- **B-M阶段（发散构思+PRD）**：用Chat模式，让AI扮演Analyst/PM，多轮对话收敛需求
- **A阶段（架构设计）**：用IDE模式，人工精细打磨技术方案
- **D阶段（12个Sprint开发）**：用Builder模式，AI按Story端到端生成代码
- **V阶段（验证）**：用SOLO模式，独立Agent盲测，避免人类偏见

## A2 — 未来触发场景

**应触发**：
- "做XX任务该用哪种AI工具？"
- "AI的自主性该设多高？"
- "IDE/Chat/Builder/SOLO怎么选"
- "为什么我的AI agent老是跑偏"
- "高风险任务（如金融、医疗）怎么用AI"
- "批量任务该怎么分配给AI"

**不应触发**（诱饵）：
- 单纯问"Cursor怎么用" → 工具教程
- 单纯问"什么是AI agent" → 概念解释
- 单纯问"怎么写好的提示词" → 用meta-rteii-prompt-principles

## E — 可执行步骤

1. **评估任务风险等级**：问自己"AI搞砸了最坏什么后果？"——生命/资金/合规=高风险；效率/美观=低风险
2. **评估任务复杂度**：单步操作=简单；多步链式=复杂
3. **查决策矩阵**：
   - 低风险+简单 → IDE（边做边看）
   - 低风险+复杂 → Builder（放手让AI干）
   - 高风险+简单 → Chat（先讨论再动手）
   - 高风险+复杂 → IDE+Chat 混合（每步都审）
4. **设置检查点**：无论选哪种，每30-60分钟必须有1次人类审阅节点
5. **失败回退策略**：AI连续3次出错 → 立即降级到更低自主性模式

## B — 边界与盲点

**不适用**：
- 需要人类创意/判断的任务（如战略决策、伦理判断）——任何模式都只是辅助
- 涉及隐私敏感数据的任务——SOLO模式绝对禁用（AI可能外传）

**作者盲点**：书中对"SOLO模式的失败处理"讨论不足。实践中：
- SOLO任务必须设硬性时间盒（最多2小时）
- SOLO任务必须有可量化的成功标准（否则AI会"自圆其说"）
- SOLO任务产出必须经过IDE/Chat模式的二次复核

## 相关 skills

- [meta-rteii-prompt-principles](../meta-rteii-prompt-principles/SKILL.md) — 每种模式都要用的提示词原则
- [meta-bmad-five-phases](../meta-bmad-five-phases/SKILL.md) — BMAD各阶段的模式选择
- [flow-ai-collaboration-loop](../flow-ai-collaboration-loop/SKILL.md) — AI出错时的闭环修复
