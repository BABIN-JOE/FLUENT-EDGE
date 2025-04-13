import unittest
from fluent_edge_core.punctuation_restorer import restore_punctuation

class TestPunctuationRestorer(unittest.TestCase):

    def test_restoring_punctuation(self):
        # Test for restoring punctuation in a sentence
        text = "this is an example of a sentence without punctuation"
        expected = "This is an example of a sentence without punctuation."
        result = restore_punctuation(text)
        self.assertEqual(result, expected)  # Should restore punctuation and capitalize first letter

    def test_restoring_punctuation_with_incomplete_text(self):
        # Test for incomplete text without proper punctuation
        text = "another example without period"
        expected = "Another example without period."
        result = restore_punctuation(text)
        self.assertEqual(result, expected)  # Should add period and capitalize first letter

    def test_empty_text(self):
        # Test for empty text input
        text = ""
        expected = ""
        result = restore_punctuation(text)
        self.assertEqual(result, expected)  # Empty input should return empty output

    def test_single_word_text(self):
        # Test for single word text without punctuation
        text = "hello"
        expected = "Hello."
        result = restore_punctuation(text)
        self.assertEqual(result, expected)  # Single word should be capitalized and have period

if __name__ == "__main__":
    unittest.main()
