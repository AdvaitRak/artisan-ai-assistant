#!/usr/bin/env python3
"""
Demo script to showcase Artisan AI Assistant functionality
without requiring full dependencies
"""

import sys
import os
sys.path.append('.')

from src.config.settings import Config, LANGUAGE_CONFIG, UI_TRANSLATIONS
from src.utils.language_utils import get_ui_text, get_supported_languages
from src.utils.file_utils import get_file_size_human

def demo_configuration():
    """Demo configuration management"""
    print("🔧 Configuration Demo")
    print("=" * 50)
    
    print(f"Default Language: {Config.DEFAULT_LANGUAGE}")
    print(f"Supported Image Formats: {Config.SUPPORTED_IMAGE_FORMATS}")
    print(f"Max Image Size: {Config.MAX_IMAGE_SIZE_MB}MB")
    print(f"Platform Sizes: {Config.PLATFORM_SIZES}")
    print()

def demo_language_support():
    """Demo multilingual support"""
    print("🌐 Language Support Demo")
    print("=" * 50)
    
    languages = get_supported_languages()
    for lang in languages:
        print(f"Language: {lang['name']} ({lang['code']})")
        title = get_ui_text(lang['code'], 'title', 'Artisan AI Assistant')
        print(f"  Title: {title}")
        upload = get_ui_text(lang['code'], 'upload_image', 'Upload Image')
        print(f"  Upload: {upload}")
        print()

def demo_ui_translations():
    """Demo UI text translations"""
    print("📝 UI Translations Demo")
    print("=" * 50)
    
    sample_keys = ['title', 'upload_image', 'voice_command', 'processing', 'download']
    
    for lang_code in ['hi', 'mr', 'en']:
        lang_name = LANGUAGE_CONFIG[lang_code]['name']
        print(f"\n{lang_name} ({lang_code}):")
        print("-" * 30)
        
        for key in sample_keys:
            text = get_ui_text(lang_code, key, f'[Missing: {key}]')
            print(f"  {key}: {text}")

def demo_file_utilities():
    """Demo file utility functions"""
    print("📁 File Utilities Demo")
    print("=" * 50)
    
    # Test file size formatting
    sizes = [1024, 1024*1024, 1024*1024*10, 1024*1024*1024]
    for size in sizes:
        formatted = get_file_size_human(size)
        print(f"  {size} bytes = {formatted}")
    print()

def demo_platform_optimization():
    """Demo platform-specific settings"""
    print("📱 Platform Optimization Demo")
    print("=" * 50)
    
    platforms = ['amazon', 'instagram', 'whatsapp']
    
    for platform in platforms:
        size = Config.PLATFORM_SIZES.get(platform, (0, 0))
        print(f"{platform.title():>10}: {size[0]}×{size[1]}px")
    print()

def demo_service_availability():
    """Demo service availability checking"""
    print("🔧 Service Availability Demo")
    print("=" * 50)
    
    # Simulate service checks
    services = {
        'Google Cloud Speech': False,  # Would be checked via actual service
        'Background Removal': False,   # Would be checked via rembg
        'Gemini AI': False,           # Would be checked via API key
        'Image Processing': True,      # Basic PIL functionality
        'Configuration': True          # Always available
    }
    
    for service, available in services.items():
        status = "✅" if available else "❌"
        print(f"  {status} {service}")
    print()

def main():
    """Run all demos"""
    print("🎨 ARTISAN AI ASSISTANT - DEMO")
    print("=" * 60)
    print()
    
    # Create directories
    Config.create_directories()
    print("✅ Directories created successfully")
    print()
    
    # Run all demos
    demo_configuration()
    demo_language_support()
    demo_ui_translations()
    demo_file_utilities()
    demo_platform_optimization()
    demo_service_availability()
    
    print("🎉 Demo completed successfully!")
    print()
    print("To run the full application:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up .env file with API keys")
    print("3. Run: streamlit run app.py")

if __name__ == "__main__":
    main()