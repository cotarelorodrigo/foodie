import unittest
from src.app import app


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_hello_world(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)