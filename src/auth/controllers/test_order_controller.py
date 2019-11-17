import unittest
from unittest.mock import patch
import json
from src.auth.controllers.baseTest import BaseTest

class OrderTestCase(BaseTest):

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
                "payWithPoints": False,
                "state": 'created',
                'price':0.0,
                "user_id": 8541
                }),
            content_type='application/json'
        )
        assert response._status_code == 200

    def test_cancel_order(self):
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
                "payWithPoints": False,
                'price':0.0,
                "state": 'created',
                "user_id": 8541
                }),
            content_type='application/json'
        )
        assert response._status_code == 200
        
        response = self.client.delete(
            '/orders/cancel/1'
        )

        assert response._status_code == 200


    def test_invalid_add_order(self):
        response = self.client.post(
            '/orders',
            data=json.dumps({
                "shop_id": 8572833,
                "products": [{
                    "product": 248524,
                    "units": 2
                },
                {
                    "product": 1414488,
                    "units": 1
                }],
                "payWithPoints": False
                }),
            content_type='application/json'
        )
        
        assert response._status_code == 400

    @patch('src.auth.services.user_service.UserService.user_order_by_favour')
    def test_create_favour_order_without_points(self, user_order_by_favour):
        user_order_by_favour.return_value = False
        response = self.client.post(
            '/users',
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
        response = self.client.post(
            '/orders',
            data=json.dumps({
                "shop_id": 125,
                "products": [{
                    "product_id": 3333,
                    "units": 14
                },
                {
                    "product_id": 444,
                    "units": 15
                }],
                "coordinates": {
                    "latitude": -33.58672,
                    "longitude": -52.52345
                },
                "payWithPoints": True,
                "favourPoints": 40,
                "user_id": 1,
                "state": "created",
                "price": 145
                }),
            content_type='application/json'
        )
        
        assert response._status_code == 200