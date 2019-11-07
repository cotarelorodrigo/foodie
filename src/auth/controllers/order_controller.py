from flask import Blueprint, request, jsonify
from src.auth.services.order_service import OrderService
from src.auth.schemas.schemas import OrderSchema
import sqlalchemy
import marshmallow 

orders_blueprint = Blueprint('orders', __name__)
order_schema = OrderSchema()

@orders_blueprint.route('/orders', methods=['POST'])
def add_order():
    content = request.get_json()
    service = OrderService()
    try:
        service.create_order(content)
    except marshmallow.exceptions.ValidationError as e:
        return jsonify({'400': 'Missing order information: {}'.format(e)}), 400
    except sqlalchemy.exc.IntegrityError:
        return jsonify({'430': 'User_id not registered'}), 430
    except:
        raise
    else:
        return jsonify({'200': 'The order was created without problems'}), 200

@orders_blueprint.route('/showorders', methods=['GET'])
def show_orders():
    service = OrderService()
    orders = service.get_orders()
    return jsonify(orders)

@orders_blueprint.route('/showproductorders', methods=['GET'])
def show_products_orders():
    service = OrderService()
    orders = service.get_products_orders()
    return jsonify(orders)

@orders_blueprint.route('/orders/cancel/<_id>', methods=['DELETE'])
def cancel_order(_id):
    service = OrderService()
    shop = service.delete_order(_id)
    if not shop: 
        return jsonify({'404': "order with that id doesn't exist."}), 404
    return jsonify({'200': "order with that id was deleted."}), 200