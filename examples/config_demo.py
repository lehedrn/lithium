"""
配置加载器使用示例
演示如何使用全局 config 获取配置项并观察自动重新加载
"""
import time
from app.config.config_loader import config


def demo_config_usage():
    """演示配置加载器的基本使用"""
    print("应用名称:", config.get("app", {}).get("name"))
    print("API 前缀:", config.get("api", {}).get("prefix"))

    # 获取日志配置
    log_cfg = config.get("log", {})
    print("日志目录:", log_cfg.get("dir"))
    print("控制台日志级别:", log_cfg.get("console", {}).get("level"))

    # 观察配置项自动重载
    print("修改配置文件 config_dev.yml 中的 debug 字段 (true/false) 以测试自动重载")
    for i in range(5):
        debug_val = config.get("app", {}).get("debug")
        print(f"[{i}] 当前 app.debug = {debug_val}")
        time.sleep(2)


if __name__ == "__main__":
    demo_config_usage() 