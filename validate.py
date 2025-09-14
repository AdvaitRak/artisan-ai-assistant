#!/usr/bin/env python3
"""
Validation script for Artisan AI Assistant
Checks all components and provides setup status
"""

import sys
import os
import importlib
from pathlib import Path

def check_file_structure():
    """Check if all required files exist"""
    print("📁 Checking File Structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        '.env.example',
        '.gitignore',
        'README.md',
        'USAGE.md',
        'src/__init__.py',
        'src/config/settings.py',
        'src/services/voice_service.py',
        'src/services/image_service.py', 
        'src/services/ai_service.py',
        'src/utils/language_utils.py',
        'src/utils/file_utils.py',
        'src/ui/voice_components.py',
        'src/ui/image_components.py',
        'static/css/style.css',
        'tests/test_config.py',
        'tests/test_utils.py',
        'tests/test_services.py'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    else:
        print("✅ All required files present")
        return True

def check_python_syntax():
    """Check Python syntax for all Python files"""
    print("\n🐍 Checking Python Syntax...")
    
    python_files = []
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    syntax_errors = []
    for py_file in python_files:
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                source = f.read()
            compile(source, py_file, 'exec')
        except SyntaxError as e:
            syntax_errors.append(f"{py_file}: {e}")
        except Exception as e:
            syntax_errors.append(f"{py_file}: {e}")
    
    if syntax_errors:
        print(f"❌ Syntax errors found:")
        for error in syntax_errors:
            print(f"   {error}")
        return False
    else:
        print(f"✅ All {len(python_files)} Python files have valid syntax")
        return True

def check_imports():
    """Check if core modules can be imported"""
    print("\n📦 Checking Core Imports...")
    
    sys.path.append('.')
    
    modules_to_check = [
        ('src.config.settings', 'Config'),
        ('src.utils.language_utils', 'get_ui_text'),
        ('src.utils.file_utils', 'get_file_size_human'),
    ]
    
    import_errors = []
    for module_name, class_or_func in modules_to_check:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, class_or_func):
                print(f"✅ {module_name}.{class_or_func}")
            else:
                import_errors.append(f"{module_name} missing {class_or_func}")
        except ImportError as e:
            import_errors.append(f"{module_name}: {e}")
        except Exception as e:
            import_errors.append(f"{module_name}: {e}")
    
    if import_errors:
        print("❌ Import errors:")
        for error in import_errors:
            print(f"   {error}")
        return False
    else:
        print("✅ All core modules import successfully")
        return True

def check_configuration():
    """Check configuration setup"""
    print("\n⚙️ Checking Configuration...")
    
    try:
        sys.path.append('.')
        from src.config.settings import Config, LANGUAGE_CONFIG, UI_TRANSLATIONS
        
        # Check basic config
        assert hasattr(Config, 'DEFAULT_LANGUAGE')
        assert hasattr(Config, 'SUPPORTED_LANGUAGES') 
        assert hasattr(Config, 'PLATFORM_SIZES')
        
        # Check language config
        assert len(LANGUAGE_CONFIG) >= 3
        for lang_code, config in LANGUAGE_CONFIG.items():
            assert 'name' in config
            assert 'stt_code' in config
            assert 'tts_code' in config
        
        # Check UI translations
        assert len(UI_TRANSLATIONS) >= 3
        for lang_code in UI_TRANSLATIONS:
            assert 'title' in UI_TRANSLATIONS[lang_code]
            assert 'upload_image' in UI_TRANSLATIONS[lang_code]
        
        print("✅ Configuration is valid")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_directories():
    """Check if necessary directories exist or can be created"""
    print("\n📂 Checking Directories...")
    
    try:
        sys.path.append('.')
        from src.config.settings import Config
        
        Config.create_directories()
        
        required_dirs = [
            Config.UPLOAD_DIR,
            Config.DOWNLOAD_DIR,
            Config.PROCESSED_DIR,
            Config.TEMP_DIR,
            Config.AUDIO_DIR,
            'logs'
        ]
        
        for directory in required_dirs:
            if os.path.exists(directory):
                print(f"✅ {directory}")
            else:
                print(f"❌ {directory} not created")
                return False
        
        print("✅ All directories created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Directory creation error: {e}")
        return False

def check_dependencies():
    """Check if dependencies are properly specified"""
    print("\n📋 Checking Dependencies...")
    
    try:
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        required_packages = [
            'streamlit',
            'google-cloud-speech',
            'google-cloud-texttospeech', 
            'google-generativeai',
            'Pillow',
            'numpy',
            'python-dotenv'
        ]
        
        missing_deps = []
        for package in required_packages:
            if not any(package.lower() in req.lower() for req in requirements):
                missing_deps.append(package)
        
        if missing_deps:
            print(f"❌ Missing dependencies: {missing_deps}")
            return False
        else:
            print(f"✅ All {len(required_packages)} core dependencies specified")
            return True
            
    except Exception as e:
        print(f"❌ Error checking dependencies: {e}")
        return False

def main():
    """Run all validation checks"""
    print("🎨 ARTISAN AI ASSISTANT - VALIDATION")
    print("=" * 60)
    
    checks = [
        check_file_structure,
        check_python_syntax,
        check_imports,
        check_configuration,
        check_directories,
        check_dependencies
    ]
    
    results = []
    for check in checks:
        result = check()
        results.append(result)
    
    print("\n" + "=" * 60)
    print("📊 VALIDATION SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"🎉 ALL CHECKS PASSED ({passed}/{total})")
        print("\n✅ Your Artisan AI Assistant is ready!")
        print("\nNext steps:")
        print("1. Set up your .env file with API keys")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Run the app: streamlit run app.py")
    else:
        print(f"⚠️  SOME CHECKS FAILED ({passed}/{total})")
        print(f"\n❌ {total - passed} issues need to be resolved")
        print("\nPlease fix the issues above and run validation again.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)