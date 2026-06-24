"""
Core calculation module.

Implements PDF calculation logic with proper separation from GUI.
Wraps diffpy.pdfgetx functionality with type-safe interfaces.
"""

from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np
import logging

from diffpy.pdfgetx import PDFConfig, PDFGetter

from ..config.settings import PDFParameters

logger = logging.getLogger(__name__)


@dataclass
class PDFResults:
    """Container for PDF calculation results with type annotations."""
    
    qi: np.ndarray  # Q values for I(Q)
    iq: np.ndarray  # Intensity I(Q)
    iq_orig: np.ndarray  # Original intensity before background subtraction
    bkg: np.ndarray  # Background
    q: np.ndarray  # Q values for S(Q) and F(Q)
    sq: np.ndarray  # Structure factor S(Q)
    fq: np.ndarray  # Reduced structure function F(Q)
    r: np.ndarray  # r values for G(r)
    gr: np.ndarray  # Pair distribution function G(r)
    
    # Optional: Lorch-corrected data (if Lorch modification was applied)
    fq_lorch: Optional[np.ndarray] = None  # Lorch-corrected F(Q)
    gr_lorch: Optional[np.ndarray] = None  # Lorch-corrected G(r)
    fq_orig: Optional[np.ndarray] = None  # Original F(Q) before Lorch
    gr_orig: Optional[np.ndarray] = None  # Original G(r) before Lorch
    
    def __repr__(self) -> str:
        lorch_str = " (with Lorch)" if self.fq_lorch is not None else ""
        return (f"PDFResults(qi: {len(self.qi)} points, "
                f"q: {len(self.q)} points, r: {len(self.r)} points){lorch_str}")


class PDFCalculator:
    """
    PDF calculation engine.
    
    Handles PDF calculations using diffpy.pdfgetx with improved error handling
    and type safety.
    """
    
    def __init__(self):
        """Initialize the PDF calculator."""
        self.last_results: Optional[PDFResults] =None
        logger.info("PDFCalculator initialized")
    
    def calculate(
        self,
        params: PDFParameters,
        file: Optional[str] = None,
        bkgfile: Optional[str] = None,
        x_data: Optional[np.ndarray] = None,
        y_data: Optional[np.ndarray] = None
    ) -> PDFResults:
        """
        Perform PDF calculation.
        
        Args:
            params: PDF calculation parameters
            file: Path to data file (if not using x_data/y_data)
            bkgfile: Path to background file
            x_data: X data array (alternative to file)
            y_data: Y data array (alternative to file)
        
        Returns:
            PDFResults object containing all calculated functions
        
        Raises:
            ValueError: If invalid parameters or input data
            RuntimeError: If calculation fails
        """
        # Validate input
        if file is None and (x_data is None or y_data is None):
            raise ValueError("Must provide either file path or x_data/y_data arrays")
        
        # Validate parameters
        params.validate()
        
        try:
            # Create PDFgetX3 configuration
            config = self._create_config(params, bkgfile)
            
            # Create PDF calculator instance
            pdfcalc = PDFGetter(config=config)
            
            # Run calculation
            if x_data is not None and y_data is not None:
                pdfcalc(x_data, y_data)
            else:
                pdfcalc(filename=file)
            
            # Extract results
            results = self._extract_results(pdfcalc)
            
            # Apply Lorch modification if requested
            if params.lorch:
                logger.info("Applying Lorch modification")
                results = self._apply_lorch_modification(results, params.qmax)
            
            self.last_results = results
            logger.info(f"PDF calculation successful: {results}")
            
            return results
            
        except Exception as e:
            logger.error(f"PDF calculation failed: {e}")
            raise RuntimeError(f"PDF calculation failed: {e}") from e
    
    def _create_config(
        self,
        params: PDFParameters,
        bkgfile: Optional[str]
    ) -> PDFConfig:
        """Create PDFConfig from parameters."""
        config = PDFConfig(
            bgscale=params.bkgscale,
            qmin=params.qmin,
            qmax=params.qmax,
            qmaxinst=params.qmaxinst,
            dataformat=params.dataformat,
            rpoly=params.rpoly,
            composition=params.composition,
            backgroundfile=bkgfile if bkgfile else "",
            rmin=params.rmin,
            rmax=params.rmax,
            rstep=params.rstep
        )
        
        if params.dataformat == "twotheta":
            config.wavelength = params.wavelength
        
        return config
    
    def _extract_results(self, pdfcalc: PDFGetter) -> PDFResults:
        """Extract results from PDFGetter instance."""
        # Get pair distribution function
        r = pdfcalc.gr[0]
        gr = pdfcalc.gr[1]
        
        # Get reduced structure functions
        fq = pdfcalc.fq[1]
        sq = pdfcalc.sq[1]
        q = pdfcalc.sq[0]
        
        # Get intensity
        iq = pdfcalc.iq[1]
        qi = pdfcalc.iq[0]
        iq_orig = pdfcalc.results[2][1]
        
        # Calculate background
        bkg = iq_orig - iq
        
        return PDFResults(
            qi=qi,
            iq=iq,
            iq_orig=iq_orig,
            bkg=bkg,
            q=q,
            sq=sq,
            fq=fq,
            r=r,
            gr=gr
        )
    
    def save_results(
        self,
        results: PDFResults,
        basename: str,
        save_iq: bool = True,
        save_sq: bool = True,
        save_fq: bool = True,
        save_gr: bool = True,
        create_dirs: bool = True
    ) -> None:
        """
        Save calculation results to files.
        
        Args:
            results: PDFResults to save
            basename: Base filename/path
            save_iq: Save I(Q)
            save_sq: Save S(Q)
            save_fq: Save F(Q)
            save_gr: Save G(r)
            create_dirs: Create output directories
        """
        from pathlib import Path
        
        base_path = Path(basename)
        out_dir = base_path.parent
        file_base = base_path.stem
        
        if create_dirs:
            (out_dir / "gr").mkdir(parents=True, exist_ok=True)
            (out_dir / "fq").mkdir(parents=True, exist_ok=True)
            (out_dir / "sq").mkdir(parents=True, exist_ok=True)
        
        try:
            if save_iq:
                iq_file = out_dir / f"{file_base}.iq"
                np.savetxt(iq_file, np.column_stack([results.qi, results.iq]))
                logger.info(f"Saved I(Q) to {iq_file}")
            
            if save_sq:
                sq_file = out_dir / "sq" / f"{file_base}.sq"
                np.savetxt(sq_file, np.column_stack([results.q, results.sq]))
                logger.info(f"Saved S(Q) to {sq_file}")
            
            if save_fq:
                fq_file = out_dir / "fq" / f"{file_base}.fq"
                np.savetxt(fq_file, np.column_stack([results.q, results.fq]))
                logger.info(f"Saved F(Q) to {fq_file}")
            
            if save_gr:
                gr_file = out_dir / "gr" / f"{file_base}.gr"
                np.savetxt(gr_file, np.column_stack([results.r, results.gr]))
                logger.info(f"Saved G(r) to {gr_file}")
                
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            raise
    
    def _apply_lorch_modification(
        self, 
        results: PDFResults, 
        qmax: float
    ) -> PDFResults:
        """
        Apply Lorch modification to reduce termination ripples in PDF.
        
        The Lorch function M(Q) = sin(πQ/Qmax) / (πQ/Qmax) smoothly damps
        F(Q) near Qmax, reducing spurious oscillations in G(r).
        
        Args:
            results: Original PDF calculation results
            qmax: Maximum Q value for normalization
        
        Returns:
            Modified PDFResults with Lorch correction applied
        """
        # Calculate Lorch modification function
        lorch_func = self._lorch_function(results.q, qmax)
        
        # Apply to F(Q)
        fq_modified = results.fq * lorch_func
        
        # Recalculate G(r) from modified F(Q)
        # G(r) = (2/π) ∫ Q*F(Q)*sin(Qr) dQ
        gr_modified = self._fourier_transform(
            results.r, 
            results.q, 
            fq_modified
        )
        
        # Create new results with modified values and save originals
        modified_results = PDFResults(
            qi=results.qi,
            iq=results.iq,
            iq_orig=results.iq_orig,
            bkg=results.bkg,
            q=results.q,
            sq=results.sq,
            fq=fq_modified,  # This is the Lorch-corrected version
            r=results.r,
            gr=gr_modified,  # This is the Lorch-corrected version
            # Store both original and Lorch-corrected versions
            fq_orig=results.fq,  # Original F(Q) before Lorch
            gr_orig=results.gr,  # Original G(r) before Lorch
            fq_lorch=fq_modified,  # Lorch-corrected F(Q)
            gr_lorch=gr_modified   # Lorch-corrected G(r)
        )
        
        logger.info("Lorch modification applied successfully")
        return modified_results
    
    @staticmethod
    def _lorch_function(Q: np.ndarray, Qmax: float) -> np.ndarray:
        """
        Calculate Lorch modification function.
        
        M(Q) = sin(πQ/Qmax) / (πQ/Qmax) = sinc(Q/Qmax)
        
        Args:
            Q: Q values array
            Qmax: Maximum Q value for normalization
        
        Returns:
            Lorch modification function values
        """
        # Using numpy's sinc function: sinc(x) = sin(πx)/(πx)
        # So sinc(Q/Qmax) = sin(πQ/Qmax) / (πQ/Qmax)
        return np.sinc(Q / Qmax)
    
    @staticmethod
    def _fourier_transform(
        r: np.ndarray, 
        q: np.ndarray, 
        fq: np.ndarray
    ) -> np.ndarray:
        """
        Fourier transform F(Q) to G(r).
        
        G(r) = (2/π) ∫ Q*F(Q)*sin(Qr) dQ
        
        Args:
            r: r-space array
            q: Q-space array
            fq: F(Q) values
        
        Returns:
            G(r) values
        """
        gr = np.zeros_like(r)
        
        # Numerical integration using trapezoidal rule
        for i, r_val in enumerate(r):
            # Integrand: Q * F(Q) * sin(Qr)
            integrand = q * fq * np.sin(q * r_val)
            # Integrate and apply prefactor
            gr[i] = (2.0 / np.pi) * np.trapezoid(integrand, q)
        
        return gr
