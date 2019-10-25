import unittest
import pytest
from unittest.mock import patch
import json
from src.auth.controllers.baseTest import BaseTest

class RegisterTestCase(BaseTest):

    def test_register_user(self):
        response = self.client.post(
            '/register/user',
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

    def test_register_delivery(self):
        response = self.client.post(
            '/register/delivery',
            data=json.dumps({
                "name": "Rodrigo",
                "email": "asd@asdtk.com",
                "phone_number": 42223333,
                "role": "usuario",
                "password": "password",
                "firebase_uid": "ajsjfkasf",
                "picture": "www.photo.com",
                "balance": 100
            }),
            content_type='application/json'
        )

        assert response._status_code == 200