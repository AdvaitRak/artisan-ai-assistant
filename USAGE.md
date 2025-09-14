# 🎨 Artisan AI Assistant - Usage Guide

## Overview

The Artisan AI Assistant is a voice-enabled application that helps local artisans create professional product images for e-commerce and social media platforms. The app supports Hindi, Marathi, and English, making it accessible to artisans across different regions.

## Getting Started

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Google Cloud Account** with the following APIs enabled:
   - Cloud Speech-to-Text API
   - Cloud Text-to-Speech API
   - Cloud AI Platform (for Vertex AI)
3. **Google AI Studio Account** for Gemini API access

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/AdvaitRak/artisan-ai-assistant.git
   cd artisan-ai-assistant
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit the `.env` file with your API keys and configuration:
   - `GEMINI_API_KEY`: Your Google AI Studio API key
   - `GOOGLE_APPLICATION_CREDENTIALS`: Path to your Google Cloud service account JSON file
   - `GOOGLE_CLOUD_PROJECT_ID`: Your Google Cloud project ID

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Features

### 🎙️ Voice Interface

- **Multilingual Support**: Speak commands in Hindi, Marathi, or English
- **Voice Commands**: 
  - "Amazon के लिए फोटो बनाओ" (Make photo for Amazon)
  - "Instagram post बनाना है" (Want to create Instagram post)
  - "Background हटाओ" (Remove background)
  - "Photo improve करो" (Improve the photo)

### 📸 Image Processing

- **Background Removal**: Automatically remove backgrounds using AI
- **Platform Optimization**: Resize and optimize for:
  - Amazon (1000×1000px, white background)
  - Instagram (1080×1080px)
  - WhatsApp (640×640px)
- **Quality Enhancement**: Improve brightness, contrast, and sharpness

### 🤖 AI-Generated Content

- **Smart Captions**: AI-generated product descriptions
- **Hashtags**: Relevant hashtags for social media
- **Multilingual Output**: Content generated in your preferred language

## Workflow

### Basic Workflow

1. **Select Language**: Choose Hindi, Marathi, or English from the sidebar
2. **Upload Image**: Upload your product photo (supports JPG, PNG, WEBP)
3. **Choose Platform**: Select Amazon, Instagram, or WhatsApp
4. **Set Options**: Configure background removal and enhancement settings
5. **Process**: Click "Process Image" or use voice commands
6. **Download**: Get your optimized images and captions

### Voice-Enabled Workflow

1. **Upload Image**: Start by uploading your product photo
2. **Voice Command**: Record or upload an audio file with your command
3. **AI Processing**: The system understands your intent and processes accordingly
4. **Voice Feedback**: Get audio confirmation of the processing
5. **Download**: Receive optimized images with AI-generated captions

## Platform-Specific Guidelines

### Amazon Listings

- **Image Requirements**: 1000×1000px minimum, white background
- **Content Focus**: Product features, specifications, and benefits
- **Keywords**: SEO-optimized titles and descriptions

### Instagram Posts

- **Image Requirements**: 1080×1080px, engaging visuals
- **Content Focus**: Lifestyle, behind-the-scenes, artistic elements
- **Hashtags**: Trending and niche-specific tags

### WhatsApp Sharing

- **Image Requirements**: 640×640px for quick sharing
- **Content Focus**: Personal touch, local community appeal
- **Messaging**: Short, engaging descriptions

## Voice Commands Reference

### Hindi Commands

| Command | Purpose |
|---------|---------|
| "Amazon के लिए तैयार करो" | Optimize for Amazon |
| "Instagram post बनाओ" | Create Instagram post |
| "Background साफ करो" | Remove background |
| "Photo अच्छी बनाओ" | Enhance image quality |
| "Caption लिखो" | Generate captions |

### Marathi Commands

| Command | Purpose |
|---------|---------|
| "Amazon साठी तयार करा" | Optimize for Amazon |
| "Instagram post बनवा" | Create Instagram post |
| "Background काढा" | Remove background |
| "Photo चांगली करा" | Enhance image quality |
| "Caption लिहा" | Generate captions |

### English Commands

| Command | Purpose |
|---------|---------|
| "Prepare for Amazon" | Optimize for Amazon |
| "Create Instagram post" | Create Instagram post |
| "Remove background" | Remove background |
| "Enhance the photo" | Enhance image quality |
| "Generate caption" | Generate captions |

## Troubleshooting

### Common Issues

1. **Voice recognition not working**:
   - Check Google Cloud credentials
   - Ensure microphone permissions are granted
   - Verify internet connection

2. **Background removal fails**:
   - Install rembg library: `pip install rembg`
   - Check image format compatibility
   - Ensure sufficient memory available

3. **AI captions not generating**:
   - Verify Gemini API key in .env file
   - Check API quota and billing
   - Ensure internet connectivity

4. **Image processing errors**:
   - Check image file size (max 10MB)
   - Verify supported formats (JPG, PNG, WEBP)
   - Ensure sufficient disk space

### Configuration Issues

If you see configuration warnings:

1. **Missing API Keys**:
   - Copy `.env.example` to `.env`
   - Fill in all required API keys
   - Restart the application

2. **Service Unavailable**:
   - Check the Service Status in the sidebar
   - Verify API credentials
   - Check internet connectivity

## Tips for Best Results

### Photography Tips

1. **Good Lighting**: Use natural light or well-lit environments
2. **Clean Background**: Start with a simple background for better processing
3. **Product Focus**: Ensure the product is the main subject
4. **High Resolution**: Use the highest quality images available

### Voice Command Tips

1. **Clear Speech**: Speak clearly and at moderate pace
2. **Natural Language**: Use conversational commands
3. **Context**: Provide context about the platform or intent
4. **Quiet Environment**: Record in a quiet space for better recognition

### Content Optimization

1. **Keywords**: Include relevant product keywords
2. **Local Appeal**: Emphasize handmade and artisan qualities
3. **Platform Context**: Tailor content for specific platforms
4. **Cultural Relevance**: Use local language and cultural references

## Advanced Features

### Batch Processing

When enabled in configuration, you can process multiple images simultaneously.

### Custom Watermarks

Add your artisan signature or brand watermark to processed images.

### Analytics

Track which platforms and content types perform best for your products.

## Support

For support and questions:

1. **Documentation**: Check this guide and inline help
2. **Issues**: Report bugs on GitHub
3. **Community**: Join artisan community discussions
4. **Updates**: Follow the repository for new features

## Version History

- **v1.0.0**: Initial release with voice interface, image processing, and AI captions
- **Future**: Planned features include batch processing, analytics, and enhanced AI models

---

Made with ❤️ for empowering local artisans worldwide