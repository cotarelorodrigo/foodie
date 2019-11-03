import unittest
import pytest
from unittest.mock import patch
import json
from src.auth.services import user_service
from src.auth.controllers.baseTest import BaseTest
import jwt

mock_user = {"fullName": "Rodrigo", "email":"asd@asd.com", "password":"asfaga", "signUpDate":"2019-02-15" , "firebaseUid":"DGHAHAEHR", "picture":"garehqerae"}

class UserTestCase(BaseTest):

    def test_wrong_less_fields_new_user(self):
        response = self.client.post(
            '/user',
            data=json.dumps({
                "fullName": "realuser",
                "email": "extra",
                "password": "password"
            }),
            content_type='application/json'
        )

        assert response._status_code == 420

    @patch("src.auth.services.user_service.UserService.check_email")
    def test_check_existing_email(self, check_email_mock):
        check_email_mock.return_value = True
        response = self.client.head('/user/email/asd@asd.com')
        assert response._status_code == 200
    
    @patch("src.auth.services.user_service.UserService.get_user")
    def test_check_existing_id(self, check_id_mock):
        check_id_mock.return_value = True
        response = self.client.head('/user/1')
        assert response._status_code == 200

    @patch("src.auth.services.user_service.UserService.get_user")
    def test_check_nonexisting_id(self, check_id_mock):
        check_id_mock.return_value = False
        response = self.client.head('/user/2')
        assert response._status_code == 404

    @patch("src.auth.services.user_service.UserService.delete_user")
    def test_delete_existing_id(self, delete_id_mock):
        delete_id_mock.return_value = True
        response = self.client.delete('/user/1')
        assert response._status_code == 200

    @patch("src.auth.services.user_service.UserService.delete_user")
    def test_delete_nonexisting_id(self, delete_id_mock):
        delete_id_mock.return_value = False
        response = self.client.delete('/user/2')
        assert response._status_code == 404

    @patch("jwt.decode")
    def test_user_profile(self, jwt_decode):
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
        jwt_decode.return_value = 'token_valido'
        response = self.client.get('/user/profile/asddd@asddd.com', headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200



