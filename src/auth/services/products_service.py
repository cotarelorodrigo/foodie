from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service

class ShopService(Service):

    def get_product_by_id(self,id):
        from src.auth.models.product_table import ProductModel
        product = ProductModel.query.get(id)
        return self.sqlachemy_to_dict(product)
