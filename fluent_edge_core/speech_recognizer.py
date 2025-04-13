import vosk
import json
import os
import sys
from .audio_handler import audio_queue
from .punctuation_restorer import PunctuationRestorer

# Define the path to the Vosk model for Indian English
MODEL_PATH = "model/Indian English/vosk-model-en-in-0.5"
# Check if the model path exists, if not, exit the program with an error message
if not os.path.exists(MODEL_PATH):
    print(f"❌ ERROR: Vosk model not found at '{MODEL_PATH}'.", flush=True)
    sys.exit(1)

# Load the Vosk model once at the start
model = vosk.Model(MODEL_PATH)
print("✅ Vosk model loaded.", flush=True)

# Initialize the punctuation restorer instance
punctuation_restorer = PunctuationRestorer()

def transcribe_audio(full_transcription, stop_recording):
    """
    Transcribes the audio input and restores punctuation in the transcribed text.

    :param full_transcription: A list that will hold the final, punctuated transcription.
    :param stop_recording: A threading event used to stop recording when needed.
    :return: The full transcription with restored punctuation.
    """
    
    # Initialize the recognizer with the Vosk model and a sample rate of 16000 Hz
    rec = vosk.KaldiRecognizer(model, 16000)
    
    # List to hold the raw transcription (without punctuation)
    raw_transcription = []
    
    # Process audio data in a loop until the recording is stopped
    while not stop_recording.is_set():
        if not audio_queue.empty():  # Check if there's data in the audio queue
            data = audio_queue.get()  # Retrieve the audio data from the queue
            # Try to process the audio data and get the recognition result
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())  # Convert the result to a JSON object
                text = result.get("text", "")  # Extract the transcribed text
                if text:  # If the transcribed text is not empty
                    # Process the text with the punctuation restorer (for streaming text)
                    processed_text = punctuation_restorer.process_streaming_text(text)
                    # Append the processed text to the full transcription and raw transcription lists
                    full_transcription.append(processed_text)
                    raw_transcription.append(text)
                    # Print the live transcription (for debugging or monitoring purposes)
                    print(f"📝 Live: {text}", flush=True)
    
    # Once recording stops, process the complete transcription with full punctuation restoration
    complete_raw_text = " ".join(raw_transcription)  # Join raw transcription into a single string
    punctuated_text = punctuation_restorer.restore_punctuation(complete_raw_text)  # Restore punctuation
    
    # Clear the full_transcription list and append the properly punctuated transcription
    full_transcription.clear()
    full_transcription.append(punctuated_text)
    
    # Return the punctuated transcription
    return punctuated_text
