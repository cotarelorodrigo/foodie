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
                "email": "asd@asd.com",
                "password": "password"
            }),
            content_type='application/json'
        )

        assert response._status_code == 200
