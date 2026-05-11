# 03 — 打包指南

> PyInstaller 打包 + Inno Setup 安装包制作

## 一、打包架构

```
应用程序代码（.py）
    ↓ PyInstaller
单文件 EXE（包含 Python 解释器 + 所有依赖 + 资源文件）
    ↓ Inno Setup（可选）
安装包（引导安装 + 创建开始菜单 + 桌面快捷方式）
```

## 二、PyInstaller 打包

### build.spec 完整模板

```python
# -*- mode: python ; coding: utf-8 -*-
import os
import sys
from pathlib import Path

# 项目路径
PROJECT_ROOT = Path(__file__).parent
BACKEND_DIR = PROJECT_ROOT / "backend"

# 收集所有 datas：模板、静态文件、配置文件
datas = [
    (str(BACKEND_DIR / "app" / "templates"), "backend/app/templates"),
    (str(BACKEND_DIR / "app" / "static"), "backend/app/static"),
    (str(PROJECT_ROOT / "config.yaml"), "."),
    (str(PROJECT_ROOT / "cookies.yaml"), "."),
    (str(PROJECT_ROOT / "icon.ico"), "."),
]

# 必须列出所有动态导入的模块！
hiddenimports = [
    # FastAPI 生态
    "uvicorn",
    "uvicorn.loggers",
    "uvicorn.loops.auto",
    "uvicorn.protocols.http.auto",
    "starlette",
    "pydantic",
    "yaml",
    "websockets",
    "multipart",
    "httpx",
    # pywebview（如果有桌面端）
    "webview",
    "win32api",
    "win32event",
    "win32gui",
    # Playwright（如果有浏览器自动化）
    "playwright",
    # 你自己的模块
    "app.js_api",
    "app.models.schemas",
    "app.models.task_store",
    "app.services.scraper",
    "app.services.downloader",
    "app.services.media_processor",
    "app.services.progress",
    "app.services.qr_login",
    "app.api.router_scraper",
    "app.api.routers.*",
]

a = Analysis(
    ['run.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter", "matplotlib", "PIL", "pandas", "numpy",
        "scipy", "sympy", "notebook", "jupyter",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='ProjectName',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,     # True=显示控制台窗口，False=纯 GUI
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='icon.ico',
)
```

### build_exe.bat

```bat
@echo off
chcp 65001 >nul
echo ==============================================
echo  打包中...
echo ==============================================

REM 清理旧的构建文件
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist

REM 执行打包
pyinstaller build.spec

REM 复制额外文件到 dist 目录
if exist config.yaml copy config.yaml dist\ >nul 2>&1
if exist cookies.yaml copy cookies.yaml dist\ >nul 2>&1

echo ==============================================
echo  打包完成！EXE 在 dist\ 目录
echo ==============================================
pause
```

## 三、路径自适应（核心）

```python
import sys
from pathlib import Path

def get_base_dir() -> Path:
    """自适应：打包后返回 _MEIPASS，dev 返回项目根目录"""
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent

# 所有路径都基于 get_base_dir()
BASE_DIR = get_base_dir()
TEMPLATES_DIR = BASE_DIR / "backend" / "app" / "templates"
STATIC_DIR = BASE_DIR / "backend" / "app" / "static"
DATA_DIR = BASE_DIR / "data"
```

## 四、常见打包问题

| 问题 | 原因 | 解决 |
|------|------|------|
| EXE 启动就闪退 | hiddenimports 遗漏 | 查看闪退前的错误消息，补全模块 |
| 找不到模板/静态文件 | datas 没包含 | 确认所有资源文件在 datas 里 |
| 中文乱码 | 编码问题 | `open(..., encoding='utf-8')`，`chcp 65001` |
| 功能正常但报错不影响运行 | excludes 误删了依赖 | 不要乱 excludes，只排除确定没用的 |
| EXE 太大 | 包含了很多不必要的库 | 适量 excludes，或者用 UPX 压缩 |
| 启动慢 | PyInstaller 解压 | 减少文件数量，合并小文件 |

### 闪退调试技巧

```bash
# 方案 A：用控制台模式运行（build.spec 里 console=True）
# 这样闪退时能看到错误信息

# 方案 B：在命令行跑 EXE，看输出
> ProjectName.exe

# 方案 C：写一个 wrapper，把错误重定向到文件
# wrapper.cmd
@echo off
ProjectName.exe > error.log 2>&1
```

## 五、Inno Setup 安装包（可选）

```iss
; installer.iss
[Setup]
AppName=ProjectName
AppVersion=1.0.0
DefaultDirName={pf}\ProjectName
DefaultGroupName=ProjectName
OutputDir=.\installer
OutputBaseFilename=ProjectName_Setup_v1.0.0
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\ProjectName.exe

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\ProjectName"; Filename: "{app}\ProjectName.exe"
Name: "{commondesktop}\ProjectName"; Filename: "{app}\ProjectName.exe"
```

## 六、打包验证清单

- [ ] dev 模式下所有功能正常
- [ ] `build.spec` 的 `hiddenimports` 覆盖所有模块
- [ ] `datas` 包含 `templates/`、`static/`、配置文件
- [ ] 打包后 EXE 在其他机器能启动
- [ ] 核心功能在 EXE 中正常
- [ ] 错误信息显示中文
- [ ] 缺失组件能自动下载（如果用了 `setup_check.py`）
