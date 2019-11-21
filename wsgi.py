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
  shops = [{"name":"Mc Donalds", "address":"Av. Corrientes 124", "latitude": -34.607711, "longitude": -58.387439, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":4},
  {"name":"Subway", "address":"Sarmiento 440", "latitude": -34.600699, "longitude": -58.392317, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":4},
  {"name":"Mostaza", "address":"Chile 8810", "latitude": -34.601054, "longitude": -58.377459, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":2.8},
  {"name":"El bar de Taller", "address":"Av Paseo Colon 100", "latitude": -34.614830, "longitude": -58.378095, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":1.9},
  {"name":"Lo de Flavio", "address":"Av Independencia 701", "latitude": -34.617232, "longitude": -58.373459, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":3.6},
  {"name":"El lugar", "address":"Moreno 247", "latitude": -34.617136, "longitude": -58.377459, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":4.025},
  {"name":"Parrilla de Moron", "address":"25 de Mayo 116", "latitude": -34.654223, "longitude": -58.635571, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":0.8},
  {"name":"Castelar01", "address":"Leandro N Alem 5581", "latitude": -34.641302, "longitude": -58.645781, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":4.99},
  {"name":"Castelar02", "address":"Machado 719", "latitude": -34.646054, "longitude": -58.631571, "photoUrl":"https://logosmarcas.com/wp-content/uploads/2018/05/McDonalds-Logo.png", "rating":3.2}]
  
  
  products = [{"shop_id": 1,"name": "Hamburguesa normal","description": "Hamburguesa sin queso. Lechuga y tomate opcionales.","price": 75},
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
  },
  {
  "shop_id": 3,
  "name": "Hamburguesa Copmleta",
  "description": "Hamburguesa con queso, jamón, huevo. Lechuga y tomate opcionales",
  "price": 120
  },
  {
  "shop_id": 3,
  "name": "Sandwich de Lomo",
  "description":"Una descripcion bastante larga para ver como queda esta descripcion en la app al mostrar el menú",
  "price": 100
  },
  {
  "shop_id": 3,
  "name": "Porción de papas fritas",
  "description": "Porción mediana de papas fritas.",
  "price": 90.0
  },
  {
  "shop_id": 3,
  "name": "Lo que sea",
  "description": "Cualquier cosa",
  "price": 150
  },
  {
  "shop_id": 4,
  "name": "Hamburguesa con queso",
  "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
  "price": 90
  },
  {
  "shop_id": 4,
  "name": "Sandwich de Lomo",
  "description":"Una descripcion bastante larga para ver como queda esta descripcion en la app al mostrar el menú",
  "price": 100
  },
  {
  "shop_id": 4,
  "name": "Porción de papas fritas",
  "description": "Porción mediana de papas fritas.",
  "price": 90.0
  },
  {
  "shop_id": 5,
  "name": "Lo que sea",
  "description": "Cualquier cosa",
  "price": 150
  },
  {
  "shop_id": 6,
  "name": "Hamburguesa normal",
  "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
  "price": 90
  },
  {
  "shop_id": 6,
  "name": "Hamburguesa con queso",
  "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
  "price": 90
  },
  {
  "shop_id": 6,
  "name": "Hamburguesa Copmleta",
  "description": "Hamburguesa con queso, jamón, huevo. Lechuga y tomate opcionales",
  "price": 120
  },
  {
  "shop_id": 6,
  "name": "Sandwich de Lomo",
  "description":"Una descripcion bastante larga para ver como queda esta descripcion en la app al mostrar el menú",
  "price": 100
  },
  {
  "shop_id": 6,
  "name": "Porción de papas fritas",
  "description": "Porción mediana de papas fritas.",
  "price": 90.0
  },
  {
  "shop_id": 7,
  "name": "Hamburguesa normal",
  "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
  "price": 90
  },
  {
  "shop_id": 7,
  "name": "Hamburguesa con queso",
  "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
  "price": 90
  },
  {
  "shop_id": 7,
  "name": "Hamburguesa Copmleta",
  "description": "Hamburguesa con queso, jamón, huevo. Lechuga y tomate opcionales",
  "price": 120
  },
  {
  "shop_id": 7,
  "name": "Sandwich de Lomo",
  "description":"Una descripcion bastante larga para ver como queda esta descripcion en la app al mostrar el menú",
  "price": 100
  },
  {
  "shop_id": 8,
  "name": "Porción de papas fritas",
  "description": "Porción mediana de papas fritas.",
  "price": 90.0
  },
  {
  "shop_id": 8,
  "name": "Lo que sea",
  "description": "Cualquier cosa",
  "price": 150
  },
  {
  "shop_id": 8,
  "name": "Hamburguesa con queso",
  "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
  "price": 90
  },
  {
  "shop_id": 9,
  "name": "Sandwich de Lomo",
  "description":"Una descripcion bastante larga para ver como queda esta descripcion en la app al mostrar el menú",
  "price": 100
  },
  {
  "shop_id": 9,
  "name": "Porción de papas fritas",
  "description": "Porción mediana de papas fritas.",
  "price": 90.0
  }
  # ,
  # {
  # "shop_id": 10,
  # "name": "Hamburguesa normal",
  # "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
  # "price": 90
  # },
  # {
  # "shop_id": 10,
  # "name": "Hamburguesa con queso",
  # "description": "Hamburguesa con queso. Lechuga y tomate opcionales",
  # "price": 90
  # }
  # {
  # "shop_id": 10,
  # "name": "Hamburguesa Copmleta",
  # "description": "Hamburguesa con queso, jamón, huevo. Lechuga y tomate opcionales",
  # "price": 120
  # },
  # {
  # "shop_id": 10,
  # "name": "Sandwich de Lomo",
  # "description":"Una descripcion bastante larga para ver como queda esta descripcion en la app al mostrar el menú",
  # "price": 100
  # }
  ]

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
  
  normal_user2 = {
    "name" : "Flavio Normal",
    "email" : "normal2@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "2yxGFRvkA3TLg1GMKjYDNzHfu6k1",
    "role": "usuario",
    "phone_number": 135138,
    "suscripcion" : "flat",
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg"
  }
  
  normal_user3 = {
    "name" : "Flavio Normal",
    "email" : "normal3@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "PKCPkcLExuh8ewLbL2dPDuVuKcY2",
    "role": "usuario",
    "phone_number": 135138,
    "suscripcion" : "flat",
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg"
  }

  normal_user4 = {
    "name" : "Flavio Perez",
    "email" : "perezflavio94@gmail.com",
    "firebase_uid" : "z5B7CMytC9YJ11LAcvREY4F5Dvg2",
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

  delivery_user2 = {
    "name" : "Flavio Delivery",
    "email" : "delivery2s@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "U5OMU4hcyJdejlEmJ1Mv73lnAnv2",
    "role":"delivery",
    "phone_number":135138,
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg",
    "balance": 0
  }

  delivery_user3 = {
    "name" : "Flavio Delivery",
    "email" : "delivery3@gmail.com",
    "password" : "taller2",
    "firebase_uid" : "9RmRydK0t1QcuYGSaVgcnAl1ewq1",
    "role":"delivery",
    "phone_number":135138,
    "picture" : "gs://foodie-taller2.appspot.com/images/61FuIoIFkLa55OvAYWODuU5SuPZ2/JPEG_20191112_200117_1526502813.jpg",
    "balance": 0
  }
  
  user_service = UserService()
  user_schema = NormalUserSchema().load(normal_user)
  user_service.create_normal_user(user_schema)
  user_schema = NormalUserSchema().load(normal_user2)
  user_service.create_normal_user(user_schema)
  user_schema = NormalUserSchema().load(normal_user3)
  user_service.create_normal_user(user_schema)
  user_schema = NormalUserSchema().load(normal_user4)
  user_service.create_normal_user(user_schema)


  del_service = DeliveryService()
  del_schema = DeliveryUserSchema().load(delivery_user)
  del_service.create_delivery_user(del_schema)  
  del_schema = DeliveryUserSchema().load(delivery_user2)
  del_service.create_delivery_user(del_schema)  
  del_schema = DeliveryUserSchema().load(delivery_user3)
  del_service.create_delivery_user(del_schema)


  coord1={
    "latitude": -34.601054,
    "longitude": -58.392317
  }
  coord2={
    "latitude": -34.611054,
    "longitude": -58.492317
  }
  coord3={
    "latitude": -34.616054,
    "longitude": -58.652317
  }
  coord4={
    "latitude": -34.606054,
    "longitude": -58.282317
  }
  coord5={
    "latitude": -34.654223,
    "longitude": -58.692317
  }
  coord6={
    "latitude": -34.651054,
    "longitude": -58.402317
  }
  coord7={
    "latitude": -34.611054,
    "longitude": -58.352317
  }

  

  user_service.update_coordinates(1,coord1)
  user_service.update_coordinates(2,coord2)
  user_service.update_coordinates(3,coord3)
  user_service.update_coordinates(4,coord4)
  user_service.update_coordinates(5,coord5)
  user_service.update_coordinates(6,coord6)
  user_service.update_coordinates(7,coord7)

  

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


