# 农业保险ABM模块

## Purpose

本模块提供农业保险ABM的专项框架，支持从研究问题发现、模型设计、Python建模到政策分析的完整工作流。专为农村金融、农业保险、政策仿真等领域设计。

---

## 1. 农业保险ABM框架

### 1.1 主体类型

| 主体类型 | 属性 | 行为 | 数量 |
|---------|------|------|------|
| 农户（Farmer） | 海拔、土地规模、风险态度、资产 | 投保决策、生产决策、还贷 | 500-2000 |
| 保险公司（Insurer） | 准备金、保费收入 | 承保、理赔、定价 | 1-3 |
| 银行（Bank） | 资本、存款、贷款利率 | 放贷、风控 | 1-5 |
| 政府（Government） | 财政预算、政策工具 | 补贴、监管 | 1 |

### 1.2 适用性评估

**适用场景**：
- ✅ 异质性农户（不同海拔/规模/风险偏好）
- ✅ 农户间交互（邻里效应、口碑传播、模仿学习）
- ✅ 涌现现象（参保率演化、系统性风险）
- ✅ 非线性反馈（保险赔付→信贷获取→生产投入→收入增加）

**不适用场景**：
- ❌ 单一代表性主体（可用均衡模型）
- ❌ 无交互的独立决策（可用计量回归）

### 1.3 选题匹配矩阵

| 研究方向 | 典型问题 | 推荐模型 |
|---------|---------|---------|
| 气象指数保险 | 最优触发阈值设计 | Schelling型协调博弈 |
| 保险+信贷 | 捆绑对违约率影响 | Farrin & Miranda (2015) 扩展 |
| 保费补贴 | 阶梯式补贴效率 | 前景理论+社会学习 |
| 风险传染 | 灾害冲击下的连锁反应 | 网络ABM+复杂网络 |

---

## 2. 理论框架

### 2.1 前景理论（Prospect Theory）

农户决策遵循前景理论，而非期望效用理论：

```
效用函数 = π(p) * v(x) + λ * Σ(邻居行为)
其中：
  - π(p): 概率权重函数（高估小概率事件）
  - v(x): 价值函数（损失厌恶系数 λ≈2.25）
  - 邻居效应：同村农户投保决策的空间自相关
```

### 2.2 社会学习机制

农户通过观察邻居行为更新投保意愿：

```python
def social_learning_update(self, neighbors, imitation_prob=0.1):
    """社会学习：模仿邻居投保决策"""
    if np.random.random() < imitation_prob:
        # 选择表现最好的邻居
        best_neighbor = max(neighbors, key=lambda n: n.performance)
        # 模仿其投保决策
        self.insurance = best_neighbor.insurance
```

### 2.3 行为方程库

#### 农户投保决策（Logit模型）

```python
P(insure=1) = 1 / (1 + exp(-(β₀ + β₁*subsidy + β₂*neighbor_rate + β₃*loss_exp)))

# 默认参数
β₀ = -1.5   # 基准倾向
β₁ = 3.2    # 补贴敏感度
β₂ = 1.8    # 邻里效应
β₃ = 0.5    # 损失经历
```

#### 银行利率定价

```python
r_i = r_base + α * (1 - insurance_flag) + γ * credit_score_i

# 默认参数
r_base = 4.2%  # 基准利率
α = 5.8%       # 未投保惩罚
γ = -0.02      # 信用分每+100，利率-2%
```

#### 保险公司盈余

```python
Profit_insurer = Σpremium - Σindemnity + investment_income
偿付能力约束: Capital >= 2 * Std(indemnity)
```

---

## 3. ODD协议模板

### 3.1 Overview（概述）

```yaml
目的:
  - 核心问题: "为何35%补贴率仍无法实现80%参保率？"
  - 政策目标: 寻找最优补贴阶梯设计
  
主体类型:
  - Farmer: n=500~2000（异质性：海拔、土地规模、风险态度）
  - InsuranceCompany: n=1（垄断或寡头）
  - Bank: n=1~3（差异化利率定价）
  - Government: n=1（外生政策制定者）
  
空间结构:
  - 选项1: GIS网格（真实地理坐标，100m×100m）
  - 选项2: 社交网络（小世界网络模拟邻里效应）
  - 选项3: 混合模式（GIS+网络双层结构）
```

### 3.2 Design Concepts（设计概念）

```yaml
涌现: 宏观参保率、系统性违约率、产业韧性指标
适应: 农户根据上年收益更新投保策略（强化学习Q-learning）
目标: 农户最大化期望效用，银行最小化坏账率
学习: 贝叶斯更新风险感知，或神经网络预测价格
交互:
  - 横向: 邻里观察（若邻居获赔，下期投保意愿+15%）
  - 纵向: 银行-农户信贷合约，保险-农户理赔合约
异质性:
  - 禀赋差异: 初始资产 N(10万，3万)
  - 风险态度: CRRA系数 ρ ~ Uniform(0.5, 2.0)
  - 海拔分层: 高海拔组霜冻概率15%，低海拔组5%
随机性:
  - 气候冲击: 泊松分布 π ~ Poisson(λ=0.05)
  - 价格波动: GBM过程 dP = μPdt + σPdW
```

### 3.3 Details（细节）

```yaml
初始化:
  - 农户数量: 500（可按实际行政村调整）
  - 初始资产: 对数正态分布 LogNormal(μ=11.5, σ=0.3)
  - 基准情景: 无保险，利率10%
  
输入数据:
  - 气象数据: 历史气温（用于指数保险触发）
  - 产量数据: 亩产（海拔依赖）
  - 价格数据: 农产品价格
  
子程序:
  - 气候生成器: 基于历史分布抽样极端事件
  - 理赔引擎: 当 T < T_critical 时自动赔付
  - 信贷审批: 信用评分决定利率
```

---

## 4. Python实现（Mesa）

### 4.1 农户主体类

```python
from mesa import Agent
import numpy as np

class FarmerAgent(Agent):
    def __init__(self, model, altitude, land_size, risk_aversion):
        super().__init__(model)
        self.altitude = altitude
        self.land_size = land_size
        self.risk_aversion = risk_aversion
        self.cash = np.random.lognormal(11.5, 0.3)
        self.insurance = False
        self.frost_risk = self.calc_frost_risk()
        
    def calc_frost_risk(self):
        """基于海拔计算霜冻风险"""
        if self.altitude > 1000:
            return 0.15
        elif self.altitude > 600:
            return 0.08
        else:
            return 0.05
    
    def decide_insure(self, subsidy_rate, neighbor_insure_rate):
        """投保决策（前景理论+邻里效应）"""
        EU_no_insure = self.expected_utility_no_insurance()
        EU_insure = self.expected_utility_with_insurance(subsidy_rate)
        
        peer_pressure = 0.3 * (neighbor_insure_rate - 0.5)
        prob_insure = 1 / (1 + np.exp(-(EU_insure - EU_no_insure + peer_pressure)))
        
        return np.random.random() < prob_insure
    
    def step(self):
        """单步执行"""
        # 1. 观测邻居投保率
        neighbors = self.model.grid.get_neighbors(self.pos, radius=2)
        neighbor_insure_rate = sum(n.insurance for n in neighbors) / len(neighbors)
        
        # 2. 更新投保决策
        self.insurance = self.decide_insure(
            subsidy_rate=self.model.policy_subsidy,
            neighbor_insure_rate=neighbor_insure_rate
        )
        
        # 3. 遭受气候冲击
        if np.random.random() < self.frost_risk:
            loss = self.calc_loss()
            if self.insurance:
                indemnity = self.model.insurer.claim(loss)
                self.cash += indemnity
        
        # 4. 生产与销售
        revenue = self.produce_and_sell()
        self.cash += revenue
```

### 4.2 主模型类

```python
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class AgriculturalInsuranceModel(Model):
    def __init__(self, num_farmers=500, grid_width=50, grid_height=50, 
                 subsidy_rate=0.25, climate_scenario='baseline', seed=None):
        
        super().__init__(seed=seed)
        self.num_farmers = num_farmers
        self.policy_subsidy = subsidy_rate
        self.climate_scenario = climate_scenario
        
        self.grid = MultiGrid(grid_width, grid_height, torus=False)
        
        self._create_farmers()
        self.insurer = InsuranceCompanyAgent(self)
        self.bank = BankAgent(self)
        self.government = GovernmentAgent(self)
        
        self.datacollector = DataCollector(
            model_reporters={
                "insure_rate": lambda m: sum(f.insurance for f in m.agents) / len(m.agents),
                "default_rate": lambda m: m.calc_default_rate(),
                "total_welfare": lambda m: m.calc_social_welfare()
            },
            agent_reporters={
                "cash": lambda a: a.cash,
                "insurance": lambda a: a.insurance,
                "altitude": lambda a: a.altitude
            }
        )
    
    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
    
    def run(self, steps=365):
        for _ in range(steps):
            self.step()
        return self.datacollector.get_model_vars_dataframe()
```

### 4.3 情景模拟器

```python
def simulate_subsidy_increase():
    """政策干预：补贴率从15%提升至35%"""
    results = []
    for subsidy in [0.15, 0.20, 0.25, 0.30, 0.35]:
        model = AgriculturalInsuranceModel(subsidy_rate=subsidy)
        df = model.run(steps=365)
        final_insure_rate = df['insure_rate'].iloc[-1]
        results.append({'subsidy': subsidy, 'insure_rate': final_insure_rate})
    return pd.DataFrame(results)

def simulate_climate_shock():
    """压力测试：连续两年倒春寒"""
    model = AgriculturalInsuranceModel(climate_scenario='severe_frost')
    df = model.run(steps=730)
    
    return {
        'bankruptcy_rate': (df['cash'] < 0).mean(),
        'default_rate': model.calc_default_rate(),
        'insurer_solvency': model.insurer.check_solvency()
    }
```

---

## 5. 参数校准

### 5.1 参数来源优先级

| 优先级 | 来源类型 | 示例 | 可信度 |
|-------|---------|------|--------|
| ★★★★★ | 实地问卷调查 | 农户收入、风险偏好 | 最高 |
| ★★★★☆ | 计量回归估计 | 投保意愿弹性系数 | 高 |
| ★★★☆☆ | 文献引用 | 前景理论参数 | 中 |
| ★★☆☆☆ | 政府统计年鉴 | 保费率、补贴政策 | 中 |
| ★☆☆☆☆ | 专家判断 | 交互强度 | 低 |

### 5.2 参数校准表模板

| 参数名称 | 符号 | 取值 | 来源 | 说明 |
|---------|------|------|------|------|
| 基准投保倾向 | β₀ | -1.5 | 本研究调查估计 | Logit截距项 |
| 补贴敏感系数 | β₁ | 3.2 | 本研究Probit估计 | p<0.01 |
| 邻里效应 | β₂ | 1.8 | 文献迁移 | TPB主观规范因子 |
| 损失厌恶系数 | λ | 2.25 | 蔡天鸣(2024) | 中国农户标准值 |
| 霜冻概率(高海拔) | p_frost | 0.15 | 气象局统计 | 海拔>1000m |
| 基准贷款利率 | r_base | 4.2% | 中国人民银行LPR | 一年期 |

### 5.3 敏感性分析

> 统一的敏感性分析函数见 [references/code-snippets.md §5](../references/code-snippets.md)。

### 5.4 稳健性检验清单

| 检验类型 | 操作 | 通过标准 |
|---------|------|---------|
| 参数敏感性 | ±20%扰动关键参数 | 定性结论不变 |
| 初始条件 | 改变初始财富分布 | 长期均衡一致 |
| 随机种子 | 更换RNG seed (n=30) | 结果统计无差异 |
| 极端边界 | 双重灾害（干旱+霜冻） | 保险公司不破产 |
| 尺度变换 | 主体数量×10 | 宏观指标收敛 |

---

## 6. 数据验证与模型诊断

### 6.1 输入数据验证

| 验证项 | 检查方法 | 通过标准 |
|-------|---------|----------|
| 农户样本量 | `len(farmers) >= 30` | 满足统计显著性最低要求 |
| 参数范围 | `ParamManager.validate()` | 所有参数在合理范围内 |
| 社会网络连通性 | `nx.is_connected(G)` | 网络图至少弱连通 |
| 收入分布 | Kolmogorov-Smirnov检验 | p > 0.05 |
| 保费率 | `0 < premium_rate < 1` | 在合理区间内 |

### 6.2 模型收敛性检查

1. **多次运行一致性**：同一参数配置运行10次，关键指标CV<0.1
2. **时间步稳定性**：最后20%时间步的指标变化率<5%
3. **敏感性分析**：OAT方法，关键参数±10%扰动

---

## 7. 核心文献库（精选6篇必引）

1. **Grimm, V., et al. (2006)** - A standard protocol for describing individual-based and agent-based models. *Ecological Modelling*, 198(1-2), 115-126.
   - ODD协议奠基论文

2. **Berger, T. (2001)** - Agent-based spatial models applied to agriculture. *Agricultural Economics*, 25(2-3), 245-260.
   - 农业ABM方法论奠基之作（被引>1085次）

3. **Kremmydas, D., et al. (2018)** - A review of agent based modeling for agricultural policy evaluation. *Agricultural Systems*, 164, 95-106.
   - 农业政策ABM系统综述（被引212次）

4. **Schreinemachers, P., & Berger, T. (2009)** - The diffusion of greenhouse agriculture in Northern Thailand. *Journal of Agricultural Economics*, 40(4), 373-388.
   - 计量+ABM融合方法范本

5. **Farrin, K., & Miranda, M. J. (2015)** - A heterogeneous agent model of credit-linked index insurance and farm technology adoption. *Journal of Development Economics*, 116, 257-268.
   - 信贷+指数保险+技术采纳三联动ABM

6. **Axtell, R. L., & Farmer, J. D. (2025)** - Agent-based modeling in economics and finance: Past, present, and future. *JEL*, 63(1), 197-287.
   - 经济金融ABM权威综述（91页，必引）

### 扩展文献

更多农业保险ABM文献见 [references/literature.md](../references/literature.md)（58篇，按主题分类）。

---

## 8. 研究设计建议

### 8.1 推荐选题路线

```
邢霞（2024）的 "调查问卷 → 理论模型 → ABM仿真" 三段式结构
         ↓ 结合
Schreinemachers & Berger（2009）的 "计量估计 → ABM参数校准" 方法论
         ↓ 聚焦于
Dubbelboer et al.（2017）的保险ABM主体框架（农户+保险公司+政府）
         ↓ 嵌入中国情境
以内江/威远黑山羊、雅安茶叶、乐山生猪等为研究区
```

### 8.2 常见误区

| 误区 | 问题所在 | 修正建议 |
|-----|---------|----------|
| 先学Mesa/NetLogo，再找研究问题 | 方法驱动而非问题驱动 | 先确定现实困境，再选择工具 |
| 直接使用默认参数 | 没有本地数据支撑 | 必须用本地调查或计量估计替换 |
| 只做基准情景，不做政策干预对比 | 研究问题回答不完整 | 至少设计3个情景 |
| ODD协议写得过于简略 | 模型可复现性差 | 严格按照Grimm et al. (2006)填写 |

---

## References

### 农业保险ABM核心文献

1. **Grimm, V., et al. (2006)** - ODD协议来源
2. **Berger, T. (2001)** - 农业ABM奠基之作
3. **Kremmydas, D., et al. (2018)** - 农业政策ABM综述
4. **Schreinemachers, P., & Berger, T. (2009)** - 计量+ABM校准范本
5. **熊熊, 郭翠, 张维, 等 (2010)** - 国内计算实验代表作
6. **Axtell, R. L., & Farmer, J. D. (2025)** - 经济金融ABM权威综述

---

*最后更新：2026-06-14*
