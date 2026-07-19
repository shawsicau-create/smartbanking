# INDEX — 13 个 Skill 导航索引

> 《智慧银行实验教程》蒸馏产物。按"学习路径 + 使用场景"双视角组织。
> 每条记录：**名称 | 一句话用途 | 前置依赖 | 触发信号**

---

## 一、按类别分组

### A. 元方法类（Meta，5 个）—— 理解"AI+金融"的底层架构

| # | Skill | 一句话用途 | 前置 | 触发信号 |
|---|---|---|---|---|
| 1 | [meta-mcp-skill-bmad-trinity](meta-mcp-skill-bmad-trinity/SKILL.md) | AI项目的三层架构分工 | 无 | "AI赋能XX业务"、"MCP/Skill/BMAD怎么配合" |
| 2 | [meta-bmad-five-phases](meta-bmad-five-phases/SKILL.md) | AI驱动开发的五阶段工作流 | 1 | "用AI做XX系统"、"BMAD"、"从想法到代码" |
| 3 | [meta-ai-collaboration-four-modes](meta-ai-collaboration-four-modes/SKILL.md) | 选择IDE/Chat/Builder/SOLO | 无 | "AI怎么用"、"哪种工具适合XX" |
| 4 | [meta-rteii-prompt-principles](meta-rteii-prompt-principles/SKILL.md) | 写/改提示词的五要素诊断 | 无 | "提示词不好"、"AI不听话" |
| 5 | [meta-mcp-three-layer-architecture](meta-mcp-three-layer-architecture/SKILL.md) | MCP协议原理与生命周期 | 1 | "MCP是什么"、"AI怎么接工具" |

### B. 流程类（Flow，3 个）—— 执行层面的标准节奏

| # | Skill | 一句话用途 | 前置 | 触发信号 |
|---|---|---|---|---|
| 6 | [flow-ai-collaboration-loop](flow-ai-collaboration-loop/SKILL.md) | AI出错的四步闭环修复 | 4 | "AI错了"、"怎么来回改" |
| 7 | [flow-six-node-skill-pipeline](flow-six-node-skill-pipeline/SKILL.md) | 金融实证6节点流水线 | 4, 5 | "实证怎么做"、"数据到论文" |
| 8 | [flow-skill-prompt-rewrite](flow-skill-prompt-rewrite/SKILL.md) | 把裸指令Skill化的10条规范 | 4 | "改成Skill"、"标准化提示词" |

### C. 决策与批判类（Decision & Critique，5 个）—— 判断与评估的框架

| # | Skill | 一句话用途 | 前置 | 触发信号 |
|---|---|---|---|---|
| 9 | [framework-fintech-four-stages](framework-fintech-four-stages/SKILL.md) | 金融科技四阶段诊断 | 无 | "金融科技发展"、"FinTech X.0" |
| 10 | [decision-ai-literacy-four-dimensions](decision-ai-literacy-four-dimensions/SKILL.md) | AI素养四维度自评 | 无 | "AI素养"、"我怎么学AI" |
| 11 | [decision-project-topic-four-principles](decision-project-topic-four-principles/SKILL.md) | 选题F-N-F-T四原则 | 10 | "选题"、"这个题行不行" |
| 12 | [framework-finance-ai-application-matrix](framework-finance-ai-application-matrix/SKILL.md) | 金融AI应用5维度矩阵 | 9 | "银行该用AI做什么" |
| 13 | [framework-knowledge-engineering-evolution](framework-knowledge-engineering-evolution/SKILL.md) | 知识工程三范式对比 | 无 | "为什么用Skill"、"规则vs模型" |

---

## 二、按典型场景推荐

### 场景 1：我想学AI但不知从哪入手
→ 先做 [10. AI素养四维自评](decision-ai-literacy-four-dimensions/SKILL.md)，找最短板，再针对性学。

### 场景 2：我要用AI做一个项目/MVP
→ 先选模式 [3. 四模式](meta-ai-collaboration-four-modes/SKILL.md) → 走 [2. BMAD五阶段](meta-bmad-five-phases/SKILL.md) → 出错时用 [6. 协作闭环](flow-ai-collaboration-loop/SKILL.md)。

### 场景 3：我要做金融实证研究/论文
→ 先 [11. 选题四原则](decision-project-topic-four-principles/SKILL.md) → 走 [7. 6节点流水线](flow-six-node-skill-pipeline/SKILL.md) → 每个节点用 [8. Skill化提示词](flow-skill-prompt-rewrite/SKILL.md) 标准化。

### 场景 4：我提示词写得不好
→ 用 [4. RTEII五原则](meta-rteii-prompt-principles/SKILL.md) 诊断 → 升级为Skill用 [8. Skill化](flow-skill-prompt-rewrite/SKILL.md)。

### 场景 5：我要给银行做AI规划
→ 先看 [9. 金融科技四阶段](framework-fintech-four-stages/SKILL.md) 定位 → 再画 [12. AI应用矩阵](framework-finance-ai-application-matrix/SKILL.md) 找盲区 → 用 [1. 三位一体](meta-mcp-skill-bmad-trinity/SKILL.md) 设计架构。

### 场景 6：我组织要沉淀专家知识
→ 用 [13. 知识工程三范式](framework-knowledge-engineering-evolution/SKILL.md) 分类 → 对Skill类知识用 [8. Skill化](flow-skill-prompt-rewrite/SKILL.md) 编码。

### 场景 7：我要给AI接入外部工具/数据
→ 理解 [5. MCP三层架构](meta-mcp-three-layer-architecture/SKILL.md) → 在 [1. 三位一体](meta-mcp-skill-bmad-trinity/SKILL.md) 框架下定位连接层。

---

## 三、Skill 间依赖图（Zettelkasten 链接）

```
                     [10. AI素养四维] ───→ [11. 选题四原则]
                                              │
                                              ▼
[1. 三位一体] ←──→ [2. BMAD五阶段] ←──→ [7. 6节点流水线]
       │                │                      │
       │                ▼                      ▼
       │          [3. 四模式]            [8. Skill化]
       │                │                      │
       ▼                ▼                      ▲
[5. MCP三层]      [6. 协作闭环] ──→ [4. RTEII五原则] ─┘
       │
       ▼
[13. 知识工程三范式]

[9. 金融科技四阶段] ──→ [12. AI应用矩阵]
```

**强连接对**（高频共现）：
- 1 ↔ 2 ↔ 5（三位一体的三个组件互依）
- 4 ↔ 8（提示词原则 → Skill化规范）
- 7 ↔ 11（实证流水线服务选题）
- 9 ↔ 12（阶段定位 → 应用矩阵诊断）

**弱连接对**（偶尔会引用）：
- 10 → 11（能力评估指导选题可行性）
- 13 → 8（知识工程视角看Skill定位）
- 3 → 2（四模式在BMAD各阶段切换）

---

## 四、阅读建议

### 入门路径（3小时，建立全局观）
1 → 9 → 10 → 4（先理解"是什么、自己在哪、怎么做"）

### 实战路径（1周，开始动手）
3 → 4 → 8 → 6 → 2（从选模式到完成第一个项目）

### 深度路径（1月，体系化）
全部13个按依赖图顺序学习 + 做3个综合练习项目
