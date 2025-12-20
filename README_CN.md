# PDFgetX3 GUI v2.0 - 优化版本

[English](README.md) | 简体中文

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**现代化、优化的 PDFgetX3 图形界面**，具有改进的代码质量、增强的用户界面和更好的性能。

## 🎯 v2.0 新功能

这是对原版 PDFgetX3 GUI 的完整优化重构，具有以下特性：

### 🆕 最新更新
- **PyQt6 迁移**: 完全迁移到 PyQt6，支持现代化的 Qt 6 框架
- **Lorch 修正**: 内置 Lorch 函数，减少 PDF 截断振铃效应
- **简化启动**: 使用 `pdfgetx3gui` 命令轻松启动

### ✨ 代码质量改进
- **MVC 架构**: UI、业务逻辑和数据的清晰分离
- **类型注解**: 完整的 Python 类型提示，更好的 IDE 支持
- **现代 Python**: 使用数据类、pathlib 和 Python 3.8+ 特性
- **完善的日志**: 详细的日志记录，便于调试
- **JSON 配置**: 人类可读的 JSON 配置文件，替代文本文件
- **完善的错误处理**: 有意义的错误消息

### 🎨 UI/UX 增强
- 更简洁、更有条理的界面
- 更好的视觉反馈
- 改进的工具提示和帮助文本
- 键盘快捷键支持
- 现代化样式

### ⚡ 性能优化
- 优化的重采样算法
- 高效的数据处理
- 快速的图表更新

### 🧪 测试与质量
- 使用 pytest 的单元测试
- 使用 mypy 的类型检查
- 使用 black 的代码格式化
- 目标代码覆盖率 >80%

## 📋 系统要求

- Python 3.8 或更高版本
- PDFgetX3 ([diffpy.pdfgetx](https://www.diffpy.org/products/pdfgetx.html))
- **PyQt6** >= 6.0.0 (Qt 6 框架)
- matplotlib >= 3.5.0 (需要 Qt6 支持)
- NumPy >= 1.19.0
- SciPy >= 1.5.0

## 🚀 安装

### 前置要求

**重要**：PDFgetX3 需要从哥伦比亚大学获取免费的学术许可证。

#### 步骤 1：获取 PDFgetX3 许可证（必需）

PDFgetX3 免费提供给学术研究使用。请按以下步骤操作：

1. 访问许可证页面：[https://columbia.resoluteinnovation.com/technologies/M11-120](https://columbia.resoluteinnovation.com/technologies/M11-120)
2. 选择 "Express Licensing" → "Sign In To Continue"
3. 登录后，搜索 "pdfgetx3" 或 "m11-120"
4. 再次选择 "Express Licensing" → 选择 "PDFgetX3 and PDFgetN3, Free Academic"
5. 提交许可证申请并等待确认邮件
6. 从此处下载：[https://columbia.resoluteinnovation.com/downloads](https://columbia.resoluteinnovation.com/downloads)

非学术用途请联系 [Columbia Technology Ventures](mailto:techtransfer@columbia.edu)。

**官方文档**：[https://www.diffpy.org/products/pdfgetx.html](https://www.diffpy.org/products/pdfgetx.html)

#### 步骤 2：安装 PDFgetX3

获取许可证后，按照下载包中提供的说明安装 PDFgetX3。

### 安装 GUI 应用程序

```bash
cd PDFgetX3GUI_v2

# 安装 Python 依赖
pip install -r requirements.txt

# 安装 GUI 程序包
pip install -e .
```

**安装后，使用以下命令启动：**
```bash
pdfgetx3gui
# 或
pdfgetx3gui-v2
```

## 💻 使用方法

### 运行 GUI

```bash
pdfgetx3gui
# 或
pdfgetx3gui-v2
```

### Python API

```python
from pdfgetx3_gui import PDFCalculator, Settings
from pdfgetx3_gui.config.settings import PDFParameters

# 配置参数
params = PDFParameters(
    qmin=1.0,
    qmax=25.0,
    composition="LaB6",
    lorch=True  # 启用 Lorch 修正
)

# 计算 PDF
calculator = PDFCalculator()
results = calculator.calculate(
    params=params,
    file="path/to/data.xy"
)

# 访问结果
print(f"G(r): {len(results.gr)} 个数据点")
print(f"r 范围: {results.r[0]:.2f} - {results.r[-1]:.2f} Å")
```

## 📖 功能特性

### 数据输入
- 支持多种格式（Q、2θ）
- 文件历史记录和快速访问
- 背景文件管理
- 拖放支持（即将推出）

### 参数控制
- 实时参数调整
- 参数预设
- 自动验证
- 步长控制

### 数据处理
- 多种重采样模式（线性、指数）
- 背景减除
- 基于成分的修正
- **Lorch 修正**: 内置 Lorch 函数减少 PDF 截断振铃

### 可视化
- I(Q)、S(Q)、F(Q)、G(r) 图表
- 交互式绘图
- 多图表对比
- 导出图表（即将推出）

### 数据导出
- 单文件保存
- 批量目录处理
- 多种输出格式

### 配置管理
- 自动设置持久化
- 导入/导出配置
- 多配置文件支持（即将推出）

## 🏗️ 项目架构

```
pdfgetx3_gui_v2/
├── src/pdfgetx3_gui/
│   ├── config/          # 设置和配置
│   ├── core/            # 计算引擎
│   ├── gui/             # 用户界面
│   ├── workers/         # 后台线程
│   ├── plotting/        # 可视化
│   └── utils/           # 工具函数
├── tests/               # 测试套件
├── examples/            # 示例脚本
└── docs/                # 文档
```

## 🔧 开发

### 运行测试

```bash
pytest
```

### 类型检查

```bash
mypy src/pdfgetx3_gui
```

### 代码格式化

```bash
black src/pdfgetx3_gui tests
```

## 📊 版本对比

| 功能 | v1.0 | v2.0 |
|---------|------|------|
| **代码行数（主文件）** | 1368 行单文件 | ~500 行模块化 |
| **GUI 框架** | PyQt5 | ✅ **PyQt6** (Qt 6) |
| **类型注解** | ❌ | ✅ 完整 |
| **配置方式** | 文本文件 | JSON |
| **测试** | ❌ | ✅ Pytest |
| **架构** | 单体模式 | MVC 模式 |
| **错误处理** | 基础 | 完善 |
| **日志记录** | Print 语句 | 专业日志 |
| **文档** | 最少 | 详尽 |
| **启动命令** | python -m ... | ✅ **pdfgetx3gui** |
| **Lorch 修正** | ❌ | ✅ **内置** |

## 🤝 贡献

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建功能分支
3. 为新功能添加测试
4. 确保所有测试通过
5. 提交 Pull Request

## 📝 许可证

MIT License - 详见 LICENSE 文件

## 🙏 致谢

- 原始 PDFgetX3 GUI 由 Kenneth P. Marshall 开发
- PDFgetX3 由 Simon Billinge 和 Pavol Juhás 开发
- 优化和现代化由 AI Assistant 完成

## 📞 支持

- **问题反馈**: [GitHub Issues](https://github.com/tianxiangchen1993/pdfgetx3gui/issues)
- **原项目**: [pdfgetx3_gui v1.0](https://github.com/msujas/pdfgetx3_gui)
- **PDFgetX3**: [DiffPy 文档](https://www.diffpy.org/products/pdfgetx.html)

## 🗺️ 开发路线图

- [ ] Web 界面版本
- [ ] 插件系统
- [ ] 高级拟合工具
- [ ] 数据库集成用于结果存储
- [ ] 自动化工作流
- [ ] 云处理支持

---

**注意**: 这是与原项目并行创建的优化版本。两个版本都在维护中，适用于不同的使用场景。
