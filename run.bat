@echo off
REM PDFgetX3 GUI v2.0 Launcher
setlocal

set "APP_DIR=%~dp0"
set "PYTHONPATH=%APP_DIR%src;%PYTHONPATH%"

for /f "delims=" %%P in ('where pdfgetx3 2^>nul') do (
    if not defined PDFGETX3_EXE set "PDFGETX3_EXE=%%P"
)

if defined PDFGETX3_EXE (
    for %%I in ("%PDFGETX3_EXE%\..\..") do set "PDFGETX3_ROOT=%%~fI"
    set "PDFGETX3GUI_DIFFPY_DIR=%PDFGETX3_ROOT%\Lib\site-packages\diffpy"
)

set "PYTHON_EXE=python"
set "GUI_IMPORT_CHECK=from PyQt6 import QtWidgets; import scipy; import diffpy.pdfgetx"
if defined CONDA_PREFIX (
    for %%P in (
        "%CONDA_PREFIX%\python.exe"
        "%CONDA_PREFIX%\..\diffpy\python.exe"
    ) do (
        if not defined QT_PYTHON_EXE if exist "%%~P" (
            "%%~P" -c "%GUI_IMPORT_CHECK%" >nul 2>nul
            if not errorlevel 1 set "QT_PYTHON_EXE=%%~P"
        )
    )
)

if not defined QT_PYTHON_EXE if defined PDFGETX3_ROOT (
    if exist "%PDFGETX3_ROOT%\envs\diffpy\python.exe" (
        "%PDFGETX3_ROOT%\envs\diffpy\python.exe" -c "%GUI_IMPORT_CHECK%" >nul 2>nul
        if not errorlevel 1 set "QT_PYTHON_EXE=%PDFGETX3_ROOT%\envs\diffpy\python.exe"
    )
)

if defined QT_PYTHON_EXE set "PYTHON_EXE=%QT_PYTHON_EXE%"

"%PYTHON_EXE%" -m pdfgetx3_gui.main
pause
