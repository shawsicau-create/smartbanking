# Stata Skill for LobsterAI

全面的 Stata 编程参考技能，支持数据分析、计量经济学、因果推断、图形绘制等功能。

## 📦 安装方法

### 方法 1：直接复制
1. 将 `stata` 文件夹复制到 LobsterAI 技能目录：
   ```bash
   # macOS
   cp -r stata "~/Library/Application Support/LobsterAI/SKILLs/"
   
   # Windows
   xcopy /E /I stata "%APPDATA%\LobsterAI\SKILLs\stata"
   
   # Linux
   cp -r stata "~/.config/LobsterAI/SKILLs/"
   ```

### 方法 2：通过 LobsterAI 界面
1. 打开 LobsterAI 设置
2. 进入"Skills"选项卡
3. 点击"Install Skill"
4. 选择此文件夹或压缩包

## 🚀 功能特性

### 核心功能
- **数据操作** - 导入/导出、清洗、变量管理、字符串/日期处理
- **统计分析** - 描述统计、线性回归、面板数据、时间序列
- **因果推断** - DiD、RD、PSM、处理效应、样本选择
- **高级方法** - 生存分析、SEM、机器学习、空间计量
- **编程能力** - 宏、循环、Mata 矩阵编程
- **输出报告** - 回归表格导出、图形美化

### 支持的社区包 (20+)
- `reghdfe` - 高维固定效应
- `estout/esttab` - 发表级表格
- `did` - 现代双重差分
- `rdrobust` - 断点回归
- `psmatch2` - 倾向得分匹配
- `coefplot` - 系数图
- 等等...

### 🇨🇳 中文作图支持
技能会自动询问是否使用中文标签和标题，支持：
- 中文字体设置 (SimHei 等)
- 中文标题、坐标轴标签
- 中文图例

## 📁 目录结构

```
stata/
├── SKILL.md                      # 主技能文件 (必须)
├── README.md                     # 本文件
├── references/                   # 参考资料 (37 个文件)
│   ├── basics-getting-started.md
│   ├── data-management.md
│   ├── linear-regression.md
│   ├── panel-data.md
│   ├── difference-in-differences.md
│   └── ... (更多)
└── packages/                     # 社区包文档 (20 个文件)
    ├── reghdfe.md
    ├── estout.md
    ├── did.md
    └── ... (更多)
```

## 💡 使用示例

### 示例 1：基础回归分析
```
帮我用 Stata 分析 auto 数据集，运行价格对 mpg 和 weight 的回归
```

### 示例 2：绘制中文图表
```
用 auto 数据集画一个散点图，显示价格和油耗的关系，使用中文标签
```

### 示例 3：双重差分法
```
如何用 Stata 实现多期 DID？有异质性处理效应该怎么处理？
```

### 示例 4：导出回归表格
```
帮我用 estout 导出三个模型的回归结果到 Word 文件
```

## ⚠️ 常见问题

### 中文字体问题
如果中文显示为乱码，请确保系统已安装中文字体：
- **macOS**: 黑体 - Simplified (SimHei)
- **Windows**: 黑体 (SimHei)
- **Linux**: 安装 `fonts-wqy-zenhei` 或类似字体包

### Stata 路径问题
如果找不到 Stata，请检查：
- macOS: `/Applications/Stata/` 或 `/Applications/StataNow/`
- Windows: `C:\Program Files\Stata\`

### 社区包安装
安装社区包命令：
```stata
ssc install reghdfe, replace
ssc install estout, replace
ssc install did, replace
```

## 📝 版本信息

- **版本**: 1.0
- **最后更新**: 2026-03-22
- **兼容**: LobsterAI 1.0+
- **Stata 版本**: Stata 15+

##  致谢

本技能基于 LobsterAI Stata Skill 制作，包含全面的 Stata 参考文档和最佳实践。

## 📞 支持

如有问题，请查看：
- LobsterAI 文档：https://docs.openclaw.ai
- Stata 官方文档：https://www.stata.com/documentation/
