# 🎯 PyTTSLib

> 🔊 A powerful and easy-to-use Python Text-to-Speech library that supports multiple TTS engines.

## ✨ Features

- 🎙️ Multiple TTS engine support:
  - 🖥️ **pyttsx3** (offline, default) - Works without internet
  - 🌐 **Google TTS** - High-quality online TTS
- 🎛️ Voice customization:
  - 🏃‍♂️ Adjustable speech rate
  - 📊 Volume control
  - 👥 Multiple voice options
- 💾 Save audio to multiple formats (MP3, WAV)
- 🔄 Smart file management with auto-cleanup
- 🖥️ Cross-platform compatibility (Windows, Linux, macOS)
- 🛡️ Robust error handling
- 📝 Well-documented API

## 🚀 Installation

```bash
pip install pyttslib
```

## 📖 Quick Start

```python
from pyttslib import TextToSpeech

# Create a TTS instance (default: pyttsx3 engine)
tts = TextToSpeech()

# Basic text-to-speech
tts.speak("Hello, world!")

# Use Google TTS instead
gtts = TextToSpeech(engine="google")
gtts.speak("Hello from Google Text-to-Speech!")

# Save speech to a file
tts.save_to_file("This will be saved as audio.", "output.mp3")
```

## 🎮 Advanced Usage

### 🎛️ Voice Configuration

```python
# Configure pyttsx3 engine
tts = TextToSpeech(engine="pyttsx3", engine_config={
    "rate": 150,    # Words per minute
    "volume": 0.8,  # Volume level (0.0 to 1.0)
})

# Configure Google TTS
tts = TextToSpeech(engine="google", engine_config={
    "lang": "en",    # Language code
    "tld": "com",    # Top-level domain
    "slow": False    # Normal speed
})
```

### 🎭 Voice Selection

```python
# List available voices
voices = tts.list_voices()
for voice in voices:
    print(f"Voice: {voice['name']} (ID: {voice['id']})")

# Set a specific voice
tts.set_voice("en_female_1")  # Voice ID from list_voices()
```

### ⚙️ Speech Properties

```python
# Adjust speech rate (pyttsx3 only)
tts.set_rate(150)  # Words per minute

# Adjust volume (pyttsx3 only)
tts.set_volume(0.8)  # 80% volume
```

## 🌟 Examples

The package includes example scripts in the `examples/` directory:

- 📝 `basic_usage.py`: Demonstrates fundamental features
- 🔧 `advanced_usage.py`: Shows advanced functionality

Run the examples:

```bash
python examples/basic_usage.py
python examples/advanced_usage.py
```

## 🔍 Supported Audio Formats

- 🎵 MP3 (Google TTS)
- 🔊 WAV (pyttsx3)
- 🎼 OGG (platform-dependent)
- 🎹 AIFF (platform-dependent)

## 🛠️ Technical Details

### File Management

- 📁 Temporary files are stored in a dedicated folder
- 🧹 Automatic cleanup after playback
- 💫 Robust retry mechanism for file operations
- 🔒 Safe file handling with proper resource cleanup

### Error Handling

- ⚠️ Custom exception classes for better error management
- 🔄 Automatic retries for transient failures
- 📢 Clear error messages and logging
- 🛡️ Graceful fallbacks for playback methods

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create your feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🎯 Open a Pull Request

## 📄 License

MIT License - feel free to use this in your projects!

## 🙏 Acknowledgments

- 🎤 [pyttsx3](https://github.com/nateshmbhat/pyttsx3) for offline TTS
- 🌐 [gTTS](https://github.com/pndurette/gTTS) for Google TTS support
- 🔊 [playsound](https://github.com/TaylorSMarks/playsound) for cross-platform audio playback

## 📞 Support

- 📧 Report issues on GitHub
- 💭 Submit feature requests
- 🤝 Pull requests are welcome

---

Made with ❤️ for the Python community
