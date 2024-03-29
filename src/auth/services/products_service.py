from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service
import random
import json

class ProductService(Service):

    def create_product(self, data):
        from src.auth.models.product_table import ProductModel
        from src.auth.schemas.schemas import ProductSchema
        product = ProductModel(data)
        return product.save()

    def get_product(self, _id):
        from src.auth.models.product_table import ProductModel
        product = ProductModel.query.get(_id)
        return self.sqlachemy_to_dict(product)

    def get_product_by_id(self, _id):
        from src.auth.models.product_table import ProductModel
        product = ProductModel.query.get(_id)
        return self.sqlachemy_to_dict(product)

    def update_product(self, _id, data):
        from src.auth.models.product_table import ProductModel
        from src.auth.schemas.schemas import ProductSchema
        return ProductModel.get_product(_id).update(data)

    def delete_product(self, _id):
        from src.auth.models.product_table import ProductModel
        return ProductModel.get_product(_id).delete()

    def get_N_products(self, shop_id, pageNumber, pageSize):
        from src.auth.models.product_table import ProductModel
        result = ProductModel.query.filter_by(shop_id=shop_id).offset(pageNumber * pageSize).limit(pageSize)
        response = {}
        response['items'] = self.sqlachemy_to_dict(result.all())
        response['totalItems'] = ProductModel.query.filter_by(shop_id=shop_id).count()
        return response

    def get_sample_products(self, quantity):
        filename = 'src/auth/services/default_products.json'
        try:
            with open(filename, 'r') as f:
                datastore = json.load(f)
                products = random.sample(datastore["products"], quantity)
        except:
            raise NotFoundException("Error con el archivo '{}'".format(filename))
        else:
            return products
