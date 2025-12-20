# PDFgetX3 GUI v2.0.0 Release Notes

## 🎉 Major Release: PyQt6 Migration + Enhanced Features

This is a major release with significant improvements and new features, powered by **Google Gemini Antigravity**.

---

## 🆕 What's New

### 1. PyQt6 Migration
- **Fully migrated from PyQt5 to PyQt6** for modern Qt 6 support
- Updated all imports, API calls, and enum values
- Matplotlib backend upgraded to QtAgg for Qt6 compatibility
- Future-proof with long-term Qt 6 support

### 2. Lorch Modification Function
- **Built-in Lorch modification** to reduce PDF termination ripples
- Mathematical implementation: `M(Q) = sinc(Q/Qmax)`
- Applies to F(Q) and recalculates G(r) via Fourier transform
- GUI checkbox option in Parameters tab
- Reduces spurious oscillations in G(r)

### 3. Simplified Startup
- **New command**: Simply type `pdfgetx3gui` to launch
- Alternative: `pdfgetx3gui-v2`
- Proper setup.py with entry points
- No more complex Python module invocation

### 4. File Format Support
- Added **.chi format support** for XRD data
- Supported formats: .txt, .dat, .xy, .xye, .csv, .chi
- Compatible with synchrotron radiation sources

### 5. Bilingual Documentation
- **Complete Chinese translation** (README_CN.md)
- Language switcher in both READMEs
- Accessible to both English and Chinese-speaking users

### 6. Corrected Installation Instructions
- Updated PDFgetX3 installation process
- Accurate Columbia University licensing information
- Official documentation links

---

## 🏗️ Architecture Improvements

- **MVC Pattern**: Clean separation of concerns
- **Type Annotations**: Full Python type hints throughout
- **Modern Python**: Dataclasses, pathlib, Python 3.8+ features
- **JSON Configuration**: Human-readable configuration files
- **Comprehensive Logging**: Detailed logging for debugging
- **Error Handling**: Meaningful error messages

---

## 📦 Installation

### Prerequisites

1. **Obtain PDFgetX3 License** (Required)
   - Visit: https://columbia.resoluteinnovation.com/technologies/M11-120
   - Free for academic research
   - Follow the licensing process

2. **Install PDFgetX3**
   - Follow instructions from the downloaded package

### Install GUI

```bash
# Download the wheel file from this release
pip install pdfgetx3gui_v2-2.0.0-py3-none-any.whl

# Or from source
git clone https://github.com/tianxiangchen1993/pdfgetx3gui.git
cd pdfgetx3gui
pip install -e .
```

### Launch

```bash
pdfgetx3gui
```

---

## 📊 Comparison with v1.0

|Feature|v1.0|v2.0|
|-------|----|----|
|**GUI Framework**|PyQt5|✅ **PyQt6** (Qt 6)|
|**Code Lines**|1368 single file|~500 modular|
|**Type Annotations**|❌|✅ Full|
|**Architecture**|Monolithic|MVC Pattern|
|**Startup Command**|python -m ...|✅ **pdfgetx3gui**|
|**Lorch Modification**|❌|✅ **Built-in**|
|**Documentation**|English only|English + Chinese|

---

## 🐛 Bug Fixes

- Fixed enum value syntax for Qt6 compatibility
- Corrected dialog return codes (exec_() → exec())
- Updated QAction import location (QtWidgets → QtGui)
- Improved file format validation

---

## 📝 Full Changelog

### Added
- PyQt6 support with Qt 6 framework
- Lorch modification function for PDF smoothing
- .chi file format support
- Simplified startup command (pdfgetx3gui)
- Chinese README (README_CN.md)
- Complete type annotations
- JSON-based configuration system
- Comprehensive logging system

### Changed
- Migrated from PyQt5 to PyQt6
- Updated matplotlib backend (Qt5Agg → QtAgg)
- Refactored to MVC architecture
- Modernized Python code with dataclasses
- Corrected PDFgetX3 installation instructions

### Fixed
- setup.py dependency handling in isolated builds
- File I/O error handling
- Configuration persistence

---

## 🤖 Powered by Google Gemini Antigravity

This entire v2.0 release was developed through collaboration with **Google Gemini Antigravity**, demonstrating the power of AI-assisted software development.

**Key AI Contributions**:
- Complete PyQt5 → PyQt6 migration
- Lorch algorithm research and implementation
- Code refactoring to MVC architecture
- Bilingual documentation generation
- GitHub deployment automation

Learn more: https://deepmind.google/technologies/gemini/

---

## 🙏 Acknowledgments

- Original PDFgetX3 GUI by Kenneth P. Marshall
- PDFgetX3 by Simon Billinge and Pavol Juhás
- Optimization powered by Google Gemini Antigravity

---

## 📞 Support

- **Issues**: https://github.com/tianxiangchen1993/pdfgetx3gui/issues
- **Documentation**: https://www.diffpy.org/products/pdfgetx.html
- **Original Project**: https://github.com/msujas/pdfgetx3_gui

---

## ⚠️ Important Notes

1. **PDFgetX3 License Required**: You must obtain a free academic license from Columbia University before using this software for PDF calculations.

2. **Python Version**: Requires Python 3.8 or higher

3. **Dependencies**: 
   - PyQt6 >= 6.0.0
   - matplotlib >= 3.5.0
   - numpy >= 1.19.0
   - scipy >= 1.5.0

4. **Lorch Modification**: While useful for reducing ripples, the Lorch function slightly broadens peaks. Use with caution for quantitative analysis.

---

Enjoy PDFgetX3 GUI v2.0! 🚀
