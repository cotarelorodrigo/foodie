class ShopService:

    def get_shop(self, _id):
        from src.app.models.shop_table import ShopModel
        return ShopModel.query.get(_id)

    def get_N_top_shops(self, n_shops):
        from src.app.models.shop_table import ShopModel
        return ShopModel.query.order_by(ShopModel.rating.desc()).limit(n_shops)