# ABM验证规则

## Purpose

本文档提供ABM模型验证的严格规则和约束，用于验证用户输入和模型设计的客观性。

---

## 1. 模型设计验证规则

### 1.1 ODD协议完整性

**规则**：ODD协议必须包含所有必要部分

**检查项**：
```yaml
overview:
  - [ ] 模型目的明确
  - [ ] 主体类型定义完整
  - [ ] 空间结构描述清晰
  
design_concepts:
  - [ ] 涌现现象定义
  - [ ] 适应机制描述
  - [ ] 学习机制描述
  - [ ] 交互机制描述
  - [ ] 异质性描述
  - [ ] 随机性描述
  
details:
  - [ ] 初始化过程
  - [ ] 输入数据来源
  - [ ] 子程序描述
```

### 1.2 主体类型定义

**规则**：每个主体类型必须有明确的属性和行为

**检查项**：
```yaml
agent_definition:
  - [ ] 名称清晰（如FarmerAgent, BankAgent）
  - [ ] 属性列表完整
  - [ ] 行为规则明确
  - [ ] 决策逻辑可解释
```

**验证函数**：
```python
def validate_agent_definition(agent_class):
    """验证主体定义（Mesa 3.x）"""
    from mesa import Agent
    assert issubclass(agent_class, Agent), "Must inherit from mesa.Agent"
    assert hasattr(agent_class, 'step'), "Missing step() method"
```

### 1.3 空间结构定义

**规则**：空间结构必须与研究问题匹配

**检查项**：
```yaml
spatial_structure:
  - [ ] 空间类型选择合理（网格/网络/地理）
  - [ ] 空间维度明确
  - [ ] 边界条件定义
  - [ ] 邻居定义清晰
```

---

## 2. 参数验证规则

### 2.1 参数来源验证

**规则**：每个参数必须有明确来源

**优先级**：
1. 实证数据校准（最高）
2. 计量估计值
3. 文献引用
4. 专家判断
5. 理论推导（最低）

**验证函数**：
```python
def validate_parameter_source(param_name, source_type, source_reference):
    """验证参数来源"""
    valid_source_types = ['empirical', 'econometric', 'literature', 'expert', 'theoretical']
    
    assert source_type in valid_source_types, f"Invalid source type: {source_type}"
    
    if source_type == 'literature':
        assert source_reference is not None, "Literature source must have reference"
        # 验证引用格式
        assert 'author' in source_reference, "Reference must have author"
        assert 'year' in source_reference, "Reference must have year"
        assert 'title' in source_reference, "Reference must have title"
```

### 2.2 参数范围验证

**规则**：参数必须在合理范围内

**常见参数范围**：
```python
PARAMETER_RANGES = {
    # 农户参数
    'risk_aversion': (0.1, 5.0),  # CRRA系数
    'discount_rate': (0.0, 0.3),  # 折现率
    'initial_assets': (0, 1e8),  # 初始资产
    
    # 保险参数
    'premium_rate': (0.0, 1.0),  # 保费率
    'subsidy_rate': (0.0, 1.0),  # 补贴率
    'coverage_ratio': (0.0, 1.0),  # 保障比例
    
    # 市场参数
    'interest_rate': (0.0, 0.5),  # 利率
    'inflation_rate': (-0.1, 0.5),  # 通胀率
    
    # 模型参数
    'num_agents': (10, 10000000),  # 主体数量
    'simulation_steps': (1, 100000),  # 仿真步数
}

def validate_parameter_range(param_name, value):
    """验证参数范围"""
    if param_name in PARAMETER_RANGES:
        min_val, max_val = PARAMETER_RANGES[param_name]
        assert min_val <= value <= max_val, \
            f"Parameter {param_name} = {value} out of range [{min_val}, {max_val}]"
```

### 2.3 参数一致性验证

**规则**：相关参数必须一致

**检查项**：
```python
def validate_parameter_consistency(params):
    """验证参数一致性"""
    
    # 1. 补贴率+自付比例=1
    if 'subsidy_rate' in params and 'farmer_share' in params:
        assert abs(params['subsidy_rate'] + params['farmer_share'] - 1.0) < 0.01, \
            "Subsidy rate + farmer share should equal 1"
    
    # 2. 保费率 < 保障比例
    if 'premium_rate' in params and 'coverage_ratio' in params:
        assert params['premium_rate'] < params['coverage_ratio'], \
            "Premium rate should be less than coverage ratio"
    
    # 3. 利率 > 0
    if 'interest_rate' in params:
        assert params['interest_rate'] >= 0, "Interest rate should be non-negative"
```

---

## 3. 模型行为验证规则

### 3.1 边界条件验证

**规则**：模型在边界条件下必须行为合理

**检查项**：
```python
def validate_boundary_conditions(model_class, base_params):
    """验证边界条件"""
    
    # 1. 零冲击下系统稳定
    params = base_params.copy()
    params['shock_intensity'] = 0
    model = model_class(**params)
    results = model.run(steps=100)
    assert results['system_stability'].iloc[-1] > 0.9, "System should be stable without shocks"
    
    # 2. 最大冲击下系统不崩溃
    params['shock_intensity'] = 1.0
    model = model_class(**params)
    results = model.run(steps=100)
    # 系统可能恶化但不应完全崩溃
    assert results['default_rate'].iloc[-1] < 1.0, "System should not completely collapse"
    
    # 3. 零主体数量
    params['num_agents'] = 0
    try:
        model = model_class(**params)
        assert False, "Should raise error for zero agents"
    except ValueError:
        pass  # 预期行为
```

### 3.2 守恒定律验证

**规则**：模型必须遵守守恒定律（如资金守恒）

**检查项**：
```python
def validate_conservation_laws(model_class, base_params):
    """验证守恒定律"""
    model = model_class(**base_params)
    
    # 记录初始总资金
    initial_total_cash = sum(a.cash for a in model.agents)
    
    # 运行模型
    for _ in range(100):
        model.step()
    
    # 计算最终总资金
    final_total_cash = sum(a.cash for a in model.agents)
    
    # 资金应守恒（允许小的数值误差）
    assert abs(final_total_cash - initial_total_cash) / initial_total_cash < 0.01, \
        f"Cash not conserved: initial={initial_total_cash}, final={final_total_cash}"
```

### 3.3 涌现行为验证

**规则**：模型必须产生预期的涌现行为

**检查项**：
```python
def validate_emergent_behavior(model_class, base_params, expected_patterns):
    """验证涌现行为"""
    model = model_class(**base_params)
    results = model.run(steps=1000)
    
    for pattern_name, pattern_check in expected_patterns.items():
        assert pattern_check(results), f"Expected pattern '{pattern_name}' not observed"
```

---

## 4. 结果验证规则

### 4.1 统计显著性验证

**规则**：结果必须具有统计显著性

**检查项**：
```python
def validate_statistical_significance(results, confidence_level=0.95):
    """验证统计显著性"""
    from scipy import stats
    
    # 计算置信区间
    mean = np.mean(results)
    std = np.std(results)
    n = len(results)
    
    # t检验
    t_value = stats.t.ppf((1 + confidence_level) / 2, n - 1)
    margin_of_error = t_value * std / np.sqrt(n)
    
    ci_lower = mean - margin_of_error
    ci_upper = mean + margin_of_error
    
    # 置信区间不应包含零（如果检验效应是否存在）
    # 或者置信区间应足够窄（如果检验效应大小）
    return ci_lower, ci_upper
```

### 4.2 稳健性验证

**规则**：结果必须在不同条件下稳健

**检查项**：
```python
def validate_robustness(model_class, base_params, robustness_checks):
    """验证稳健性"""
    baseline_results = run_model(model_class, base_params)
    
    for check_name, check_params in robustness_checks.items():
        modified_params = {**base_params, **check_params}
        modified_results = run_model(model_class, modified_params)
        
        # 检查定性结论是否一致
        baseline_conclusion = extract_conclusion(baseline_results)
        modified_conclusion = extract_conclusion(modified_results)
        
        assert baseline_conclusion == modified_conclusion, \
            f"Robustness check '{check_name}' failed: conclusions differ"
```

### 4.3 可复现性验证

**规则**：结果必须可复现

**检查项**：
```python
def validate_reproducibility(model_class, base_params, n_runs=30):
    """验证可复现性"""
    results = []
    
    for i in range(n_runs):
        model = model_class(**base_params, seed=i)
        result = model.run()
        results.append(result)
    
    # 计算变异系数
    means = [r['key_metric'].iloc[-1] for r in results]
    cv = np.std(means) / np.mean(means)
    
    # 变异系数应小于阈值
    assert cv < 0.1, f"Coefficient of variation too high: {cv}"
```

---

## 5. 代码质量验证规则

### 5.1 代码规范验证

**规则**：代码必须符合编码规范

**检查项**：
```python
def validate_code_quality(code_file):
    """验证代码质量"""
    import ast
    
    with open(code_file, 'r') as f:
        tree = ast.parse(f.read())
    
    # 1. 检查函数长度
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if len(node.body) > 50:
                print(f"Warning: Function '{node.name}' is too long ({len(node.body)} lines)")
    
    # 2. 检查类定义
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            if not node.name[0].isupper():
                print(f"Warning: Class '{node.name}' should start with uppercase")
    
    # 3. 检查文档字符串
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            if not ast.get_docstring(node):
                print(f"Warning: '{node.name}' missing docstring")
```

### 5.2 单元测试验证

**规则**：核心功能必须有单元测试

**检查项**：
```python
def validate_unit_tests(test_file):
    """验证单元测试覆盖"""
    import unittest
    
    # 运行测试
    loader = unittest.TestLoader()
    suite = loader.discover('.', pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # 检查测试通过率
    pass_rate = result.testsRun / (result.testsRun + len(result.failures) + len(result.errors))
    
    assert pass_rate > 0.9, f"Test pass rate too low: {pass_rate}"
    
    return result
```

---

## 6. 论文写作验证规则

### 6.1 方法描述验证

**规则**：论文必须包含完整的方法描述

**检查项**：
```yaml
method_section:
  - [ ] ODD协议完整
  - [ ] 伪代码提供
  - [ ] 参数表完整
  - [ ] 数据来源说明
  - [ ] 验证方法描述
```

### 6.2 结果呈现验证

**规则**：结果必须清晰呈现

**检查项**：
```yaml
results_section:
  - [ ] 图表清晰
  - [ ] 图注完整
  - [ ] 统计检验报告
  - [ ] 置信区间提供
  - [ ] 敏感性分析报告
```

### 6.3 讨论部分验证

**规则**：讨论必须充分

**检查项**：
```yaml
discussion_section:
  - [ ] 结果解释清晰
  - [ ] 局限性讨论
  - [ ] 政策建议
  - [ ] 未来研究方向
```

---

## 7. 验证流程

### 7.1 验证步骤

```
1. 设计验证
   ├── ODD协议完整性检查
   ├── 主体定义检查
   └── 空间结构检查

2. 参数验证
   ├── 参数来源检查
   ├── 参数范围检查
   └── 参数一致性检查

3. 行为验证
   ├── 边界条件检查
   ├── 守恒定律检查
   └── 涌现行为检查

4. 结果验证
   ├── 统计显著性检查
   ├── 稳健性检查
   └── 可复现性检查

5. 代码验证
   ├── 代码规范检查
   └── 单元测试检查
```

### 7.2 验证报告模板

```markdown
# 验证报告

## 1. 模型概述
- 模型名称：[名称]
- 验证日期：[日期]
- 验证人员：[姓名]

## 2. 验证结果

### 2.1 设计验证
- [ ] ODD协议完整性：通过/未通过
- [ ] 主体定义：通过/未通过
- [ ] 空间结构：通过/未通过

### 2.2 参数验证
- [ ] 参数来源：通过/未通过
- [ ] 参数范围：通过/未通过
- [ ] 参数一致性：通过/未通过

### 2.3 行为验证
- [ ] 边界条件：通过/未通过
- [ ] 守恒定律：通过/未通过
- [ ] 涌现行为：通过/未通过

### 2.4 结果验证
- [ ] 统计显著性：通过/未通过
- [ ] 稳健性：通过/未通过
- [ ] 可复现性：通过/未通过

## 3. 问题记录
- [问题1描述]
- [问题2描述]

## 4. 建议
- [建议1]
- [建议2]

## 5. 结论
[总体评估]
```

---

## References

- **验证方法**：Grimm, V., et al. (2006). A standard protocol for describing individual-based and agent-based models.
- **统计检验**：Scipy文档：https://docs.scipy.org/doc/scipy/reference/stats.html

---

*最后更新：2026-06-14*
