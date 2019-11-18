from flask import Blueprint, request, jsonify
from src.auth.services.products_service import ProductService
from src.auth.services.delivery_service import DeliveryService
from src.auth.schemas.schemas import ShopSchema
from src.auth.auth_exception import InvalidQueryParameters
import json

products_blueprint = Blueprint('products', __name__)

@products_blueprint.route('/products/<_id>', methods=['GET'])
def get_product(_id):
    service = ProductService()
    product = service.get_product(_id)
    return jsonify(product)

