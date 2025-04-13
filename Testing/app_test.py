import unittest
from app import app  # Assuming your Flask app is in 'app.py'

class AppTest(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()  # Flask test client

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)  # Check if the home page loads

    def test_start_button(self):
        response = self.client.get('/start')  # Replace with the actual route for the Start button
        self.assertEqual(response.status_code, 200)

    def test_stop_button(self):
        response = self.client.get('/stop')  # Replace with the actual route for the Stop button
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
