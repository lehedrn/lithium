"""
主应用入口
"""

from app.utils.logger import logger
from app.config.config_loader import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动
    logger.info("应用启动")
    yield
    # 应用关闭
    logger.info("应用关闭")

# 创建FastAPI应用
app = FastAPI(
    title=config.get("app", {}).get("name", "Lithium"),
    version=config.get("app", {}).get("version", "0.1.0"),
    description="多智能体协调引擎API",
    docs_url=config.get("api", {}).get("prefix", "/api/v1") + "/docs",
    redoc_url=config.get("api", {}).get("prefix", "/api/v1") + "/redoc",
    openapi_url=config.get("api", {}).get("prefix", "/api/v1") + "/openapi.json",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get(config.get("api", {}).get("prefix", "/api/v1") + "/")
async def root():
    """根路由"""
    return {"message": f"Welcome to {config.get('app', {}).get('name', 'Lithium')} Multi-Agent Engine"}

if __name__ == "__main__":
    import uvicorn

    host = config.get("api", {}).get("host", "0.0.0.0")
    port = config.get("api", {}).get("port", 8000)
    debug = config.get("app", {}).get("debug", False)

    logger.info(f"启动服务器： host={host}, port={port}, reload={debug}")
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=debug
    )
