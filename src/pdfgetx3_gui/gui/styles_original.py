"""
Modern stylesheet for PDFgetX3 GUI.

Provides a clean, modern look with proper contrast and spacing.
"""


MODERN_STYLE = """
/* Global Font */
* {
    font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
    font-size: 9pt;
}

/* Main Window */
QMainWindow {
    background-color: #f5f5f5;
}

/* Tab Widget */
QTabWidget::pane {
    border: 1px solid #ddd;
    background: white;
    border-radius: 4px;
}

QTabBar::tab {
    background: #e0e0e0;
    color: #333;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    font-weight: 500;
}

QTabBar::tab:selected {
    background: white;
    color: #2196F3;
    border-bottom: 2px solid #2196F3;
}

QTabBar::tab:hover:!selected {
    background: #eeeeee;
}

/* Buttons */
QPushButton {
    background-color: #2196F3;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    font-weight: 500;
    min-width: 80px;
}

QPushButton:hover {
    background-color: #1976D2;
}

QPushButton:pressed {
    background-color: #0D47A1;
}

QPushButton:disabled {
    background-color: #BDBDBD;
    color: #757575;
}

QPushButton#calculate_btn {
    background-color: #4CAF50;
    font-size: 11pt;
}

QPushButton#calculate_btn:hover {
    background-color: #45a049;
}

QPushButton#save_btn {
    background-color: #FF9800;
}

QPushButton#save_btn:hover {
    background-color: #F57C00;
}

/* Input Fields */
QLineEdit {
    padding: 6px;
    border: 1px solid #ccc;
    border-radius: 3px;
    background: white;
    selection-background-color: #2196F3;
}

QLineEdit:focus {
    border: 1px solid #2196F3;
}

QLineEdit:disabled {
    background-color: #f5f5f5;
    color: #999;
}

/* Spin Boxes */
QDoubleSpinBox, QSpinBox {
    padding: 6px 4px;
    border: 1px solid #ccc;
    border-radius: 3px;
    background: white;
    min-width: 100px;
}

QDoubleSpinBox:focus, QSpinBox:focus {
    border: 1px solid #2196F3;
}

/* Group Boxes */
QGroupBox {
    font-weight: 600;
    border: 1px solid #ddd;
    border-radius: 4px;
    margin-top: 12px;
    padding: 12px;
    background: white;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    padding: 0 8px;
    color: #2196F3;
}

/* Labels */
QLabel {
    color: #333;
    padding: 2px;
}

/* Form Layout Labels */
QFormLayout QLabel {
    min-width: 120px;
    padding-right: 8px;
}

QLabel[class="header"] {
    font-size: 12pt;
    font-weight: 600;
    color: #2196F3;
}

/* List Widget */
QListWidget {
    border: 1px solid #ddd;
    border-radius: 3px;
    background: white;
    padding: 4px;
    outline: none;
}

QListWidget::item {
    padding: 6px;
    border-radius: 2px;
}

QListWidget::item:hover {
    background: #e3f2fd;
}

QListWidget::item:selected {
    background: #2196F3;
    color: white;
}

/* Scroll Bars */
QScrollBar:vertical {
    border: none;
    background: #f0f0f0;
    width: 10px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #ccc;
    border-radius: 5px;
    min-height: 20px;
}

QScrollBar::handle:vertical:hover {
    background: #999;
}

QScrollBar:horizontal {
    border: none;
    background: #f0f0f0;
    height: 10px;
    margin: 0;
}

QScrollBar::handle:horizontal {
    background: #ccc;
    border-radius: 5px;
    min-width: 20px;
}

QScrollBar::handle:horizontal:hover {
    background: #999;
}

/* Status Bar */
QStatusBar {
    background: #fafafa;
    border-top: 1px solid #ddd;
    color: #666;
}

QStatusBar::item {
    border: none;
}

/* Menu Bar */
QMenuBar {
    background: white;
    border-bottom: 1px solid #ddd;
    padding: 2px;
}

QMenuBar::item {
    padding: 6px 12px;
    background: transparent;
}

QMenuBar::item:selected {
    background: #e3f2fd;
    color: #2196F3;
}

QMenu {
    background: white;
    border: 1px solid #ddd;
    padding: 4px;
}

QMenu::item {
    padding: 6px 24px;
    border-radius: 2px;
}

QMenu::item:selected {
    background: #e3f2fd;
    color: #2196F3;
}

/* Toolbar */
QToolBar {
    background: white;
    border-bottom: 1px solid #ddd;
    spacing: 4px;
    padding: 4px;
}

QToolButton {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 3px;
    padding: 6px;
    margin: 2px;
}

QToolButton:hover {
    background: #e3f2fd;
    border: 1px solid #2196F3;
}

QToolButton:pressed {
    background: #BBDEFB;
}

/* Checkboxes */
QCheckBox {
    spacing: 6px;
}

QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 2px solid #999;
}

QCheckBox::indicator:checked {
    background: #2196F3;
    border: 2px solid #2196F3;
    image: url(none);  /* Would add checkmark icon here */
}

QCheckBox::indicator:hover {
    border: 2px solid #2196F3;
}

/* Radio Buttons */
QRadioButton {
    spacing: 6px;
}

QRadioButton::indicator {
    width: 18px;
    height: 18px;
    border-radius: 9px;
    border: 2px solid #999;
}

QRadioButton::indicator:checked {
    background: #2196F3;
    border: 2px solid #2196F3;
}

QRadioButton::indicator:hover {
    border: 2px solid #2196F3;
}

/* Splitter */
QSplitter::handle {
    background: #ddd;
}

QSplitter::handle:hover {
    background: #2196F3;
}

QSplitter::handle:horizontal {
    width: 2px;
}

QSplitter::handle:vertical {
    height: 2px;
}

/* Progress Bar (for future use) */
QProgressBar {
    border: 1px solid #ddd;
    border-radius: 4px;
    text-align: center;
    background: white;
}

QProgressBar::chunk {
    background-color: #2196F3;
    border-radius: 3px;
}

/* Tooltip */
QToolTip {
    background: #333;
    color: white;
    border: 1px solid #333;
    padding: 4px 8px;
    border-radius: 2px;
}
"""


DARK_STYLE = """
/* Dark Theme */
QMainWindow {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

QWidget {
    background-color: #1e1e1e;
    color: #e0e0e0;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #3d3d3d;
    background: #2d2d2d;
}

QTabBar::tab {
    background: #3d3d3d;
    color: #e0e0e0;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background: #2d2d2d;
    color: #64B5F6;
    border-bottom: 2px solid #64B5F6;
}

/* Buttons */
QPushButton {
    background-color: #0D47A1;
    color: #e0e0e0;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}

QPushButton:hover {
    background-color: #1976D2;
}

/* Input fields */
QLineEdit, QDoubleSpinBox, QSpinBox {
    background: #2d2d2d;
    border: 1px solid #3d3d3d;
    color: #e0e0e0;
    padding: 6px;
    border-radius: 3px;
}

QLineEdit:focus, QDoubleSpinBox:focus, QSpinBox:focus {
    border: 1px solid #64B5F6;
}

/* Group boxes */
QGroupBox {
    border: 1px solid #3d3d3d;
    background: #2d2d2d;
    color: #e0e0e0;
    margin-top: 12px;
    padding: 12px;
}

QGroupBox::title {
    color: #64B5F6;
}

/* Lists */
QListWidget {
    background: #2d2d2d;
    border: 1px solid #3d3d3d;
    color: #e0e0e0;
}

QListWidget::item:selected {
    background: #0D47A1;
}

/* Menu */
QMenuBar {
    background: #2d2d2d;
    border-bottom: 1px solid #3d3d3d;
}

QMenuBar::item:selected {
    background: #3d3d3d;
    color: #64B5F6;
}

QMenu {
   background: #2d2d2d;
    border: 1px solid #3d3d3d;
}

QMenu::item:selected {
    background: #3d3d3d;
    color: #64B5F6;
}

/* Status bar */
QStatusBar {
    background: #2d2d2d;
    border-top: 1px solid #3d3d3d;
    color: #e0e0e0;
}
"""
