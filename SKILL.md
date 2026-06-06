---
name: GJKF-Fairc11
description: Use when 用户要做桌面工具、Web 工具、平台抓取工具、媒体处理工具或数据管理工具，或提到"做一个XX工具"、"帮我开发"、"做到一半了"、"项目乱了"、"规范化"、"性能太慢"、"又报错了"、"打包"、"零前置条件"、"干净机测试"、"发布新版本"、"上传到GitHub"、"打标签"、"发布Release"、"帮我发版"。
---

# GJKF-skill — 工具开发工作流

> 基于实际项目的经验总结：Ptu（抖音图文下载器，已沉淀到零前置条件发布流程） + 微书薯（微博备份工具）

## 快速使用

### 场景 A：从零开始一个新工具

```
1. 执行"阶段 -1：需求分析" → 明确功能清单 + 确定技术栈
2. 按阶段顺序推进：阶段 0 → 1 → 2 → 3 → 4
3. 每个阶段完成后验证再进入下个阶段
```

### 场景 B：项目做到一半，有点乱，想接上规范流程

```
1. 先执行"半路接入诊断"（见下方）
2. 根据诊断报告决定：继续当前阶段 / 补漏 / 跳到下阶段
3. 用脚手架模板对齐项目结构，不破坏已有代码
```

### 场景 C：修 Bug / 迭代优化

```
1. 进入"快速开发循环"：开发模式改 → 测试 → 改 → 测试
2. 全部验证通过后再打包
3. 避免"改→打包→测试→又改→又打包"的循环
```

### 场景 D：发布新版本 / 上传到 GitHub

```
1. 完成阶段 4 打包后，先进入"阶段 4.5：封包态验收"
2. 通过开发版测试、封包版冒烟、干净机/清运行时测试
3. 用户确认可用后，再进入"阶段 5：GitHub 发布"
4. 做资产审计 → commit → tag → push → 创建 Release + 上传安装包
```

---

## 必须先守住的红线

1. **先读项目事实源**：接手已有项目时，先找 README、AGENTS/CLAUDE、技术文档、release checklist、handoff/plan；不要凭记忆判断项目状态。
2. **零前置条件优先**：面向普通用户分发的桌面工具，默认目标是安装后无需手装 Python、浏览器、FFmpeg、Node、证书或其他运行时依赖；确实无法内置时要写清楚检测、提示和降级路径。
3. **开发版能跑不等于封包版能发**：`python run.py` 通过后，还必须单独验收 PyInstaller/Inno Setup 产物，覆盖 `sys.frozen`、`sys.stdout is None`、CWD、hiddenimports、datas、权限路径和内置依赖。
4. **运行时数据不写安装目录**：安装到 `C:\Program Files\...` 后，日志、缓存、Cookie、数据库、下载临时文件必须写到用户可写目录，如 `%LOCALAPPDATA%\项目名`。
5. **敏感文件绝不进仓库/安装包**：`.env`、`cookies.yaml`、token、日志、运行时目录和本地缓存必须在 git 跟踪、打包 datas、Release 资产三层都排除。
6. **用户确认前不替换线上资产**：发布前可以准备 tag、草稿和安装包，但正式 GitHub Release/资产替换必须等用户确认封包版或干净机测试通过。
7. **长期真相来源要同步更新**：版本号、README、AGENTS/CLAUDE、技术文档、release checklist、测试记录和 GitHub Release notes 不应相互矛盾。

---

## 0. 半路接入 — 项目阶段诊断

项目开发到一半想规范化时，执行以下诊断：

### 诊断扫描

扫描项目目录，检查以下内容：

| 检查项 | 判断标准 |
|--------|----------|
| 目录结构 | 是否存在 `backend/`、`frontend/`、`app/` 等标准目录 |
| 配置文件 | 是否存在 `config.yaml`、`.env`、`requirements.txt` |
| 入口文件 | 是否存在 `run.py`、`main.py` |
| 后端代码 | 是否存在 `models/`、`services/`、`api/routers/` |
| 前端代码 | 是否存在 `templates/`、`static/` |
| 桌面端 | 是否存在 `desktop_app.py`、pywebview 相关代码 |
| 打包配置 | 是否存在 `build.spec`、`setup_check.py`、`installer.iss` |

### 阶段判定

| 阶段 | 判断条件 |
|------|----------|
| 阶段 -1（需求分析） | 只有需求文档，无代码 |
| 阶段 0（脚手架） | 有入口文件 + 配置文件，无核心业务代码 |
| 阶段 1（后端） | 有 models/services/routers，无前端 |
| 阶段 2（前端） | 有 templates/static/，无桌面端 |
| 阶段 3（桌面端） | 有 desktop_app.py |
| 阶段 4（打包） | 有 build.spec / PyInstaller 配置 |
| 阶段 4.5（封包态验收） | 有可运行安装包/onedir，且已做清运行时或干净机测试 |

### 诊断输出

```
当前阶段：阶段 X（已完成 Y%）
已完成：[列表]
缺失/待完成：[列表]
推荐操作：
  方案 A：继续在当前阶段收尾
  方案 B：跳到下个阶段
  方案 C：先补漏再继续
```

详见 `references/07-phase-diagnosis.md`

---

## 1. 核心开发流程（7+1阶段）

### 阶段 -1：需求分析

**目标**：明确工具要做什么、用什么做

**步骤**：
1. 用户描述需求 → 整理成功能清单
2. 执行技术栈决策树（见 `references/05-tech-stack-guide.md`）
3. 确定项目名称和目录位置
4. 产出：一份 PRD / 功能清单

**验收**：用户确认功能清单无误，技术栈确定

### 阶段 0：项目脚手架

**目标**：搭建项目骨架，确保能跑起来

**步骤**：
1. 创建标准目录结构（参考 `references/02-project-templates.md`）
2. 编写 `config.yaml` + `.env`（配置管理参考 `assets/scaffold/`）
3. 编写 `run.py` 入口
4. 编写 `requirements.txt`
5. 生成 `启动.bat` 快捷入口
6. 验证：`python run.py` 能正常启动

**产出**：项目骨架代码、快捷启动脚本

### 阶段 1：后端核心

**目标**：实现核心业务逻辑

**步骤**（FastAPI 默认路线）：
1. `models/schemas.py` — Pydantic 数据模型、请求/响应结构
2. `models/task_store.py` — 数据持久化（JSON 文件 / SQLite）
3. `services/` — 核心业务服务层
4. `api/routers/` — API 接口层
5. `main.py` — FastAPI 应用组装 + 静态文件挂载

**关键模式**：
- 三层架构：models → services → routers
- WebSocket 实时进度推送（`router_ws.py`）
- 中文错误提示（参考 `references/06-cn-error-handling.md`）

**验收**：所有 API 端点可用，返回正确数据

### 阶段 2：前端 / UI

**目标**：用户交互界面

**步骤**：
1. `templates/base.html` — 基础布局
2. `templates/index.html` — 主页面
3. `static/css/app.css` — 样式
4. `static/js/app.js` — 前端交互

**验收**：所有功能可通过界面操作

### 阶段 3：桌面端（可选）

**目标**：pywebview 包装成桌面应用

**步骤**：
1. 编写 `desktop_app.py`
2. JS-Python 桥接（`js_api.py`）
3. 系统托盘、单实例锁、窗口位置记忆

详见 `references/04-desktop-pattern.md`

**验收**：双击启动显示原生窗口

### 阶段 4：打包发布

**目标**：可分发 EXE

**步骤**：
1. `setup_check.py` — 环境自检
2. `build.spec` — PyInstaller 配置
3. `build_exe.bat` — 一键打包
4. `installer.iss` — Inno Setup 安装包（可选）
5. 内置或检测必要运行时依赖（浏览器、FFmpeg、WebView2、证书等）
6. 确认运行时数据、日志和缓存写入用户可写目录

详见 `references/03-packaging-guide.md`

**验收**：打包 EXE 在其他机器能正常运行

### 阶段 4.5：封包态与干净机验收

**目标**：证明用户拿到的安装包真的可用

**步骤**：
1. 开发版验证：测试、编译检查、release check 或等价脚本全部通过
2. 封包版冒烟：双击 EXE/安装包，验证启动、核心功能、日志、退出
3. 清运行时验证：临时移走本机缓存和依赖目录，确认不会依赖开发机残留
4. 干净机验证：Windows Sandbox、虚拟机或另一台机器安装运行
5. 失败时收集用户数据目录下的日志，不要只让用户压缩安装目录

详见 `references/09-zero-prereq-release.md`

**验收**：无手动前置安装，核心流程在干净环境通过；用户确认前不发布正式 Release

### 阶段 5：GitHub 发布

**目标**：把工具发布到 GitHub，创建 Release，用户能下载安装包

**触发场景**："发布新版本"、"上传到GitHub"、"打标签发布"

**步骤**：
1. 先确认真实 repo root，不要在外层源码目录误跑 tag/release
2. 做发布资产审计：必须上传、绝不上传、可选上传
3. 配置 `.gitignore`（敏感文件、运行时数据、构建缓存要排除；可复现构建配置通常要保留）
4. `git add -A` → `git commit -m "feat: vX.X.X - 更新说明"`
5. `git tag vX.X.X`
6. `git push origin main --tags`
7. 用户确认后创建 GitHub Release + 上传安装包

**Commit message 规范**：

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: v1.3.0 - 新增用户主页抓取` |
| `fix:` | 修 Bug | `fix: 修复登录按钮不响应` |
| `docs:` | 文档 | `docs: 更新使用说明` |
| `chore:` | 杂项 | `chore: 清理敏感文件` |
| `refactor:` | 重构 | `refactor: 重写抓取逻辑` |

详见 `references/08-github-release.md`

**验收**：GitHub 仓库可见，Release 可下载

---

## 2. 快速开发循环

> 核心目标：减少"改 → 打包 → 测试 → 再打包"的循环

### 开发模式 vs 生产模式

```
开发模式（python run.py）        生产模式（PyInstaller EXE）
─────────────────────────────    ─────────────────────────
python run.py 直接跑             双击 EXE 运行
热重载，改完即生效                改完要重新打包
错误直接显示在终端                 弹出友好中文提示
路径用开发目录                     路径用打包后的环境
```

### 关键规则

1. **路径一致性** — 开发模式下必须模拟打包后的路径行为，用 `sys.frozen` + `sys._MEIPASS` 检测，让 dev 和 prod 路径一致
2. **阶段门禁** — 每个阶段完成后必须验证再进入下个阶段，不跳过验收
3. **先复现再修** — 错误必须先能稳定复现，找到根因再修复，不猜原因
4. **先 profile 再优化** — 性能问题先测出瓶颈（IO vs CPU），再针对优化，不盲目改
5. **打包前冒烟** — 打包前跑完整冒烟测试：启动 → 核心功能 → 退出，确认正常再打包
6. **快捷入口** — 生成 `启动.bat`，用户双击就能启动 dev 模式，不用敲命令
7. **验收证据先行** — 说“完成/可发布”前必须有命令输出、日志路径、产物路径或干净机测试记录
8. **文档同步** — 代码改动涉及版本、入口、依赖、发布或用户流程时，同步更新 README、AGENTS/CLAUDE、技术文档或 release checklist

---

## 3. 调试体系

### 通用调试流程

```
1. 复现问题 → 2. 缩小范围 → 3. 根因分析 → 4. 修复 → 5. 验证闭环
```

### 常见问题分类速查

**爬虫/抓取类：**
- API 返回空 → 检查 Cookie/登录态 → 检查端点是否更新 → 检查参数
- 提取数量不对 → 是否混入了推荐内容 → 懒加载 → 分页未处理
- Playwright 提取失败 → 浏览器路径 → 页面结构变化 → 超时

**桌面端：**
- 打包后闪退 → hiddenimports 缺失 → 路径不对 → 资源文件缺失
- 编码错误 → Windows gbk ↔ UTF-8 冲突
- 端口被占用 → 自动检测 + 备用端口
- 干净机失败 → 开发机缓存依赖 → 检查内置浏览器/FFmpeg/WebView2/证书和用户数据目录
- 安装目录权限错误 → 运行时数据写入 `{app}`/`Program Files` → 改写到 `%LOCALAPPDATA%`

详见 `references/01-debug-checklist.md`

---

## 4. 技术栈决策树

根据项目需求动态推荐：

```
需要图形界面吗？
├─ 否 → CLI 工具（Python + argparse）
└─ 是 → 桌面端还是 Web 端？
    ├─ 桌面端 → pywebview（轻量）| Tauri（跨平台）
    └─ Web 端 → 复杂度如何？
        ├─ 简单 → FastAPI + Jinja2（默认路线）
        └─ 复杂 → FastAPI + React/Vue

需要抓取/自动化吗？
├─ 是 → Playwright（默认）| requests（简单 API）
└─ 否 → 跳过

需要打包分发吗？
├─ 是 → PyInstaller（Python）| Nuitka（性能）
└─ 否 → dev 模式即可
```

详见 `references/05-tech-stack-guide.md`

---

## 5. 中文错误处理

所有用户可见的错误信息必须用中文：

```python
class ToolError(Exception):
    """统一异常：用户看 cn_message，调试看 en_debug"""
    def __init__(self, cn_message: str, en_debug: str = ""):
        self.cn_message = cn_message
        self.en_debug = en_debug

# API 错误响应格式
{"error": true, "message": "Cookie 已过期，请重新登录", "detail": "..."}
```

详见 `references/06-cn-error-handling.md`

---

## 参考文件索引

| 文件 | 内容 | 什么时候读 |
|------|------|-----------|
| `references/00-development-flow.md` | 各阶段详细执行步骤、验收标准 | 执行每个阶段前 |
| `references/01-debug-checklist.md` | 问题排查清单 | 遇到 Bug 时 |
| `references/02-project-templates.md` | 项目结构模板、代码模板 | 阶段 0 脚手架 |
| `references/03-packaging-guide.md` | PyInstaller + Inno Setup | 阶段 4 打包 |
| `references/04-desktop-pattern.md` | pywebview 桌面端实现 | 阶段 3 桌面端 |
| `references/05-tech-stack-guide.md` | 技术栈决策树 | 阶段 -1 技术选型 |
| `references/06-cn-error-handling.md` | 中文错误处理规范 | 阶段 1 写 API 时 |
| `references/07-phase-diagnosis.md` | 半路接入诊断 | 项目做到一半接入时 |
| `references/08-github-release.md` | GitHub 发布流程 | 阶段 5 发布时 |
| `references/09-zero-prereq-release.md` | 零前置条件和干净机发布门禁 | 阶段 4.5 验收时 |

## 脚手架模板

`assets/scaffold/` 包含项目初始化模板文件，在阶段 0 时使用。
