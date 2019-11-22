from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service

class ShopService(Service):

    def create_shop(self, shop_data):
        from src.auth.models.shop_table import ShopModel
        from src.auth.schemas.schemas import ShopSchema
        shop_data, products = ShopSchema().load(shop_data)
        shop = ShopModel(shop_data)
        return shop.save()

    def get_shop(self, _id):
        from src.auth.models.shop_table import ShopModel
        response = ShopModel.get_shop(_id)
        return self.sqlachemy_to_dict(response)
    
    def delete_shop(self, _id):
        from src.auth.models.shop_table import ShopModel
        return ShopModel.get_shop(_id).delete()
    
    def update_shop(self, _id, data):
        from src.auth.models.shop_table import ShopModel
        from src.auth.schemas.schemas import ShopSchema
        shop_data, products = ShopSchema().load(data)
        return ShopModel.get_shop(_id).update(shop_data)
        
    def get_products(self,shop_id):
        from src.auth.models.product_table import ProductModel
        response = ProductModel.query.filter_by(shop_id=shop_id).all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)

    def get_N_top_shops(self, n_shops):
        from src.auth.models.shop_table import ShopModel
        query = ShopModel.query.order_by(ShopModel.rating.desc()).limit(n_shops)
        response = {}
        response['items'] = self.sqlachemy_to_dict(query.all())
        return response

    def get_N_shops(self, pageNumber, pageSize):
        from src.auth.models.shop_table import ShopModel
        query = ShopModel.query.offset(pageNumber*pageSize).limit(pageSize)
        response = {}
        response['items'] = self.sqlachemy_to_dict(query.all())
        response['totalItems'] = query.count()
        return response

    def add_review(self,id,review):
        from src.auth.models.shop_table import ShopModel
        shop = ShopModel.get_shop(id)
        old_rating = shop.rating
        reviews = shop.reviews
        new_rating = (reviews * old_rating + review) / (reviews + 1.0)
        shop.reviews = (reviews + 1)
        shop.rating = new_rating
        shop.save()