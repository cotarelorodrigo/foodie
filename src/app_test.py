import unittest
from src.auth.controllers.baseTest import BaseTest

class TestApp(BaseTest):

    def test_hello_world(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)