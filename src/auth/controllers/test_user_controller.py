import unittest
from unittest.mock import patch
import json

from src.app import app


class AuthControllerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_wrong_less_fields_new_user(self):
        response = self.app.post(
            '/user',
            data=json.dumps({
                "fullName": "realuser",
                "email": "extra",
                "password": "password"
            }),
            content_type='application/json'
        )

        assert response._status_code == 420