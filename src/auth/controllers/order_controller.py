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
        order = service.create_order(content)
    except marshmallow.exceptions.ValidationError as e:
        return jsonify({'msg': 'Missing order information: {}'.format(e)}), 400
    except sqlalchemy.exc.IntegrityError:
        return jsonify({'msg': 'User_id not registered'}), 430
    except:
        raise
    else:
        return jsonify({'order_id': order.order_id}), 200

@orders_blueprint.route('/orders', methods=['GET'])
def show_orders():
    service = OrderService()
    orders = service.get_orders()
    return jsonify(orders)

@orders_blueprint.route('/orders/<_id>',methods=['GET'])
def get_order_by_id(_id):
    service = OrderService()
    order = service.get_order_by_id(_id)
    return jsonify(order), 200

@orders_blueprint.route('/showproductorders', methods=['GET'])
def show_products_orders():
    service = OrderService()
    orders = service.get_products_orders()
    return jsonify(orders)

@orders_blueprint.route('/orders/cancel/<_id>', methods=['DELETE'])
def cancel_order(_id):
    service = OrderService()
    order = service.change_order_state(_id, 'cancelled')
    if not order: 
        return jsonify({'msg': "order with that id doesn't exist."}), 404
    return jsonify({'msg': "order with that id was cancelled."}), 200