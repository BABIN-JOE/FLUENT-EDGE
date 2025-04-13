import sounddevice as sd
import queue
import sys

# Queue for storing audio data
audio_queue = queue.Queue()

# Callback function to capture audio data
def audio_callback(indata, frames, time, status):
    """
    Callback function that gets called by the audio stream for each block of audio data captured.

    :param indata: The input audio data in raw format.
    :param frames: The number of frames in the audio block.
    :param time: Timestamp information about the current audio block.
    :param status: Status information related to the audio stream (e.g., overflow or underflow).
    """
    if status:
        print(f"⚠️ Audio status: {status}", file=sys.stderr, flush=True)  # Print warnings to stderr if any
    audio_queue.put(bytes(indata))  # Store the captured audio data in the queue

# Function to start audio recording
def start_recording():
    """
    Starts an audio recording stream using the sounddevice library.

    :return: The stream object if recording starts successfully, otherwise None.
    """
    try:
        # Initialize the audio input stream with specific parameters
        stream = sd.RawInputStream(
            samplerate=16000,  # Set the sample rate to 16kHz
            blocksize=4000,    # Block size of 4000 frames per callback
            dtype='int16',     # Audio data type (16-bit signed integers)
            channels=1,        # Mono audio (single channel)
            callback=audio_callback  # Set the callback function to capture audio
        )
        stream.start()  # Start the audio stream
        print("🎤 Audio stream started.", flush=True)  # Inform the user that recording has started
        return stream  # Return the stream object
    except Exception as e:
        print(f"❌ ERROR: Failed to start audio recording. {e}", flush=True)  # Print error message if stream fails to start
        return None  # Return None to indicate failure

# Function to stop audio recording
def stop_recording(stream):
    """
    Stops the audio recording stream and releases the resources.

    :param stream: The audio stream to stop.
    """
    if stream:
        stream.stop()  # Stop the audio stream
        stream.close()  # Close the audio stream
        print("🎤 Audio stream stopped.", flush=True)  # Inform the user that recording has stopped
