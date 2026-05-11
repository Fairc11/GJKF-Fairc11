@echo off
chcp 65001 >nul
title 项目名称

echo ==============================================
echo  项目名称 - 开发模式
echo ==============================================

python run.py
if errorlevel 1 (
    echo.
    echo 启动失败！请确认：
    echo 1. Python 已安装
    echo 2. 依赖已安装：pip install -r requirements.txt
    echo.
    pause
) else (
    pause
)
