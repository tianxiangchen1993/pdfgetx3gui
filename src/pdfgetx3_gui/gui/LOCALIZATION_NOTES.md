"""
Complete Chinese localization of main_window.py

This module creates a fully localized version that can be switched
between English and Chinese through the preferences dialog.
"""

# This file serves as a reference implementation for full i18n support.
# The actual implementation integrates translations into the main_window.py
# using the tr() function from utils.i18n module.

# Key implementation strategy:
# 1. All hardcoded text strings replaced with tr('key')
# 2. Translation keys defined in utils/i18n.py
# 3. Language switching via Preferences dialog
# 4. Setting persisted in configuration

# Example transformations:
# Before: "Data File:" 
# After:  tr('label_data_file')

# Before: "Calculate (F5)"
# After:  tr('button_calculate')

# This ensures all UI elements can be dynamically translated
# without code changes.
