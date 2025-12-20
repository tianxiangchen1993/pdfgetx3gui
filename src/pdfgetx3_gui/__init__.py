"""
PDFgetX3 GUI - Modern GUI for PDFgetX3
Version 2.0 - Optimized Architecture

A graphical user interface for running PDFgetX3 with improved code quality,
modern UI/UX, and better performance.
"""

__version__ = "2.0.0"
__author__ = "Optimized by AI Assistant, Original by Kenneth P. Marshall"

from .config.settings import Settings
from .core.calculator import PDFCalculator

__all__ = ["Settings", "PDFCalculator", "__version__"]
