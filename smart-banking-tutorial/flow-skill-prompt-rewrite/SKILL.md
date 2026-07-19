---
name: flow-skill-prompt-rewrite
description: 当用户需要把一段裸代码/裸指令/裸Stata或Python脚本改写为"Skill化提示词"时使用。判断信号：用户提到"Skill化"、"把代码封装成Skill"、"标准化提示词"、"改写prompt"、"Skill模板"、有现成代码想变成可复用Skill、设计Skill库、抱怨提示词不可复用。区别于meta-rteii-prompt-principles（讲五要素诊断），本skill提供的是"把粗糙指令升级为Skill资产"的10条具体改写规范。
---

# Skill化提示词 10 条改写原则

## R — 原文引用

> "Skill不是普通的提示词，而是**可复用、可组合、可迭代的提示词资产**。把一段裸代码或自然语言指令升级为Skill，需要遵循10条改写原则。这10条原则的目标是：让Skill像函数一样有明确的接口、像文档一样有说明、像测试一样有验收标准。"
> — 《智慧银行实验教程》ch06 §6.1.2

## I — 方法论骨架

### Skill化提示词的标准化模板

```markdown
---
name: <skill-name>
description: <触发场景 + 判断信号 + 与同类skill的区别>
---

# <Skill标题>

## 输入
- input1: <类型> - <说明>
- input2: <类型> - <说明>

## 输出
- output1: <类型> - <说明>

## 执行步骤
1. ...
2. ...

## 失败回退
- 如果<情况A>，则<动作B>

## 验收标准
- <可量化标准1>
- <可量化标准2>
```

### 10条改写原则

| # | 原则 | 改写前 | 改写后 |
|---|---|---|---|
| 1 | **明示Skill名** | "帮我跑个回归" | `name: ols-regression` |
| 2 | **写触发场景** | （无） | "当用户要做线性回归时使用，信号：提到OLS、系数、显著" |
| 3 | **声明输入输出** | "给数据出结果" | "输入：DataFrame；输出：RegressionResults对象+摘要表" |
| 4 | **固化执行步骤** | "你看着办" | "1.检查缺失值 2.设定模型 3.拟合 4.输出摘要" |
| 5 | **定义失败回退** | （无） | "若共线性VIF>10，自动转为岭回归并提示" |
| 6 | **给验收标准** | "差不多就行" | "R²、系数、p值、F统计量齐全且可解析" |
| 7 | **避免hardcode** | "茅台股票代码600519" | "ticker: <参数>" |
| 8 | **显式Skill间依赖** | （隐式） | "依赖：tushare-data-skill（先拉数据）" |
| 9 | **写明不适用边界** | （无） | "不适用：时间序列（用ARIMA-skill）；logit（用logit-skill）" |
| 10 | **版本化** | （无） | "version: 1.2，更新：加了异方差稳健标准误" |

## A1 — 书中案例

**Stata回归脚本Skill化**（ch06 §6.1.2）：

改写前（裸Stata代码）：
```stata
use bank_data.dta, clear
reg risk taking ls pr, robust
```

改写后（Skill化提示词）：
```markdown
---
name: ols-bank-risk-regression
description: 当用户研究银行风险承担的影响因素时使用。信号：提到"银行风险"、"风险承担"、"影响因素回归"。
---

## 输入
- data: Stata/CSV格式的面板数据，必须含银行id、年份、风险指标、解释变量

## 输出
- reg_result: 回归结果表（系数、标准误、p值、R²）
- interpretation: 一段对系数方向和显著性的自然语言解读

## 执行步骤
1. 检查缺失值和异常值，报告缺失比例
2. 设定模型：Y=风险指标，X=核心解释变量，控制变量=规模、ROA、资本充足率
3. 拟合（双向固定效应：银行+年份），用稳健标准误
4. 输出结果表 + 解读

## 失败回退
- 若核心变量VIF>10 → 提示共线性，建议剔除某控制变量
- 若样本<30 → 提示样本不足，建议扩大时间窗

## 验收标准
- 结果表含N、R²、F、所有系数和p值
- 解读必须说明"系数方向是否和理论预期一致"
```

## A2 — 未来触发场景

**应触发**：
- "把这段代码/指令改成Skill"
- "怎么写可复用的提示词"
- "Skill化改写规范"
- "我的提示词每次都要重写怎么办"
- "怎么建Skill库"
- "标准化提示词模板"

**不应触发**（诱饵）：
- 单纯问"提示词五要素" → 用meta-rteii-prompt-principles
- 单纯问"某段代码怎么写" → 具体编码问题
- 问"Skill是什么概念" → 概念解释

## E — 可执行步骤

1. **找原始素材**：把你要Skill化的裸代码/指令/过往的prompt找出来
2. **套模板**：复制上面的标准化模板框架
3. **逐条对照10原则**：每条原则问自己"这条做到了吗？"——做不到就补
4. **命名规范**：用 `<类别>-<动作>-<对象>` 格式（如 `data-fetch-stock`、`regression-panel-fe`）
5. **写description要狠**：description决定Skill能否被正确触发——要写清"什么场景触发"+"什么场景不触发"
6. **跑3个测试用例**：用不同的输入跑Skill，看输出是否稳定、验收标准是否都满足
7. **归档版本**：在Skill末尾记 `version: 1.0`，后续每次大改升版本号

## B — 边界与盲点

**不适用**：
- 一次性任务（如"帮我把这3个数字加起来"）——Skill化收益小于成本
- 高度创意的任务（如"写一首诗"）——无法标准化输入输出
- 探索性分析（每次都不一样）——Skill会束缚探索

**作者盲点**：书中对"Skill库的治理"讨论不足。实践中：
- Skill多了会冲突（两个Skill都声称处理"回归"）——需要建索引 + description里明确区分
- Skill会过时（API变了、数据源变了）——需要定期 review，半年一次大扫除
- 团队协作时Skill要进版本控制（Git），不要散落在个人本地

## 相关 skills

- [meta-rteii-prompt-principles](../meta-rteii-prompt-principles/SKILL.md) — Skill化是RTEII的极致形态
- [flow-six-node-skill-pipeline](../flow-six-node-skill-pipeline/SKILL.md) — 每个节点都是由Skill化提示词组成
- [meta-mcp-skill-bmad-trinity](../meta-mcp-skill-bmad-trinity/SKILL.md) — Skill在三位一体中的知识层定位
