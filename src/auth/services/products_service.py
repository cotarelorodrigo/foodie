from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service

class ProductService(Service):

    def create_product(self, data):
        from src.auth.models.product_table import ProductModel
        from src.auth.schemas.schemas import ProductSchema
        product = ProductModel(data)
        return product.save()

    def get_product_by_id(self, _id):
        from src.auth.models.product_table import ProductModel
        product = ProductModel.query.get(_id)
        return self.sqlachemy_to_dict(product)

    def update_product(self, _id, data):
        from src.auth.models.product_table import ProductModel
        from src.auth.schemas.schemas import ProductSchema
        product_data = ProductSchema().load(data)
        return ProductModel.get_product(_id).update(product_data)

    def delete_product(self, _id):
        from src.auth.models.product_table import ProductModel
        return ProductModel.get_product(_id).delete()

    def get_N_products(self, shop_id, pageNumber, pageSize):
        from src.auth.models.product_table import ProductModel
        response = ProductModel.query.filter_by(shop_id=shop_id).offset(pageNumber*pageSize).limit(pageSize)
        if not response:
            return []
        return self.sqlachemy_to_dict(response)
