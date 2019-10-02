from flask import Blueprint, request, jsonify
from src.auth.services.shop_service import ShopService
from src.auth.schemas.schemas import ShopSchema

shops_blueprint = Blueprint('shops', __name__)


@shops_blueprint.route('/shops/<_id>', methods=['GET'])
def get_shop(_id):
    service = ShopService()
    shop = service.get_shop(_id)
    if not shop: 
        return jsonify({'401': "shop with that id doesn't exist."}), 404
    return jsonify({'200': "shop with that id exists."}), 200

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
