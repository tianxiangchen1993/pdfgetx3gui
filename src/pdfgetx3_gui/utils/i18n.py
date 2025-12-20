"""
Internationalization (i18n) module.

Provides translation support for multiple languages.
"""

from typing import Dict
import json
from pathlib import Path


class Translator:
    """Simple translator for GUI text."""
    
    # Translation dictionaries
    TRANSLATIONS = {
        'en': {
            # Menu
            'menu_file': '&File',
            'menu_open': '&Open Data File...',
            'menu_open_bkg': 'Open &Background File...',
            'menu_save': '&Save Results...',
            'menu_exit': 'E&xit',
            'menu_settings': '&Settings',
            'menu_preferences': '&Preferences...',
            'menu_help': '&Help',
            'menu_about': '&About',
            
            # Toolbar
            'toolbar_open': 'Open',
            'toolbar_calculate': 'Calculate',
            'toolbar_stop': 'Stop',
            'toolbar_save': 'Save',
            
            # Tabs
            'tab_files_processing': 'Files && Processing',
            'tab_parameters': 'Parameters',
            'tab_display': 'Display',
            
            # Files & Processing Tab
            'section_data_files': 'Data Files',
            'label_data_file': 'Data File:',
            'label_background': 'Background:',
            'button_browse': 'Browse...',
            'placeholder_data_file': 'Select data file...',
            'placeholder_bkg_file': 'Select background file...',
            'radio_rebin_exp': 'Exp',
            
            'section_recent_files': 'Recent Files',
            
            # Parameters Tab
            'label_composition': 'Composition:',
            'group_q_params': 'Q-space Parameters',
            'label_qmin': 'Qmin:',
            'label_qmax': 'Qmax:',
            'label_qmax_inst': 'Qmax (inst):',
            
            'group_r_params': 'R-space Parameters',
            'label_rmin': 'rmin:',
            'label_rmax': 'rmax:',
            'label_rstep': 'rstep:',
            
            # Display Tab
            'group_plots': 'Plots to Display',
            'check_plot_iq': 'I(Q) - Intensity',
            'check_plot_sq': 'S(Q) - Structure Factor',
            'check_plot_fq': 'F(Q) - Reduced Structure Function',
            'check_plot_gr': 'G(r) - Pair Distribution Function',
            'check_reset_axes': 'Reset axes on update',
            
            # Buttons
            'button_calculate': 'Calculate (F5)',
            'button_save_results': 'Save Results',
            'button_add_files': 'Add Files',
            'button_remove_selected': 'Remove Selected',
            'button_clear_all': 'Clear All',
            'group_options': 'Options',
            
            # Status messages
            'status_ready': 'Ready',
            'status_calculating': 'Calculating...',
            'status_completed': 'Calculation completed successfully',
            'status_failed': 'Calculation failed',
            
            # Dialogs
            'dialog_no_data_file': 'No Data File',
            'dialog_select_file_first': 'Please select a data file first.',
            'dialog_no_plots': 'No Plots Selected',
            'dialog_select_plot': 'Please select at least one plot to display.',
            'dialog_no_results': 'No Results',
            'dialog_run_calc_first': 'Please run a calculation first before saving.',
            'dialog_calc_error': 'Calculation Error',
            'dialog_save_error': 'Save Error',
            'dialog_preferences_title': 'Preferences',
            'dialog_about_title': 'About PDFgetX3 GUI v2.0',
            
            # Preferences
            'pref_language': 'Language:',
            'pref_language_english': 'English',
            'pref_language_chinese': '中文',
            'pref_theme': 'Theme:',
            'pref_theme_light': 'Light',
            'pref_theme_dark': 'Dark',
            
            # Window title
            'window_title': 'PDFgetX3 GUI v2.0 - Optimized & Modern',
        },
        
        'zh': {
            # 菜单
            'menu_file': '文件(&F)',
            'menu_open': '打开数据文件(&O)...',
            'menu_open_bkg': '打开背景文件(&B)...',
            'menu_save': '保存结果(&S)...',
            'menu_exit': '退出(&X)',
            'menu_settings': '设置(&S)',
            'menu_preferences': '首选项(&P)...',
            'menu_help': '帮助(&H)',
            'menu_about': '关于(&A)',
            
            # 工具栏
            'toolbar_open': '打开',
            'toolbar_calculate': '计算',
            'toolbar_stop': '停止',
            'toolbar_save': '保存',
            
            # 标签页
            'tab_files_processing': '文件 && 处理',
            'tab_parameters': '参数',
            'tab_display': '显示',
            
            # 文件和处理标签页
            'section_data_files': '数据文件',
            'label_data_file': '数据文件:',
            'label_background': '背景文件:',
            'button_browse': '浏览...',
            'placeholder_data_file': '选择数据文件...',
            'placeholder_bkg_file': '选择背景文件...',
            
            'section_processing': '数据处理',
            'label_bkg_scale': '背景缩放:',
            'label_rpoly': 'Rpoly:',
            'label_wavelength': '波长:',
            'section_resampling': '重采样',
           'label_resampling': '重采样:',
            'section_data_format': '数据格式',
            'label_data_format': '数据格式:',
            'radio_format_q': 'Q (Å⁻¹)',
            'radio_format_2theta': '2θ (度)',
            'radio_rebin_none': '无',
            'radio_rebin_linear': '线性',
            'radio_rebin_exp': '指数',
            
            'section_recent_files': '当前文件',
            
            # 参数标签页
            'label_composition': '化学式:',
            'group_q_params': 'Q空间参数',
            'label_qmin': 'Qmin:',
            'label_qmax': 'Qmax:',
            'label_qmax_inst': 'Qmax (仪器):',
            
            'group_r_params': 'R空间参数',
            'label_rmin': 'rmin:',
            'label_rmax': 'rmax:',
            'label_rstep': 'rstep:',
            
            # 显示标签页
            'group_plots': '显示图表',
            'check_plot_iq': 'I(Q) - 强度',
            'check_plot_sq': 'S(Q) - 结构因子',
            'check_plot_fq': 'F(Q) - 约化结构函数',
            'check_plot_gr': 'G(r) - 配对分布函数',
            'check_reset_axes': '更新时重置坐标轴',
            
            # 按钮
            'button_calculate': '计算 (F5)',
            'button_save_results': '保存结果',
            'button_add_files': '添加文件',
            'button_remove_selected': '移除选中',
            'button_clear_all': '清空全部',
            'group_options': '选项',
            
            # 状态消息
            'status_ready': '就绪',
            'status_calculating': '计算中...',
            'status_completed': '计算成功完成',
            'status_failed': '计算失败',
            
            # 对话框
            'dialog_no_data_file': '无数据文件',
            'dialog_select_file_first': '请先选择数据文件。',
            'dialog_no_plots': '未选择图表',
            'dialog_select_plot': '请至少选择一个要显示的图表。',
            'dialog_no_results': '无结果',
            'dialog_run_calc_first': '请先运行计算再保存。',
            'dialog_calc_error': '计算错误',
            'dialog_save_error': '保存错误',
            'dialog_preferences_title': '首选项',
            'dialog_about_title': '关于 PDFgetX3 GUI v2.0',
            
            # 首选项
            'pref_language': '语言:',
            'pref_language_english': 'English',
            'pref_language_chinese': '中文',
            'pref_theme': '主题:',
            'pref_theme_light': '浅色',
            'pref_theme_dark': '深色',
            
            # 窗口标题
            'window_title': 'PDFgetX3 GUI v2.0 - 优化现代版',
        }
    }
    
    def __init__(self, language: str = 'en'):
        """Initialize translator with specified language."""
        self.language = language
        self._current_translations = self.TRANSLATIONS.get(language, self.TRANSLATIONS['en'])
    
    def tr(self, key: str) -> str:
        """
        Translate a key to current language.
        
        Args:
            key: Translation key
            
        Returns:
            Translated text, or key if not found
        """
        return self._current_translations.get(key, key)
    
    def set_language(self, language: str):
        """Set current language."""
        if language in self.TRANSLATIONS:
            self.language = language
            self._current_translations = self.TRANSLATIONS[language]
    
    def get_available_languages(self) -> Dict[str, str]:
        """Get available languages."""
        return {
            'en': 'English',
            'zh': '中文'
        }


# Global translator instance
_translator = Translator()


def tr(key: str) -> str:
    """Global translation function."""
    return _translator.tr(key)


def set_language(language: str):
    """Set global language."""
    _translator.set_language(language)


def get_translator() -> Translator:
    """Get global translator instance."""
    return _translator
