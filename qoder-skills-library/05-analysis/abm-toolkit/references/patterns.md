# ABM建模模式库

## Purpose

本文档提供ABM建模的常用设计模式，帮助研究者快速构建高质量的ABM模型。

---

## 1. 主体设计模式

### 1.1 状态机模式（State Machine）

**适用场景**：主体行为有明确的状态转换

```python
class StateMachineAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.state = 'initial'
        self.transitions = {
            'initial': {'trigger': self.should_activate, 'target': 'active'},
            'active': {'trigger': self.should_complete, 'target': 'completed'},
            'completed': {'trigger': lambda: False, 'target': 'completed'}
        }
    
    def step(self):
        transition = self.transitions[self.state]
        if transition['trigger']():
            self.state = transition['target']
```

### 1.2 信念-欲望-意图模式（BDI）

**适用场景**：主体有复杂的认知过程

```python
class BDIAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.beliefs = {}  # 信念
        self.desires = []  # 欲望
        self.intentions = []  # 意图
    
    def update_beliefs(self, perceptions):
        """更新信念"""
        for key, value in perceptions.items():
            self.beliefs[key] = value
    
    def generate_desires(self):
        """生成欲望"""
        self.desires = []
        if self.beliefs.get('income', 0) < self.beliefs.get('target_income', 0):
            self.desires.append('increase_income')
    
    def select_intentions(self):
        """选择意图"""
        self.intentions = []
        for desire in self.desires:
            if self.can_achieve(desire):
                self.intentions.append(desire)
    
    def execute(self):
        """执行意图"""
        for intention in self.intentions:
            self.execute_intention(intention)
```

### 1.3 学习主体模式（Learning Agent）

**适用场景**：主体需要从经验中学习

```python
class LearningAgent(Agent):
    def __init__(self, model):
        super().__init__(model)
        self.q_table = {}  # Q-learning表
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.1
    
    def choose_action(self, state):
        """选择动作（探索-利用权衡）"""
        if np.random.random() < self.exploration_rate:
            return np.random.choice(self.actions)
        else:
            return self.best_action(state)
    
    def learn(self, state, action, reward, next_state):
        """学习更新"""
        current_q = self.q_table.get((state, action), 0)
        max_next_q = max([self.q_table.get((next_state, a), 0) for a in self.actions])
        new_q = current_q + self.learning_rate * (reward + self.discount_factor * max_next_q - current_q)
        self.q_table[(state, action)] = new_q
```

---

## 2. 交互模式

### 2.1 市场交易模式（Market Transaction）

**适用场景**：主体间进行买卖交易

```python
class Market:
    def __init__(self):
        self.buyers = []
        self.sellers = []
    
    def add_buyer(self, buyer, price, quantity):
        self.buyers.append({'agent': buyer, 'price': price, 'quantity': quantity})
    
    def add_seller(self, seller, price, quantity):
        self.sellers.append({'agent': seller, 'price': price, 'quantity': quantity})
    
    def match(self):
        """匹配买卖双方"""
        self.buyers.sort(key=lambda x: -x['price'])  # 买家按价格降序
        self.sellers.sort(key=lambda x: x['price'])   # 卖家按价格升序
        
        trades = []
        for buyer in self.buyers:
            for seller in self.sellers:
                if buyer['price'] >= seller['price'] and buyer['quantity'] > 0 and seller['quantity'] > 0:
                    trade_quantity = min(buyer['quantity'], seller['quantity'])
                    trade_price = (buyer['price'] + seller['price']) / 2
                    
                    trades.append({
                        'buyer': buyer['agent'],
                        'seller': seller['agent'],
                        'price': trade_price,
                        'quantity': trade_quantity
                    })
                    
                    buyer['quantity'] -= trade_quantity
                    seller['quantity'] -= trade_quantity
        
        return trades
```

### 2.2 网络扩散模式（Network Diffusion）

**适用场景**：信息、行为、疾病在网络中扩散

```python
def network_diffusion(model, seed_nodes, diffusion_prob=0.1):
    """网络扩散过程"""
    infected = set(seed_nodes)
    newly_infected = set()
    
    for node in infected:
        neighbors = model.grid.get_neighbors(node, include_center=False)
        for neighbor in neighbors:
            if neighbor not in infected and np.random.random() < diffusion_prob:
                newly_infected.add(neighbor)
    
    infected.update(newly_infected)
    return infected
```

### 2.3 协商模式（Negotiation）

**适用场景**：主体间进行多轮协商

```python
def negotiate(buyer, seller, max_rounds=10):
    """简单协商协议"""
    buyer_price = buyer.initial_offer
    seller_price = seller.initial_offer
    
    for round in range(max_rounds):
        if buyer_price >= seller_price:
            # 达成协议
            return (buyer_price + seller_price) / 2
        
        # 双方让步
        buyer_price += buyer.step_size
        seller_price -= seller.step_size
    
    return None  # 协商失败
```

---

## 3. 环境模式

### 3.1 空间网格模式（Spatial Grid）

**适用场景**：主体在二维空间中移动和交互

```python
from mesa.space import MultiGrid

class SpatialModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, torus=False)
    
    def place_agent(self, agent, pos):
        """放置主体"""
        self.grid.place_agent(agent, pos)
    
    def move_agent(self, agent, new_pos):
        """移动主体"""
        self.grid.move_agent(agent, new_pos)
    
    def get_neighbors(self, agent, radius=1):
        """获取邻居"""
        return self.grid.get_neighbors(agent.pos, radius=radius, include_center=False)
```

### 3.2 网络环境模式（Network Environment）

**适用场景**：主体在网络节点上交互

```python
import networkx as nx

class NetworkEnvironment:
    def __init__(self, G):
        self.G = G
        self.agent_positions = {}  # agent_id -> node
    
    def place_agent(self, agent, node):
        self.agent_positions[agent.unique_id] = node
    
    def get_neighbors(self, agent):
        node = self.agent_positions[agent.unique_id]
        neighbor_nodes = self.G.neighbors(node)
        return [self.get_agent_at(n) for n in neighbor_nodes]
    
    def move_agent(self, agent, new_node):
        self.agent_positions[agent.unique_id] = new_node
```

### 3.3 资源环境模式（Resource Environment）

**适用场景**：主体在环境中收集或消耗资源

```python
class ResourceEnvironment:
    def __init__(self, width, height, resource_regeneration_rate=0.01):
        self.width = width
        self.height = height
        self.resources = np.random.rand(width, height) * 100
        self.regeneration_rate = resource_regeneration_rate
    
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
```

---

## 4. 调度模式

### 4.1 随机激活（Random Activation）

**适用场景**：主体执行顺序随机（Mesa 3.x 默认行为）

```python
class RandomModel(Model):
    def __init__(self):
        super().__init__()
    
    def step(self):
        self.agents.shuffle_do("step")  # 随机顺序激活所有主体
```

### 4.2 同时激活（Simultaneous Activation）

**适用场景**：所有主体同时决策，然后同时更新

```python
class SimultaneousModel(Model):
    def __init__(self):
        super().__init__()
    
    def step(self):
        self.agents.do("step")  # 同时激活所有主体
```

### 4.3 分层激活（Staged Activation）

**适用场景**：不同类型的主体在不同阶段执行

```python
from mesa import Agent

class StagedModel(Model):
    def __init__(self):
        super().__init__()
    
    def step(self):
        # 按主体类型分阶段执行
        for agent_type in [FarmerAgent, BankAgent, GovernmentAgent]:
            self.agents.select(lambda a: isinstance(a, agent_type)).do("step")
```

---

## 5. 数据收集模式

### 5.1 数据收集器模式（DataCollector）

**适用场景**：收集模型和主体层面的数据

```python
from mesa.datacollection import DataCollector

class DataCollectionModel(Model):
    def __init__(self):
        self.datacollector = DataCollector(
            model_reporters={
                "gini": self.calculate_gini,
                "total_wealth": lambda m: sum(a.wealth for a in m.agents)
            },
            agent_reporters={
                "wealth": lambda a: a.wealth,
                "state": lambda a: a.state
            }
        )
    
    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)
    
    def get_results(self):
        model_data = self.datacollector.get_model_vars_dataframe()
        agent_data = self.datacollector.get_agent_vars_dataframe()
        return model_data, agent_data
```

### 5.2 快照模式（Snapshot）

**适用场景**：保存模型状态用于后续分析

```python
import pickle

def save_snapshot(model, filename):
    """保存模型快照"""
    state = {
        'step': model.steps,
        'agents': [{
            'id': a.unique_id,
            'state': a.state,
            'pos': a.pos
        } for a in model.agents],
        'random_state': np.random.get_state()
    }
    with open(filename, 'wb') as f:
        pickle.dump(state, f)

def load_snapshot(model, filename):
    """加载模型快照"""
    with open(filename, 'rb') as f:
        state = pickle.load(f)
    
    model.steps = state['step']
    # 恢复主体状态...
```

---

## 6. 验证模式

### 6.1 基准测试模式（Benchmark）

**适用场景**：与已知结果对比验证

```python
def benchmark_test(model_class, params, expected_results, tolerance=0.05):
    """基准测试"""
    model = model_class(**params)
    results = model.run()
    
    for metric, expected in expected_results.items():
        actual = results[metric].iloc[-1]
        if abs(actual - expected) / expected > tolerance:
            print(f"FAIL: {metric} expected {expected}, got {actual}")
            return False
    
    print("PASS: All metrics within tolerance")
    return True
```

### 6.2 敏感性分析模式（Sensitivity Analysis）

**适用场景**：检验参数变化对结果的影响

> 统一的敏感性分析函数见 [code-snippets.md §5](code-snippets.md)。

---

## References

- **设计模式**：Gamma, E., et al. (1994). Design Patterns: Elements of Reusable Object-Oriented Software.
- **ABM模式**：Railsback, S.F. & Grimm, V. (2019). Agent-Based and Individual-Based Modeling.

---

*最后更新：2026-06-14*
