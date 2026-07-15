---
name: gjkf-fairc11
description: Use when 用户要创建、接手、规范化、调试、跨平台改造、打包、验收或发布桌面工具、Web 工具、平台数据工具、媒体工具和数据管理工具，或提到“做一个工具”“项目做到一半”“项目乱了”“打包 DMG/EXE”“零前置条件”“干净机测试”“账号隔离”“上传 GitHub”“发布新版本”。
---

# GJKF-Fairc11 V2 — 跨平台工具开发工作流

## 核心原则

先读取事实源，再选择交付形态；先验证开发态，再验证用户真正收到的产物。不要把 Windows、macOS、Web、源码公开和二进制发布混成一条固定流水线。

## 开始前

1. 读取仓库内 `AGENTS.md`、`CLAUDE.md`、README、风险文档、架构决策、handoff、release checklist 和测试命令。
2. 确认真实仓库根目录、当前分支、Git 状态、未跟踪文件和已有产物。
3. 把用户文件、登录数据、运行时数据和构建资源分开识别。
4. 不确定路径、键名、按钮文字、版本号或产物状态时，读取代码、配置、日志或真实产物；禁止猜测。
5. 发现已有未提交改动时，先确定归属；不得覆盖、恢复或顺手提交。

已有项目先读 [项目接入与事实源](references/project-intake.md)。

## 第一步：选择交付形态

不要默认使用 FastAPI + pywebview，也不要因为开发者只有一台 Mac 就直接放弃 Windows 用户。

| 需求 | 优先评估 | 关键限制 |
|---|---|---|
| 本机文件、系统窗口、离线处理、私有登录态 | 原生或桌面壳 | 需要分平台打包与验收 |
| 现有前端和后端已经是 HTTP 架构 | 本地 Web + 薄桌面壳 | 浏览器与本地服务生命周期 |
| Windows 用户只需通过浏览器使用 | 托管 Web 或局域网 Web | 服务端成本、账号安全、上传数据 |
| 纯本地且需要真正跨平台安装包 | Tauri/Electron/Qt/pywebview | 重写成本、系统 WebView 差异 |
| 自动化、批处理、开发者使用 | CLI | 普通用户门槛较高 |

必须比较“保留现有后端 + 新增 Web 入口”“分平台桌面壳”“全面迁移跨平台框架”三类方案的改动量、能力缺口和维护成本。

详见 [交付形态与平台决策](references/delivery-platform-decision.md)。

## 第二步：判定当前状态

不要用“存在 `desktop_app.py`”就宣布桌面端完成。按证据判定：

| 状态 | 最低证据 |
|---|---|
| 需求明确 | 成功标准、非目标、数据边界已确认 |
| 开发态可用 | 核心流程真实运行，自动测试通过 |
| 桌面态可用 | 真实窗口、系统桥接、退出与日志通过 |
| 可构建 | 构建脚本输出预期架构产物 |
| 封包态可用 | 从 `.app`、DMG、onedir 或安装包启动并完成核心流程 |
| 可交付 | 清运行时或干净机通过，前置条件已写明 |
| 可公开 | 仓库和资产审计通过，许可证与发布政策无冲突 |

输出必须包含：当前状态、已验证证据、未验证边界、推荐下一步。避免使用虚构百分比。

详见 [项目接入与事实源](references/project-intake.md)。

## 第三步：实施循环

1. 为行为变化先写测试或最小复现。
2. 做最小实现，不顺手改无关架构。
3. 运行针对性测试。
4. 运行项目规定的全量门禁。
5. 涉及路径、资源、登录或浏览器时，同时验证开发态和 frozen/封包态。
6. 同步更新用户文档、开发文档和内部事实源，但按公开级别分离内容。
7. 精确暂存目标文件；禁止默认使用 `git add -A`。

遇到 Bug 时使用 `systematic-debugging` 或项目规定的诊断流程。详见 [开发与调试循环](references/development-debugging.md)。

## 第四步：数据与账号隔离

至少区分四类数据：

| 类型 | 示例 | 能否打包 | 能否迁移 |
|---|---|---:|---:|
| 只读程序资源 | 模板、图标、内置浏览器归档 | 可以 | 随应用 |
| 登录数据 | Cookie 文件、WKWebView/WebView2 站点数据、token | 禁止 | 默认禁止 |
| 运行时数据 | 日志、缓存、数据库、任务状态 | 禁止 | 按产品设计 |
| 用户产物 | 电子书、媒体、导出数据库 | 禁止 | 可以整体迁移 |

必须同时审计：Git 跟踪内容、构建配置、真实封包产物、发布资产。不能只看 `.gitignore`，也不能只看 PyInstaller `datas`。

不要把“文件权限隔离”写成“钥匙串加密”。不要猜测 WebKit/WebView2 的物理数据路径；从实现读取并只声明已验证边界。

详见 [账号、隐私与数据隔离](references/account-data-isolation.md)。

## 第五步：按平台构建

### macOS

关注 `.app`/DMG、目标架构、最低系统版本、系统 WebKit、应用数据目录、ad-hoc/Developer ID 签名、公证和 Gatekeeper。使用者是否可以首次打开，必须写成明确前置条件。

详见 [macOS 打包与分发](references/packaging-macos.md)。

### Windows

关注 PyInstaller onedir、Inno Setup、WebView2、`%LOCALAPPDATA%`、GBK/UTF-8、无控制台输出和卸载残留。不要把 onefile 当成默认目标。

详见 [Windows 打包与分发](references/packaging-windows.md)。

### Web

区分本机 Web、局域网 Web和公网托管 Web。不得把需要开发者电脑持续运行的本机服务描述成“任何 Windows 用户打开网页就能使用”。

详见 [Web 交付与跨平台入口](references/web-delivery.md)。

## 第六步：封包态验收

开发版通过不代表产物可交付。至少验证：

1. 真实产物启动、核心流程、退出和日志。
2. 资源存在且版本一致；必要时挂载 DMG或检查 onedir 内文件哈希。
3. 临时移走开发机缓存和运行时目录后仍可运行。
4. 新用户目录、虚拟机、Sandbox 或另一台机器的首次使用流程。
5. 安装包内没有登录数据、用户产物、日志或个人路径。
6. README 中的系统、架构、磁盘、网络、账号、浏览器和首次打开条件与产物一致。

详见 [封包态与干净环境验收](references/packaged-acceptance.md)。

## 第七步：仓库与发布策略

先分清四种动作：

1. 只在本地 Git 提交。
2. 推送公开或私有源码仓库。
3. 私域交付二进制。
4. 创建公开 Release 并上传二进制。

这些动作授权不同，不能相互推导。用户说“上传 GitHub”时，先确认是源码、标签、PR、Release 还是安装包。

发布前：

- 精确暂存并审查 `git diff --cached --name-status`。
- 检查 Git 历史和已跟踪文档中的个人路径、真实账号、档案统计和密钥。
- 区分 README 用户说明、DEVELOPMENT 开发说明、内部 handoff/验收证据。
- 检查许可证授权与维护者的官方二进制发布政策是否被混写。
- 用户未明确授权时，不 push、不建标签、不创建 Release、不替换线上资产。

详见 [仓库公开与发布策略](references/repository-release-strategy.md)。

## 文档职责

| 文件 | 读者 | 内容 |
|---|---|---|
| README | 普通用户和仓库访客 | 用途、前置条件、安装、使用、隐私、风险、分发边界 |
| DEVELOPMENT | 开发者 | 环境、架构、启动、构建、测试、路径规则 |
| AGENTS/CLAUDE | 代理与维护者 | 不变量、验证命令、危险操作、事实源入口 |
| handoff/验收记录 | 内部维护 | 真实路径、阶段证据、未完成项；公开前单独审计 |
| CHANGELOG/Release notes | 版本使用者 | 已交付变化，不写未经验证的计划 |

## 完成声明门禁

只有获得对应证据时才可以这样表述：

- “代码完成”需要自动测试和项目门禁。
- “Mac/Windows 端完成”需要真实桌面产物验收。
- “可直接下载安装”需要前置条件、首次打开和干净环境证据。
- “不包含个人信息”需要 Git、构建配置和真实产物三层检查。
- “可以公开 GitHub”需要整个已跟踪仓库与历史的公开前审计；README 干净不等于仓库干净。
- “已发布”需要远程标签、Release 和资产的实际状态。

## 红旗

- 未读事实源就按旧经验改项目。
- 把 Windows 路径、按钮名或注册表键套到 macOS/Web。
- 把开发态成功当成封包态成功。
- 只检查 `.gitignore` 就宣称没有敏感数据。
- 只检查 README 就宣称整个仓库可以公开。
- 用 `git add -A` 混入用户文件。
- 用户只授权本地提交，却顺手 push、建标签或 Release。
- 用过时 handoff 否定已经重新构建的真实产物，或反过来只看产物忽略长期文档失真。

任何一项出现，都应停止完成声明并补充证据。

## 引用导航

| 场景 | 读取 |
|---|---|
| 接手已有项目、状态混乱 | [项目接入与事实源](references/project-intake.md) |
| 选择 Mac、Windows、Web 或混合方案 | [交付形态与平台决策](references/delivery-platform-decision.md) |
| 开发、修复、性能与回归 | [开发与调试循环](references/development-debugging.md) |
| Cookie、WebView 数据、用户档案 | [账号、隐私与数据隔离](references/account-data-isolation.md) |
| macOS `.app`、DMG、签名、公证 | [macOS 打包与分发](references/packaging-macos.md) |
| Windows onedir、Inno、WebView2 | [Windows 打包与分发](references/packaging-windows.md) |
| 新增浏览器入口或减少 Windows 改动 | [Web 交付与跨平台入口](references/web-delivery.md) |
| 封包态、清运行时、干净机 | [封包态与干净环境验收](references/packaged-acceptance.md) |
| GitHub、源码公开、私域和 Release | [仓库公开与发布策略](references/repository-release-strategy.md) |
