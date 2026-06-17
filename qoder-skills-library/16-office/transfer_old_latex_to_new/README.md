# LaTeX 标书智能迁移器

**技能名称**: `migrating-latex-templates`
**版本**: v1.4.1
**最后更新**: 2026-01-29

---

## 📖 这是什么？

**LaTeX 标书智能迁移器**是国自然科学基金（NSFC）标书跨版本迁移的 AI 助手。当你需要：

- 把旧版标书迁移到新版模板
- 不同版本的 NSFC 模板互相转换
- 应对模板结构变化（章节拆分、合并、新增）

**只需一句话**，AI 会自动完成结构分析、内容迁移、格式调整、编译验证。

---

## 🎯 核心能力

| 能力 | 说明 |
|------|------|
| **映射推断** | AIIntegration（可选）+ 启发式回退（文件名匹配/包含/Jaccard） |
| **资源文件智能处理** | 自动扫描、复制、验证资源文件（图片、代码等），保证引用完整性 |
| **自动识别版本** | 自动识别各年份 NSFC 模板版本 |
| **迁移任务生成** | 生成一对一复制/新增占位符/需人工处理（低置信度）任务 |
| **内容零丢失** | 无法自动迁移的内容会标记，确保不遗漏 |
| **一键恢复** | 迁移前自动备份，不满意可随时回滚 |
| **编译验证** | 自动运行 LaTeX 4步法编译，确保生成 PDF |

---

## 💡 如何使用

直接告诉 AI 你的需求：

```
请使用 migrating-latex-templates 迁移标书：
- 旧项目：/Users/xxx/Documents/NSFC_Old
- 新项目：/Users/xxx/Documents/NSFC_New
```

AI 会自动执行迁移并输出结果。

也可以直接使用脚本一键迁移（推荐）：

```bash
bash scripts/migrate.sh --old /path/to/NSFC_2025 --new /path/to/NSFC_2026
```

---

## 🔧 环境要求

### Python 环境

```bash
python --version  # 需要 >= 3.8
```

### LaTeX 环境

**macOS**:
```bash
brew install --cask mactex
```

**Ubuntu/Debian**:
```bash
sudo apt-get install texlive-full
```

**Windows**:
下载并安装 TeX Live: https://tug.org/texlive/

### 验证安装

```bash
xelatex --version
bibtex --version
```

---

## 📥 输入

迁移前需要准备：

| 输入项 | 说明 | 示例 |
|--------|------|------|
| **旧项目路径** | 旧版本标书所在目录的**绝对路径** | `/Users/xxx/Documents/NSFC_Old/` |
| **新项目路径** | 新模板项目的**绝对路径**（需提前创建） | `/Users/xxx/Documents/NSFC_New/` |

**要求**：
- 两个目录都必须存在且可访问

---

## 📤 输出

迁移完成后，会在 `skills/transfer_old_latex_to_new/runs/<run_id>/` 目录生成：

### 核心交付物

| 文件 | 说明 |
|------|------|
| **deliverables/migrated_proposal.pdf** | 迁移后的标书 PDF |
| **deliverables/change_summary.md** | 变更摘要（哪些章节迁移了） |
| **deliverables/structure_comparison.md** | 结构对比报告 |
| **deliverables/unmapped_old_content.md** | 未映射的旧内容（需人工处理） |
| **deliverables/restore_guide.md** | 恢复指南 |

### 分析与日志

| 目录/文件 | 说明 |
|-----------|------|
| **analysis/** | 结构分析 JSON（章节树、差异分析） |
| **plan/** | 迁移计划 JSON |
| **logs/** | 执行日志（apply_result.json） |
| **backup/** | Apply 前的新项目快照（用于恢复） |

---

## ⚠️ 重要说明

### 迁移前

- ✅ 新项目需要提前创建好

### 迁移中

- ✅ AI 只修改新项目的 `extraTex/*.tex` 内容文件
- ✅ AI 会自动备份新项目的内容文件（可随时恢复）
- ❌ 绝不修改 `main.tex`、`@config.tex`、`.cls`、`.sty` 等系统文件

### 迁移后

- ✅ 通读生成的 PDF，检查逻辑连贯性
- ✅ 重点查看 `unmapped_old_content.md`（如有未迁移的内容）
- ⚠️ 部分内容可能需要人工润色

---

## 📖 参考文档

| 文档 | 路径 | 说明 |
|------|------|------|
| **版本差异指南** | [references/version_differences_2025_2026.md](references/version_differences_2025_2026.md) | 2025→2026 结构变化详解 |
| **映射指南** | [references/structure_mapping_guide.md](references/structure_mapping_guide.md) | 章节映射决策参考 |
| **迁移模式库** | [references/migration_patterns.md](references/migration_patterns.md) | 常见迁移模式案例 |
| **快速开始** | [references/quickstart.md](references/quickstart.md) | 命令速查与 runs 目录说明 |
| **配置指南** | [references/config_guide.md](references/config_guide.md) | config.yaml 关键块说明 |
| **接口参考** | [references/api_reference.md](references/api_reference.md) | CLI/模块/产物格式 |
| **故障排除** | [references/troubleshooting.md](references/troubleshooting.md) | 常见问题与处理建议 |
| **FAQ** | [references/faq.md](references/faq.md) | 高频问题速查 |
| **迁移案例** | [references/case_study_2025_to_2026.md](references/case_study_2025_to_2026.md) | 2025→2026 迁移流程示例 |

---

## 📋 版本与变更

**当前版本**: v1.4.1（与 [config.yaml](config.yaml) 同步）

**变更记录**: 见根级 [CHANGELOG.md](../../../CHANGELOG.md)

---

**最后更新**: 2026-01-29
**维护者**: AI Agent (Claude Code)
