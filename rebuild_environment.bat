@echo off
echo ========================================
echo PDFgetX3 环境完全重建脚本
echo ========================================
echo.

echo [1/5] 删除旧环境...
call conda env list
call conda env remove -n pdfgetx3 -y
if %ERRORLEVEL% NEQ 0 (
    echo 注意: 旧环境可能不存在或已删除
)
echo.

echo [2/5] 创建新环境 (Python 3.11)...
call conda create -n pdfgetx3 python=3.11 -y
if %ERRORLEVEL% NEQ 0 (
    echo 错误: 创建环境失败
    pause
    exit /b 1
)
echo.

echo [3/5] 激活环境并添加conda-forge通道...
call conda activate pdfgetx3
call conda config --add channels conda-forge
echo.

echo [4/5] 安装pdfgetx3 (尝试安装最新版本)...
call conda install diffpy.pdfgetx -y
if %ERRORLEVEL% NEQ 0 (
    echo 警告: conda安装失败，可能需要手动安装pdfgetx3
    echo 如果您有wheel或tar.gz文件，请手动运行:
    echo   conda activate pdfgetx3
    echo   pip install 路径\到\pdfgetx3文件
)
echo.

echo [5/5] 安装PDFgetX3 GUI...
cd /d "%~dp0"
call pip install -e .
if %ERRORLEVEL% NEQ 0 (
    echo 错误: GUI安装失败
    pause
    exit /b 1
)
echo.

echo ========================================
echo 安装完成！
echo ========================================
echo.
echo 测试安装:
call python -c "import pdfgetx3_gui; print('GUI模块导入成功!')"
echo.
echo 运行命令: pdfgetx3gui-v2
echo ========================================
pause
