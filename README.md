# Lithium - 多智能体引擎

## 项目描述
这是一个多智能体引擎系统，用于协调多个不同智能体进行分工协作，并提供API接口供外部系统调用。

## 技术栈
- Python 3.12
- FastAPI 0.109.2
- SQLAlchemy 2.0.27
- Pydantic 2.6.1
- Uvicorn 0.27.1

## 项目结构
```
lithium/
├── app/                    # 主应用程序代码
│   ├── api/               # API接口
│   ├── core/              # 核心功能
│   ├── model/             # 数据库模型
│   ├── schema/            # Pydantic模型
│   ├── service/           # 业务逻辑
│   └── config/            # 配置文件加载
├── tests/                 # 测试文件
├── examples/              # 示例代码
├── migrations/            # 数据库迁移
├── docs/                  # 项目文档
├── scripts/               # 脚本文件
├── configs/               # 配置文件
├── environment.yml        # Conda环境配置
└── README.md             # 项目说明文档
```

## 开发环境配置
1. 创建conda环境：
```bash
conda env create -f environment.yml
```

2. 激活环境：
```bash
conda activate lithium
```

## 运行环境
- Windows/Linux/MacOS
- Python 3.12+

## 功能特性
- 多智能体任务协调
- 智能体角色分配
- 任务调度和管理
- RESTful API接口
- 可扩展的智能体系统 