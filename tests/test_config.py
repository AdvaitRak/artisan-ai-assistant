"""
Test configuration settings
"""
import pytest
import os
import sys
sys.path.append('/home/runner/work/artisan-ai-assistant/artisan-ai-assistant')
from src.config.settings import Config, LANGUAGE_CONFIG, UI_TRANSLATIONS

def test_config_initialization():
    """Test configuration initialization"""
    assert Config.DEFAULT_LANGUAGE in ['hi', 'mr', 'en']
    assert Config.MAX_IMAGE_SIZE_MB > 0
    assert len(Config.SUPPORTED_IMAGE_FORMATS) > 0

def test_language_config():
    """Test language configuration"""
    for lang_code, config in LANGUAGE_CONFIG.items():
        assert 'name' in config
        assert 'code' in config
        assert 'stt_code' in config
        assert 'tts_code' in config
        assert 'tts_voice' in config

def test_ui_translations():
    """Test UI translations"""
    required_keys = ['title', 'upload_image', 'voice_command', 'processing', 'download']
    
    for lang in ['hi', 'mr', 'en']:
        assert lang in UI_TRANSLATIONS
        for key in required_keys:
            assert key in UI_TRANSLATIONS[lang]

def test_platform_sizes():
    """Test platform size configuration"""
    for platform in ['amazon', 'instagram', 'whatsapp']:
        assert platform in Config.PLATFORM_SIZES
        size = Config.PLATFORM_SIZES[platform]
        assert len(size) == 2
        assert size[0] > 0 and size[1] > 0

def test_directory_creation():
    """Test directory creation"""
    # This test would check if directories are created properly
    Config.create_directories()
    
    expected_dirs = [
        Config.UPLOAD_DIR,
        Config.DOWNLOAD_DIR,
        Config.PROCESSED_DIR,
        Config.TEMP_DIR,
        Config.AUDIO_DIR,
        'logs'
    ]
    
    for directory in expected_dirs:
        assert os.path.exists(directory)

def test_config_validation():
    """Test configuration validation"""
    # Test should check if validation works correctly
    missing = Config.validate_config()
    assert isinstance(missing, list)