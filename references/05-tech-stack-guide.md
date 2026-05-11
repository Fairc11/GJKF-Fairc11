# 05 — 技术栈推荐决策树

> 根据项目需求动态推荐最优技术栈

## 决策树

```
开始 → 问用户：这个工具解决什么问题？
    │
    ├─ 需要图形界面吗？
    │   ├─ ❌ 不需要 → CLI 工具
    │   │   └─ Python + argparse + requests
    │   │
    │   └─ ✅ 需要 → 桌面端还是 Web 端？
    │       │
    │       ├─ 🖥️ 桌面端
    │       │   ├─ pywebview（轻量，Windows）
    │       │   │   ├─ Python 生态，FastAPI 后端
    │       │   │   ├─ 资源占用小，适合小工具
    │       │   │   └─ 缺点：仅 Windows，Edge 依赖
    │       │   │
    │       │   ├─ Tauri（跨平台，现代）
    │       │   │   ├─ Rust + 系统 WebView
    │       │   │   ├─ 打包小，性能好
    │       │   │   └─ 缺点：需要 Rust 编译环境
    │       │   │
    │       │   └─ Electron（重量级）
    │       │       └─ 不推荐：打包 100MB+，除非必须
    │       │
    │       └─ 🌐 Web 端
    │           ├─ 复杂度如何？
    │           │   ├─ 简单 CRUD / 单页工具
    │           │   │   └─ FastAPI + Jinja2 [默认路线]
    │           │   │
    │           │   ├─ 中等复杂度
    │           │   │   └─ FastAPI + Alpine.js + Tailwind
    │           │   │
    │           │   └─ 高交互 / 复杂 SPA
    │           │       └─ FastAPI + React/Vue
    │           │
    │           └─ 部署方式？
    │               ├─ 纯本地 → 无额外需求
    │               └─ 需要远程访问 → 加 Nginx 反向代理
    │
    ├─ 需要抓取/网页自动化吗？
    │   ├─ ✅ 需要
    │   │   ├─ 简单 REST API 调用
    │   │   │   └─ httpx / requests
    │   │   ├─ 需要渲染 JS 的 SPA 页面
    │   │   │   └─ Playwright [默认]
    │   │   └─ 大量数据采集
    │   │       └─ Scrapy + Playwright
    │   │
    │   └─ ❌ 不需要 → 跳过
    │
    ├─ 需要打包分发吗？
    │   ├─ ✅ 需要
    │   │   ├─ 纯 Python → PyInstaller [默认]
    │   │   └─ 需要性能优化 → Nuitka
    │   │
    │   └─ ❌ 不需要 → dev 模式即可
    │
    └─ 用户已有工具集？
        └─ Ptu 风格 → FastAPI + Playwright + pywebview
```

## 默认路线说明

### FastAPI + Playwright + pywebview

这是用户的默认路线，适合大多数工具场景。

**适用场景**：本地运行的爬虫/媒体处理/数据管理工具
**优点**：Python 全栈、开发快、打包简单
**缺点**：仅 Windows、不适合跨平台分发

### 什么时候换路线

| 场景 | 推荐路线 |
|------|---------|
| 跨平台桌面应用 | Tauri + Rust |
| 高性能后端 | FastAPI + asyncpg |
| 需要远程访问 | FastAPI + Nginx + 前端框架 |
| 纯数据处理（无 UI） | Python CLI + argparse |
| 移动端 | Flutter / React Native |

## 迁移指南

### pywebview → Tauri

如果需要跨平台分发，从 pywebview 迁移到 Tauri：

1. 保留 FastAPI 后端不变
2. 用 Tauri 替代 pywebview（Tauri 的 WebView 通过 Rust 包装）
3. Tauri 前端可以是任何 Web 框架
4. 通信方式从 `JsApi` 类换成 Tauri 的 `invoke` API
