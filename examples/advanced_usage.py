"""
Advanced usage examples for the PyTTSLib text-to-speech package.

This script demonstrates more advanced functionality of the PyTTSLib package,
including reading long text files, processing large chunks of text, and
dynamically switching between TTS engines.
"""

import os
import sys
import time
import argparse

# Add the parent directory to the Python path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyttslib import TextToSpeech, TTSError
from pyttslib.utils import text_to_chunks, ensure_dir_exists

SAMPLE_TEXT = """
Artificial intelligence is intelligence demonstrated by machines, as opposed to the natural
intelligence displayed by humans and animals. AI research has been defined as the field of
study of intelligent agents, which refers to any system that perceives its environment and
takes actions that maximize its chance of achieving its goals.

The term "artificial intelligence" had previously been used to describe machines that mimic
and display "human" cognitive skills that are associated with the human mind, such as
"learning" and "problem-solving." This definition has since been rejected by major AI
researchers who now describe AI in terms of rationality and acting rationally, which does
not limit how intelligence can be articulated.

AI applications include advanced web search engines, recommendation systems, understanding
human speech, self-driving cars, automated decision-making and competing at the highest
level in strategic game systems.

As machines become increasingly capable, tasks considered to require "intelligence" are
often removed from the definition of AI, a phenomenon known as the AI effect. For instance,
optical character recognition is frequently excluded from things considered to be AI,
having become a routine technology.
"""

def process_long_text_example():
    """Demonstrate processing long text by breaking it into chunks."""
    print("\nAdvanced Example 1: Processing Long Text")
    print("--------------------------------------")
    
    # Break the text into smaller chunks
    chunks = text_to_chunks(SAMPLE_TEXT, max_length=200)
    print(f"Text broken into {len(chunks)} chunks.")
    
    # Process each chunk with different TTS engines
    tts_engines = {
        "pyttsx3": TextToSpeech(engine="pyttsx3"),
        "google": TextToSpeech(engine="google", 
                            engine_config={"lang": "en", "tld": "us", "slow": False})
    }
    
    try:
        # Toggle between engines for demonstration purposes
        for i, chunk in enumerate(chunks[:2]):  # Only process first 2 chunks for demo
            engine_name = "pyttsx3" if i % 2 == 0 else "google"
            print(f"\nChunk {i+1} (using {engine_name}):")
            print(f"'{chunk[:50]}...'")
            
            tts_engines[engine_name].speak(chunk)
            time.sleep(0.5)
        
        print("\n✓ Long text processing completed")
    
    except TTSError as e:
        print(f"✗ Error: {e}")

def file_to_speech_example(output_dir="output"):
    """Demonstrate reading text from a file and converting it to speech."""
    print("\nAdvanced Example 2: File to Speech")
    print("-------------------------------")
    
    # Create a sample text file
    ensure_dir_exists(output_dir)
    sample_file = os.path.join(output_dir, "sample_text.txt")
    
    with open(sample_file, "w") as f:
        f.write(SAMPLE_TEXT)
    
    print(f"Sample text saved to {sample_file}")
    
    # Read the file and convert to speech
    try:
        # Create TTS instance with custom parameters
        tts = TextToSpeech(engine="pyttsx3", engine_config={
            "rate": 160,
            "volume": 0.9
        })
        
        # Read the file
        with open(sample_file, "r") as f:
            text = f.read()
        
        # Convert to speech and save to file
        output_file = os.path.join(output_dir, "file_to_speech.wav")
        print(f"Converting text file to speech and saving to {output_file}")
        
        tts.save_to_file(text, output_file)
        print("✓ File to speech conversion completed")
    
    except Exception as e:
        print(f"✗ Error: {e}")

def voice_selection_example():
    """Demonstrate selecting different voices."""
    print("\nAdvanced Example 3: Voice Selection")
    print("--------------------------------")
    
    try:
        tts = TextToSpeech()
        
        # Get available voices
        voices = tts.list_voices()
        
        if not voices:
            print("No voices available for this engine.")
            return
        
        # Show available voices
        print(f"Found {len(voices)} voices.")
        
        # Try to use different voices (will only work if multiple voices are installed)
        if len(voices) >= 2:
            # Use the first voice
            first_voice = voices[0]["id"]
            print(f"Setting voice to: {voices[0]['name']}")
            tts.set_voice(first_voice)
            tts.speak("This is the first voice.")
            
            time.sleep(1)
            
            # Use the second voice
            second_voice = voices[1]["id"]
            print(f"Setting voice to: {voices[1]['name']}")
            tts.set_voice(second_voice)
            tts.speak("This is the second voice.")
        else:
            print("Only one voice available.")
            tts.speak("Only one voice is available on this system.")
        
        print("✓ Voice selection example completed")
        
    except TTSError as e:
        print(f"✗ Error: {e}")

def main():
    """Run the advanced usage examples."""
    parser = argparse.ArgumentParser(description="PyTTSLib Advanced Examples")
    parser.add_argument("--example", type=int, choices=[1, 2, 3], 
                        help="Run a specific example (1-3)")
    args = parser.parse_args()
    
    print("PyTTSLib Advanced Usage Examples")
    print("===============================")
    
    if args.example == 1 or args.example is None:
        process_long_text_example()
    
    if args.example == 2 or args.example is None:
        file_to_speech_example()
    
    if args.example == 3 or args.example is None:
        voice_selection_example()
    
    print("\nAdvanced examples completed!")

if __name__ == "__main__":
    main() 