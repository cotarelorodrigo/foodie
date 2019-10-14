import os
from src.app import app, db
from src.auth.models.user_table import UserModel
from src.auth.models.product_table import ProductModel
from src.auth.models.shop_table import ShopModel

def set_shops():
	shops = [{"id": 12, "name":"Mc Donalds", "address":"call3 falsa", "latitude": 50.45, "longitude": 100.123, "photoUrl":"wqatgayeesyws", "rating":8},
	 		{"id": 13, "name":"Subway", "address":"call3 falsa", "latitude": 50.45, "longitude": 100.123, "photoUrl":"dsgw", "rating":7.3},
			 {"id": 14, "name":"Mostaza", "address":"call3 falsa", "latitude": 50.45, "longitude": 100.123, "photoUrl":"dsgw", "rating":9}]
	products = [{
      "shopId": 12,
      "id": 51985,
      "name": "Hamburguesa normal",
      "description": "Hamburguesa sin queso. Lechuga y tomate opcionales.",
      "price": 75
    },
    {
      "shopId": 12,
      "id": 40815,
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

db.drop_all()
db.create_all()
set_shops()
db.session.commit()

if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)


