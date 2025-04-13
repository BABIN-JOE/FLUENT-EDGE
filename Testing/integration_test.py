import unittest
from fluent_edge_core.audio_handler import record_audio, transcribe_audio
from fluent_edge_core.grammar_checker import check_grammar

class IntegrationTest(unittest.TestCase):
    def test_full_transcription_process(self):
        # Simulate the complete process from recording to transcription and grammar checking
        audio_file = record_audio()
        transcription = transcribe_audio(audio_file)
        errors = check_grammar(transcription)

        self.assertTrue(transcription)  # Ensure transcription is returned
        self.assertGreater(len(errors), 0)  # Grammar errors should be checked

if __name__ == '__main__':
    unittest.main()
