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

**完成时间**：2026-06-02  
**CNB 仓库**：https://cnb.cool/xiaosicau/smartbanking
