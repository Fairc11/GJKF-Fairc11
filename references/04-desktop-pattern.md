# 04 — 桌面端模式（pywebview）

> FastAPI + pywebview 实现桌面应用

## 架构

```
Python 进程
├── 线程 1: Uvicorn（FastAPI HTTP 服务）
├── 线程 2: pywebview GUI 窗口（Edge WebView2）
└── JsApi 桥接（JS ↔ Python 双向通信）
```

## 基础实现

### desktop_app.py

```python
"""桌面客户端 — pywebview 包装 FastAPI"""
from __future__ import annotations
import os
import sys
import threading
import webview
from pathlib import Path


class JsApi:
    """JS ↔ Python 桥接类
    JS 端通过 window.pywebview.api.method_name() 调用
    """
    
    def open_folder(self, path: str) -> None:
        """打开文件夹（系统文件管理器）"""
        os.startfile(path)
    
    def show_notification(self, title: str, message: str) -> None:
        """显示系统通知"""
        webview.evaluate_js(f"new Notification('{title}', {{body: '{message}'}})")
    
    def get_app_path(self) -> str:
        """获取应用数据路径（打包后也能用）"""
        if getattr(sys, 'frozen', False):
            return os.path.dirname(sys.executable)
        return str(Path(__file__).parent)


def run_server(host: str, port: int):
    """启动 FastAPI 服务（线程）"""
    import uvicorn
    uvicorn.run("app.main:app", host=host, port=port, log_level="info")


def create_window(title: str, url: str, js_api: JsApi, icon_path: str = ""):
    """创建 pywebview 窗口"""
    window = webview.create_window(
        title=title,
        url=url,
        js_api=js_api,
        width=1200,
        height=800,
        resizable=True,
        fullscreen=False,
        icon=icon_path,
    )
    return window


def main():
    from app.config import settings
    
    # 启动 FastAPI（后台线程）
    server_thread = threading.Thread(
        target=run_server,
        args=(settings.host, settings.port),
        daemon=True,
    )
    server_thread.start()
    
    # 创建窗口
    js_api = JsApi()
    window = create_window(
        title="Project Name",
        url=f"http://127.0.0.1:{settings.port}",
        js_api=js_api,
        icon_path="icon.ico",
    )
    
    webview.start(debug=settings.debug)
```

### 在 JS 端调用

```javascript
// JS → Python 调用
async function openDownloadFolder(path) {
    await window.pywebview.api.open_folder(path);
}

// Python → JS 调用（通过 evaluate_js）
// 在 Python 端：
// webview.evaluate_js("showProgress(50)")
```

## 高级特性

### 系统托盘

```python
import webview

def minimize_to_tray(window):
    """最小化到系统托盘"""
    window.hide()
    webview.tray_set_icon("icon.ico")
    webview.tray_set_tooltip("Project Name 运行中")

# 在 webview.start() 后设置
# 但 pywebview 的托盘 API 各版本不同，需要查当前版本的文档
```

### 单实例锁

```python
import win32event
import win32api
import win32error

MUTEX_NAME = "Global\\ProjectName_SingleInstance"

def is_already_running() -> bool:
    """检测是否已有实例运行"""
    try:
        handle = win32event.CreateMutex(None, False, MUTEX_NAME)
        return win32api.GetLastError() == win32error.ERROR_ALREADY_EXISTS
    except:
        return False
```

### 窗口位置记忆

```python
import json
from pathlib import Path

class WindowState:
    """记住窗口位置和大小"""
    
    def __init__(self, state_file: str = "window_state.json"):
        self.state_file = Path(state_file)
        self.data = self._load()
    
    def _load(self) -> dict:
        if self.state_file.exists():
            return json.loads(self.state_file.read_text(encoding='utf-8'))
        return {"x": None, "y": None, "width": 1200, "height": 800}
    
    def save(self, x: int, y: int, width: int, height: int):
        self.data.update({"x": x, "y": y, "width": width, "height": height})
        self.state_file.write_text(json.dumps(self.data), encoding='utf-8')
    
    def get_geometry(self) -> dict:
        return self.data
```

## 常见问题

### 1. 打包后 `js_api` 模块找不到
- 原因：`build.spec` 的 `hiddenimports` 没有包含 `app.js_api`
- 解决：添加 `"app.js_api"` 到 `hiddenimports`

### 2. pywebview 窗口不显示
- 检查 WebView2 是否可用（Windows 10/11 应有）
- 检查端口是否被占用
- 先打印 URL，手动在浏览器打开验证服务是否正常

### 3. JS 调用 Python 没反应
- JS 端方法名：`window.pywebview.api.method_name()`
- Python 端方法名必须和 JS 调用一致
- 方法必须是异步的或同步的？取决于 pywebview 版本

### 4. 窗口标题乱码
- 确保 Python 文件编码是 UTF-8
- 在文件头加 `# -*- coding: utf-8 -*-`
