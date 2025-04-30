from typing import List, Dict, Any, Optional, AsyncGenerator
import httpx
from openai import AsyncOpenAI
from pydantic import BaseModel

from app.core.agents.model_config import ModelConfig


class Message(BaseModel):
    """对话消息类"""
    role: str
    content: str
    name: Optional[str] = None
    function_call: Optional[Dict[str, Any]] = None


class BaseAgent:
    """Agent基类
    
    提供与OpenAI API交互的基本功能
    """
    def __init__(
        self,
        model_config: ModelConfig,
        system_prompt: Optional[str] = None,
    ):
        """初始化Agent
        
        Args:
            model_config: 模型配置
            system_prompt: 系统提示词
        """
        self.model_config = model_config
        self._messages: List[Message] = []
        
        # 创建httpx客户端，设置正确的超时和限制
        http_client = httpx.AsyncClient(
            timeout=60.0,
            limits=httpx.Limits(
                max_keepalive_connections=5,
                max_connections=10,
                keepalive_expiry=30
            )
        )
        
        # 创建OpenAI客户端
        self.client = AsyncOpenAI(
            api_key=model_config.api_key,
            base_url=model_config.api_base,
            http_client=http_client,
            timeout=60.0
        )
        
        if system_prompt:
            self.add_message("system", system_prompt)
    
    def add_message(self, role: str, content: str, name: Optional[str] = None) -> None:
        """添加消息到历史记录
        
        Args:
            role: 消息角色
            content: 消息内容
            name: 可选的名称
        """
        self._messages.append(Message(role=role, content=content, name=name))
    
    def clear_messages(self) -> None:
        """清空历史消息"""
        self._messages.clear()
    
    @property
    def messages(self) -> List[Dict[str, Any]]:
        """获取消息历史"""
        return [msg.dict(exclude_none=True) for msg in self._messages]
    
    async def _create_chat_completion(
        self,
        messages: Optional[List[Dict[str, Any]]] = None,
        **kwargs
    ) -> Any:
        """创建聊天完成
        
        Args:
            messages: 消息列表，如果为None则使用历史消息
            **kwargs: 其他参数
        
        Returns:
            OpenAI API的响应
        """
        messages = messages or self.messages
        params = {
            "model": self.model_config.model,
            "messages": messages,
            "stream": self.model_config.stream,
            **{k: v for k, v in self.model_config.dict().items() 
               if k not in ["model", "stream", "api_key", "api_base"] and v is not None},
            **kwargs
        }
        
        return await self.client.chat.completions.create(**params)
    
    async def generate(
        self,
        prompt: str,
        stream: Optional[bool] = None,
        **kwargs
    ) -> AsyncGenerator[str, None] | str:
        """生成回复
        
        Args:
            prompt: 提示词
            stream: 是否使用流式响应，覆盖配置中的设置
            **kwargs: 其他参数
        
        Returns:
            如果是流式响应，返回异步生成器；否则返回完整响应
        """
        self.add_message("user", prompt)
        
        if stream is not None:
            self.model_config.stream = stream
        
        response = await self._create_chat_completion(**kwargs)
        
        if self.model_config.stream:
            full_content = []  # 使用列表存储内容片段，避免频繁的字符串拼接
            async def response_generator() -> AsyncGenerator[str, None]:
                nonlocal full_content
                async for chunk in response:
                    if chunk.choices[0].delta.content is not None:
                        content = chunk.choices[0].delta.content
                        yield content  # 先yield确保实时性
                        full_content.append(content)  # 后存储内容
                # 流式响应结束后，将完整内容添加到消息历史
                self.add_message("assistant", "".join(full_content))
            return response_generator()
        else:
            content = response.choices[0].message.content
            self.add_message("assistant", content)
            return content
            
    async def close(self):
        """关闭客户端"""
        await self.client.close()        # 关闭底层的httpx客户端
        await self.client.http_client.aclose()
