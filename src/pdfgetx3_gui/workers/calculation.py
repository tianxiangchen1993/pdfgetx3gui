"""
Worker threads for background calculations.

Uses QThread to run PDF calculations without blocking the GUI.
"""

from PyQt6 import QtCore
from pathlib import Path
from typing import Optional
import logging

from ..config.settings import PDFParameters
from ..core.calculator import PDFCalculator, PDFResults
from ..core.resampler import DataResampler
from ..utils.file_io import FileIO
from ..utils.logger import get_logger

logger = get_logger(__name__)


class CalculationWorker(QtCore.QThread):
    """
    Background worker for PDF calculations.
    
    Signals:
        progress: (int) Progress percentage (0-100)
        finished: (PDFResults) Calculation completed successfully
        error: (str) Error message if calculation failed
    """
    
    progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal(object)  # PDFResults
    error = QtCore.pyqtSignal(str)
    
    def __init__(
        self,
        params: PDFParameters,
        data_file: str,
        bkg_file: Optional[str] = None
    ):
        """
        Initialize the calculation worker.
        
        Args:
            params: PDF calculation parameters
            data_file: Path to data file
            bkg_file: Optional path to background file
        """
        super().__init__()
        
        self.params = params
        self.data_file = data_file
        self.bkg_file = bkg_file
        self.calculator = PDFCalculator()
        self._is_running = True
        
        logger.debug(f"Worker initialized for {data_file}")
    
    def run(self):
        """Run the calculation in background thread."""
        try:
            logger.info("Starting PDF calculation...")
            self.progress.emit(10)
            
            # Load data
            logger.debug(f"Loading data from {self.data_file}")
            x, y = FileIO.load_data(self.data_file)
            self.progress.emit(20)
            
            if not self._is_running:
                return
            
            # Apply resampling if needed
            if self.params.rebin_mode != "none":
                logger.debug(f"Applying {self.params.rebin_mode} resampling")
                x, y = DataResampler.resample(
                    x, y,
                    mode=self.params.rebin_mode,
                    linear_gradient=self.params.linear_gradient,
                    exponential_constant=self.params.exponential_constant
                )
            self.progress.emit(40)
            
            if not self._is_running:
                return
            
            # Run calculation
            logger.debug("Running PDF calculation")
            results = self.calculator.calculate(
                params=self.params,
                bkgfile=self.bkg_file,
                x_data=x,
                y_data=y
            )
            self.progress.emit(80)
            
            if not self._is_running:
                return
            
            # Emit results
            self.progress.emit(100)
            self.finished.emit(results)
            logger.info("PDF calculation completed successfully")
            
        except Exception as e:
            error_msg = f"Calculation failed: {str(e)}"
            logger.error(error_msg, exc_info=True)
            self.error.emit(error_msg)
    
    def stop(self):
        """Stop the calculation."""
        self._is_running = False
        logger.info("Calculation stopped by user")


class BatchWorker(QtCore.QThread):
    """
    Background worker for batch processing multiple files.
    
    Signals:
        progress: (int, int) Current file index and total files
        file_processed: (str) File that was just processed
        finished: () All files processed
        error: (str, str) Filename and error message
    """
    
    progress = QtCore.pyqtSignal(int, int)
    file_processed = QtCore.pyqtSignal(str)
    finished = QtCore.pyqtSignal()
    error = QtCore.pyqtSignal(str, str)
    
    def __init__(
        self,
        params: PDFParameters,
        data_files: list,
        bkg_file: Optional[str] = None
    ):
        """
        Initialize the batch worker.
        
        Args:
            params: PDF calculation parameters
            data_files: List of data file paths
            bkg_file: Optional background file path
        """
        super().__init__()
        
        self.params = params
        self.data_files = data_files
        self.bkg_file = bkg_file
        self.calculator = PDFCalculator()
        self._is_running = True
        
        logger.debug(f"Batch worker initialized for {len(data_files)} files")
    
    def run(self):
        """Process all files in batch."""
        total = len(self.data_files)
        
        for idx, data_file in enumerate(self.data_files):
            if not self._is_running:
                break
            
            try:
                logger.info(f"Processing file {idx+1}/{total}: {data_file}")
                self.progress.emit(idx + 1, total)
                
                # Load and calculate
                x, y = FileIO.load_data(data_file)
                
                if self.params.rebin_mode != "none":
                    x, y = DataResampler.resample(
                        x, y,
                        mode=self.params.rebin_mode
                    )
                
                results = self.calculator.calculate(
                    params=self.params,
                    bkgfile=self.bkg_file,
                    x_data=x,
                    y_data=y
                )
                
                # Save results
                basename = str(Path(data_file).with_suffix(''))
                self.calculator.save_results(
                    results,
                    basename=basename,
                    save_iq=self.params.show_iq,
                    save_sq=self.params.show_sq,
                    save_fq=self.params.show_fq,
                    save_gr=self.params.show_gr
                )
                
                self.file_processed.emit(data_file)
                logger.info(f"Successfully processed {data_file}")
                
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Error processing {data_file}: {error_msg}")
                self.error.emit(data_file, error_msg)
        
        self.finished.emit()
        logger.info("Batch processing completed")
    
    def stop(self):
        """Stop batch processing."""
        self._is_running = False
        logger.info("Batch processing stopped by user")

class MultiCalculationWorker(QtCore.QThread):
    """
    Background worker for processing multiple files for plotting.
    Returns a list of (filename, results) tuples.
    
    Signals:
        progress: (int) Progress percentage (0-100)
        finished: (list) List of (filename, PDFResults) tuples
        error: (str) Error message if calculation failed
    """
    
    progress = QtCore.pyqtSignal(int)
    finished = QtCore.pyqtSignal(list)
    error = QtCore.pyqtSignal(str)
    
    def __init__(
        self,
        params: PDFParameters,
        data_files: list,
        bkg_file: Optional[str] = None
    ):
        super().__init__()
        self.params = params
        self.data_files = data_files
        self.bkg_file = bkg_file
        self.calculator = PDFCalculator()
        self._is_running = True
        
    def run(self):
        try:
            import time
            results_list = []
            total = len(self.data_files)
            
            for idx, data_file in enumerate(self.data_files):
                if not self._is_running:
                    return
                
                # Update progress
                current_progress = int((idx / total) * 100)
                self.progress.emit(current_progress)
                
                # Give UI time to update
                time.sleep(0.01)
                
                # Load data
                x, y = FileIO.load_data(data_file)
                
                # Resample
                if self.params.rebin_mode != "none":
                    x, y = DataResampler.resample(
                        x, y,
                        mode=self.params.rebin_mode,
                        linear_gradient=self.params.linear_gradient,
                        exponential_constant=self.params.exponential_constant
                    )
                
                # Calculate
                results = self.calculator.calculate(
                    params=self.params,
                    bkgfile=self.bkg_file,
                    x_data=x,
                    y_data=y
                )
                
                # Add to list
                from pathlib import Path
                filename = Path(data_file).name
                results_list.append((filename, results))
            
            if not self._is_running:
                return
                
            self.progress.emit(100)
            self.finished.emit(results_list)
            
        except Exception as e:
            import traceback
            logger.error(f"Batch calculation error: {e}\n{traceback.format_exc()}")
            self.error.emit(str(e))
    
    def stop(self):
        self._is_running = False
