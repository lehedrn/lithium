"""
日志使用示例
演示各种日志记录的使用方法，包括链路追踪功能
"""
import time
import json
import asyncio
from contextvars import Context, copy_context
from app.utils.logger import logger, set_trace_id, get_trace_id


def demo_basic_logging():
    """演示基本的日志级别使用"""
    # 设置一个追踪ID
    set_trace_id("basic001")
    
    logger.debug("这是一条调试日志，通常用于记录详细的调试信息")
    logger.info("这是一条信息日志，通常用于记录正常的业务流程")
    logger.warning("这是一条警告日志，通常用于记录需要注意但不影响系统运行的问题")
    logger.error("这是一条错误日志，通常用于记录系统错误但不影响系统继续运行")
    logger.critical("这是一条严重错误日志，通常用于记录导致系统无法继续运行的错误")


def demo_trace_id():
    """演示链路追踪ID的使用"""
    # 自动生成trace_id
    logger.info("这条日志会自动生成trace_id")
    current_trace = get_trace_id()
    logger.info(f"当前的trace_id是: {current_trace}")
    
    # 手动设置trace_id
    set_trace_id("manual123")
    logger.info("这条日志使用手动设置的trace_id")
    
    # 在新的上下文中使用新的trace_id
    ctx = copy_context()
    def run_in_new_context():
        set_trace_id("context456")
        logger.info("这条日志在新的上下文中，使用不同的trace_id")
    ctx.run(run_in_new_context)
    
    # 回到原来的上下文
    logger.info("这条日志仍然使用之前手动设置的trace_id")


def demo_structured_logging():
    """演示结构化日志记录"""
    # 设置业务追踪ID
    set_trace_id("biz789")
    
    # 记录用户登录
    user_info = {
        "user_id": "12345",
        "ip": "192.168.1.1",
        "login_time": "2024-02-21 14:30:00",
        "device": "Chrome/Windows"
    }
    logger.info("用户登录系统 | {user_info}", user_info=user_info)
    
    # 记录业务操作
    order_info = {
        "order_id": "ORD20240221001",
        "user_id": "12345",
        "amount": 199.99,
        "products": ["商品1", "商品2"]
    }
    logger.info("订单创建成功 | {order_info}", order_info=order_info)


def demo_exception_logging():
    """演示异常日志记录"""
    # 设置异常追踪ID
    set_trace_id("error001")
    
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


async def demo_async_logging():
    """演示异步环境下的日志记录"""
    logger.info("开始异步日志测试")
    
    async def async_task(task_id: str):
        # 每个任务使用独立的trace_id
        set_trace_id(f"task_{task_id}")
        logger.info(f"异步任务 {task_id} 开始执行")
        await asyncio.sleep(0.1)
        logger.info(f"异步任务 {task_id} 执行完成")
    
    # 创建多个异步任务
    tasks = [async_task(str(i)) for i in range(3)]
    await asyncio.gather(*tasks)
    
    logger.info("异步日志测试完成")


def demo_contextual_logging():
    """演示上下文相关的日志记录"""
    set_trace_id(f"req_001")
    # 创建带有额外字段的logger
    req_logger = logger.bind(
        request_id="REQ001",
        user_agent="Mozilla/5.0",
        client_ip="127.0.0.1"
    )
    
    # 记录请求处理过程
    req_logger.info("开始处理请求")
    req_logger.debug("验证请求参数")
    req_logger.info("请求处理完成")


if __name__ == "__main__":
    # 运行所有示例
    logger.info("=== 开始运行日志示例程序 ===")
    
    logger.info("--- 1. 基本日志级别演示 ---")
    demo_basic_logging()
    
    logger.info("--- 2. 链路追踪演示 ---")
    demo_trace_id()
    
    logger.info("--- 3. 结构化日志演示 ---")
    demo_structured_logging()
    
    logger.info("--- 4. 异常日志演示 ---")
    demo_exception_logging()
    
    logger.info("--- 5. 上下文日志演示 ---")
    demo_contextual_logging()
    
    logger.info("--- 6. 异步日志演示 ---")
    asyncio.run(demo_async_logging())

    logger.info("--- 7. 演示上下文相关的日志记录 ---")
    demo_contextual_logging()
    
    logger.info("=== 日志示例程序运行完成 ===") 