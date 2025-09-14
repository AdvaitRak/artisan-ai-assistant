"""
AI service for generating captions and hashtags using Gemini
"""
import logging
from typing import Dict, Any, List, Optional
import base64
import io
from PIL import Image

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logging.warning("Google Generative AI not available")

from ..config import Config, LANGUAGE_CONFIG

logger = logging.getLogger(__name__)

class AIService:
    """Handles AI-powered caption and hashtag generation"""
    
    def __init__(self):
        self.model = None
        
        if GEMINI_AVAILABLE and Config.GEMINI_API_KEY:
            try:
                genai.configure(api_key=Config.GEMINI_API_KEY)
                self.model = genai.GenerativeModel(Config.GEMINI_MODEL)
                logger.info("Gemini AI service initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Gemini AI: {e}")
        else:
            logger.warning("Gemini AI service not available")
    
    def generate_product_caption(self, image: Image.Image, platform: str = 'amazon',
                                language: str = 'hi', user_input: str = '') -> Dict[str, Any]:
        """
        Generate product caption and hashtags for specific platform
        
        Args:
            image: PIL Image object
            platform: Target platform ('amazon', 'instagram', 'whatsapp')
            language: Language code (hi, mr, en)
            user_input: Additional context from user voice input
            
        Returns:
            Dictionary with caption, hashtags and metadata
        """
        if not self.model:
            return self._fallback_caption(platform, language, user_input)
        
        try:
            # Convert image to base64 for Gemini
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()
            
            # Create prompt based on platform and language
            prompt = self._create_prompt(platform, language, user_input)
            
            # Generate content with image
            response = self.model.generate_content([prompt, image])
            
            # Parse response
            result = self._parse_ai_response(response.text, platform, language)
            result['success'] = True
            result['ai_generated'] = True
            
            logger.info(f"AI caption generated for {platform} in {language}")
            return result
            
        except Exception as e:
            logger.error(f"AI caption generation failed: {e}")
            return self._fallback_caption(platform, language, user_input)
    
    def _create_prompt(self, platform: str, language: str, user_input: str) -> str:
        """Create AI prompt based on platform and language"""
        
        language_names = {
            'hi': 'Hindi (हिंदी)',
            'mr': 'Marathi (मराठी)',
            'en': 'English'
        }
        
        platform_requirements = {
            'amazon': {
                'hi': 'Amazon उत्पाद विवरण के लिए व्यावसायिक और आकर्षक शीर्षक',
                'mr': 'Amazon उत्पाद वर्णनासाठी व्यावसायिक आणि आकर्षक शीर्षक',
                'en': 'Professional and compelling product title for Amazon listing'
            },
            'instagram': {
                'hi': 'Instagram पोस्ट के लिए आकर्षक कैप्शन और हैशटैग',
                'mr': 'Instagram पोस्टसाठी आकर्षक कॅप्शन आणि हॅशटॅग',
                'en': 'Engaging Instagram caption with hashtags'
            },
            'whatsapp': {
                'hi': 'WhatsApp शेयर के लिए छोटा और आकर्षक संदेश',
                'mr': 'WhatsApp शेअरसाठी लहान आणि आकर्षक संदेश',
                'en': 'Short and engaging message for WhatsApp sharing'
            }
        }
        
        base_prompt = f"""
You are helping a local artisan create {platform_requirements[platform][language]}.

Analyze this product image and generate:
1. A compelling product caption in {language_names[language]}
2. Relevant hashtags (5-10) in {language_names[language]}
3. A brief product description in {language_names[language]}

Additional context from user: {user_input if user_input else 'None'}

Platform: {platform.upper()}
Language: {language_names[language]}

Please respond in the following format:
CAPTION: [Your caption here]
HASHTAGS: [#hashtag1 #hashtag2 #hashtag3 ...]
DESCRIPTION: [Brief product description]

Make it authentic, engaging, and suitable for local artisan products.
Focus on handmade quality, traditional craftsmanship, and unique features.
"""
        
        return base_prompt
    
    def _parse_ai_response(self, response_text: str, platform: str, language: str) -> Dict[str, Any]:
        """Parse AI response and extract caption, hashtags, description"""
        try:
            lines = response_text.strip().split('\n')
            
            caption = ''
            hashtags = []
            description = ''
            
            for line in lines:
                line = line.strip()
                if line.startswith('CAPTION:'):
                    caption = line.replace('CAPTION:', '').strip()
                elif line.startswith('HASHTAGS:'):
                    hashtag_text = line.replace('HASHTAGS:', '').strip()
                    hashtags = [tag.strip() for tag in hashtag_text.split() if tag.startswith('#')]
                elif line.startswith('DESCRIPTION:'):
                    description = line.replace('DESCRIPTION:', '').strip()
            
            # Fallback if parsing fails
            if not caption:
                caption = response_text[:200] + '...' if len(response_text) > 200 else response_text
            
            return {
                'caption': caption,
                'hashtags': hashtags,
                'description': description,
                'platform': platform,
                'language': language,
                'full_response': response_text
            }
            
        except Exception as e:
            logger.error(f"Failed to parse AI response: {e}")
            return self._fallback_caption(platform, language, '')
    
    def _fallback_caption(self, platform: str, language: str, user_input: str) -> Dict[str, Any]:
        """Generate fallback caption when AI is not available"""
        
        fallback_captions = {
            'amazon': {
                'hi': {
                    'caption': 'हस्तनिर्मित उत्पाद - पारंपरिक कारीगरी का अनुपम नमूना',
                    'hashtags': ['#हस्तनिर्मित', '#पारंपरिक', '#कारीगरी', '#भारतीय', '#हस्तशिल्प'],
                    'description': 'स्थानीय कारीगरों द्वारा प्रेम से बनाया गया यह उत्पाद आपके घर की शोभा बढ़ाएगा।'
                },
                'mr': {
                    'caption': 'हस्तनिर्मित उत्पादन - पारंपरिक कारागिरीचा अनुपम नमुना',
                    'hashtags': ['#हस्तनिर्मित', '#पारंपरिक', '#कारागिरी', '#भारतीय', '#हस्तकला'],
                    'description': 'स्थानिक कारागिरांनी प्रेमाने बनवलेले हे उत्पादन तुमच्या घराची शोभा वाढवेल।'
                },
                'en': {
                    'caption': 'Handmade Product - Exquisite Traditional Craftsmanship',
                    'hashtags': ['#handmade', '#traditional', '#craftsmanship', '#indian', '#artisan'],
                    'description': 'Lovingly crafted by local artisans, this product will enhance your home décor.'
                }
            },
            'instagram': {
                'hi': {
                    'caption': '✨ हाथों की कलाकारी का जादू ✨\n\n#कारीगरी #हस्तनिर्मित #भारतीयकला',
                    'hashtags': ['#कारीगरी', '#हस्तनिर्मित', '#भारतीयकला', '#परंपरा', '#हस्तशिल्प'],
                    'description': 'पारंपरिक कला का आधुनिक रूप'
                },
                'mr': {
                    'caption': '✨ हातांच्या कलाकारीचा जादू ✨\n\n#कारागिरी #हस्तनिर्मित #भारतीयकला',
                    'hashtags': ['#कारागिरी', '#हस्तनिर्मित', '#भारतीयकला', '#परंपरा', '#हस्तकला'],
                    'description': 'पारंपरिक कलेचे आधुनिक रूप'
                },
                'en': {
                    'caption': '✨ Magic of handcrafted artistry ✨\n\n#artisan #handmade #indianart',
                    'hashtags': ['#artisan', '#handmade', '#indianart', '#traditional', '#crafts'],
                    'description': 'Traditional art in modern form'
                }
            },
            'whatsapp': {
                'hi': {
                    'caption': '🎨 देखिए मेरी नई कृति! हस्तनिर्मित और खुशी से भरपूर ✨',
                    'hashtags': ['#हस्तनिर्मित', '#कारीगरी', '#कला'],
                    'description': 'स्थानीय कारीगर का प्रेम'
                },
                'mr': {
                    'caption': '🎨 पाहा माझी नवी कलाकृती! हस्तनिर्मित आणि आनंदाने भरलेली ✨',
                    'hashtags': ['#हस्तनिर्मित', '#कारागिरी', '#कला'],
                    'description': 'स्थानिक कारागिराचे प्रेम'
                },
                'en': {
                    'caption': '🎨 Check out my new creation! Handmade with love ✨',
                    'hashtags': ['#handmade', '#artisan', '#art'],
                    'description': 'Made with artisan love'
                }
            }
        }
        
        platform_data = fallback_captions.get(platform, fallback_captions['amazon'])
        lang_data = platform_data.get(language, platform_data['en'])
        
        return {
            'success': True,
            'ai_generated': False,
            'caption': lang_data['caption'],
            'hashtags': lang_data['hashtags'],
            'description': lang_data['description'],
            'platform': platform,
            'language': language,
            'user_input': user_input
        }
    
    def analyze_voice_command(self, voice_text: str, language: str = 'hi') -> Dict[str, Any]:
        """
        Analyze voice command to extract intent and parameters
        
        Args:
            voice_text: Transcribed voice input
            language: Language of the input
            
        Returns:
            Analyzed intent and parameters
        """
        try:
            # Simple keyword-based analysis for now
            voice_lower = voice_text.lower()
            
            # Detect platform intent
            platform = 'amazon'  # default
            
            platform_keywords = {
                'amazon': ['amazon', 'अमेज़न', 'अमेझन', 'selling', 'sell', 'विक्री', 'बेचना'],
                'instagram': ['instagram', 'इंस्टाग्राम', 'insta', 'इन्स्टा', 'social', 'सोशल'],
                'whatsapp': ['whatsapp', 'व्हाट्सऐप', 'व्हाट्सअप', 'share', 'शेयर', 'भेजना']
            }
            
            for plat, keywords in platform_keywords.items():
                if any(keyword in voice_lower for keyword in keywords):
                    platform = plat
                    break
            
            # Detect enhancement intent
            enhance_keywords = ['enhance', 'improve', 'सुधार', 'बेहतर', 'background', 'बैकग्राउंड']
            remove_bg = any(keyword in voice_lower for keyword in enhance_keywords)
            
            return {
                'platform': platform,
                'remove_background': remove_bg,
                'original_text': voice_text,
                'language': language,
                'confidence': 0.8  # Static confidence for keyword matching
            }
            
        except Exception as e:
            logger.error(f"Voice command analysis failed: {e}")
            return {
                'platform': 'amazon',
                'remove_background': True,
                'original_text': voice_text,
                'language': language,
                'confidence': 0.5
            }
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.model is not None

# Global AI service instance
ai_service = AIService()