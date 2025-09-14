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
- Streamlit account (for deployment)

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
# Edit .env with your API keys
```

5. **Run the application**
```bash
streamlit run app.py
```

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

**Made with ❤️ for empowering local artisans worldwide