# CNB CI/CD 配置指南

本项目使用腾讯云CNB平台的CI/CD系统实现自动化构建。

## 配置文件

### `.cnb.yml`

CNB CI/CD 配置文件，定义了：

- 构建阶段（build stage）
- 触发条件（rules）
- 构建脚本（script）
- 产物保存（artifacts）

## 配置说明

### 构建阶段

```yaml
stages:
  - name: build
    image: texlive/texlive:latest
    script:
      - apt-get update && apt-get install -y texlive-lang-chinese texlive-fonts-recommended texlive-fonts-extra texlive-latex-extra texlive-bibtex-extra biber
      - cd 智慧银行实验教程chapters
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
      - biber "智慧银行实验教程"
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
    artifacts:
      paths:
        - 智慧银行实验教程chapters/智慧银行实验教程.pdf
      expire_in: 7 days
```

### 触发条件

```yaml
rules:
  - if: $CI_COMMIT_BRANCH == "main"
    when: always
  - if: $CI_COMMIT_BRANCH == "master"
    when: always
  - if: $CI_PIPELINE_SOURCE == "web"
    when: always
```

- **main/master分支**：每次推送自动触发
- **手动触发**：通过CNB Web界面手动触发

## 使用方法

### 1. 提交代码

```bash
# 添加更改
git add .

# 提交更改
git commit -m "feat: 添加新功能"

# 推送到远程
git push origin main
```

### 2. 查看构建状态

1. 登录 [CNB控制台](https://cnb.cool)
2. 进入项目仓库
3. 查看"CI/CD"或"Pipelines"页面
4. 查看构建日志和状态

### 3. 下载构建产物

构建成功后，在CI/CD页面可以下载：
- `智慧银行实验教程.pdf` - 编译后的PDF文件

### 4. 手动触发构建

在CNB Web界面：
1. 进入项目仓库
2. 点击"CI/CD"或"Pipelines"
3. 选择"Run Pipeline"或"手动触发"
4. 选择分支和配置

## 配置优化

### 使用缓存加速构建

```yaml
stages:
  - name: build
    image: texlive/texlive:latest
    cache:
      key: texlive-cache
      paths:
        - /usr/local/texlive
    script:
      - cd 智慧银行实验教程chapters
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
      - biber "智慧银行实验教程"
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
```

### 多阶段构建

```yaml
stages:
  - name: check
    image: texlive/texlive:latest
    script:
      - cd 智慧银行实验教程chapters
      - xelatex -interaction=nonstopmode -no-pdf "智慧银行实验教程.tex"
    rules:
      - if: $CI_PIPELINE_SOURCE == "merge_request_event"

  - name: build
    image: texlive/texlive:latest
    script:
      - cd 智慧银行实验教程chapters
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
      - biber "智慧银行实验教程"
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
      - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
    artifacts:
      paths:
        - 智慧银行实验教程chapters/智慧银行实验教程.pdf
    rules:
      - if: $CI_COMMIT_BRANCH == "main"
```

## 故障排除

### 构建失败

1. **检查LaTeX语法**：本地运行 `make check`
2. **查看构建日志**：在CNB控制台查看详细错误信息
3. **检查依赖**：确保所有LaTeX宏包都已安装

### 常见问题

#### 1. 中文字体问题

```yaml
script:
  - apt-get install -y fonts-noto-cjk
```

#### 2. 参考文献问题

```yaml
script:
  - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
  - biber "智慧银行实验教程"
  - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
  - xelatex -interaction=nonstopmode "智慧银行实验教程.tex"
```

#### 3. 内存不足

```yaml
script:
  - xelatex -interaction=nonstopmode -extra-mem-top=5000000 "智慧银行实验教程.tex"
```

## 与GitHub Actions对比

| 特性 | CNB CI/CD | GitHub Actions |
|------|-----------|----------------|
| 配置文件 | `.cnb.yml` | `.github/workflows/*.yml` |
| 触发条件 | 分支推送、手动 | 分支推送、PR、手动 |
| 构建环境 | Docker镜像 | Ubuntu/Windows/macOS |
| 产物保存 | CNB存储 | GitHub Artifacts |
| 集成平台 | 腾讯云CNB | GitHub |

## 最佳实践

1. **频繁提交**：小步提交，便于问题定位
2. **本地测试**：先本地测试再推送
3. **查看日志**：构建失败时及时查看日志
4. **使用缓存**：缓存TeX Live加速构建
5. **分支策略**：使用分支进行功能开发

## 相关链接

- [CNB文档](https://cnb.cool/docs)
- [LaTeX编译指南](https://www.latex-project.org/help/documentation/)
- [TeX Live镜像](https://hub.docker.com/r/texlive/texlive)
