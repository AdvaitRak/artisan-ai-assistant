"""
File utilities for handling uploads and downloads
"""
import os
import io
import zipfile
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
from PIL import Image
from ..config import Config

logger = logging.getLogger(__name__)

def save_uploaded_file(uploaded_file, directory: str = None) -> Dict[str, Any]:
    """
    Save uploaded file to specified directory
    
    Args:
        uploaded_file: Streamlit uploaded file object
        directory: Target directory (default: uploads)
        
    Returns:
        Dictionary with file info and path
    """
    try:
        if directory is None:
            directory = Config.UPLOAD_DIR
        
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{uploaded_file.name}"
        filepath = os.path.join(directory, filename)
        
        # Save file
        with open(filepath, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        return {
            'success': True,
            'filepath': filepath,
            'filename': filename,
            'original_name': uploaded_file.name,
            'size': uploaded_file.size,
            'timestamp': timestamp
        }
        
    except Exception as e:
        logger.error(f"Failed to save uploaded file: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def save_processed_image(image: Image.Image, filename: str, 
                        directory: str = None, format: str = 'JPEG') -> Dict[str, Any]:
    """
    Save processed image to specified directory
    
    Args:
        image: PIL Image object
        filename: Filename without extension
        directory: Target directory (default: processed_images)
        format: Image format (JPEG, PNG)
        
    Returns:
        Dictionary with save result and path
    """
    try:
        if directory is None:
            directory = Config.PROCESSED_DIR
        
        # Create directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Add appropriate extension
        extension = '.jpg' if format.upper() == 'JPEG' else '.png'
        full_filename = f"{filename}{extension}"
        filepath = os.path.join(directory, full_filename)
        
        # Save image with appropriate quality
        save_kwargs = {
            'format': format.upper(),
            'optimize': True
        }
        
        if format.upper() == 'JPEG':
            save_kwargs['quality'] = Config.OUTPUT_IMAGE_QUALITY
        
        image.save(filepath, **save_kwargs)
        
        return {
            'success': True,
            'filepath': filepath,
            'filename': full_filename,
            'format': format,
            'size': image.size
        }
        
    except Exception as e:
        logger.error(f"Failed to save processed image: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def create_download_package(images: List[Dict], captions: Dict, 
                          package_name: str = None) -> Dict[str, Any]:
    """
    Create downloadable ZIP package with images and captions
    
    Args:
        images: List of image dictionaries with filepath and metadata
        captions: Dictionary with captions and hashtags
        package_name: Name for the package (default: timestamp)
        
    Returns:
        Dictionary with package info and download path
    """
    try:
        if package_name is None:
            package_name = f"artisan_package_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        download_dir = Config.DOWNLOAD_DIR
        os.makedirs(download_dir, exist_ok=True)
        
        package_path = os.path.join(download_dir, f"{package_name}.zip")
        
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add images
            for i, img_info in enumerate(images):
                if img_info.get('success') and os.path.exists(img_info['filepath']):
                    # Use platform-specific name
                    platform = img_info.get('platform', f'image_{i+1}')
                    ext = os.path.splitext(img_info['filepath'])[1]
                    zip_filename = f"{platform}_optimized{ext}"
                    zipf.write(img_info['filepath'], zip_filename)
            
            # Add captions file
            if captions:
                caption_content = create_caption_file_content(captions)
                zipf.writestr("captions_and_hashtags.txt", caption_content)
        
        return {
            'success': True,
            'package_path': package_path,
            'package_name': f"{package_name}.zip",
            'size': os.path.getsize(package_path)
        }
        
    except Exception as e:
        logger.error(f"Failed to create download package: {e}")
        return {
            'success': False,
            'error': str(e)
        }

def create_caption_file_content(captions: Dict) -> str:
    """
    Create formatted content for captions file
    
    Args:
        captions: Dictionary with captions and hashtags
        
    Returns:
        Formatted text content
    """
    content = "🎨 ARTISAN AI ASSISTANT - GENERATED CONTENT\n"
    content += "=" * 50 + "\n\n"
    
    for platform, data in captions.items():
        if isinstance(data, dict):
            content += f"📱 {platform.upper()} CONTENT:\n"
            content += "-" * 30 + "\n"
            
            if 'caption' in data:
                content += f"Caption: {data['caption']}\n\n"
            
            if 'hashtags' in data and data['hashtags']:
                content += f"Hashtags: {' '.join(data['hashtags'])}\n\n"
            
            if 'description' in data:
                content += f"Description: {data['description']}\n\n"
            
            content += "\n"
    
    content += "Generated by Artisan AI Assistant\n"
    content += f"Created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    
    return content

def cleanup_temp_files(max_age_hours: int = 24):
    """
    Clean up temporary files older than specified hours
    
    Args:
        max_age_hours: Maximum age of files to keep in hours
    """
    try:
        current_time = datetime.now().timestamp()
        max_age_seconds = max_age_hours * 3600
        
        directories_to_clean = [
            Config.UPLOAD_DIR,
            Config.TEMP_DIR,
            Config.AUDIO_DIR
        ]
        
        for directory in directories_to_clean:
            if os.path.exists(directory):
                for filename in os.listdir(directory):
                    filepath = os.path.join(directory, filename)
                    if os.path.isfile(filepath):
                        file_age = current_time - os.path.getmtime(filepath)
                        if file_age > max_age_seconds:
                            try:
                                os.remove(filepath)
                                logger.info(f"Cleaned up old file: {filepath}")
                            except Exception as e:
                                logger.warning(f"Failed to remove {filepath}: {e}")
        
    except Exception as e:
        logger.error(f"Cleanup failed: {e}")

def get_file_size_human(size_bytes: int) -> str:
    """
    Convert file size to human readable format
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Human readable size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"