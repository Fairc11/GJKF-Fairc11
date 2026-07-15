# GJKF-Fairc11 V2

面向桌面工具、Web 工具、平台数据工具、媒体工具和数据管理工具的跨平台开发工作流 Skill。

V2 不再默认使用“Windows + EXE + Inno Setup”路线，而是先读取项目事实源，再根据真实需求选择 macOS、Windows、Web、CLI 或混合交付方案，并分别完成开发态、封包态、隐私和发布验收。

## V2 更新内容

| 方面 | V1 | V2 |
|---|---|---|
| 平台 | 主要面向 Windows EXE | macOS、Windows、Web 分别决策和验收 |
| 技术路线 | 默认 FastAPI + pywebview | 先比较现有后端复用、分平台桌面壳和跨平台迁移 |
| macOS | 缺少正式路线 | `.app`、DMG、arm64、Developer ID、公证、Gatekeeper |
| Windows | EXE/Inno 单一路线 | PyInstaller onedir、Inno、WebView2、用户数据目录 |
| Web | 简单技术树分支 | 本机 Web、局域网 Web、公网托管 Web分别评估 |
| 隐私 | 主要检查 Cookie 文件 | Cookie、WKWebView/WebView2、运行时数据、用户产物四层隔离 |
| 仓库发布 | 容易直接进入 GitHub Release | 本地提交、源码公开、私域二进制、公开 Release 分开授权 |
| Git | 曾使用 `git add -A` | 默认精确暂存并审查缓存区 |
| 验收 | 开发版和 EXE 验收 | 开发态、封包态、清运行时、干净环境四级门禁 |
| 文档 | README 与开发记录容易混合 | README、DEVELOPMENT、AGENTS、handoff 分级管理 |

## 适用场景

- 从零开发一个工具。
- 接手做到一半、结构混乱的项目。
- 修复开发态正常但封包态失败的问题。
- 把 Mac 工具增加 Windows 或浏览器使用方式。
- 打包 `.app`、DMG、EXE 或安装器。
- 检查安装包是否包含账号、Cookie 或个人数据。
- 做清运行时、干净机和首次启动验收。
- 提交 Git、上传 GitHub、创建 PR 或发布 Release。

## 使用方法

在 Codex 中调用：

```text
$gjkf-fairc11
```

示例：

```text
使用 $gjkf-fairc11 检查这个工具现在处于什么阶段，并制定最小改动的 Mac 与 Windows 交付方案。
```

```text
使用 $gjkf-fairc11 审查安装包、Git 仓库和发布资产中是否包含我的登录信息或个人数据。
```

Skill 的磁盘目录仍保留 `GJKF-Fairc11`，界面显示为 `GJKF-Fairc11 V2`；调用标识使用符合新版规范的小写 `$gjkf-fairc11`。

## 核心流程

1. 读取项目事实源和 Git 状态。
2. 选择桌面端、Web、CLI 或混合交付形态。
3. 通过测试与最小改动完成开发。
4. 隔离程序资源、登录数据、运行时数据和用户产物。
5. 按 macOS、Windows 或 Web 路线构建。
6. 验证真实封包产物和干净环境。
7. 区分本地提交、源码公开、私域交付和公开 Release。

完整工作流见 [SKILL.md](SKILL.md)。

## 资料结构

```text
GJKF-Fairc11/
├── SKILL.md
├── agents/openai.yaml
└── references/
    ├── project-intake.md
    ├── delivery-platform-decision.md
    ├── development-debugging.md
    ├── account-data-isolation.md
    ├── packaging-macos.md
    ├── packaging-windows.md
    ├── web-delivery.md
    ├── packaged-acceptance.md
    └── repository-release-strategy.md
```

旧版固定脚手架已经移除。V2 会先读取现有项目结构，再决定是否创建或调整脚手架，避免把 Windows 专用文件强加给 macOS、Web 或已有项目。

## 隐私原则

- 不把 Cookie、token、WebView 站点数据、日志、缓存和用户产物加入 Skill、仓库或安装包。
- 不用 `.gitignore` 代替 Git 历史、构建配置和真实产物审计。
- 不把文件权限隔离描述成钥匙串加密。
- README 通过检查不等于整个仓库已经适合公开。
- 用户只授权本地提交时，不自动 push、建标签或创建 Release。

## 验证

V2 已通过：

- Skill frontmatter 官方验证；
- 主入口与全部 references 的相对链接检查；
- macOS、发布分离、账号隔离和 Web 交付场景断言；
- Git 差异与隐私扫描。

## 许可证

MIT，详见 [LICENSE](LICENSE)。
