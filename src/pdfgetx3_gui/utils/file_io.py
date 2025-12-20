"""
File I/O utilities.

Handles loading and saving data files with robust error handling.
"""

from pathlib import Path
from typing import Tuple, Optional, Union
import numpy as np
import re
import logging

logger = logging.getLogger(__name__)


class FileIO:
    """File input/output operations."""
    
    SUPPORTED_EXTENSIONS = [".txt", ".dat", ".xy", ".xye", ".csv"]
    
    @staticmethod
    def load_data(filepath: Union[str, Path]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Load data from file with automatic comment detection.
        
        Args:
            filepath: Path to data file
        
        Returns:
            Tuple of (x_data, y_data)
        
        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is invalid
        """
        filepath = Path(filepath)
        
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")
            
        # Try using diffpy.pdfgetx.loadData first (handles .chi and headers better)
        try:
            from diffpy.pdfgetx import loadData
            x, y = loadData(str(filepath))
            logger.debug(f"Loaded {len(x)} data points using diffpy.pdfgetx from {filepath}")
            return x, y
        except (ImportError, Exception) as e:
            logger.debug(f"diffpy.pdfgetx.loadData failed: {e}, falling back to numpy")
        
        # Try loading with standard comment character first
        try:
            x, y = np.loadtxt(
                filepath,
                unpack=True,
                comments='#',
                usecols=(0, 1)
            )
            logger.debug(f"Loaded {len(x)} data points from {filepath}")
            return x, y
            
        except ValueError:
            logger.debug("Standard loading failed, trying line-by-line detection")
        
        # Fall back to line-by-line parsing
        try:
            with open(filepath, 'r') as f:
                lines = f.read().split('\n')
            
            # Find first line with numeric data
            for i, line in enumerate(lines):
                if not line.strip():
                    continue
                
                # Check if first non-whitespace character is numeric
                if re.search('[0-9]', line.replace(' ', '')[0].lower()):
                    x, y = np.loadtxt(
                        filepath,
                        unpack=True,
                        skiprows=i,
                        usecols=(0, 1)
                    )
                    logger.debug(f"Loaded {len(x)} data points from {filepath} (skipped {i} lines)")
                    return x, y
            
            raise ValueError(f"No numeric data found in {filepath}")
            
        except Exception as e:
            logger.error(f"Failed to load data from {filepath}: {e}")
            raise ValueError(f"Could not load data from {filepath}: {e}") from e
    
    @staticmethod
    def save_data(
        filepath: Union[str, Path],
        x: np.ndarray,
        y: np.ndarray,
        header: Optional[str] = None
    ) -> None:
        """
        Save data to file.
        
        Args:
            filepath: Output file path
            x: X data array
            y: Y data array
            header: Optional header comment
        """
        filepath = Path(filepath)
        
        # Ensure directory exists
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        data = np.column_stack([x, y])
        
        if header:
            np.savetxt(filepath, data, header=header, fmt='%.6f')
        else:
            np.savetxt(filepath, data, fmt='%.6f')
        
        logger.info(f"Saved data to {filepath}")
    
    @staticmethod
    def validate_file(filepath: Union[str, Path]) -> bool:
        """Check if file exists and has supported extension."""
        filepath = Path(filepath)
        
        if not filepath.exists():
            return False
        
        if filepath.suffix.lower() not in FileIO.SUPPORTED_EXTENSIONS:
            logger.warning(f"File has unsupported extension: {filepath.suffix}")
            return False
        
        return True
