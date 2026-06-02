# CNB 项目同步教程

本教程演示如何将本地项目同步到 CNB（CodeNotebook）代码托管平台。

---

## 前置条件

1. 已安装 Git
2. 已安装 Node.js（建议 LTS 版本）
3. 已安装 CNB CLI 工具和 Skills 工具
4. 拥有 CNB 账号和访问令牌
这个是老师的token ，你需要用微信登陆生成自己的token 
 # CNB Access Token (Not synced)
# Token Name: trae 2
# Git Username: cnb
# Token: chjklefx37Pgr16c1LVoE8c8iGO

### 安装 CNB CLI 和 Skills（Windows）

```bash
# 安装 CNB CLI
npm install @cnbcool/cnb-cli -g

# 安装 Skills 工具
npm install skills -g

# 添加 CNB Skill（用于增强 IDE 功能）
npx skills add https://cnb.cool/cnb/skills/cnb-skill.git --agent codebuddy -y --copy
```

### 验证安装

```bash
# 检查 CNB CLI 版本
cnb --version

# 检查 Skills 是否安装成功
skills list
```

安装成功后会显示已安装的技能列表，包括：
- cnb-api - CNB 平台交互命令
- cnb-code-commit - 代码提交和 PR 创建
- cnb-code-review - PR 代码评审
- cnb-docs - 文档操作
- cnb-pr-summary - PR 总结生成

---

## 步骤 1：检查项目状态

首先查看项目是否为 Git 仓库：

```bash
cd "中小商业银行课程"
git status
```

如果显示 `Not a git repository`，需要初始化：

```bash
git init
```

---

## 步骤 2：配置 .gitignore

创建 `.gitignore` 文件排除不需要同步的文件：

```bash
cat > .gitignore << EOF
*.lock
.DS_Store
Thumbs.db
EOF
```

---

## 步骤 3：初始提交

添加所有文件并进行首次提交：

```bash
git add .
git commit -m "Initial commit: 中小商业银行课程资料"
```

---

## 步骤 4：配置 Git 用户信息

```bash
git config --global user.name "cnb"
git config --global user.email "your-email@example.com"
```

---

## 步骤 5：登录 CNB（可选）

使用 CNB CLI 登录：

```bash
cnb login
```

按照提示打开浏览器完成授权。

---

## 步骤 6：查看可用组织

```bash
cnb organizations list-top-groups
```

找到您有权限的组织（例如：`xiaosicau`）。

---

## 步骤 7：查看组织下的仓库

```bash
cnb repositories get-group-sub-repos --slug xiaosicau
```

找到目标仓库（例如：`smartbanking`）。

---

## 步骤 8：配置远程仓库

使用令牌配置远程仓库地址：

```bash
git remote add origin https://cnb:your-token@cnb.cool/xiaosicau/smartbanking.git
```

**注意**：将 `your-token` 替换为您的实际访问令牌。

如果远程仓库已存在，更新地址：

```bash
git remote set-url origin https://cnb:your-token@cnb.cool/xiaosicau/smartbanking.git
```

---

## 步骤 9：推送代码

```bash
git push -u origin main
```

成功输出示例：

```
branch 'main' set up to track 'origin/main'.
Everything up-to-date
```

---

## 步骤 10：添加 README 文件（可选但推荐）

创建 `README.md` 文件：

```markdown
# 项目名称

项目简介...

## 文件结构

...
```

提交并推送：

```bash
git add README.md
git commit -m "Add README.md documentation"
git push
```

---

## 验证同步结果

访问 CNB 仓库地址查看同步结果：
- `https://cnb.cool/组织名/仓库名`

---

## 常见问题

### Q1：权限不足错误

```
remote: Your token does not have repo-code:rw permission
```

**解决方案**：在 CNB 平台检查令牌权限，确保具有 `repo-code:rw` 权限。

### Q2：仓库不存在错误

```
fatal: repository '...' not found
```

**解决方案**：确认组织名和仓库名正确，或在 CNB 平台创建新仓库。

### Q3：凭证锁错误

```
fatal: unable to get credential storage lock
```

**解决方案**：等待几秒后重试，或关闭其他 Git 进程。

---

## 完整命令汇总

```bash
# 1. 进入项目目录
cd "中小商业银行课程"

# 2. 初始化 Git（如未初始化）
git init

# 3. 创建 .gitignore
echo "*.lock" > .gitignore

# 4. 首次提交
git add .
git commit -m "Initial commit"

# 5. 配置远程仓库
git remote add origin https://cnb:your-token@cnb.cool/xiaosicau/smartbanking.git

# 6. 推送代码
git push -u origin main
```

---

## CNB 与 GitHub 命令对比

CNB（CodeNotebook）的基础 Git 命令与 GitHub **完全相同**，因为它们都基于 Git 版本控制系统。

### 1. 基础 Git 命令（完全相同）

| 操作 | Git 命令 | CNB 中使用 |
|------|----------|------------|
| 克隆仓库 | `git clone <url>` | ✅ 相同 |
| 添加文件 | `git add <file>` | ✅ 相同 |
| 提交 | `git commit -m "message"` | ✅ 相同 |
| 推送 | `git push origin main` | ✅ 相同 |
| 拉取 | `git pull origin main` | ✅ 相同 |
| 分支管理 | `git branch`, `git checkout` | ✅ 相同 |

### 2. CNB 专属 CLI 命令（额外功能）

CNB 提供了 `cnb` 命令行工具来管理平台资源：

```bash
# 登录/登出
cnb login
cnb logout

# 组织管理
cnb organizations list-top-groups
cnb organizations create-organization

# 仓库管理
cnb repositories list-repos
cnb repositories create-repo

# Issue 和 PR 管理
cnb issues list-issues
cnb pulls list-pulls

# AI 功能
cnb ai summarize-pr
```

### 3. 仓库地址格式（略有不同）

**GitHub**:
```
https://github.com/用户名/仓库名.git
git@github.com:用户名/仓库名.git
```

**CNB**:
```
https://cnb.cool/组织名/仓库名.git
https://cnb:令牌@cnb.cool/组织名/仓库名.git  (带令牌认证)
```

### 总结

- **Git 核心命令**：完全一致，您可以使用熟悉的 Git 命令进行代码管理
- **平台管理命令**：CNB 提供额外的 `cnb` CLI 来管理组织、仓库、Issue 等
- **认证方式**：CNB 使用访问令牌（Token）进行认证

如果您熟悉 GitHub 的使用，切换到 CNB 几乎没有学习成本！

---

**完成时间**：2026-06-02  
**CNB 仓库**：https://cnb.cool/xiaosicau/smartbanking
