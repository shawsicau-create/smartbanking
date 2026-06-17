# 经济系统ABM模块

## Purpose

本模块提供经济系统ABM的专项框架，适用于银行风险传染、市场动态仿真、政策评估等经济领域研究。包含经济主体设计、金融网络建模、政策实验方法等内容。

---

## 1. 经济系统ABM框架

### 1.1 典型经济主体类型

| 主体类型 | 属性 | 行为 | 交互方式 |
|---------|------|------|----------|
| 家庭/消费者 | 财富、偏好、风险态度 | 消费、储蓄、投资 | 购买、借贷 |
| 企业/生产者 | 资本、技术、规模 | 生产、定价、雇佣 | 交易、竞争 |
| 银行 | 资本、存款、贷款 | 吸储、放贷、风控 | 同业拆借、信贷 |
| 政府/监管者 | 政策工具、目标 | 征税、补贴、监管 | 政策干预 |
| 保险公司 | 准备金、保费收入 | 承保、理赔 | 风险转移 |

### 1.2 经济系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                      经济系统架构                            │
├───────────────────────┬─────────────────────────────────────┤
│   微观层（主体）       │   宏观层（涌现）                     │
│  • 异质性主体          │  • 市场均衡                         │
│  • 有限理性决策        │  • 价格动态                         │
│  • 社会学习           │  • 系统性风险                        │
├───────────────────────┴─────────────────────────────────────┤
│                  反馈机制                                    │
│  价格信号 → 主体决策 → 行为聚合 → 价格更新                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 2. 银行风险传染建模

### 2.1 银行间网络模型

```python
from mesa import Agent, Model
import networkx as nx
import numpy as np

class BankAgent(Agent):
    def __init__(self, model, capital, assets, liabilities):
        super().__init__(model)
        self.capital = capital  # 资本金
        self.assets = assets  # 资产
        self.liabilities = liabilities  # 负债
        self.interbank_assets = {}  # 银行间资产
        self.interbank_liabilities = {}  # 银行间负债
        self.defaulted = False
    
    def calculate_solvency_ratio(self):
        """计算资本充足率"""
        total_risk_weighted_assets = self._calculate_risk_weighted_assets()
        if total_risk_weighted_assets == 0:
            return float('inf')
        return self.capital / total_risk_weighted_assets
    
    def check_default(self):
        """检查是否违约"""
        solvency_ratio = self.calculate_solvency_ratio()
        if solvency_ratio < 0.08:  # 巴塞尔协议最低要求
            self.defaulted = True
            return True
        return False
    
    def apply_shock(self, shock_size):
        """施加冲击"""
        self.assets -= shock_size
        self.capital -= shock_size
        return self.check_default()
    
    def contagion_effect(self):
        """传染效应"""
        if self.defaulted:
            # 计算对其他银行的损失
            for creditor_id, amount in self.interbank_liabilities.items():
                creditor = self.model.get_agent(creditor_id)
                loss = amount * (1 - self.model.recovery_rate)
                creditor.apply_shock(loss)
```

### 2.2 系统性风险度量

```python
def calculate_systemic_risk(banks):
    """计算系统性风险指标"""
    
    # 1. 违约率
    default_rate = sum(1 for b in banks if b.defaulted) / len(banks)
    
    # 2. 银行间网络连通性
    G = nx.Graph()
    for bank in banks:
        for counterparty in bank.interbank_assets:
            G.add_edge(bank.unique_id, counterparty)
    
    connectivity = nx.density(G)
    
    # 3. 集中度（HHI）
    total_assets = sum(b.assets for b in banks)
    market_shares = [b.assets / total_assets for b in banks]
    hhi = sum(s**2 for s in market_shares)
    
    # 4. 系统性风险贡献（CoVaR思想）
    def calculate_covar(banks, confidence=0.95):
        """简化版CoVaR：银行违约时系统损失的条件分位数

        CoVaR_{i} = VaR(system | bank_i = distressed) - VaR(system | median)
        """
        import numpy as np
        # 收集各银行的资产变动作为系统状态代理变量
        bank_losses = np.array([b.capital - b.assets * 0.1 for b in banks])
        # 假设违约银行资本充足率<8%时触发系统性损失
        distressed_mask = np.array([b.defaulted for b in banks])
        if distressed_mask.sum() == 0:
            return 0.0
        system_loss_given_distress = np.mean(bank_losses[distressed_mask])
        median_loss = np.median(bank_losses)
        covar = system_loss_given_distress - median_loss
        return covar
    
    covar = calculate_covar(banks)
    
    return {
        'default_rate': default_rate,
        'connectivity': connectivity,
        'concentration_hhi': hhi,
        'covar': covar,
    }
```

### 2.3 风险传染机制

#### 直接传染（银行间借贷）

```python
def direct_contagion(model):
    """直接传染：银行间借贷违约"""
    newly_defaulted = []
    
    for bank in model.agents:
        if isinstance(bank, BankAgent) and bank.defaulted:
            # 对每个债权银行造成损失
            for creditor_id, exposure in bank.interbank_liabilities.items():
                creditor = model.get_agent(creditor_id)
                loss = exposure * (1 - model.recovery_rate)
                
                if creditor.apply_shock(loss):
                    newly_defaulted.append(creditor)
    
    return newly_defaulted
```

#### 间接传染（资产价格下跌）

```python
def indirect_contagion(model, fire_sale_multiplier=0.5):
    """间接传染：资产甩卖导致价格下跌"""
    
    # 计算总甩卖资产
    total_fire_sales = sum(
        bank.assets * fire_sale_multiplier 
        for bank in model.agents 
        if bank.defaulted
    )
    
    # 资产价格下跌
    price_impact = total_fire_sales / model.total_market_assets
    
    # 所有银行资产缩水
    for bank in model.agents:
        if not bank.defaulted:
            asset_loss = bank.assets * price_impact
            bank.apply_shock(asset_loss)
```

---

## 3. 市场动态仿真

### 3.1 资产定价模型

```python
class AssetMarket:
    def __init__(self, fundamental_value, noise_traders_ratio=0.3):
        self.price = fundamental_value
        self.fundamental_value = fundamental_value
        self.noise_traders_ratio = noise_traders_ratio
        self.price_history = [fundamental_value]
    
    def update_price(self, agents):
        """更新资产价格"""
        
        # 计算总需求
        total_demand = 0
        for agent in agents:
            if isinstance(agent, NoiseTrader):
                # 噪声交易者：随机需求
                demand = np.random.normal(0, 10)
            elif isinstance(agent, FundamentalTrader):
                # 基本面交易者：基于价值
                demand = (self.fundamental_value - self.price) * agent.sensitivity
            elif isinstance(agent, Chartist):
                # 趋势交易者：基于历史趋势
                trend = self._calculate_trend()
                demand = trend * agent.sensitivity
            
            total_demand += demand
        
        # 价格调整（简化微观结构）
        price_change = total_demand * self.market_impact
        self.price *= (1 + price_change)
        self.price = max(self.price, 0)  # 价格非负
        
        self.price_history.append(self.price)
        
        return self.price
    
    def _calculate_trend(self, window=10):
        """计算价格趋势"""
        if len(self.price_history) < window:
            return 0
        recent_prices = self.price_history[-window:]
        return (recent_prices[-1] - recent_prices[0]) / recent_prices[0]
```

### 3.2 投资者行为建模

```python
class FundamentalTrader(Agent):
    """基本面交易者"""
    def __init__(self, model, sensitivity=0.5):
        super().__init__(model)
        self.sensitivity = sensitivity
        self.portfolio = 0
    
    def decide(self, market):
        """基于价值的决策"""
        expected_return = (self.estimate_fundamental() - market.price) / market.price
        
        if expected_return > self.threshold:
            # 买入
            self.portfolio += self.buy_amount
        elif expected_return < -self.threshold:
            # 卖出
            self.portfolio -= self.sell_amount

class Chartist(Agent):
    """趋势交易者"""
    def __init__(self, model, lookback=10):
        super().__init__(model)
        self.lookback = lookback
    
    def decide(self, market):
        """基于趋势的决策"""
        trend = market._calculate_trend(self.lookback)
        
        if trend > 0:
            # 追涨
            self.portfolio += self.buy_amount
        elif trend < 0:
            # 杀跌
            self.portfolio -= self.sell_amount

class NoiseTrader(Agent):
    """噪声交易者"""
    def __init__(self, model):
        super().__init__(model)
    
    def decide(self, market):
        """随机决策"""
        action = np.random.choice(['buy', 'sell', 'hold'])
        if action == 'buy':
            self.portfolio += np.random.randint(1, 10)
        elif action == 'sell':
            self.portfolio -= np.random.randint(1, 10)
```

### 3.3 市场微观结构

```python
class OrderBook:
    """订单簿"""
    def __init__(self):
        self.bids = []  # 买单 [(price, quantity, agent_id), ...]
        self.asks = []  # 卖单 [(price, quantity, agent_id), ...]
    
    def add_bid(self, price, quantity, agent_id):
        """添加买单"""
        self.bids.append((price, quantity, agent_id))
        self.bids.sort(key=lambda x: -x[0])  # 价格降序
    
    def add_ask(self, price, quantity, agent_id):
        """添加卖单"""
        self.asks.append((price, quantity, agent_id))
        self.asks.sort(key=lambda x: x[0])  # 价格升序
    
    def match(self):
        """撮合交易"""
        trades = []
        
        while self.bids and self.asks:
            best_bid = self.bids[0]
            best_ask = self.asks[0]
            
            if best_bid[0] >= best_ask[0]:
                # 成交
                trade_price = (best_bid[0] + best_ask[0]) / 2
                trade_quantity = min(best_bid[1], best_ask[1])
                
                trades.append({
                    'price': trade_price,
                    'quantity': trade_quantity,
                    'buyer': best_bid[2],
                    'seller': best_ask[2]
                })
                
                # 更新订单
                if best_bid[1] > trade_quantity:
                    self.bids[0] = (best_bid[0], best_bid[1] - trade_quantity, best_bid[2])
                else:
                    self.bids.pop(0)
                
                if best_ask[1] > trade_quantity:
                    self.asks[0] = (best_ask[0], best_ask[1] - trade_quantity, best_ask[2])
                else:
                    self.asks.pop(0)
            else:
                break
        
        return trades
```

---

## 4. 政策评估框架

### 4.1 政策实验设计

```python
class PolicyExperiment:
    def __init__(self, model_class, base_params):
        self.model_class = model_class
        self.base_params = base_params
        self.results = {}
    
    def run_baseline(self, n_runs=30):
        """基准情景"""
        baseline_results = []
        for _ in range(n_runs):
            model = self.model_class(**self.base_params)
            result = model.run()
            baseline_results.append(result)
        self.results['baseline'] = baseline_results
    
    def run_policy(self, policy_params, n_runs=30):
        """政策情景"""
        policy_results = []
        params = {**self.base_params, **policy_params}
        for _ in range(n_runs):
            model = self.model_class(**params)
            result = model.run()
            policy_results.append(result)
        self.results['policy'] = policy_results
    
    def compare_results(self):
        """比较结果"""
        baseline = pd.DataFrame(self.results['baseline'])
        policy = pd.DataFrame(self.results['policy'])
        
        comparison = {}
        for col in baseline.columns:
            baseline_mean = baseline[col].mean()
            policy_mean = policy[col].mean()
            change = (policy_mean - baseline_mean) / baseline_mean * 100
            
            # t检验
            from scipy import stats
            t_stat, p_value = stats.ttest_ind(baseline[col], policy[col])
            
            comparison[col] = {
                'baseline': baseline_mean,
                'policy': policy_mean,
                'change_pct': change,
                'p_value': p_value,
                'significant': p_value < 0.05
            }
        
        return pd.DataFrame(comparison).T
```

### 4.2 常用政策工具

| 政策类型 | 工具 | 作用机制 | 评估指标 |
|---------|------|----------|---------|
| 货币政策 | 利率、准备金率 | 影响信贷成本和供给 | 贷款量、违约率 |
| 财政政策 | 税收、补贴 | 影响收入和投资 | GDP、就业率 |
| 监管政策 | 资本要求、杠杆限制 | 影响风险承担 | 资本充足率、系统性风险 |
| 宏观审慎 | 逆周期缓冲、压力测试 | 防范系统性风险 | 金融稳定性 |

### 4.3 情景分析

```python
def scenario_analysis(model_class, base_params, scenarios):
    """
    scenarios: dict of scenario_name -> policy_params
    """
    results = {}
    
    for scenario_name, policy_params in scenarios.items():
        print(f"Running scenario: {scenario_name}")
        
        scenario_results = []
        params = {**base_params, **policy_params}
        
        for run in range(30):  # 30次重复
            model = model_class(**params, seed=run)
            result = model.run()
            scenario_results.append(result)
        
        results[scenario_name] = scenario_results
    
    # 汇总结果
    summary = {}
    for scenario_name, scenario_results in results.items():
        df = pd.DataFrame(scenario_results)
        summary[scenario_name] = {
            'mean': df.mean(),
            'std': df.std(),
            'ci_lower': df.quantile(0.025),
            'ci_upper': df.quantile(0.975)
        }
    
    return summary

# 使用示例
scenarios = {
    'baseline': {},
    'low_interest': {'interest_rate': 0.02},
    'high_capital': {'capital_requirement': 0.12},
    'combined': {'interest_rate': 0.02, 'capital_requirement': 0.12}
}
results = scenario_analysis(BankingModel, base_params, scenarios)
```

---

## 5. 金融网络分析

### 5.1 网络构建

```python
def build_financial_network(transactions):
    """从交易数据构建金融网络"""
    G = nx.DiGraph()
    
    for transaction in transactions:
        lender = transaction['lender']
        borrower = transaction['borrower']
        amount = transaction['amount']
        
        if G.has_edge(lender, borrower):
            G[lender][borrower]['weight'] += amount
        else:
            G.add_edge(lender, borrower, weight=amount)
    
    return G
```

### 5.2 网络风险指标

```python
def calculate_network_risk(G):
    """计算网络风险指标"""
    
    # 1. 度中心性
    degree_centrality = nx.degree_centrality(G)
    
    # 2. 介数中心性（识别系统重要性节点）
    betweenness_centrality = nx.betweenness_centrality(G)
    
    # 3. 特征向量中心性
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000)
    
    # 4. 网络密度
    density = nx.density(G)
    
    # 5. 聚类系数
    clustering = nx.average_clustering(G)
    
    # 6. 识别系统重要性银行（SIBs）
    sibs = sorted(betweenness_centrality.items(), key=lambda x: -x[1])[:5]
    
    return {
        'density': density,
        'clustering': clustering,
        'top_sibs': sibs,
        'degree_centrality': degree_centrality,
        'betweenness_centrality': betweenness_centrality,
    }
```

### 5.3 网络韧性分析

```python
def network_resilience_analysis(G, attack_strategy='random', n_simulations=100):
    """网络韧性分析"""
    
    results = []
    
    for sim in range(n_simulations):
        G_copy = G.copy()
        
        if attack_strategy == 'random':
            # 随机攻击
            nodes_to_remove = np.random.choice(
                list(G_copy.nodes()), 
                size=int(len(G_copy) * 0.1), 
                replace=False
            )
        elif attack_strategy == 'targeted':
            # 定向攻击（攻击中心节点）
            centrality = nx.betweenness_centrality(G_copy)
            nodes_to_remove = sorted(centrality, key=centrality.get, reverse=True)[:int(len(G_copy) * 0.1)]
        
        # 移除节点
        G_copy.remove_nodes_from(nodes_to_remove)
        
        # 计算剩余网络的连通性
        if nx.is_connected(G_copy):
            largest_component_size = len(G_copy)
        else:
            largest_component_size = len(max(nx.connected_components(G_copy), key=len))
        
        results.append({
            'simulation': sim,
            'nodes_removed': len(nodes_to_remove),
            'largest_component_size': largest_component_size,
            'connectivity': largest_component_size / len(G)
        })
    
    return pd.DataFrame(results)
```

---

## 6. 经济系统ABM最佳实践

### 6.1 模型设计原则

1. **KISS原则**：Keep It Simple, Stupid - 从简单开始
2. **异质性**：主体应有真实的属性差异
3. **有限理性**：避免完美理性假设
4. **反馈机制**：包含价格-行为-价格的反馈循环

### 6.2 校准建议

1. **使用真实数据**：银行资产、负债、资本金来自监管报告
2. **网络结构**：基于真实银行间市场数据构建
3. **行为参数**：引用实证研究估计的弹性系数

### 6.3 验证要点

1. **复制已知现象**：如银行挤兑、资产泡沫
2. **与历史事件对比**：如2008年金融危机
3. **专家评审**：银行从业者评审模型合理性

---

## References

### 经济系统ABM核心文献

1. **Axtell, R. L., & Farmer, J. D. (2025)** - Agent-based modeling in economics and finance: Past, present, and future. *Journal of Economic Literature*, 63(1), 197-287.
   - 经济金融ABM权威综述

2. **Bookstaber, R., Paddrik, M., & Tivnan, B. (2018)** - An agent-based model for financial vulnerability. *Journal of Economic Interaction and Coordination*, 13(2), 433-466.
   - 金融脆弱性ABM模型

3. **Heinrich, T., Sabuco, J., & Farmer, J. D. (2021)** - A simulation of the insurance industry: the problem of risk model homogeneity. *Journal of Economic Interaction and Coordination*, 17(2), 535-576.
   - 保险行业ABM

4. **LeBaron, B. (2000)** - Agent-based computational finance: Suggested readings and early research. *Journal of Economic Dynamics and Control*, 24(5), 679-702.
   - 计算实验金融综述

5. **Mizuta, T. (2019)** - An agent-based model for designing a financial market that works well. arXiv:1906.06000.
   - 金融市场ABM设计

---

*最后更新：2026-06-14*
