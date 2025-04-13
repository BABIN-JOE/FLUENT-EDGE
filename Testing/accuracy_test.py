import unittest
from fluent_edge_core.accuracy_checker import calculate_accuracy

class TestAccuracyChecker(unittest.TestCase):

    def test_accuracy_with_no_errors(self):
        # Test for transcription with no errors
        text = "This is a correct sentence."
        corrections = []  # No grammar errors
        accuracy = calculate_accuracy(text, corrections)
        self.assertEqual(accuracy, 100.0)  # Should be 100% accuracy

    def test_accuracy_with_some_errors(self):
        # Test for transcription with some grammar errors
        text = "She go to school yesterday."
        corrections = [
            {"sentence": "She go to school yesterday.", "message": "Past tense required", "suggestions": ["Went"]},
        ]
        accuracy = calculate_accuracy(text, corrections)
        expected_accuracy = 100 - (len(corrections) / len(text.split()) * 100)
        self.assertEqual(accuracy, round(expected_accuracy, 2))  # Should be calculated based on errors

    def test_accuracy_with_empty_text(self):
        # Test for empty transcription text
        text = ""
        corrections = []
        accuracy = calculate_accuracy(text, corrections)
        self.assertEqual(accuracy, 0)  # No text means 0% accuracy

    def test_accuracy_with_invalid_corrections(self):
        # Test for invalid corrections format (e.g., not a list)
        text = "This is a sentence."
        corrections = None  # Invalid format
        accuracy = calculate_accuracy(text, corrections)
        self.assertEqual(accuracy, 0)  # Should return 0% accuracy due to invalid corrections

if __name__ == "__main__":
    unittest.main()
