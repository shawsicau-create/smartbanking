<div align="center">

# ABM Toolkit

> *「从研究问题到可运行仿真——跳过ODD协议和Mesa脚手架的200小时摸索期」*

[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-abm--toolkit-blueviolet)](SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Mesa 3.x](https://img.shields.io/badge/Mesa-3.x-blue)](https://mesa.readthedocs.io/)

**基于代理建模（ABM）的Agent副驾驶：帮你从研究问题走到可运行的仿真代码**

[看效果](#效果示例) · [什么时候用](#什么时候需要它) · [触发方式](#触发方式) · [它和同类有什么不同](#它和同类有什么不同) · [安全边界](#安全边界)

</div>

---

## 什么时候需要它

你正在做一个涉及**异质性主体交互**的研究问题——银行风险传染、农户参保决策、技术扩散、政策评估——传统计量模型假设同质性主体和线性关系，你试过CGE/DSGE但发现它们无法捕捉涌现行为。

你需要的是ABM（Agent-Based Modeling）。但ABM的起步门槛极高：ODD协议怎么写？Mesa怎么用？参数从哪来？网络结构选什么？敏感性分析怎么做？

这个Skill把这些问题的答案整合成一个模块化知识包，让Agent直接指导你从问题定义到可运行代码的全流程。

## 效果示例

```text
用户: 设计一个农业保险参保决策的ABM模型，500个农户，考虑补贴政策和邻里效应。

Agent: → 加载 modules/agricultural-insurance.md（前景理论框架+Logit投保决策模型）
       → 生成ODD协议草稿（Overview→Design Concepts→Details）
       → 生成Mesa 3.x代码（FarmerAgent + InsuranceCompany + Government）
       → 生成参数校准表（6个参数，每个标注来源）

参考完整实现: examples/insurance-adoption/
```

运行 `examples/insurance-adoption/run.py` 的真实输出：

```
[1/3] 单次运行 (补贴率=25%, 50步)...
  最终参保率: 71.0%
  最终违约率: 0.0%
  社会福利:   39,966,583

[2/3] 情景对比 (不同补贴率)...
           final_insure_rate_mean  final_insure_rate_std
无补贴 (0%)                    0.664               0.027
低补贴 (15%)                   0.710               0.016
中补贴 (25%)                   0.725               0.014
高补贴 (35%)                   0.725               0.014
```

## 快速开始

### 运行示例项目

```bash
cd examples/insurance-adoption
pip install -r requirements.txt
python run.py
```

### 在Agent中使用

装完Skill后对Agent说：

```text
帮我构建一个银行间市场风险传染的ABM模型，10家银行，核心-外围网络，生成ODD协议和Mesa代码。
```

## 触发方式

- "构建一个银行间市场风险传染的ABM模型"
- "设计一个农业保险参保决策的仿真"
- "用Mesa实现一个简单的市场ABM"
- "我的ABM模型跑完了，想做敏感性分析"
- "帮我写ODD协议"
- "农户行为怎么建模？前景理论的参数怎么设？"
- "模拟系统性风险在银行网络中的传播"

## 它和同类有什么不同

| 维度 | 普通做法 | 本 Skill |
|------|---------|----------|
| ODD协议 | 从零手写，容易漏项 | 完整模板 + 填写示例 |
| 代码起步 | 从Mesa文档学起 | 直接生成可运行的Mesa 3.x代码骨架 |
| 参数校准 | 参数凭直觉设 | 参数来源优先级表 + 校准方法模板 |
| 领域深度 | 通用ABM方法论 | 农业保险/金融风险垂直模块（前景理论、社会学习、CoVaR） |
| 文献支撑 | 自己搜索 | 58篇精选文献库（含被引>1000次的奠基论文） |
| 可验证产物 | 无 | 可运行示例 + test-prompts + 检查点设计 |

## 文件结构

```
abm-toolkit/
├── SKILL.md                    # 主入口（工作流 + 检查点 + 安全边界）
├── modules/
│   ├── core-framework.md       # 核心框架：ABM概念、ODD协议、校准方法
│   ├── economic-systems.md     # 经济系统：银行风险传染、市场动态
│   ├── agricultural-insurance.md # 农业保险：前景理论、农户行为建模
│   └── implementation.md       # 实现指南：Mesa/NetLogo/Repast4Py
├── references/
│   ├── patterns.md             # 建模模式库（状态机、BDI、学习主体）
│   ├── sharp_edges.md          # 常见陷阱（过度复杂、过拟合、样本量不足）
│   ├── validations.md          # 验证规则（守恒定律、涌现行为、统计显著性）
│   └── literature.md           # 文献库（58篇精选）
├── templates/
│   ├── odd-protocol.md         # ODD协议模板
│   └── code-templates.md       # 代码模板库
├── examples/
│   └── insurance-adoption/     # 可运行示例：农业保险参保决策ABM
├── test-prompts.json           # 测试prompt
└── LICENSE
```

## 验证与测试

3个测试prompt见 `test-prompts.json`，每个包含expected_behavior、checkpoint和pass_criteria。

验收prompt：

```text
帮我构建一个银行间市场风险传染的ABM模型，10家银行，核心-外围网络，生成ODD协议和Mesa代码骨架。
```

合格表现：输出包含完整ODD协议（≥6项）+ 可运行Python代码（import齐全，BankAgent含check_default和apply_shock方法）。

## 安全边界

- Agent **不会**自动执行 `pip install` 或修改Python环境
- Agent **不会**自动提交git或创建文件（除非明确要求）
- Agent **不会**硬编码真实个人数据
- 参数无来源时，Agent **会暂停**并提醒用户用本地数据替换
- 模型行为异常（NaN、负值）时，Agent **会暂停**报告问题

## 致谢

- ODD协议：Grimm, V., et al. (2006). *Ecological Modelling*, 198(1-2), 115-126.
- 前景理论：Tversky, A. & Kahneman, D. (1992). *Risk Analysis*, 13(2), 295-316.
- Mesa框架：https://github.com/projectmesa/mesa
- 经济金融ABM综述：Axtell, R.L. & Farmer, J.D. (2025). *JEL*, 63(1), 197-287.

## License

[MIT](LICENSE)

---

<div align="center">

*从问题到代码，从代码到论文——ABM建模全流程副驾驶*

</div>
