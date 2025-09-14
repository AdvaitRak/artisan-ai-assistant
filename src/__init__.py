"""
Main package initialization
"""
from .config import Config
from .services import voice_service, image_processor, ai_service
from .utils import get_ui_text, get_supported_languages
from .ui import *

# Initialize configuration on import
Config.create_directories()

__version__ = "1.0.0"
__all__ = [
    'Config',
    'voice_service', 
    'image_processor',
    'ai_service',
    'get_ui_text',
    'get_supported_languages'
]