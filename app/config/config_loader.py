"""
配置文件加载器
- 只加载 yaml/yml 文件
- 从 configs 目录加载 config_{env}.yml, 默认使用 config_dev.yml
- 监控文件变化并自动重新加载
- 暴露全局 config 变量，可通过 config.get(key, default) 访问
- 使用 logger 输出关键步骤日志
"""
import os
import time
import yaml
from pathlib import Path
from threading import Thread, Event
from typing import Union
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from app.utils.logger import logger


class ConfigChangeHandler(FileSystemEventHandler):
    """文件系统事件处理，监视配置文件变化"""
    def __init__(self, loader: 'ConfigLoader'):
        self.loader = loader

    def on_modified(self, event):
        # 只对指定的配置文件做出响应
        if not event.is_directory and Path(event.src_path) == self.loader.file:
            logger.info("检测到配置文件修改 (watchdog), 重新加载...")
            self.loader._load()

class ConfigLoader:
    """配置文件加载器，支持热重载"""
    def __init__(self,
                 config_dir: Union[str, Path] = "configs",
                 default_env: str = "dev"):
        self.config_dir = Path(config_dir)
        self.env = os.getenv("ENV", default_env)
        self.file = self._find_config_file()
        self._data = {}
        # 初始加载配置
        self._load()
        # 使用 watchdog 监视配置文件
        handler = ConfigChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(handler, str(self.config_dir), recursive=False)
        self.observer.start()

    def _find_config_file(self) -> Path:
        """查找要加载的配置文件，支持 .yml 和 .yaml"""
        # 尝试加载指定环境的配置文件
        for ext in ("yml", "yaml"):
            file_path = self.config_dir / f"config_{self.env}.{ext}"
            if file_path.exists():
                return file_path
        # 未找到环境配置，使用默认 dev
        for ext in ("yml", "yaml"):
            file_path = self.config_dir / f"config_dev.{ext}"
            if file_path.exists():
                return file_path
        raise FileNotFoundError(
            f"配置文件不存在: {'或'.join(str(self.config_dir / f'config_{self.env}.{ext}') for ext in ['yml','yaml'])} 或 dev 环境配置"
        )

    def _load(self):
        """加载配置文件内容"""
        try:
            logger.info(f"加载配置文件: {self.file}")
            with open(self.file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
            self._data = data
            logger.info("配置文件加载成功")
            logger.info(f"加载到的配置信息: {self._data}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")

    def get(self, key: str, default=None):
        """获取配置项"""
        return self._data.get(key, default)

    def stop(self):
        """停止监视器"""
        self.observer.stop()
        self.observer.join()


# 全局配置实例
config = ConfigLoader() 