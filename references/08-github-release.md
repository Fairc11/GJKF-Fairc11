# 08 — GitHub 发布流程

> 把工具发布到 GitHub，从 git 初始化到 Release 下载包

## 准备工作

| 工具 | 用途 | 安装方式 |
|------|------|----------|
| Git | 版本管理 | https://git-scm.com/ |
| curl | API 调用 | Windows 10/11 自带 |

## .gitignore 配置

在仓库根目录创建 `.gitignore`，排除敏感文件和不需要的文件：

```gitignore
# ── 敏感信息 ──────────────────────────────────
cookies.yaml                    # 登录 Cookie
.env                            # 环境变量
*.key                           # 密钥文件
*.pem                           # 证书

# ── 运行时数据 ────────────────────────────────
data/
logs/
*.log

# ── 构建产物 ──────────────────────────────────
dist/
build/
*.spec
*.exe

# ── 发布产物（走 GitHub Releases）─────────────
releases/

# ── 本地备份 ──────────────────────────────────
备份_*/

# ── Python 缓存 ──────────────────────────────
__pycache__/
*.pyc
*.pyo

# ── IDE / 编辑器 ──────────────────────────────
.vscode/
.idea/
*~

# ── OS ────────────────────────────────────────
Thumbs.db
desktop.ini
```

> ⚠️ 第一次 `git add` 之前一定要确认 `.gitignore` 已配置好，避免把密码、证书、token 等敏感文件提交上去。

## 首次发布

```bash
# 1. 初始化 git
cd 你的项目目录
git init
git checkout -b main

# 2. 添加所有文件
git add -A

# 3. 首次提交
git commit -m "feat: v1.0.0 - 初始版本"

# 4. 关联远程仓库
git remote add origin https://github.com/你的用户名/你的仓库名.git

# 5. 推送
git push -u origin main
```

## 日常发布流程

### 1. 查看变更

```bash
git status               # 看哪些文件改了
git diff --stat          # 看改动量
```

### 2. 提交代码

```bash
git add -A
git commit -m "feat: vX.X.X - 一句话概括本次更新"
```

### 3. 打标签

```bash
git tag vX.X.X           # 版本号前一定要带 v
```

### 4. 推送到 GitHub

```bash
git push origin main --tags
```

## 创建 Release

### 网页方式（推荐）

打开 `https://github.com/你的用户名/你的仓库名/releases/new`

| 字段 | 内容 |
|------|------|
| Tag version | `vX.X.X` |
| Release title | `vX.X.X` |
| Description | 更新说明（面向用户，不要写技术细节） |
| Attach binaries | 上传 zip 安装包 |

点 **Publish release**。

### API 方式

```bash
set TOKEN=你的_GitHub_Token
set VERSION=vX.X.X
set ZIP_PATH=C:\path\to\安装包_vX.X.X.zip

REM 第一步：创建 Release
curl -s -X POST ^
  -H "Authorization: token %TOKEN%" ^
  -H "Accept: application/vnd.github.v3+json" ^
  https://api.github.com/repos/你的用户名/你的仓库名/releases ^
  -d "{\"tag_name\":\"%VERSION%\",\"name\":\"%VERSION%\",\"body\":\"更新说明\",\"draft\":false,\"prerelease\":false}" > release.json

REM 提取 Release ID
for /f "tokens=2 delims=:," %%a in ('type release.json ^| findstr /C:"\"id\":"') do set REL_ID=%%a

REM 第二步：上传安装包
curl -s -X POST ^
  -H "Authorization: token %TOKEN%" ^
  -H "Content-Type: application/zip" ^
  "https://uploads.github.com/repos/你的用户名/你的仓库名/releases/%REL_ID%/assets?name=项目名_%VERSION%.zip" ^
  --data-binary @"%ZIP_PATH%"
```

> ⚠️ Token 有仓库读写权限，不要提交到代码里，用完及时撤销。

## 更新说明模板

```
🎉 项目名 vX.X.X

**新增**
- ...

**修复**
- ...

**优化**
- ...
```

## 一条龙示例

```bash
REM 假设当前版本是 v1.3.0

REM 1. 提交
git add -A
git commit -m "feat: v1.3.0 - 新增XX功能"

REM 2. 打标签
git tag v1.3.0

REM 3. 推送
git push origin main --tags

REM 4. 到 GitHub 网页创建 Release
```

## 常见问题

**Q: 不小心提交了敏感文件怎么办？**
```bash
git rm --cached 文件名
echo "文件名" >> .gitignore
git add .gitignore
git commit -m "chore: 移除敏感文件"
git push
```

**Q: Tag 打错了怎么删？**
```bash
git tag -d v1.2.0                  # 本地删除
git push origin :refs/tags/v1.2.0  # 远程删除
```

**Q: 怎么查看发布历史？**
打开 `https://github.com/你的用户名/你的仓库名/releases`

**Q: 提交后想改 commit message？**
```bash
git commit --amend -m "新的commit信息"
git push --force-with-lease
```
