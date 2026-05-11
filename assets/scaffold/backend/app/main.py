"""FastAPI 应用入口"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from .config import settings

app = FastAPI(title="项目名称", version="1.0.0")

# 挂载静态文件
STATIC_DIR = settings.BASE_DIR / "backend" / "app" / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

# 全局异常处理器
from fastapi import Request
from fastapi.responses import JSONResponse


class ToolError(Exception):
    def __init__(self, cn_message: str, en_debug: str = ""):
        self.cn_message = cn_message
        self.en_debug = en_debug


@app.exception_handler(ToolError)
async def tool_error_handler(request: Request, exc: ToolError):
    return JSONResponse(
        status_code=400,
        content={"error": True, "message": exc.cn_message, "detail": exc.en_debug},
    )


@app.exception_handler(Exception)
async def general_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": True, "message": "服务器内部错误", "detail": str(exc)},
    )


@app.get("/")
async def index():
    index_path = settings.TEMPLATES_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return {"message": "Hello from GJKF-Fairc!"}


@app.get("/api/health")
async def health():
    return {"status": "ok"}
