"""
Main window implementation.

Modern PyQt6 GUI with improved layout and organization.
"""

from PyQt6 import QtCore, QtWidgets, QtGui
from pathlib import Path
import logging
from typing import Optional

from ..config.settings import Settings, PDFParameters
from ..core.calculator import PDFCalculator
from ..utils.logger import get_logger
from ..utils.i18n import get_translator, tr, set_language

logger = get_logger(__name__)


class FreeNumberEdit(QtWidgets.QLineEdit):
    valueChanged = QtCore.pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self._decimals = 6
        self.textEdited.connect(self._emit_value_changed)

    def setRange(self, _minimum: float, _maximum: float) -> None:
        pass

    def setSingleStep(self, _step: float) -> None:
        pass

    def setDecimals(self, decimals: int) -> None:
        self._decimals = decimals

    def setSuffix(self, suffix: str) -> None:
        self.setPlaceholderText(suffix.strip())

    def setValue(self, value: float) -> None:
        self.setText(f"{float(value):.{self._decimals}f}".rstrip("0").rstrip("."))
        self.valueChanged.emit(float(value))

    def value(self) -> float:
        text = self.text().strip()
        if not text:
            raise ValueError("参数不能为空")
        try:
            return float(text)
        except ValueError as exc:
            raise ValueError(f"参数必须是数字：{text}") from exc

    def _emit_value_changed(self) -> None:
        try:
            value = self.value()
        except ValueError:
            return
        self.valueChanged.emit(value)


class MainWindow(QtWidgets.QMainWindow):
    """
    Main application window with improved design.
    
    Features:
    - Tab-based organization
    - Clear parameter grouping
    - Modern styling
    - Better error feedback
    - Real-time parameter updates
    """
    
    # Signals
    calculation_requested = QtCore.pyqtSignal(PDFParameters, str, str)
    
    def __init__(self):
        """Initialize the main window."""
        super().__init__()
        
        self.settings = Settings()
        self.calculator = PDFCalculator()
        self.current_results = None
        self.translator = get_translator()
        
        # Load saved settings
        self.settings.load()
        
        # Set language if saved in settings
        if hasattr(self.settings, 'language'):
            set_language(self.settings.language)
        
        self._setup_ui()
        self._apply_stylesheet()
        self._connect_signals()
        self._apply_settings()
        
        logger.info("Main window initialized")
    
    def _apply_stylesheet(self):
        """Apply modern stylesheet to the application."""
        from .styles import MODERN_STYLE
        self.setStyleSheet(MODERN_STYLE)
        
        # Set object names for custom styling
        self.calculate_btn.setObjectName("calculate_btn")
        self.save_btn.setObjectName("save_btn")
    
    def _setup_ui(self):
        """Setup the user interface."""
        self.setWindowTitle("PDFgetX3GUI V2.0")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Set window icon
        icon_path = Path(__file__).parent / "resources" / "icon.png"
        if icon_path.exists():
            self.setWindowIcon(QtGui.QIcon(str(icon_path)))
        
        # Central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(central_widget)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)
        
        # Create menu bar
        self._create_menu_bar()
        
        # Create toolbar
        self._create_toolbar()
        
        # Create main content area with splitter
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal)
        
        # Left panel: Parameters
        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel: Plot area
        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)
        
        # Set splitter sizes (30% left, 70% right)
        splitter.setSizes([400, 800])
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        logger.debug("UI setup completed")
    
    def _create_menu_bar(self):
        """Create menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu(tr('menu_file'))
        
        self.open_action = QtGui.QAction(tr('menu_open'), self)
        self.open_action.setShortcut("Ctrl+O")
        file_menu.addAction(self.open_action)
        
        self.open_bkg_action = QtGui.QAction(tr('menu_open_bkg'), self)
        self.open_bkg_action.setShortcut("Ctrl+B")
        file_menu.addAction(self.open_bkg_action)
        
        file_menu.addSeparator()
        
        self.save_action = QtGui.QAction(tr('menu_save'), self)
        self.save_action.setShortcut("Ctrl+S")
        file_menu.addAction(self.save_action)
        
        file_menu.addSeparator()
        
        exit_action = QtGui.QAction(tr('menu_exit'), self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Settings menu
        settings_menu = menubar.addMenu(tr('menu_settings'))
        
        self.pref_action = QtGui.QAction(tr('menu_preferences'), self)
        settings_menu.addAction(self.pref_action)
        
        # Help menu
        help_menu = menubar.addMenu(tr('menu_help'))
        
        self.about_action = QtGui.QAction(tr('menu_about'), self)
        help_menu.addAction(self.about_action)
    
    def _create_toolbar(self):
        """Create toolbar."""
        toolbar = self.addToolBar("Main")
        toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonTextUnderIcon)
        
        # Open file
        open_tb_action = QtGui.QAction(tr('toolbar_open'), self)
        open_tb_action.setToolTip("Open data file (Ctrl+O)")
        open_tb_action.triggered.connect(lambda: self.open_action.trigger())
        toolbar.addAction(open_tb_action)
        
        toolbar.addSeparator()
        
        # Calculate
        self.calc_action = QtGui.QAction(tr('toolbar_calculate'), self)
        self.calc_action.setToolTip("Run PDF calculation (F5)")
        toolbar.addAction(self.calc_action)
        
        # Stop
        self.stop_action = QtGui.QAction(tr('toolbar_stop'), self)
        self.stop_action.setToolTip("Stop calculation")
        self.stop_action.setEnabled(False)
        toolbar.addAction(self.stop_action)
        
        toolbar.addSeparator()
        
        # Save
        save_tb_action = QtGui.QAction(tr('toolbar_save'), self)
        save_tb_action.setToolTip("Save results (Ctrl+S)")
        save_tb_action.triggered.connect(lambda: self.save_action.trigger())
        toolbar.addAction(save_tb_action)
    
    def _create_left_panel(self) -> QtWidgets.QWidget:
        """Create left parameter panel."""
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        #Tab widget for different parameter groups
        self.param_tabs = QtWidgets.QTabWidget()
        
        # Files & Processing tab
        files_tab = self._create_files_tab()
        self.param_tabs.addTab(files_tab, tr('tab_files_processing'))
        
        # Parameters tab (now includes Display)
        params_tab = self._create_parameters_tab()
        self.param_tabs.addTab(params_tab, tr('tab_parameters'))
        

        layout.addWidget(self.param_tabs)
        
        # Action buttons at bottom
        button_layout = QtWidgets.QHBoxLayout()
        
        self.calculate_btn = QtWidgets.QPushButton(tr('button_calculate'))
        self.calculate_btn.setMinimumHeight(40)
        button_layout.addWidget(self.calculate_btn)
        
        self.save_btn = QtWidgets.QPushButton(tr('button_save_results'))
        self.save_btn.setMinimumHeight(40)
        button_layout.addWidget(self.save_btn)
        
        layout.addLayout(button_layout)
        
        return panel
    
    def _create_files_tab(self) -> QtWidgets.QWidget:
        """Create files and processing tab."""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(tab)
        layout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        
        # === Data Format (FIRST) ===
        format_section = QtWidgets.QLabel("<b>data_format</b>")
        layout.addRow(format_section)
        
        format_layout = QtWidgets.QHBoxLayout()
        self.format_q = QtWidgets.QRadioButton(tr('Q'))
        format_layout.addWidget(self.format_q)
        
        self.format_2theta = QtWidgets.QRadioButton(tr('2theta'))
        self.format_2theta.setChecked(True)
        format_layout.addWidget(self.format_2theta)
        format_layout.addStretch()
        
        layout.addRow(tr('data_format'), format_layout)
        
        self.wavelength_spin = FreeNumberEdit()
        self.wavelength_spin.setRange(0.01, 10.0)
        self.wavelength_spin.setValue(0.270793)
        self.wavelength_spin.setSingleStep(0.001)
        self.wavelength_spin.setDecimals(6)
        self.wavelength_spin.setSuffix(" Å")
        self.wavelength_spin.setEnabled(True)
        self.wavelength_spin.setMinimumWidth(120)
        self.wavelength_spin.setToolTip("波长 / Wavelength")
        layout.addRow(tr('wavelength'), self.wavelength_spin)
        
        self.format_2theta.toggled.connect(self.wavelength_spin.setEnabled)
        
        # Composition (SECOND)
        self.composition_edit = QtWidgets.QLineEdit("LaB6")
        self.composition_edit.setToolTip("Chemical composition (e.g., LaB6, Si, SiO2)")
        self.composition_edit.setMinimumWidth(150)
        layout.addRow(tr('label_composition'), self.composition_edit)
        
        layout.addRow(QtWidgets.QLabel(""))  # Spacer
        
        # === Data Files ===
        file_section = QtWidgets.QLabel(f"<b>{tr('data_files')}</b>")
        layout.addRow(file_section)
        
        data_layout = QtWidgets.QHBoxLayout()
        self.data_file_edit = QtWidgets.QLineEdit()
        self.data_file_edit.setPlaceholderText(tr('placeholder_data_file'))
        data_layout.addWidget(self.data_file_edit)
        
        browse_data_btn = QtWidgets.QPushButton(tr('button_browse'))
        browse_data_btn.setMaximumWidth(80)
        data_layout.addWidget(browse_data_btn)
        
        layout.addRow(tr('label_data_file'), data_layout)
        
        bkg_layout = QtWidgets.QHBoxLayout()
        self.bkg_file_edit = QtWidgets.QLineEdit()
        self.bkg_file_edit.setPlaceholderText(tr('placeholder_bkg_file'))
        bkg_layout.addWidget(self.bkg_file_edit)
        
        browse_bkg_btn = QtWidgets.QPushButton(tr('button_browse'))
        browse_bkg_btn.setMaximumWidth(80)
        bkg_layout.addWidget(browse_bkg_btn)
        
        layout.addRow(tr('label_background'), bkg_layout)
        
        # Connect browse buttons
        browse_data_btn.clicked.connect(lambda: self.open_action.trigger())
        browse_bkg_btn.clicked.connect(lambda: self.open_bkg_action.trigger())
        
        layout.addRow(QtWidgets.QLabel(""))  # Spacer
        
        # === Resampling ===
        resampling_section = QtWidgets.QLabel(f"<b>{tr('Resampling')}</b>")
        layout.addRow(resampling_section)
        
        resampling_layout = QtWidgets.QHBoxLayout()
        self.rebin_none = QtWidgets.QRadioButton(tr('Rebin None'))
        self.rebin_none.setChecked(True)
        resampling_layout.addWidget(self.rebin_none)
        
        self.rebin_linear = QtWidgets.QRadioButton(tr('Rebin Linear'))
        resampling_layout.addWidget(self.rebin_linear)
        
        self.rebin_exp = QtWidgets.QRadioButton(tr('Rebin_exp'))
        resampling_layout.addWidget(self.rebin_exp)
        resampling_layout.addStretch()
        
        layout.addRow(tr('resampling'), resampling_layout)
        
        layout.addRow(QtWidgets.QLabel(""))  # Spacer
        
        # === Recent Files ===
        recent_section = QtWidgets.QLabel(f"<b>{tr('section_recent_files')}</b>")
        layout.addRow(recent_section)
        
        self.current_files_list = QtWidgets.QListWidget()
        self.current_files_list.setMaximumHeight(150)
        self.current_files_list.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        layout.addRow(self.current_files_list)
        
        # File management buttons
        file_mgmt_layout = QtWidgets.QHBoxLayout()
        
        add_file_btn = QtWidgets.QPushButton(tr('button_add_files'))
        add_file_btn.clicked.connect(self._open_file)
        add_file_btn.setMinimumWidth(120)
        file_mgmt_layout.addWidget(add_file_btn)
        
        remove_file_btn = QtWidgets.QPushButton(tr('button_remove_selected'))
        remove_file_btn.clicked.connect(self._remove_selected_files)
        remove_file_btn.setMinimumWidth(160)
        file_mgmt_layout.addWidget(remove_file_btn)
        
        clear_all_btn = QtWidgets.QPushButton(tr('button_clear_all'))
        clear_all_btn.clicked.connect(self._clear_all_files)
        clear_all_btn.setMinimumWidth(120)
        file_mgmt_layout.addWidget(clear_all_btn)
        
        layout.addRow("", file_mgmt_layout)
        
        return tab
    
    def _create_parameters_tab(self) -> QtWidgets.QWidget:
        """Create parameters tab."""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QFormLayout(tab)
        layout.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        
        # === Processing ===
        processing_section = QtWidgets.QLabel(f"<b>{tr('Processing')}</b>")
        layout.addRow(processing_section)
        
        self.bkgscale_spin = FreeNumberEdit()
        self.bkgscale_spin.setRange(0.0, 10.0)
        self.bkgscale_spin.setValue(1.0)
        self.bkgscale_spin.setSingleStep(0.1)
        self.bkgscale_spin.setDecimals(3)
        self.bkgscale_spin.setMinimumWidth(120)
        self.bkgscale_spin.setToolTip("背景缩放因子 / Background scaling factor")
        layout.addRow(tr('bkg_scale'), self.bkgscale_spin)
        
        self.rpoly_spin = FreeNumberEdit()
        self.rpoly_spin.setRange(0.0, 3.0)
        self.rpoly_spin.setValue(1.0)
        self.rpoly_spin.setSingleStep(0.1)
        self.rpoly_spin.setDecimals(2)
        self.rpoly_spin.setMinimumWidth(120)
        self.rpoly_spin.setToolTip("PDF截断波纹修正多项式参数")
        layout.addRow(tr('rpoly'), self.rpoly_spin)
        
        # Lorch modification checkbox
        self.lorch_check = QtWidgets.QCheckBox("Apply Lorch Modification / 应用Lorch修正")
        self.lorch_check.setToolTip(
            "Apply Lorch modification to reduce PDF termination ripples.\n"
            "This smoothly damps F(Q) near Qmax, reducing spurious oscillations in G(r).\n"
            "应用 Lorch 修正以减少 PDF 截断振铃效应。\n"
            "在接近 Qmax 处平滑衰减 F(Q)，减少 G(r) 中的虚假振荡。"
        )
        layout.addRow("", self.lorch_check)
        
        layout.addRow(QtWidgets.QLabel(""))  # Spacer
        
        # === Q-space ===
        q_section = QtWidgets.QLabel(f"<b>{tr('group_q_params')}</b>")
        layout.addRow(q_section)
        
        # Qmax(inst) first
        self.qmaxinst_spin = FreeNumberEdit()
        self.qmaxinst_spin.setRange(1.0, 100.0)
        self.qmaxinst_spin.setValue(23.0)
        self.qmaxinst_spin.setSingleStep(0.1)
        self.qmaxinst_spin.setDecimals(2)
        self.qmaxinst_spin.setSuffix(" Å⁻¹")
        self.qmaxinst_spin.setMinimumWidth(120)
        self.qmaxinst_spin.setToolTip("仪器Q最大值 / Instrument Q max")
        layout.addRow(tr('label_qmax_inst'), self.qmaxinst_spin)
        
        # Then qmin
        self.qmin_spin = FreeNumberEdit()
        self.qmin_spin.setRange(0.01, 100.0)
        self.qmin_spin.setValue(1.0)
        self.qmin_spin.setSingleStep(0.1)
        self.qmin_spin.setDecimals(2)
        self.qmin_spin.setSuffix(" Å⁻¹")
        self.qmin_spin.setMinimumWidth(120)
        self.qmin_spin.setToolTip("Q最小值 / Q minimum")
        layout.addRow(tr('label_qmin'), self.qmin_spin)
        
        # Then qmax
        self.qmax_spin = FreeNumberEdit()
        self.qmax_spin.setRange(1.0, 100.0)
        self.qmax_spin.setValue(23.0)
        self.qmax_spin.setSingleStep(0.1)
        self.qmax_spin.setDecimals(2)
        self.qmax_spin.setSuffix(" Å⁻¹")
        self.qmax_spin.setMinimumWidth(120)
        self.qmax_spin.setToolTip("Q最大值 / Q maximum")
        layout.addRow(tr('label_qmax'), self.qmax_spin)
        
        layout.addRow(QtWidgets.QLabel(""))  # Spacer
        
        # === R-space ===
        r_section = QtWidgets.QLabel(f"<b>{tr('group_r_params')}</b>")
        layout.addRow(r_section)
        
        self.rmin_spin = FreeNumberEdit()
        self.rmin_spin.setRange(0.01, 100.0)
        self.rmin_spin.setValue(0.5)
        self.rmin_spin.setSingleStep(0.1)
        self.rmin_spin.setDecimals(2)
        self.rmin_spin.setSuffix(" Å")
        self.rmin_spin.setMinimumWidth(120)
        self.rmin_spin.setToolTip("R最小值 / R minimum")
        layout.addRow(tr('label_rmin'), self.rmin_spin)
        
        self.rmax_spin = FreeNumberEdit()
        self.rmax_spin.setRange(1.0, 10000.0)
        self.rmax_spin.setValue(30.0)
        self.rmax_spin.setSingleStep(1.0)
        self.rmax_spin.setDecimals(1)
        self.rmax_spin.setSuffix(" Å")
        self.rmax_spin.setMinimumWidth(120)
        self.rmax_spin.setToolTip("R最大值 / R maximum")
        layout.addRow(tr('label_rmax'), self.rmax_spin)
        
        self.rstep_spin = FreeNumberEdit()
        self.rstep_spin.setRange(0.001, 1.0)
        self.rstep_spin.setValue(0.01)
        self.rstep_spin.setSingleStep(0.001)
        self.rstep_spin.setDecimals(3)
        self.rstep_spin.setSuffix(" Å")
        self.rstep_spin.setMinimumWidth(120)
        self.rstep_spin.setToolTip("R步长 / R step")
        layout.addRow(tr('label_rstep'), self.rstep_spin)
        
        layout.addRow(QtWidgets.QLabel(""))  # Spacer
        
        # === Display Options ===
        display_section = QtWidgets.QLabel(f"<b>{tr('tab_display')}</b>")
        layout.addRow(display_section)
        
        self.show_iq_check = QtWidgets.QCheckBox(tr('check_plot_iq'))
        layout.addRow("", self.show_iq_check)
        
        self.show_sq_check = QtWidgets.QCheckBox(tr('check_plot_sq'))
        layout.addRow("", self.show_sq_check)
        
        self.show_fq_check = QtWidgets.QCheckBox(tr('check_plot_fq'))
        layout.addRow("", self.show_fq_check)
        
        self.show_gr_check = QtWidgets.QCheckBox(tr('check_plot_gr'))
        self.show_gr_check.setChecked(True)
        layout.addRow("", self.show_gr_check)
        
        self.reset_axis_check = QtWidgets.QCheckBox(tr('check_reset_axes'))
        self.reset_axis_check.setChecked(True)
        layout.addRow("", self.reset_axis_check)
        
        return tab
    
    def _create_display_tab(self) -> QtWidgets.QWidget:
        """Create display tab."""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        
        # Plot selection group
        plot_group = QtWidgets.QGroupBox(tr('group_plots'))
        plot_layout = QtWidgets.QVBoxLayout()
        
        self.show_iq_check = QtWidgets.QCheckBox(tr('check_plot_iq'))
        plot_layout.addWidget(self.show_iq_check)
        
        self.show_sq_check = QtWidgets.QCheckBox(tr('check_plot_sq'))
        plot_layout.addWidget(self.show_sq_check)
        
        self.show_fq_check = QtWidgets.QCheckBox(tr('check_plot_fq'))
        plot_layout.addWidget(self.show_fq_check)
        
        self.show_gr_check = QtWidgets.QCheckBox(tr('check_plot_gr'))
        self.show_gr_check.setChecked(True)
        plot_layout.addWidget(self.show_gr_check)
        
        plot_group.setLayout(plot_layout)
        layout.addWidget(plot_group)
        
        # Options
        options_group = QtWidgets.QGroupBox(tr('group_options'))
        options_layout = QtWidgets.QVBoxLayout()
        
        self.reset_axis_check = QtWidgets.QCheckBox(tr('check_reset_axes'))
        self.reset_axis_check.setChecked(True)
        options_layout.addWidget(self.reset_axis_check)
        
        options_group.setLayout(options_layout)
        layout.addWidget(options_group)
        
        layout.addStretch()
        
        return tab
    
    def _create_right_panel(self) -> QtWidgets.QWidget:
        """Create right plot panel."""
        from ..plotting import PlotWidget
        
        panel = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Add matplotlib plot widget
        self.plot_widget = PlotWidget()
        layout.addWidget(self.plot_widget)
        
        return panel
    
    def _connect_signals(self):
        """Connect UI signals to handlers."""
        # File menu/toolbar actions
        self.open_action.triggered.connect(self._open_file)
        self.open_bkg_action.triggered.connect(self._open_background_file)
        self.save_action.triggered.connect(self._save_results)
        
        # Settings menu actions
        self.pref_action.triggered.connect(self._show_preferences)
        
        # Help menu actions
        self.about_action.triggered.connect(self._show_about)
        
        # Toolbar calculate action
        self.calc_action.triggered.connect(self._run_calculation)
        
        # Buttons
        self.calculate_btn.clicked.connect(self._run_calculation)
        self.save_btn.clicked.connect(self._save_results)
        
        # Current files - click to select for processing
        self.current_files_list.itemClicked.connect(self._on_current_file_clicked)
        
        # F5 shortcut
        self.calc_shortcut = QtGui.QShortcut(QtGui.QKeySequence("F5"), self)
        self.calc_shortcut.activated.connect(self._run_calculation)
        
        # Auto-update signals
        self._connect_auto_update_signals()
        
        logger.debug("Signals connected")
    
    def _connect_auto_update_signals(self):
        """Connect parameter change signals for auto-update."""
        # Q-space parameters
        self.qmin_spin.valueChanged.connect(self._on_parameter_changed)
        self.qmax_spin.valueChanged.connect(self._on_parameter_changed)
        self.qmaxinst_spin.valueChanged.connect(self._on_parameter_changed)
        
        # R-space parameters
        self.rmin_spin.valueChanged.connect(self._on_parameter_changed)
        self.rmax_spin.valueChanged.connect(self._on_parameter_changed)
        self.rstep_spin.valueChanged.connect(self._on_parameter_changed)
        
        # Processing parameters
        self.bkgscale_spin.valueChanged.connect(self._on_parameter_changed)
        self.rpoly_spin.valueChanged.connect(self._on_parameter_changed)
        self.lorch_check.stateChanged.connect(self._on_parameter_changed)
        
        # Display options
        self.show_iq_check.stateChanged.connect(self._on_display_changed)
        self.show_sq_check.stateChanged.connect(self._on_display_changed)
        self.show_fq_check.stateChanged.connect(self._on_display_changed)
        self.show_gr_check.stateChanged.connect(self._on_display_changed)
        
        logger.debug("Auto-update signals connected")
    
    def _on_parameter_changed(self):
        """Handle parameter change - auto recalculate if data exists."""
        if hasattr(self, 'current_results') and self.current_results is not None:
            if self.data_file_edit.text():
                logger.debug("Parameter changed, triggering auto-recalculation")
                self._run_calculation()
    
    def _on_display_changed(self):
        """Handle display option change - update plot if results exist."""
        if hasattr(self, 'current_results') and self.current_results is not None:
            logger.debug("Display option changed, updating plot")
            params = self._get_parameters()
            self.plot_widget.plot_results(
                self.current_results,
                show_iq=params.show_iq,
                show_sq=params.show_sq,
                show_fq=params.show_fq,
                show_gr=params.show_gr,
                reset_axes=params.reset_axis_on_update
            )
    
    def _apply_settings(self):
        """Apply loaded settings to UI controls."""
        params = self.settings.parameters
        
        # Set values from params
        self.composition_edit.setText(params.composition)
        self.qmin_spin.setValue(params.qmin)
        self.qmax_spin.setValue(params.qmax)
        self.qmaxinst_spin.setValue(params.qmaxinst)
        self.rmin_spin.setValue(params.rmin)
        self.rmax_spin.setValue(params.rmax)
        self.rstep_spin.setValue(params.rstep)
        self.bkgscale_spin.setValue(params.bkgscale)
        self.rpoly_spin.setValue(params.rpoly)
        
        # Data format
        if params.dataformat == "QA":
            self.format_q.setChecked(True)
        else:
            self.format_2theta.setChecked(True)
        
        # Display options
        self.show_iq_check.setChecked(params.show_iq)
        self.show_sq_check.setChecked(params.show_sq)
        self.show_fq_check.setChecked(params.show_fq)
        self.show_gr_check.setChecked(params.show_gr)
        self.reset_axis_check.setChecked(params.reset_axis_on_update)
        
        # Lorch modification
        self.lorch_check.setChecked(params.lorch)
        
        logger.debug("Settings applied to UI")
    
    

    
    def _update_current_files_list(self):
        """Update current files list display."""
        self.current_files_list.clear()
        for filepath in self.settings.file_config.current_data_files:
            from pathlib import Path
            self.current_files_list.addItem(str(Path(filepath).name))
    
    def _remove_selected_files(self):
        """Remove selected files from current files list."""
        selected_items = self.current_files_list.selectedItems()
        if not selected_items:
            return
        
        from pathlib import Path
        # Get filenames to remove
        names_to_remove = [item.text() for item in selected_items]
        
        # Remove from settings
        current_files = self.settings.file_config.current_data_files
        self.settings.file_config.current_data_files = [
            f for f in current_files 
            if Path(f).name not in names_to_remove
        ]
        self.settings.save()
        
        # Update display
        self._update_current_files_list()
        
        # Update data_file_edit if needed
        if self.settings.file_config.current_data_files:
            self.data_file_edit.setText(self.settings.file_config.current_data_files[0])
        else:
            self.data_file_edit.setText("")
        
        logger.info(f"Removed {len(names_to_remove)} file(s)")
    
    def _clear_all_files(self):
        """Clear all files from current files list."""
        self.settings.file_config.current_data_files = []
        self.settings.save()
        self.current_files_list.clear()
        self.data_file_edit.setText("")
        logger.info("Cleared all files")
    
    def _on_current_file_clicked(self, item):
        """Handle click on current file - set as active for processing."""
        from pathlib import Path
        filename = item.text()
        
        # Find full path
        for filepath in self.settings.file_config.current_data_files:
            if Path(filepath).name == filename:
                self.data_file_edit.setText(filepath)
                logger.info(f"Selected file: {filename}")
                break

    def _update_recent_files(self):

        """Update recent files list."""

        self.recent_files_list.clear()

        for filepath in self.settings.file_config.recent_files:

            from pathlib import Path

            self.recent_files_list.addItem(str(Path(filepath).name))

    def _get_parameters(self) -> PDFParameters:
        """Get current parameters from UI."""
        params = PDFParameters()
        
        # Basic parameters
        params.composition = self.composition_edit.text()
        params.qmin = self.qmin_spin.value()
        params.qmax = self.qmax_spin.value()
        params.qmaxinst = self.qmaxinst_spin.value()
        params.rmin = self.rmin_spin.value()
        params.rmax = self.rmax_spin.value()
        params.rstep = self.rstep_spin.value()
        params.bkgscale = self.bkgscale_spin.value()
        params.rpoly = self.rpoly_spin.value()
        
        # Data format
        params.dataformat = "QA" if self.format_q.isChecked() else "twotheta"
        params.wavelength = self.wavelength_spin.value()
        
        # Resampling
        if self.rebin_linear.isChecked():
            params.rebin_mode = "linear"
        elif self.rebin_exp.isChecked():
            params.rebin_mode = "exponential"
        else:
            params.rebin_mode = "none"
        
        # Lorch modification
        params.lorch = self.lorch_check.isChecked()
        
        # Display options
        params.show_iq = self.show_iq_check.isChecked()
        params.show_sq = self.show_sq_check.isChecked()
        params.show_fq = self.show_fq_check.isChecked()
        params.show_gr = self.show_gr_check.isChecked()
        params.reset_axis_on_update = self.reset_axis_check.isChecked()
        
        return params
    
    def _run_calculation(self):
        """Run PDF calculation (single or batch)."""
        from ..workers import CalculationWorker, MultiCalculationWorker
        
        try:
            params = self._get_parameters()
        except ValueError as exc:
            QtWidgets.QMessageBox.warning(self, "参数错误", str(exc))
            return
        bkg_file = self.bkg_file_edit.text() if self.bkg_file_edit.text() else None
        
        # Check for selected files in list
        selected_items = self.current_files_list.selectedItems()
        files_to_process = []
        
        if len(selected_items) > 1:
            # Multiple files selected
            from pathlib import Path
            selected_names = [item.text() for item in selected_items]
            
            # Find full paths
            for name in selected_names:
                for filepath in self.settings.file_config.current_data_files:
                    if Path(filepath).name == name:
                        files_to_process.append(filepath)
                        break
            logger.info(f"Selected {len(files_to_process)} files for batch processing")
            
        else:
            # Single file (from edit box)
            data_file = self.data_file_edit.text()
            if data_file:
                files_to_process = [data_file]
        
        if not files_to_process:
            QtWidgets.QMessageBox.warning(self, tr('dialog_no_data_file'), tr('dialog_select_file_first'))
            return
        
        if not any([params.show_iq, params.show_sq, params.show_fq, params.show_gr]):
            QtWidgets.QMessageBox.warning(self, tr('dialog_no_plots'), tr('dialog_select_plot'))
            return
        
        # Stop any existing calculation
        if hasattr(self, 'worker') and self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        
        # Create worker based on number of files
        if len(files_to_process) > 1:
            # Batch processing
            self.worker = MultiCalculationWorker(params, files_to_process, bkg_file)
            self.worker.finished.connect(self._on_multi_calculation_finished)
            msg = f"Calculating {len(files_to_process)} files..."
        else:
            # Single file processing
            self.worker = CalculationWorker(params, files_to_process[0], bkg_file)
            self.worker.finished.connect(self._on_calculation_finished)
            msg = tr('status_calculating')
            
        # Common signals
        self.worker.progress.connect(self._on_calculation_progress)
        self.worker.error.connect(self._on_calculation_error)
        
        # Update UI
        self.calc_action.setEnabled(False)
        self.calculate_btn.setEnabled(False)
        self.stop_action.setEnabled(True)
        try:
            self.stop_action.triggered.disconnect()
        except:
            pass
        self.stop_action.triggered.connect(self.worker.stop)
        
        # Start
        self.statusBar().showMessage(msg)
        self.worker.start()
        logger.info(msg)
    
    def _on_calculation_progress(self, percent: int):
        """Handle calculation progress."""
        self.statusBar().showMessage(f"Calculating... {percent}%")
    
    def _on_calculation_finished(self, results):
        """Handle calculation completion."""
        self.current_results = results
        
        # Update plot
        params = self._get_parameters()
        self.plot_widget.plot_results(
            results,
            show_iq=params.show_iq,
            show_sq=params.show_sq,
            show_fq=params.show_fq,
            show_gr=params.show_gr,
            reset_axes=params.reset_axis_on_update
        )
        
        # Update UI
        self.calc_action.setEnabled(True)
        self.calculate_btn.setEnabled(True)
        self.stop_action.setEnabled(False)
        
        self.statusBar().showMessage(tr('status_completed'), 5000)
        logger.info("Calculation completed")
    
    def _on_multi_calculation_finished(self, results_list):
        """Handle batch calculation completion."""
        self.current_results = results_list  # Store list of results
        
        # Update plot with all results
        params = self._get_parameters()
        self.plot_widget.plot_results(
            results_list,
            show_iq=params.show_iq,
            show_sq=params.show_sq,
            show_fq=params.show_fq,
            show_gr=params.show_gr,
            reset_axes=params.reset_axis_on_update
        )
        
        # Update UI
        self.calc_action.setEnabled(True)
        self.calculate_btn.setEnabled(True)
        self.stop_action.setEnabled(False)
        
        self.statusBar().showMessage(f"Batch calculation completed ({len(results_list)} files)", 5000)
        logger.info(f"Batch calculation completed for {len(results_list)} files")

    def _on_calculation_error(self, error_msg: str):
        """Handle calculation error."""
        self.calc_action.setEnabled(True)
        self.calculate_btn.setEnabled(True)
        self.stop_action.setEnabled(False)
        
        QtWidgets.QMessageBox.critical(
            self,
            tr('dialog_calc_error'),
            f"An error occurred during calculation:\n\n{error_msg}"
        )
        
        self.statusBar().showMessage(tr('status_failed'), 5000)
        logger.error(f"Calculation failed: {error_msg}")
    
    def _open_file(self):
        """Open data file(s) - supports multiple selection."""
        start_dir = self.settings.file_config.last_data_directory or ""
        
        file_paths, _ = QtWidgets.QFileDialog.getOpenFileNames(
            self,
            "Open Data File(s)",
            start_dir,
            "Data Files (*.xy *.xye *.dat *.txt);;All Files (*.*)"
        )
        
        if file_paths:
            from pathlib import Path
            self.settings.file_config.last_data_directory = str(Path(file_paths[0]).parent)
            self.settings.save()
            
            self.data_file_edit.setText(file_paths[0])
            self.settings.file_config.current_data_files = file_paths
            self.settings.save()
            
            # Update current files list
            self._update_current_files_list()
            
            logger.info(f"Loaded {len(file_paths)} data file(s)")
            logger.info(f"First file: {file_paths[0]}")
            logger.info(f"All files: {file_paths}")
            logger.info(f"Current data files saved: {self.settings.file_config.current_data_files}")
    
    def _open_background_file(self):
        """Open background file."""
        start_dir = self.settings.file_config.last_bkg_directory or ""
        
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Open Background File",
            start_dir,
            "Data Files (*.xy *.xye *.dat *.txt);;All Files (*.*)"
        )
        
        if file_path:
            from pathlib import Path
            self.bkg_file_edit.setText(file_path)
            self.settings.file_config.last_bkg_directory = str(Path(file_path).parent)
            self.settings.save()
            logger.info(f"Loaded background file: {file_path}")
    

    def _save_config_file(self, config_path, data_type):
        """Save processing parameters to config file."""
        params = self._get_parameters()
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(f"# PDFgetX3 Configuration for {data_type}\n")
            f.write(f"# Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n[pdfgetx3]\n")
            
            # Input files
            f.write(f"datafile = {self.data_file_edit.text()}\n")
            if self.bkg_file_edit.text():
                f.write(f"bgfile = {self.bkg_file_edit.text()}\n")
            
            # Data format
            f.write(f"\n# Data Format\n")
            f.write(f"dataformat = {params.dataformat}\n")
            if params.dataformat == 'twotheta':
                f.write(f"wavelength = {params.wavelength}\n")
            
            # Composition
            f.write(f"composition = {params.composition}\n")
            
            # Q-space parameters
            f.write(f"\n# Q-space Parameters\n")
            f.write(f"qmin = {params.qmin}\n")
            f.write(f"qmax = {params.qmax}\n")
            f.write(f"qmaxinst = {params.qmaxinst}\n")
            
            # R-space parameters
            f.write(f"\n# R-space Parameters\n")
            f.write(f"rmin = {params.rmin}\n")
            f.write(f"rmax = {params.rmax}\n")
            f.write(f"rstep = {params.rstep}\n")
            
            # Processing parameters
            f.write(f"\n# Processing Parameters\n")
            f.write(f"bkgscale = {params.bkgscale}\n")
            f.write(f"rpoly = {params.rpoly}\n")
            
            # Resampling
            if params.rebin_mode != 'none':
                f.write(f"\n# Resampling\n")
                f.write(f"mode = {params.rebin_mode}\n")

    def _save_results(self):
        """Save calculation results with user-selected options."""
        if not hasattr(self, 'current_results') or self.current_results is None:
            QtWidgets.QMessageBox.warning(
                self, 
                tr('dialog_no_results'), 
                tr('dialog_run_calc_first')
            )
            return
        
        # Create save options dialog
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Save Results")
        dialog.setMinimumWidth(300)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        
        # Title
        title = QtWidgets.QLabel("Select files to save:")
        title.setStyleSheet("font-weight: bold; font-size: 12pt;")
        layout.addWidget(title)
        
        # Checkboxes for each data type
        iq_check = QtWidgets.QCheckBox("I(Q) - Intensity")
        iq_check.setChecked(True)
        layout.addWidget(iq_check)
        
        sq_check = QtWidgets.QCheckBox("S(Q) - Structure Factor")
        sq_check.setChecked(True)
        layout.addWidget(sq_check)
        
        fq_check = QtWidgets.QCheckBox("F(Q) - Reduced Structure Function")
        fq_check.setChecked(True)
        layout.addWidget(fq_check)
        
        gr_check = QtWidgets.QCheckBox("G(r) - Pair Distribution Function")
        gr_check.setChecked(True)
        layout.addWidget(gr_check)
        
        layout.addWidget(QtWidgets.QLabel(""))  # Spacer
        
        # Lorch correction checkbox (only if Lorch is enabled)
        lorch_check = QtWidgets.QCheckBox("保存Lorch修正后的F(Q)和G(r) / Save Lorch-corrected F(Q) and G(r)")
        lorch_check.setChecked(True)
        lorch_check.setEnabled(self.lorch_check.isChecked())  # Enable only if Lorch is applied
        if self.lorch_check.isChecked():
            lorch_check.setToolTip("保存Lorch修正后的数据 (*.fq_lorch, *.gr_lorch)")
        else:
            lorch_check.setToolTip("仅当启用Lorch修正时可用")
        layout.addWidget(lorch_check)
        
        layout.addWidget(QtWidgets.QLabel(""))  # Spacer
        
        # Config file checkbox
        cfg_check = QtWidgets.QCheckBox("Save configuration file (.cfg)")
        cfg_check.setChecked(True)
        layout.addWidget(cfg_check)
        
        # Buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        # Show dialog
        if dialog.exec() != QtWidgets.QDialog.DialogCode.Accepted:
            return
        
        # Select save directory
        save_dir = QtWidgets.QFileDialog.getExistingDirectory(
            self,
            "Select Save Directory",
            "",
            QtWidgets.QFileDialog.Option.ShowDirsOnly
        )
        
        if not save_dir:
            return
        
        try:
            from pathlib import Path
            import numpy as np
            
            # Get base name for files and qmax value
            data_file = self.data_file_edit.text()
            if data_file:
                base_name = Path(data_file).stem
            else:
                base_name = "result"
            
            # Get qmax value for filename
            qmax_value = self.qmax_spin.value()
            # Create base filename with qmax
            base_filename = f"{base_name}_qmax{qmax_value:.0f}"
            
            results = self.current_results
            save_path = Path(save_dir)
            files_saved = []
            
            # Save I(Q) if selected and available
            if iq_check.isChecked() and hasattr(results, 'qi') and hasattr(results, 'iq'):
                iq_file = save_path / f"{base_filename}.iq"
                data = np.column_stack([results.qi, results.iq])
                np.savetxt(iq_file, data, header="Q(1/A)  I(Q)", fmt='%.6f', comments='# ')
                files_saved.append(iq_file.name)
            
            # Save S(Q) if selected and available
            if sq_check.isChecked() and hasattr(results, 'q') and hasattr(results, 'sq'):
                sq_file = save_path / f"{base_filename}.sq"
                data = np.column_stack([results.q, results.sq])
                np.savetxt(sq_file, data, header="Q(1/A)  S(Q)", fmt='%.6f', comments='# ')
                files_saved.append(sq_file.name)
            
            # Save F(Q) if selected and available
            # If Lorch is enabled, save the ORIGINAL (uncorrected) F(Q)
            if fq_check.isChecked() and hasattr(results, 'q') and hasattr(results, 'fq'):
                fq_file = save_path / f"{base_filename}.fq"
                # Use fq_orig if Lorch was applied, otherwise use fq
                fq_data = results.fq_orig if (hasattr(results, 'fq_orig') and results.fq_orig is not None) else results.fq
                data = np.column_stack([results.q, fq_data])
                np.savetxt(fq_file, data, header="Q(1/A)  F(Q)", fmt='%.6f', comments='# ')
                files_saved.append(fq_file.name)
            
            # Save G(r) if selected and available
            # If Lorch is enabled, save the ORIGINAL (uncorrected) G(r)
            if gr_check.isChecked() and hasattr(results, 'r') and hasattr(results, 'gr'):
                gr_file = save_path / f"{base_filename}.gr"
                # Use gr_orig if Lorch was applied, otherwise use gr
                gr_data = results.gr_orig if (hasattr(results, 'gr_orig') and results.gr_orig is not None) else results.gr
                data = np.column_stack([results.r, gr_data])
                np.savetxt(gr_file, data, header="r(A)  G(r)", fmt='%.6f', comments='# ')
                files_saved.append(gr_file.name)
            
            # Save config file if selected
            if cfg_check.isChecked():
                cfg_file = save_path / f"{base_filename}.cfg"
                self._save_single_config_file(cfg_file, base_name, files_saved)
                files_saved.append(cfg_file.name)
            
            # Save Lorch-corrected data if selected and available
            if lorch_check.isChecked() and lorch_check.isEnabled():
                # Save Lorch-corrected F(Q) if available (use .lorch before extension)
                if hasattr(results, 'fq_lorch') and results.fq_lorch is not None:
                    fq_lorch_file = save_path / f"{base_filename}.lorch.fq"
                    data = np.column_stack([results.q, results.fq_lorch])
                    np.savetxt(fq_lorch_file, data, header="Q(1/A)  F(Q)_Lorch-corrected", fmt='%.6f', comments='# ')
                    files_saved.append(fq_lorch_file.name)
                
                # Save Lorch-corrected G(r) if available (use .lorch before extension)
                if hasattr(results, 'gr_lorch') and results.gr_lorch is not None:
                    gr_lorch_file = save_path / f"{base_filename}.lorch.gr"
                    data = np.column_stack([results.r, results.gr_lorch])
                    np.savetxt(gr_lorch_file, data, header="r(A)  G(r)_Lorch-corrected", fmt='%.6f', comments='# ')
                    files_saved.append(gr_lorch_file.name)
            
            # Success message
            QtWidgets.QMessageBox.information(
                self,
                "Save Successful",
                f"Saved {len(files_saved)} file(s) to:\n{save_dir}\n\nFiles:\n" + "\n".join(files_saved)
            )
            
            logger.info(f"Results saved to {save_dir}: {files_saved}")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self,
                "Save Error",
                f"Failed to save results:\n{str(e)}"
            )
            logger.error(f"Failed to save results: {e}")
    
    def _save_single_config_file(self, config_path, base_name, output_files):
        """Save a single configuration file for the project."""
        params = self._get_parameters()
        
        with open(config_path, 'w', encoding='utf-8') as f:
            f.write(f"# PDFgetX3 Configuration\n")
            f.write(f"# Project: {base_name}\n")
            f.write(f"# Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("\n[pdfgetx3]\n")
            
            # Input files
            f.write(f"\n## Input Files\n")
            f.write(f"datafile = {self.data_file_edit.text()}\n")
            if self.bkg_file_edit.text():
                f.write(f"backgroundfile = {self.bkg_file_edit.text()}\n")
            
            # Output files
            f.write(f"\n## Output Files\n")
            for out_file in output_files:
                if out_file.endswith('.cfg'):
                    continue
                f.write(f"# {out_file}\n")
            
            # Data format
            f.write(f"\n## Data Format\n")
            f.write(f"dataformat = {params.dataformat}\n")
            if params.dataformat == 'twotheta':
                f.write(f"wavelength = {params.wavelength}\n")
            
            # Composition
            f.write(f"composition = {params.composition}\n")
            
            # Q-space parameters
            f.write(f"\n## Q-space Parameters\n")
            f.write(f"qmin = {params.qmin}\n")
            f.write(f"qmax = {params.qmax}\n")
            f.write(f"qmaxinst = {params.qmaxinst}\n")
            
            # R-space parameters
            f.write(f"\n## R-space Parameters\n")
            f.write(f"rmin = {params.rmin}\n")
            f.write(f"rmax = {params.rmax}\n")
            f.write(f"rstep = {params.rstep}\n")
            
            # Processing parameters
            f.write(f"\n## Processing Parameters\n")
            f.write(f"bkgscale = {params.bkgscale}\n")
            f.write(f"rpoly = {params.rpoly}\n")
            
            # Resampling
            if params.rebin_mode != 'none':
                f.write(f"\n## Resampling\n")
                f.write(f"mode = {params.rebin_mode}\n")

    def _load_recent_file(self, item):
        """Load file from recent files list."""
        file_path = item.text()
        self.data_file_edit.setText(file_path)
        logger.info(f"Loaded recent file: {file_path}")
    
    def _show_preferences(self):
        """Show preferences dialog."""
        from .preferences_dialog import PreferencesDialog
        
        dialog = PreferencesDialog(self, self.settings.language, self.settings.theme)
        
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            logger.info("Preferences updated")
    
    def _show_about(self):
        """Show about dialog."""
        about_text = """
        <div style='text-align: center;'>
            <h2 style='color: #2196F3; margin-bottom: 10px;'>PDFgetX3GUI V2.0</h2>
            <p style='font-size: 11pt; color: #666;'><i></i></p>
    
            
            <hr style='margin: 20px 0; border: none; border-top: 1px solid #ddd;'>
            
            <p style='margin-top: 20px;'>
                <b>开发单位:</b> 杭州同辐智测<br>
                <b>微信:</b>  synchrotron_XRD_PDF<br>
                <b>许可证:</b> MIT License
            </p>
            
            <p style='margin-top: 15px; font-size: 9pt; color: #999;'>
                基于 Python, PyQt5, NumPy, SciPy & Matplotlib 构建
            </p>
        </div>
        """
        
        QtWidgets.QMessageBox.about(
            self,
            "关于 PDFgetX3 GUI v2.0",
            about_text
        )
