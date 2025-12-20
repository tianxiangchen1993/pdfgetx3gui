# PDFgetX3 GUI v2.0 安装指南

## 系统要求

- Python 3.8 或更高版本
- Windows / Linux / macOS
- 至少 500 MB 可用磁盘空间

## 安装步骤

### 1. 检查 Python 版本

```bash
python --version
# 或
python3 --version
```

应该显示 Python 3.8.x 或更高版本。

### 2. 安装 PDFgetX3 依赖

PDFgetX3 是必需的核心依赖：

```bash
# 使用 conda (推荐)
conda install -c conda-forge diffpy.pdfgetx

# 或使用 pip
pip install diffpy.pdfgetx
```

### 3. 进入项目目录

```bash
cd e:\pdfgetx3_gui-master\pdfgetx3_gui_v2
```

### 4. 安装新版本

#### 方法 A：开发模式（推荐用于测试）

```bash
# 安装基础版本
pip install -e .

# 或安装开发版本（包含测试工具）
pip install -e ".[dev]"
```

**优点**：
- 代码更改立即生效
- 适合开发和测试
- 可以运行测试

#### 方法 B：标准安装

```bash
pip install .
```

### 5. 验证安装

```bash
# 运行主程序
pdfgetx3gui-v2

# 或使用 Python 模块方式
python -m pdfgetx3_gui.main
```

您应该看到类似输出：

```
🚀 PDFgetX3 GUI v2.0 - Optimized Version
============================================================

⚠️  GUI is currently under development.

✅ Core modules implemented:
   • Configuration management (settings.py)
   • PDF calculator (calculator.py)
   ...
```

## 运行测试（可选）

如果安装了开发版本：

```bash
# 运行所有测试
pytest

# 运行特定测试
pytest tests/test_config.py -v

# 查看测试覆盖率
pytest --cov=pdfgetx3_gui --cov-report=html
```

## Python API 使用示例

安装后，您可以在 Python 脚本中使用：

```python
from pdfgetx3_gui import PDFCalculator, PDFParameters
from pdfgetx3_gui.utils import FileIO

# 加载数据
x, y = FileIO.load_data("your_data.xy")

# 配置参数
params = PDFParameters(
    qmin=1.0,
    qmax=25.0,
    composition="LaB6"
)

# 计算 PDF
calculator = PDFCalculator()
results = calculator.calculate(
    params=params,
    file="your_data.xy"
)

# 使用结果
print(f"G(r) 有 {len(results.gr)} 个数据点")
print(f"r 范围: {results.r[0]:.2f} - {results.r[-1]:.2f} Å")

# 保存结果
calculator.save_results(
    results,
    basename="output/my_sample",
    save_gr=True,
    save_sq=True
)
```

## 常见问题

### Q: 提示找不到 diffpy.pdfgetx？

**A**: 请先安装 PDFgetX3：
```bash
conda install -c conda-forge diffpy.pdfgetx
```

### Q: 提示 Python 版本过低？

**A**: 请升级到 Python 3.8 或更高版本。

### Q: GUI 无法启动？

**A**: 当前 GUI 尚未完成，核心模块可通过 Python API 使用。

### Q: 如何卸载？

**A**: 
```bash
pip uninstall pdfgetx3gui-v2
```

## 与原版共存

新版本和原版可以同时安装：

- **原版命令**: `pdfgetx3gui`
- **新版命令**: `pdfgetx3gui-v2`

两个版本互不干扰。

## 下一步

- 阅读 [README.md](README.md) 了解功能特性
- 查看 [DEVELOPMENT.md](DEVELOPMENT.md) 了解开发状态
- 运行测试验证安装：`pytest`

## 技术支持

遇到问题？
1. 检查 Python 版本 (>=3.8)
2. 确认 PDFgetX3 已安装
3. 查看日志文件：`~/.pdfgetx3gui_v2/pdfgetx3gui.log`
4. 提交 GitHub Issue
