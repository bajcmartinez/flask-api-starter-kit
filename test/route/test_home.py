from unittest import TestCase
from app import create_app


class TestWelcome(TestCase):
    def setUp(self):
        self.app = create_app().test_client()

    def test_welcome(self):
        """
        Tests the route screen message
        """
        rv = self.app.get('/api/')

        # If we recalculate the hash on the block we should get the same result as we have stored
        self.assertEqual({"message": 'Hello World!'}, rv.get_json())
