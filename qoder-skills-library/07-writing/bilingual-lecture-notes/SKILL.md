---
name: bilingual-lecture-notes
description: '将中文学术LaTeX讲义（ctexart/ctexbook）转换为中英双语版本，同时对主要知识点进行面向本科基础水平的拓展。

  适用于任何学科的中文LaTeX讲义。处理内容包括：正文段落双语化、表格中英对照、TikZ图示双语标注、

  定理/tcolorbox环境双语化、封面双语化、知识点直觉解释拓展。

  触发场景：当用户要求对中文讲义进行双语化处理、为留学生准备中英文教材、

  或要求对LaTeX讲义添加英文翻译时使用。

  '
workflow_stage: writing
compatibility:
- claude-code
- cursor
- codex
author: Qoder Skills Library
version: 1.0.0
tags:
- bilingual
- lecture
- notes
---


# 中文学术讲义双语化处理流程

## 适用场景

- 中文 LaTeX 讲义需要同时服务中国学生和留学生
- 已有纯中文 `.tex` 讲义，需添加标准学术英文对照
- 需要在双语化的同时对关键知识点进行本科基础水平的拓展解释

## 前置条件

- 源文件为 `.tex` 格式，使用 `ctexart` 或 `ctexbook` 文档类
- 编译器为 `xelatex`
- **操作前必须备份原始文件**



## 处理规则（7条核心规则）

### R1 段落双语格式

每段中文正文后紧跟学术英文翻译。格式：

```latex
中文段落内容……

\medskip
\textit{English translation of the paragraph...}
```

- 公式保留数学符号，不翻译，不重复
- 英文段落使用 `\textit{}` 斜体，与中文正文视觉区分
- 段间用 `\medskip` 分隔

### R2 表格中英对照

表格内所有中文文字后加英文括注：

```latex
\textbf{机制 (Mechanism)} & \textbf{原理 (Principle)} \\
共保率 (Coinsurance) & 投保人自担部分损失 (Insured bears partial loss) \\
```

表格标题（`\caption`）同样双语：

```latex
\caption{道德风险控制机制 / Moral Hazard Control Mechanisms}
```

### R3 TikZ 图示双语标注

所有 TikZ 节点文字改为中英双行：

```latex
\node[box] (ins) {保险业\\Insurance Industry};
\node[box] (farmer) {农户\\Farmer};
```

图注（`\caption`）双语：

```latex
\caption{模型架构图 (Model Architecture)}
```

坐标轴标签双语：

```latex
\draw[->] (0,0) -- (10,0) node[right] {年份 Year};
```

### R4 环境标题双语

**定理类环境**（`\newtheorem`）：

```latex
\newtheorem{definition}{定义 Definition}[section]
\newtheorem{theorem}{定理 Theorem}[section]
\newtheorem{proposition}{命题 Proposition}[section]
\newtheorem{example}{案例 Case Study}[section]
\newtheorem{remark}{注记 Remark}[section]
```

定理环境的可选参数名也双语化：

```latex
\begin{definition}[风险态度分类 / Classification of Risk Attitudes]
```

**tcolorbox 环境**默认标题双语：

```latex
\newtcolorbox{keypoint}[1][]{
  ..., title={核心要点 Key Points}, #1
}
```

带 `title=` 覆盖的也需双语：

```latex
\begin{modelbox}[title={最优保险覆盖率 Optimal Insurance Coverage}]
```

### R5 封面页双语

封面需包含：中文大标题 → 英文大标题 → 中文学期信息 → 英文学期信息 → 双语受众说明 → 双语日期。

必须包含一行说明：

```latex
{\normalsize 本讲义采用中英双语编写，适用于中国学生与国际学生\par}
{\normalsize This lecture note is prepared bilingually for both domestic and international students.\par}
```

### R6 章节标题双语

`\section`、`\subsection`、`\subsubsection`、`\paragraph` 标题后加英文括注：

```latex
\section{保险经济学基础理论 (Foundations of Insurance Economics)}
\subsection{保险需求理论 (Insurance Demand Theory)}
\paragraph{期望效用理论与风险厌恶 (Expected Utility Theory and Risk Aversion)}
```

### R7 知识点拓展

对**主要知识点和关键知识点**，以"本科简单学过该领域基础"的水平进行拓展。拓展方式：

1. **直觉解释**：用 `\noindent\textbf{直觉解释 / Intuitive Explanation:}` 标题引入，给出非数学的直觉阐述
2. **数字案例**：用简单数字帮助理解（如"假设你面临1%概率损失10万元"）
3. **与本科知识的衔接**：说明该知识点与本科已学内容（如保险原理基础概念）的关系和拓展之处
4. 拓展内容同样遵循 R1 的中英双语格式

判断标准：如果一个概念对于只上过本科入门课的学生可能感到陌生或抽象，就需要拓展。

---

## 执行流程

### Step 1: 备份

```
cp 原始文件.tex 工作目录/原始文件_backup.tex
```

### Step 2: 分析讲义结构

阅读整份 `.tex` 文件，识别：

- 所有 `\newtheorem` 定义 → 按 R4 双语化
- 所有 `\newtcolorbox` 定义 → 按 R4 双语化
- 封面页 (`titlepage`) → 按 R5 双语化
- 所有 `\section`/`\subsection`/`\subsubsection`/`\paragraph` → 按 R6 双语化
- 所有表格 (`tabular`/`tabularx`) → 按 R2 双语化
- 所有 TikZ 图 → 按 R3 双语化
- 所有正文段落 → 按 R1 双语化
- 需要拓展的关键知识点 → 按 R7 添加直觉解释

### Step 3: 全文改写

**重要：由于改动覆盖面极大（几乎每一段都需要处理），应一次性写出完整的新文件，而非逐段 Edit。**

对于多份讲义，使用 Task 工具启动子代理并行处理，每个子代理处理一份 `.tex` 文件。

子代理 prompt 应包含：
1. 完整的 7 条规则（R1-R7）摘要
2. 目标文件路径
3. "读取文件 → 写出完整修改版"的明确指令
4. 具体需要拓展的知识点列表（由主代理根据讲义内容预先分析给出）

### Step 4: 编译验证

```bash
xelatex -interaction=nonstopmode 文件.tex   # 第一遍
xelatex -interaction=nonstopmode 文件.tex   # 第二遍（修正交叉引用）
```

检查编译输出：
- `Output written on ... .pdf (N pages)` → 成功
- 仅有 Warning（如 `headheight too small`、`Overfull \hbox`）→ 可接受
- 有 Error → 需修复

### Step 5: 交付

将修改后的 `.tex` 源文件和编译生成的 `.pdf` 一并交付。

---

## 不应修改的内容

- 数学公式内容（仅保持原样）
- LaTeX 宏包引用（除非需要添加新宏包支持双语功能）
- 文档整体结构和章节编号逻辑
- 代码块（`lstlisting` 等）内容
- 参考文献条目（保持原始语言）

## 英文翻译质量要求

- 使用标准学术英文（非口语化）
- 专业术语使用该学科通用的英文表达
- 保持与中文段落严格的语义对应
- 人名、机构名保持原文（如不翻译"中国人保"为英文缩写，而是保留或用通用英文名）

## 典型处理规模参考

| 原始文件 | 处理后 | PDF页数 |
|---------|--------|---------|
| ~550行 | ~900行 | ~27页 |
| ~980行 | ~1400行 | ~41页 |

文件行数通常增加 50%--80%。
