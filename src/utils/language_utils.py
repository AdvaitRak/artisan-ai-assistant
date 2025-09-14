"""
Language utilities for multilingual support
"""
from typing import Dict, Any, List
from ..config import LANGUAGE_CONFIG, UI_TRANSLATIONS

def get_ui_text(language: str, key: str, default: str = '') -> str:
    """
    Get UI text in specified language
    
    Args:
        language: Language code (hi, mr, en)
        key: Text key
        default: Default text if key not found
        
    Returns:
        Localized text
    """
    return UI_TRANSLATIONS.get(language, {}).get(key, default or key)

def get_supported_languages() -> List[Dict[str, str]]:
    """
    Get list of supported languages with details
    
    Returns:
        List of language dictionaries
    """
    return [
        {
            'code': code,
            'name': config['name'],
            'stt_code': config['stt_code'],
            'tts_code': config['tts_code']
        }
        for code, config in LANGUAGE_CONFIG.items()
    ]

def detect_language_from_text(text: str) -> str:
    """
    Simple language detection based on script
    
    Args:
        text: Input text
        
    Returns:
        Detected language code
    """
    # Simple detection based on character sets
    hindi_chars = set('अआइईउऊएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ')
    marathi_chars = set('अआइईउऊएऐओऔकखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसहळ')
    
    if any(char in hindi_chars for char in text):
        # Both Hindi and Marathi use Devanagari, default to Hindi
        # Could be enhanced with more sophisticated detection
        return 'hi'
    elif any(char in marathi_chars for char in text):
        return 'mr'
    else:
        return 'en'

def translate_platform_name(platform: str, language: str) -> str:
    """
    Translate platform names to local language
    
    Args:
        platform: Platform name (amazon, instagram, whatsapp)
        language: Target language
        
    Returns:
        Translated platform name
    """
    translations = {
        'amazon': {
            'hi': 'Amazon',
            'mr': 'Amazon', 
            'en': 'Amazon'
        },
        'instagram': {
            'hi': 'Instagram',
            'mr': 'Instagram',
            'en': 'Instagram'
        },
        'whatsapp': {
            'hi': 'WhatsApp',
            'mr': 'WhatsApp',
            'en': 'WhatsApp'
        }
    }
    
    return translations.get(platform, {}).get(language, platform.title())