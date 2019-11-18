import os
import pytest
from src.app import create_app, db
from src.config import app_config
from src.auth.models.user_table import UserModel
from src.auth.models.product_table import ProductModel
from src.auth.models.shop_table import ShopModel
from src.auth.models.order_table import OrderModel, OrderProductsModel, OrderOffersModel
from src.auth.models.admin_table import AdminModel
from src.auth.schemas.schemas import NormalUserSchema, DeliveryUserSchema
from src.auth.services.user_service import UserService
from src.auth.services.delivery_service import DeliveryService

def set_shops():
	shops = [{"name":"Mc Donalds", "address":"call3 falsa", "latitude": -34.753899, "longitude": -58.657026, "photoUrl":"wqatgayeesyws", "rating":4},
	 		{"name":"Subway", "address":"call3 falsa", "latitude": -34.7832, "longitude": -58.6576, "photoUrl":"dsgw", "rating":4},
			 {"name":"Mostaza", "address":"call3 falsa", "latitude": -34.8444, "longitude": -58.6560, "photoUrl":"dsgw", "rating":3}]
	products = [{
      "shop_id": 1,
      "name": "Hamburguesa normal",
      "description": "Hamburguesa sin queso. Lechuga y tomate opcionales.",
      "price": 75
    },
    {
      "shop_id": 1,
      "name": "Hamburguesa con queso",
      "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
      "price": 90
    },
    {
      "shop_id": 2,
      "name": "Hamburguesa normal",
      "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
      "price": 90
    },
    {
      "shop_id": 2,
      "name": "Hamburguesa con queso",
      "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
      "price": 90
    },
    {
      "shop_id": 3,
      "name": "Hamburguesa normal",
      "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
      "price": 90
    },
    {
      "shop_id": 3,
      "name": "Hamburguesa con queso",
      "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
      "price": 90
    }]



	for shop_data in shops:
		shop = ShopModel(shop_data)
		shop.save()
	for product_data in products:
		product = ProductModel(product_data)
		product.save()
  

def set_admin():
  admin = {"email": "admin@foodie.com", "password": "admin"}
  admin = AdminModel(admin)
  admin.save()

def set_users():
  normal_user = {
    "name" : "Flavio Normal",
    "email" : "normal@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "SJElQiZPrMMHGRzjrBuScvLW8Cc2",
    "role": "usuario",
    "phone_number": 135138,
    "suscripcion" : "flat",
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg"
  }

  delivery_user = {
    "name" : "Flavio Delivery",
    "email" : "delivery@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "05FvThkGGaaDu4PW1qFde3obrjQ2",
    "role":"delivery",
    "phone_number":135138,
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg",
    "balance": 0
  }

  delivery_user_2 = {
    "name" : "Flavio Delivery",
    "email" : "delivery2s@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "05FvThkGGaaDu4PW1qFde3obrjQ2",
    "role":"delivery",
    "phone_number":135138,
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg",
    "balance": 0
  }

    delivery_user_3 = {
    "name" : "Flavio Delivery",
    "email" : "delivery3@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "05FvThkGGaaDu4PW1qFde3obrjQ2",
    "role":"delivery",
    "phone_number":135138,
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg",
    "balance": 0
  }

  delivery_user_4 = {
    "name" : "Flavio Delivery",
    "email" : "delivery4@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "05FvThkGGaaDu4PW1qFde3obrjQ2",
    "role":"delivery",
    "phone_number":135138,
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg",
    "balance": 0
  }



  
  user_service = UserService()
  user_schema = NormalUserSchema().load(normal_user)
  user_service.create_normal_user(user_schema)

  user_service.update_coordinates()

  del_service = DeliveryService()
  del_schema = DeliveryUserSchema().load(delivery_user)
  del_service.create_delivery_user(del_schema)

  

app = create_app()
with app.app_context():
  db.drop_all()
  db.create_all()
  set_shops()
  set_admin()
  set_users()
  db.session.commit()

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)


