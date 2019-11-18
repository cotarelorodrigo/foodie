import unittest
import pytest
from unittest.mock import patch
from flask import jsonify
import json
from src.auth.services import user_service
from src.auth.controllers.baseTest import BaseTest
import jwt

delivery_data = {"name": "Rodrigo","email": "asd@asdtk.com","phone_number": 42223333,"role": "delivery","password": "password","firebase_uid": "ajsjfkasf","picture": "www.photo.com","balance": 0}
delivery2_data = {"name": "PEdro","email": "assad@asdtk.com","phone_number": 42223333,"role": "delivery","password": "password","firebase_uid": "sdaadassa","picture": "www.photo.com","balance": 0}

class DeliveryTestCase(BaseTest):

    def test_get_deliverys_ordered(self):
        from  src.auth.models.user_table import DeliveryUserModel
        user = DeliveryUserModel(delivery_data)
        user.latitude = -34.849859
        user.longitude = -58.386222
        user.save()
        user_d = DeliveryUserModel(delivery2_data)
        user_d.latitude = -34.859575
        user_d.longitude = -58.380182
        user_d.save()
        response = self.client.get(
            '/deliveries?latitude=-34.859138&longitude=-58.387252&cantidad=3',
            data=json.dumps({
                "fullName": "realuser",
                "email": "extra",
                "password": "password"
            }),
            content_type='application/json'
        )

        assert response._status_code == 200
    
    def test_get_deliverys_direc_ordered(self):
        from  src.auth.models.user_table import DeliveryUserModel
        from src.auth.services.delivery_service import DeliveryService
        from src.auth.services.direc_service import DirecService
        user = DeliveryUserModel(delivery_data)
        user.latitude = -34.849859
        user.longitude = -58.386222
        user.save()
        user_d = DeliveryUserModel(delivery2_data)
        user_d.latitude = -34.859575
        user_d.longitude = -58.380182
        user_d.save()
        delivery_service = DeliveryService()
        users = delivery_service.get_available_deliverys()
        assert users[0]["user_id"] == 1
        assert len(users) == 2
        direc_service = DirecService()
        shop = {"latitude": -34.859138, "longitude": -58.387252}
        users = direc_service.get_nearly_deliverys(shop, users)
        #Al ordenarlos el primer usuario tendria que ser el usuario 2
        assert users[0]["user_id"] == 2
