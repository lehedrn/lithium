"""
日志使用示例
演示各种日志记录的使用方法
"""
import time
import json
from app.utils.logger import logger


def demo_basic_logging():
    """演示基本的日志级别使用"""
    logger.debug("这是一条调试日志，通常用于记录详细的调试信息")
    logger.info("这是一条信息日志，通常用于记录正常的业务流程")
    logger.warning("这是一条警告日志，通常用于记录需要注意但不影响系统运行的问题")
    logger.error("这是一条错误日志，通常用于记录系统错误但不影响系统继续运行")
    logger.critical("这是一条严重错误日志，通常用于记录导致系统无法继续运行的错误")


def demo_structured_logging():
    """演示结构化日志记录"""
    # 记录用户登录
    user_info = {
        "user_id": "12345",
        "ip": "192.168.1.1",
        "login_time": "2024-02-21 14:30:00",
        "device": "Chrome/Windows"
    }
    logger.info("用户登录系统 | {}", json.dumps(user_info, ensure_ascii=False))
    
    # 记录业务操作
    order_info = {
        "order_id": "ORD20240221001",
        "user_id": "12345",
        "amount": 199.99,
        "products": ["商品1", "商品2"]
    }
    logger.info("订单创建成功 | {}", json.dumps(order_info, ensure_ascii=False))
    
    # 记录系统指标
    system_metrics = {
        "cpu_usage": "45%",
        "memory_usage": "60%",
        "disk_usage": "75%",
        "network_traffic": "2.5MB/s"
    }
    logger.info("系统性能指标 | {}", json.dumps(system_metrics, ensure_ascii=False))


def demo_exception_logging():
    """演示异常日志记录"""
    try:
        # 模拟一个除零错误
        1/0
    except Exception as e:
        # 使用exception()方法会自动记录异常堆栈
        logger.exception("发生除零错误")
        
    try:
        # 模拟一个字典键错误
        data = {"a": 1}
        value = data["b"]
    except KeyError as e:
        # 使用error()方法手动记录异常信息
        error_info = {
            "error_type": type(e).__name__,
            "error_msg": str(e),
            "data": data
        }
        logger.error("访问字典时发生键错误 | {}", json.dumps(error_info, ensure_ascii=False))
        
    try:
        # 模拟一个文件操作错误
        with open("not_exist.txt", "r") as f:
            content = f.read()
    except FileNotFoundError as e:
        # 记录带有上下文信息的异常
        error_context = {
            "error": str(e),
            "file": "not_exist.txt",
            "operation": "read"
        }
        logger.error("文件操作失败 | {}", json.dumps(error_context, ensure_ascii=False))


def demo_file_rotation():
    """演示日志文件切割"""
    logger.info("开始测试日志文件切割功能")
    
    # 生成大量日志来触发文件切割
    for i in range(10000):
        log_data = {
            "index": i,
            "timestamp": time.time(),
            "data": "*" * 100  # 生成较大的日志内容
        }
        logger.debug("日志文件切割测试 | {}", json.dumps(log_data))
    
    logger.info("日志文件切割测试完成")


def demo_async_logging():
    """演示异步日志记录"""
    logger.info("开始测试异步日志写入")
    
    # 模拟一个耗时操作中的日志记录
    for i in range(100):
        # 由于启用了异步写入，这些日志记录不会阻塞主程序
        task_info = {
            "task_id": f"TASK_{i}",
            "progress": f"{i}%",
            "status": "processing",
            "timestamp": time.time()
        }
        logger.debug("异步处理任务进度 | {}", json.dumps(task_info))
        time.sleep(0.01)  # 模拟处理时间
    
    logger.info("异步日志测试完成")
    # 等待一会确保异步日志写入完成
    time.sleep(1)


if __name__ == "__main__":
    # 运行所有示例
    logger.info("=== 开始运行日志示例程序 ===")
    
    logger.info("--- 1. 基本日志级别演示 ---")
    demo_basic_logging()
    
    logger.info("--- 2. 结构化日志演示 ---")
    demo_structured_logging()
    
    logger.info("--- 3. 异常日志演示 ---")
    demo_exception_logging()
    
    # logger.info("--- 4. 日志文件切割演示 ---")
    # demo_file_rotation()
    
    logger.info("--- 5. 异步日志演示 ---")
    demo_async_logging()
    
    logger.info("=== 日志示例程序运行完成 ===") 