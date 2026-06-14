# CI/CD 配置说明

本项目使用 GitHub Actions 实现自动化构建和发布。

## 工作流程

### 1. 自动构建

当代码推送到 `main` 或 `master` 分支时，系统会自动：

1. 检出代码
2. 安装 LaTeX 环境
3. 编译 PDF 文件
4. 上传构建产物

### 2. 发布流程

当推送标签时，系统会自动：

1. 编译 PDF 文件
2. 创建 GitHub Release
3. 上传 PDF 附件

## 配置文件

### `.github/workflows/build-pdf.yml`

主要工作流配置文件，定义了：

- 触发条件（push、PR、手动触发）
- 构建环境（Ubuntu、LaTeX）
- 编译步骤（xelatex、biber）
- 发布配置（GitHub Release）

### `Makefile`

本地构建工具，提供：

- `make pdf` - 编译PDF
- `make clean` - 清理文件
- `make check` - 语法检查
- `make view` - 编译并查看

### `test-cicd.sh`

CI/CD 测试脚本，用于：

- 验证本地环境
- 测试构建流程
- 检查生成文件

## 使用指南

### 本地开发

```bash
# 编译PDF
make pdf

# 清理文件
make clean

# 检查语法
make check
```

### 提交代码

```bash
# 添加更改
git add .

# 提交更改
git commit -m "feat: 添加新功能"

# 推送到远程
git push origin main
```

### 创建发布版本

```bash
# 更新版本号
# 提交更改
git commit -m "release: v5.1"

# 创建标签
git tag v5.1

# 推送标签
git push origin v5.1
```

## 故障排除

### 构建失败

1. 检查 LaTeX 语法错误
2. 查看 GitHub Actions 日志
3. 本地运行 `make check` 测试

### PDF 生成问题

1. 确保安装了必要的宏包
2. 检查字体配置
3. 验证参考文献格式

### 环境问题

1. 确保安装了 TeX Live
2. 检查 PATH 环境变量
3. 验证 xelatex 和 biber 命令

## 最佳实践

1. **频繁提交**：小步提交，便于问题定位
2. **语义化版本**：使用语义化版本号
3. **测试先行**：本地测试后再推送
4. **文档更新**：修改内容时同步更新文档
5. **代码审查**：使用 Pull Request 进行代码审查

## 相关链接

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [LaTeX 编译指南](https://www.latex-project.org/help/documentation/)
- [Makefile 教程](https://www.gnu.org/software/make/manual/make.html)
