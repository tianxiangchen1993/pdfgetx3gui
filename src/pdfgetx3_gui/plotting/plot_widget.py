"""Enhanced plotting widget with modern styling."""

from PyQt6 import QtWidgets, QtCore
import matplotlib
matplotlib.use('QtAgg')  # Auto-detects Qt version
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import numpy as np
from typing import Optional, List
import logging

from ..core.calculator import PDFResults
from ..utils.logger import get_logger

logger = get_logger(__name__)

# Color cycle for multiple datasets
import matplotlib.pyplot as plt
color_cycle = plt.cm.tab10.colors  # 10 distinct colors


class PlotWidget(QtWidgets.QWidget):
    """
    Enhanced matplotlib plot widget with modern styling.
    """
    
    def __init__(self, parent=None):
        """Initialize the plot widget."""
        super().__init__(parent)
        
        # Create figure with modern styling
        self.figure = Figure(figsize=(10, 7), dpi=100, facecolor='#fafafa')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background-color: #fafafa;")
        
        # Create toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # Layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Store current plots
        self.axes: List = []
        self.results: Optional[PDFResults] = None
        
        # Show welcome message
        self._show_welcome()
        
        logger.debug("Plot widget initialized")
    
    def _show_welcome(self):
        """Show welcome message when no data is plotted."""
        self.figure.clf()
        ax = self.figure.add_subplot(111)
        ax.text(
            0.5, 0.5,
            '📊 PDFgetX3 GUI v2.0\n\n'
            'Load a data file and click Calculate\n'
            'to see your PDF results here',
            horizontalalignment='center',
            verticalalignment='center',
            transform=ax.transAxes,
            fontsize=14,
            color='#999',
            style='italic'
        )
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis('off')
        self.canvas.draw()
    
    def clear_plots(self):
        """Clear all plots."""
        self._show_welcome()
        self.axes = []
        logger.debug("Plots cleared")
    
    def plot_results(
        self,
        results,  # Can be PDFResults or List[Tuple[str, PDFResults]]
        show_iq: bool = False,
        show_sq:bool = False,
        show_fq: bool = False,
        show_gr: bool = True,
        reset_axes: bool = True
    ):
        """Plot PDF results with modern styling. Supports single or multiple datasets."""
        # Handle both single result and multiple results
        if isinstance(results, list):
            # Multiple results: [(filename, result), ...]
            self.multi_results = results
            self.results = results[0][1] if results else None
            is_multi = True
        else:
            # Single result
            self.results = results
            self.multi_results = [("", results)]
            is_multi = False
        
        # Count number of plots
        plot_flags = [show_iq, show_sq, show_fq, show_gr]
        n_plots = sum(plot_flags)
        
        if n_plots == 0:
            logger.warning("No plots selected")
            self._show_welcome()
            return
        
        # Clear previous plots
        self.figure.clf()
        self.axes = []
        
        # Modern color scheme
        colors = {
            'primary': '#2196F3',
            'secondary': '#FF5722',
            'tertiary': '#4CAF50',
            'grid': '#e0e0e0',
            'text': '#333333'
        }
        
        # Create subplots
        plot_idx = 1
        
        if show_iq:
            ax = self.figure.add_subplot(n_plots, 1, plot_idx)
            self._plot_iq(ax, self.multi_results, reset_axes, colors, is_multi)
            self.axes.append(ax)
            plot_idx += 1
        
        if show_sq:
            ax = self.figure.add_subplot(n_plots, 1, plot_idx)
            self._plot_sq(ax, self.multi_results, reset_axes, colors, is_multi)
            self.axes.append(ax)
            plot_idx += 1
        
        if show_fq:
            ax = self.figure.add_subplot(n_plots, 1, plot_idx)
            self._plot_fq(ax, self.multi_results, reset_axes, colors, is_multi)
            self.axes.append(ax)
            plot_idx += 1
        
        if show_gr:
            ax = self.figure.add_subplot(n_plots, 1, plot_idx)
            self._plot_gr(ax, self.multi_results, reset_axes, colors, is_multi)
            self.axes.append(ax)
        
        # Apply modern styling
        for ax in self.axes:
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color(colors['grid'])
            ax.spines['bottom'].set_color(colors['grid'])
            ax.tick_params(colors=colors['text'], which='both')
            for label in ax.get_xticklabels() + ax.get_yticklabels():
                label.set_color(colors['text'])
        
        # Adjust layout with better spacing
        self.figure.tight_layout(pad=2.0)
        self.canvas.draw()
        
        logger.info(f"Plotted {n_plots} subplots")
    
    def _plot_iq(self, ax, multi_results, reset_axes: bool, colors: dict, is_multi: bool):
        """Plot I(Q) with modern styling. Supports multiple datasets."""
        for idx, (filename, results) in enumerate(multi_results):
            if is_multi:
                color = color_cycle[idx % len(color_cycle)]
                label_prefix = f"{filename}: " if filename else f"S{idx+1}: "
            else:
                # Single dataset - use original color scheme
                ax.plot(results.qi, results.iq, color=colors['primary'], 
                        label='Total', linewidth=2, alpha=0.9)
                ax.plot(results.qi, results.bkg, color=colors['secondary'], 
                        label='Background', linewidth=1.5, alpha=0.7, linestyle='--')
                ax.plot(results.qi, results.iq - results.bkg, color=colors['tertiary'], 
                        label='Signal', linewidth=1.5, alpha=0.7)
                
                if reset_axes:
                    ax.set_xlim(results.qi[0], results.qi[-1])
                break
            
            # Multi dataset - only plot total intensity
            ax.plot(results.qi, results.iq, color=color, 
                   label=label_prefix + "Total", linewidth=2, alpha=0.85)
            
            if reset_axes and idx == 0:
                ax.set_xlim(results.qi[0], results.qi[-1])
        
        ax.set_ylabel('I(Q)', fontsize=11, fontweight='bold', color=colors['text'])
        ax.legend(fontsize=9, loc='best', framealpha=0.9)
        ax.grid(True, alpha=0.3, linestyle=':', color=colors['grid'])
    
    def _plot_sq(self, ax, multi_results, reset_axes: bool, colors: dict, is_multi: bool):
        """Plot S(Q) with modern styling. Supports multiple datasets."""
        for idx, (filename, results) in enumerate(multi_results):
            if is_multi:
                color = color_cycle[idx % len(color_cycle)]
                label = filename if filename else f"Sample {idx+1}"
            else:
                color = colors['primary']
                label = None
            
            ax.plot(results.q, results.sq, color=color, linewidth=2, 
                   label=label, alpha=0.85)
            
            if reset_axes and idx == 0:
                ax.set_xlim(results.q[0], results.q[-1])
        
        if is_multi:
            ax.legend(fontsize=9, loc='best', framealpha=0.9)
        
        ax.set_ylabel('S(Q)', fontsize=11, fontweight='bold', color=colors['text'])
        ax.grid(True, alpha=0.3, linestyle=':', color=colors['grid'])
    
    def _plot_fq(self, ax, multi_results, reset_axes: bool, colors: dict, is_multi: bool):
        """Plot F(Q) with modern styling. Supports multiple datasets."""
        for idx, (filename, results) in enumerate(multi_results):
            if is_multi:
                color = color_cycle[idx % len(color_cycle)]
                label = filename if filename else f"Sample {idx+1}"
            else:
                color = colors['primary']
                label = None
            
            ax.plot(results.q, results.fq, color=color, linewidth=2, 
                   label=label, alpha=0.85)
            
            if reset_axes and idx == 0:
                ax.set_xlim(results.q[0], results.q[-1])
        
        if is_multi:
            ax.legend(fontsize=9, loc='best', framealpha=0.9)
        
        ax.set_xlabel('Q (Å⁻¹)', fontsize=11, fontweight='bold', color=colors['text'])
        ax.set_ylabel('F(Q)', fontsize=11, fontweight='bold', color=colors['text'])
        ax.grid(True, alpha=0.3, linestyle=':', color=colors['grid'])
    
    def _plot_gr(self, ax, multi_results, reset_axes: bool, colors: dict, is_multi: bool):
        """Plot G(r) with modern styling. Supports multiple datasets."""
        # Add zero line with subtle styling
        ax.axhline(y=0, color=colors['text'], linestyle='--', 
                   linewidth=1, alpha=0.3)
        
        # Plot each dataset
        for idx, (filename, results) in enumerate(multi_results):
            if is_multi:
                # Use color cycle for multiple datasets
                color = color_cycle[idx % len(color_cycle)]
                label = filename if filename else f"Sample {idx+1}"
            else:
                # Single dataset - use primary color, no label
                color = colors['primary']
                label = None
            
            ax.plot(results.r, results.gr, color=color, linewidth=2.5, 
                   label=label, alpha=0.85)
            
            if reset_axes and idx == 0:
                ax.set_xlim(results.r[0], results.r[-1])
        
        # Add legend if multiple datasets
        if is_multi:
            ax.legend(fontsize=9, loc='best', framealpha=0.9)
        
        ax.set_xlabel('r (Å)', fontsize=11, fontweight='bold', color=colors['text'])
        ax.set_ylabel('G(r) (Å⁻²)', fontsize=11, fontweight='bold', color=colors['text'])
        ax.grid(True, alpha=0.3, linestyle=':', color=colors['grid'])
