# 🎨 Artisan AI Assistant

**Empowering Local Artisans with Voice-Enabled AI for Professional Product Photography**

Transform your handmade products into professional e-commerce listings and stunning social media content using the power of AI and voice interaction in your local language.

## 🌟 Features

- **🎙️ Multilingual Voice Interface** - Speak in Hindi, Marathi, or English
- **📸 Smart Photo Enhancement** - Professional product photos in seconds
- **🛍️ Platform-Specific Optimization** - Amazon-ready vs Instagram-ready outputs
- **✨ AI-Generated Captions** - Automatic captions and hashtags in your language
- **📱 Mobile-Friendly** - Works on any smartphone browser
- **🔄 Before/After Comparison** - See the AI magic in action

## 🚀 User Flow

1. **📷 Upload/Capture** - Add your product photo
2. **🗣️ Voice Command** - Tell us what you want in your language
3. **🤖 AI Processing** - Our AI understands and enhances your image
4. **📱 Get Results** - Download professional photos and captions
5. **💼 Use Anywhere** - Ready for Amazon, Instagram, or WhatsApp

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| AI Chatbot | Google Vertex AI Gemini |
| Speech-to-Text | Google Cloud STT |
| Text-to-Speech | Google Cloud TTS |
| Image Enhancement | rembg + Pillow + OpenCV |
| Hosting | Streamlit Cloud |

## 🔧 Setup Instructions

### Prerequisites
- Python 3.8+
- Google Cloud Account (for AI services)
- Google AI Studio account (for Gemini API)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/AdvaitRak/artisan-ai-assistant.git
cd artisan-ai-assistant
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your API keys (see Configuration section below)
```

5. **Run the application**
```bash
streamlit run app.py
```

### Configuration

Edit the `.env` file with your API credentials:

```env
# Required: Google AI Studio API key for Gemini
GEMINI_API_KEY=your-gemini-api-key-here

# Required: Google Cloud credentials for speech services
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json
GOOGLE_CLOUD_PROJECT_ID=your-project-id

# Optional: Customize other settings as needed
DEFAULT_LANGUAGE=hi
MAX_IMAGE_SIZE_MB=10
```

#### Getting API Keys

1. **Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy to your `.env` file

2. **Google Cloud Speech Services**:
   - Create a project in [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Speech-to-Text and Text-to-Speech APIs
   - Create a service account and download the JSON key
   - Set the path in `GOOGLE_APPLICATION_CREDENTIALS`

## 🎯 Example Demo Interaction

```
🧑‍🎨 Artisan: Opens app → uploads pottery photo
🗣️ Speaks: "Amazon साठी फोटो सुधार" (Enhance photo for Amazon)
🤖 AI: Converts voice → understands intent → enhances image
✨ Result: Clean white background, 1000x1000px, professional quality
📝 Caption: "Handmade pottery, perfect for your kitchen! #handmade #pottery"
🔊 Voice Response: "तुमचा फोटो आता Amazon लिस्टिंगसाठी तयार आहे."
⬇️ Download: Ready-to-use image + captions
```

## 📚 Documentation

- **[USAGE.md](USAGE.md)** - Complete usage guide with voice commands
- **[Demo Script](demo.py)** - Run `python demo.py` to see core functionality

## 🧪 Testing

Run the test suite to verify your installation:

```bash
# Install test dependencies
pip install pytest

# Run tests
python -m pytest tests/ -v

# Run demo
python demo.py
```

## 📁 Project Structure

```
artisan-ai-assistant/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Dependencies
├── .env.example             # Configuration template
├── demo.py                  # Functionality demo
├── USAGE.md                 # Detailed usage guide
├── src/
│   ├── config/              # Configuration management
│   ├── services/            # Core services (AI, image, voice)
│   ├── utils/               # Utility functions
│   └── ui/                  # UI components
├── static/                  # Static assets (CSS, JS)
└── tests/                   # Test suite
```

## 🌍 Supported Languages

| Language | Code | Voice Support | UI Support |
|----------|------|---------------|------------|
| हिंदी (Hindi) | `hi` | ✅ | ✅ |
| मराठी (Marathi) | `mr` | ✅ | ✅ |
| English | `en` | ✅ | ✅ |

## 🚀 Platform Optimization

| Platform | Image Size | Background | Best For |
|----------|------------|------------|----------|
| Amazon | 1000×1000px | White | Product listings |
| Instagram | 1080×1080px | Artistic | Social media |
| WhatsApp | 640×640px | Any | Quick sharing |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Local Artisan Community** - For inspiration and feedback
- **Google Cloud AI** - For powerful AI services
- **Streamlit** - For the amazing web framework
- **Open Source Community** - For the wonderful libraries

**Made with ❤️ for empowering local artisans worldwide**