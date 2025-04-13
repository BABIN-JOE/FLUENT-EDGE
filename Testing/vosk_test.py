import unittest
from fluent_edge_core.audio_handler import transcribe_audio  # Adjust import according to your project structure
from vosk import Model, KaldiRecognizer
import os
import wave

class VoskTest(unittest.TestCase):
    
    def setUp(self):
        # Load the Vosk model before each test
        model_path = "model/Indian English/vosk-model-en-in-0.5"  # Path to the Vosk model
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)  # Assuming 16000 Hz audio rate

    def test_audio_transcription_with_vosk(self):
        # Test that Vosk can correctly transcribe a known audio file
        audio_file = "testing_audio.wav"  # Path to the test audio file
        transcription = self.transcribe_audio_with_vosk(audio_file)

        # Check if the transcription is not empty
        self.assertTrue(transcription)
        self.assertIsInstance(transcription, str)  # Ensure it's a string

    def transcribe_audio_with_vosk(self, audio_path):
        """
        Function to transcribe audio using Vosk API.
        
        :param audio_path: Path to the audio file
        :return: Transcribed text from the audio
        """
        if not os.path.exists(audio_path):
            self.fail(f"Test audio file does not exist: {audio_path}")

        # Open the audio file for reading
        with wave.open(audio_path, "rb") as wf:
            if wf.getframerate() != 16000:
                self.fail(f"Audio file must have a 16kHz sample rate, but got {wf.getframerate()}Hz.")
            
            recognizer = self.recognizer
            result = ''
            while True:
                data = wf.readframes(4000)
                if len(data) == 0:
                    break
                if recognizer.AcceptWaveform(data):
                    result += recognizer.Result()
                else:
                    result += recognizer.PartialResult()

            # Final result (end of speech)
            result += recognizer.FinalResult()
            return result

    def test_invalid_audio_file(self):
        # Test handling of an invalid audio file
        invalid_audio = "nonexistent_audio.wav"  # Invalid path
        with self.assertRaises(FileNotFoundError):
            self.transcribe_audio_with_vosk(invalid_audio)

    def test_empty_audio(self):
        # Test empty or silent audio
        empty_audio = "silent_audio.wav"  # Path to a silent audio file
        transcription = self.transcribe_audio_with_vosk(empty_audio)
        self.assertEqual(transcription, '{"text":""}')  # Expect an empty transcription for silent audio

if __name__ == "__main__":
    unittest.main()
