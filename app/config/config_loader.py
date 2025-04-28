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

from app.utils.logger import logger


class ConfigLoader:
    """配置文件加载器，支持热重载"""
    def __init__(self,
                 config_dir: Union[str, Path] = "configs",
                 default_env: str = "dev",
                 watch_interval: float = 1.0):
        self.config_dir = Path(config_dir)
        self.env = os.getenv("ENV", default_env)
        self.file = self._find_config_file()
        self._data = {}
        self._mtime = 0
        self._stop_event = Event()
        self.watch_interval = watch_interval
        # 初始加载配置
        self._load()
        # 启动文件监视器
        self._start_watcher()

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
            self._mtime = self.file.stat().st_mtime
            logger.info("配置文件加载成功")
            logger.info(f"加载到的配置信息: {self._data}")
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")

    def _start_watcher(self):
        """启动监视线程"""
        t = Thread(target=self._watcher, daemon=True)
        t.start()

    def _watcher(self):
        """监视配置文件变化并重载"""
        logger.info(f"启动配置文件监视器, 监控间隔: {self.watch_interval}s")
        while not self._stop_event.is_set():
            try:
                current_mtime = self.file.stat().st_mtime
                if current_mtime != self._mtime:
                    logger.info("检测到配置文件变化, 重新加载...")
                    self._load()
                time.sleep(self.watch_interval)
            except Exception as e:
                logger.error(f"监视配置文件失败: {e}")
                time.sleep(self.watch_interval)

    def get(self, key: str, default=None):
        """获取配置项"""
        return self._data.get(key, default)

    def stop(self):
        """停止监视器"""
        self._stop_event.set()


# 全局配置实例
config = ConfigLoader() 