from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service

class ShopService(Service):

    def create_shop(self, shop_data):
        from src.auth.models.shop_table import ShopModel
        from src.auth.schemas.schemas import ShopSchema
        shop_data = ShopSchema().load(shop_data)
        shop = ShopModel(shop_data)
        shop.save()

    def get_shop(self, _id):
        from src.auth.models.shop_table import ShopModel
        try:
            response = ShopModel.query.get(_id)
        except AttributeError:
            raise NotFoundException("No shop with provided id")
        return self.sqlachemy_to_dict(response)
    
    def delete_shop(self, _id):
        from src.auth.models.shop_table import ShopModel
        response = ShopModel.query.filter_by(shop_id=_id).delete()
        return response


    def get_products(self,shop_id):
        from src.auth.models.product_table import ProductModel
        response = ProductModel.query.filter_by(shopId=shop_id).all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)

    def get_N_top_shops(self, n_shops):
        from src.auth.models.shop_table import ShopModel
        return ShopModel.query.order_by(ShopModel.rating.desc()).limit(n_shops)

    def get_N_shops(self, pageNumber, pageSize):
        from src.auth.models.shop_table import ShopModel
        query = ShopModel.query.offset(pageNumber*pageSize).limit(pageSize)
        response = {}
        response['items'] = self.sqlachemy_to_dict(query.all())
        response['totalItems'] = query.count()
        return response