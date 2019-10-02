import os
from src.app import app, db
from src.auth.models.user_table import UserModel
from src.auth.models.shop_table import ShopModel

def set_shops():
	shops = [{"id": 12, "name":"Mc Donalds", "address":"call3 falsa", "description":"comida rapida", "photoUrl":"wqatgayeesyws", "rating":8},
	 		{"id": 13, "name":"Subway", "address":"call3 falsa", "description":"comida rapida", "photoUrl":"dsgw", "rating":7.3},
			 {"id": 14, "name":"Mostaza", "address":"call3 falsa", "description":"comida rapida", "photoUrl":"dsgw", "rating":9}]
	for shop_data in shops:
		shop = ShopModel(shop_data)
		shop.save()

db.drop_all()
db.create_all()
set_shops()
db.session.commit()



if __name__ == "__main__":
	port = int(os.environ.get('PORT', 5000))
	app.run(host='0.0.0.0', port=port)


