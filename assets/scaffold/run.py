#!/usr/bin/env python3
"""项目启动入口

Usage:
  python run.py              Web 模式
  python run.py -d           桌面端模式
"""
import os
import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "backend"))


def main():
    parser = argparse.ArgumentParser(description="项目名称")
    parser.add_argument("-d", "--desktop", action="store_true", help="启动桌面客户端")
    parser.add_argument("--port", type=int, default=None, help="指定端口")
    args = parser.parse_args()

    if args.desktop:
        _run_desktop(args.port)
    else:
        _run_web(args.port)


def _run_web(port=None):
    """启动 Web 服务"""
    import uvicorn
    from app.config import settings

    host = settings.get("host", "127.0.0.1")
    p = port or settings.get("port", 8000)
    debug = settings.get("debug", True)

    print(f"启动服务器 (端口 {p})...")
    print(f"打开浏览器访问: http://{host}:{p}")
    uvicorn.run("app.main:app", host=host, port=p, reload=debug)


def _run_desktop(port=None):
    """启动桌面客户端"""
    import threading
    import uvicorn
    import webview
    from app.config import settings
    from app.js_api import JsApi

    host = settings.get("host", "127.0.0.1")
    p = port or settings.get("port", 18080)
    debug = settings.get("debug", True)

    # 后台启动 FastAPI
    def start_server():
        uvicorn.run("app.main:app", host=host, port=p, log_level="info")

    t = threading.Thread(target=start_server, daemon=True)
    t.start()

    # 创建桌面窗口
    webview.create_window(
        title="项目名称",
        url=f"http://{host}:{p}",
        js_api=JsApi(),
        width=1200,
        height=800,
        resizable=True,
        icon="icon.ico",
    )
    webview.start(debug=debug)


if __name__ == "__main__":
    main()
