"""
Voice interface UI components
"""
import streamlit as st
import io
import base64
from typing import Dict, Any, Optional
import logging

from ..services import voice_service
from ..utils import get_ui_text

logger = logging.getLogger(__name__)

def render_voice_interface(language: str = 'hi') -> Dict[str, Any]:
    """
    Render voice interface components
    
    Args:
        language: Current language setting
        
    Returns:
        Dictionary with voice interaction results
    """
    result = {'success': False, 'transcript': '', 'audio_data': None}
    
    st.subheader(get_ui_text(language, 'voice_command', '🎙️ Voice Command'))
    
    # Check if voice service is available
    if not voice_service.is_available():
        st.warning("Voice services not available. Please check your Google Cloud configuration.")
        return result
    
    # Voice input section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("**Record your voice command:**")
        
        # Audio recorder component (would need streamlit-webrtc or similar)
        # For now, show placeholder
        audio_bytes = st.file_uploader(
            "Upload audio file",
            type=['wav', 'mp3', 'm4a'],
            help="Record and upload your voice command"
        )
        
        if audio_bytes is not None:
            st.audio(audio_bytes, format="audio/wav")
            
            # Process audio
            if st.button("🎯 Process Voice Command", key="process_voice"):
                with st.spinner("Processing voice..."):
                    # Convert audio to speech-to-text
                    stt_result = voice_service.speech_to_text(
                        audio_bytes.read(), 
                        language
                    )
                    
                    if stt_result['success']:
                        result['success'] = True
                        result['transcript'] = stt_result['transcript']
                        result['confidence'] = stt_result['confidence']
                        
                        st.success(f"✅ Understood: {stt_result['transcript']}")
                        st.info(f"Confidence: {stt_result['confidence']:.2f}")
                    else:
                        st.error(f"❌ Speech recognition failed: {stt_result['error']}")
    
    with col2:
        st.write("**Or type your command:**")
        text_input = st.text_area(
            "Type your command",
            placeholder=get_ui_text(language, 'voice_command', 'Tell us what you want...'),
            height=100
        )
        
        if text_input and st.button("📝 Use Text Command", key="process_text"):
            result['success'] = True
            result['transcript'] = text_input
            result['confidence'] = 1.0
            st.success(f"✅ Text input received: {text_input}")
    
    return result

def render_voice_feedback(text: str, language: str = 'hi') -> None:
    """
    Render voice feedback component
    
    Args:
        text: Text to convert to speech
        language: Language for TTS
    """
    if not text or not voice_service.is_available():
        return
    
    st.subheader("🔊 Voice Response")
    
    # Generate TTS
    tts_result = voice_service.text_to_speech(text, language)
    
    if tts_result['success']:
        # Create audio player
        audio_html = f"""
        <audio controls autoplay>
            <source src="data:audio/mp3;base64,{tts_result['audio_base64']}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """
        st.markdown(audio_html, unsafe_allow_html=True)
        st.write(f"🗣️ Speaking: {text}")
    else:
        st.warning("Voice feedback not available")

def render_language_selector() -> str:
    """
    Render language selection component
    
    Returns:
        Selected language code
    """
    language_options = {
        'हिंदी (Hindi)': 'hi',
        'मराठी (Marathi)': 'mr', 
        'English': 'en'
    }
    
    selected = st.selectbox(
        "🌐 Select Language / भाषा चुनें / भाषा निवडा",
        options=list(language_options.keys()),
        index=0
    )
    
    return language_options[selected]

def render_voice_tips(language: str) -> None:
    """
    Render voice command tips
    
    Args:
        language: Current language
    """
    tips = {
        'hi': [
            "📷 'Amazon के लिए फोटो बनाओ' - Amazon listing के लिए",
            "📱 'Instagram post बनाना है' - Social media के लिए", 
            "🎨 'Background हटाओ' - Background removal के लिए",
            "✨ 'Photo improve करो' - Image enhancement के लिए"
        ],
        'mr': [
            "📷 'Amazon साठी फोटो बनवा' - Amazon listing साठी",
            "📱 'Instagram post बनवायचे आहे' - Social media साठी",
            "🎨 'Background काढा' - Background removal साठी", 
            "✨ 'Photo सुधारा' - Image enhancement साठी"
        ],
        'en': [
            "📷 'Make photo for Amazon' - For Amazon listings",
            "📱 'Create Instagram post' - For social media",
            "🎨 'Remove background' - For background removal",
            "✨ 'Enhance the photo' - For image improvement"
        ]
    }
    
    with st.expander("💡 Voice Command Examples"):
        for tip in tips.get(language, tips['en']):
            st.write(tip)