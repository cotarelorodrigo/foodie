import os
import pytest
from src.app import create_app, db
from src.config import app_config
from src.auth.models.user_table import UserModel
from src.auth.models.product_table import ProductModel
from src.auth.models.shop_table import ShopModel
from src.auth.models.order_table import OrderModel, OrderProductsModel, OrderOfertsModel
from src.auth.models.admin_table import AdminModel

def set_shops():
	shops = [{"name":"Mc Donalds", "address":"call3 falsa", "latitude": 50.45, "longitude": 100.123, "photoUrl":"wqatgayeesyws", "rating":8},
	 		{"name":"Subway", "address":"call3 falsa", "latitude": 50.45, "longitude": 100.123, "photoUrl":"dsgw", "rating":7.3},
			 {"name":"Mostaza", "address":"call3 falsa", "latitude": 50.45, "longitude": 100.123, "photoUrl":"dsgw", "rating":9}]
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

app = create_app()
with app.app_context():
  db.drop_all()
  db.create_all()
  set_shops()
  set_admin()
  db.session.commit()

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)


