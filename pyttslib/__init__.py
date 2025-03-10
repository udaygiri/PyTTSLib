"""
PyTTSLib - A Comprehensive Text-to-Speech Library

This package provides an easy-to-use interface for text-to-speech functionality,
supporting multiple TTS engines, voice customization, and various output formats.
"""

__version__ = "0.1.0"

from .tts import TextToSpeech
from .exceptions import TTSError, EngineNotFoundError

__all__ = ["TextToSpeech", "TTSError", "EngineNotFoundError"] 