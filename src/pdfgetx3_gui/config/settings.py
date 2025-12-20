"""
Configuration management module.

Handles application settings, parameter persistence, and validation.
Uses JSON for configuration storage with dataclass-based models.
"""

from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import List, Optional
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class PDFParameters:
    """PDF calculation parameters with type annotations."""
    
    # Q-space parameters
    qmin: float = 1.0
    qmax: float = 23.0
    qmaxinst: float = 23.0
    
    # R-space parameters  
    rmin: float = 0.5
    rmax: float = 30.0
    rstep: float = 0.01
    
    # Processing parameters
    rpoly: float = 1.0
    bkgscale: float = 1.0
    composition: str = "LaB6"
    
    # Input format
    dataformat: str = "twotheta"  # or "QA" - default changed to twotheta
    wavelength: float = 0.270793
    
    # Resampling
    rebin_mode: str = "none"  # "none", "linear", "exponential"
    linear_gradient: float = 1.1
    exponential_constant: float = 0.0005
    
    # Lorch modification
    lorch: bool = False  # Apply Lorch modification to reduce termination ripples
    
    # Display options
    atom_density: float = 0.0
    density_extent: float = 2.0
    scale: float = 1.0
    
    # Plot selection
    show_iq: bool = False
    show_sq: bool = False
    show_fq: bool = False
    show_gr: bool = False
    
    # UI preferences
    reset_axis_on_update: bool = False
    qmax_together: bool = False
    
    def __post_init__(self):
        """Validate parameters after initialization."""
        self.validate()
    
    def validate(self) -> None:
        """Validate parameter ranges and relationships."""
        if self.qmin >= self.qmax:
            raise ValueError(f"qmin ({self.qmin}) must be less than qmax ({self.qmax})")
        if self.qmax > self.qmaxinst:
            raise ValueError(f"qmax ({self.qmax}) cannot exceed qmaxinst ({self.qmaxinst})")
        if self.rmin >= self.rmax:
            raise ValueError(f"rmin ({self.rmin}) must be less than rmax ({self.rmax})")
        if self.rstep <= 0:
            raise ValueError(f"rstep ({self.rstep}) must be positive")
        if self.dataformat not in ["QA", "twotheta"]:
            raise ValueError(f"dataformat must be 'QA' or 'twotheta', got '{self.dataformat}'")


@dataclass
class FileConfig:
    """File paths and recent files configuration."""
    
    current_file: Optional[str] = None
    current_bkg_file: Optional[str] = None
    current_data_files: List[str] = field(default_factory=list)  # For batch processing
    recent_files: List[str] = field(default_factory=list)
    recent_bkg_files: List[str] = field(default_factory=list)
    last_data_directory: Optional[str] = None  # Remember last opened folder
    last_bkg_directory: Optional[str] = None  # Remember last background folder
    max_recent: int = 10
    
    def add_recent_file(self, filepath: str, is_background: bool = False) -> None:
        """Add a file to recent files list."""
        if is_background:
            files = self.recent_bkg_files
        else:
            files = self.recent_files
        
        # Remove if already exists
        if filepath in files:
            files.remove(filepath)
        
        # Add to front
        files.insert(0, filepath)
        
        # Trim to max
        if len(files) > self.max_recent:
            files[:] = files[:self.max_recent]


class Settings:
    """Application settings manager."""
    
    DEFAULT_CONFIG_NAME = "pdfgetx3_config.json"
    
    def __init__(self, config_dir: Optional[Path] = None):
        """
        Initialize settings manager.
        
        Args:
            config_dir: Directory for config files. If None, uses package directory.
        """
        if config_dir is None:
            config_dir = Path(__file__).parent.parent
        
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / self.DEFAULT_CONFIG_NAME
        
        self.parameters = PDFParameters()
        self.file_config = FileConfig()
        
        # UI preferences
        self.language: str = 'zh'  # Language preference
        self.theme: str = 'light'  # Theme preference (light/dark)
        
        logger.info(f"Settings initialized with config at: {self.config_file}")
    
    def load(self) -> bool:
        """
        Load settings from JSON file.
        
        Returns:
            True if loaded successfully, False otherwise.
        """
        if not self.config_file.exists():
            logger.warning(f"Config file not found: {self.config_file}")
            return False
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Load parameters
            if 'parameters' in data:
                self.parameters = PDFParameters(**data['parameters'])
            
            # Load file config
            if 'file_config' in data:
                self.file_config = FileConfig(**data['file_config'])
            
            # Load UI preferences
            if 'language' in data:
                self.language = data['language']
            if 'theme' in data:
                self.theme = data['theme']
            
            logger.info("Settings loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            return False
    
    def save(self) -> bool:
        """
        Save settings to JSON file.
        
        Returns:
            True if saved successfully, False otherwise.
        """
        try:
            # Ensure directory exists
            self.config_dir.mkdir(parents=True, exist_ok=True)
            
            data = {
                'parameters': asdict(self.parameters),
                'file_config': asdict(self.file_config),
                'language': self.language,
                'theme': self.theme
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Settings saved to: {self.config_file}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False
    
    def reset_to_defaults(self) -> None:
        """Reset all settings to default values."""
        self.parameters = PDFParameters()
        self.file_config = FileConfig()
        logger.info("Settings reset to defaults")
