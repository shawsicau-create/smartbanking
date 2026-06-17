# ABM核心框架

## Purpose

本模块提供ABM的基础理论和通用方法论，是所有ABM项目的基础。包含ABM基本概念、ODD协议、主体设计模式、参数校准方法等核心内容。

---

## 1. ABM基本概念

### 1.1 什么是ABM

基于代理的建模（Agent-Based Modeling, ABM）是一种自底向上的建模方法，通过模拟个体代理（Agent）的行为和交互来研究复杂系统的涌现行为。

**核心要素**：
- **代理（Agent）**：具有自主决策能力的个体实体
- **环境（Environment）**：代理存在和交互的空间
- **规则（Rules）**：代理的行为决策规则
- **涌现（Emergence）**：宏观模式从微观交互中产生

### 1.2 ABM适用性评估

**适用场景**：
- ✅ 存在异质性主体（不同属性、行为规则）
- ✅ 主体间有交互（直接或间接影响）
- ✅ 涌现现象（宏观模式从微观产生）
- ✅ 非线性反馈（正反馈、负反馈循环）

**不适用场景**：
- ❌ 单一代表性主体（可用均衡模型）
- ❌ 无交互的独立决策（可用计量回归）
- ❌ 纯静态比较（可用CGE模型）

### 1.3 ABM vs 其他方法

| 方法 | 优势 | 劣势 | 适用场景 |
|------|------|------|----------|
| ABM | 异质性、交互、涌现 | 计算成本高、验证难 | 复杂适应系统 |
| 计量经济学 | 统计推断、因果识别 | 假设线性、同质性 | 政策评估 |
| DSGE | 理论严谨、均衡分析 | 代表性主体、理性预期 | 宏观经济 |
| 系统动力学 | 反馈循环、存量流量 | 忽视个体异质性 | 系统行为 |

### 1.4 选型决策树

```
你的研究问题是否涉及：
├── 异质性个体行为差异？ → ABM
├── 同质性聚合体的反馈循环？ → SD（系统动力学）
├── 离散事件序列和资源调度？ → DES（离散事件仿真）
└── 不确定？ → 问以下问题：
    ├── 个体行为差异对结果重要吗？ → ABM
    ├── 关注存量-流量和反馈循环？ → SD
    ├── 关注排队、资源分配？ → DES
    ├── 需要空间交互？ → ABM + GIS
    └── 需要均衡分析？ → DSGE / CGE
```

**关键区分**：
- **ABM vs SD**：ABM 自底向上（个体→系统），SD 自顶向下（系统→反馈）。当个体异质性和交互模式重要时选 ABM。
- **ABM vs DES**：DES 关注事件序列和资源调度（如排队论），ABM 关注主体决策和交互。
- **ABM vs 计量**：计量用于因果识别和参数估计，ABM 用于机制探索和政策仿真。两者可互补（计量估计参数→ABM仿真）。

---

## 2. ODD协议

### 2.1 概述

ODD（Overview, Design concepts, Details）是描述ABM的标准协议，由Grimm et al. (2006)提出，已成为ABM领域的规范。

**三大组成部分**：
- **Overview**：模型目的、主体类型、空间结构
- **Design concepts**：基本设计概念
- **Details**：初始化、输入数据、子程序

### 2.2 ODD协议模板

#### A. Overview（概述）

```yaml
目的:
  - 核心问题：[描述研究问题]
  - 政策目标：[如有]
  
主体类型:
  - AgentType1:
      数量: N
      属性: [属性列表]
      行为: [行为描述]
  - AgentType2:
      数量: M
      属性: [属性列表]
      行为: [行为描述]
      
空间结构:
  - 类型: [网格/网络/地理/混合]
  - 尺寸: [维度描述]
  - 拓扑: [连接方式]
```

#### B. Design Concepts（设计概念）

```yaml
涌现:
  - 宏观指标1: [描述]
  - 宏观指标2: [描述]

适应:
  - 学习机制: [强化学习/社会学习/贝叶斯更新]
  - 决策频率: [每步/定期/事件触发]

目标:
  - 代理目标: [最大化效用/最小化成本/满意即可]

交互:
  - 直接交互: [交易/协商/竞争]
  - 间接交互: [模仿/学习/环境反馈]

异质性:
  - 属性差异: [初始禀赋/偏好/能力]
  - 行为差异: [决策规则/学习速度]

随机性:
  - 环境随机: [气候/价格/政策]
  - 行为随机: [探索/噪声/有限理性]
```

#### C. Details（细节）

```yaml
初始化:
  - 时间步: [起始时间]
  - 代理数量: [各类型数量]
  - 初始状态: [属性初始分布]

输入数据:
  - 数据源: [文件/数据库/实时]
  - 数据格式: [CSV/JSON/API]
  - 更新频率: [静态/动态]

子程序:
  - 子程序1: [功能描述]
  - 子程序2: [功能描述]
```

---

## 3. 主体设计模式

### 3.1 主体类结构

> 完整的 Mesa 3.x 基类代码见 [references/code-snippets.md §1](../references/code-snippets.md)。以下为通用设计模式说明。

```python
from mesa import Agent

class MyAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.state = {}  # 状态变量
        self.memory = []  # 历史记忆
    
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
```

### 3.2 常用决策规则

#### 效用最大化

```python
def utility_maximizing_decision(self, options):
    """选择期望效用最大的选项"""
    best_option = max(options, key=lambda o: self.expected_utility(o))
    return best_option
```

#### Logit选择模型

```python
def logit_choice(self, options, beta=1.0):
    """Logit概率选择"""
    utilities = [self.expected_utility(o) for o in options]
    exp_utilities = [np.exp(beta * u) for u in utilities]
    sum_exp = sum(exp_utilities)
    probabilities = [eu / sum_exp for eu in exp_utilities]
    return np.random.choice(options, p=probabilities)
```

#### 满意即可

```python
def satisficing_decision(self, options, threshold):
    """选择第一个满足阈值的选项"""
    for option in options:
        if self.expected_utility(option) >= threshold:
            return option
    return options[-1]  # 默认选择最后一个
```

### 3.3 学习机制

#### 强化学习（Q-learning）

```python
def q_learning_update(self, state, action, reward, next_state, alpha=0.1, gamma=0.9):
    """Q值更新"""
    current_q = self.q_table.get((state, action), 0)
    max_next_q = max([self.q_table.get((next_state, a), 0) for a in self.actions])
    new_q = current_q + alpha * (reward + gamma * max_next_q - current_q)
    self.q_table[(state, action)] = new_q
```

#### 社会学习

```python
def social_learning(self, neighbors, imitation_prob=0.1):
    """模仿邻居行为"""
    if np.random.random() < imitation_prob:
        # 选择表现最好的邻居
        best_neighbor = max(neighbors, key=lambda n: n.performance)
        # 模仿其策略
        self.strategy = best_neighbor.strategy.copy()
```

#### 贝叶斯更新

```python
def bayesian_update(self, prior, likelihood, evidence):
    """贝叶斯信念更新（离散版）

    参数:
        prior: 先验概率数组，形状 (n_hypotheses,)
        likelihood: 似然值数组，形状 (n_hypotheses,)
        evidence: 边缘似然（标量），即 sum(prior * likelihood)
    返回:
        posterior: 后验概率数组，和为1
    """
    posterior = (likelihood * prior) / evidence
    # 归一化，防止浮点误差导致概率和不为1
    posterior = posterior / posterior.sum()
    return posterior
```

---

## 4. 网络结构

### 4.1 常用网络类型

| 网络类型 | 特征 | 适用场景 |
|---------|------|----------|
| 随机网络 | 任意两节点等概率连接 | 完全竞争市场 |
| 小世界网络 | 高聚类、短路径 | 邻里效应、口碑传播 |
| 无标度网络 | 幂律度分布 | 金融网络、社交网络 |
| 核心-外围 | 核心节点高度连接 | 银行间市场、供应链 |

### 4.2 网络生成代码

> 完整的网络生成和分析函数见 [references/code-snippets.md §3](../references/code-snippets.md)。以下为常用示例。

```python
import networkx as nx

# 随机网络（Erdos-Renyi）
G_random = nx.erdos_renyi_graph(n=100, p=0.1)

# 小世界网络（Watts-Strogatz）
G_smallworld = nx.watts_strogatz_graph(n=100, k=6, p=0.3)

# 无标度网络（Barabasi-Albert）
G_scalefree = nx.barabasi_albert_graph(n=100, m=2)

# 核心-外围网络
def core_periphery_graph(core_size, periphery_size, core_density=0.8, cross_density=0.1):
    G = nx.Graph()
    # 核心节点
    for i in range(core_size):
        G.add_node(f'core_{i}', type='core')
    # 外围节点
    for i in range(periphery_size):
        G.add_node(f'peri_{i}', type='periphery')
    # 核心内部连接
    for i in range(core_size):
        for j in range(i+1, core_size):
            if np.random.random() < core_density:
                G.add_edge(f'core_{i}', f'core_{j}')
    # 核心-外围连接
    for i in range(core_size):
        for j in range(periphery_size):
            if np.random.random() < cross_density:
                G.add_edge(f'core_{i}', f'peri_{j}')
    return G
```

### 4.3 网络分析指标

```python
def network_analysis(G):
    """网络结构分析"""
    metrics = {
        'num_nodes': G.number_of_nodes(),
        'num_edges': G.number_of_edges(),
        'density': nx.density(G),
        'avg_clustering': nx.average_clustering(G),
        'avg_shortest_path': nx.average_shortest_path_length(G) if nx.is_connected(G) else None,
        'degree_centrality': nx.degree_centrality(G),
        'betweenness_centrality': nx.betweenness_centrality(G),
    }
    return metrics
```

---

## 5. 参数校准

### 5.1 参数来源优先级

| 优先级 | 来源类型 | 示例 | 可信度 |
|-------|---------|------|--------|
| 1 | 实证数据校准 | 问卷调查、实验数据 | ★★★★★ |
| 2 | 计量估计值 | 回归系数、弹性估计 | ★★★★☆ |
| 3 | 文献引用 | 已发表研究的参数值 | ★★★☆☆ |
| 4 | 专家判断 | 领域专家经验值 | ★★☆☆☆ |
| 5 | 理论推导 | 模型均衡条件 | ★★☆☆☆ |

### 5.2 校准方法

#### 矩匹配（Method of Moments）

```python
def moment_matching(simulated_moments, target_moments):
    """最小化模拟矩与目标矩的差异"""
    def objective(params):
        model = create_model(params)
        results = model.run()
        sim_moments = extract_moments(results)
        return np.sum((sim_moments - target_moments)**2)
    
    from scipy.optimize import minimize
    result = minimize(objective, x0=initial_params, bounds=param_bounds)
    return result.x
```

#### 贝叶斯估计

```python
def bayesian_calibration(prior, data, obs_sd, model_prediction, n_samples=2000):
    """贝叶斯参数估计（PyMC v5+）

    参数:
        prior: dict，键为参数名，值为 (mu, sigma) 元组
        data: 观测数据数组
        obs_sd: 观测噪声标准差
        model_prediction: callable，输入参数返回模型预测值
        n_samples: MCMC采样数
    """
    import pymc as pm
    import arviz as az

    with pm.Model() as model:
        # 为每个参数设置先验分布
        param_vars = {}
        for name, (mu, sigma) in prior.items():
            param_vars[name] = pm.Normal(name, mu=mu, sigma=sigma)

        # 似然函数
        mu_obs = model_prediction(**param_vars)
        pm.Normal('likelihood', mu=mu_obs, sigma=obs_sd, observed=data)

        # MCMC采样
        idata = pm.sample(n_samples, return_inferencedata=True)

    return idata
```

### 5.3 敏感性分析

#### OAT（One-At-a-Time）方法

```python
def oat_sensitivity(model_class, base_params, param_ranges, n_runs=10):
    """单因素敏感性分析"""
    results = []
    
    for param_name, (low, high, steps) in param_ranges.items():
        for value in np.linspace(low, high, steps):
            params = base_params.copy()
            params[param_name] = value
            
            metrics = []
            for _ in range(n_runs):
                model = model_class(**params)
                result = model.run()
                metrics.append(result['key_metric'])
            
            results.append({
                'parameter': param_name,
                'value': value,
                'mean': np.mean(metrics),
                'std': np.std(metrics)
            })
    
    return pd.DataFrame(results)
```

#### 全局敏感性分析（Sobol指数）

```python
def sobol_sensitivity(model_class, param_ranges, n_samples=1000):
    """Sobol全局敏感性分析"""
    from SALib.sample import saltelli
    from SALib.analyze import sobol
    
    problem = {
        'num_vars': len(param_ranges),
        'names': list(param_ranges.keys()),
        'bounds': [param_ranges[name] for name in param_ranges.keys()]
    }
    
    # 生成样本
    param_values = saltelli.sample(problem, n_samples)
    
    # 运行模型
    Y = np.zeros([param_values.shape[0]])
    for i, params in enumerate(param_values):
        model = model_class(**dict(zip(problem['names'], params)))
        result = model.run()
        Y[i] = result['key_metric']
    
    # 分析
    Si = sobol.analyze(problem, Y)
    
    return Si
```

---

## 6. 模型验证

### 6.1 验证类型

| 验证类型 | 方法 | 目的 |
|---------|------|------|
| Face Validation | 专家评审 | 行为合理性 |
| Historical Validation | 与历史数据对比 | 预测能力 |
| Cross-Validation | 与其他模型对比 | 结果一致性 |
| Pattern Validation | 重现已知模式 | 机制正确性 |

### 6.2 验证代码

```python
def validate_model(model_output, empirical_data, metrics=['mean', 'std', 'distribution']):
    """模型验证"""
    validation_results = {}
    
    if 'mean' in metrics:
        # 均值对比
        sim_mean = np.mean(model_output)
        emp_mean = np.mean(empirical_data)
        validation_results['mean_error'] = abs(sim_mean - emp_mean) / emp_mean
    
    if 'std' in metrics:
        # 标准差对比
        sim_std = np.std(model_output)
        emp_std = np.std(empirical_data)
        validation_results['std_error'] = abs(sim_std - emp_std) / emp_std
    
    if 'distribution' in metrics:
        # 分布对比（KS检验）
        from scipy import stats
        ks_stat, p_value = stats.ks_2samp(model_output, empirical_data)
        validation_results['ks_statistic'] = ks_stat
        validation_results['ks_p_value'] = p_value
    
    return validation_results
```

### 6.3 稳健性检验清单

| 检验类型 | 操作 | 通过标准 |
|---------|------|---------|
| 参数敏感性 | ±20%扰动关键参数 | 定性结论不变 |
| 初始条件 | 改变初始状态分布 | 长期均衡一致 |
| 随机种子 | 更换RNG seed (n=30) | 结果统计无差异 |
| 极端边界 | 压力测试 | 模型不崩溃 |
| 尺度变换 | 主体数量×10 | 宏观指标收敛 |

---

## 7. ABM输出分析

### 7.1 遍历性检验

ABM 可能产生非遍历路径依赖（不同随机种子导致定性不同的结果）。必须检验：

```python
def test_ergodicity(model_class, params, n_runs=50, burn_in=100):
    """检验模型是否遍历

    返回:
        is_ergodic: bool
        cv: 变异系数
    """
    final_values = []
    for seed in range(n_runs):
        model = model_class(**params, seed=seed)
        for _ in range(burn_in):
            model.step()
        df = model.datacollector.get_model_vars_dataframe()
        final_values.append(df['key_metric'].iloc[-1])

    cv = np.std(final_values) / max(np.mean(final_values), 1e-10)
    return cv < 0.1, cv  # CV<0.1 认为近似遍历
```

### 7.2 瞬态 vs 稳态分析

```python
def detect_steady_state(series, window=50, threshold=0.05):
    """检测时间序列是否达到稳态

    返回:
        is_steady: bool
        steady_start: 稳态开始的位置（步数）
    """
    if len(series) < 2 * window:
        return False, len(series)

    recent = series[-window:]
    early = series[-2 * window:-window]

    if abs(early.mean()) < 1e-10:
        return False, len(series)

    change_rate = abs(recent.mean() - early.mean()) / abs(early.mean())
    return change_rate < threshold, len(series) - window
```

### 7.3 输出分析清单

| 检查项 | 方法 | 通过标准 |
|-------|------|---------|
| 遍历性 | 多次运行取CV | CV < 0.1 |
| 稳态检测 | 最后20%时间步变化率 | 变化率 < 5% |
| 分布形状 | 直方图 + KS检验 | 符合预期分布 |
| 极端值 | 检查NaN/Inf/负值 | 无异常值 |
| 时间序列平稳性 | ADF检验 | p < 0.05（如需平稳） |

---

## References

### 核心文献

1. **Grimm, V., et al. (2006)** - A standard protocol for describing individual-based and agent-based models. *Ecological Modelling*, 198(1-2), 115-126.
   - ODD协议奠基论文

2. **Railsback, S.F. & Grimm, V. (2019)** - Agent-Based and Individual-Based Modeling: A Practical Introduction. Princeton University Press.
   - ABM方法论教材

3. **Wilensky, U. & Rand, W. (2015)** - Introduction to Agent-Based Modeling. MIT Press.
   - NetLogo ABM入门

4. **Epstein, J.M. & Axtell, R. (1996)** - Growing Artificial Societies: Social Science from the Bottom Up. MIT Press.
   - ABM社会科学应用先驱

5. **Bonabeau, E. (2002)** - Agent-based modeling: Methods and techniques for simulating human systems. *PNAS*, 99(suppl 3), 7280-7287.
   - ABM方法论综述

---

*最后更新：2026-06-14*
