from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field


class ModelConfig(BaseModel):
    """OpenAI模型配置类
    
    用于配置调用OpenAI API时的各项参数
    """
    api_key: str = Field(..., description="OpenAI API密钥")
    api_base: Optional[str] = Field(default=None, description="OpenAI API基础URL")
    model: str = Field(default="gpt-3.5-turbo", description="OpenAI模型名称")
    temperature: float = Field(default=0.7, ge=0, le=2, description="采样温度，控制输出的随机性")
    top_p: float = Field(default=1.0, ge=0, le=1, description="核采样参数")
    n: int = Field(default=1, ge=1, description="生成的候选回复数量")
    max_tokens: Optional[int] = Field(default=None, description="生成的最大token数")
    presence_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="重复惩罚系数")
    frequency_penalty: float = Field(default=0.0, ge=-2.0, le=2.0, description="频率惩罚系数")
    stream: bool = Field(default=False, description="是否启用流式响应")
    stop: Optional[List[str]] = Field(default=None, description="停止生成的标记序列")
    functions: Optional[List[Dict[str, Any]]] = Field(default=None, description="可用的函数列表")
    function_call: Optional[Dict[str, Any]] = Field(default=None, description="函数调用配置")
    
    class Config:
        """Pydantic配置类"""
        arbitrary_types_allowed = True