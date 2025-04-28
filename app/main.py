"""
主应用入口
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utils.logger import get_logger

# 获取日志实例
logger = get_logger()

# 创建FastAPI应用
app = FastAPI(
    title="Lithium",
    version="0.1.0",
    description="多智能体协调引擎API",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """应用启动时的处理"""
    logger.info("应用启动")
    
@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭时的处理"""
    logger.info("应用关闭")
    
@app.get("/")
async def root():
    """根路由"""
    return {"message": "Welcome to Lithium Multi-Agent Engine"} 