# GLOSSARY — 关键术语表

> 《智慧银行实验教程》蒸馏产物。收录13个skill涉及的核心术语。
> 每条记录：**术语 | 定义 | 来源章节 | 相关skill**

---

## A-B

### AI Skill（AI 技能）
- **定义**：用自然语言（通常Markdown）描述的"做什么、怎么做、何时做"流程文档，由大模型用推理能力执行。兼具专家系统的可解释性和机器学习的灵活性。
- **来源**：ch04 §4.1
- **相关**：[framework-knowledge-engineering-evolution](framework-knowledge-engineering-evolution/SKILL.md)、[flow-skill-prompt-rewrite](flow-skill-prompt-rewrite/SKILL.md)

### AI 协作四模式（IDE/Chat/Builder/SOLO）
- **定义**：按AI自主性↑、人类控制↓划分的四类人机协作模式。IDE（人在环里）→ Chat（人主导）→ Builder（AI主导）→ SOLO（AI自主）。
- **来源**：ch02 §2.5
- **相关**：[meta-ai-collaboration-four-modes](meta-ai-collaboration-four-modes/SKILL.md)

### AI 素养四维度（认知/操作/协作/创造）
- **定义**：AI素养的递进模型。认知（懂原理）→ 操作（会用工具）→ 协作（人机分工）→ 创造（AI原生成果）。前两维是门槛，后两维是金融人的差异化优势。
- **来源**：ch01 §1.5
- **相关**：[decision-ai-literacy-four-dimensions](decision-ai-literacy-four-dimensions/SKILL.md)

### BMAD（Breakthrough Method of Agile AI-Driven Development）
- **定义**：AI驱动的敏捷开发方法论。核心是"让AI扮演不同角色（Analyst/PM/Architect/Developer/QA）完成专业工作，人类负责决策与审核"。五阶段：B-M-A-D-V。
- **来源**：ch07 §7.1
- **相关**：[meta-bmad-five-phases](meta-bmad-five-phases/SKILL.md)、[meta-mcp-skill-bmad-trinity](meta-mcp-skill-bmad-trinity/SKILL.md)

---

## C-D

### 三位一体框架（MCP + Skill + BMAD）
- **定义**：AI赋能业务系统的三层架构。连接层（MCP，让AI有手脚）、知识层（Skill，让AI有专业脑）、方法层（BMAD，让AI有工作流）。
- **来源**：ch01 §1.4
- **相关**：[meta-mcp-skill-bmad-trinity](meta-mcp-skill-bmad-trinity/SKILL.md)

### 低代码高集成（中小银行AI路线）
- **定义**：中小金融机构上AI的差异化策略。不自研大模型（用开源/商用API），通过MCP高集成外部AI能力，聚焦1-2个垂直场景做深。
- **来源**：ch01 §1.2
- **相关**：[framework-finance-ai-application-matrix](framework-finance-ai-application-matrix/SKILL.md)

---

## F-H

### FinTech 1.0/2.0/3.0/4.0（金融科技四阶段）
- **定义**：金融科技演化的四阶段——信息化（1.0）、互联网化（2.0）、移动化（3.0）、智能化（4.0）。前三阶段是效率提升（量变），4.0是能力跃迁（质变）。
- **来源**：ch01 §1.1.1
- **相关**：[framework-fintech-four-stages](framework-fintech-four-stages/SKILL.md)

### F-N-F-T（选题四原则）
- **定义**：选题的四个否决式原则——Feasible（可行）、Novel（新颖）、Focused（聚焦）、Tech-adaptive（技术适配）。任何一条不过即淘汰。
- **来源**：ch12 §12.1.1
- **相关**：[decision-project-topic-four-principles](decision-project-topic-four-principles/SKILL.md)

---

## I-K

### JSON-RPC 生命周期（MCP的6步）
- **定义**：MCP协议下Host与Server的完整交互流程——initialize → tools/list → tools/call → 执行 → 结果返回 → AI整合。
- **来源**：ch03 §3.1
- **相关**：[meta-mcp-three-layer-architecture](meta-mcp-three-layer-architecture/SKILL.md)

### 知识工程三范式
- **定义**：人类沉淀专业知识的三种方式——专家系统（IF-THEN规则）、机器学习（数据训练权重）、AI Skill（自然语言流程+AI推理）。三者共存，各擅其场。
- **来源**：ch04 §4.2
- **相关**：[framework-knowledge-engineering-evolution](framework-knowledge-engineering-evolution/SKILL.md)

---

## M-P

### MCP（Model Context Protocol）
- **定义**：让AI模型与外部工具、数据源、API标准化通信的协议。三层架构（Host/Client/Server），把"人→工具"的传统调用变为"人→AI→工具"的中介层。N×M接入成本降为N+M。
- **来源**：ch03 §3.1
- **相关**：[meta-mcp-three-layer-architecture](meta-mcp-three-layer-architecture/SKILL.md)

### 6节点 Skill 流水线
- **定义**：金融实证研究的标准流程——文献 → 数据 → 清洗 → 回归 → 图表 → 论文。每节点封装为Skill，配合反馈环。
- **来源**：ch06 §6.1
- **相关**：[flow-six-node-skill-pipeline](flow-six-node-skill-pipeline/SKILL.md)

---

## R-T

### RTEII（提示词五原则）
- **定义**：好提示词的五要素——Role（角色）、Task（任务）、Environment/Example（环境/样例）、Input/Output（输入输出）、Iteration（迭代）。缺任何一项输出质量下降。
- **来源**：ch02 §2.5.6
- **相关**：[meta-rteii-prompt-principles](meta-rteii-prompt-principles/SKILL.md)

### Skill化提示词（10条改写原则）
- **定义**：把裸代码/裸指令升级为可复用Skill资产的10条规范。包括明示Skill名、写触发场景、声明输入输出、固化步骤、定义失败回退、给验收标准、避免hardcode、显式依赖、写边界、版本化。
- **来源**：ch06 §6.1.2
- **相关**：[flow-skill-prompt-rewrite](flow-skill-prompt-rewrite/SKILL.md)

### 三范式共存原则
- **定义**：专家系统、机器学习、AI Skill三种知识工程范式不是替代关系，而是按场景分工——硬合规用专家系统，数据驱动用ML，流程判断用Skill。
- **来源**：ch04 §4.2
- **相关**：[framework-knowledge-engineering-evolution](framework-knowledge-engineering-evolution/SKILL.md)

---

## X-Z

### 协作闭环（分析→生成→运行→调试）
- **定义**：AI协作的四步节奏感。每步有进入/退出条件，通常2-5轮收敛。原则：不跳步、不恋战（3轮无进展退回分析）、留痕迹。
- **来源**：ch02 §2.6.3
- **相关**：[flow-ai-collaboration-loop](flow-ai-collaboration-loop/SKILL.md)

### 质变论断（4.0 vs 前三阶段）
- **定义**：金融科技前三阶段（1.0-3.0）是效率革命（更快/更广/更便宜），4.0是能力革命（让人做不到的事变为可能）。判断标志：替代脑力、创造增量、离开AI不能运转。
- **来源**：ch01 §1.1.1
- **相关**：[framework-fintech-four-stages](framework-fintech-four-stages/SKILL.md)

### 中介层对比（人→AI→工具 vs 人→工具）
- **定义**：MCP带来的本质改变。传统API由人写死调用逻辑；MCP让AI根据语义自主决定调用什么工具、传什么参数。
- **来源**：ch03 §3.1
- **相关**：[meta-mcp-three-layer-architecture](meta-mcp-three-layer-architecture/SKILL.md)

---

## 附：缩写速查

| 缩写 | 全称 | 中文 |
|---|---|---|
| MCP | Model Context Protocol | 模型上下文协议 |
| BMAD | Breakthrough Method of Agile AI-Driven Development | AI驱动敏捷开发突破法 |
| RTEII | Role-Task-Env/Example-Input/Output-Iteration | 提示词五要素 |
| F-N-F-T | Feasible-Novel-Focused-Tech-adaptive | 选题四原则 |
| RPC | Remote Procedure Call | 远程过程调用 |
| MVP | Minimum Viable Product | 最小可行产品 |
| PRD | Product Requirements Document | 产品需求文档 |
| ROI | Return on Investment | 投资回报率 |
| RPA | Robotic Process Automation | 机器人流程自动化 |
| RegTech | Regulatory Technology | 监管科技 |
