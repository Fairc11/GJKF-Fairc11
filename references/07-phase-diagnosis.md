# 07 — 半路接入 & 阶段诊断

> 项目开发到一半想规范化？先诊断再继续

## 诊断流程

```
用户说"做到一半了" / "项目有点乱" / "帮我看看现在到哪了"

→ 步骤 1: 扫描目录结构
→ 步骤 2: 检查各阶段产出物
→ 步骤 3: 综合判定当前阶段
→ 步骤 4: 输出诊断报告 + 推荐操作
→ 步骤 5: 标准化对齐（不破坏已有代码）
```

## 扫描清单

### 目录结构扫描

```python
def scan_project(project_path: str) -> dict:
    """扫描项目结构，返回各阶段完成情况"""
    from pathlib import Path
    p = Path(project_path)
    
    result = {
        "has_entry": (p / "run.py").exists() or (p / "main.py").exists(),
        "has_config": (p / "config.yaml").exists() or (p / ".env").exists(),
        "has_requirements": (p / "requirements.txt").exists(),
        "has_backend": (p / "backend" / "app").exists(),
        "has_models": (p / "backend" / "app" / "models").exists(),
        "has_services": (p / "backend" / "app" / "services").exists(),
        "has_routers": (p / "backend" / "app" / "api").exists(),
        "has_templates": (p / "backend" / "app" / "templates").exists(),
        "has_static": (p / "backend" / "app" / "static").exists(),
        "has_desktop": (p / "desktop_app.py").exists(),
        "has_build_spec": (p / "build.spec").exists(),
        "has_setup_check": (p / "setup_check.py").exists(),
        "has_launcher": any(p.glob("*.bat")),
        "has_releases": (p / "releases").exists(),
    }
    return result
```

### 阶段判定表

| 阶段 | 必要条件 | 加分项 |
|------|---------|--------|
| 阶段 -1（需求） | 无代码或有需求文档 | 无 |
| 阶段 0（脚手架） | `has_entry` + `has_config` + `has_requirements` | `has_launcher` |
| 阶段 1（后端） | `has_backend` + `has_models` + `has_services` | `has_routers` |
| 阶段 2（前端） | `has_templates` + `has_static` | 前端可交互 |
| 阶段 3（桌面端） | `has_desktop` | pywebview 可用 |
| 阶段 4（打包） | `has_build_spec` + `has_setup_check` | 有 releases/ |

### 诊断输出模板

```
┌────────────────────────────────────────────────┐
│              项目阶段诊断报告                    │
├────────────────────────────────────────────────┤
│ 项目名称: xxx                                   │
│ 当前阶段: 阶段 1（后端核心）                     │
│ 完成度:   45%                                   │
├────────────────────────────────────────────────┤
│ ✅ 已完成:                                      │
│   • 入口文件 run.py                             │
│   • 配置文件 config.yaml + .env                 │
│   • 依赖文件 requirements.txt                   │
│   • 启动.bat 快捷入口                           │
│   • 后端基础结构（main.py + config.py）          │
│   • 数据模型 schemas.py                         │
│                                                  │
│ ❌ 缺失/待完成:                                 │
│   • 业务服务层 services/ — 未实现                │
│   • API 路由 api/routers/ — 未实现               │
│   • WebSocket 进度推送 — 未实现                  │
│   • 中文异常处理器 — 未实现                      │
│   • 前端 templates/ + static/ — 未开始           │
├────────────────────────────────────────────────┤
│ 📋 推荐操作:                                    │
│   方案 A（推荐）: 补全 services/ + routers/，    │
│   完成阶段 1                                     │
│                                                  │
│   方案 B: 跳到阶段 2（不推荐，后端未完成会导致    │
│   前端无数据展示）                                │
└────────────────────────────────────────────────┘
```

## 标准化对齐

把已有项目结构对齐到标准结构，不破坏已有代码：

### 对齐原则

1. **不动已有代码** — 不修改、不移动已有文件
2. **只补充缺失** — 添加缺失的目录和文件
3. **新增文件遵循标准结构** — 新代码按标准组织

### 对齐操作

```python
def align_to_standard(project_path: str):
    """将项目结构对齐到标准模板"""
    from pathlib import Path
    p = Path(project_path)
    
    # 创建缺失的标准目录（不会覆盖已有）
    dirs_to_create = [
        "backend/app/models",
        "backend/app/services", 
        "backend/app/api",
        "backend/app/templates",
        "backend/app/static/css",
        "backend/app/static/js",
        "data/downloads",
        "data/output",
        "logs",
    ]
    
    for dir_path in dirs_to_create:
        (p / dir_path).mkdir(parents=True, exist_ok=True)
    
    # 创建缺失的 __init__.py
    init_dirs = [
        "backend",
        "backend/app",
        "backend/app/models",
        "backend/app/services",
        "backend/app/api",
    ]
    
    for dir_path in init_dirs:
        init_file = p / dir_path / "__init__.py"
        if not init_file.exists():
            init_file.write_text("", encoding='utf-8')
```

### 对齐后检查

- [ ] 所有标准目录存在
- [ ] 所有 Python 包有 `__init__.py`
- [ ] 配置文件存在（config.yaml / .env）
- [ ] 快捷启动脚本存在（启动.bat）
- [ ] 已有代码未被修改
- [ ] 项目能正常启动
