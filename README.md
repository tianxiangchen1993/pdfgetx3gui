# PDFgetX3GUI v2.0

PDFgetX3GUI 是一个面向 PDFgetX3 的 Windows 图形界面，用于从 X-ray / neutron total scattering 数据中计算和查看 PDF 结果。

本项目重点解决命令行 PDFgetX3 对新用户不够友好的问题：把数据文件选择、参数设置、计算、绘图和结果保存集中到一个 PyQt6 桌面界面中。

## 当前状态

- GUI 版本：v2.0.0
- 推荐系统：Windows
- 推荐 Python 环境：Conda 环境 `pdfgetx3`
- GUI 框架：PyQt6
- 计算核心：PDFgetX3 / `diffpy.pdfgetx`

安装包只包含 GUI 和相关 Python 依赖，不包含 PDFgetX3 本体。使用前请先确认 PDFgetX3 已经可以在本机正常运行。

## 主要功能

- 支持选择实验数据文件和背景文件。
- 支持 Q / 2theta 数据格式。
- 支持设置 wavelength、composition、qmin、qmax、rmin、rmax、rstep 等 PDFgetX3 参数。
- 支持 I(Q)、S(Q)、F(Q)、G(r) 图形显示。
- 支持批量文件处理和结果保存。
- 支持 Lorch 修正，用于降低 PDF 截断振荡。
- 提供 Windows 安装包构建脚本，便于分发给已有 PDFgetX3 环境的用户。

## 安装前提

请先完成以下准备：

1. 安装 Anaconda 或 Miniconda。
2. 创建或准备名为 `pdfgetx3` 的 conda 环境。
3. 在该环境中安装并确认 PDFgetX3 可用。

可用下面命令检查 PDFgetX3：

```bat
conda activate pdfgetx3
pdfgetx3 --version
python -c "import diffpy.pdfgetx; print('PDFgetX3 OK')"
```

如果上述命令失败，请先修复 PDFgetX3 环境，再安装本 GUI。

## 使用安装包安装

面向普通用户，推荐使用发布包：

```text
PDFgetX3GUI-v2.0.0-win-installer.zip
```

安装步骤：

1. 解压 zip 文件。
2. 双击运行 `install_pdfgetx3gui.bat`。
3. 等待出现 `PDFgetX3GUI import check OK`。
4. 双击 `launch_pdfgetx3gui.bat` 启动程序。

安装包会从自带的 `wheels/` 目录安装 GUI 依赖，因此可以减少网络依赖。它仍然要求本机已经有可用的 `pdfgetx3` conda 环境。

## 从源码安装

适合开发者或需要修改源码的用户。

```bat
git clone https://github.com/tianxiangchen1993/pdfgetx3gui.git
cd pdfgetx3gui

conda activate pdfgetx3
python -m pip install -e .
```

安装后可以运行：

```bat
pdfgetx3gui-v2
```

如果系统中旧启动器指向了错误 Python，也可以直接运行：

```bat
python -m pdfgetx3_gui.main
```

## 从源码直接启动

在项目目录中运行：

```bat
conda activate pdfgetx3
run.bat
```

`run.bat` 会检查 PyQt6、SciPy 和 `diffpy.pdfgetx` 是否可导入，并尽量选择正确的 Python 解释器启动 GUI。

## 打包 Windows 安装包

项目提供了打包脚本：

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_windows_installer.ps1
```

默认会生成：

```text
dist\PDFgetX3GUI-v2.0.0-win-installer\
dist\PDFgetX3GUI-v2.0.0-win-installer.zip
```

如果 PDFgetX3 环境名称不是 `pdfgetx3`，可以指定环境名：

```powershell
powershell -ExecutionPolicy Bypass -File tools\build_windows_installer.ps1 -EnvName YOUR_ENV_NAME
```

注意：生成的 zip 文件较大，不建议直接提交到 GitHub 仓库。更适合放在 GitHub Release、网盘或邮件附件中。

## 基本使用流程

1. 打开 GUI。
2. 选择数据文件。
3. 选择数据格式：`Q` 或 `2theta`。
4. 填写 wavelength 和 composition。
5. 设置 PDFgetX3 计算参数。
6. 点击“计算”或按 `F5`。
7. 查看 I(Q)、S(Q)、F(Q)、G(r)。
8. 点击“保存结果”导出数据。

## 输出文件

程序会根据用户设置保存不同类型的数据文件。常见输出包括：

- `.iq`：I(Q)
- `.sq`：S(Q)
- `.fq`：F(Q)
- `.gr`：G(r)
- `.cfg`：PDFgetX3 配置文件

启用 Lorch 修正时，程序会区分原始结果和 Lorch 修正后的结果，避免覆盖或混淆。

## 项目结构

```text
src/pdfgetx3_gui/
  config/      配置和参数
  core/        PDF 计算封装
  gui/         PyQt6 界面
  plotting/    绘图组件
  workers/     后台计算线程
  utils/       文件、日志和工具函数
tools/
  build_windows_installer.ps1
examples/
  示例数据和输出
```

## 常见问题

### 1. 启动时报 PyQt6 DLL load failed

通常是启动器使用了错误的 Python 环境。请先激活 `pdfgetx3` 环境，再运行：

```bat
python -m pdfgetx3_gui.main
```

当前版本已加入自动转交逻辑：如果旧启动器从 base Python 启动，会尝试切换到当前激活的 conda 环境 Python。

### 2. 提示找不到 `diffpy.pdfgetx`

说明 PDFgetX3 没有安装到当前 Python 环境。请先确认：

```bat
conda activate pdfgetx3
python -c "import diffpy.pdfgetx"
```

### 3. 提示找不到 `scipy`

请在 `pdfgetx3` 环境中重新安装 GUI：

```bat
conda activate pdfgetx3
python -m pip install -e .
```

或者运行安装包中的 `install_pdfgetx3gui.bat`。

### 4. 安装包是否包含 PDFgetX3

不包含。安装包只包含 GUI 和 GUI 依赖。PDFgetX3 本体需要用户提前按其许可和安装说明配置好。

## 开发说明

推荐在 `pdfgetx3` 环境中开发：

```bat
conda activate pdfgetx3
python -m pip install -e .
python -m pdfgetx3_gui.main
```

提交前建议至少做一次启动检查：

```bat
set QT_QPA_PLATFORM=offscreen
python -c "from PyQt6 import QtWidgets; import scipy; import diffpy.pdfgetx; from pdfgetx3_gui.gui import MainWindow; app=QtWidgets.QApplication([]); window=MainWindow(); print('OK')"
```

## 许可证

本项目使用 MIT License。PDFgetX3 本体及其许可请参考 PDFgetX3 官方说明。

## 致谢

- PDFgetX3：Simon Billinge 和 Pavol Juhás 等开发者。
- 原始 PDFgetX3 GUI：Kenneth P. Marshall。
- 本项目在原有 GUI 思路基础上进行了 PyQt6 化、界面整理、启动环境修复和 Windows 打包流程整理。
