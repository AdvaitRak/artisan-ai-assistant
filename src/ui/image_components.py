"""
Image processing UI components
"""
import streamlit as st
from typing import Dict, Any, Optional, List
from PIL import Image
import io

from ..services import image_processor, ai_service
from ..utils import get_ui_text, save_uploaded_file, save_processed_image, get_file_size_human
from ..config import Config

def render_image_upload(language: str = 'hi') -> Optional[Image.Image]:
    """
    Render image upload component
    
    Args:
        language: Current language setting
        
    Returns:
        Uploaded PIL Image or None
    """
    st.subheader(get_ui_text(language, 'upload_image', '📷 Upload Product Photo'))
    
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=Config.SUPPORTED_IMAGE_FORMATS,
        help=f"Supported formats: {', '.join(Config.SUPPORTED_IMAGE_FORMATS)}\nMax size: {Config.MAX_IMAGE_SIZE_MB}MB"
    )
    
    if uploaded_file is not None:
        # Validate image
        validation = image_processor.validate_image(uploaded_file)
        
        if validation['valid']:
            # Display image info
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.image(validation['image'], caption="Original Image", use_column_width=True)
            
            with col2:
                st.write("**Image Details:**")
                st.write(f"📐 Size: {validation['size'][0]} × {validation['size'][1]}")
                st.write(f"📁 Format: {validation['format']}")
                st.write(f"💾 File Size: {get_file_size_human(uploaded_file.size)}")
                st.write(f"🎨 Mode: {validation['mode']}")
            
            return validation['image']
        else:
            st.error(f"❌ {validation['error']}")
    
    return None

def render_platform_selector(language: str = 'hi') -> str:
    """
    Render platform selection component
    
    Args:
        language: Current language setting
        
    Returns:
        Selected platform
    """
    platform_options = {
        '🛒 Amazon': 'amazon',
        '📱 Instagram': 'instagram', 
        '💬 WhatsApp': 'whatsapp'
    }
    
    selected = st.selectbox(
        "🎯 Target Platform / लक्ष्य प्लेटफॉर्म / लक्ष्य प्लॅटफॉर्म",
        options=list(platform_options.keys()),
        help="Choose the platform where you'll use this image"
    )
    
    return platform_options[selected]

def render_processing_options(language: str = 'hi') -> Dict[str, Any]:
    """
    Render image processing options
    
    Args:
        language: Current language setting
        
    Returns:
        Processing options dictionary
    """
    st.subheader("⚙️ Processing Options")
    
    col1, col2 = st.columns(2)
    
    with col1:
        remove_bg = st.checkbox(
            "🎨 Remove Background",
            value=True,
            help="Remove background and add clean white background"
        )
        
        enhance_quality = st.checkbox(
            "✨ Enhance Quality", 
            value=True,
            help="Improve brightness, contrast, and sharpness"
        )
    
    with col2:
        auto_resize = st.checkbox(
            "📐 Auto Resize for Platform",
            value=True, 
            help="Automatically resize to platform requirements"
        )
        
        add_watermark = st.checkbox(
            "🏷️ Add Artisan Watermark",
            value=False,
            help="Add small watermark to identify as artisan-made"
        )
    
    return {
        'remove_background': remove_bg,
        'enhance_quality': enhance_quality,
        'auto_resize': auto_resize,
        'add_watermark': add_watermark
    }

def render_image_processing(image: Image.Image, platform: str, options: Dict, 
                          voice_input: str = '', language: str = 'hi') -> Dict[str, Any]:
    """
    Render image processing interface and execute processing
    
    Args:
        image: Input PIL Image
        platform: Target platform
        options: Processing options
        voice_input: Voice command context
        language: Current language
        
    Returns:
        Processing results
    """
    if st.button("🚀 Process Image", type="primary", use_container_width=True):
        with st.spinner(get_ui_text(language, 'processing', 'Processing...')):
            # Process image
            processing_result = image_processor.process_for_platform(
                image, 
                platform, 
                remove_bg=options['remove_background']
            )
            
            if processing_result['success']:
                processed_image = processing_result['image']
                
                # Generate captions
                caption_result = ai_service.generate_product_caption(
                    processed_image, platform, language, voice_input
                )
                
                # Display results
                st.success("✅ Processing completed!")
                
                # Show before/after comparison
                render_before_after_comparison(image, processed_image, language)
                
                # Show generated content
                render_generated_content(caption_result, language)
                
                # Save processed image
                timestamp = int(st.session_state.get('processing_timestamp', 0))
                filename = f"{platform}_{timestamp}"
                save_result = save_processed_image(
                    processed_image, 
                    filename, 
                    format='PNG' if processed_image.mode == 'RGBA' else 'JPEG'
                )
                
                return {
                    'success': True,
                    'processed_image': processed_image,
                    'image_save_result': save_result,
                    'caption_result': caption_result,
                    'platform': platform
                }
            else:
                st.error(f"❌ Processing failed: {processing_result['error']}")
                return {'success': False, 'error': processing_result['error']}
    
    return {'success': False}

def render_before_after_comparison(original: Image.Image, processed: Image.Image, 
                                 language: str = 'hi') -> None:
    """
    Render before/after image comparison
    
    Args:
        original: Original image
        processed: Processed image
        language: Current language
    """
    st.subheader("🔄 Before & After Comparison")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Before (Original)**")
        st.image(original, use_column_width=True)
        st.write(f"Size: {original.size[0]} × {original.size[1]}")
    
    with col2:
        st.write("**After (Processed)**")
        st.image(processed, use_column_width=True) 
        st.write(f"Size: {processed.size[0]} × {processed.size[1]}")

def render_generated_content(caption_result: Dict, language: str = 'hi') -> None:
    """
    Render generated captions and hashtags
    
    Args:
        caption_result: AI-generated content
        language: Current language
    """
    st.subheader("📝 Generated Content")
    
    if caption_result.get('success'):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.write("**Caption:**")
            st.text_area(
                "Generated Caption",
                value=caption_result.get('caption', ''),
                height=100,
                help="You can edit this caption before using"
            )
            
            st.write("**Description:**")
            st.text_area(
                "Product Description", 
                value=caption_result.get('description', ''),
                height=80
            )
        
        with col2:
            st.write("**Hashtags:**")
            hashtags = caption_result.get('hashtags', [])
            if hashtags:
                for tag in hashtags:
                    st.code(tag, language='')
            
            st.write("**Platform:**")
            st.info(f"📱 {caption_result.get('platform', '').title()}")
            
            st.write("**AI Generated:**")
            if caption_result.get('ai_generated', False):
                st.success("🤖 Yes")
            else:
                st.warning("📝 Template")
    else:
        st.error("❌ Content generation failed")

def render_download_section(processed_results: List[Dict], language: str = 'hi') -> None:
    """
    Render download section for processed images
    
    Args:
        processed_results: List of processing results
        language: Current language
    """
    if not processed_results:
        return
    
    st.subheader(get_ui_text(language, 'download', '⬇️ Download'))
    
    col1, col2, col3 = st.columns(3)
    
    for i, result in enumerate(processed_results):
        if result.get('success') and result.get('processed_image'):
            with [col1, col2, col3][i % 3]:
                platform = result.get('platform', 'image').title()
                
                # Convert image to bytes for download
                img_bytes = io.BytesIO()
                format_type = 'PNG' if result['processed_image'].mode == 'RGBA' else 'JPEG'
                result['processed_image'].save(img_bytes, format=format_type)
                img_bytes = img_bytes.getvalue()
                
                st.download_button(
                    label=f"📱 {platform} Ready",
                    data=img_bytes,
                    file_name=f"{platform.lower()}_ready.{format_type.lower()}",
                    mime=f"image/{format_type.lower()}",
                    use_container_width=True
                )

def render_service_status(language: str = 'hi') -> None:
    """
    Render service availability status
    
    Args:
        language: Current language
    """
    with st.expander("🔧 Service Status"):
        image_status = image_processor.is_available()
        
        st.write("**Image Processing:**")
        st.write(f"🎨 Background Removal: {'✅' if image_status['background_removal'] else '❌'}")
        st.write(f"🖼️ OpenCV: {'✅' if image_status['opencv'] else '❌'}")
        st.write(f"⚙️ Basic Processing: {'✅' if image_status['basic_processing'] else '❌'}")
        
        st.write("**AI Services:**")
        st.write(f"🤖 Gemini AI: {'✅' if ai_service.is_available() else '❌'}")
        
        st.write("**Voice Services:**")
        st.write(f"🎙️ Speech Services: {'✅' if voice_service.is_available() else '❌'}")