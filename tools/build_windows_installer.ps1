param(
    [string]$EnvName = "pdfgetx3",
    [string]$Version = "2.0.0"
)

$ErrorActionPreference = "Stop"

$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot "..")
$DistRoot = Join-Path $RepoRoot "dist"
$ReleaseName = "PDFgetX3GUI-v$Version-win-installer"
$BuildRoot = Join-Path $DistRoot "_installer_build"
$ReleaseDir = Join-Path $BuildRoot $ReleaseName
$WheelsDir = Join-Path $ReleaseDir "wheels"
$ZipPath = Join-Path $DistRoot "$ReleaseName.zip"

if (Test-Path $BuildRoot) {
    Remove-Item -LiteralPath $BuildRoot -Recurse -Force
}
New-Item -ItemType Directory -Force -Path $WheelsDir | Out-Null

if (Test-Path $ZipPath) {
    Remove-Item -LiteralPath $ZipPath -Force
}

$CondaBat = Join-Path $env:ProgramData "anaconda3\Scripts\activate.bat"
if (-not (Test-Path $CondaBat)) {
    throw "Cannot find conda activate script at $CondaBat"
}

$BuildBat = Join-Path $ReleaseDir "_build_wheels.bat"
@"
@echo off
call "$CondaBat" $EnvName
if errorlevel 1 exit /b 1
python -m pip wheel --no-deps -w "$WheelsDir" "$RepoRoot"
if errorlevel 1 exit /b 1
python -m pip download --only-binary=:all: -r "$RepoRoot\requirements.txt" -d "$WheelsDir"
if errorlevel 1 exit /b 1
"@ | Set-Content -Path $BuildBat -Encoding ASCII

cmd /d /c "`"$BuildBat`""
if ($LASTEXITCODE -ne 0) {
    throw "Wheel build/download failed"
}
Remove-Item -LiteralPath $BuildBat -Force

@"
@echo off
setlocal
echo ========================================
echo PDFgetX3GUI v$Version Installer
echo ========================================
echo.

set "CONDA_ACTIVATE=%ProgramData%\anaconda3\Scripts\activate.bat"
if not exist "%CONDA_ACTIVATE%" set "CONDA_ACTIVATE=%USERPROFILE%\anaconda3\Scripts\activate.bat"
if not exist "%CONDA_ACTIVATE%" set "CONDA_ACTIVATE=%USERPROFILE%\miniconda3\Scripts\activate.bat"
if not exist "%CONDA_ACTIVATE%" (
    echo ERROR: Could not find conda activate.bat.
    echo Please install Anaconda or Miniconda first.
    pause
    exit /b 1
)

call "%CONDA_ACTIVATE%" $EnvName
if errorlevel 1 (
    echo ERROR: Could not activate conda environment "$EnvName".
    echo Please install PDFgetX3 first, then re-run this installer.
    pause
    exit /b 1
)

python -c "import diffpy.pdfgetx" >nul 2>nul
if errorlevel 1 (
    echo ERROR: PDFgetX3 Python package was not found in "$EnvName".
    echo Please install PDFgetX3 first, then re-run this installer.
    pause
    exit /b 1
)

python -m pip show pdfgetx3gui-v2 >nul 2>nul
if not errorlevel 1 (
    echo Existing PDFgetX3GUI installation found. Uninstalling old version...
    python -m pip uninstall -y pdfgetx3gui-v2
    if errorlevel 1 (
        echo ERROR: Could not uninstall existing PDFgetX3GUI.
        pause
        exit /b 1
    )
) else (
    echo No existing PDFgetX3GUI installation found.
)

python -m pip install --no-index --find-links "%~dp0wheels" --force-reinstall pdfgetx3gui-v2==$Version
if errorlevel 1 (
    echo ERROR: PDFgetX3GUI installation failed.
    pause
    exit /b 1
)

python -c "from PyQt6 import QtWidgets; import scipy; import diffpy.pdfgetx; import pdfgetx3_gui; print('PDFgetX3GUI import check OK')"
if errorlevel 1 (
    echo ERROR: Installation completed, but import check failed.
    pause
    exit /b 1
)

echo.
echo Installation completed successfully.
echo Run launch_pdfgetx3gui.bat to start the GUI.
pause
"@ | Set-Content -Path (Join-Path $ReleaseDir "install_pdfgetx3gui.bat") -Encoding ASCII

@"
@echo off
setlocal
set "CONDA_ACTIVATE=%ProgramData%\anaconda3\Scripts\activate.bat"
if not exist "%CONDA_ACTIVATE%" set "CONDA_ACTIVATE=%USERPROFILE%\anaconda3\Scripts\activate.bat"
if not exist "%CONDA_ACTIVATE%" set "CONDA_ACTIVATE=%USERPROFILE%\miniconda3\Scripts\activate.bat"
if not exist "%CONDA_ACTIVATE%" (
    echo ERROR: Could not find conda activate.bat.
    pause
    exit /b 1
)
call "%CONDA_ACTIVATE%" $EnvName
if errorlevel 1 (
    echo ERROR: Could not activate conda environment "$EnvName".
    pause
    exit /b 1
)
python -m pdfgetx3_gui.main
pause
"@ | Set-Content -Path (Join-Path $ReleaseDir "launch_pdfgetx3gui.bat") -Encoding ASCII

@"
PDFgetX3GUI v$Version Windows Installer

Prerequisite:
- PDFgetX3 is already installed in the conda environment named "$EnvName".

Install:
1. Double-click install_pdfgetx3gui.bat.
2. The installer checks for an older PDFgetX3GUI, uninstalls it if present,
   then installs the bundled version.
3. Wait for the import check to print "PDFgetX3GUI import check OK".

Run:
- Double-click launch_pdfgetx3gui.bat.

Notes:
- This package installs only the GUI and its Python dependencies from bundled wheels.
- It does not install PDFgetX3 itself.
- If your PDFgetX3 environment has another name, run:
  powershell -ExecutionPolicy Bypass -File tools\build_windows_installer.ps1 -EnvName YOUR_ENV_NAME
"@ | Set-Content -Path (Join-Path $ReleaseDir "README_INSTALL.txt") -Encoding UTF8

Get-ChildItem -Path $DistRoot -Filter "*.png" -File -ErrorAction SilentlyContinue |
    Copy-Item -Destination $ReleaseDir -Force

Compress-Archive -LiteralPath $ReleaseDir -DestinationPath $ZipPath -Force

Write-Host "Installer folder: $ReleaseDir"
Write-Host "Installer zip:    $ZipPath"
