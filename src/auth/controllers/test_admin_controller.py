import unittest
from unittest.mock import patch
import json
from src.auth.controllers.baseTest import BaseTest
import jwt

class AdminTestCase(BaseTest):

    @patch("jwt.decode")
    def test_admin_statics(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/statistics',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    def test_admin_statics_users(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/statistics/users?year_from=2017&month_from=5&year_to=2017&month_to=9',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    def test_admin_statics_deliveries(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/statistics/deliveries?year_from=2017&month_from=5&year_to=2017&month_to=9',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    def test_admin_statics_orders_completed(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/statistics/orders/completed?year_from=2017&month_from=5&year_to=2017&month_to=9',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    def test_admin_statics_orders_cancellled(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/statistics/orders/completed?year_from=2017&month_from=5&year_to=2017&month_to=9',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200
    
    ###################### SHOPS ######################

    @patch("jwt.decode")
    def test_admin_shops(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/shops?p=0&pSize=2',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    def test_admin_shop_create(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.post(
            '/admin/shop',
            headers={'Authorization':'tokenfalso123'},
            data=json.dumps({
                "name":"Club de la milanesa", 
                "address":"call3 falsa", 
                "coordinates": {"latitude": 50.45, "longitude": 100.123 }, 
                "description": "Resto de milanesas",
                "photoUrl":"wqatgayeesyws", 
                "rating":8
                }),
            content_type='application/json'
        )
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.shop_service.ShopService.get_shop")
    def test_admin_shop_get(self, get_shop, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        get_shop.return_value = True
        response = self.client.get('/admin/shop?id=1',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.shop_service.ShopService.delete_shop")
    def test_admin_shop_delete(self, delete_shop, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        delete_shop.return_value = True
        response = self.client.delete('/admin/shop?id=1',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.shop_service.ShopService.update_shop")
    def test_admin_shop_update(self, update_shop, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        update_shop.return_value = True
        response = self.client.put(
            '/admin/shop?id=1',
            headers={'Authorization':'tokenfalso123'},
            data=json.dumps({
                "name":"Club de la milanesa", 
                "address":"call3 falsa", 
                "coordinates": {"latitude": 48.45, "longitude": 70.123 }, 
                "description": "Resto de milanesas",
                "photoUrl":"wqatgayeesyws", 
                "rating":8844
                }),
            content_type='application/json'
        )
        assert response._status_code == 200


    ###################### DELIVERYS ######################
    @patch("jwt.decode")
    def test_admin_deliveries(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/deliveries?p=0&pSize=2',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    def test_admin_delivery_create(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.post(
            '/admin/delivery',
            headers={'Authorization':'tokenfalso123'},
            data=json.dumps({
                "name": "Rodrigo",
                "email": "asd@asdtk.com",
                "phone_number": 42223333,
                "role": "delivery",
                "password": "password",
                "firebase_uid": "ajsjfkasf",
                "picture": "www.photo.com",
                "balance": 100
            }),
            content_type='application/json'
        )
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.delivery_service.DeliveryService.get_delivery")
    def test_admin_delivery_get(self, get_delivery, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        get_delivery.return_value = True
        response = self.client.get('/admin/delivery?id=1',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.delivery_service.DeliveryService.delete_delivery")
    def test_admin_delivery_delete(self, delete_delivery, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        delete_delivery.return_value = True
        response = self.client.delete('/admin/delivery?id=1',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.delivery_service.DeliveryService.update_delivery")
    def test_admin_delivery_update(self, update_delivery, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        update_delivery.return_value = True
        response = self.client.put(
            '/admin/delivery?id=1',
            headers={'Authorization':'tokenfalso123'},
            data=json.dumps({
                "name": "Rodrigo",
                "email": "asd@asdtk.com",
                "phone_number": 42223333,
                "role": "delivery",
                "password": "password",
                "firebase_uid": "ajsjfkasf",
                "picture": "www.photo.com",
                "balance": 4646648
            }),
            content_type='application/json'
        )
        assert response._status_code == 200

    ###################### USERS ######################
    @patch("jwt.decode")
    def test_admin_users(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/users?p=0&pSize=2',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    def test_admin_user_create(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.post(
            '/admin/user',
            headers={'Authorization':'tokenfalso123'},
            data=json.dumps({
                "name": "Rodrigo",
                "email": "cotarelorodrigo@gmail.com",
                "phone_number": 42223333,
                "role": "usuario",
                "password": "password",
                "firebase_uid": ";iugugu",
                "suscripcion": "flat"
            }),
            content_type='application/json'
        )
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.user_service.UserService.get_normal_user")
    def test_admin_user_get(self, get_normal_user, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        get_normal_user.return_value = True
        response = self.client.get('/admin/user?id=1',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.user_service.UserService.delete_user")
    def test_admin_user_delete(self, delete_user, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        delete_user.return_value = True
        response = self.client.delete('/admin/user?id=1',  headers={'Authorization':'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.user_service.UserService.update_normal_user")
    def test_admin_user_update(self, update_normal_user, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        update_normal_user.return_value = True
        response = self.client.put(
            '/admin/user?id=1',
            headers={'Authorization':'tokenfalso123'},
            data=json.dumps({
                "name": "Rodrigo",
                "email": "cotarelorodrigo@gmail.com",
                "phone_number": 42223333,
                "role": "usuario",
                "password": "password",
                "firebase_uid": ";iugugu",
                "suscripcion": "PREMIUMMMMM"
            }),
            content_type='application/json'
        )
        assert response._status_code == 200

    ###################### ORDERS ######################
    @patch("jwt.decode")
    @patch("src.auth.services.order_service.OrderService.get_N_orders_filtered")
    def test_admin_orders_only_user(self, get_N_orders_filtered, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        get_N_orders_filtered.return_value = True
        response = self.client.get('/admin/orders?user_id=1&p=1&pSize=5', headers={'Authorization': 'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.order_service.OrderService.get_N_orders_filtered")
    def test_admin_orders_only_delivery(self, get_N_orders_filtered, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        get_N_orders_filtered.return_value = True
        response = self.client.get('/admin/orders?delivery_id=5&p=1&pSize=5', headers={'Authorization': 'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.order_service.OrderService.get_N_orders_filtered")
    def test_admin_orders_only_shop(self, get_N_orders_filtered, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        get_N_orders_filtered.return_value = True
        response = self.client.get('/admin/orders?shop_id=5&p=1&pSize=5', headers={'Authorization': 'tokenfalso123'})
        assert response._status_code == 200

    ###################### MENU ######################

    @patch("jwt.decode")
    def test_admin_menu(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.get('/admin/menu?shop_id=1&p=0&pSize=2', headers={'Authorization': 'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    def test_admin_product_create(self, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        response = self.client.post(
            '/admin/product',
            headers={'Authorization': 'tokenfalso123'},
            data=json.dumps({
                "name": "Rodrigo",
                "shop_id": 1,
                "description": "ieieiei",
                "price": 45,

            }),
            content_type='application/json'
        )
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.products_service.ProductService.delete_product")
    def test_admin_product_delete(self, delete_product, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        delete_product.return_value = True
        response = self.client.delete('/admin/product?id=1', headers={'Authorization': 'tokenfalso123'})
        assert response._status_code == 200

    @patch("jwt.decode")
    @patch("src.auth.services.products_service.ProductService.update_product")
    def test_admin_product_update(self, update_product, jwt_decode):
        jwt_decode.return_value = {"is_admin": True}
        update_product.return_value = True
        response = self.client.put(
            '/admin/product?id=1',
            headers={'Authorization': 'tokenfalso123'},
            data=json.dumps({
                "name": "Rodrigo",
                "description": "ieieiei",
                "price": 45,
            }),
            content_type='application/json'
        )
        assert response._status_code == 200