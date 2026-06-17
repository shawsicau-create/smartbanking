# ABM 共享代码片段

## Purpose

本文件是 ABM toolkit 共享代码的**单一来源（Single Source of Truth）**。其他模块通过引用本文件避免代码重复。

---

## 1. Agent 基类（Mesa 3.x）

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

## 2. 主模型基类（Mesa 3.x）

```python
from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class BaseModel(Model):
    """主模型基类"""

    def __init__(self, config, seed=None):
        super().__init__(seed=seed)
        self.config = config

        self.grid = MultiGrid(
            config.get('grid_width', 50),
            config.get('grid_height', 50),
            torus=False
        )

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

## 3. 网络工具

```python
import networkx as nx
import numpy as np

def create_social_network(n, network_type='small_world', **kwargs):
    """创建社会网络"""
    if network_type == 'small_world':
        return nx.watts_strogatz_graph(n, k=kwargs.get('k', 6), p=kwargs.get('p', 0.3))
    elif network_type == 'random':
        return nx.erdos_renyi_graph(n, p=kwargs.get('p', 0.1))
    elif network_type == 'scale_free':
        return nx.barabasi_albert_graph(n, m=kwargs.get('m', 2))
    elif network_type == 'core_periphery':
        return create_core_periphery_network(n, **kwargs)
    else:
        raise ValueError(f"Unknown network type: {network_type}")

def create_core_periphery_network(n, core_ratio=0.2, core_density=0.8, cross_density=0.1):
    """创建核心-外围网络"""
    G = nx.Graph()
    core_size = int(n * core_ratio)
    periphery_size = n - core_size

    for i in range(core_size):
        G.add_node(f'core_{i}', type='core')
    for i in range(periphery_size):
        G.add_node(f'peri_{i}', type='periphery')

    for i in range(core_size):
        for j in range(i + 1, core_size):
            if np.random.random() < core_density:
                G.add_edge(f'core_{i}', f'core_{j}')

    for i in range(core_size):
        for j in range(periphery_size):
            if np.random.random() < cross_density:
                G.add_edge(f'core_{i}', f'peri_{j}')

    return G

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

## 4. 参数校准

### 4.1 矩匹配校准

```python
from scipy.optimize import minimize
import numpy as np

def moment_matching_calibration(model_class, param_names, target_moments,
                                initial_params, param_bounds, n_runs=10):
    """矩匹配校准

    参数:
        model_class: ABM模型类
        param_names: 参数名列表，如 ['alpha', 'beta']
        target_moments: 目标矩，如 {'mean': 0.5, 'std': 0.1}
        initial_params: 初始参数值数组
        param_bounds: 参数边界列表，如 [(0, 1), (0, 2)]
        n_runs: 每组参数运行次数（取均值降噪）
    """

    def objective(params):
        all_moments = {'mean': [], 'std': [], 'skew': []}
        for _ in range(n_runs):
            param_dict = dict(zip(param_names, params))
            model = model_class(**param_dict)
            results = model.run()

            key_data = results['key_metric']
            all_moments['mean'].append(key_data.mean())
            all_moments['std'].append(key_data.std())
            if hasattr(key_data, 'skew'):
                all_moments['skew'].append(key_data.skew())

        loss = 0
        for key in target_moments:
            sim_val = np.mean(all_moments.get(key, [0]))
            loss += (sim_val - target_moments[key]) ** 2

        return loss

    result = minimize(
        objective,
        x0=initial_params,
        bounds=param_bounds,
        method='L-BFGS-B'
    )

    return dict(zip(param_names, result.x))
```

### 4.2 近似贝叶斯计算（ABC）校准

```python
def abc_calibration(model_class, prior_params, observed_data,
                    summary_stat='mean', tolerance=0.1, n_samples=5000):
    """近似贝叶斯计算(ABC)校准 — 适用于不可微分的ABM

    参数:
        model_class: ABM模型类
        prior_params: dict，键为参数名，值为 (mu, sigma) 元组
        observed_data: 观测数据数组
        summary_stat: 摘要统计量（'mean', 'std', 'median'）
        tolerance: 接受阈值（相对误差）
        n_samples: 先验采样数
    """
    accepted = []
    obs_stat = getattr(observed_data, summary_stat)()

    for _ in range(n_samples):
        # 1. 从先验抽样
        params = {name: np.random.normal(mu, sigma)
                  for name, (mu, sigma) in prior_params.items()}

        # 2. 运行ABM
        model = model_class(**params)
        result = model.run()
        sim_stat = getattr(result['key_metric'], summary_stat)()

        # 3. ABC拒绝步骤
        if abs(sim_stat - obs_stat) / max(abs(obs_stat), 1e-10) < tolerance:
            accepted.append(params)

    return pd.DataFrame(accepted)
```

## 5. 敏感性分析

```python
import pandas as pd
import numpy as np

def sensitivity_analysis(model_class, base_params, param_ranges, n_runs=30, seed_offset=0):
    """OAT（One-At-a-Time）敏感性分析

    参数:
        model_class: ABM模型类
        base_params: 基准参数字典
        param_ranges: dict，键为参数名，值为 (low, high, steps) 元组
        n_runs: 每组参数运行次数
        seed_offset: 随机种子偏移
    """
    results = []

    for param_name, (low, high, steps) in param_ranges.items():
        for value in np.linspace(low, high, steps):
            params = base_params.copy()
            params[param_name] = value

            metrics = []
            for run in range(n_runs):
                model = model_class(**params, seed=seed_offset + run)
                result = model.run()
                metrics.append(result['key_metric'].iloc[-1])

            results.append({
                'parameter': param_name,
                'value': value,
                'mean': np.mean(metrics),
                'std': np.std(metrics)
            })

    return pd.DataFrame(results)
```

## 6. 可视化

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_time_series(data, columns, title="Model Dynamics", figsize=(12, 8)):
    """绘制时间序列"""
    fig, axes = plt.subplots(len(columns), 1, figsize=figsize)

    if len(columns) == 1:
        axes = [axes]

    for i, col in enumerate(columns):
        axes[i].plot(data[col])
        axes[i].set_ylabel(col)
        axes[i].grid(True, alpha=0.3)

    axes[-1].set_xlabel('Time Step')
    plt.suptitle(title)
    plt.tight_layout()
    return fig

def plot_distribution(data, title="Distribution", figsize=(10, 6)):
    """绘制分布图"""
    fig, ax = plt.subplots(figsize=figsize)

    ax.hist(data, bins=30, density=True, alpha=0.7, edgecolor='black')
    ax.axvline(np.mean(data), color='red', linestyle='--', label=f'Mean: {np.mean(data):.2f}')
    ax.axvline(np.median(data), color='green', linestyle='--', label=f'Median: {np.median(data):.2f}')

    ax.set_xlabel('Value')
    ax.set_ylabel('Density')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    return fig

def plot_network(G, node_colors=None, node_sizes=None, title="Network", figsize=(10, 10)):
    """绘制网络图"""
    import networkx as nx

    fig, ax = plt.subplots(figsize=figsize)
    pos = nx.spring_layout(G)
    nx.draw(
        G, pos,
        node_color=node_colors,
        node_size=node_sizes or 50,
        with_labels=False,
        edge_color='gray',
        alpha=0.7,
        ax=ax
    )
    ax.set_title(title)
    return fig

def create_publication_figures(model_output):
    """生成论文级图表"""
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    axes[0, 0].plot(model_output['insure_rate'])
    axes[0, 0].set_title('Insurance Rate Over Time')
    axes[0, 0].set_xlabel('Time Step')
    axes[0, 0].set_ylabel('Rate')

    axes[0, 1].plot(model_output['default_rate'], color='red')
    axes[0, 1].set_title('Default Rate Over Time')
    axes[0, 1].set_xlabel('Time Step')
    axes[0, 1].set_ylabel('Rate')

    if 'wealth_distribution' in model_output:
        sns.histplot(model_output['wealth_distribution'], kde=True, ax=axes[1, 0])
        axes[1, 0].set_title('Wealth Distribution')

    if 'altitude' in model_output and 'insurance' in model_output:
        axes[1, 1].scatter(model_output['altitude'], model_output['insurance'], alpha=0.5)
        axes[1, 1].set_title('Altitude vs Insurance')
        axes[1, 1].set_xlabel('Altitude (m)')
        axes[1, 1].set_ylabel('Insurance (0/1)')

    plt.tight_layout()
    return fig
```

## 7. 实验运行

```python
def scenario_analysis(model_class, base_params, scenarios, n_runs=30):
    """情景分析

    参数:
        model_class: ABM模型类
        base_params: 基准参数字典
        scenarios: dict，键为情景名，值为参数覆盖字典
        n_runs: 每个情景运行次数
    """
    results = {}

    for scenario_name, scenario_params in scenarios.items():
        print(f"Running scenario: {scenario_name}")

        scenario_results = []
        for run in range(n_runs):
            params = {**base_params, **scenario_params, 'seed': run}
            model = model_class(**params)
            result = model.run()
            scenario_results.append(result)

        results[scenario_name] = scenario_results

    return results
```

## 8. 验证工具

```python
def validate_model(model_output, empirical_data, metrics=['mean', 'std', 'distribution']):
    """模型验证"""
    import numpy as np
    from scipy import stats

    validation_results = {}

    if 'mean' in metrics:
        sim_mean = np.mean(model_output)
        emp_mean = np.mean(empirical_data)
        validation_results['mean_error'] = abs(sim_mean - emp_mean) / emp_mean

    if 'std' in metrics:
        sim_std = np.std(model_output)
        emp_std = np.std(empirical_data)
        validation_results['std_error'] = abs(sim_std - emp_std) / emp_std

    if 'distribution' in metrics:
        ks_stat, p_value = stats.ks_2samp(model_output, empirical_data)
        validation_results['ks_statistic'] = ks_stat
        validation_results['ks_p_value'] = p_value

    return validation_results
```

---

## References

- Mesa 3.x 文档: https://mesa.readthedocs.io/
- NetworkX 文档: https://networkx.org/documentation/

---

*最后更新：2026-06-14*
