"""Preferences dialog for application settings."""

from PyQt6 import QtWidgets, QtCore
from ..utils.i18n import get_translator, tr


class PreferencesDialog(QtWidgets.QDialog):
    """Preferences dialog for language and theme settings."""
    
    # Signals emitted when preferences change
    languageChanged = QtCore.pyqtSignal(str)
    themeChanged = QtCore.pyqtSignal(str)
    
    def __init__(self, parent=None, current_language='en', current_theme='light'):
        """Initialize preferences dialog."""
        super().__init__(parent)
        
        self.current_language = current_language
        self.current_theme = current_theme
        self.translator = get_translator()
        
        self.setWindowTitle(tr('dialog_preferences_title'))
        self.setMinimumWidth(400)
        self.setModal(True)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Setup the UI."""
        layout = QtWidgets.QVBoxLayout(self)
        
        # Language selection
        lang_group = QtWidgets.QGroupBox(tr('pref_language'))
        lang_layout = QtWidgets.QVBoxLayout()
        
        self.lang_en = QtWidgets.QRadioButton(tr('pref_language_english'))
        self.lang_zh = QtWidgets.QRadioButton(tr('pref_language_chinese'))
        
        if self.current_language == 'en':
            self.lang_en.setChecked(True)
        else:
            self.lang_zh.setChecked(True)
        
        lang_layout.addWidget(self.lang_en)
        lang_layout.addWidget(self.lang_zh)
        lang_group.setLayout(lang_layout)
        
        layout.addWidget(lang_group)
        
        # Theme selection
        theme_group = QtWidgets.QGroupBox(tr('pref_theme'))
        theme_layout = QtWidgets.QVBoxLayout()
        
        self.theme_light = QtWidgets.QRadioButton(tr('pref_theme_light'))
        self.theme_dark = QtWidgets.QRadioButton(tr('pref_theme_dark'))
        
        # Set current theme
        if self.current_theme == 'dark':
            self.theme_dark.setChecked(True)
        else:
            self.theme_light.setChecked(True)
        
        theme_layout.addWidget(self.theme_light)
        theme_layout.addWidget(self.theme_dark)
        theme_group.setLayout(theme_layout)
        
        layout.addWidget(theme_group)
        
        # Buttons
        button_box = QtWidgets.QDialogButtonBox(
            QtWidgets.QDialogButtonBox.StandardButton.Ok | QtWidgets.QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._on_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def _on_accept(self):
        """Handle OK button click."""
        new_language = 'en' if self.lang_en.isChecked() else 'zh'
        new_theme = 'dark' if self.theme_dark.isChecked() else 'light'
        
        # Check if preferences changed
        language_changed = new_language != self.current_language
        theme_changed = new_theme != self.current_theme
        
        # Save to settings file via parent's settings
        if hasattr(self.parent(), 'settings'):
            self.parent().settings.language = new_language
            self.parent().settings.theme = new_theme
            self.parent().settings.save()
        
        # Emit signals
        if language_changed:
            self.languageChanged.emit(new_language)
        
        if theme_changed:
            self.themeChanged.emit(new_theme)
        
        # Show restart message if needed
        if language_changed or theme_changed:
            QtWidgets.QMessageBox.information(
                self,
                tr('dialog_preferences_title'),
                "Preferences saved. Please restart the application for changes to take effect.\n"
                "首选项已保存。请重启应用程序以使更改生效。"
            )
        
        self.accept()
