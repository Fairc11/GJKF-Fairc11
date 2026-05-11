@echo off
chcp 65001 >nl
title 安装必要组件

echo 正在安装 Python 依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 安装失败，请检查网络连接和 Python 环境
    pause
    exit /b 1
)

echo 检查 Playwright Chromium...
python -m playwright install 2>nul
if errorlevel 1 (
    echo Chromium 自动安装失败，可手动执行：python -m playwright install chromium
)

echo.
echo 安装完成！
pause
