class ShopService:

    def get_shop(self,_id):
        from src.auth.models.shop_table import ShopModel
        return UserModel.query.get(_id)