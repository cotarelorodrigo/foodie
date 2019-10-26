import unittest
import pytest
from unittest.mock import patch
import json
from src.auth.controllers.baseTest import BaseTest

class LoginTestCase(BaseTest):

    def test_login_without_passwd_field(self):
        response = self.client.post(
            '/user/login',
            data=json.dumps({
                "email": "asd@asd.com"
            }),
            content_type='application/json'
        )

        assert response._status_code == 410

    def test_login_with_not_register_user(self):
        response = self.client.post(
            '/user',
            data=json.dumps({
                "name": "Rodrigo",
                "email": "asd@asd.com",
                "phone_number": 42223333,
                "role": "usuario",
                "password": "123123",
                "firebase_uid": "rjrr",
                "suscripcion": "flat"
            }),
            content_type='application/json'
        )
        assert response._status_code == 200
        response = self.client.post(
            '/user/login',
            data=json.dumps({
                "email": "nada@nada.com",
                "password": "123123"
            }),
            content_type='application/json'
        )
        assert response._status_code == 411

    def test_login_wrong_passwd(self):
        response = self.client.post(
            '/user',
            data=json.dumps({
                "name": "Rodrigo",
                "email": "asdd@asdd.com",
                "phone_number": 42223333,
                "role": "usuario",
                "password": "123123",
                "firebase_uid": "rjrrsrjs",
                "suscripcion": "flat"
            }),
            content_type='application/json'
        )
        assert response._status_code == 200
        response = self.client.post(
            '/user/login',
            data=json.dumps({
                "email": "asdd@asdd.com",
                "password": "123233312211221"
            }),
            content_type='application/json'
        )
        assert response._status_code == 412


    def test_good_login(self):
        response = self.client.post(
            '/user',
            data=json.dumps({
                "name": "Rodrigo",
                "email": "asddd@asddd.com",
                "phone_number": 42223333,
                "role": "usuario",
                "password": "123",
                "firebase_uid": "agrrr",
                "suscripcion": "flat"
            }),
            content_type='application/json'
        )
        assert response._status_code == 200
        response = self.client.post(
            '/user/login',
            data=json.dumps({
                "email": "asddd@asddd.com",
                "password": "123"
            }),
            content_type='application/json'
        )
        assert response._status_code == 200
