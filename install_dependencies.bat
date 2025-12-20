@echo off
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Note: diffpy.pdfgetx must be installed via conda:
echo conda install -c conda-forge diffpy.pdfgetx
echo.
pause
