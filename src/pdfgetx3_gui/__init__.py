"""
PDFgetX3 GUI - Modern GUI for PDFgetX3
Version 2.0 - Optimized Architecture

A graphical user interface for running PDFgetX3 with improved code quality,
modern UI/UX, and better performance.
"""

__version__ = "2.0.0"
__author__ = "Optimized by AI Assistant, Original by Kenneth P. Marshall"

import os
from pathlib import Path


def _extend_pdfgetx_path():
    """Allow launchers to point at an existing PDFgetX3 installation."""
    diffpy_dir = os.environ.get("PDFGETX3GUI_DIFFPY_DIR")
    if not diffpy_dir:
        return

    diffpy_path = Path(diffpy_dir)
    if not diffpy_path.is_dir():
        return

    try:
        import diffpy
    except ImportError:
        return

    diffpy_path_str = str(diffpy_path)
    if diffpy_path_str not in diffpy.__path__:
        diffpy.__path__.append(diffpy_path_str)


_extend_pdfgetx_path()

from .config.settings import Settings
from .core.calculator import PDFCalculator

__all__ = ["Settings", "PDFCalculator", "__version__"]
