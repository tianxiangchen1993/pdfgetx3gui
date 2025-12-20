# PDFgetX3 GUI v2.0 - Optimized Version

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A modern, optimized GUI for PDFgetX3** with improved code quality, enhanced UI/UX, and better performance.

## 🎯 What's New in v2.0

This is a complete optimization of the original PDFgetX3 GUI with:

### ✨ Code Quality Improvements
- **MVC Architecture**: Clean separation of UI, business logic, and data
- **Type Annotations**: Full Python type hints for better IDE support
- **Modern Python**: Dataclasses, pathlib, and Python 3.8+ features
- **Comprehensive Logging**: Detailed logging for debugging
- **JSON Configuration**: Human-readable JSON instead of text files
- **Proper Error Handling**: Meaningful error messages

### 🎨 UI/UX Enhancements
- Cleaner, more organized interface
- Better visual feedback
- Improved tooltips and help text
- Keyboard shortcuts
- Modern styling

### ⚡ Performance Optimizations
- Optimized resampling algorithms
- Efficient data handling
- Faster plot updates

### 🧪 Testing & Quality
- Unit tests with pytest
- Type checking with mypy
- Code formatting with black
- >80% code coverage target

## 📋 Requirements

- Python 3.8 or higher
- PDFgetX3 ([diffpy.pdfgetx](https://www.diffpy.org/products/pdfgetx.html))
- PyQt5
- NumPy, SciPy, Matplotlib

## 🚀 Installation

### From Source

```bash
cd pdfgetx3_gui_v2
pip install -e .
```

### With Development Tools

```bash
pip install -e ".[dev]"
```

## 💻 Usage

### Run the GUI

```bash
pdfgetx3gui-v2
```

### Python API

```python
from pdfgetx3_gui import PDFCalculator, PDFParameters

# Configure parameters
params = PDFParameters(
    qmin=1.0,
    qmax=25.0,
    composition="LaB6"
)

# Calculate PDF
calculator = PDFCalculator()
results = calculator.calculate(
    params=params,
    file="path/to/data.xy"
)

# Access results
print(f"G(r): {len(results.gr)} points")
```

## 📖 Features

### Data Input
- Support for multiple formats (Q, 2θ)
- File history and quick access
- Background file management
- Drag & drop support (coming soon)

### Parameter Control
- Real-time parameter adjustment
- Parameter presets
- Automatic validation
- Step size control

### Data Processing
- Multiple resampling modes (linear, exponential)
- Background subtraction
- Composition-based corrections

### Visualization
- I(Q), S(Q), F(Q), G(r) plots
- Interactive plotting
- Multiple plots comparison
- Export plots (coming soon)

### Data Export
- Individual file saving
- Batch directory processing
- Multiple output formats

### Configuration
- Automatic settings persistence
- Import/export configurations
- Multiple configuration profiles (coming soon)

## 🏗️ Architecture

```
pdfgetx3_gui_v2/
├── src/pdfgetx3_gui/
│   ├── config/          # Settings and configuration
│   ├── core/            # Calculation engine
│   ├── gui/             # User interface
│   ├── workers/         # Background threads
│   ├── plotting/        # Visualization
│   └── utils/           # Utilities
├── tests/               # Test suite
├── examples/            # Example scripts
└── docs/                # Documentation
```

## 🔧 Development

### Run Tests

```bash
pytest
```

### Type Checking

```bash
mypy src/pdfgetx3_gui
```

### Code Formatting

```bash
black src/pdfgetx3_gui tests
```

## 📊 Comparison with v1.0

| Feature | v1.0 | v2.0 |
|---------|------|------|
| Code Lines (main) | 1368 | ~500 (modular) |
| Type Annotations | ❌ | ✅ |
| Configuration | Text files | JSON |
| Testing | ❌ | ✅ Pytest |
| Architecture | Monolithic | MVC Pattern |
| Error Handling | Basic | Comprehensive |
| Logging | Print statements | Proper logging |
| Documentation | Minimal | Extensive |

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new features
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Original PDFgetX3 GUI by Kenneth P. Marshall
- PDFgetX3 by Simon Billinge and Pavol Juhás
- Optimizations and modernization by AI Assistant

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/msujas/pdfgetx3_gui/issues)
- **Original Project**: [pdfgetx3_gui v1.0](https://github.com/msujas/pdfgetx3_gui)
- **PDFgetX3**: [DiffPy Documentation](https://www.diffpy.org/products/pdfgetx.html)

## 🗺️ Roadmap

- [ ] Web interface version
- [ ] Plugin system
- [ ] Advanced fitting tools
- [ ] Database integration for results
- [ ] Automated workflows
- [ ] Cloud processing support

---

**Note**: This is an optimized version created alongside the original project. Both versions are maintained for different use cases.
