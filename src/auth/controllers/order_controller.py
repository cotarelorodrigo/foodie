from flask import Blueprint, request, jsonify
from src.auth.services.order_service import OrderService
from src.auth.schemas.schemas import OrderSchema

orders_blueprint = Blueprint('orders', __name__)
order_schema = OrderSchema()

@orders_blueprint.route('/orders', methods=['POST'])
def add_order():
    content = request.get_json()
    order_data = order_schema.load(content)
    
    service = OrderService()
  
    try:
        for product in order_data['items']:
            order = {
                    "shop_id": order_data['shopId'],
                    "item": product['id'],
                    "cantidad": product['units'],
                    "latitud": order_data['coordinates']['latitude'],
                    "longitud": order_data['coordinates']['longitude'],
                    "payWithPoints": order_data['payWithPoints']
                    }
            service.create_order(order)
    except:
        raise
    else:
        return jsonify({'200': 'The order was created without problems'})

@orders_blueprint.route('/showorders', methods=['GET'])
def show_orders():
    service = OrderService()
    orders = service.get_orders()
    return jsonify(orders)

@orders_blueprint.route('/orders/cancel/<_id>', methods=['DELETE'])
def cancel_order(_id):
    service = OrderService()
    shop = service.delete_order(_id)
    if not shop: 
        return jsonify({'404': "order with that id doesn't exist."}), 404
    return jsonify({'200': "order with that id was deleted."}), 200