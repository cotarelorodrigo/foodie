from flask import Blueprint, request, jsonify
from src.auth.services.order_service import OrderService
from src.auth.schemas.schemas import OrderSchema
from src.auth.services.service import Service
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
    from src.auth.models.order_table import OrderModel
    orders = OrderModel.query
    user_id = request.args.get("user_id")
    if not user_id is None:
        orders = orders.filter_by(user_id=user_id)
    delivery_id = request.args.get("delivery_id")
    if not delivery_id is None:
        orders = orders.filter_by(delivery_id=delivery_id)
    state = request.args.get("state")
    if not state is None:
        orders = orders.filter_by(state=state)

    orders = Service().sqlachemy_to_dict(orders.all())

    return jsonify(orders)

@orders_blueprint.route('/orders/<_id>/items', methods=['GET'])
def get_order_items(_id):
    service = OrderService()
    items = service.get_order_items(_id)
    return jsonify(items)


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

@orders_blueprint.route('/orders/<_id>/shop_review', methods=['POST'])
def post_shop_review(_id):
    service = OrderService()
    content = request.get_json()
    try:
        review = content["review"]
        service.review_shop(_id,review)
    except KeyError:
        return jsonify({"msg": "Falta el campo review en el request"}), 412
    else:
        return jsonify({"msg":"calificacion procesada sin problemas"}), 200

@orders_blueprint.route('/orders/<_id>/delivery_review', methods=['POST'])
def post_delivery_review(_id):
    service = OrderService()
    content = request.get_json()
    try:
        review = content["review"]
        service.review_delivery(_id,review)
    except KeyError:
        return jsonify({"msg": "Falta el campo review en el request"}), 412
    else:
        return jsonify({"msg":"calificacion procesada sin problemas"}), 200


@orders_blueprint.route('/orders/cancel/<_id>', methods=['DELETE'])
def cancel_order(_id):
    service = OrderService()
    order = service.change_order_state(_id, 'cancelled')
    if not order: 
        return jsonify({'msg': "order with that id doesn't exist."}), 404
    return jsonify({'msg': "order with that id was cancelled."}), 200

@orders_blueprint.route('/orders/<_id>/state',methods=['PUT'])
def change_order_state(_id):
    service = OrderService()
    content = request.get_json()
    new_state = content["state"]
    if new_state == "delivered":
        service.order_delivered(_id)
    elif new_state == "cancelled":
        service.order_cancelled(_id)
    elif new_state == "pickedUp":
        service.order_picked_up(_id)
    else :
        return jsonify({"msg": "Estado inválido" }), 409
    return jsonify({"msg":"El estado fue cambiado"}), 200
