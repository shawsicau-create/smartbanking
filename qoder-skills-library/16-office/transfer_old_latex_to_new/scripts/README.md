# Scripts 目录

本目录包含 `transfer_old_latex_to_new` 技能的可执行脚本。

## 脚本列表

### `run.py` - 主执行入口

完整的 MVP 闭环脚本,支持四个核心命令:

```bash
# 分析结构差异并生成迁移计划
python scripts/run.py analyze --old <旧项目> --new <新项目>

# 执行迁移(写入新项目)
python scripts/run.py apply --run-id <run_id> --old <旧项目> --new <新项目>

# 编译验证
python scripts/run.py compile --run-id <run_id> --new <新项目>

# 回滚恢复
python scripts/run.py restore --run-id <run_id> --new <新项目>
```

**详细文档**: 见 [../SKILL.md](../SKILL.md)

补充：P1 起 `run.py` 增加了 `runs list/show/delete` 子命令，用于管理 runs（迁移历史可追溯）。

---

### `migrate.sh` - 一键迁移脚本

对 `run.py` 的简单封装：`analyze → apply → (可选) compile`。

```bash
# 最小用法：一键迁移
bash scripts/migrate.sh --old <旧项目> --new <新项目>

# 将 runs 输出隔离到指定目录（建议：测试/CI 使用）
bash scripts/migrate.sh --old <旧项目> --new <新项目> --runs-root /path/to/runs
```

**适用场景**:
- 不想手动复制粘贴 run_id
- 需要“一条命令跑完整流程”
- 希望把 runs 输出放到指定目录（保持项目干净）

---

### `validate_config.py` - 配置校验工具（P1）

用于提前发现 `config.yaml` 常见配置错误（类型、范围、关键字段组合等）。

```bash
python scripts/validate_config.py

# 可选：应用 profile 再校验
python scripts/validate_config.py --profile balanced

# 可选：打印最终合并后的配置（调试）
python scripts/validate_config.py --print-effective
```

---

### `demo.py` - 核心功能演示

演示三大核心功能的独立脚本:

1. **字数自动适配** - `WordCountAdapter`
2. **引用强制保护** - `ReferenceGuardian`
3. **AI 内容智能优化** - `ContentOptimizer`

```bash
# 运行演示
python scripts/demo.py
```

**输出示例**:
```
🚀 LaTeX 标书智能迁移技能 - 核心功能演示
📊 演示：字数自动适配
   当前字数: 1800
   旧版本要求: 2000 字
   新版本要求: 1500 字
   是否需要适配: 是
...
```

**适用场景**:
- 新功能快速验证
- 向用户展示功能特性
- 开发调试

---

### `quicktest.py` - 快速测试工具

简单的单元测试运行器,不依赖 pytest 环境:

```bash
# 运行快速测试
python scripts/quicktest.py
```

**测试覆盖**:
- WordCountAdapter 字数统计与报告
- ReferenceGuardian 引用保护与恢复
- ContentOptimizer 内容分析与优化
- AIIntegration 异步集成

**适用场景**:
- 快速验证模块可用性
- 无 pytest 环境时的基础测试
- CI/CD 轻量级检查

**注意**: 完整的测试套件在 [../tests/](../tests/) 目录,使用 pytest 运行:
```bash
pytest tests/
```

---

## 使用建议

| 场景 | 推荐脚本 |
|------|---------|
| **生产使用** | `run.py` |
| **功能演示** | `demo.py` |
| **快速验证** | `quicktest.py` |
| **完整测试** | `pytest tests/` |

---

**最后更新**: 2026-01-08
