import sounddevice as sd
import numpy as np

def test_audio(duration=5, samplerate=16000):
    """
    Test microphone functionality by recording audio for a specified duration.

    :param duration: The duration (in seconds) to record audio.
    :param samplerate: The sample rate for recording (default is 16000 Hz).
    :return: Recorded audio as a numpy array.
    """
    print(f"Recording for {duration} seconds... Speak now!")
    # Record audio for the specified duration
    audio = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is finished
    print("Recording complete!")
    return audio

# Example test call
if __name__ == "__main__":
    audio_data = test_audio()  # You can specify duration and sample rate here
    print("Audio captured:", np.any(audio_data))  # Print if any audio was recorded (non-empty array)
