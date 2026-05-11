# GJKF-Fairc — 工具开发工作流 Skill

> **版本 1.0.0** | 基于实战经验沉淀的 Claude Code Skill

GJKF-Fairc 是一个 Claude Code Skill，用于**规范化桌面工具类软件的开发流程**。它把从零到一的开发过程拆解为清晰的阶段，同时支持项目开发到一半时「半路接入」诊断。

## 解决的问题

你有没有遇到过这样的情况？

- 做个工具，做着做着项目结构就乱了
- 改完 Bug → 打包 → 测试 → 又改 → 又打包，循环到崩溃
- 每次都要敲一堆命令行才能启动
- 英文报错看不懂，不知道出了什么问题

GJKF-Fairc 就是解决这些问题的。

## 适用场景

| 场景 | 说明 |
|------|------|
| 🆕 从零开始做工具 | 按 6 个阶段逐步推进，每个阶段有明确验收标准 |
| 🔧 项目做到一半想规范 | 用「半路接入」诊断当前状态，对齐标准结构 |
| 🐛 迭代修 Bug | 开发模式快速改 → 测试，全部验证通过再打包 |
| 🖥️ 桌面工具 / Web 工具 / CLI 工具 | 灵活技术栈推荐 |

## 快速开始

### 安装

```bash
# 将 .skill 文件放到 Claude Code 的 skill 目录
cp GJKF-Fairc.skill ~/.claude/skills/

# 或者在 Claude Code 中直接加载
# Claude Code 会自动识别
```

### 使用

在 Claude Code 中说：

```
"我想做一个抖音图片下载工具"
"帮我开发一个微博备份工具"
"这个项目做到一半了，有点乱，帮我看看现在到哪了"
```

Claude 会自动触发 GJKF-Fairc Skill，按标准化流程推进。

## 核心流程

### 6+1 阶段

```
阶段 -1: 需求分析 → 明确功能 + 确定技术栈
阶段 0:  项目脚手架 → 目录结构 + 配置 + 启动脚本
阶段 1:  后端核心 → models → services → routers
阶段 2:  前端/UI → 模板 + 交互 + 样式
阶段 3:  桌面端 → pywebview（可选）
阶段 4:  打包发布 → PyInstaller + 安装包
```

### 半路接入

项目开发到一半也能接入：

1. 扫描项目目录结构
2. 检查各阶段产出物
3. 输出诊断报告（当前阶段、完成度、缺失项）
4. 推荐操作（继续 / 补漏 / 跳转）
5. 用脚手架模板标准化对齐

## 默认技术路线

```
后端: FastAPI + Uvicorn
前端: Jinja2 + 原生 JS + CSS
爬虫: Playwright（按需）
桌面: pywebview（按需）
打包: PyInstaller + Inno Setup（按需）
```

> 也支持根据项目需求推荐其他技术栈（Tauri、React、Node.js 等）。

## Skill 结构

```
GJKF-Fairc/
├── SKILL.md                    # 主流程指令
├── references/
│   ├── 00-development-flow.md     # 阶段化开发流程
│   ├── 01-debug-checklist.md      # 问题排查清单
│   ├── 02-project-templates.md    # 项目结构模板
│   ├── 03-packaging-guide.md      # 打包指南
│   ├── 04-desktop-pattern.md      # 桌面端模式
│   ├── 05-tech-stack-guide.md     # 技术栈决策树
│   ├── 06-cn-error-handling.md    # 中文错误处理
│   └── 07-phase-diagnosis.md      # 半路接入诊断
└── assets/scaffold/               # 脚手架模板
```

## 设计理念

- **基于实战**：从 Ptu（抖音下载器，v1.1.0）和微书薯（微博备份工具）两个真实项目中提炼
- **全中文**：所有用户可见的消息都是中文
- **渐进式**：需要什么读什么 reference，不一次加载全部
- **灵活**：默认 FastAPI 路线，但根据需求动态推荐

## 技术栈要求

- Python 3.10+
- 依赖：fastapi, uvicorn, pyyaml, httpx 等（按项目实际需求安装）

## License

MIT
