"""
Configuration management for Artisan AI Assistant
"""
import os
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Google Cloud Configuration
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_CLOUD_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT_ID')
    
    # Speech-to-Text Configuration
    STT_LANGUAGE_CODES = {
        'hi': os.getenv('GOOGLE_STT_LANGUAGE_CODE', 'hi-IN'),
        'mr': os.getenv('GOOGLE_STT_LANGUAGE_CODE_MARATHI', 'mr-IN'),
        'en': os.getenv('GOOGLE_STT_LANGUAGE_CODE_ENGLISH', 'en-US')
    }
    
    # Text-to-Speech Configuration
    TTS_LANGUAGE_CODE = os.getenv('GOOGLE_TTS_LANGUAGE_CODE', 'hi-IN')
    TTS_VOICE_NAME = os.getenv('GOOGLE_TTS_VOICE_NAME', 'hi-IN-Neural2-A')
    
    # Gemini AI Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-pro')
    
    # OpenAI Configuration (Alternative)
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    
    # Image Processing Settings
    MAX_IMAGE_SIZE_MB = int(os.getenv('MAX_IMAGE_SIZE_MB', '10'))
    SUPPORTED_IMAGE_FORMATS = os.getenv('SUPPORTED_IMAGE_FORMATS', 'jpg,jpeg,png,webp').split(',')
    OUTPUT_IMAGE_QUALITY = int(os.getenv('OUTPUT_IMAGE_QUALITY', '95'))
    
    # UI Configuration
    STREAMLIT_SERVER_PORT = int(os.getenv('STREAMLIT_SERVER_PORT', '8501'))
    STREAMLIT_SERVER_ADDRESS = os.getenv('STREAMLIT_SERVER_ADDRESS', 'localhost')
    STREAMLIT_THEME_PRIMARY_COLOR = os.getenv('STREAMLIT_THEME_PRIMARY_COLOR', '#FF6B6B')
    
    # Language Settings
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'hi')
    SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'hi,mr,en').split(',')
    
    # Platform Optimization Settings
    PLATFORM_SIZES = {
        'amazon': tuple(map(int, os.getenv('AMAZON_IMAGE_SIZE', '1000x1000').split('x'))),
        'instagram': tuple(map(int, os.getenv('INSTAGRAM_IMAGE_SIZE', '1080x1080').split('x'))),
        'whatsapp': tuple(map(int, os.getenv('WHATSAPP_IMAGE_SIZE', '640x640').split('x')))
    }
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = os.getenv('LOG_FILE', 'logs/app.log')
    
    # Feature Flags
    ENABLE_VOICE_FEEDBACK = os.getenv('ENABLE_VOICE_FEEDBACK', 'true').lower() == 'true'
    ENABLE_BEFORE_AFTER_COMPARISON = os.getenv('ENABLE_BEFORE_AFTER_COMPARISON', 'true').lower() == 'true'
    ENABLE_BATCH_PROCESSING = os.getenv('ENABLE_BATCH_PROCESSING', 'false').lower() == 'true'
    
    # Directories
    UPLOAD_DIR = 'uploads'
    DOWNLOAD_DIR = 'downloads'
    PROCESSED_DIR = 'processed_images'
    STATIC_DIR = 'static'
    TEMP_DIR = 'temp'
    AUDIO_DIR = 'audio_files'
    
    @classmethod
    def create_directories(cls):
        """Create necessary directories if they don't exist"""
        directories = [
            cls.UPLOAD_DIR,
            cls.DOWNLOAD_DIR, 
            cls.PROCESSED_DIR,
            cls.TEMP_DIR,
            cls.AUDIO_DIR,
            'logs'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @classmethod
    def validate_config(cls) -> List[str]:
        """Validate required configuration and return list of missing items"""
        missing = []
        
        if not cls.GEMINI_API_KEY:
            missing.append('GEMINI_API_KEY')
            
        if not cls.GOOGLE_APPLICATION_CREDENTIALS:
            missing.append('GOOGLE_APPLICATION_CREDENTIALS')
            
        if not cls.GOOGLE_CLOUD_PROJECT_ID:
            missing.append('GOOGLE_CLOUD_PROJECT_ID')
            
        return missing

# Language-specific configurations
LANGUAGE_CONFIG = {
    'hi': {
        'name': 'हिंदी',
        'code': 'hi',
        'stt_code': 'hi-IN',
        'tts_code': 'hi-IN',
        'tts_voice': 'hi-IN-Neural2-A'
    },
    'mr': {
        'name': 'मराठी', 
        'code': 'mr',
        'stt_code': 'mr-IN',
        'tts_code': 'mr-IN',
        'tts_voice': 'mr-IN-Standard-A'
    },
    'en': {
        'name': 'English',
        'code': 'en',
        'stt_code': 'en-US',
        'tts_code': 'en-US',
        'tts_voice': 'en-US-Neural2-D'
    }
}

# UI Text Translations
UI_TRANSLATIONS = {
    'hi': {
        'title': '🎨 शिल्पकार AI सहायक',
        'upload_image': 'उत्पाद की तस्वीर अपलोड करें',
        'voice_command': 'आवाज़ में बताएं कि आप क्या चाहते हैं',
        'processing': 'प्रसंस्करण हो रहा है...',
        'download': 'डाउनलोड करें',
        'amazon_ready': 'Amazon के लिए तैयार',
        'instagram_ready': 'Instagram के लिए तैयार',
        'whatsapp_ready': 'WhatsApp के लिए तैयार'
    },
    'mr': {
        'title': '🎨 कारागीर AI सहाय्यक',
        'upload_image': 'उत्पादनाचा फोटो अपलोड करा',
        'voice_command': 'आवाजात सांगा तुम्हाला काय हवे',
        'processing': 'प्रक्रिया सुरू आहे...',
        'download': 'डाउनलोड करा',
        'amazon_ready': 'Amazon साठी तयार',
        'instagram_ready': 'Instagram साठी तयार', 
        'whatsapp_ready': 'WhatsApp साठी तयार'
    },
    'en': {
        'title': '🎨 Artisan AI Assistant',
        'upload_image': 'Upload Product Photo',
        'voice_command': 'Tell us what you want via voice',
        'processing': 'Processing...',
        'download': 'Download',
        'amazon_ready': 'Amazon Ready',
        'instagram_ready': 'Instagram Ready',
        'whatsapp_ready': 'WhatsApp Ready'
    }
}