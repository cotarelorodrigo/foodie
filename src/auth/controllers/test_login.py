import unittest
import pytest
from unittest.mock import patch
import json
from src.auth.controllers.baseTest import BaseTest

class LoginTestCase(BaseTest):

    def test_login(self):
        response = self.client.post(
            '/user/login',
            data=json.dumps({
                "name": "Rodrigo",
                "email": "asd@asd.com",
                "phone_number": 42223333,
                "role": "usuario",
                "password": "password",
                "firebase_uid": "rjrr",
                "suscripcion": "flat"
            }),
            content_type='application/json'
        )

        assert response._status_code == 200
