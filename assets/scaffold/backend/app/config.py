"""配置管理 — 支持 dev 和打包两种环境"""
from __future__ import annotations
import os
import sys
import yaml
from pathlib import Path
from functools import lru_cache


class Settings:
    """配置类：自动适应 dev / 打包两种环境"""

    def __init__(self):
        # 基础路径
        if getattr(sys, 'frozen', False):
            self.BASE_DIR = Path(sys._MEIPASS)
        else:
            self.BASE_DIR = Path(__file__).resolve().parent.parent.parent

        # 数据目录
        self.DATA_DIR = self.BASE_DIR / "data"
        self.DOWNLOAD_DIR = self.DATA_DIR / "downloads"
        self.OUTPUT_DIR = self.DATA_DIR / "output"
        self.LOG_DIR = self.BASE_DIR / "logs"

        # 模板和静态文件
        self.TEMPLATES_DIR = self.BASE_DIR / "backend" / "app" / "templates"
        self.STATIC_DIR = self.BASE_DIR / "backend" / "app" / "static"

        # 从 .env 读取
        self.host = os.getenv("HOST", "127.0.0.1")
        self.port = int(os.getenv("PORT", "8000"))
        self.debug = os.getenv("DEBUG", "true").lower() == "true"

        # 从 config.yaml 读取
        self._load_config()

    def _load_config(self):
        config_path = self.BASE_DIR / "config.yaml"
        if config_path.exists():
            with open(config_path, encoding='utf-8') as f:
                cfg = yaml.safe_load(f) or {}
            self.host = cfg.get("host", self.host)
            self.port = cfg.get("port", self.port)
            self.debug = cfg.get("debug", self.debug)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def ensure_dirs(self):
        """确保数据目录存在"""
        for d in [self.DATA_DIR, self.DOWNLOAD_DIR, self.OUTPUT_DIR, self.LOG_DIR]:
            d.mkdir(parents=True, exist_ok=True)


settings = Settings()
