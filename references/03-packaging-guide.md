# 03 — 打包指南

> PyInstaller 打包 + Inno Setup 安装包制作

## 一、打包架构

```
应用程序代码（.py）
    ↓ PyInstaller
onedir/EXE（包含 Python 解释器 + 应用依赖 + 必要资源）
    ↓ Inno Setup（可选）
安装包（引导安装 + 创建开始菜单 + 桌面快捷方式）
```

面向普通用户发布时，优先选择可检查、可打安装包的 onedir 结构，再用 Inno Setup 输出单个安装包 EXE。不要只为了“看起来一个文件”切到 PyInstaller onefile，除非已经验证启动速度、依赖路径和日志收集都没问题。

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
    (str(PROJECT_ROOT / "icon.ico"), "."),
]

# 绝不要把 .env、cookies.yaml、token、日志、缓存目录放进 datas。
# 需要默认配置时，提供 config.example.yaml 或空模板，由首次启动生成用户配置。

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
        # 只排除已经确认不会被间接导入的依赖。
        # 不确定时先保留，封包版验证通过后再瘦身。
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

### 用户数据目录

打包后不要把日志、缓存、数据库、下载临时文件写入安装目录。安装到 `C:\Program Files\ProjectName` 后，普通用户通常没有写权限。

```python
import os
from pathlib import Path

def get_user_data_dir(app_name: str = "ProjectName") -> Path:
    root = os.environ.get("LOCALAPPDATA")
    if root:
        base = Path(root) / app_name
    else:
        base = Path.home() / f".{app_name.lower()}"
    base.mkdir(parents=True, exist_ok=True)
    return base

USER_DATA_DIR = get_user_data_dir()
LOG_DIR = USER_DATA_DIR / "logs"
CACHE_DIR = USER_DATA_DIR / "cache"
```

## 四、零前置条件打包

普通用户分发版默认目标：安装后无需手动安装 Python、Playwright 浏览器、Chromium、FFmpeg、Node、证书或其他运行时依赖。

### 必须处理

| 依赖 | 推荐策略 | 验收方式 |
|------|----------|----------|
| Python 包 | PyInstaller 收集 | 封包版启动 + hiddenimports 检查 |
| 浏览器/Playwright | 内置浏览器目录，启动时优先查 `_internal` | 清空本机浏览器缓存后扫码/自动化流程可用 |
| FFmpeg | 内置二进制，或首次启动明确检测并提示 | 媒体合成功能在干净环境通过 |
| WebView2 | 安装器检测，缺失时中文提示或引导安装 | 新机器可打开桌面窗口 |
| 证书/模板/静态文件 | 加入 datas | 封包版实际访问页面和 API |

### setup_check 原则

- 自检脚本必须能在开发版和封包版运行。
- 检测路径同时覆盖开发目录、`sys._MEIPASS`、安装目录和用户数据目录。
- 缺失依赖时给中文错误，说明用户能做什么。
- 不要在只缺一个依赖时触发无关的大量安装。
- 不要依赖开发机 PATH；封包版先找内置二进制。

## 五、常见打包问题

| 问题 | 原因 | 解决 |
|------|------|------|
| EXE 启动就闪退 | hiddenimports 遗漏 | 查看闪退前的错误消息，补全模块 |
| 找不到模板/静态文件 | datas 没包含 | 确认所有资源文件在 datas 里 |
| 中文乱码 | 编码问题 | `open(..., encoding='utf-8')`，`chcp 65001` |
| 功能正常但报错不影响运行 | excludes 误删了依赖 | 不要乱 excludes，只排除确定没用的 |
| EXE 太大 | 包含了很多不必要的库 | 适量 excludes，或者用 UPX 压缩 |
| 启动慢 | PyInstaller 解压 | 减少文件数量，合并小文件 |
| 开发机正常，朋友电脑失败 | 依赖来自开发机缓存 | 做清运行时/干净机测试，内置或检测缺失依赖 |
| 安装后 Permission denied | 写入安装目录 | 日志、缓存、数据库改写到 `%LOCALAPPDATA%` |
| GUI 模式无日志 | `sys.stdout is None` 或 console=False | 启动早期写 boot log 到用户日志目录 |

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

## 六、Inno Setup 安装包（可选）

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

## 七、封包版验收

开发版能跑不代表封包版能发。每次发布至少跑：

1. 开发版测试：单元测试、编译检查、release check 或等价脚本。
2. onedir 冒烟：双击 `dist\ProjectName\ProjectName.exe`，验证启动、核心功能、退出。
3. 安装包冒烟：安装到默认目录，验证普通用户权限下能写日志和缓存。
4. 清运行时冒烟：临时移走本机用户数据、浏览器缓存、FFmpeg 缓存等，确认没有依赖开发机残留。
5. 干净机测试：Windows Sandbox、虚拟机或另一台机器。

失败时优先收集用户数据目录里的日志，不要只让用户压缩安装目录。

## 八、GitHub 发布流程

打包完成后发布到 GitHub，让用户能下载安装包。

### 1. 初始化 git
```bash
git init
git checkout -b main
```

### 2. .gitignore 配置

```gitignore
# 敏感信息
cookies.yaml
.env
*.key
*.pem

# 运行时数据
data/
logs/
*.log

# 构建产物
dist/
build/
*.spec
*.exe

# 发布产物（走 GitHub Releases）
releases/

# 本地备份
备份_*/

# Python 缓存
__pycache__/
*.pyc
*.pyo

# IDE
.vscode/
.idea/

# OS
Thumbs.db
desktop.ini
```

> ⚠️ 第一次 add 前确认 `.gitignore` 已配置好，避免把密钥提交上去。

### 3. 提交代码

```bash
git add -A
git commit -m "feat: vX.X.X - 更新说明"
```

**Commit message 规范：**

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feat:` | 新功能 | `feat: v1.3.0 - 新增用户主页抓取` |
| `fix:` | 修 Bug | `fix: 修复登录按钮不响应` |
| `docs:` | 文档 | `docs: 更新使用说明` |
| `chore:` | 杂项 | `chore: 清理敏感文件` |
| `refactor:` | 重构 | `refactor: 重写抓取逻辑` |

### 4. 打标签 + 推送

```bash
git tag vX.X.X          # 版本号前带 v
git push origin main --tags
```

### 5. 创建 Release（网页方式）

打开 `https://github.com/用户名/仓库名/releases/new`：
1. Tag version: `vX.X.X`
2. Release title: `vX.X.X`
3. Description: 写更新说明
4. Attach binaries: 上传 zip 安装包
5. 点 Publish release

### 6. 创建 Release（API 方式）

```bash
set TOKEN=你的_GitHub_Token
set VERSION=vX.X.X
set ZIP_PATH=C:\path\to\安装包_vX.X.X.zip

REM 创建 Release
curl -s -X POST ^
  -H "Authorization: token %TOKEN%" ^
  -H "Accept: application/vnd.github.v3+json" ^
  https://api.github.com/repos/用户名/仓库名/releases ^
  -d "{\"tag_name\":\"%VERSION%\",\"name\":\"%VERSION%\",\"body\":\"更新说明\"}" > release.json

REM 获取 Release ID
for /f "tokens=2 delims=:," %%a in ('type release.json ^| findstr /C:"\"id\":"') do set REL_ID=%%a

REM 上传安装包
curl -s -X POST ^
  -H "Authorization: token %TOKEN%" ^
  -H "Content-Type: application/zip" ^
  "https://uploads.github.com/repos/用户名/仓库名/releases/%REL_ID%/assets?name=项目名_%VERSION%.zip" ^
  --data-binary @"%ZIP_PATH%"
```

> 注意：不要把你的 Token 提交到代码里！

### 7. 一条龙示例

```bash
REM 假设当前版本 v1.3.0
cd 项目目录
git add -A
git commit -m "feat: v1.3.0 - 新增XX功能"
git tag v1.3.0
git push origin main --tags

REM 然后到 GitHub 网页创建 Release
```

## 八、打包验证清单

- [ ] dev 模式下所有功能正常
- [ ] `build.spec` 的 `hiddenimports` 覆盖所有模块
- [ ] `datas` 包含 `templates/`、`static/`、配置文件
- [ ] 打包后 EXE 在其他机器能启动
- [ ] 核心功能在 EXE 中正常
- [ ] 错误信息显示中文
- [ ] 缺失组件能自动下载（如果用了 `setup_check.py`）
