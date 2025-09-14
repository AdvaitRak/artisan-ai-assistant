"""
Main package initialization
"""
from .config import Config

# Initialize configuration on import
Config.create_directories()

__version__ = "1.0.0"
__all__ = [
    'Config'
]