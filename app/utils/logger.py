"""
日志模块配置
"""
import os
import sys
import time
from pathlib import Path
from typing import Dict, Any

import yaml
from loguru import logger as _logger


def load_log_config() -> Dict[str, Any]:
    """
    加载日志配置
    
    Returns:
        Dict[str, Any]: 日志配置字典
    """
    # 获取环境配置
    env = os.getenv("ENV", "dev")
    
    # 构建配置文件路径
    config_dir = Path("configs")
    config_file = config_dir / f"config_{env}.yml"
    
    # 如果配置文件不存在，使用示例配置
    if not config_file.exists():
        config_file = config_dir / "config.yml.example"
    
    # 读取配置文件
    if not config_file.exists():
        raise FileNotFoundError(f"配置文件不存在: {config_file}")
        
    with open(config_file, 'r', encoding='utf-8') as f:
        try:
            config = yaml.safe_load(f)
            return config.get("log", {})
        except yaml.YAMLError as e:
            raise yaml.YAMLError(f"配置文件格式错误: {e}")
        except Exception as e:
            raise Exception(f"加载配置文件失败: {e}")


def setup_logger() -> None:
    """
    配置日志记录器
    """
    # 加载配置
    config = load_log_config()
    
    # 创建日志目录
    log_dir = Path(config.get("dir", "logs"))
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # 移除默认的处理器
    _logger.remove()
    
    # 配置控制台输出
    console_config = config.get("console", {})
    _logger.add(
        sys.stdout,
        level=console_config.get("level", "INFO"),
        colorize=console_config.get("colorize", True),
        format=console_config.get("format", 
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )
    )
    
    # 配置文件输出
    file_config = config.get("file", {})
    if file_config:
        log_file = log_dir / file_config.get("filename", "lithium.log")
        _logger.add(
            str(log_file),
            level=file_config.get("level", "DEBUG"),
            format=file_config.get("format",
                "{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | "
                "{name}:{function}:{line} - {message}"
            ),
            rotation=file_config.get("rotation", "1 MB"),
            retention=file_config.get("retention", "7 days"),
            compression=file_config.get("compression", "zip"),
            encoding=file_config.get("encoding", "utf-8"),
            enqueue=file_config.get("enqueue", True),
            backtrace=file_config.get("backtrace", True),
            diagnose=file_config.get("diagnose", True)
        )


# 初始化日志配置
setup_logger()

# 创建全局logger实例
logger = _logger

