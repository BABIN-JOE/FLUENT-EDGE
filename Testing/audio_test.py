import unittest
from fluent_edge_core.audio_handler import record_audio, transcribe_audio  # Adjust imports

class AudioTest(unittest.TestCase):
    def test_audio_recording(self):
        audio_file = record_audio()  # Assuming this function saves the audio
        self.assertTrue(audio_file)  # Check if the audio file is recorded

    def test_audio_transcription(self):
        audio_file = "path_to_audio.wav"  # Provide an actual audio file path for testing
        transcription = transcribe_audio(audio_file)
        self.assertTrue(transcription)  # Check if transcription is returned

if __name__ == '__main__':
    unittest.main()
