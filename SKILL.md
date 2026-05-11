---
name: GJKF-Fairc11
description: 用于构建桌面工具类软件（Python FastAPI 后端 + Web 前端或 pywebview 桌面端）。用户说"做一个XX工具"、"帮我开发一个XX"、"做到一半了帮我看看"时触发。适用于：平台内容抓取工具、媒体处理工具、数据管理工具、任何需要 Web UI 或桌面端的 Python 工具。默认技术路线 FastAPI + Playwright + pywebview，根据需求动态推荐其他技术栈。
---

# GJKF-skill — 工具开发工作流

> 基于实际项目的经验总结：Ptu（抖音图文下载器，v1.1.0） + 微书薯（微博备份工具）

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

## 1. 核心开发流程（6+1阶段）

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

详见 `references/03-packaging-guide.md`

**验收**：打包 EXE 在其他机器能正常运行

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

1. **开发模式下必须模拟打包后的路径行为** — 用 `setup_check.py` 中的路径判断逻辑，让 dev 和 prod 路径一致
2. **只有全部功能验证通过才进打包流程**
3. **打包前跑一遍完整的冒烟测试**：启动 → 登录（如果有）→ 核心功能 → 退出
4. **生成 `启动.bat`** — 用户双击就能启动 dev 模式，不用敲命令

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

## 脚手架模板

`assets/scaffold/` 包含项目初始化模板文件，在阶段 0 时使用。
