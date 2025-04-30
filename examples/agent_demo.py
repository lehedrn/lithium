import asyncio
from typing import AsyncGenerator
from app.core.agents.model_config import ModelConfig
from app.core.agents.base_agent import BaseAgent
from app.config.config_loader import config


async def test_basic_chat(agent: BaseAgent) -> None:
    """测试基本对话功能
    
    Args:
        agent: BaseAgent实例
    """
    print("\n=== 测试基本对话 ===")
    response = await agent.generate(
        "你好，请介绍一下你自己。",
        stream=False
    )
    print(f"AI助手: {response}\n")


async def test_code_generation(agent: BaseAgent) -> None:
    """测试代码生成功能
    
    Args:
        agent: BaseAgent实例
    """
    print("\n=== 测试代码生成 ===")
    prompt = """
    请生成一个Python类，要求：
    1. 实现一个简单的缓存装饰器
    2. 支持设置过期时间
    3. 支持最大缓存数量
    4. 使用示例
    """
    response = await agent.generate(prompt, stream=False)
    print(f"生成的代码:\n{response}\n")


async def test_stream_chat(agent: BaseAgent) -> None:
    """测试流式对话
    
    Args:
        agent: BaseAgent实例
    """
    print("\n=== 测试流式对话 ===")
    print("AI助手: ", end="", flush=True)
    
    prompt = """
    请详细解释以下概念：
    1. Python的异步编程
    2. asyncio的工作原理
    3. 实际应用场景
    请分点说明，要简洁清晰。
    """
    
    async for chunk in await agent.generate(prompt, stream=True):
        print(chunk, end="", flush=True)
    print("\n")


async def test_continuous_conversation(agent: BaseAgent) -> None:
    """测试连续对话
    
    Args:
        agent: BaseAgent实例
    """
    print("\n=== 测试连续对话 ===")
    
    # 第一轮对话
    response = await agent.generate(
        "什么是依赖注入？",
        stream=False
    )
    print(f"问题: 什么是依赖注入？")
    print(f"AI助手: {response}\n")
    
    # 第二轮对话（基于上下文）
    response = await agent.generate(
        "请给出一个Python的具体示例。",
        stream=False
    )
    print(f"问题: 请给出一个Python的具体示例。")
    print(f"AI助手: {response}\n")


async def main() -> None:
    """主函数"""
    agent = None
    try:
        # 从配置文件获取LLM配置
        llm_config = config.get("llm", {})
        
        # 创建ModelConfig实例
        model_config = ModelConfig(
            api_key=llm_config.get("api_key"),
            api_base=llm_config.get("api_base"),
            model=llm_config.get("model", "gpt-3.5-turbo"),
            temperature=llm_config.get("temperature", 0.7),
            stream=True  # 默认启用流式响应
        )
        
        # 创建BaseAgent实例
        agent = BaseAgent(
            model_config=model_config,
            system_prompt="你是一个专业的Python开发助手，精通Python编程、设计模式和最佳实践。"
        )
        
        # 运行各种测试
        await test_basic_chat(agent)
        await test_code_generation(agent)
        await test_stream_chat(agent)
        await test_continuous_conversation(agent)
            
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        if agent:
            await agent.close()


if __name__ == "__main__":
    asyncio.run(main()) 