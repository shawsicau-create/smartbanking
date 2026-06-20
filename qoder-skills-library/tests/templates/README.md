# 技能测试模板

本目录包含用于测试Qoder技能的标准化模板。

## 文件说明

- `test_skill_loading.py` - 技能加载测试模板
- `conftest.py` - 测试配置和夹具
- `pytest.ini` - pytest配置文件

## 使用方法

### 1. 复制模板到技能目录

```bash
# 复制测试模板到目标技能目录
cp -r tests/templates/* qoder-skills-library/NN-category/skill-name/tests/
```

### 2. 运行测试

```bash
# 进入技能目录
cd qoder-skills-library/NN-category/skill-name

# 运行测试
pytest

# 运行特定测试
pytest tests/test_skill_loading.py

# 运行带标记的测试
pytest -m "not slow"
```

### 3. 自定义测试

根据需要修改 `test_skill_loading.py` 文件，添加特定于技能的测试。

## 测试覆盖

测试模板包含以下测试：

1. **目录结构测试**
   - 技能目录是否存在
   - SKILL.md文件是否存在

2. **前置数据测试**
   - 是否包含YAML前置数据
   - 是否包含必需字段
   - 字段格式是否正确

3. **内容质量测试**
   - 技能名称是否与目录匹配
   - 工作流阶段是否有效
   - 兼容性平台是否有效
   - 版本号格式是否正确
   - 标签格式是否正确
   - 描述是否符合要求
   - 正文内容是否充分

## 最佳实践

1. **测试覆盖率** - 目标至少50%的测试覆盖率
2. **测试命名** - 使用描述性的测试名称
3. **测试隔离** - 每个测试应该独立运行
4. **测试速度** - 保持测试快速运行
5. **测试维护** - 定期更新测试以反映技能变化

## 故障排除

### 测试失败

1. 检查SKILL.md文件格式是否正确
2. 检查必需字段是否完整
3. 检查字段格式是否符合规范

### 测试跳过

1. 确保使用了正确的pytest.ini配置
2. 检查测试发现路径是否正确

## 更多信息

- [pytest文档](https://docs.pytest.org/)
- [Qoder技能规范](../SKILL_TEMPLATE.md)
- [技能开发指南](../19-devtools/create-skill/SKILL.md)
