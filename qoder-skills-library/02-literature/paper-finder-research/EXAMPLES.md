# 使用示例

本文件提供了 PaperFinder 文献综述助手技能的详细使用示例。

## 示例 1：机器学习基础研究

### 场景
您正在开始一个关于 Transformer 架构的研究项目，需要全面了解该领域的发展历程和最新进展。

### 调用方式
```
使用 paper-finder-research 技能：
- 研究主题: "Transformer architecture evolution in deep learning"
- 最大论文数: 30
- 年份范围: "2017-2024"
- 下载重要文献: true
```

### 预期输出
```
literature-review/
├── review-transformer-architecture-2024-02-03.md
├── bibliography-transformer-architecture-2024-02-03.bib
└── paper-list-transformer-architecture-2024-02-03.json

papers/
├── Vaswani_2017_attention-is-all-you-need.pdf
├── Devlin_2019_bert.pdf
├── Brown_2020_gpt3.pdf
├── Dosovitskiy_2021_vision-transformer.pdf
└── ...（共 15-20 篇重要文献）
```

### 综述报告示例内容
```markdown
# 文献综述报告：Transformer Architecture Evolution

## 1. 研究背景与概述
Transformer 架构自 2017 年由 Vaswani 等人提出以来，已成为自然语言处理和
计算机视觉领域的主导架构...

## 2. 核心文献分析

### 2.1 基础理论与方法
- **Attention Is All You Need** (Vaswani et al., 2017)
  原始 Transformer 架构，引入自注意力机制...

### 2.2 最新研究进展
- **LLaMA** (Touvron et al., 2023)
  开源大语言模型的重要里程碑...
```

---

## 示例 2：特定应用领域调研

### 场景
您需要为论文撰写关于医疗影像分析中深度学习应用的文献综述章节。

### 调用方式
```
使用 paper-finder-research 技能：
- 研究主题: "Deep learning for medical image segmentation"
- 最大论文数: 25
- 年份范围: "2019-2024"
- 下载重要文献: true
- 输出格式: "markdown"
```

### 输出结构
```
literature-review/
└── review-medical-image-segmentation-2024-02-03.md
    包含：
    - 深度学习在医疗影像中的应用概述
    - 主流分割方法对比（U-Net, SegNet, DeepLab等）
    - 不同疾病类型的应用案例
    - 数据集和评估指标总结
    - 临床应用挑战与未来方向
```

---

## 示例 3：快速技术调研

### 场景
快速了解某个新兴技术的最新进展，用于项目提案或技术选型。

### 调用方式
```
使用 paper-finder-research 技能：
- 研究主题: "Retrieval-Augmented Generation (RAG) systems"
- 最大论文数: 15
- 年份范围: "2023-2024"
- 下载重要文献: true
```

### 输出特点
- 聚焦最新研究（2023-2024）
- 快速生成概览（15篇精选文献）
- 重点关注实际应用和系统设计
- 提供技术对比和选型建议

---

## 示例 4：跨学科研究综述

### 场景
您正在进行跨学科研究，需要整合多个领域的文献。

### 调用方式（分步执行）

#### 步骤 1：第一个子领域
```
使用 paper-finder-research 技能：
- 研究主题: "Reinforcement learning for robotics control"
- 最大论文数: 20
- 年份范围: "2020-2024"
```

#### 步骤 2：第二个子领域
```
使用 paper-finder-research 技能：
- 研究主题: "Computer vision for robot perception"
- 最大论文数: 20
- 年份范围: "2020-2024"
```

#### 步骤 3：交叉整合
手动整合两个综述，识别交叉引用和共同主题

---

## 示例 5：论文写作辅助

### 场景
为即将投稿的论文补充和更新参考文献，确保引用最新相关工作。

### 调用方式
```
使用 paper-finder-research 技能：
- 研究主题: "Multi-task learning with meta-learning"
- 最大论文数: 30
- 年份范围: "2022-2024"
- 下载重要文献: false  # 只需要引用信息
- 输出格式: "json"
```

### 使用建议
1. 导出 BibTeX 文件到论文项目
2. 使用 JSON 输出快速浏览论文元数据
3. 识别需要在论文中引用的关键工作
4. 补充遗漏的重要文献

---

## 示例 6：教学与课程准备

### 场景
准备研究生课程的阅读材料清单。

### 调用方式
```
使用 paper-finder-research 技能：
- 研究主题: "Introduction to neural architecture search"
- 最大论文数: 20
- 年份范围: "2018-2024"
- 下载重要文献: true
```

### 教学用途
- 生成的综述作为课程导论材料
- 按难度和重要性排序的必读论文清单
- 下载的 PDF 作为课程资料分享（需注意版权）
- BibTeX 文件用于学生参考文献管理

---

## 高级使用技巧

### 技巧 1：渐进式调研
```
# 第一轮：获取广泛概览
研究主题: "Neural networks"
最大论文数: 50
年份范围: "2015-2024"

# 第二轮：深入特定方向
研究主题: "Convolutional neural networks for image classification"
最大论文数: 30
年份范围: "2018-2024"

# 第三轮：聚焦最新进展
研究主题: "Vision Transformers vs CNNs"
最大论文数: 15
年份范围: "2022-2024"
```

### 技巧 2：对比研究
```
# 分别调研两种方法
主题 A: "Supervised learning approaches"
主题 B: "Self-supervised learning approaches"

# 然后手动对比分析
```

### 技巧 3：时间序列分析
```
# 按时间段分别调研
2015-2017: "Early deep learning methods"
2018-2020: "Deep learning maturation"
2021-2024: "Recent advances and trends"
```

---

## 输出文件使用指南

### 综述报告 (.md)
- 直接用于论文撰写的 Related Work 章节
- 作为项目提案的技术背景
- 团队内部知识分享文档

### BibTeX 文件 (.bib)
- 导入到 LaTeX 论文项目
- 使用 Zotero/Mendeley 等工具管理
- 作为引用数据库的一部分

### JSON 文件 (.json)
- 用于数据分析和可视化
- 集成到文献管理系统
- 作为结构化数据存储

### PDF 文件
- 详细阅读和笔记
- 团队内部分享（注意版权）
- 离线参考和学习

---

## 常见问题

### Q: 如何处理非英文文献？
A: 当前主要支持英文文献。如需其他语言，可以在研究主题中用对应语言描述。

### Q: 能否搜索特定作者的论文？
A: 可以在研究主题中包含作者名，如 "Geoffrey Hinton deep learning"

### Q: 如何获取付费论文的 PDF？
A: 技能只能下载开放获取论文。付费论文请通过机构订阅、Sci-Hub 或联系作者获取。

### Q: 综述质量如何保证？
A: 技能会评估引用数、期刊质量等指标，但建议人工审核和补充。

### Q: 可以定制输出格式吗？
A: 当前支持 markdown 和 json。如需其他格式，可以后处理转换。

---

## 最佳实践建议

1. **明确研究范围**: 提供具体的研究主题，避免过于宽泛
2. **合理设置论文数量**: 20-30 篇适合深入综述，10-15 篇适合快速调研
3. **选择合适的年份范围**: 基础研究可以更宽，追踪热点可以聚焦近期
4. **人工审核补充**: 技能输出是起点，需要人工判断和补充
5. **版权意识**: 遵守学术规范和版权法律
6. **定期更新**: 活跃领域建议每季度更新一次综述

---

**祝您研究顺利！如有任何问题，欢迎反馈改进建议。**