import unittest
import json
from unittest.mock import patch
from src.app import app
from src.app.services import shop_service

mock_shop = {"id": 12, "name":"Mc Donalds", "photoUrl":"wqatgayeesyws", "rating":0.3}
mock_shops = [{"id": 12, "name":"Mc Donalds", "address":"call3 falsa", "description":"comida rapida", "photoUrl":"wqatgayeesyws", "rating":8},
	 		{"id": 13, "name":"Subway", "address":"call3 falsa", "description":"comida rapida", "photoUrl":"dsgw", "rating":7.3},
			 {"id": 14, "name":"Mostaza", "address":"call3 falsa", "description":"comida rapida", "photoUrl":"dsgw", "rating":9}]

class AuthControllerTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    @patch("src.app.services.shop_service.ShopService.get_shop")
    def test_get_shop_by_id(self, check_id_mock):
        check_id_mock.return_value = mock_shop
        response = self.app.head('/shops/2')
        assert response._status_code == 200
