# PDFgetX3 GUI v2.0 - Optimized Version

English | [简体中文](README_CN.md)

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A modern, optimized GUI for PDFgetX3** with improved code quality, enhanced UI/UX, and better performance.

## 🎯 What's New in v2.0

This is a complete optimization of the original PDFgetX3 GUI with:

### 🆕 Latest Updates
- **PyQt6 Migration**: Fully migrated to PyQt6 for modern Qt 6 support
- **Lorch Modification**: Built-in Lorch function to reduce PDF termination ripples
- **Simplified Startup**: Easy installation with `pdfgetx3gui` command

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
- **PyQt6** >= 6.0.0 (Qt 6 framework)
- matplotlib >= 3.5.0 (Qt6 support required)
- NumPy >= 1.19.0
- SciPy >= 1.5.0

## 🚀 Installation

### Prerequisites

**Important**: PDFgetX3 requires a free academic license from Columbia University.

#### Step 1: Obtain PDFgetX3 License (Required)

PDFgetX3 is available for free for academic research. Follow these steps:

1. Visit the licensing page: [https://columbia.resoluteinnovation.com/technologies/M11-120](https://columbia.resoluteinnovation.com/technologies/M11-120)
2. Select "Express Licensing" → "Sign In To Continue"
3. After sign-in, search for "pdfgetx3" or "m11-120"
4. Select "Express Licensing" again → Choose "PDFgetX3 and PDFgetN3, Free Academic"
5. Submit the license request and wait for confirmation email
6. Download from: [https://columbia.resoluteinnovation.com/downloads](https://columbia.resoluteinnovation.com/downloads)

For non-academic use, contact [Columbia Technology Ventures](mailto:techtransfer@columbia.edu).

**Official Documentation**: [https://www.diffpy.org/products/pdfgetx.html](https://www.diffpy.org/products/pdfgetx.html)

#### Step 2: Install PDFgetX3

After obtaining the license, install PDFgetX3 following the instructions provided in the download package.

### Install GUI Application

```bash
cd PDFgetX3GUI_v2

# Install Python dependencies
pip install -r requirements.txt

# Install the GUI package
pip install -e .
```

**After installation, launch with:**
```bash
pdfgetx3gui
# or
pdfgetx3gui-v2
```

## 💻 Usage

### Run the GUI

```bash
pdfgetx3gui
# or
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
- **Lorch Modification**: Reduce PDF termination ripples with built-in Lorch function

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
| **Code Lines (main)** | 1368 lines single file | ~500 lines modular |
| **GUI Framework** | PyQt5 | ✅ **PyQt6** (Qt 6) |
| **Type Annotations** | ❌ | ✅ Full |
| **Configuration** | Text files | JSON |
| **Testing** | ❌ | ✅ Pytest |
| **Architecture** | Monolithic | MVC Pattern |
| **Error Handling** | Basic | Comprehensive |
| **Logging** | Print statements | Proper logging |
| **Documentation** | Minimal | Extensive |
| **Startup Command** | python -m ... | ✅ **pdfgetx3gui** |
| **Lorch Modification** | ❌ | ✅ **Built-in** |

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

- Original PDFgetX3 GUI developed by Kenneth P. Marshall
- PDFgetX3 developed by Simon Billinge and Pavol Juhás
- **Optimization and modernization powered by [Google Gemini Antigravity](https://deepmind.google/technologies/gemini/)**

### 🤖 Developed with Google Gemini Antigravity

This project demonstrates the power of AI-assisted software development. The entire v2.0 optimization was accomplished through collaboration with **Google Gemini Antigravity**, Google's advanced AI coding assistant.

#### How Antigravity Helped Build This Project

**1. PyQt5 → PyQt6 Migration**
- Analyzed all source files to identify PyQt5 dependencies
- Systematically updated imports, API calls, and enum values
- Ensured Qt6 compatibility across the entire codebase

**2. Code Modernization**
- Refactored monolithic code into clean MVC architecture
- Added comprehensive type annotations throughout
- Implemented proper error handling and logging
- Created JSON-based configuration system

**3. New Features Implementation**
- **Lorch Modification**: Researched the algorithm, implemented the mathematical function, integrated into calculation pipeline
- **Simplified Startup**: Created `setup.py` with proper entry points
- **.chi Format Support**: Verified and documented file format compatibility

**4. GitHub Deployment**
- Initialized Git repository with proper `.gitignore`
- Crafted meaningful commit messages
- Created comprehensive bilingual documentation (English + Chinese)
- Pushed to GitHub with complete version history

**5. Documentation**
- Generated detailed README files in two languages
- Created implementation plans and walkthroughs
- Corrected installation instructions based on official sources

#### The Antigravity Workflow

```mermaid
graph LR
    A[User Request] --> B[Antigravity Analysis]
    B --> C[Code Planning]
    C --> D[Implementation]
    D --> E[Testing & Verification]
    E --> F[Documentation]
    F --> G[GitHub Deployment]
    G --> H[Iteration & Refinement]
```

**Key Benefits**:
- ✅ **Speed**: Complete migration and feature additions in hours, not days
- ✅ **Quality**: Consistent code style, comprehensive error handling
- ✅ **Documentation**: Bilingual README, detailed comments
- ✅ **Best Practices**: Modern Python patterns, proper project structure

#### Why Antigravity?

[Google Gemini Antigravity](https://deepmind.google/technologies/gemini/) is not just a code generator—it's a true pair programming partner that:
- Understands complex codebases and their architecture
- Reasons about technical decisions and trade-offs
- Maintains context across long development sessions
- Generates production-quality code with proper testing
- Creates comprehensive documentation automatically

**This project is a testament to what's possible when human expertise meets advanced AI assistance.**

---

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
