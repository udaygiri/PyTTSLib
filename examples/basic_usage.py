"""
Basic usage examples for the PyTTSLib text-to-speech package.

This script demonstrates the basic functionality of the PyTTSLib package,
including speaking text, saving speech to a file, and changing voice properties.
"""

import os
import sys
import time

# Add the parent directory to the Python path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyttslib import TextToSpeech, TTSError

def main():
    """Run the basic usage examples."""
    print("PyTTSLib Basic Usage Examples")
    print("-----------------------------")
    
    # Example 1: Basic speech with default engine (pyttsx3)
    print("\nExample 1: Basic speech with pyttsx3 engine")
    try:
        tts = TextToSpeech()
        tts.speak("Hello! This is a demonstration of the PyTTSLib package using the pyttsx3 engine.")
        print("✓ Speech completed")
    except TTSError as e:
        print(f"✗ Error: {e}")
    
    time.sleep(1)  # Pause between examples
    
    # Example 2: Save speech to a file
    print("\nExample 2: Save speech to a file")
    try:
        output_file = "output_pyttsx3.wav"
        tts.save_to_file(
            "This text is being saved to a WAV file using the pyttsx3 engine.",
            output_file
        )
        print(f"✓ Speech saved to {output_file}")
    except TTSError as e:
        print(f"✗ Error: {e}")
    
    time.sleep(1)  # Pause between examples
    
    # Example 3: Change speech rate and volume
    print("\nExample 3: Change speech rate and volume")
    try:
        tts.set_rate(150)  # Slightly faster
        tts.set_volume(0.8)  # 80% volume
        tts.speak("This speech is a bit faster and at 80 percent volume.")
        print("✓ Speech completed with modified rate and volume")
    except TTSError as e:
        print(f"✗ Error: {e}")
    
    time.sleep(1)  # Pause between examples
    
    # Example 4: List available voices
    print("\nExample 4: List available voices")
    try:
        voices = tts.list_voices()
        print(f"Available voices ({len(voices)}):")
        for i, voice in enumerate(voices[:3]):  # Show first 3 voices
            print(f"  Voice {i+1}: {voice['name']} ({voice['id']})")
        if len(voices) > 3:
            print(f"  ... and {len(voices) - 3} more")
    except TTSError as e:
        print(f"✗ Error: {e}")
    
    time.sleep(1)  # Pause between examples
    
    # Example 5: Use Google TTS engine
    print("\nExample 5: Use Google TTS engine")
    try:
        gtts = TextToSpeech(engine="google")
        gtts.speak("Hello! This is a demonstration of the PyTTSLib package using the Google Text-to-Speech engine.")
        print("✓ Speech completed with Google TTS")
    except TTSError as e:
        print(f"✗ Error: {e}")
    
    time.sleep(1)  # Pause between examples
    
    # Example 6: Save Google TTS to a file
    print("\nExample 6: Save Google TTS to a file")
    try:
        output_file = "output_google.mp3"
        gtts.save_to_file(
            "This text is being saved to an MP3 file using the Google Text-to-Speech engine.",
            output_file
        )
        print(f"✓ Speech saved to {output_file}")
    except TTSError as e:
        print(f"✗ Error: {e}")
    
    print("\nExamples completed!")

if __name__ == "__main__":
    main() 