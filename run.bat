@echo off
REM PDFgetX3 GUI v2.0 Launcher
set PYTHONPATH=%~dp0src;%PYTHONPATH%
python -m pdfgetx3_gui.main
pause
