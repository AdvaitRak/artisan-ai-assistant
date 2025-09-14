"""
🎨 Artisan AI Assistant - Main Streamlit Application

Voice-enabled AI assistant for local artisans to create professional product images
for e-commerce and social media platforms.
"""

import streamlit as st
import logging
import os
import time
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import application modules
from src.config import Config, UI_TRANSLATIONS
from src.services import voice_service, image_processor, ai_service
from src.utils import get_ui_text, cleanup_temp_files
from src.ui import (
    render_voice_interface,
    render_voice_feedback,
    render_language_selector,
    render_voice_tips,
    render_image_upload,
    render_platform_selector,
    render_processing_options,
    render_image_processing,
    render_download_section,
    render_service_status
)

# Page configuration
st.set_page_config(
    page_title="🎨 Artisan AI Assistant",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_session_state():
    """Initialize Streamlit session state variables"""
    if 'language' not in st.session_state:
        st.session_state.language = Config.DEFAULT_LANGUAGE
    
    if 'processing_results' not in st.session_state:
        st.session_state.processing_results = []
    
    if 'voice_transcript' not in st.session_state:
        st.session_state.voice_transcript = ''
    
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    
    if 'processing_timestamp' not in st.session_state:
        st.session_state.processing_timestamp = int(time.time())

def render_header(language: str):
    """Render application header"""
    title = get_ui_text(language, 'title', '🎨 Artisan AI Assistant')
    st.title(title)
    
    # Subtitle with description
    if language == 'hi':
        st.markdown("**स्थानीय कारीगरों के लिए AI-संचालित फोटो एन्हांसमेंट और कैप्शन जेनरेशन**")
        st.markdown("अपनी हस्तकृतियों को Amazon, Instagram और WhatsApp के लिए प्रोफेशनल बनाएं")
    elif language == 'mr':
        st.markdown("**स्थानिक कारागिरांसाठी AI-चालित फोटो एन्हांसमेंट आणि कॅप्शन जनरेशन**")
        st.markdown("तुमच्या हस्तकलेला Amazon, Instagram आणि WhatsApp साठी व्यावसायिक बनवा")
    else:
        st.markdown("**AI-powered photo enhancement and caption generation for local artisans**")
        st.markdown("Transform your handmade products for Amazon, Instagram, and WhatsApp")

def render_sidebar(language: str) -> Dict[str, Any]:
    """Render sidebar with controls"""
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Language selector
        current_language = render_language_selector()
        if current_language != st.session_state.language:
            st.session_state.language = current_language
            st.rerun()
        
        st.divider()
        
        # Platform selector
        platform = render_platform_selector(language)
        
        st.divider()
        
        # Processing options
        processing_options = render_processing_options(language)
        
        st.divider()
        
        # Voice command tips
        render_voice_tips(language)
        
        st.divider()
        
        # Service status
        render_service_status(language)
        
        return {
            'language': current_language,
            'platform': platform,
            'processing_options': processing_options
        }

def render_main_workflow(settings: Dict[str, Any]):
    """Render main application workflow"""
    language = settings['language']
    platform = settings['platform']
    options = settings['processing_options']
    
    # Create tabs for different workflows
    tab1, tab2, tab3 = st.tabs([
        "📷 Image Upload",
        "🎙️ Voice Commands", 
        "⬇️ Downloads"
    ])
    
    with tab1:
        st.header(get_ui_text(language, 'upload_image', '📷 Upload Product Photo'))
        
        # Image upload
        uploaded_image = render_image_upload(language)
        
        if uploaded_image:
            st.session_state.current_image = uploaded_image
            
            # Processing section
            st.divider()
            
            # Process image button and results
            processing_result = render_image_processing(
                uploaded_image,
                platform,
                options,
                st.session_state.voice_transcript,
                language
            )
            
            if processing_result.get('success'):
                # Add to results
                processing_result['timestamp'] = datetime.now()
                st.session_state.processing_results.append(processing_result)
                
                # Voice feedback
                if Config.ENABLE_VOICE_FEEDBACK:
                    success_messages = {
                        'hi': f"आपका {platform} फोटो तैयार है! डाउनलोड करने के लिए डाउनलोड टैब पर जाएं।",
                        'mr': f"तुमचा {platform} फोटो तयार आहे! डाउनलोड करण्यासाठी डाउनलोड टॅबवर जा।",
                        'en': f"Your {platform} photo is ready! Go to the Downloads tab to download."
                    }
                    render_voice_feedback(success_messages.get(language, success_messages['en']), language)
    
    with tab2:
        st.header(get_ui_text(language, 'voice_command', '🎙️ Voice Commands'))
        
        # Voice interface
        voice_result = render_voice_interface(language)
        
        if voice_result.get('success'):
            st.session_state.voice_transcript = voice_result['transcript']
            
            # Analyze voice command
            if voice_result['transcript']:
                analysis = ai_service.analyze_voice_command(
                    voice_result['transcript'], 
                    language
                )
                
                st.success(f"🎯 Command understood: {voice_result['transcript']}")
                
                # Show analysis results
                col1, col2 = st.columns(2)
                with col1:
                    st.info(f"📱 Detected Platform: **{analysis['platform'].title()}**")
                with col2:
                    st.info(f"🎨 Background Removal: **{'Yes' if analysis['remove_background'] else 'No'}**")
                
                # Update settings based on voice command
                if analysis['platform'] != platform:
                    st.warning(f"💡 Consider switching to {analysis['platform'].title()} in the sidebar")
                
                # Voice feedback
                if Config.ENABLE_VOICE_FEEDBACK:
                    feedback_messages = {
                        'hi': f"समझ गया! {analysis['platform']} के लिए फोटो प्रोसेसिंग करूंगा।",
                        'mr': f"समजले! {analysis['platform']} साठी फोटो प्रक्रिया करणार.",
                        'en': f"Understood! I'll process the photo for {analysis['platform']}."
                    }
                    render_voice_feedback(feedback_messages.get(language, feedback_messages['en']), language)
    
    with tab3:
        st.header(get_ui_text(language, 'download', '⬇️ Downloads'))
        
        if st.session_state.processing_results:
            # Show processed results
            render_download_section(st.session_state.processing_results, language)
            
            # Clear results button
            if st.button("🗑️ Clear All Results", type="secondary"):
                st.session_state.processing_results = []
                st.success("Results cleared!")
                st.rerun()
        else:
            st.info("No processed images yet. Upload and process an image first!")

def render_footer(language: str):
    """Render application footer"""
    st.divider()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center; color: #666; font-size: 14px;'>
                Made with ❤️ for empowering local artisans worldwide<br>
                🎨 Artisan AI Assistant v1.0.0
            </div>
            """,
            unsafe_allow_html=True
        )

def check_configuration():
    """Check and validate application configuration"""
    missing_config = Config.validate_config()
    
    if missing_config:
        st.error("⚠️ Configuration Issues Detected")
        st.write("The following configuration items are missing:")
        for item in missing_config:
            st.write(f"❌ {item}")
        
        st.info("""
        **To fix this:**
        1. Copy `.env.example` to `.env`
        2. Fill in your API keys and configuration
        3. Restart the application
        """)
        
        with st.expander("📖 Configuration Help"):
            st.markdown("""
            **Required Configuration:**
            
            - **GEMINI_API_KEY**: Get from Google AI Studio
            - **GOOGLE_APPLICATION_CREDENTIALS**: Path to Google Cloud service account JSON
            - **GOOGLE_CLOUD_PROJECT_ID**: Your Google Cloud project ID
            
            **Optional but Recommended:**
            - Voice services require Google Cloud Speech API
            - Background removal requires rembg library
            """)
        
        return False
    
    return True

def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Check configuration
    if not check_configuration():
        st.stop()
    
    # Create necessary directories
    Config.create_directories()
    
    # Cleanup old files (run periodically)
    if st.session_state.get('last_cleanup', 0) < time.time() - 3600:  # Every hour
        cleanup_temp_files()
        st.session_state.last_cleanup = time.time()
    
    # Get current language
    language = st.session_state.language
    
    # Render header
    render_header(language)
    
    # Render sidebar and get settings
    settings = render_sidebar(language)
    
    # Render main workflow
    render_main_workflow(settings)
    
    # Render footer
    render_footer(language)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Application error: {e}")
        st.error(f"An error occurred: {e}")
        st.error("Please check the logs for more details.")