# DIGEST — 《智慧银行实验教程》蒸馏总结

> 使用 cangjie-skill（RIA-TV++ 流水线）将一本 253 页的高校教材蒸馏为 13 个可执行 AI Skill。
> 完成日期：2026-07-19
> 来源：《智慧银行实验教程》（肖诗顺 著，四川农业大学）

---

## 一、来源信息

| 项目 | 内容 |
|---|---|
| **书名** | 智慧银行实验教程 |
| **作者** | 肖诗顺 |
| **单位** | 四川农业大学 经济学院 |
| **页数** | 约 253 页 |
| **结构** | 前言 + 8 章 + 附录，含 12 个实验 |
| **源格式** | LaTeX（`智慧银行实验教程chapters/` 目录） |
| **核心主题** | AI（MCP+Skill+BMAD）在金融业的实验性应用教学 |

---

## 二、蒸馏过程（7 阶段流水线）

| 阶段 | 动作 | 产出 | 状态 |
|---|---|---|---|
| **0. Adler 概览** | 通读全书，4步分析 | BOOK_OVERVIEW.md（154行） | ✅ |
| **1. 五类并行提取** | 框架/原则/案例/反例/术语 | candidates/（18个原始候选） | ✅ |
| **1.5 三重验证** | V1跨域+V2预测力+V3独创性 | verified.md（13通过+5淘汰） | ✅ |
| **2. RIA++构造** | R/I/A1/A2/E/B 六段式 | 13个SKILL.md | ✅ |
| **3. Zettelkasten链接** | 依赖图+术语关联 | INDEX.md + GLOSSARY.md | ✅ |
| **4. 压力测试** | 正例/反例/边界/综合 | test-prompts.json（52个用例） | ✅ |
| **5. 交付** | 总结+归档 | 本文件 DIGEST.md | ✅ |

---

## 三、13 个 Skill 清单

### A. 元方法类（5 个）—— 底层架构理解

| # | Skill | 核心解决 |
|---|---|---|
| 1 | meta-mcp-skill-bmad-trinity | AI项目的三层分工（连接/知识/方法） |
| 2 | meta-bmad-five-phases | AI驱动开发的五阶段工作流 |
| 3 | meta-ai-collaboration-four-modes | IDE/Chat/Builder/SOLO 模式选择 |
| 4 | meta-rteii-prompt-principles | 提示词五要素诊断（R-T-E-I-I） |
| 5 | meta-mcp-three-layer-architecture | MCP协议原理与生命周期 |

### B. 流程类（3 个）—— 执行层面的标准节奏

| # | Skill | 核心解决 |
|---|---|---|
| 6 | flow-ai-collaboration-loop | AI出错的四步闭环修复 |
| 7 | flow-six-node-skill-pipeline | 金融实证6节点流水线 |
| 8 | flow-skill-prompt-rewrite | Skill化的10条改写规范 |

### C. 决策与批判类（5 个）—— 判断与评估

| # | Skill | 核心解决 |
|---|---|---|
| 9 | framework-fintech-four-stages | 金融科技四阶段诊断 |
| 10 | decision-ai-literacy-four-dimensions | AI素养四维自评 |
| 11 | decision-project-topic-four-principles | 选题F-N-F-T否决式筛选 |
| 12 | framework-finance-ai-application-matrix | 金融AI应用5维度矩阵 |
| 13 | framework-knowledge-engineering-evolution | 知识工程三范式对比 |

---

## 四、Skill 间的核心叙事

这13个skill不是散点，而是一条完整的叙事链：

```
[我想上AI] → 评估能力(10) → 定位阶段(9) → 找切入点(12)
     → 设计架构(1) → 选协作模式(3) → 走开发流程(2)
     → 写提示词(4) → Skill化(8) → 执行出错修(6)
     → 做研究选题(11) → 走实证流水线(7)
     → 沉淀知识(13) → 接外部工具(5)
```

**三个核心叙事簇**：
1. **架构簇**（1, 2, 5）：理解AI系统的三层构成
2. **协作簇**（3, 4, 6, 8）：掌握人机协作的模式与节奏
3. **金融应用簇**（9, 11, 12, 7）：在金融场景落地（含研究方法论）

---

## 五、被淘汰的5个候选（审计轨迹）

| 候选 | 淘汰原因 | 去向 |
|---|---|---|
| Python环境四种配置 | V3不足（通用知识） | rejected/environment-python-setup.md |
| BMAD角色代号 | V3不足（开源项目设计） | rejected/bmad-role-names.md |
| 金融Python库全景 | V3不足（工具盘点非方法论） | rejected/python-library-list.md |
| MCP 30+服务器配置 | V3不足（技术参考） | rejected/mcp-config-list.md |
| 贪吃蛇实验代码 | V2不足（无独立方法论价值） | rejected/snake-game.md |

---

## 六、质量评估

### 优势
- **跨章节佐证强**：13个候选平均在2.4个章节独立出现，非孤例
- **预测力明确**：每个skill都能回答一类"未明说"的隐含问题
- **独创性达标**：核心论断（三层分工、四模式、质变论断等）非通用常识
- **RIA++结构完整**：每个skill都有R/I/A1/A2/E/B六段，可执行

### 不足与建议
1. **A1（书中案例）偏金融场景**：非金融领域用户共鸣度可能不足 → 后续可补充跨行业案例
2. **B（边界）部分依赖推断**：书中对部分边界讨论不足，由蒸馏过程补充 → 标记为"作者盲点"
3. **测试集以中文为主**：52个test case全中文 → 英文场景的触发准确率未验证
4. **Skill间触发可能冲突**：如"提示词"相关有2个skill（RTEII vs Skill化）→ 通过description里的"区别于"条款缓解

---

## 七、使用建议

### 对教师
- 作为《智慧银行实验教程》的配套教学包
- 13个skill对应教材核心知识点，可在每章开始时调用相应skill做导入

### 对学生
- 入门路径：先做 [AI素养四维自评](decision-ai-literacy-four-dimensions/SKILL.md)
- 实战路径：跟着 [6节点流水线](flow-six-node-skill-pipeline/SKILL.md) 做一次完整实证
- 毕设路径：[选题四原则](decision-project-topic-four-principles/SKILL.md) → [BMAD五阶段](meta-bmad-five-phases/SKILL.md)

### 对金融从业者
- 战略视角：[金融科技四阶段](framework-fintech-four-stages/SKILL.md) + [AI应用矩阵](framework-finance-ai-application-matrix/SKILL.md)
- 落地视角：[三位一体](meta-mcp-skill-bmad-trinity/SKILL.md) + [BMAD五阶段](meta-bmad-five-phases/SKILL.md)

### 对AI工具开发者
- 参考 [Skill化10条规范](flow-skill-prompt-rewrite/SKILL.md) 设计自己的Skill库
- 参考 [知识工程三范式](framework-knowledge-engineering-evolution/SKILL.md) 定位自己的产品

---

## 八、文件清单

```
smart-banking-tutorial/
├── DIGEST.md                          ← 本文件（项目总结）
├── BOOK_OVERVIEW.md                   ← 阶段0：全书Adler分析
├── verified.md                        ← 阶段1.5：13通过+5淘汰
├── INDEX.md                           ← 阶段3：13个skill导航
├── GLOSSARY.md                        ← 阶段3：关键术语表
├── test-prompts.json                  ← 阶段4：52个压力测试用例
├── candidates/                        ← 阶段1原始候选（审计）
├── rejected/                          ← 被淘汰候选（审计）
├── meta-mcp-skill-bmad-trinity/SKILL.md
├── meta-bmad-five-phases/SKILL.md
├── meta-ai-collaboration-four-modes/SKILL.md
├── meta-rteii-prompt-principles/SKILL.md
├── meta-mcp-three-layer-architecture/SKILL.md
├── flow-ai-collaboration-loop/SKILL.md
├── flow-six-node-skill-pipeline/SKILL.md
├── flow-skill-prompt-rewrite/SKILL.md
├── framework-fintech-four-stages/SKILL.md
├── decision-ai-literacy-four-dimensions/SKILL.md
├── decision-project-topic-four-principles/SKILL.md
├── framework-finance-ai-application-matrix/SKILL.md
└── framework-knowledge-engineering-evolution/SKILL.md
```

---

## 九、方法论致谢

本蒸馏使用 **cangjie-skill**（仓颉技能）的 RIA-TV++ 七阶段流水线：
- RIA++：Reading + Interpretation + Application（past + future trigger）+ Execution + Boundary
- TV：Triple Verification（V1跨域 + V2预测力 + V3独创性）
- Zettelkasten 链接 + 压力测试

cangjie-skill 源仓库：https://github.com/kangarooking/cangjie-skill

---

*蒸馏完成。13个skill可直接被AI agent调用，覆盖"学AI、用AI做项目、做金融研究、银行AI规划"四大典型场景。*
