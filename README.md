# PDFgetX3 GUI v2.0 - Modern PyQt6 Implementation

English | [简体中文](README_CN.md)

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PyQt6](https://img.shields.io/badge/PyQt-6.0+-green.svg)](https://www.riverbankcomputing.com/software/pyqt/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**A modern, fully-functional GUI for PDFgetX3** with complete PyQt6 migration, enhanced UI/UX, and robust PDF analysis features.

## 🎯 What's New in v2.0.1 (December 2024)

### 🔧 Critical Fixes
- ✅ **PyQt6 Compatibility**: Fixed all PyQt5→PyQt6 enum access issues (QAbstractItemView, QFormLayout, QDialogButtonBox, QFileDialog)
- ✅ **Lorch Algorithm Bug**: **CRITICAL FIX** - Lorch-corrected and uncorrected files now save different data correctly
- ✅ **Plot Display**: Added missing x-axis labels for I(Q) and S(Q) plots
- ✅ **Module Migration**: Moved QShortcut from QtWidgets to QtGui for Qt6 compatibility

### ✨ New Features
- 🎨 **Enhanced SpinBox UI**: Color-coded up/down buttons (green ↑ increase, red ↓ decrease) with tooltips
- 📁 **Smart File Naming**: New convention `{sample}_qmax{value}.lorch.{extension}` for better data organization
- 📊 **Lorch Data Export**: Separate export for original and Lorch-corrected F(Q) and G(r) data

## 📋 Requirements

- Python 3.8 or higher
- **PyQt6** >= 6.0.0 (Qt 6 framework)
- PDFgetX3 ([diffpy.pdfgetx](https://www.diffpy.org/products/pdfgetx.html))
- matplotlib >= 3.5.0 (with Qt6 backend support)
- NumPy >= 1.19.0
- SciPy >= 1.5.0

## 🚀 Quick Start

### 1. Install PDFgetX3 (Required)

PDFgetX3 requires a free academic license from Columbia University:

1. Visit: [https://columbia.resoluteinnovation.com/technologies/M11-120](https://columbia.resoluteinnovation.com/technologies/M11-120)
2. Sign up for academic license (free for research use)
3. Download and install following the provided instructions

**Documentation**: [https://www.diffpy.org/products/pdfgetx.html](https://www.diffpy.org/products/pdfgetx.html)

### 2. Install GUI

```bash
# Clone repository
git clone https://github.com/tianxiangchen1993/pdfgetx3gui.git
cd pdfgetx3gui

# Install dependencies
pip install -r requirements.txt

# Install package
pip install -e .
```

### 3. Launch

```bash
pdfgetx3gui-v2
# or simply
pdfgetx3gui
```

## 💻 Usage Guide

### Basic Workflow

1. **Load Data**: Select your diffraction data file (.xy, .chi, or 2θ format)
2. **Set Parameters**: 
   - Qmax(inst): Instrument Q maximum
   - Qmin/Qmax: Analysis range
   - Composition: Sample chemical formula
3. **Optional**: Enable Lorch modification to reduce PDF termination ripples
4. **Calculate**: Press F5 or click Calculate button
5. **Review**: Check I(Q), S(Q), F(Q), and G(r) plots
6. **Save**: Export results with smart file naming

### File Naming Convention

**Without Lorch**:
- `sample_qmax20.iq`, `.sq`, `.fq`, `.gr`

**With Lorch enabled**:
- `sample_qmax20.fq` - Original F(Q)
- `sample_qmax20.gr` - Original G(r)
- `sample_qmax20.lorch.fq` - Lorch-corrected F(Q)
- `sample_qmax20.lorch.gr` - Lorch-corrected G(r)

### Lorch Modification

The Lorch function `M(Q) = sinc(Q/Qmax)` smoothly damps F(Q) near Qmax, reducing spurious oscillations in G(r):

- **Enable**: Check "Apply Lorch Modification" in Parameters tab
- **Effect**: Reduces termination ripples while preserving peak positions
- **Output**: Both original and Lorch-corrected data can be saved separately

## ✨ Key Features

### Data Input
- Multiple format support (Q-space, 2θ-space)
- Background file subtraction
- File history and quick access
- Smart parameter validation

### Parameter Control
- Color-coded SpinBox controls with visual feedback
- Real-time validation
- Parameter presets support
- Comprehensive tooltips (bilingual)

### Data Processing
- Composition-based corrections
- Background scaling
- Polynomial termination ripple correction
- **Lorch modification** for PDF quality improvement

### Visualization
- Real-time plot updates
- Multiple simultaneous plots (I(Q), S(Q), F(Q), G(r))
- Modern matplotlib styling
- Interactive zoom and pan

### Data Export
- Smart file naming with qmax values
- Separate original and Lorch-corrected outputs
- Configuration file (.cfg) export
- Batch processing support

## 🏗️ Architecture

```
pdfgetx3gui/
├── src/pdfgetx3_gui/
│   ├── config/          # Settings management
│   │   └── settings.py  # PDFParameters dataclass
│   ├── core/            # Calculation engine
│   │   └── calculator.py # PDFCalculator with Lorch support
│   ├── gui/             # User interface
│   │   ├── main_window.py # Main application window
│   │   └── styles.py    # Modern UI styling
│   ├── plotting/        # Visualization
│   │   └── plot_widget.py # Enhanced matplotlib plots
│   └── utils/           # Logging and utilities
├── tests/               # Test suite
├── examples/            # Example data and outputs
└── docs/                # Documentation
```

## 🔧 Development

### Run from Source

```bash
cd pdfgetx3gui
python -m pdfgetx3_gui.main
```

### Code Quality

```bash
# Type checking
mypy src/pdfgetx3_gui

# Code formatting  
black src/pdfgetx3_gui

# Run tests
pytest tests/
```

## 📊 PyQt6 Migration Details

| Component | PyQt5 API | PyQt6 API (Fixed) |
|-----------|-----------|-------------------|
| Selection Mode | `QAbstractItemView.ExtendedSelection` | `QAbstractItemView.SelectionMode.ExtendedSelection` |
| Field Growth | `QFormLayout.ExpandingFieldsGrow` | `QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow` |
| Dialog Buttons | `QDialogButtonBox.Ok` | `QDialogButtonBox.StandardButton.Ok` |
| File Dialog | `QFileDialog.ShowDirsOnly` | `QFileDialog.Option.ShowDirsOnly` |
| Shortcuts | `QtWidgets.QShortcut` | `QtGui.QShortcut` |

## 🐛 Known Issues & Fixes

### Fixed in v2.0.1
- ✅ Lorch-corrected files were identical to uncorrected files (CRITICAL)
- ✅ Missing x-axis labels on I(Q) and S(Q) plots
- ✅ PyQt6 enum AttributeErrors on startup
- ✅ QShortcut module import error

### Current Limitations
- Drag & drop file support (planned)
- Plot export to image files (planned)
- Multiple configuration profiles (planned)

## 🤝 Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🙏 Acknowledgments

- **Original PDFgetX3 GUI**: Kenneth P. Marshall
- **PDFgetX3 Algorithm**: Simon Billinge and Pavol Juhás (Columbia University)
- **Development**: Powered by [Google Gemini](https://deepmind.google/technologies/gemini/)

### 🤖 AI-Assisted Development

This project demonstrates modern AI-assisted software engineering. The v2.0 optimization was accomplished through collaboration with **Google Gemini 2.0**, featuring:

- Complete PyQt5 → PyQt6 migration with API compatibility fixes
- Implementation of Lorch modification algorithm
- Modern Python architecture (MVC pattern, type hints, dataclasses)
- Comprehensive bilingual documentation
- Critical bug detection and resolution

**Production-ready code, delivered at unprecedented speed.**

## 📞 Support

- **Repository**: [https://github.com/tianxiangchen1993/pdfgetx3gui](https://github.com/tianxiangchen1993/pdfgetx3gui)
- **Issues**: [GitHub Issues](https://github.com/tianxiangchen1993/pdfgetx3gui/issues)
- **PDFgetX3 Docs**: [https://www.diffpy.org/products/pdfgetx.html](https://www.diffpy.org/products/pdfgetx.html)

## 🗺️ Roadmap

- [ ] Drag & drop file loading
- [ ] Plot export (PNG, SVG, PDF)
- [ ] Multiple dataset comparison
- [ ] Advanced fitting tools
- [ ] Configuration profiles management
- [ ] Plugin system for custom processing

---

**Last Updated**: December 2024 | **Version**: 2.0.1
