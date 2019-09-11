import unittest
import requests
from src.app import app


class TestApp(unittest.TestCase):

    def test_hello_world(self):
        response = requests.get('http://localhost:4000/')
        self.assertEqual(response.status_code, 200)
