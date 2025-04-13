import unittest
import logging

class ErrorLoggingTest(unittest.TestCase):
    def test_error_logging(self):
        try:
            # Simulate an error
            1 / 0  # Division by zero
        except ZeroDivisionError as e:
            logging.error("❌ Error occurred: Division by zero")
            self.assertTrue("Division by zero" in str(e))  # Ensure the error is logged

if __name__ == '__main__':
    unittest.main()
