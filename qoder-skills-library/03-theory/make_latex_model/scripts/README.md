# make_latex_model 辅助工具集

本目录包含 `make_latex_model` 技能的辅助工具，包括样式分析、标题对比、验证器系统、优化流程和跨平台支持。

## 工具清单

### 0. check_state.py - 项目状态检查工具

**功能**: AI 执行优化前的预检查工具，了解项目当前状态

**使用方法**:
```bash
# 检查项目状态
python3 scripts/check_state.py projects/NSFC_Young
```

**输出内容**:
- ✅ 项目是否已初始化（@config.tex 存在）
- ✅ 是否有 Word PDF 基准文件
- 🎯 基准来源检测（Word PDF / QuickLook / 未知）
- ✅ 编译状态
- ✅ PDF 分析结果状态
- 💾 导出 JSON 格式状态报告

**输出示例**:
```
============================================================
项目状态检查报告
============================================================
项目路径: /Volumes/2T01/Github/ChineseResearchLaTeX/projects/NSFC_Young
检查时间: 2026-01-05T23:47:45.810753

状态概览:
  ✅ 已初始化
  ✅ 有基准
  compilation_status: success
  ⚠️ 无分析

基准来源: word_pdf
基准质量: high

建议:
  1. 缺少 PDF 分析结果，建议执行: python scripts/analyze_pdf.py <baseline.pdf>
============================================================
```

**使用场景**:
- AI 执行优化前的必选步骤
- 快速了解项目当前状态
- 诊断常见问题（缺少基准、未编译等）

**状态输出**: JSON 文件保存到 `projects/{project}/artifacts/state_check.json`

---

### 1. analyze_pdf.py - PDF 样式分析工具

**功能**: 从 PDF（Word 导出的基准 PDF）中自动提取关键样式参数

**使用方法**:
```bash
# 安装依赖（首次使用）
pip install PyMuPDF

# 分析 Word PDF 基准
python3 scripts/analyze_pdf.py projects/NSFC_Young/template/word_baseline.pdf
```

**输出内容**:
- 📐 **页面布局**: 页面尺寸、边距（左/右/上/下，单位：cm）
- 🔤 **字体统计**: 字体名称、使用频率、字号列表、颜色（RGB）
- 📏 **行距分析**: 平均行距（pt）
- 💾 **详细分析结果**: 自动保存为 `*_analysis.json`

**使用场景**:
- Word 模板更新时，自动提取新的样式参数
- 对比不同年份模板的样式差异
- 验证 LaTeX 样式配置是否正确

**依赖**: `PyMuPDF` (fitz)

---

### 2. validate.sh / validate.bat - 自动化验证脚本（跨平台）

**功能**: 自动检查技能状态和项目配置

**使用方法**:
```bash
# macOS/Linux
cd skills/make_latex_model
./scripts/validate.sh --project NSFC_Young

# Windows
cd skills\make_latex_model
scripts\validate.bat --project NSFC_Young
```

**检查项**:
- ✅ 第一优先级: 基础编译检查 (项目目录、配置文件、编译状态、版本号一致性)
- ✅ 第二优先级: 样式参数一致性 (行距、颜色、边距、标题格式、**标题文字一致性**)
- ℹ️ 第三优先级: 视觉相似度 (需人工验证)
- ℹ️ 第四优先级: 像素对比 (需 Word 打印 PDF 基准)

**Python 版本**（推荐）:
```bash
python3 scripts/run_validators.py --project NSFC_Young
```

---

### 3. benchmark.sh / benchmark.bat - 性能基准测试（跨平台）

**功能**: 测量 LaTeX 编译性能

**使用方法**:
```bash
# macOS/Linux
cd skills/make_latex_model
./scripts/benchmark.sh NSFC_Young

# Windows
cd skills\make_latex_model
scripts\benchmark.bat NSFC_Young
```

**输出**:
- ⏱️ 平均编译时间（秒）
- 📄 PDF 文件大小（MB）
- 📊 JSON 格式性能报告

**输出示例**:
```json
{
  "test_info": {
    "test_time": "2026-01-05T13:14:12Z",
    "platform": "Darwin 25.2.0",
    "machine": "arm64"
  },
  "compilation": {
    "times": 3,
    "total_time_ms": 2372,
    "average_time_ms": 790,
    "average_time_sec": 0.79
  },
  "pdf": {
    "size_bytes": 1164515,
    "size_mb": 1.11
  }
}
```

---

### 4. extract_headings.py - 标题文字提取工具

**功能**: 从 Word 或 LaTeX 文件中提取标题文字结构

**使用方法**:
```bash
# 从 LaTeX 文件提取
python3 scripts/extract_headings.py latex --file projects/NSFC_Young/main.tex

# 从 Word 文档提取
python3 scripts/extract_headings.py word --file projects/NSFC_Young/template/2026年最新word模板-青年科学基金项目（C类）-正文.docx

# 输出为 JSON
python3 scripts/extract_headings.py latex --file main.tex --format json --output headings.json
```

**输出示例**:
```
# 标题文字提取结果
# 源文件: main.tex

section_1: （一）立项依据与研究内容
subsection_1_1: 1. 项目的立项依据
subsection_1_2: 2. 项目的研究内容、研究目标，以及拟解决的关键科学问题
...
```

---

### 5. compare_headings.py - 标题文字对比工具

**功能**: 对比“基准模板（推荐 PDF）”与 LaTeX 文件的标题文字差异（可选：加粗位置对齐）

**使用方法**:
```bash
# 推荐：用 PDF 作为唯一真相源（Single Source of Truth）
python3 scripts/compare_headings.py baseline.pdf main.tex

# 生成 HTML 可视化报告
python3 scripts/compare_headings.py baseline.pdf main.tex --report heading_report.html

# 生成 Markdown 报告
python3 scripts/compare_headings.py baseline.pdf main.tex --report heading_report.md

# 检查“加粗位置”是否一致（格式对比）
python3 scripts/compare_headings.py baseline.pdf main.tex --check-format --report heading_format_report.html

# 兼容旧流程（不推荐）：Word .docx
python3 scripts/compare_headings.py word.docx main.tex --report heading_report.html
```

**输出示例**:
```
============================================================
  标题文字对比报告
============================================================

总标题数: 14
✅ 完全匹配: 12
⚠️  有差异: 2
❌ 仅在一方: 0

# 完全匹配的标题
✅ section_1: （一）立项依据与研究内容
✅ subsection_1_1: 1. 项目的立项依据
...

# 有差异的标题
⚠️  subsection_1_3:
   Word:  3. 拟采取的研究方案及可行性分析
   LaTeX: 3. 拟采取的研究方案及可行性
```

**HTML 报告特性**:
- 🎨 美观的可视化界面
- 📊 统计卡片（匹配/差异/仅在一方）
- 🎯 颜色编码（绿色=匹配，黄色=差异，红色=仅在一方）
- 📱 响应式设计

---

## 工作流集成

### 标准优化流程

1. **修改样式配置**
   ```bash
   # 编辑 projects/NSFC_Young/extraTex/@config.tex
   vim projects/NSFC_Young/extraTex/@config.tex
   ```

2. **快速验证**
   ```bash
   cd skills/make_latex_model
   ./scripts/validate.sh
   ```

3. **性能测试**（可选）
   ```bash
   ./scripts/benchmark.sh
   ```

4. **人工验证**（如需）
   - 对比 Word PDF 和 LaTeX PDF
   - 检查视觉相似度
   - 验证像素对齐（如有 Word PDF 基准）

---

## 测试会话管理

### 创建新的测试会话

```bash
# 使用时间戳命名
TIMESTAMP=$(date +%Y%m%d%H%M)
mkdir -p skills/make_latex_model/tests/v${TIMESTAMP}/{scripts,output}

# 复制测试工具
cp skills/make_latex_model/scripts/*.sh skills/make_latex_model/tests/v${TIMESTAMP}/scripts/
```

### 测试会话结构

```
tests/v{TIMESTAMP}/
├── BUG_REPORT.md           # 问题报告
├── OPTIMIZATION_PLAN.md   # 优化计划
├── TEST_REPORT.md          # 测试报告
├── scripts/                # 测试工具
│   ├── validate.sh
│   └── benchmark.sh
└── output/                 # 测试输出
    └── benchmark_results.json
```

---

## 常见问题

### Q: 验证脚本提示"行距设置: 未找到 baselinestretch 定义"?

A: 这是正常的。当前项目使用 `\linespread` 而非 `\baselinestretch`,两者都是有效的行距设置方式。

### Q: 如何使用标题对比工具？

A: 首先安装依赖：
```bash
pip install python-docx
```

然后运行对比：
```bash
python3 scripts/compare_headings.py word.docx main.tex --report report.html
```

### Q: Word 文档是 .doc 格式，如何处理？

A: 使用 LibreOffice 转换为 .docx：
```bash
soffice --headless --convert-to docx template.doc
```

### Q: 性能测试中的编译时间波动很大?

A: 编译时间受系统负载影响。benchmark.sh 会运行 3 次取平均值,减少波动影响。

### Q: 如何在 Windows 上运行这些脚本?

A: 现在提供原生 .bat 脚本支持：
```bash
# Windows 命令行
scripts\validate.bat --project NSFC_Young
scripts\optimize.bat --project NSFC_Young
scripts\benchmark.bat NSFC_Young
```

也可以使用 Git Bash 运行 .sh 脚本。

---

## 新增工具（v2.1.0）

### 6. run_validators.py - 验证器运行器（Python 版本）

**功能**: 运行所有验证器插件并生成报告

**使用方法**:
```bash
python3 scripts/run_validators.py --project NSFC_Young
```

---

### 7. compare_pdf_pixels.py - PDF 像素对比工具

**功能**: 像素级 PDF 对比，支持整页对比与逐段对比

**使用方法**:
```bash
# 对比两个 PDF
python3 scripts/compare_pdf_pixels.py baseline.pdf output.pdf

# 推荐：逐段对比（更适配“空模板 vs 有正文”导致的整页噪声）
python3 scripts/compare_pdf_pixels.py baseline.pdf output.pdf --mode paragraph --features-out diff_features.json

# 生成 HTML 报告
python3 scripts/compare_pdf_pixels.py baseline.pdf output.pdf --report diff_report.html

# 生成差异热图
python3 scripts/compare_pdf_pixels.py baseline.pdf output.pdf --heatmap diff.png

# 保存结构化结果（供脚本解析）
python3 scripts/compare_pdf_pixels.py baseline.pdf output.pdf --json-out pixel_compare.json

# 保存差异特征（供 DiffAnalyzer/AIOptimizer 复用）
python3 scripts/compare_pdf_pixels.py baseline.pdf output.pdf --features-out diff_features.json
```

**依赖**: `PyMuPDF`, `Pillow`

---

### 8. sync_config.py - 样式配置双向同步工具

**功能**: 解析 LaTeX 配置并与 PDF 分析结果对比

**使用方法**:
```bash
# 对比配置
python3 scripts/sync_config.py @config.tex --analysis word_baseline_analysis.json

# 自动应用修改
python3 scripts/sync_config.py @config.tex --analysis word_baseline_analysis.json --apply

# 预览模式
python3 scripts/sync_config.py @config.tex --analysis word_baseline_analysis.json --dry-run
```

---

### 9. optimize.py / optimize.sh / optimize.bat - 一键式优化流程

**功能**: 自动化完整优化工作流（8 步）

**使用方法**:
```bash
# macOS/Linux
./scripts/optimize.sh --project NSFC_Young

# 交互模式
./scripts/optimize.sh --project NSFC_Young --interactive

# Windows
scripts\optimize.bat --project NSFC_Young
```

**8 步流程**:
1. 分析 Word PDF 基准
2. 提取标题文字
3. 对比样式参数
4. 生成修改建议
5. 应用修改（可选）
6. 编译 LaTeX 项目
7. 运行验证器
8. 生成优化报告

---

### 10. setup_wizard.py - 交互式配置向导

**功能**: 引导用户完成新项目配置

**使用方法**:
```bash
python3 scripts/setup_wizard.py

# 使用预设模板
python3 scripts/setup_wizard.py --template nsfc/young
```

**配置步骤**:
1. 项目信息（名称、描述）
2. 模板选择
3. 优化级别
4. Word 模板路径
5. 高级选项

---

### 11. scripts/core/font_detector.py - 字体路径自动检测

**功能**: 跨平台字体路径检测

**使用方法**:
```bash
# 显示系统信息
python3 -m scripts.core.font_detector --info

# 检测特定字体
python3 -m scripts.core.font_detector --font "KaiTi"

# 检测常见中文字体
python3 -m scripts.core.font_detector --chinese

# 检测常见英文字体
python3 -m scripts.core.font_detector --english
```

---

## 维护指南

### 更新验证脚本

当添加新的检查项时:
1. 编辑 `scripts/core/validators/` 中的验证器
2. 或编辑 `scripts/validate.sh`
3. 更新本文档的"检查项"列表

### 更新性能基准

当项目结构变化导致编译时间变化时:
1. 运行 `benchmark.sh` 获取新的基准数据
2. 更新 `config.yaml` 中的性能目标
3. 记录在 CHANGELOG 中

---

## 版本历史

- **v2.2.0** (2026-01-05): 架构澄清：AI 与硬编码协调改进
  - **新增 `check_state.py`**: 项目状态检查工具，AI 执行前的必选步骤
  - **更新 SKILL.md**: 新增「0.6) 执行模式说明」和「0.7) AI 决策点规范」章节

- **v2.1.0** (2026-01-05): 核心功能完善与工作流优化
  - **验证器插件系统**: CompilationValidator, StyleValidator, HeadingValidator, VisualValidator
  - **PDF 像素对比工具**: compare_pdf_pixels.py
  - **样式配置同步工具**: sync_config.py
  - **一键式优化流程**: optimize.py + optimize.sh + optimize.bat
  - **交互式配置向导**: setup_wizard.py
  - **Windows 兼容性**: validate.bat, benchmark.bat, optimize.bat
  - **字体路径自动检测**: scripts/core/font_detector.py

- v1.4.0 (2026-01-05): 新增标题文字工具
  - 新增 `extract_headings.py`：从 Word/LaTeX 提取标题文字
  - 新增 `compare_headings.py`：对比标题文字差异，生成 HTML 可视化报告
  - 更新 `validate.sh`：集成自动标题文字一致性检查
  - 更新工作流：支持标题对齐自动化

- v1.3.0 (2026-01-05): 初始版本
  - 集成到 make_latex_model 技能
  - 自动化验证脚本
  - 性能基准测试脚本
