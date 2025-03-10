"""
Utility functions for the PyTTSLib package.

This module provides helper functions and utilities that support the main
text-to-speech functionality but aren't directly part of the core API.
"""

import os
import re
from typing import List, Optional

def text_to_chunks(text: str, max_length: int = 1000) -> List[str]:
    """
    Split text into chunks to handle TTS engine limitations.
    
    Some TTS engines have limitations on the length of text they can process at once.
    This function splits long text into smaller chunks at sentence boundaries when possible.
    
    Args:
        text (str): The text to split into chunks
        max_length (int, optional): Maximum length of each chunk. Defaults to 1000 characters.
        
    Returns:
        List[str]: List of text chunks, each no longer than max_length
    """
    if len(text) <= max_length:
        return [text]
    
    # Split on sentence boundaries (period, question mark, exclamation point)
    sentence_endings = r'[.!?][\s]+'
    sentences = re.split(sentence_endings, text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        # Add back the sentence ending that was removed by the split
        if sentence != sentences[-1]:
            sentence += "."
            
        # If adding this sentence would exceed max_length, start a new chunk
        if len(current_chunk) + len(sentence) > max_length:
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # If the sentence itself is longer than max_length, split it further
            if len(sentence) > max_length:
                words = sentence.split()
                current_chunk = ""
                
                for word in words:
                    if len(current_chunk) + len(word) + 1 > max_length:
                        chunks.append(current_chunk.strip())
                        current_chunk = word + " "
                    else:
                        current_chunk += word + " "
            else:
                current_chunk = sentence + " "
        else:
            current_chunk += sentence + " "
    
    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def is_supported_audio_format(file_path: str) -> bool:
    """
    Check if the file extension is a supported audio format.
    
    Args:
        file_path (str): Path to the audio file
        
    Returns:
        bool: True if the file format is supported, False otherwise
    """
    supported_formats = ['.mp3', '.wav', '.ogg', '.aiff']
    _, ext = os.path.splitext(file_path)
    return ext.lower() in supported_formats

def ensure_dir_exists(file_path: str) -> None:
    """
    Ensure that the directory for the given file path exists.
    
    Args:
        file_path (str): Path to a file
        
    Returns:
        None
    """
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory) 