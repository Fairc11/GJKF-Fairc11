# 02 — 项目结构模板

## 标准目录结构

### FastAPI + Jinja2（默认路线）

```
project-name/
├── run.py                       # 启动入口
├── desktop_app.py               # pywebview 桌面端（可选）
├── setup_check.py               # 环境自检
├── build_exe.bat                # 打包脚本
├── build.spec                   # PyInstaller 配置（可选）
├── installer.iss                # Inno Setup 配置（可选）
├── 启动.bat                     # 双击启动 dev 模式
├── 安装必要组件.bat             # 依赖安装
├── config.yaml                  # 可修改配置
├── cookies.yaml                 # Cookie 存储（爬虫工具用）
├── icon.ico                     # 应用图标
├── requirements.txt             # 依赖
├── CLAUDE.md                    # 项目说明
├── PTU_TECHNICAL_DOCUMENTATION.md  # 技术文档（定型时）
│
├── backend/
│   ├── .env                     # 环境变量/密钥
│   ├── requirements.txt         # 后端依赖（可选拆分）
│   └── app/
│       ├── __init__.py
│       ├── main.py              # FastAPI 应用组装
│       ├── config.py            # 配置读取 + 路径自动检测
│       ├── models/
│       │   ├── __init__.py
│       │   ├── schemas.py       # Pydantic 数据模型
│       │   └── task_store.py    # 数据持久化
│       ├── services/
│       │   ├── __init__.py
│       │   ├── scraper.py       # 抓取服务（爬虫工具）
│       │   ├── downloader.py    # 下载服务
│       │   ├── media_processor.py  # 媒体处理
│       │   ├── progress.py      # WebSocket 进度
│       │   └── qr_login.py      # 扫码登录
│       ├── api/
│       │   ├── __init__.py
│       │   ├── router_scraper.py
│       │   ├── router_download.py
│       │   ├── router_media.py
│       │   ├── router_ws.py
│       │   └── router_login.py
│       ├── templates/
│       │   ├── base.html
│       │   └── index.html
│       └── static/
│           ├── css/
│           │   └── app.css
│           └── js/
│               └── app.js
│
├── data/
│   ├── downloads/               # 下载文件
│   └── output/                  # 输出文件
│
├── logs/                        # 日志
│
└── releases/                    # 发布版本
    ├── 1.0.0/
    └── 1.1.0/
```

### CLI 工具路线（无 UI）

```
project-name/
├── main.py                      # 入口
├── config.yaml
├── requirements.txt
├── services/
│   ├── scraper.py
│   └── processor.py
└── data/
    └── output/
```

---

## 关键文件模板

### `run.py` — 启动入口

```python
#!/usr/bin/env python3
"""Project Name - 启动入口

Usage:
  python run.py              Web 模式
  python run.py -d           桌面端模式
"""
import os
import sys
import argparse
from pathlib import Path

# 确保 backend 在 sys.path 中
sys.path.insert(0, str(Path(__file__).parent / "backend"))


def main():
    parser = argparse.ArgumentParser(description="Project Name")
    parser.add_argument("-d", "--desktop", action="store_true", help="启动桌面客户端")
    args = parser.parse_args()

    if args.desktop:
        _run_desktop()
    else:
        _run_web()


def _run_web():
    """启动 Web 服务"""
    import uvicorn
    from app.config import settings
    
    print(f"启动服务器 (端口 {settings.port})...")
    uvicorn.run("app.main:app", host=settings.host, port=settings.port, reload=True)


def _run_desktop():
    """启动桌面客户端"""
    import uvicorn
    import webview
    import threading
    from app.config import settings
    from app.js_api import JsApi
    
    # 启动 FastAPI 服务
    server = uvicorn.Server(...)
    # 启动 pywebview 窗口
    webview.create_window("Project Name", f"http://127.0.0.1:{settings.port}", js_api=JsApi())
    webview.start()


if __name__ == "__main__":
    main()
```

---

### `config.py` — 配置管理

```python
"""配置管理 — 支持 dev 和打包两种环境的路径自动检测"""
from __future__ import annotations
import os
import sys
from pathlib import Path


class Settings:
    def __init__(self):
        # 基础路径：自适应 dev / 打包环境
        if getattr(sys, 'frozen', False):
            self.BASE_DIR = Path(sys._MEIPASS)
        else:
            self.BASE_DIR = Path(__file__).resolve().parent.parent.parent
        
        # 数据目录
        self.DATA_DIR = self.BASE_DIR / "data"
        self.DOWNLOAD_DIR = self.DATA_DIR / "downloads"
        self.OUTPUT_DIR = self.DATA_DIR / "output"
        
        # 从 yaml 或 .env 读取配置
        self.host = os.getenv("HOST", "127.0.0.1")
        self.port = int(os.getenv("PORT", "8000"))
        self.debug = os.getenv("DEBUG", "true").lower() == "true"

settings = Settings()
```

---

### `启动.bat` — 快捷入口

```bat
@echo off
chcp 65001 >nul
echo 正在启动...
python run.py
if errorlevel 1 (
    echo 启动失败，请检查 Python 是否安装
    pause
)
```

### `安装必要组件.bat`

```bat
@echo off
chcp 65001 >nul
echo 正在安装依赖...
pip install -r requirements.txt
echo 检查 Playwright Chromium...
python -m playwright install
echo 安装完成！
pause
```
