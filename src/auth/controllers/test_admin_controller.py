import unittest
from unittest.mock import patch
import json
from src.auth.controllers.baseTest import BaseTest
import jwt

class AdminTestCase(BaseTest):

    @patch("jwt.decode")
    def test_admin_statics(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/statics',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200