"""
Main application entry point.

This is a minimal entry point. Full GUI implementation is in progress.
"""

import sys
import logging
from pathlib import Path

from pdfgetx3_gui.utils.logger import setup_logging


def main():
    """Main application entry point."""
    # Setup logging
    log_dir = Path.home() / ".pdfgetx3gui v2.0"
    log_dir.mkdir(exist_ok=True)
    setup_logging(
        level=logging.INFO,
        log_file=log_dir / "pdfgetx3gui.log",
        console=True
    )
    
    logger = logging.getLogger(__name__)
    logger.info("=" * 60)
    logger.info("PDFgetX3GUI V2.0")
    logger.info("=" * 60)
    
    # Create and launch Qt application
    from PyQt6 import QtWidgets
    from pdfgetx3_gui.gui import MainWindow
    
    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationName("PDFgetX3GUI V2.0")
    app.setOrganizationName("DiffPy")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    logger.info("Application started successfully")
    
    # Run event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
