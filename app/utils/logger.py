"""
日志模块配置
"""
import os
import sys
import uuid
import contextvars
from pathlib import Path
from typing import Dict, Any, Optional

import yaml
from loguru import logger as _logger


# 创建一个上下文变量来存储trace_id
trace_id_var = contextvars.ContextVar("trace_id", default=None)


def generate_trace_id() -> str:
    """
    生成链路追踪ID
    
    Returns:
        str: 8位追踪ID
    """
    return uuid.uuid4().hex


def get_trace_id() -> Optional[str]:
    """
    获取当前上下文的trace_id
    
    Returns:
        Optional[str]: 追踪ID，如果不存在则返回None
    """
    return trace_id_var.get()


def set_trace_id(trace_id: Optional[str] = None) -> str:
    """
    设置trace_id到当前上下文
    
    Args:
        trace_id: 要设置的追踪ID，如果为None则自动生成
        
    Returns:
        str: 设置的追踪ID
    """
    if trace_id is None:
        trace_id = generate_trace_id()
    trace_id_var.set(trace_id)
    return trace_id


class TracedLogger:
    """带有追踪功能的日志记录器"""
    
    def __init__(self, logger):
        self._logger = logger
        
    def _log(self, level: str, message: str, *args, **kwargs):
        """
        记录日志，自动添加trace_id，并调整depth使caller信息正确显示
        """
        # 确保存在trace_id
        if get_trace_id() is None:
            set_trace_id()
        # 使用opt调整深度，跳过包装调用
        opt_logger = self._logger.opt(depth=2)
        return getattr(opt_logger, level)(message, *args, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        return self._log("debug", message, *args, **kwargs)
        
    def info(self, message: str, *args, **kwargs):
        return self._log("info", message, *args, **kwargs)
        
    def warning(self, message: str, *args, **kwargs):
        return self._log("warning", message, *args, **kwargs)
        
    def error(self, message: str, *args, **kwargs):
        return self._log("error", message, *args, **kwargs)
        
    def critical(self, message: str, *args, **kwargs):
        return self._log("critical", message, *args, **kwargs)
        
    def exception(self, message: str, *args, **kwargs):
        return self._log("exception", message, *args, **kwargs)
    
    def bind(self, **kwargs):
        """支持loguru的bind方法"""
        return TracedLogger(self._logger.bind(**kwargs))


class TraceIDFilter:
    """为日志添加trace_id的过滤器"""
    
    def __call__(self, record: Dict[str, Any]) -> bool:
        """处理日志记录，添加trace_id"""
        trace_id = get_trace_id()
        if trace_id is None:
            trace_id = set_trace_id()
        record["extra"]["trace_id"] = trace_id or "no_trace"  # 确保始终有值
        return True


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
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "{extra[trace_id]} | "
            "<level>{message}</level>"
        ),
        filter=TraceIDFilter(),
        # 异步写入会导致控制台输出乱序，在开发阶段还是不建议使用
        # enqueue=True  # 启用异步写入
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
                "{name}:{function}:{line} | "
                "{extra[trace_id]} | "
                "{message}"
            ),
            rotation=file_config.get("rotation", "1 MB"),
            retention=file_config.get("retention", "7 days"),
            compression=file_config.get("compression", "zip"),
            encoding=file_config.get("encoding", "utf-8"),
            enqueue=True,  # 启用异步写入
            backtrace=file_config.get("backtrace", True),
            diagnose=file_config.get("diagnose", True),
            filter=TraceIDFilter()
        )


# 初始化日志配置
setup_logger()

# 创建全局logger实例
logger = TracedLogger(_logger)

