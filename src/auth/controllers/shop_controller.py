from flask import Blueprint, request, jsonify
from src.auth.services.shop_service import ShopService
from src.auth.services.delivery_service import DeliveryService
from src.auth.schemas.schemas import ShopSchema

shops_blueprint = Blueprint('shops', __name__)


@shops_blueprint.route('/shops/<_id>', methods=['GET'])
def get_shop(_id):
    service = ShopService()
    shop = service.get_shop(_id)
    return jsonify(shop)

@shops_blueprint.route('/shops/<_id>/menu', methods=['GET'])
def get_shop_menu(_id):
    service = ShopService()
    shop = service.get_shop(_id)
    products = service.get_products(_id)
    return jsonify(products)

@shops_blueprint.route('/shops/<_id>/deliveryPrice', methods=['GET'])
def get_delivery_price(_id):
    service = ShopService()
    shop = service.get_shop(_id)
    delivery_service = DeliveryService()
    return jsonify(delivery_service.get_delivery_price(None,None,shop,50.44,100.133))

@shops_blueprint.route('/shops/top', methods=['GET'])
def get_top_shops():
    N_TOPS_SHOPS = 3
    service = ShopService()
    shops = service.get_N_top_shops(N_TOPS_SHOPS)
    result = {}
    ranking = 1
    for u in shops:
        result[ranking] = u.name
        ranking += 1
    print(result)
    if not shops:
        return jsonify({'401': "There are not shops"}), 401
    return result, 200
