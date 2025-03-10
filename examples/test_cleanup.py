"""
Test script to verify the proper creation and cleanup of temporary audio files.
"""

import os
import sys
import time

# Add the parent directory to the Python path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pyttslib import TextToSpeech, TTSError

def main():
    """Run the cleanup test."""
    print("PyTTSLib Cleanup Test")
    print("====================")
    
    # Create a TTS instance
    print("\nCreating Google TTS instance...")
    tts = TextToSpeech(engine="google")
    
    # Get the temporary directory path
    temp_dir = tts.temp_dir
    print(f"Temporary directory: {temp_dir}")
    
    # Generate some speech
    print("\nGenerating speech...")
    for i in range(3):
        print(f"\nTest {i+1}:")
        tts.speak(f"This is test number {i+1} to verify audio file cleanup.")
        time.sleep(1)
    
    # Check if the directory exists and see what's inside
    print("\nChecking temporary directory contents:")
    if os.path.exists(temp_dir):
        files = os.listdir(temp_dir)
        if files:
            print(f"Found {len(files)} files in temporary directory:")
            for file in files:
                print(f"  - {file}")
        else:
            print("Temporary directory is empty. All files were properly deleted.")
    else:
        print("Temporary directory does not exist.")
    
    # Manually call cleanup
    print("\nManually calling cleanup...")
    tts.cleanup()
    
    # Check again after cleanup
    print("\nChecking temporary directory after manual cleanup:")
    if os.path.exists(temp_dir):
        files = os.listdir(temp_dir)
        if files:
            print(f"Found {len(files)} files in temporary directory:")
            for file in files:
                print(f"  - {file}")
        else:
            print("Temporary directory is empty. All files were properly deleted.")
    else:
        print("Temporary directory was removed during cleanup.")
    
    print("\nTest completed.")

if __name__ == "__main__":
    main() 