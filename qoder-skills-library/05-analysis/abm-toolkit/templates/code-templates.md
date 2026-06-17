# ABM代码模板库

## Purpose

本模板库提供ABM开发的常用代码模板，帮助研究者快速构建ABM模型。

> **注意**：通用基类（BaseAgent、BaseModel）、网络工具、校准方法、可视化函数等共享代码见 [references/code-snippets.md](../references/code-snippets.md)。本文件仅包含领域特定的主体模板。

---

## 1. Mesa基础模板

### 1.1 主体模板

```python
from mesa import Agent
import numpy as np

class BaseAgent(Agent):
    """主体基类"""
    
    def __init__(self, model):
        super().__init__(model)
        self.state = {}
        self.memory = []
    
    def perceive(self):
        """感知环境"""
        pass
    
    def decide(self):
        """决策"""
        pass
    
    def act(self):
        """执行行动"""
        pass
    
    def step(self):
        """单步执行"""
        self.perceive()
        self.decide()
        self.act()
        self._record_history()
    
    def _record_history(self):
        """记录历史"""
        self.memory.append(self.state.copy())
```

### 1.2 主模型模板

```python
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class BaseModel(Model):
    """主模型基类"""
    
    def __init__(self, config, seed=None):
        super().__init__(seed=seed)
        self.config = config
        
        # 空间
        self.grid = MultiGrid(
            config.get('grid_width', 50),
            config.get('grid_height', 50),
            torus=False
        )
        
        # 初始化
        self._create_agents()
        self._setup_datacollector()
    
    def _create_agents(self):
        """创建主体（子类实现）"""
        raise NotImplementedError
    
    def _setup_datacollector(self):
        """设置数据收集器"""
        self.datacollector = DataCollector(
            model_reporters={
                "num_agents": lambda m: len(m.agents),
            },
            agent_reporters={
                "wealth": lambda a: getattr(a, 'wealth', 0),
            }
        )
    
    def step(self):
        """单步推进"""
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
    
    def run(self, steps=100):
        """运行仿真"""
        for _ in range(steps):
            self.step()
        return self.datacollector.get_model_vars_dataframe()
```

---

## 2. 经济主体模板

### 2.1 家庭/消费者模板

```python
class HouseholdAgent(BaseAgent):
    """家庭主体"""
    
    def __init__(self, model, income, risk_aversion):
        super().__init__(model)
        self.income = income
        self.risk_aversion = risk_aversion
        self.wealth = np.random.lognormal(10, 1)
        self.consumption = 0
        self.savings = 0
    
    def perceive(self):
        """感知市场状态"""
        self.market_price = self.model.market_price
        self.interest_rate = self.model.interest_rate
    
    def decide(self):
        """消费-储蓄决策"""
        # 简单规则：固定储蓄率
        savings_rate = 0.2
        self.savings = self.income * savings_rate
        self.consumption = self.income - self.savings
    
    def act(self):
        """执行决策"""
        self.wealth += self.savings * (1 + self.interest_rate)
        self.wealth -= self.consumption
```

### 2.2 企业模板

```python
class FirmAgent(BaseAgent):
    """企业主体"""
    
    def __init__(self, model, capital, productivity):
        super().__init__(model)
        self.capital = capital
        self.productivity = productivity
        self.output = 0
        self.profit = 0
        self.workers = []
    
    def perceive(self):
        """感知市场"""
        self.labor_cost = self.model.labor_cost
        self.product_price = self.model.product_price
    
    def decide(self):
        """生产决策"""
        # 柯布-道格拉斯生产函数
        labor = len(self.workers)
        self.output = self.productivity * (self.capital ** 0.3) * (labor ** 0.7)
        
        # 雇佣决策
        desired_labor = (self.output / self.productivity) ** (1/0.7)
        if desired_labor > labor:
            self._hire(int(desired_labor - labor))
        elif desired_labor < labor:
            self._fire(int(labor - desired_labor))
    
    def act(self):
        """执行生产"""
        self.profit = self.output * self.product_price - len(self.workers) * self.labor_cost
        self.capital += self.profit * 0.5  # 50%利润再投资
```

### 2.3 银行模板

```python
class BankAgent(BaseAgent):
    """银行主体"""
    
    def __init__(self, model, capital, interest_rate):
        super().__init__(model)
        self.capital = capital
        self.deposits = 0
        self.loans = 0
        self.interest_rate = interest_rate
        self.default_rate = 0
    
    def perceive(self):
        """感知市场"""
        self.central_bank_rate = self.model.central_bank_rate
        self.credit_demand = sum(
            a.credit_demand for a in self.model.agents 
            if hasattr(a, 'credit_demand')
        )
    
    def decide(self):
        """信贷决策"""
        # 利率定价
        self.lending_rate = self.central_bank_rate + 0.02 + self.default_rate
        
        # 信贷配给
        self.max_loans = self.capital * 10  # 资本充足率10%
        self.approved_loans = min(self.credit_demand, self.max_loans)
    
    def act(self):
        """执行信贷"""
        self.loans = self.approved_loans
        self.deposits = self.loans * 0.8  # 80%贷款来自存款
        self.capital = self.loans * 0.1  # 10%资本充足率
```

---

## 3. 农业保险主体模板

### 3.1 农户模板

```python
class FarmerAgent(BaseAgent):
    """农户主体"""
    
    def __init__(self, model, altitude, land_size, risk_aversion):
        super().__init__(model)
        self.altitude = altitude
        self.land_size = land_size
        self.risk_aversion = risk_aversion
        self.cash = np.random.lognormal(11.5, 0.3)
        self.insurance = False
        self.loan = 0
        self.frost_risk = self._calc_frost_risk()
    
    def _calc_frost_risk(self):
        """计算霜冻风险"""
        if self.altitude > 1000:
            return 0.15
        elif self.altitude > 600:
            return 0.08
        else:
            return 0.05
    
    def perceive(self):
        """感知环境"""
        # 观察邻居投保率
        neighbors = self.model.grid.get_neighbors(self.pos, radius=2)
        self.neighbor_insure_rate = sum(
            n.insurance for n in neighbors
        ) / max(len(neighbors), 1)
        
        # 获取政策信息
        self.subsidy_rate = self.model.policy_subsidy
    
    def decide(self):
        """投保决策"""
        # 计算期望效用
        EU_no_insure = self._calc_EU_no_insurance()
        EU_insure = self._calc_EU_with_insurance()
        
        # 邻里效应
        peer_pressure = 0.3 * (self.neighbor_insure_rate - 0.5)
        
        # Logit选择
        prob = 1 / (1 + np.exp(-(EU_insure - EU_no_insure + peer_pressure)))
        self.insurance = np.random.random() < prob
    
    def act(self):
        """执行行动"""
        # 遭受气候冲击
        if np.random.random() < self.frost_risk:
            loss = self._calc_loss()
            if self.insurance:
                indemnity = self.model.insurer.claim(loss)
                self.cash += indemnity
        
        # 生产与销售
        revenue = self._produce_and_sell()
        self.cash += revenue
        
        # 还贷
        if self.loan > 0:
            self._repay_loan()
    
    def _calc_EU_no_insurance(self):
        """计算不投保的期望效用"""
        # 简化计算
        return self.cash * (1 - self.frost_risk * 0.5)
    
    def _calc_EU_with_insurance(self):
        """计算投保的期望效用"""
        premium = self.model.premium_rate * (1 - self.subsidy_rate)
        return self.cash * (1 - premium) + self.frost_risk * 0.3
    
    def _calc_loss(self):
        """计算损失"""
        return self.cash * np.random.uniform(0.1, 0.5)
    
    def _produce_and_sell(self):
        """生产与销售"""
        base_revenue = self.land_size * 1000
        noise = np.random.normal(1, 0.1)
        return base_revenue * noise
    
    def _repay_loan(self):
        """还贷"""
        repayment = min(self.loan * 1.1, self.cash * 0.3)
        self.cash -= repayment
        self.loan -= repayment / 1.1
```

### 3.2 保险公司模板

```python
class InsurerAgent(BaseAgent):
    """保险公司主体"""
    
    def __init__(self, model, capital):
        super().__init__(model)
        self.capital = capital
        self.premium_income = 0
        self.claims_paid = 0
        self.policies = []
    
    def perceive(self):
        """感知市场"""
        self.demand = sum(
            1 for a in self.model.agents 
            if isinstance(a, FarmerAgent) and a.insurance
        )
    
    def decide(self):
        """定价决策"""
        # 简单定价：基于历史赔付率
        if self.premium_income > 0:
            loss_ratio = self.claims_paid / self.premium_income
            self.premium_rate = loss_ratio * 1.2  # 20%利润率
        else:
            self.premium_rate = self.model.base_premium_rate
    
    def claim(self, loss_amount):
        """理赔"""
        # 检查是否在保障范围内
        if loss_amount > 0:
            payout = loss_amount * 0.8  # 80%赔付
            self.claims_paid += payout
            return payout
        return 0
    
    def step(self):
        """单步执行"""
        self.perceive()
        self.decide()
        
        # 收取保费
        self.premium_income = sum(
            self.premium_rate * (1 - a.subsidy_rate) 
            for a in self.model.agents 
            if isinstance(a, FarmerAgent) and a.insurance
        )
        
        # 检查偿付能力
        if self.capital < self.claims_paid * 0.5:
            self._raise_capital()
```

### 3.3 政府模板

```python
class GovernmentAgent(BaseAgent):
    """政府主体"""
    
    def __init__(self, model, budget):
        super().__init__(model)
        self.budget = budget
        self.subsidy_spent = 0
    
    def perceive(self):
        """感知社会状态"""
        self.insurance_rate = sum(
            a.insurance for a in self.model.agents 
            if isinstance(a, FarmerAgent)
        ) / sum(1 for a in self.model.agents if isinstance(a, FarmerAgent))
        
        self.default_rate = sum(
            1 for a in self.model.agents 
            if isinstance(a, FarmerAgent) and a.cash < 0
        ) / sum(1 for a in self.model.agents if isinstance(a, FarmerAgent))
    
    def decide(self):
        """政策决策"""
        # 调整补贴率
        if self.insurance_rate < 0.5:
            self.model.policy_subsidy = min(self.model.policy_subsidy + 0.05, 0.5)
        elif self.insurance_rate > 0.8:
            self.model.policy_subsidy = max(self.model.policy_subsidy - 0.05, 0.1)
    
    def act(self):
        """执行政策"""
        # 支付补贴
        self.subsidy_spent = sum(
            self.model.premium_rate * self.model.policy_subsidy
            for a in self.model.agents 
            if isinstance(a, FarmerAgent) and a.insurance
        )
        self.budget -= self.subsidy_spent
```

---

## 4. 网络与空间模板

### 4.1 社会网络模板

```python
import networkx as nx

class SocialNetwork:
    """社会网络"""
    
    def __init__(self, network_type='small_world', **kwargs):
        self.network_type = network_type
        self.G = self._create_network(**kwargs)
    
    def _create_network(self, **kwargs):
        """创建网络"""
        if self.network_type == 'small_world':
            return nx.watts_strogatz_graph(
                kwargs.get('n', 100),
                kwargs.get('k', 6),
                kwargs.get('p', 0.3)
            )
        elif self.network_type == 'scale_free':
            return nx.barabasi_albert_graph(
                kwargs.get('n', 100),
                kwargs.get('m', 2)
            )
        elif self.network_type == 'random':
            return nx.erdos_renyi_graph(
                kwargs.get('n', 100),
                kwargs.get('p', 0.1)
            )
        else:
            raise ValueError(f"Unknown network type: {self.network_type}")
    
    def get_neighbors(self, node):
        """获取邻居"""
        return list(self.G.neighbors(node))
    
    def add_edge(self, u, v, **kwargs):
        """添加边"""
        self.G.add_edge(u, v, **kwargs)
    
    def remove_edge(self, u, v):
        """移除边"""
        self.G.remove_edge(u, v)
    
    def get_degree(self, node):
        """获取度数"""
        return self.G.degree(node)
    
    def get_clustering_coefficient(self):
        """获取聚类系数"""
        return nx.average_clustering(self.G)
    
    def get_shortest_path(self, source, target):
        """获取最短路径"""
        return nx.shortest_path(self.G, source, target)
```

### 4.2 资源环境模板

```python
class ResourceEnvironment:
    """资源环境"""
    
    def __init__(self, width, height, initial_resource=100, regeneration_rate=0.01):
        self.width = width
        self.height = height
        self.resources = np.full((width, height), initial_resource, dtype=float)
        self.regeneration_rate = regeneration_rate
    
    def get_resource(self, pos):
        """获取资源"""
        return self.resources[pos[0], pos[1]]
    
    def harvest(self, pos, amount):
        """收获资源"""
        available = self.resources[pos[0], pos[1]]
        harvested = min(amount, available)
        self.resources[pos[0], pos[1]] -= harvested
        return harvested
    
    def regenerate(self):
        """资源再生"""
        self.resources += self.regeneration_rate * (100 - self.resources)
        self.resources = np.clip(self.resources, 0, 100)
    
    def step(self):
        """单步更新"""
        self.regenerate()
```

---

## 5. 参数校准模板

### 5.1 矩匹配校准

> 统一的校准函数见 [references/code-snippets.md §4](../references/code-snippets.md)。

### 5.2 ABC校准

> 近似贝叶斯计算(ABC)校准函数见 [references/code-snippets.md §4.2](../references/code-snippets.md)。ABM不可微分，不能直接用PyMC做MCMC。

---

## 6. 可视化模板

> 可视化函数（时间序列、分布图、网络图、论文级图表）见 [references/code-snippets.md §6](../references/code-snippets.md)。

---

## 7. 实验模板

> 情景分析和敏感性分析函数见 [references/code-snippets.md §5,§7](../references/code-snippets.md)。

---

*最后更新：2026-06-14*
