from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException

class ShopService:

    def get_shop(self, _id):
        from src.auth.models.shop_table import ShopModel
        try:
            response = ShopModel.query.get(_id).__dict__
        except AttributeError:
            raise NotFoundException("No shop with provided id")
        response.pop("_sa_instance_state")
        return response 

    def get_products(self,shop_id):
        from src.auth.models.product_table import ProductModel
        response = ProductModel.query.filter_by(shopId=shop_id).all()
        if not response:
            return []
        products = [p.__dict__ for p in response]
        for p in products: p.pop("_sa_instance_state")
        return products

    def get_N_top_shops(self, n_shops):
        from src.auth.models.shop_table import ShopModel
        return ShopModel.query.order_by(ShopModel.rating.desc()).limit(n_shops)