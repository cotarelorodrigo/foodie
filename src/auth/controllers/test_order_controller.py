import unittest
from unittest.mock import patch
from src.auth.auth_exception import NotFoundException
import json
from src.auth.controllers.baseTest import BaseTest

user_data = {"name": "Rodrigo","email": "asd@asd.com","phone_number": 42223333,"role": "usuario","password": "password","firebase_uid": "rjrr","suscripcion": "flat"}
user2_data = {"name": "JUan","email": "asfgd@asd.com","phone_number": 42223333,"role": "usuario","password": "password","firebase_uid": "argare","suscripcion": "flat"}
delivery_data = {"name": "Rodrigo","email": "asd@asdtk.com","phone_number": 42223333,"role": "delivery","password": "password","firebase_uid": "ajsjfkasf","picture": "www.photo.com","balance": 100}
order_data = {"shop_id": 125,"products": [{"product_id": 3333,"units": 14},{"product_id": 444,"units": 15}],"coordinates": {"latitude": -33.58672,"longitude": -52.52345},
"payWithPoints": True,"favourPoints": 40,"user_id": 1,"state": "created","price": 145}
order_ofert_data = {"order_id": 1, "delivery_id": 2, "delivery_pay": 0, 'delivery_price': 0}
favour_offer_data={"order_id":1,"user_id":2,"points":20}


class OrderTestCase(BaseTest):

    @patch("src.auth.services.order_service.OrderService.set_order_price")
    def test_add_order(self, set_order_price):
        set_order_price.return_value = True
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

    @patch("src.auth.services.order_service.OrderService.set_order_price")
    def test_cancel_order(self, set_order_price):
        set_order_price.return_value = True
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

    def test_create_favour_order_without_points(self):
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
        
        order_response = self.client.post(
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
                #"favourPoints": 40,
                "user_id": 1,
                "state": "created",
                "price": 145
                }),
            content_type='application/json'
        )
        response = self.client.post('users/2/favour_offers',
            data=json.dumps({
                'order_id':1,
                'user_id':2,
                'points': 1000
                }),
            content_type='application/json'
        )
        assert response._status_code == 408

    @patch("src.auth.services.order_service.OrderService.set_order_price")
    def test_delivery_cant_accept_favours(self, set_order_price):
        from  src.auth.models.user_table import NormalUserModel
        from src.auth.models.user_table import DeliveryUserModel
        from src.auth.services.order_service import OrderService
        from src.auth.services.order_ofert_service import OrderOfferService
        from src.auth.auth_exception import NotFoundException

        set_order_price.return_value = True
        CANTIDAD_FAVOUR_POINTS = 20
        user = NormalUserModel(user_data)
        user.save()
        delivery = DeliveryUserModel(delivery_data)
        delivery.save()
        order_service = OrderService()
        order_data["user_id"] = user.user_id
        order_data["payWithPoints"] = True
        order_data["favourPoints"] = CANTIDAD_FAVOUR_POINTS
        order = order_service.create_order(order_data)
        assert order.state == 'created'
        order_ofert_service = OrderOfferService()
        order_ofert = order_ofert_service.create_order_ofert(order_ofert_data)
        with self.assertRaisesRegex(NotFoundException, "ID invalido: Solo los usuarios comunes pueden aceptar favores"):
            order_ofert_service.update_offer_state(delivery.user_id, order.order_id, 'accepted')


    @patch("src.auth.services.order_service.OrderService.set_order_price")
    def test_complete_order_gain_favour_points(self, set_order_price):
        from  src.auth.models.user_table import NormalUserModel
        from src.auth.models.user_table import DeliveryUserModel
        from src.auth.services.order_service import OrderService
        from src.auth.services.order_ofert_service import OrderOfferService
        from src.auth.auth_exception import NotFoundException

        set_order_price.return_value = True
        CANTIDAD_FAVOUR_POINTS = 20
        user = NormalUserModel(user_data)
        user.save()
        user_old_favour_points = user.favourPoints
        user_d = NormalUserModel(user2_data)
        user_d.save()
        user_d_old_favour_points = user.favourPoints
        order_service = OrderService()
        order_data["user_id"] = user.user_id
        order_data["payWithPoints"] = True
        order_data["favourPoints"] = CANTIDAD_FAVOUR_POINTS
        order = order_service.create_order(order_data)
        assert order.state == 'created'
        order_ofert_service = OrderOfferService()
        order_ofert_id = order_ofert_service.create_favour_offer(favour_offer_data)
        order_ofert_service.update_favour_offer_state(user_d.user_id, order_ofert_id, 'accepted')
        assert order.state == 'onWay'
        #Orden entregada
        order_service.order_delivered(order.order_id)
        assert user.favourPoints == user_old_favour_points - CANTIDAD_FAVOUR_POINTS
        assert user_d.favourPoints == user_d_old_favour_points + CANTIDAD_FAVOUR_POINTS

    def test_get_users_work_favours_ordered(self):
        from src.auth.models.user_table import NormalUserModel
        from src.auth.services.user_service import UserService
        from src.auth.services.direc_service import DirecService
        user = NormalUserModel(user_data)
        user.latitude = -34.849859
        user.longitude = -58.386222
        user.save()
        user_d = NormalUserModel(user2_data)
        user_d.latitude = -34.859575
        user_d.longitude = -58.380182
        user_d.save()
        user_service = UserService()
        users = user_service.get_available_users_favours()
        assert users[0]["user_id"] == 1
        assert len(users) == 2
        direc_service = DirecService()
        shop = {"latitude": -34.859138, "longitude": -58.387252}
        users = direc_service.get_nearly_deliverys(shop, users)
        #Al ordenarlos el primer usuario tendria que ser el usuario 2
        assert users[0]["user_id"] == 2

    def test_order_with_invalid_products(self):
        from src.auth.services.order_service import OrderService
        from src.auth.models.order_table import OrderProductsModel
        from src.auth.models.product_table import ProductModel
        order_service = OrderService()
        with self.assertRaisesRegex(NotFoundException, "El producto que quiere agregar no existe"):
            order = order_service.create_order(order_data)

    def test_order_with_discount(self):
        from src.auth.services.order_service import OrderService
        from src.auth.models.product_table import ProductModel
        #Agrego dos productos
        p1 = ProductModel({"shop_id": 1,"name": "Hamburguesa con queso","description": "Hamburguesa con queso. Lechuga y tomate opcionales","price": 120})
        p2 = ProductModel({"shop_id": 2,"name": "Hamburguesa normal","description": "Hamburguesa con queso. Lechuga y tomate opcionales","price": 90})
        p1.save()
        p2.save()
        #Los sumo a la orden
        order_data["products"] = [{"product_id": p1.product_id,"units": 2},{"product_id": p2.product_id,"units": 1}]
        order_data["discount"] = True
        order_service = OrderService()
        order = order_service.create_order(order_data)
        price_with_discount = (order_data["products"][0]["units"] * p1.price) + (order_data["products"][1]["units"] * p2.price)
        price_with_discount = price_with_discount - (0.2*price_with_discount)
        assert price_with_discount == order.price

    def test_order_wit_discount_subtract_user_favour_pounts(self):
        from src.auth.models.user_table import NormalUserModel, DeliveryUserModel
        from src.auth.services.order_service import OrderService
        from src.auth.models.product_table import ProductModel
        #Agrego dos productos
        p1 = ProductModel({"shop_id": 1,"name": "Hamburguesa con queso","description": "Hamburguesa con queso. Lechuga y tomate opcionales","price": 120})
        p2 = ProductModel({"shop_id": 2,"name": "Hamburguesa normal","description": "Hamburguesa con queso. Lechuga y tomate opcionales","price": 90})
        p1.save()
        p2.save()
        #Creo el user y el delivery
        user = NormalUserModel(user_data)
        user.save()
        delivery = DeliveryUserModel(delivery_data)
        delivery.save()
        #Los sumo a la orden
        order_data_test = order_data
        order_data_test["products"] = [{"product_id": p1.product_id,"units": 2},{"product_id": p2.product_id,"units": 1}]
        order_data_test["discount"] = True
        order_data_test["user_id"] = user.user_id
        order_data_test["delivery_id"] = delivery.user_id
        order_service = OrderService()
        order = order_service.create_order(order_data_test)
        order_service.order_delivered(order.order_id)
        assert order.state == 'delivered'
        






