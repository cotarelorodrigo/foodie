import unittest
from unittest.mock import patch
import json
from src.auth.controllers.baseTest import BaseTest

class AuthControllerTestCase(BaseTest):

    def test_aacancel_order(self):
        response = self.client.post(
            '/orders',
            data=json.dumps({
                "shop_id": 8572833,
                "products": [{
                    "product_id": 248524,
                    "units": 2
                },
                {
                    "product_id": 1414488,
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
        
        response = self.client.delete(
            '/orders/cancel/1'
        )

        assert response._status_code == 200

    def test_add_order(self):
        response = self.client.post(
            '/orders',
            data=json.dumps({
                "shop_id": 8572833,
                "products": [{
                    "product_id": 248524,
                    "units": 2
                },
                {
                    "product_id": 1414488,
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