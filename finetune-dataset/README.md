# 智慧银行实验教程 - 课程微调数据集

## 数据集概述

基于《智慧银行实验教程——AI驱动的金融科技实践》课程讲义生成的领域微调数据集，适用于Qwen2.5-7B-Instruct的LoRA轻量微调。

## 数据集统计

| 文件 | 主题 | 样本数 | 来源章节 |
|------|------|--------|----------|
| ch01_fintech_basics.jsonl | 金融科技基础 | 70 | 第1章 绪论 |
| ch02_dev_environment.jsonl | 开发环境搭建 | 28 | 第2章 开发环境+实验讲义 |
| ch03_mcp_protocol.jsonl | MCP协议 | 25 | 第3章 MCP协议 |
| ch04_skill_system.jsonl | Skill体系 | 29 | 第4章 Skill体系 |
| ch05_econometrics.jsonl | 计量经济学 | 27 | 第6章 金融数据分析 |
| ch06_bmad_method.jsonl | BMAD方法论 | 21 | 第7章 BMAD+第8章综合项目 |
| **合计** | | **200** | 8个章节 |

## 数据格式

采用OpenAI/Qwen兼容的JSONL格式：

```jsonl
{"messages": [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}
```

## 训练配置（推荐）

参见 `system_prompt.json` 中的 training_config：

- 基座模型：Qwen2.5-7B-Instruct
- 微调方法：LoRA（rank=64, alpha=128）
- 学习率：2e-4
- 训练轮数：3 epochs
- 最大序列长度：2048
- 批次大小：4（梯度累积4步，等效batch=16）

## 使用方法

### 1. 合并数据集

已提供合并好的 `train_all.jsonl`（200条），也可自行重新生成：
```bash
cat ch*.jsonl > train_all.jsonl
```

**验证统计**：
- 总样本数：200条（system/user/assistant各200条）
- 总字符数：~600,000（估算~300,000 tokens）
- 最大单条token：~800（远低于max_seq_length=2048）
- JSON格式校验：0错误

### 2. 在PAI-DSW上微调

```python
# 使用LLaMA-Factory或ms-swift
llamafactory-cli train \
  --model_name_or_path Qwen/Qwen2.5-7B-Instruct \
  --dataset train_all.jsonl \
  --finetuning_type lora \
  --lora_rank 64 \
  --lora_alpha 128 \
  --learning_rate 2e-4 \
  --num_train_epochs 3 \
  --output_dir ./smartbank-lora
```

### 3. 部署到PAI-EAS

微调完成后，通过PAI-EAS部署为公网API端点，替代百炼或作为第四模型选项。

## 数据来源

- `智慧银行实验教程chapters/ch01.tex` ~ `ch13.tex`（8章LaTeX讲义）
- `实验讲义/本地大模型部署指南.md`
- `实验讲义/BMAD-CRM系统开发实验手册.md`

## 文件清单

| 文件 | 说明 |
|------|------|
| ch01_fintech_basics.jsonl | 金融科技基础（70条）|
| ch02_dev_environment.jsonl | 开发环境搭建（28条）|
| ch03_mcp_protocol.jsonl | MCP协议（25条）|
| ch04_skill_system.jsonl | Skill体系（29条）|
| ch05_econometrics.jsonl | 计量经济学（27条）|
| ch06_bmad_method.jsonl | BMAD方法论（21条）|
| train_all.jsonl | 合并训练集（200条）|
| system_prompt.json | 系统提示词与训练配置 |
| README.md | 本文件 |

## 数据集扩展记录

### 2026年7月15日扩展
- 目标：从30条扩展至200+条
- 方法：从讲义中提取更多Q&A对，覆盖金融科技基础、开发环境、MCP协议、Skill体系、计量经济学、BMAD方法论等主题
- 结果：200条有效样本

### 内容覆盖
- **ch01**：金融科技四阶段、AI在银行业应用、数字化转型、智能客服/风控/营销/运营/合规、LLM架构、Agent能力、MCP协议、Skill机制、BMAD方法论、AI素养、数字人民币、数据治理、DevOps等
- **ch02**：AI IDE对比、Python/Node.js/Git环境、CNB平台、提示工程、Jupyter Notebook、API、数据库、机器学习、云计算、Docker等
- **ch03**：MCP协议原理、配置、工具调用、安全机制等
- **ch04**：Skill开发、配置、生命周期管理、权限控制、A/B测试、多轮对话、国际化等
- **ch05**：面板数据、GARCH、Hausman检验、GMM、SARIMA、LSTM、DID、RDD、IV、SCM、单位根检验、协整检验、分位数回归、空间计量、门限回归、PSM-DID等
- **ch06**：金融数据类型、尖峰厚尾、ARCH效应、面板数据优势、固定/随机效应、Hausman检验、GMM动态面板、SARIMA/LSTM/Prophet预测、DID/RDD/IV/SCM因果推断、中介效应、异质性分析等

## 扩展建议

当前200条为完整的领域微调数据集，可进一步扩展：
1. 添加更多多轮对话样本
2. 添加金融计算题和代码生成样本
3. 添加实验步骤指导样本
4. 根据微调效果针对性补充薄弱主题
