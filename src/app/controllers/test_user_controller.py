import unittest
from unittest.mock import patch
import json
from src.app import app
from src.app.services import user_service

mock_user = {"fullName": "Rodrigo", "email":"asd@asd.com", "password":"asfaga", "signUpDate":"2019-02-15" , "firebaseUid":"DGHAHAEHR", "picture":"garehqerae"}

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

    @patch("src.app.services.user_service.UserService.check_email")
    def test_check_existing_email(self, check_email_mock):
        check_email_mock.return_value = True
        response = self.app.head('/user/email/asd@asd.com')
        assert response._status_code == 200
    
    @patch("src.app.services.user_service.UserService.get_user")
    def test_check_existing_id(self, check_id_mock):
        check_id_mock.return_value = True
        response = self.app.head('/user/1')
        assert response._status_code == 200

    @patch("src.app.services.user_service.UserService.get_user")
    def test_check_nonexisting_id(self, check_id_mock):
        check_id_mock.return_value = False
        response = self.app.head('/user/2')
        assert response._status_code == 404

    @patch("src.app.services.user_service.UserService.delete_user")
    def test_delete_existing_id(self, delete_id_mock):
        delete_id_mock.return_value = True
        response = self.app.delete('/user/1')
        assert response._status_code == 200

    @patch("src.app.services.user_service.UserService.delete_user")
    def test_delete_nonexisting_id(self, delete_id_mock):
        delete_id_mock.return_value = False
        response = self.app.delete('/user/2')
        assert response._status_code == 404



