"""
Exception classes for the PyTTSLib package.

This module defines custom exception types used throughout the PyTTSLib package
to provide informative error messages and enable proper error handling.
"""

class TTSError(Exception):
    """
    Base exception class for all PyTTSLib errors.
    
    This exception is raised when there is a general error during text-to-speech
    operations that doesn't fall into a more specific error category.
    """
    pass

class EngineNotFoundError(TTSError):
    """
    Exception raised when an unsupported or unavailable TTS engine is requested.
    
    This exception is raised when trying to initialize a TextToSpeech instance
    with an engine name that is not supported by the PyTTSLib package.
    """
    pass 