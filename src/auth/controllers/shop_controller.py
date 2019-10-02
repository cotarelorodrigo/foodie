from flask import Blueprint, request, jsonify
from src.auth.services.shop_service import ShopService
from src.auth.schemas.schemas import ShopSchema

shops_blueprint = Blueprint('shops', __name__)


@shops_blueprint.route('/shop/<int(min=1, max=300):id>', methods=['GET'])
def get_shop(id):
    service = ShopService()
    shop = service.get_shop(id)
    if not shop: 
        return jsonify({'401': "shop with that id doesn't exist."}), 404
    return jsonify({'200': "shop with that id exists."}), 200