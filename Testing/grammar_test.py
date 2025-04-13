import unittest
from fluent_edge_core.grammar_checker import check_grammar  # Import your grammar checking function

class GrammarTest(unittest.TestCase):
    def test_correct_text(self):
        text = "This is a correct sentence."
        errors = check_grammar(text)
        self.assertEqual(errors, [])  # No errors expected

    def test_incorrect_text(self):
        text = "She go to school."
        errors = check_grammar(text)
        self.assertGreater(len(errors), 0)  # Errors should be found

if __name__ == '__main__':
    unittest.main()
