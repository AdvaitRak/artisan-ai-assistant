"""
Image processing service for background removal and enhancement
"""
import os
import io
from typing import Tuple, Optional, Dict, Any
import logging
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    logging.warning("OpenCV not available")

try:
    from rembg import remove, new_session
    REMBG_AVAILABLE = True
except ImportError:
    REMBG_AVAILABLE = False
    logging.warning("rembg not available")

from ..config import Config

logger = logging.getLogger(__name__)

class ImageProcessor:
    """Handles image processing operations"""
    
    def __init__(self):
        self.rembg_session = None
        if REMBG_AVAILABLE:
            try:
                # Initialize rembg session for product images
                self.rembg_session = new_session('u2net')
                logger.info("Background removal service initialized")
            except Exception as e:
                logger.error(f"Failed to initialize background removal: {e}")
    
    def remove_background(self, image: Image.Image) -> Image.Image:
        """
        Remove background from image
        
        Args:
            image: PIL Image object
            
        Returns:
            Image with transparent background
        """
        if not REMBG_AVAILABLE or not self.rembg_session:
            logger.warning("Background removal not available, returning original image")
            return image
        
        try:
            # Convert PIL to bytes
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Remove background
            output = remove(img_byte_arr, session=self.rembg_session)
            
            # Convert back to PIL
            result_image = Image.open(io.BytesIO(output))
            
            logger.info("Background removed successfully")
            return result_image
            
        except Exception as e:
            logger.error(f"Background removal failed: {e}")
            return image
    
    def add_white_background(self, image: Image.Image) -> Image.Image:
        """
        Add white background to transparent image
        
        Args:
            image: PIL Image object (can have transparency)
            
        Returns:
            Image with white background
        """
        try:
            # Create white background
            white_bg = Image.new('RGB', image.size, (255, 255, 255))
            
            if image.mode == 'RGBA':
                # Composite with white background
                white_bg.paste(image, mask=image.split()[-1])
            else:
                # Convert to RGB if necessary
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                white_bg = image
            
            return white_bg
            
        except Exception as e:
            logger.error(f"Failed to add white background: {e}")
            return image.convert('RGB')
    
    def enhance_image(self, image: Image.Image, platform: str = 'amazon') -> Image.Image:
        """
        Enhance image for specific platform
        
        Args:
            image: PIL Image object
            platform: Target platform ('amazon', 'instagram', 'whatsapp')
            
        Returns:
            Enhanced image
        """
        try:
            # Get target size for platform
            target_size = Config.PLATFORM_SIZES.get(platform, (1000, 1000))
            
            # Enhance image quality
            enhanced = image
            
            # Adjust brightness slightly
            enhancer = ImageEnhance.Brightness(enhanced)
            enhanced = enhancer.enhance(1.05)
            
            # Increase contrast slightly
            enhancer = ImageEnhance.Contrast(enhanced)
            enhanced = enhancer.enhance(1.1)
            
            # Sharpen the image
            enhanced = enhanced.filter(ImageFilter.UnsharpMask(radius=1, percent=150, threshold=3))
            
            # Resize to platform requirements
            enhanced = self.resize_image(enhanced, target_size, maintain_aspect=True)
            
            logger.info(f"Image enhanced for {platform}: {enhanced.size}")
            return enhanced
            
        except Exception as e:
            logger.error(f"Image enhancement failed: {e}")
            return image
    
    def resize_image(self, image: Image.Image, size: Tuple[int, int], 
                    maintain_aspect: bool = True) -> Image.Image:
        """
        Resize image to specified dimensions
        
        Args:
            image: PIL Image object
            size: Target size (width, height)
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Resized image
        """
        try:
            if maintain_aspect:
                # Calculate size maintaining aspect ratio
                image.thumbnail(size, Image.Resampling.LANCZOS)
                
                # Create new image with target size and center the resized image
                new_image = Image.new('RGB', size, (255, 255, 255))
                
                # Calculate position to center the image
                x = (size[0] - image.size[0]) // 2
                y = (size[1] - image.size[1]) // 2
                
                if image.mode == 'RGBA':
                    new_image.paste(image, (x, y), image)
                else:
                    new_image.paste(image, (x, y))
                
                return new_image
            else:
                # Resize without maintaining aspect ratio
                return image.resize(size, Image.Resampling.LANCZOS)
                
        except Exception as e:
            logger.error(f"Image resize failed: {e}")
            return image
    
    def process_for_platform(self, image: Image.Image, platform: str = 'amazon',
                           remove_bg: bool = True) -> Dict[str, Any]:
        """
        Complete processing pipeline for specific platform
        
        Args:
            image: Input PIL Image object
            platform: Target platform ('amazon', 'instagram', 'whatsapp')
            remove_bg: Whether to remove background
            
        Returns:
            Dictionary with processed image and metadata
        """
        try:
            processed_image = image.copy()
            
            # Step 1: Remove background if requested
            if remove_bg:
                processed_image = self.remove_background(processed_image)
            
            # Step 2: Add white background (important for e-commerce)
            if platform == 'amazon':
                processed_image = self.add_white_background(processed_image)
            
            # Step 3: Enhance image
            processed_image = self.enhance_image(processed_image, platform)
            
            # Get final dimensions
            final_size = processed_image.size
            
            return {
                'success': True,
                'image': processed_image,
                'platform': platform,
                'size': final_size,
                'background_removed': remove_bg,
                'format': 'PNG' if processed_image.mode == 'RGBA' else 'JPEG'
            }
            
        except Exception as e:
            logger.error(f"Image processing failed for {platform}: {e}")
            return {
                'success': False,
                'error': str(e),
                'image': image,
                'platform': platform
            }
    
    def validate_image(self, image_file) -> Dict[str, Any]:
        """
        Validate uploaded image file
        
        Args:
            image_file: Uploaded file object
            
        Returns:
            Validation result
        """
        try:
            # Check file size
            file_size_mb = len(image_file.read()) / (1024 * 1024)
            image_file.seek(0)  # Reset file pointer
            
            if file_size_mb > Config.MAX_IMAGE_SIZE_MB:
                return {
                    'valid': False,
                    'error': f'File size ({file_size_mb:.1f}MB) exceeds limit ({Config.MAX_IMAGE_SIZE_MB}MB)'
                }
            
            # Try to open image
            image = Image.open(image_file)
            
            # Check format
            format_lower = image.format.lower() if image.format else ''
            if format_lower not in [fmt.lower() for fmt in Config.SUPPORTED_IMAGE_FORMATS]:
                return {
                    'valid': False,
                    'error': f'Unsupported format: {image.format}. Supported: {Config.SUPPORTED_IMAGE_FORMATS}'
                }
            
            return {
                'valid': True,
                'image': image,
                'size': image.size,
                'format': image.format,
                'mode': image.mode,
                'file_size_mb': file_size_mb
            }
            
        except Exception as e:
            return {
                'valid': False,
                'error': f'Invalid image file: {str(e)}'
            }
    
    def is_available(self) -> Dict[str, bool]:
        """Check availability of image processing features"""
        return {
            'background_removal': REMBG_AVAILABLE and self.rembg_session is not None,
            'opencv': CV2_AVAILABLE,
            'basic_processing': True
        }

# Global image processor instance
image_processor = ImageProcessor()