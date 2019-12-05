import unittest
import pytest
from unittest.mock import patch
from flask import jsonify
import json
from src.auth.services import user_service
from src.auth.controllers.baseTest import BaseTest
import jwt

mock_user = {"fullName": "Rodrigo", "email":"asd@asd.com", "password":"asfaga", "signUpDate":"2019-02-15" , "firebaseUid":"DGHAHAEHR", "picture":"garehqerae"}

class UserTestCase(BaseTest):

    def test_wrong_less_fields_new_user(self):
        response = self.client.post(
            '/users',
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
        response = self.client.head('/users/email/asd@asd.com')
        assert response._status_code == 200
    
    @patch("src.auth.services.user_service.UserService.get_user")
    def test_check_nonexisting_id(self, check_id_mock):
        check_id_mock.return_value = False
        response = self.client.head('/users/2')
        assert response._status_code == 404

    def test_set_premium_subscription(self):
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

        self.assertEqual(response._status_code,200)
        response = self.client.put(
            '/users/1/premium_subscription',
            data=json.dumps({
              "number": "5678-9143-0689-4572",
              "security_code": 123
            }),
            content_type='application/json'
        )
        self.assertEqual(response._status_code,200)
        user = self.client.get("/users/1").json
        self.assertEqual(user["suscripcion"],"premium")

    @patch("src.auth.services.user_service.UserService.delete_user")
    def test_delete_existing_id(self, delete_id_mock):
        delete_id_mock.return_value = True
        response = self.client.delete('/users/1')
        assert response._status_code == 200

    @patch("src.auth.services.user_service.UserService.delete_user")
    def test_delete_nonexisting_id(self, delete_id_mock):
        delete_id_mock.return_value = False
        response = self.client.delete('/users/2')
        assert response._status_code == 404

    @patch("jwt.decode")
    def test_user_profile(self, jwt_decode):
        response = self.client.post(
            '/users',
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
        response = self.client.get('/users/profile/asddd@asddd.com', headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    def test_wrong_auth_no_header(self):
        response = self.client.get('/users/profile/asddd@asddd.com')
        assert response._status_code == 421

    def test_wrong_invalid_token(self):
        response = self.client.get('/users/profile/asddd@asddd.com', headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 422

    def test_user_change_state(self):
        from src.auth.services.user_service import UserService
        content_user = {"name":"Rodrigo","email":"asd@asd.com","phone_number":42223333,"role":"usuario","password": "password","firebase_uid": "ajsjfkasf","suscripcion":"flat"}
        user = UserService().create_normal_user(content_user)
        assert user.state == 'free'
        UserService().user_start_working(user.user_id, None)
        assert user.state == 'working'
        UserService().user_finish_working(user.user_id)
        assert user.state == 'free'
    
    def test_user_catch_favour_change_state(self):
        from src.auth.models.order_table import OrderModel
        from src.auth.services.user_service import UserService
        from src.auth.services.order_service import OrderService
        order_service = OrderService()
        user_service = UserService()
        #Creo usuario 1
        content_user = {"name":"Rodrigo","email":"asd@asd.com","phone_number":42223333,"role":"usuario","password": "password","firebase_uid": "ajsjfkasf","suscripcion":"flat"}
        user = user_service.create_normal_user(content_user)
        assert user.state == 'free'
        #Creo usuario 2
        content_user = {"name":"Juan","email":"asd@asde.com","phone_number":42223333,"role":"usuario","password": "password","firebase_uid": "ajsjfkasefef","suscripcion":"flat"}
        user_delivery = user_service.create_normal_user(content_user)
        assert user_delivery.state == 'free'
        #Creo orden
        order_info = {"shop_id": 8572833,"products": [{"product_id": 248524,"units": 2},{"product_id": 1414488,"units": 1}], "latitude": -33.58672,"longitude": -52.52345,
        "payWithPoints": True,"state": 'created', 'user_id':1, "price":200, "favourPoints":20}
        order = OrderModel(order_info)
        order.save()
        offer_info={}
        offer_info["points"] = 20
        #Agarro la orden
        order_service.catch_order(order.order_id, user_delivery.user_id,offer_info)
        assert user.state == 'waiting'
        assert user_delivery.state == 'working'
        #Entro la orden
        order_service.order_delivered(order.order_id)
        assert user.state == 'free'
        assert user_delivery.state == 'free'

    def test_user_catch_order_change_state(self):
        from src.auth.models.order_table import OrderModel
        from src.auth.services.user_service import UserService
        from src.auth.services.delivery_service import DeliveryService
        from src.auth.services.order_service import OrderService
        order_service = OrderService()
        user_service = UserService()
        delivery_service = DeliveryService()
        #Creo usuario normal
        content_user = {"name":"Rodrigo","email":"asd@asd.com","phone_number":42223333,"role":"usuario","password": "password","firebase_uid": "ajsjfkasf","suscripcion":"flat"}
        user = user_service.create_normal_user(content_user)
        assert user.state == 'free'
        #Creo usuario delivery
        content_user =  {"name": "JUan","email": "asd@adaasd.com","phone_number": 42223333,"role": "usuario","password": "password", "firebase_uid": "ajsjadasfkasf","picture": "www.photo.com","balance": 100}
        user_delivery = delivery_service.create_delivery_user(content_user)
        assert user_delivery.state == 'free'
        #Creo orden
        order_info = {"shop_id": 8572833,"products": [{"product_id": 248524,"units": 2},{"product_id": 1414488,"units": 1}], "latitude": -33.58672,"longitude": -52.52345,
        "payWithPoints": False,"state": 'created', 'user_id':1, "price":200}
        order = OrderModel(order_info)
        order.save()
        #Agarro la orden
        offer_info={}
        offer_info["delivery_price"] = 200
        offer_info["delivery_pay"] = 100
        order_service.catch_order(order.order_id, user_delivery.user_id,offer_info)
        assert user.state == 'waiting'
        assert user_delivery.state == 'working'
        #Entro la orden
        order_service.order_delivered(order.order_id)
        assert user.state == 'free'
        assert user_delivery.state == 'free'

    def test_update_user_coordinates(self):
        from src.auth.services.user_service import UserService
        user_service = UserService()
        #Creo usuario normal
        content_user = {"name":"Rodrigo","email":"asd@asd.com","phone_number":42223333,"role":"usuario","password": "password","firebase_uid": "ajsjfkasf","suscripcion":"flat"}
        user = user_service.create_normal_user(content_user)
        assert user.latitude == None
        assert user.longitude == None
        coordinates = {"latitude": 20.00, "longitude": 14.5}
        user_service.update_coordinates(user.user_id, coordinates)
        assert user.latitude == 20.00
        assert user.longitude == 14.5