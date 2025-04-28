@echo off
rem 设置PYTHONPATH为项目根目录
set PYTHONPATH=%~dp0.. 
rem 运行主应用
python -m app.main
pause
