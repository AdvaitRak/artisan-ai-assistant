"""
Voice interface service for speech-to-text and text-to-speech
"""
import os
import io
import base64
from typing import Optional, Dict, Any
import logging

try:
    from google.cloud import speech
    from google.cloud import texttospeech
    GOOGLE_CLOUD_AVAILABLE = True
except ImportError:
    GOOGLE_CLOUD_AVAILABLE = False
    logging.warning("Google Cloud Speech libraries not available")

from ..config import Config, LANGUAGE_CONFIG

logger = logging.getLogger(__name__)

class VoiceService:
    """Handles speech-to-text and text-to-speech operations"""
    
    def __init__(self):
        self.stt_client = None
        self.tts_client = None
        
        if GOOGLE_CLOUD_AVAILABLE and Config.GOOGLE_APPLICATION_CREDENTIALS:
            try:
                self.stt_client = speech.SpeechClient()
                self.tts_client = texttospeech.TextToSpeechClient()
                logger.info("Google Cloud Speech services initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Google Cloud Speech services: {e}")
        else:
            logger.warning("Google Cloud Speech services not available")
    
    def speech_to_text(self, audio_data: bytes, language: str = 'hi') -> Dict[str, Any]:
        """
        Convert speech to text
        
        Args:
            audio_data: Audio data in bytes
            language: Language code (hi, mr, en)
            
        Returns:
            Dictionary with transcription and confidence
        """
        if not self.stt_client:
            return {
                'success': False,
                'error': 'Speech-to-text service not available',
                'transcript': '',
                'confidence': 0.0
            }
        
        try:
            # Get language configuration
            lang_config = LANGUAGE_CONFIG.get(language, LANGUAGE_CONFIG['hi'])
            
            # Configure recognition
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=16000,
                language_code=lang_config['stt_code'],
                alternative_language_codes=['hi-IN', 'mr-IN', 'en-US'],
                enable_automatic_punctuation=True,
                model='latest_long'
            )
            
            audio = speech.RecognitionAudio(content=audio_data)
            
            # Perform recognition
            response = self.stt_client.recognize(config=config, audio=audio)
            
            if response.results:
                result = response.results[0]
                transcript = result.alternatives[0].transcript
                confidence = result.alternatives[0].confidence
                
                logger.info(f"STT successful: {transcript[:50]}... (confidence: {confidence})")
                
                return {
                    'success': True,
                    'transcript': transcript,
                    'confidence': confidence,
                    'language_detected': language
                }
            else:
                return {
                    'success': False,
                    'error': 'No speech detected',
                    'transcript': '',
                    'confidence': 0.0
                }
                
        except Exception as e:
            logger.error(f"Speech-to-text error: {e}")
            return {
                'success': False,
                'error': str(e),
                'transcript': '',
                'confidence': 0.0
            }
    
    def text_to_speech(self, text: str, language: str = 'hi') -> Dict[str, Any]:
        """
        Convert text to speech
        
        Args:
            text: Text to convert to speech
            language: Language code (hi, mr, en)
            
        Returns:
            Dictionary with audio data and metadata
        """
        if not self.tts_client:
            return {
                'success': False,
                'error': 'Text-to-speech service not available',
                'audio_data': None
            }
        
        try:
            # Get language configuration
            lang_config = LANGUAGE_CONFIG.get(language, LANGUAGE_CONFIG['hi'])
            
            # Configure synthesis
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            voice = texttospeech.VoiceSelectionParams(
                language_code=lang_config['tts_code'],
                name=lang_config['tts_voice'],
                ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
            )
            
            audio_config = texttospeech.AudioConfig(
                audio_encoding=texttospeech.AudioEncoding.MP3,
                speaking_rate=0.9,
                pitch=0.0,
                volume_gain_db=0.0
            )
            
            # Perform synthesis
            response = self.tts_client.synthesize_speech(
                input=synthesis_input,
                voice=voice,
                audio_config=audio_config
            )
            
            # Encode audio data as base64 for web delivery
            audio_base64 = base64.b64encode(response.audio_content).decode('utf-8')
            
            logger.info(f"TTS successful for text: {text[:50]}...")
            
            return {
                'success': True,
                'audio_data': response.audio_content,
                'audio_base64': audio_base64,
                'language': language,
                'voice': lang_config['tts_voice']
            }
            
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            return {
                'success': False,
                'error': str(e),
                'audio_data': None
            }
    
    def is_available(self) -> bool:
        """Check if voice services are available"""
        return self.stt_client is not None and self.tts_client is not None
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return list(LANGUAGE_CONFIG.keys())

# Global voice service instance
voice_service = VoiceService()