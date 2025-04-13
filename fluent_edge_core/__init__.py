# Importing necessary functions and classes from other modules
from .audio_handler import start_recording, stop_recording  # Handles starting and stopping audio recording
from .speech_recognizer import transcribe_audio  # Handles audio transcription to text
from .grammar_checker import check_grammar  # Checks the grammar of the transcribed text
from .accuracy_checker import calculate_accuracy  # Calculates the accuracy of the transcription
from .punctuation_restorer import PunctuationRestorer  # Restores punctuation to the transcribed text

# Define the public interface of this module
__all__ = [
    'start_recording',        # Allows external modules to access the start_recording function
    'stop_recording',         # Allows external modules to access the stop_recording function
    'transcribe_audio',       # Allows external modules to access the transcribe_audio function
    'check_grammar',          # Allows external modules to access the check_grammar function
    'calculate_accuracy',     # Allows external modules to access the calculate_accuracy function
    'PunctuationRestorer'     # Allows external modules to access the PunctuationRestorer class
]
