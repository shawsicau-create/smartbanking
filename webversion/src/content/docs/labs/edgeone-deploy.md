---
title: 'CNB流水线自动部署到EdgeOne Pages'
description: '使用 CNB 云原生构建流水线，实现代码推送后自动部署静态网站到 EdgeOne Pages'
---

**实验步骤：CNB 云原生构建 + EdgeOne Pages 自动部署**

本实验指导学生配置 CNB（Cloud Native Build）流水线，实现"代码推送即部署"的持续集成/持续部署（CI/CD）工作流，将课程网站自动发布到 EdgeOne Pages。

## 第一部分：理解 CI/CD 与云原生构建

### 一、什么是 CI/CD

CI/CD（持续集成/持续部署）是现代软件开发的核心实践：

| 概念 | 含义 | 本项目中的体现 |
|------|------|--------------|
| CI（持续集成） | 代码变更后自动构建和测试 | CNB 推送后自动安装依赖、构建网站 |
| CD（持续部署） | 构建通过后自动发布到生产环境 | 构建完成后自动部署到 EdgeOne Pages |

传统方式：手动在本地构建 → 手动上传文件到服务器 → 手动配置域名

CI/CD 方式：`git push` → 云端自动构建 → 自动部署 → 网站更新（全程无需人工干预）

### 二、本项目的部署架构

```
你的电脑                    CNB 云端                      EdgeOne Pages CDN
┌──────────┐   git push   ┌──────────────┐  部署产物   ┌──────────────┐
│ 修改代码  │ ──────────→ │ 1. 拉取代码   │ ────────→ │ 全球边缘节点  │
│ git commit│             │ 2. 安装依赖   │            │ 用户访问网站  │
│ git push  │             │ 3. 构建网站   │            └──────────────┘
└──────────┘             │ 4. 部署 EdgeOne│
                         └──────────────┘
```

核心组件：

| 组件 | 作用 | 本项目配置 |
|------|------|----------|
| CNB（cnb.cool） | 代码托管 + 云原生构建流水线 | 仓库 xiaosicau/smartbanking |
| EdgeOne Pages | 腾讯云全球 CDN 静态网站托管 | smartbanking 项目 |
| Astro + Starlight | 静态网站生成框架 | webversion/ 目录 |
| .cnb.yml | 流水线配置文件 | 仓库根目录 |

:::tip[为什么选择 EdgeOne Pages？]
EdgeOne Pages 是腾讯云提供的全球 CDN 静态网站托管服务，具有以下优势：
- **国内访问速度快**：EdgeOne 在中国大陆有大量边缘节点，相比海外 CDN 延迟更低
- **免费额度充足**：适合教学项目和个人项目
- **与 CNB 无缝集成**：同属腾讯云生态，CI/CD 流水线配置简单
- **支持 CLI 部署**：可通过 `edgeone pages deploy` 命令行工具一键部署
:::

## 第二部分：配置流水线（.cnb.yml）

### 一、认识 .cnb.yml

CNB 的流水线配置遵循"配置即代码"原则——在仓库根目录放置一个 `.cnb.yml` 文件，CNB 平台会根据该文件自动执行构建任务。

本项目中 `.cnb.yml` 的完整内容：

```yaml
main:                              # 目标分支：main
  push:                            # 触发事件：代码推送到 main 分支时
    - name: deploy-webversion-to-edgeone
      docker:
        image: node:22             # 使用 Node.js 22 Docker 镜像
      imports:
        # 从密钥仓库导入 EdgeOne Pages API Token（敏感信息不存放在代码中）
        - https://cnb.cool/xiaosicau/secrets/-/blob/main/edgeone.yml
      stages:
        - name: 安装 pnpm
          script: corepack enable && corepack prepare pnpm@latest --activate
        - name: 安装依赖
          script: cd webversion && pnpm install
        - name: 构建网站
          script: cd webversion && pnpm build
        - name: 部署到 EdgeOne Pages
          script: |
            cd webversion
            npx edgeone pages deploy ./dist -n smartbanking -t $EDGEONE_PAGES_API_TOKEN
```

### 二、逐行解读流水线配置

**(1) 触发条件**

```yaml
main:
  push:
```

含义：当 `main` 分支收到 `push` 事件（即有人执行 `git push` 到 main 分支）时，自动触发构建。

**(2) 执行环境**

```yaml
docker:
  image: node:22
```

含义：使用 Node.js 22 的 Docker 容器作为构建环境。Docker 保证了环境一致性——无论谁推送代码，构建环境都是相同的。

**(3) 密钥导入**

```yaml
imports:
  - https://cnb.cool/xiaosicau/secrets/-/blob/main/edgeone.yml
```

含义：从 CNB 的密钥仓库中导入敏感信息（EdgeOne Pages API Token）。密钥仓库是一种特殊类型的仓库，专门存放密码、API Key 等敏感数据，禁止 Git Clone 到本地，只能通过流水线引用。

:::caution[安全要点]
Token 等敏感信息**绝不能**写入代码文件，必须使用密钥仓库管理。
:::

**(4) 构建步骤**

流水线包含 4 个顺序执行的 stages（阶段）：

| 阶段 | 命令 | 作用 |
|------|------|------|
| 安装 pnpm | `corepack enable && corepack prepare pnpm@latest` | 激活 Node.js 内置的包管理器 |
| 安装依赖 | `pnpm install` | 下载 357 个 npm 包 |
| 构建网站 | `pnpm build` | Astro 编译 Markdown → HTML |
| 部署 EdgeOne Pages | `edgeone pages deploy ./dist -n ... -t ...` | 上传到 EdgeOne CDN |

### 三、EdgeOne CLI 部署命令详解

```bash
npx edgeone pages deploy ./dist -n smartbanking -t $EDGEONE_PAGES_API_TOKEN
```

| 参数 | 含义 |
|------|------|
| `./dist` | Astro 构建产物目录 |
| `-n smartbanking` | EdgeOne Pages 项目名称 |
| `-t $EDGEONE_PAGES_API_TOKEN` | API Token（从密钥仓库导入） |

:::note[edgeone CLI vs edgeone-makers-mcp]
EdgeOne 提供两种部署方式：
1. **CLI 方式**（`npx edgeone pages deploy`）：适合 CI/CD 流水线，支持部署整个目录
2. **MCP 方式**（`deploy-html` 工具）：适合 AI IDE 中快速部署单个 HTML 页面
本项目在流水线中使用 CLI 方式，因为它能部署完整的 Astro 多页面站点。
:::

### 四、pnpm v10+ 构建脚本配置

项目依赖的 esbuild 和 sharp 需要在安装时执行构建脚本（编译原生模块）。pnpm v10+ 默认禁止所有构建脚本，需要在 `pnpm-workspace.yaml` 中显式允许：

```yaml
# webversion/pnpm-workspace.yaml
allowBuilds:
  esbuild: true
  sharp: true
```

如果缺少此配置，`pnpm install` 会报错：

```
[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild@0.27.7, sharp@0.34.5
Run "pnpm approve-builds" to pick which dependencies should be allowed to run scripts.
```

## 第三部分：设置密钥仓库

### 一、创建 EdgeOne Pages 项目和 API Token

**步骤一：创建 EdgeOne Pages 项目**

1. 访问 [EdgeOne Pages 控制台](https://console.cloud.tencent.com/edgeone/pages)
2. 点击「创建项目」，选择「直接上传」类型
3. 上传任意一个文件（如空的 index.html），系统会自动部署
4. 记住项目名称（如 `smartbanking`）

**步骤二：创建 API Token**

1. 访问 [EdgeOne API Token 页面](https://pages.edgeone.ai/document/api-token)
2. 点击「Create Token」
3. 填写信息：

| 字段 | 填写内容 |
|------|---------|
| Name | cnb-deploy |
| Scope | 选择你的项目 |
| Expiration | 按需设置 |

4. 点击「Create」，**立即复制**生成的 Token

:::caution
Token 仅显示一次，请妥善保存。
:::

### 二、创建 CNB 密钥仓库

1. 打开 <https://cnb.cool> → 点击左上角「+」→「创建仓库」
2. 配置信息：

| 字段 | 填写内容 |
|------|---------|
| 仓库类型 | **密钥仓库**（必须选这个） |
| 归属 | 你的组织（如 xiaosicau） |
| 名称 | secrets |
| 公开性 | 私有 |

3. 点击「创建」

### 三、添加 EdgeOne Token 到密钥仓库

1. 进入密钥仓库页面，点击「在线编辑」
2. 新建文件 `edgeone.yml`，内容为：

```yaml
EDGEONE_PAGES_API_TOKEN: "粘贴你的EdgeOne Pages API Token"
```

3. 点击「提交」保存

:::note[密钥仓库的安全特性]
- 禁止 Git Clone 到本地（防止敏感数据泄露）
- 禁止本地推送更改（所有修改必须通过 Web 界面）
- 所有页面自动添加用户水印（防止截图泄露）
- 完整的审计日志（谁在什么时候访问了什么密钥）
:::

## 第四部分：触发部署与验证

### 一、首次触发部署

密钥仓库配置完成后，推送任意提交即可触发构建：

```bash
# 如果没有新的代码变更，可以创建一个空提交：
git commit --allow-empty -m "trigger: 首次触发CNB自动部署到EdgeOne"
git push origin main
```

### 二、查看构建状态

**方式 A：命令行查看**

```bash
cnb build get-build-logs --repo 你的用户名/smartbanking --page-size 3
```

**方式 B：网页查看**

打开 `https://cnb.cool/你的用户名/smartbanking/-/build`，可以看到所有构建记录和详细日志。

### 三、构建状态说明

| 状态 | 含义 | 后续操作 |
|------|------|---------|
| pending | 构建排队中或正在执行 | 等待完成 |
| success | 构建和部署均成功 | 打开网站验证 |
| error | 某一步骤执行失败 | 查看日志排查原因 |
| cancel | 构建被手动取消 | 重新推送触发 |

### 四、验证部署结果

构建成功后（通常 1-2 分钟），打开网站确认更新：

- 访问 EdgeOne Pages 控制台中显示的域名（形如 `smartbanking-xxx.edgeone.app`）
- 确认页面显示最新内容

## 第五部分：常见构建问题排查

| 错误信息 | 原因 | 解决方法 |
|---------|------|---------|
| ERR_PNPM_IGNORED_BUILDS | pnpm v10+ 禁止构建脚本 | 在 `pnpm-workspace.yaml` 添加 `allowBuilds` |
| imports 失败 | 密钥仓库路径错误或权限不足 | 检查 `.cnb.yml` 中 imports URL 是否正确 |
| Token 无效 / Authentication error | EdgeOne API Token 过期或错误 | 重新创建 Token，更新密钥仓库 |
| Build failed (astro build 报错) | Markdown 语法错误或依赖缺失 | 先在本地 `pnpm build` 验证通过再推送 |
| Deploy timeout | EdgeOne 服务异常或网络超时 | 等待几分钟后重新推送触发 |
| node_modules 相关错误 | 依赖版本冲突 | 删除 `pnpm-lock.yaml` 后重新 `pnpm install` |
| Project not found | EdgeOne Pages 项目不存在 | 先在控制台创建「直接上传」类型项目 |

## 第六部分：进阶——理解完整工作流

### 一、日常更新流程

当你需要更新网站内容时，只需要：

1. 修改 Markdown 文件（如 `webversion/src/content/docs/ch06.md`）
2. `git add` → `git commit` → `git push`
3. CNB 自动构建 → 自动部署 → 网站更新

全程无需手动登录服务器或上传文件。

### 二、本地预览 vs 线上部署

| 场景 | 命令 | 访问地址 |
|------|------|---------|
| 本地预览 | `cd webversion && pnpm dev` | http://localhost:4321 |
| 手动部署 | `cd webversion && npx edgeone pages deploy ./dist -n smartbanking` | smartbanking-xxx.edgeone.app |
| 自动部署 | `git push origin main` | 同上（CNB 流水线自动执行） |

:::tip[建议]
推送前先用 `pnpm dev` 在本地预览确认效果，避免推送后发现问题。
:::

### 三、多人协作场景

当多名同学同时修改仓库时：

1. 每次推送都会触发一次独立构建
2. 构建按推送顺序执行，不会并行
3. 最新一次成功构建的版本即为线上版本
4. 可通过 CNB 网页查看每次构建对应的提交者和变更内容

## 验收清单

完成以下全部检查项，截图保存作为实验报告交付物：

- [ ] 理解 CI/CD 的基本概念（能用自己的话解释）
- [ ] 能说出 `.cnb.yml` 中每个 stage 的作用
- [ ] 理解密钥仓库的安全特性（为什么不能把 Token 写在代码里）
- [ ] 在 CNB 网页上能看到构建记录（status: success）
- [ ] 构建日志中显示 4 个 stage 全部通过
- [ ] 打开 EdgeOne Pages 网站确认内容与最新代码一致
- [ ] 能说出 `pnpm-workspace.yaml` 中 `allowBuilds` 的作用
