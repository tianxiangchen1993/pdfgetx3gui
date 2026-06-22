"""
Main application entry point.

This is a minimal entry point. Full GUI implementation is in progress.
"""

import sys
import os
import logging
import subprocess
from pathlib import Path

from pdfgetx3_gui.utils.logger import setup_logging


def _reexec_with_active_conda_python():
    """Restart with the active conda environment when a stale launcher is used."""
    if os.environ.get("PDFGETX3GUI_REEXECED") == "1":
        return None

    conda_prefix = os.environ.get("CONDA_PREFIX")
    if not conda_prefix:
        return None

    python_exe = Path(conda_prefix) / "python.exe"
    if not python_exe.exists():
        return None

    if python_exe.resolve() == Path(sys.executable).resolve():
        return None

    import_check = "from PyQt6 import QtWidgets; import scipy; import diffpy.pdfgetx"
    check = subprocess.run(
        [str(python_exe), "-c", import_check],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if check.returncode != 0:
        return None

    env = os.environ.copy()
    env["PDFGETX3GUI_REEXECED"] = "1"
    package_parent = str(Path(__file__).resolve().parents[1])
    env["PYTHONPATH"] = (
        package_parent
        if not env.get("PYTHONPATH")
        else package_parent + os.pathsep + env["PYTHONPATH"]
    )

    return subprocess.call(
        [str(python_exe), "-m", "pdfgetx3_gui.main", *sys.argv[1:]],
        env=env,
    )


def main():
    """Main application entry point."""
    reexec_status = _reexec_with_active_conda_python()
    if reexec_status is not None:
        return reexec_status

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
