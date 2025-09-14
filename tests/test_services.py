"""
Test image processing services
"""
import pytest
from PIL import Image
import io
from src.services.image_service import image_processor

def create_test_image(size=(100, 100), mode='RGB', color=(255, 0, 0)):
    """Create a test image"""
    return Image.new(mode, size, color)

def test_image_processor_initialization():
    """Test image processor initialization"""
    assert image_processor is not None

def test_image_validation():
    """Test image validation"""
    # Create test image
    test_image = create_test_image()
    
    # Convert to file-like object
    img_bytes = io.BytesIO()
    test_image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Test validation
    result = image_processor.validate_image(img_bytes)
    assert result['valid'] == True
    assert 'image' in result
    assert 'size' in result

def test_white_background_addition():
    """Test adding white background"""
    # Create RGBA image with transparency
    test_image = create_test_image(mode='RGBA', color=(255, 0, 0, 128))
    
    # Add white background
    result = image_processor.add_white_background(test_image)
    
    assert result.mode == 'RGB'
    assert result.size == test_image.size

def test_image_resize():
    """Test image resizing"""
    test_image = create_test_image(size=(200, 200))
    
    # Test resize with aspect ratio
    resized = image_processor.resize_image(test_image, (100, 100), maintain_aspect=True)
    assert resized.size == (100, 100)
    
    # Test resize without aspect ratio
    resized = image_processor.resize_image(test_image, (150, 100), maintain_aspect=False)
    assert resized.size == (150, 100)

def test_platform_processing():
    """Test platform-specific processing"""
    test_image = create_test_image()
    
    # Test Amazon processing
    result = image_processor.process_for_platform(test_image, 'amazon', remove_bg=False)
    assert result['success'] == True
    assert result['platform'] == 'amazon'
    assert 'image' in result

def test_service_availability():
    """Test service availability check"""
    availability = image_processor.is_available()
    assert isinstance(availability, dict)
    assert 'basic_processing' in availability
    assert availability['basic_processing'] == True