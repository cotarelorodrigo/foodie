from flask import Blueprint, request, jsonify
from src.auth.services.shop_service import ShopService
from src.auth.services.delivery_service import DeliveryService
from src.auth.schemas.schemas import ShopSchema
from src.auth.auth_exception import InvalidQueryParameters
import json

shops_blueprint = Blueprint('shops', __name__)


@shops_blueprint.route('/shops/<_id>', methods=['GET'])
def get_shop(_id):
    service = ShopService()
    shop = service.get_shop(_id)
    return jsonify(shop)

@shops_blueprint.route('/shops', methods=['GET'])
def shops():
    pageNumber = request.args.get('p')
    pageSize = request.args.get('pSize')
    if (pageNumber is None) | (pageSize is None):
        raise InvalidQueryParameters("Invalid query values")
    result = ShopService().get_N_shops(int(pageNumber), int(pageSize))
    return jsonify(result["items"]), 200

@shops_blueprint.route('/shops/<_id>/menu', methods=['GET'])
def get_shop_menu(_id):
    service = ShopService()
    shop = service.get_shop(_id)
    products = service.get_products(_id)
    return jsonify(products)

@shops_blueprint.route('/shops/<_id>/deliveryPrice', methods=['GET'])
def get_delivery_price(_id):
    user_id = request.args.get('user_id')
    delivery_id = request.args.get('delivery_id')
    client_lat = request.args.get('latitude')
    client_long = request.args.get('longitude')
    if (user_id is None) | (delivery_id is None) | (client_lat is None) | (client_long is None):
        raise InvalidQueryParameters("Invalid query values")
    service = ShopService()
    shop = service.get_shop(_id)
    delivery_service = DeliveryService()
    price, pay = delivery_service.get_delivery_price_and_pay(user_id,delivery_id,shop,client_lat,client_long)
    return jsonify({
            'price': price,
            'pay': pay
        })

@shops_blueprint.route('/shops/top', methods=['GET'])
def get_top_shops():
    N_TOPS_SHOPS = 3
    service = ShopService()
    result = service.get_N_top_shops(N_TOPS_SHOPS)
    return jsonify(result), 200

@shops_blueprint.route('/shops/<_id>', methods=['GET'])
def get_shop_by_id():
    service = ShopService()
    result = service.get_shop(_id)
    return jsonify(result), 200
