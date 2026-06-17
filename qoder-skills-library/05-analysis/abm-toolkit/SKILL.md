---
name: abm-toolkit
description: "ABM建模副驾驶：从ODD协议到Mesa 3.x代码生成、参数校准、敏感性分析全流程"
argument-hint: "<研究问题描述，如：农业保险参保决策ABM，500个农户>"
negative_triggers:
  - 均衡分析 → 用DSGE或CGE模型
  - 因果识别 → 用计量回归或IV
  - 纯静态比较 → 用系统动力学
workflow_stage: analysis
compatibility:
  - claude-code
  - cursor
  - codex
  - gemini-cli
author: Qoder Skills Library
version: 3.0.0
tags:
  - abm
  - agent-based-modeling
  - simulation
  - economics
  - python
---

# ABM Toolkit - 统一基于代理建模技能包

## Purpose

本技能包提供统一的基于代理建模（Agent-Based Modeling, ABM）框架，支持经济系统仿真、农业保险建模等多种应用场景。采用模块化设计，用户可按需加载相关模块。

**核心价值**：
- 统一的ABM理论框架和方法论
- 可复用的代码模板和建模模式
- 领域特定的扩展模块（经济系统、农业保险等）
- 完整的文献库和参考资源

## When to Use

- 需要构建基于代理的模型模拟复杂系统
- 研究个体交互产生的涌现行为
- 进行政策评估和情景分析
- 涉及银行风险、市场动态、农业保险等领域

**触发关键词**：ABM、agent-based、multi-agent、涌现行为、社会仿真、系统仿真、Mesa、NetLogo

**不适用场景**：均衡分析（用DSGE/CGE）、因果识别（用计量回归）、纯静态比较（用系统动力学）

## Architecture

### 模块化架构

```
abm-toolkit/
├── SKILL.md                    # 本文件（主入口）
├── modules/                    # 功能模块
│   ├── core-framework.md       # 核心框架（必读）
│   ├── economic-systems.md     # 经济系统模块
│   ├── agricultural-insurance.md # 农业保险模块
│   └── implementation.md       # 实现指南
├── references/                 # 参考资源
│   ├── patterns.md             # 建模模式库
│   ├── sharp_edges.md          # 常见陷阱
│   ├── validations.md          # 验证规则
│   └── literature.md           # 文献库
├── templates/                  # 模板库
│   ├── odd-protocol.md         # ODD协议模板
│   └── code-templates.md       # 代码模板
└── examples/                   # 示例项目
```

### 模块加载策略

1. **核心框架**（必读）：`modules/core-framework.md` - ABM基础理论和通用方法
2. **领域模块**（按需）：
   - 经济系统研究 → `modules/economic-systems.md`
   - 农业保险研究 → `modules/agricultural-insurance.md`
3. **实现指南**（编码时）：`modules/implementation.md` - 技术栈和代码实现

## Quick Start

### 5分钟快速入门

1. **阅读核心框架**：了解ABM基本概念和ODD协议
2. **选择领域模块**：根据研究问题选择对应模块
3. **使用模板**：从 `templates/` 获取ODD协议和代码模板
4. **参考示例**：查看 `examples/` 中的案例

### 标准工作流程

```
问题定义 → 主体设计 → 环境构建 → 交互规则 → 仿真实验 → 结果分析
    ↓           ↓           ↓           ↓           ↓           ↓
 ODD协议    Agent类    空间/网络   行为方程    参数校准    可视化
```

## Modules

### 核心框架（必读）

**文件**：`modules/core-framework.md`

**内容**：
- ABM基本概念和原理
- ODD协议（Overview, Design concepts, Details）
- 主体设计模式
- 网络结构选择
- 参数校准方法
- 模型验证流程

**适用场景**：所有ABM项目的基础

### 经济系统模块

**文件**：`modules/economic-systems.md`

**内容**：
- 银行风险传染建模
- 市场动态仿真
- 政策评估框架
- 金融网络分析

**适用场景**：金融、银行、市场等经济系统研究

### 农业保险模块

**文件**：`modules/agricultural-insurance.md`

**内容**：
- 农业保险ABM框架
- 农户行为建模（前景理论、社会学习）
- 保险产品设计
- 政策情景分析
- 核心文献库（20篇精选）

**适用场景**：农业保险、农村金融、政策仿真

### 实现指南

**文件**：`modules/implementation.md`

**内容**：
- Python/Mesa实现模板
- NetLogo实现指南
- Repast4Py高性能方案
- 代码模板库

**适用场景**：编码实现阶段

## Workflow

### 阶段1：问题定义（1-2天）

1. 明确研究问题
2. 评估ABM适用性
3. 填写ODD协议概述部分

**输出**：研究问题文档、ODD协议草稿

### 阶段2：模型设计（3-5天）

1. 设计主体类型和属性
2. 定义行为空间和决策规则
3. 选择网络/空间结构
4. 确定交互机制

**输出**：完整的ODD协议、UML类图

### 阶段3：编码实现（1-2周）

1. 选择技术栈（Mesa/NetLogo/Repast4Py）
2. 实现主体类和环境
3. 编写调度器和数据收集器
4. 单元测试

**输出**：可运行的ABM代码

### 阶段4：实验运行（3-5天）

1. 参数校准
2. 基准情景运行
3. 敏感性分析
4. 政策情景模拟

**输出**：实验数据、统计结果

### 阶段5：结果分析（3-5天）

1. 生成可视化图表
2. 机制分解和解释
3. 稳健性检验
4. 撰写分析报告

**输出**：分析报告、图表、论文草稿

## Checkpoints

ABM建模是高风险工作流——模型设计错了会浪费数周。以下检查点**必须暂停并等用户确认**后再继续：

| 检查点 | 触发时机 | 暂停动作 | 通过条件 |
|-------|---------|---------|----------|
| **CP1: ODD协议审核** | 阶段1完成后 | 展示ODD协议草稿，询问"主体类型和行为规则是否需要调整？" | 用户确认或修改后 |
| **CP2: 参数来源确认** | 阶段4参数校准前 | 展示参数校准表，提醒"以下参数为默认值（来自文献），建议用本地调查数据替换。" | 每个参数标注来源 ||
| **CP3: 基准情景验证** | 阶段4基准运行后 | 检查模型行为是否合理（如参保率是否在0-100%之间，无负值） | Face Validation通过 |
| **CP4: 结果可信度** | 阶段5稳健性检验后 | 展示敏感性分析结果，确认定性结论不变 | CV<0.1且参数±20%扰动后结论一致 |

**Agent行为约束**：
- 遇到参数无明确来源时，必须暂停并提醒用户
- 生成的代码必须能在 `pip install "mesa>=3.0" numpy pandas matplotlib` 后直接运行
- 不要自动 `pip install`，只生成代码和依赖列表

## Safety Boundaries

**Agent不会做的事**：
- 不会自动执行 `pip install` 或修改用户Python环境
- 不会自动提交git或创建文件（除非用户明确要求）
- 不会删除已有模型代码或数据文件
- 不会调用外部API或发送网络请求
- 不会硬编码真实个人数据（如真实农户姓名、真实银行名称）

**Agent会停下来问用户的情况**：
- 参数无来源且无法从文献推导时
- 模型行为不合理（如出现NaN、负值参保率）时
- 用户要求超出ABM适用范围的均衡分析或因果识别时
- 代码模板无法直接满足用户特殊需求，需要定制时

## Requirements

### 软件环境

- **Python**：3.8+（推荐3.10+）
- **Jupyter Notebook**：可选，用于交互式分析

### 核心依赖

```bash
pip install mesa numpy networkx matplotlib seaborn pandas scipy
```

### 可选依赖

```bash
# 高性能计算
pip install mesa-geo repast4py mpi4py

# 统计分析
pip install statsmodels scikit-learn

# 数据处理
pip install geopandas shapely
```

## Best Practices

### 模型设计

1. **从简单开始**：先实现最小可行模型，再逐步扩展
2. **文档先行**：使用ODD协议完整记录模型设计
3. **模块化代码**：主体、环境、调度器分离

### 参数校准

1. **数据驱动**：优先使用实证数据校准参数
2. **文献支撑**：理论参数引用权威文献
3. **敏感性测试**：关键参数±20%扰动检验

### 验证流程

1. **Face Validation**：专家评审模型行为合理性
2. **Historical Validation**：与历史数据对比
3. **Cross-Validation**：与其他模型结果对比

### 代码质量

1. **版本控制**：使用Git管理代码版本
2. **单元测试**：核心函数编写测试用例
3. **代码审查**：同行评审代码逻辑

## Common Pitfalls

### 模型设计

- ❌ **过度复杂**：初始模型包含过多主体类型和规则
- ❌ **缺乏文档**：模型设计未使用ODD协议记录
- ❌ **忽视验证**：未进行模型验证就进行政策分析

### 参数设置

- ❌ **随意设定**：参数无明确来源和依据
- ❌ **过度拟合**：参数校准过度拟合特定数据集
- ❌ **忽视敏感性**：未检验参数变化对结果的影响

### 实验设计

- ❌ **单一情景**：只运行基准情景，缺乏对比分析
- ❌ **随机种子**：未控制随机性，结果不可复现
- ❌ **样本量不足**：运行次数过少，结果缺乏统计意义

## Example Prompts

### 通用ABM

- "构建一个银行间市场风险传染的ABM模型"
- "设计一个产品扩散的社会仿真模型"
- "用Mesa实现一个简单的市场ABM"

### 经济系统

- "模拟系统性风险在银行网络中的传播"
- "评估不同货币政策对市场稳定性的影响"
- "分析投资者情绪对资产价格的影响"

### 农业保险

- "设计一个农业保险参保决策的ABM模型"
- "模拟补贴政策对农户投保行为的影响"
- "分析气候风险对农业保险市场的影响"

## References

### 核心资源

- **共享代码库**：`references/code-snippets.md`（BaseAgent、校准、敏感性分析、可视化等）
- **建模模式库**：`references/patterns.md`
- **常见陷阱**：`references/sharp_edges.md`
- **验证规则**：`references/validations.md`
- **文献库**：`references/literature.md`（58篇精选，含被引>1000次的奠基论文）

### 可运行示例

- **农业保险参保决策ABM**：`examples/insurance-adoption/`（Mesa 3.x，前景理论+社会学习，可一键运行）

### 外部资源

- **Mesa文档**：https://mesa.readthedocs.io/
- **NetLogo文档**：https://ccl.northwestern.edu/netlogo/docs/
- **ABM维基**：https://en.wikipedia.org/wiki/Agent-based_model

## Changelog

### v3.0.0 (2026-06-14)

- **Mesa 3.x 全面迁移**：所有模板和模块更新至 Mesa 3.x API（Agent无unique_id、AgentSet调度、SolaraViz）
- **代码去重**：新建 `references/code-snippets.md` 作为共享代码单一来源
- **Bayesian calibration 修复**：ABM不可微分，改用ABC（近似贝叶斯计算）方法
- **validations.md 适配**：`validate_agent_definition()` 不再强制 perceive/decide/act
- **SKILL.md frontmatter 优化**：单行 description + argument-hint
- **hanyuan-pepper-insurance 示例**：迁移到 Mesa 3.x API

### v2.1.0 (2026-06-14)

- 新增 `examples/insurance-adoption/` 可运行Mesa 3.x项目（前景理论+社会学习）
- 新增 Checkpoints（4个检查点）和 Safety Boundaries 节
- 新增 `test-prompts.json`（3个典型测试prompt）
- 修复代码模板bug：PyMC sd→sigma、pymc3→pymc、param_names未定义、CoVaR空壳函数
- 更新Frontmatter：场景触发导向description + negative_triggers
- 新增 LICENSE (MIT)

### v2.0.0 (2026-06-14)

- 统一三个ABM技能为模块化技能包
- 新增核心框架、经济系统、农业保险模块
- 整合文献库和代码模板
- 优化目录结构和文档组织

### v1.0.0

- 初始版本，包含基础ABM功能
