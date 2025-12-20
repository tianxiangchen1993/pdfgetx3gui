"""
Data resampling module.

Implements various rebinning algorithms for high-Q noise reduction.
"""

from typing import Tuple
import numpy as np
from scipy.interpolate import interp1d
import logging

logger = logging.getLogger(__name__)

# ResampleMode can be: "none", "linear", "exponential"


class DataResampler:
    """Handles data resampling/rebinning operations."""
    
    @staticmethod
    def resample(
        x: np.ndarray,
        y: np.ndarray,
        mode: str = "none",  # "none", "linear", or "exponential"
        linear_gradient: float = 1.1,
        exponential_constant: float = 0.0005
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Resample data using specified method.
        
        Args:
            x: X data array
            y: Y data array
            mode: Resampling mode ("none", "linear", "exponential")
            linear_gradient: Gradient for linear binning
            exponential_constant: Constant for exponential binning
        
        Returns:
            Tuple of (resampled_x, resampled_y)
        """
        if mode == "none":
            return x, y
        elif mode == "linear":
            return DataResampler._linear_rebin(x, y, linear_gradient)
        elif mode == "exponential":
            return DataResampler._exponential_rebin(x, y, exponential_constant)
        else:
            raise ValueError(f"Invalid resampling mode: {mode}")
    
    @staticmethod
    def _linear_rebin(
        x: np.ndarray,
        y: np.ndarray,
        gradient: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Linear rebinning implementation."""
        x_spacing = (x[-1] - x[0]) / (len(x) - 1)
        x_overgrid = np.arange(x[0], x[-1], x_spacing / 15)
        
        interp_func = interp1d(x, y)
        y_overgrid = interp_func(x_overgrid)
        
        # Create new bins
        new_x = np.array([
            xn * gradient - (x[0] * gradient - x[0])
            for xn in x
            if xn * gradient - (x[0] * gradient - x[0]) < x[-1]
        ])
        
        return DataResampler._average_bins(x_overgrid, y_overgrid, new_x, x)
    
    @staticmethod
    def _exponential_rebin(
        x: np.ndarray,
        y: np.ndarray,
        exponent: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Exponential rebinning implementation."""
        x_spacing = (x[-1] - x[0]) / (len(x) - 1)
        x_overgrid = np.arange(x[0], x[-1], x_spacing / 15)
        
        interp_func = interp1d(x, y)
        y_overgrid = interp_func(x_overgrid)
        
        # Create exponentially-spaced bins
        new_x = np.array([
            xn * np.exp(exponent * i)
            for i, xn in enumerate(x)
            if xn * np.exp(exponent * i) < x[-1]
        ])
        
        return DataResampler._average_bins(x_overgrid, y_overgrid, new_x, x)
    
    @staticmethod
    def _average_bins(
        x_overgrid: np.ndarray,
        y_overgrid: np.ndarray,
        new_x: np.ndarray,
        original_x: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Average data into new bins."""
        new_y = np.array([])
        
        for n in range(len(new_x)):
            # Determine bin edges
            if n == 0:
                x_min = new_x[n]
            else:
                x_min = (new_x[n] + new_x[n-1]) / 2
            
            if n == len(new_x) - 1:
                x_max = new_x[n]
            else:
                x_max = (new_x[n+1] + new_x[n]) / 2
            
            # Find data in this bin
            min_idx = np.abs(x_overgrid - x_min).argmin()
            max_idx = np.abs(x_overgrid - x_max).argmin()
            
            # Average
            y_avg = np.average(y_overgrid[min_idx:max_idx])
            new_y = np.append(new_y, y_avg)
        
        # Interpolate back to original grid (partial)
        max_idx = np.abs(original_x - new_x[-1]).argmin()
        interp_func2 = interp1d(new_x, new_y)
        final_y = interp_func2(original_x[1:max_idx])
        
        return original_x[1:max_idx], final_y
