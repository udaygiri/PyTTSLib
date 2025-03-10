"""
Core TTS module implementing the main TextToSpeech class and its functionality.
"""

import os
import tempfile
import platform
import time
import subprocess
import shutil
from typing import Dict, List, Optional, Union, Any

# Import TTS engines
import pyttsx3
from gtts import gTTS
import playsound

from .exceptions import TTSError, EngineNotFoundError

class TextToSpeech:
    """
    Main TextToSpeech class that provides a unified interface for different TTS engines.
    
    This class supports multiple text-to-speech engines and provides methods for
    converting text to speech, saving audio to files, and customizing voice properties.
    
    Attributes:
        engine (str): The name of the TTS engine being used
        engine_instance: The instance of the TTS engine
        config (dict): Configuration parameters for the TTS engine
    """
    
    def __init__(self, engine: str = "pyttsx3", engine_config: Optional[Dict[str, Any]] = None):
        """
        Initialize a new TextToSpeech instance with the specified engine.
        
        Args:
            engine (str): The name of the TTS engine to use. Options: "pyttsx3" (default), "google"
            engine_config (dict, optional): Configuration parameters for the engine.
                Default is None, which uses engine defaults.
        
        Raises:
            EngineNotFoundError: If the specified engine is not supported.
        """
        self.engine = engine.lower()
        self.config = engine_config or {}
        self.engine_instance = None
        
        # Create a dedicated folder for temporary audio files
        self.temp_dir = os.path.join(tempfile.gettempdir(), "pyttslib_audio")
        if not os.path.exists(self.temp_dir):
            os.makedirs(self.temp_dir)
            
        print(f"Temporary audio files will be stored in: {self.temp_dir}")
        
        # Track temporary files for cleanup
        self._temp_files = []
        
        # Initialize the appropriate engine
        if self.engine == "pyttsx3":
            self._init_pyttsx3()
        elif self.engine == "google":
            self._init_google_tts()
        else:
            raise EngineNotFoundError(f"Engine '{engine}' is not supported. Use 'pyttsx3' or 'google'.")
    
    def __del__(self):
        """Destructor to ensure cleanup of any remaining temporary files."""
        self._cleanup_temp_files()
        self._cleanup_temp_folder()
    
    def _cleanup_temp_files(self):
        """Clean up all tracked temporary files."""
        for temp_file in self._temp_files[:]:  # Create a copy of the list to avoid modification during iteration
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    print(f"Deleted temporary file: {os.path.basename(temp_file)}")
                self._temp_files.remove(temp_file)
            except Exception as e:
                print(f"Failed to delete temporary file {os.path.basename(temp_file)}: {str(e)}")
    
    def _cleanup_temp_folder(self):
        """Clean up all files in the temporary folder."""
        try:
            # Delete all files in the temporary folder
            for filename in os.listdir(self.temp_dir):
                file_path = os.path.join(self.temp_dir, filename)
                if os.path.isfile(file_path):
                    try:
                        os.unlink(file_path)
                        print(f"Deleted file from temp folder: {filename}")
                    except Exception as e:
                        print(f"Failed to delete file {filename}: {str(e)}")
        except Exception as e:
            print(f"Error cleaning temp folder: {str(e)}")
    
    def _init_pyttsx3(self):
        """Initialize the pyttsx3 TTS engine with configuration."""
        try:
            self.engine_instance = pyttsx3.init()
            
            # Apply configuration if provided
            if "rate" in self.config:
                self.engine_instance.setProperty("rate", self.config["rate"])
            
            if "volume" in self.config:
                self.engine_instance.setProperty("volume", self.config["volume"])
                
            if "voice" in self.config:
                self.engine_instance.setProperty("voice", self.config["voice"])
        
        except Exception as e:
            raise TTSError(f"Failed to initialize pyttsx3 engine: {str(e)}")
    
    def _init_google_tts(self):
        """Initialize the Google TTS engine configuration."""
        # Google TTS is initialized on-demand for each request
        self.engine_instance = {
            "lang": self.config.get("lang", "en"),
            "tld": self.config.get("tld", "com"),
            "slow": self.config.get("slow", False)
        }
    
    def _play_audio_file_windows(self, file_path):
        """
        Play an audio file on Windows using the most reliable method available.
        
        Args:
            file_path (str): Path to the audio file to play
            
        Returns:
            bool: True if playback was successful, False otherwise
        """
        # Method 1: Try winsound (most reliable for WAV files)
        try:
            import winsound
            # Check if it's a WAV file (winsound only supports WAV)
            if file_path.lower().endswith('.wav'):
                winsound.PlaySound(file_path, winsound.SND_FILENAME)
                return True
        except Exception:
            pass
            
        # Method 2: Try PowerShell's System.Media.SoundPlayer (good for WAV files)
        try:
            ps_path = file_path.replace("'", "''")
            cmd = f'powershell -c "(New-Object Media.SoundPlayer \'{ps_path}\').PlaySync()"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                return True
        except Exception:
            pass
            
        # Method 3: Try Windows Media Player
        try:
            # Escape the path for the command line
            cmd = f'powershell -c "Add-Type -AssemblyName PresentationCore; ' \
                  f'$mediaPlayer = New-Object System.Windows.Media.MediaPlayer; ' \
                  f'$mediaPlayer.Open(\'{ps_path}\'); ' \
                  f'$mediaPlayer.Play(); ' \
                  f'Start-Sleep -s 5; ' \
                  f'$mediaPlayer.Stop()"'
            subprocess.run(cmd, shell=True, timeout=10)
            return True
        except Exception:
            pass
            
        # Method 4: Last resort - try playsound
        try:
            playsound.playsound(file_path)
            return True
        except Exception:
            pass
            
        return False  # All methods failed
    
    def _play_audio_file_unix(self, file_path):
        """
        Play an audio file on Unix-like systems (Linux, macOS) using the most reliable method available.
        
        Args:
            file_path (str): Path to the audio file to play
            
        Returns:
            bool: True if playback was successful, False otherwise
        """
        # Method 1: Try playsound
        try:
            playsound.playsound(file_path)
            return True
        except Exception:
            pass
            
        # Method 2: Try using native command-line players
        players = [
            ['afplay', file_path],  # macOS
            ['aplay', file_path],   # Linux
            ['mpg123', file_path],  # Linux, MP3
            ['mpg321', file_path],  # Linux, MP3 alternative
            ['play', file_path],    # SoX
        ]
        
        for player in players:
            try:
                subprocess.run(player, check=True)
                return True
            except Exception:
                pass
                
        return False  # All methods failed
    
    def _create_temp_file(self, suffix=".mp3"):
        """
        Create a temporary file in the dedicated temporary directory.
        
        Args:
            suffix (str): File extension to use for the temporary file
            
        Returns:
            str: Path to the created temporary file
        """
        # Create a unique filename based on timestamp to avoid conflicts
        timestamp = int(time.time() * 1000)
        filename = f"pyttslib_audio_{timestamp}{suffix}"
        file_path = os.path.join(self.temp_dir, filename)
        
        # Add to tracked files list
        self._temp_files.append(file_path)
        
        return file_path
    
    def _play_audio_file(self, file_path):
        """
        Play an audio file using the appropriate method for the current platform.
        Ensures the audio playback completes before returning.
        
        Args:
            file_path (str): Path to the audio file to play
        
        Raises:
            TTSError: If there is an error playing the audio file
        """
        try:
            # Display a message about playing
            print(f"Playing audio... (file: {os.path.basename(file_path)})")
                
            # Choose platform-specific playback method
            playback_success = False
            if platform.system() == 'Windows':
                playback_success = self._play_audio_file_windows(file_path)
            else:
                playback_success = self._play_audio_file_unix(file_path)
                
            # If all playback methods failed, inform the user
            if not playback_success:
                print(f"Could not play audio automatically. File saved at: {file_path}")
                print("You can play this file manually.")
                # Keep the file since we couldn't play it
                return
                
            print("Audio playback completed.")
        
        except Exception as e:
            print(f"Warning: Error during audio playback: {str(e)}")
        finally:
            # Give time for any buffered audio to complete playback
            time.sleep(0.5)
            # Delete the file after playback
            self._delete_audio_file(file_path)
    
    def _delete_audio_file(self, file_path):
        """
        Delete an audio file with multiple retries to ensure it's removed.
        
        Args:
            file_path (str): Path to the audio file to delete
        """
        # Try to delete the file up to 3 times (useful if file is still locked)
        for attempt in range(3):
            try:
                if os.path.exists(file_path) and file_path in self._temp_files:
                    os.unlink(file_path)
                    self._temp_files.remove(file_path)
                    print(f"Successfully deleted audio file: {os.path.basename(file_path)}")
                    return
            except Exception as e:
                if attempt < 2:  # Don't log on the last attempt
                    print(f"Note: Could not delete temporary audio file on attempt {attempt+1}. Will retry.")
                # If deletion fails, wait a bit longer each time and try again
                time.sleep(0.5 * (attempt + 1))
                
        # If we reach here, we couldn't delete the file after all attempts
        print(f"Note: Could not delete temporary audio file: {os.path.basename(file_path)}")
        print("The file will be deleted when the program exits.")
    
    def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.
        
        Args:
            text (str): The text to convert to speech
            
        Raises:
            TTSError: If there is an error during speech synthesis or playback
        """
        if not text:
            return
            
        temp_filename = None
        try:
            if self.engine == "pyttsx3":
                self.engine_instance.say(text)
                self.engine_instance.runAndWait()
            
            elif self.engine == "google":
                # For Google TTS, we need to save to a temporary file and play it
                try:
                    # Create a temp file in our dedicated temp directory
                    temp_filename = self._create_temp_file(suffix=".mp3")
                    
                    # Create the TTS file
                    tts = gTTS(
                        text=text,
                        lang=self.engine_instance["lang"],
                        tld=self.engine_instance["tld"],
                        slow=self.engine_instance["slow"]
                    )
                    tts.save(temp_filename)
                    
                    # Play the audio file with improved error handling
                    self._play_audio_file(temp_filename)
                    
                except Exception as e:
                    raise TTSError(f"Error during Google TTS processing: {str(e)}")
                    
        except Exception as e:
            raise TTSError(f"Error during speech synthesis: {str(e)}")
        finally:
            # Clean up any temporary files that might remain
            self._cleanup_temp_files()
    
    def save_to_file(self, text: str, output_file: str) -> None:
        """
        Convert text to speech and save it to a file.
        
        Args:
            text (str): The text to convert to speech
            output_file (str): Path to the output audio file
            
        Raises:
            TTSError: If there is an error during speech synthesis or saving
        """
        if not text:
            return
            
        try:
            if self.engine == "pyttsx3":
                # Get file extension to determine format
                _, ext = os.path.splitext(output_file)
                if not ext:
                    output_file += ".wav"  # Default to WAV if no extension
                
                self.engine_instance.save_to_file(text, output_file)
                self.engine_instance.runAndWait()
            
            elif self.engine == "google":
                tts = gTTS(
                    text=text,
                    lang=self.engine_instance["lang"],
                    tld=self.engine_instance["tld"],
                    slow=self.engine_instance["slow"]
                )
                tts.save(output_file)
                
        except Exception as e:
            raise TTSError(f"Error saving speech to file: {str(e)}")
    
    def set_rate(self, rate: int) -> None:
        """
        Set the speaking rate.
        
        Args:
            rate (int): Words per minute for pyttsx3. Typical values are between 100-200.
                        Not applicable for Google TTS (will be ignored).
                        
        Raises:
            TTSError: If there is an error setting the rate
        """
        if self.engine == "pyttsx3":
            try:
                self.engine_instance.setProperty("rate", rate)
            except Exception as e:
                raise TTSError(f"Error setting speech rate: {str(e)}")
        else:
            # For other engines, rate setting might not be applicable
            pass
    
    def set_volume(self, volume: float) -> None:
        """
        Set the speaking volume.
        
        Args:
            volume (float): Volume level from 0.0 to 1.0 for pyttsx3.
                           Not applicable for Google TTS (will be ignored).
                           
        Raises:
            TTSError: If there is an error setting the volume
        """
        if self.engine == "pyttsx3":
            try:
                volume = max(0.0, min(1.0, volume))  # Clamp between 0 and 1
                self.engine_instance.setProperty("volume", volume)
            except Exception as e:
                raise TTSError(f"Error setting speech volume: {str(e)}")
        else:
            # For other engines, volume setting might not be applicable
            pass
    
    def set_voice(self, voice_id: str) -> None:
        """
        Set the voice to use for speech.
        
        Args:
            voice_id (str): ID of the voice to use.
                For pyttsx3, this should be a voice ID from list_voices().
                For Google TTS, this should be a language code (e.g., 'en', 'fr', 'es').
                
        Raises:
            TTSError: If there is an error setting the voice
        """
        try:
            if self.engine == "pyttsx3":
                self.engine_instance.setProperty("voice", voice_id)
            elif self.engine == "google":
                self.engine_instance["lang"] = voice_id
        except Exception as e:
            raise TTSError(f"Error setting voice: {str(e)}")
    
    def list_voices(self) -> List[Dict[str, str]]:
        """
        Get a list of available voices for the current engine.
        
        Returns:
            list: A list of dictionary objects containing voice information.
                For pyttsx3, each dict contains 'id', 'name', and 'languages' keys.
                For Google TTS, a list of supported language codes.
                
        Raises:
            TTSError: If there is an error retrieving voices
        """
        if self.engine == "pyttsx3":
            try:
                voices = []
                for voice in self.engine_instance.getProperty("voices"):
                    voices.append({
                        "id": voice.id,
                        "name": voice.name,
                        "languages": voice.languages
                    })
                return voices
            except Exception as e:
                raise TTSError(f"Error listing voices: {str(e)}")
        elif self.engine == "google":
            # Return a predefined list of common language codes for Google TTS
            return [
                {"id": "en", "name": "English"},
                {"id": "fr", "name": "French"},
                {"id": "es", "name": "Spanish"},
                {"id": "de", "name": "German"},
                {"id": "it", "name": "Italian"},
                {"id": "pt", "name": "Portuguese"},
                {"id": "ru", "name": "Russian"},
                {"id": "ja", "name": "Japanese"},
                {"id": "ko", "name": "Korean"},
                {"id": "zh", "name": "Chinese"}
            ]
    
    def cleanup(self):
        """
        Clean up all temporary files and the temporary directory.
        This can be called manually to clean up resources before program exit.
        """
        print("Cleaning up all temporary files...")
        self._cleanup_temp_files()
        self._cleanup_temp_folder() 