"""
Setup configuration for PDFgetX3 GUI v2.0
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements
requirements = []
with open('requirements.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith('#') and not line.startswith('conda'):
            requirements.append(line)

setup(
    name="pdfgetx3gui-v2",
    version="2.0.0",
    author="Optimized by AI Assistant, Original by Kenneth P. Marshall",
    description="Modern GUI for PDFgetX3 - Pair Distribution Function Analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msujas/pdfgetx3_gui",
    
    # Package configuration
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    
    # Dependencies
    install_requires=requirements,
    
    # Python version requirement
    python_requires=">=3.8",
    
    # Entry points for command-line scripts
    entry_points={
        "console_scripts": [
            "pdfgetx3gui=pdfgetx3_gui.main:main",
            "pdfgetx3gui-v2=pdfgetx3_gui.main:main",
        ],
    },
    
    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
    ],
    
    # Additional metadata
    keywords="pdf pair-distribution-function x-ray neutron scattering diffraction",
    project_urls={
        "Bug Reports": "https://github.com/msujas/pdfgetx3_gui/issues",
        "Source": "https://github.com/msujas/pdfgetx3_gui",
        "Documentation": "https://www.diffpy.org/products/pdfgetx.html",
    },
    
    # Include package data
    include_package_data=True,
    zip_safe=False,
)
