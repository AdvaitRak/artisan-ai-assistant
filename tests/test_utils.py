"""
Test language utilities
"""
import pytest
import sys
sys.path.append('/home/runner/work/artisan-ai-assistant/artisan-ai-assistant')
from src.utils.language_utils import (
    get_ui_text, 
    get_supported_languages, 
    detect_language_from_text,
    translate_platform_name
)

def test_get_ui_text():
    """Test UI text retrieval"""
    # Test existing keys
    title_hi = get_ui_text('hi', 'title')
    assert title_hi != ''
    assert 'शिल्पकार' in title_hi or 'Artisan' in title_hi
    
    # Test fallback
    missing_text = get_ui_text('hi', 'nonexistent_key', 'fallback')
    assert missing_text == 'fallback'

def test_get_supported_languages():
    """Test supported languages retrieval"""
    languages = get_supported_languages()
    assert isinstance(languages, list)
    assert len(languages) >= 3
    
    # Check required fields
    for lang in languages:
        assert 'code' in lang
        assert 'name' in lang
        assert 'stt_code' in lang
        assert 'tts_code' in lang

def test_detect_language_from_text():
    """Test language detection"""
    # Test Hindi text
    hindi_text = "नमस्ते, मेरा नाम राम है।"
    detected = detect_language_from_text(hindi_text)
    assert detected in ['hi', 'mr']  # Both use Devanagari
    
    # Test English text
    english_text = "Hello, my name is John."
    detected = detect_language_from_text(english_text)
    assert detected == 'en'
    
    # Test empty text
    detected = detect_language_from_text("")
    assert detected in ['hi', 'mr', 'en']

def test_translate_platform_name():
    """Test platform name translation"""
    # Test Amazon
    amazon_hi = translate_platform_name('amazon', 'hi')
    assert amazon_hi == 'Amazon'
    
    # Test Instagram
    instagram_en = translate_platform_name('instagram', 'en')
    assert instagram_en == 'Instagram'
    
    # Test unknown platform
    unknown = translate_platform_name('unknown', 'hi')
    assert unknown == 'Unknown'