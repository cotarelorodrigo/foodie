import unittest
from unittest.mock import patch
import json
from src.app import app
#from src.auth.services import user_service

class AuthControllerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_add_order(self):
        response = self.app.post(
            '/orders',
            data=json.dumps({
                "shopId": 8572833,
                "items": [{
                    "id": 248524,
                    "units": 2
                },
                {
                    "id": 1414488,
                    "units": 1
                }],
                "coordinates": {
                    "latitude": -33.58672,
                    "longitude": -52.52345
                },
                "payWithPoints": False
                }),
            content_type='application/json'
        )
        assert response._status_code == 200