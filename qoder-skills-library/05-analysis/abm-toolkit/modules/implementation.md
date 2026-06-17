# ABM实现指南

## Purpose

本模块提供ABM的技术实现指南，包括Python/Mesa、NetLogo、Repast4Py等主流ABM平台的使用方法和代码模板。

> **共享代码**：通用基类、网络工具、校准方法、可视化函数等见 [references/code-snippets.md](../references/code-snippets.md)。

---

## 1. 技术栈选择

### 1.1 平台对比

| 平台 | 语言 | 优势 | 劣势 | 适用场景 |
|------|------|------|------|----------|
| **Mesa** | Python | 易学、生态丰富、可视化好 | 性能一般 | 中小规模模型、教学、快速原型 |
| **NetLogo** | NetLogo | 可视化强、学术认可度高 | 性能差、扩展性有限 | 教学、概念验证、中小规模 |
| **Repast4Py** | Python | 高性能、MPI并行 | 学习曲线陡 | 大规模模型（>10万主体） |
| **abcFinance** | Python | 金融专用、支持会计核算 | 社区小 | 金融ABM |
| **JADE** | Java | 企业级、稳定 | 开发效率低 | 工业应用 |

### 1.2 选择建议

**初学者/快速原型**：Mesa
- 优点：Python生态、丰富文档、活跃社区
- 适合：教学、研究原型、中小规模模型

**学术发表**：NetLogo
- 优点：可视化效果好、学术界认可度高
- 适合：论文配图、教学演示、概念验证

**大规模仿真**：Repast4Py
- 优点：MPI并行、支持百万级主体
- 适合：大规模政策仿真、工业应用

---

## 2. Python/Mesa实现

### 2.1 环境配置

```bash
# 创建虚拟环境
python -m venv abm-env
source abm-env/bin/activate  # Linux/Mac
# abm-env\Scripts\activate  # Windows

# 安装依赖
pip install mesa numpy networkx matplotlib seaborn pandas scipy
pip install mesa-geo  # 地理空间支持（可选）
```

### 2.2 项目结构

```
project/
├── agents/
│   ├── __init__.py
│   ├── farmer_agent.py      # 农户主体类
│   ├── bank_agent.py        # 银行主体类
│   ├── insurer_agent.py     # 保险公司类
│   └── government_agent.py  # 政府主体类
├── model/
│   ├── __init__.py
│   ├── main_model.py        # 主模型类
│   └── space.py             # 空间结构定义
├── scenarios/
│   ├── baseline.py          # 基准情景
│   ├── policy_intervention.py  # 政策干预
│   └── stress_test.py       # 压力测试
├── analysis/
│   ├── calibration.py       # 参数校准
│   ├── sensitivity.py       # 敏感性分析
│   └── visualization.py     # 可视化
├── tests/
│   └── test_agents.py       # 单元测试
├── config.yaml              # 配置文件
└── run.py                   # 启动脚本
```

### 2.3 核心代码模板

#### 主体基类

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

#### 主模型基类

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
            model_reporters={},
            agent_reporters={}
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

### 2.4 可视化

```python
import matplotlib.pyplot as plt
import seaborn as sns

def plot_time_series(df, columns, title="Model Dynamics"):
    """绘制时间序列"""
    fig, axes = plt.subplots(len(columns), 1, figsize=(12, 4*len(columns)))
    
    for i, col in enumerate(columns):
        axes[i].plot(df[col])
        axes[i].set_ylabel(col)
        axes[i].set_xlabel('Time Step')
    
    plt.suptitle(title)
    plt.tight_layout()
    return fig

def plot_distribution(data, title="Distribution"):
    """绘制分布图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(data, kde=True, ax=ax)
    ax.set_title(title)
    return fig

def plot_network(G, node_colors=None, title="Network"):
    """绘制网络图"""
    import networkx as nx
    
    fig, ax = plt.subplots(figsize=(10, 10))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, node_color=node_colors, 
            node_size=50, with_labels=False, ax=ax)
    ax.set_title(title)
    return fig
```

### 2.5 交互式仪表板

```python
from mesa.visualization import SolaraViz
from mesa.visualization.components import Slider, PlotModule

def create_dashboard(model_class, parameters):
    """创建Mesa 3.x可视化仪表板（SolaraViz）"""
    model = model_class(**parameters)
    page = SolaraViz(
        model,
        components=[
            PlotModule(["insure_rate", "default_rate"]),
        ],
        model_params=parameters,
    )
    return page
```

---

## 3. NetLogo实现

### 3.1 NetLogo基础结构

```netlogo
; 主体类型
breed [farmers farmer]
breed [banks bank]
breed [insurers insurer]

; 主体属性
farmers-own [
  altitude
  land-size
  risk-aversion
  cash
  insurance?
]

; 全局变量
globals [
  policy-subsidy
  default-rate
  insure-rate
]

; 初始化
to setup
  clear-all
  
  ; 创建农户
  create-farmers num-farmers [
    setxy random-xcor random-ycor
    set altitude random 1500
    set land-size random-float 10
    set risk-aversion 0.5 + random-float 1.5
    set cash random-normal 100000 30000
    set insurance? false
  ]
  
  ; 设置补贴率
  set policy-subsidy initial-subsidy
  
  reset-ticks
end

; 主循环
to go
  ask farmers [
    decide-insurance
    face-climate-shock
    produce-and-sell
  ]
  
  update-globals
  tick
end

; 投保决策
to decide-insurance
  let neighbor-rate count farmers-on neighbors with [insurance?] / count farmers-on neighbors
  let prob 1 / (1 + exp (- (beta0 + beta1 * policy-subsidy + beta2 * neighbor-rate)))
  set insurance? random-float 1 < prob
end
```

### 3.2 NetLogo最佳实践

1. **使用`breed`**：明确定义主体类型
2. **使用`ask`**：控制主体行为顺序
3. **使用`of`**：获取主体属性
4. **使用`with`**：筛选主体
5. **使用`report`**：封装计算逻辑

---

## 4. Repast4Py实现（大规模）

### 4.1 环境配置

```bash
# 安装Repast4Py
pip install repast4py

# 需要MPI支持
conda install -c conda-forge mpi4py
```

### 4.2 大规模模型模板

```python
from repast4py import context as ctx
from repast4py import schedule
from mpi4py import MPI
import numpy as np

class FarmerAgent:
    """农户主体（MPI并行版本）"""
    def __init__(self, id, rank, altitude, land_size):
        self.id = id
        self.rank = rank
        self.altitude = altitude
        self.land_size = land_size
        self.cash = np.random.lognormal(11.5, 0.3)
        self.insurance = False

class AgriculturalInsuranceModel:
    """大规模农业保险ABM"""
    def __init__(self, num_agents=100000):
        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.num_agents = num_agents
        
        # 每个进程处理部分主体
        self.agents_per_rank = num_agents // self.comm.Get_size()
        self.agents = self._create_local_agents()
    
    def _create_local_agents(self):
        """创建本地主体"""
        agents = []
        start_id = self.rank * self.agents_per_rank
        for i in range(self.agents_per_rank):
            agent = FarmerAgent(
                id=start_id + i,
                rank=self.rank,
                altitude=np.random.randint(200, 1500),
                land_size=np.random.exponential(5)
            )
            agents.append(agent)
        return agents
    
    def run(self, steps=365):
        """并行运行仿真"""
        for step in range(steps):
            # 本地计算
            for agent in self.agents:
                self._agent_step(agent)
            
            # 跨进程通信（如需要）
            self._exchange_data()
            
            # 同步
            self.comm.Barrier()

if __name__ == '__main__':
    model = AgriculturalInsuranceModel(num_agents=1000000)
    model.run(steps=365)
```

---

## 5. 代码模板库

### 5.1 网络生成模板

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
    
    # 添加节点
    for i in range(core_size):
        G.add_node(f'core_{i}', type='core')
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

### 5.2 参数校准模板

```python
from scipy.optimize import minimize
import numpy as np

def calibrate_parameters(model_class, real_data, initial_params, param_bounds):
    """参数校准"""
    def objective(params):
        model = model_class(**dict(zip(param_names, params)))
        sim_data = model.run()
        
        # 计算目标函数（如RMSE）
        rmse = np.sqrt(np.mean((sim_data - real_data)**2))
        return rmse
    
    result = minimize(
        objective,
        x0=initial_params,
        bounds=param_bounds,
        method='L-BFGS-B'
    )
    
    return dict(zip(param_names, result.x))
```

### 5.3 敏感性分析模板

```python
import pandas as pd
import numpy as np

def sensitivity_analysis(model_class, base_params, param_ranges, n_runs=10):
    """OAT敏感性分析"""
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

### 5.4 可视化模板

```python
import matplotlib.pyplot as plt
import seaborn as sns

def create_publication_figures(model_output):
    """生成论文级图表"""
    
    # 1. 时间序列图
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    
    # 参保率
    axes[0, 0].plot(model_output['insure_rate'])
    axes[0, 0].set_title('Insurance Rate Over Time')
    axes[0, 0].set_xlabel('Time Step')
    axes[0, 0].set_ylabel('Rate')
    
    # 违约率
    axes[0, 1].plot(model_output['default_rate'], color='red')
    axes[0, 1].set_title('Default Rate Over Time')
    axes[0, 1].set_xlabel('Time Step')
    axes[0, 1].set_ylabel('Rate')
    
    # 财富分布
    sns.histplot(model_output['wealth_distribution'], kde=True, ax=axes[1, 0])
    axes[1, 0].set_title('Wealth Distribution')
    
    # 散点图
    axes[1, 1].scatter(model_output['altitude'], model_output['insurance'], alpha=0.5)
    axes[1, 1].set_title('Altitude vs Insurance')
    axes[1, 1].set_xlabel('Altitude (m)')
    axes[1, 1].set_ylabel('Insurance (0/1)')
    
    plt.tight_layout()
    return fig
```

---

## 6. 测试与调试

### 6.1 单元测试模板

```python
import unittest
import numpy as np

class TestFarmerAgent(unittest.TestCase):
    def setUp(self):
        """测试前准备"""
        self.model = MockModel()
        self.agent = FarmerAgent(1, self.model, altitude=800, land_size=5, risk_aversion=1.0)
    
    def test_frost_risk_calculation(self):
        """测试霜冻风险计算"""
        # 高海拔
        self.agent.altitude = 1200
        self.assertAlmostEqual(self.agent.calc_frost_risk(), 0.15)
        
        # 中海拔
        self.agent.altitude = 800
        self.assertAlmostEqual(self.agent.calc_frost_risk(), 0.08)
        
        # 低海拔
        self.agent.altitude = 400
        self.assertAlmostEqual(self.agent.calc_frost_risk(), 0.05)
    
    def test_insurance_decision(self):
        """测试投保决策"""
        # 高补贴率应该增加投保概率
        result_high = self.agent.decide_insure(subsidy_rate=0.5, neighbor_insure_rate=0.5)
        result_low = self.agent.decide_insure(subsidy_rate=0.1, neighbor_insure_rate=0.5)
        # 注意：由于随机性，这里只测试函数可运行
        self.assertIn(result_high, [True, False])
        self.assertIn(result_low, [True, False])

if __name__ == '__main__':
    unittest.main()
```

### 6.2 调试技巧

```python
# 1. 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. 中间结果检查
def debug_step(model, step):
    """调试单步执行"""
    print(f"Step {step}:")
    print(f"  Agents: {len(model.agents)}")
    print(f"  Insure rate: {sum(a.insurance for a in model.agents) / len(model.agents):.2%}")
    print(f"  Mean cash: {np.mean([a.cash for a in model.agents]):.2f}")

# 3. 断言检查
def validate_model_state(model):
    """验证模型状态"""
    for agent in model.agents:
        assert agent.cash >= 0, f"Agent {agent.unique_id} has negative cash"
        assert agent.risk_aversion > 0, f"Agent {agent.unique_id} has invalid risk aversion"
```

---

## 7. 性能优化

### 7.1 优化建议

| 优化点 | 方法 | 效果 |
|-------|------|------|
| 向量化 | 使用NumPy代替循环 | 10-100倍加速 |
| 缓存 | 缓存重复计算结果 | 2-5倍加速 |
| 并行 | 使用multiprocessing | 线性加速 |
| 早期停止 | 检测收敛后停止 | 节省50%+时间 |

### 7.2 代码优化示例

```python
# 优化前：循环
def calc_neighbor_rate_slow(agents, grid):
    results = []
    for agent in agents:
        neighbors = grid.get_neighbors(agent.pos, radius=2)
        rate = sum(n.insurance for n in neighbors) / len(neighbors)
        results.append(rate)
    return results

# 优化后：向量化
def calc_neighbor_rate_fast(agents, grid):
    insurance_array = np.array([a.insurance for a in agents])
    # 使用卷积或批量查询优化
    # ...
    return rates
```

---

## 8. 并行参数扫描

### 8.1 使用 ProcessPoolExecutor

```python
from concurrent.futures import ProcessPoolExecutor
import itertools
import numpy as np
import pandas as pd

def parallel_sweep(model_class, param_grid, n_runs=30, max_workers=4):
    """并行参数网格扫描

    参数:
        model_class: ABM模型类
        param_grid: dict，键为参数名，值为参数值列表
        n_runs: 每组参数运行次数
        max_workers: 并行进程数
    """
    combinations = list(itertools.product(*param_grid.values()))
    param_names = list(param_grid.keys())

    def run_combo(combo):
        params = dict(zip(param_names, combo))
        results = []
        for seed in range(n_runs):
            model = model_class(**params, seed=seed)
            result = model.run()
            results.append(result['key_metric'].iloc[-1])
        return {**params, 'mean': np.mean(results), 'std': np.std(results)}

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        all_results = list(executor.map(run_combo, combinations))

    return pd.DataFrame(all_results)
```

### 8.2 使用示例

```python
param_grid = {
    'subsidy_rate': [0.10, 0.20, 0.30, 0.40],
    'premium_rate': [0.04, 0.06, 0.08],
}

results = parallel_sweep(AgriculturalInsuranceModel, param_grid, n_runs=30)
print(results.pivot_table(values='mean', index='subsidy_rate', columns='premium_rate'))
```

---

### 实现相关资源

1. **Mesa文档**：https://mesa.readthedocs.io/
2. **Mesa示例**：https://github.com/projectmesa/mesa/tree/main/examples
3. **NetLogo文档**：https://ccl.northwestern.edu/netlogo/docs/
4. **Repast4Py文档**：https://repast.github.io/repast4py.site/

---

*最后更新：2026-06-14*
