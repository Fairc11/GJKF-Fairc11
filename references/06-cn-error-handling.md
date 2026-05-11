# 06 — 中文错误处理规范

> 所有用户可见的错误信息必须用中文

## 统一异常类

```python
class ToolError(Exception):
    """统一异常类
    
    用户看到的 → cn_message（中文）
    调试用的 → en_debug（英文/技术细节）
    """
    def __init__(self, cn_message: str, en_debug: str = ""):
        self.cn_message = cn_message
        self.en_debug = en_debug
        super().__init__(cn_message)


# 预定义错误类型
class CookieExpiredError(ToolError):
    def __init__(self, detail: str = ""):
        super().__init__(
            cn_message="登录已过期，请重新登录",
            en_debug=detail,
        )

class NetworkError(ToolError):
    def __init__(self, detail: str = ""):
        super().__init__(
            cn_message="网络请求失败，请检查网络连接",
            en_debug=detail,
        )

class ParseError(ToolError):
    def __init__(self, detail: str = ""):
        super().__init__(
            cn_message="数据解析失败，平台页面结构可能已更新",
            en_debug=detail,
        )

class ConfigError(ToolError):
    def __init__(self, detail: str = ""):
        super().__init__(
            cn_message="配置错误，请检查配置文件",
            en_debug=detail,
        )

class DependencyError(ToolError):
    def __init__(self, detail: str = ""):
        super().__init__(
            cn_message="缺少必要组件，正在自动安装...",
            en_debug=detail,
        )
```

## API 错误响应格式

```python
# FastAPI 全局异常处理器
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ToolError)
async def tool_error_handler(request: Request, exc: ToolError):
    return JSONResponse(
        status_code=400,
        content={
            "error": True,
            "message": exc.cn_message,     # 用户看到的中文消息
            "detail": exc.en_debug,         # 调试信息
        }
    )

@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "服务器内部错误，请查看日志",
            "detail": str(exc),
        }
    )
```

## 前端错误展示

```javascript
// 统一的错误展示函数
function showError(message, detail = '') {
    const errorEl = document.getElementById('error-message');
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
        // 5秒后自动隐藏
        setTimeout(() => { errorEl.style.display = 'none'; }, 5000);
    }
}

// 所有 API 调用统一错误处理
async function apiCall(url, options = {}) {
    try {
        const resp = await fetch(url, options);
        if (!resp.ok) {
            const data = await resp.json();
            showError(data.message || '请求失败');
            return null;
        }
        return await resp.json();
    } catch (err) {
        showError('网络连接失败，请检查服务是否在运行');
        return null;
    }
}
```

## 日志中的错误格式

```python
import logging

logger = logging.getLogger(__name__)

def safe_log_error(logger, cn_message: str, exc_info: Exception = None):
    """安全记录错误（处理 gbk 编码问题）"""
    try:
        logger.error(f"[用户提示] {cn_message}", exc_info=exc_info)
    except UnicodeEncodeError:
        # gbk 兼容
        logger.error(f"[Error] {cn_message.encode('ascii', errors='replace')}")
```

## 控制台输出处理

```python
# 启动时处理编码问题
import sys
import io

if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
```
