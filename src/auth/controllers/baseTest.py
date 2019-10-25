import unittest
from src.app import create_app, db
from src.config import app_config
from src.auth.models.user_table import NormalUserModel, DeliveryUserModel, UserModel
from src.auth.models.product_table import ProductModel
from src.auth.models.shop_table import ShopModel
from src.auth.models.order_table import OrderModel
from src.auth.models.order_product_table import OrderProductsModel

class BaseTest(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.config.from_object(app_config['testing'])
        ctx = app.app_context()
        ctx.push()  
        db.create_all()
        self.client = app.test_client()

    def tearDown(self):
        pass
        #db.drop_all()