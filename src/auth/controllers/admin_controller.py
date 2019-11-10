from flask import Blueprint, request, jsonify
from src.auth.services.user_service import UserService
from src.auth.services.delivery_service import DeliveryService
from src.auth.services.order_service import OrderService
from src.auth.services.shop_service import ShopService
from src.auth.schemas.schemas import StaticsDatetimeRangeSchema
from src.auth.controllers.common_functions_controllers import auth_required, user_is_admin
from marshmallow import ValidationError
from src.auth.auth_exception import NotFoundException
import sqlalchemy
import marshmallow 

admins_blueprint = Blueprint('admins', __name__)
#admin_service = AdminService()
statics_datetime_schema = StaticsDatetimeRangeSchema()


@admins_blueprint.route('/admin', methods=['GET'])
@auth_required
@user_is_admin
def admin():
     return jsonify({'200': 'Hola admin!!!'}), 200

###################### STATISTICS ######################

@admins_blueprint.route('/admin/statistics', methods=['GET'])
@auth_required
@user_is_admin
def statics():
    return jsonify({"users": UserService().get_quantity_users(), "deliverys": DeliveryService().get_quantity_deliverys(), 
    "completeOrders": OrderService().get_quantity_complete_orders(), "canceledOrders": OrderService().get_quantity_cancelled_orders()}), 200

@admins_blueprint.route('/admin/statistics/users', methods=['GET'])
@auth_required
@user_is_admin
def statics_users():
     try:
          data = {"year_from":request.args.get('year_from'), "month_from":request.args.get('month_from'),
                    "year_to":request.args.get('year_to'), "month_to":request.args.get('month_to')}
          data = statics_datetime_schema.load(data)
          result = UserService().get_quantity_users_by_month(data['year_from'], data['month_from'], data['year_to'], data['month_to'])
     except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
     except:
          raise
     else:
          return jsonify(result), 200

@admins_blueprint.route('/admin/statistics/deliverys', methods=['GET'])
@auth_required
@user_is_admin
def statics_deliverys():
     try:
          data = {"year_from":request.args.get('year_from'), "month_from":request.args.get('month_from'),
                    "year_to":request.args.get('year_to'), "month_to":request.args.get('month_to')}
          data = statics_datetime_schema.load(data)
          result = DeliveryService().get_quantity_deliverys_by_month(data['year_from'], data['month_from'], data['year_to'], data['month_to'])
     except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
     except:
          raise
     else:
          return jsonify(result), 200
    
@admins_blueprint.route('/admin/statistics/orders/completed', methods=['GET'])
@auth_required
@user_is_admin
def statics_orders_completed():
     try:
          data = {"year_from":request.args.get('year_from'), "month_from":request.args.get('month_from'),
                    "year_to":request.args.get('year_to'), "month_to":request.args.get('month_to')}
          data = statics_datetime_schema.load(data)
          result = OrderService().get_quantity_orders_by_month(data['year_from'], data['month_from'], data['year_to'], data['month_to'], 'delivered')
     except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
     except:
          raise
     else:
          return jsonify(result), 200

@admins_blueprint.route('/admin/statistics/orders/cancelled', methods=['GET'])
@auth_required
@user_is_admin
def statics_orders_cancelled():
     try:
          data = {"year_from":request.args.get('year_from'), "month_from":request.args.get('month_from'),
                    "year_to":request.args.get('year_to'), "month_to":request.args.get('month_to')}
          data = statics_datetime_schema.load(data)
          result = OrderService().get_quantity_orders_by_month(data['year_from'], data['month_from'], data['year_to'], data['month_to'], 'cancelled')
     except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
     except:
          raise
     else:
          return jsonify(result), 200

###################### SHOPS ######################

@admins_blueprint.route('/admin/shops', methods=['GET'])
@auth_required
@user_is_admin
def shops():
     pageNumber = request.args.get('p')
     pageSize = request.args.get('pSize')
     result = ShopService().get_N_shops(int(pageNumber), int(pageSize))
     return jsonify(result), 200


@admins_blueprint.route('/admin/shop', methods=['POST'])
@auth_required
@user_is_admin
def create_shop():
     try:
          content = request.get_json()
          ShopService().create_shop(content)
     except ValidationError:
        return jsonify({"error": "Informacion del shop Incorrecta"}), 420
     except:
          raise
     else:
          return jsonify({"OK": "Shop creado con exito!"}), 200

@admins_blueprint.route('/admin/shop', methods=['GET'])
@auth_required
@user_is_admin
def get_shop():
     shop_id = request.args.get('id')
     try:
          response = ShopService().get_shop(shop_id)
     except NotFoundException as e:
          return jsonify({'404': "shop {}".format(e.msg)}), 404
     except:
          raise
     else:
          return jsonify(response), 200

@admins_blueprint.route('/admin/shop', methods=['DELETE'])
@auth_required
@user_is_admin
def delete_shop():
     shop_id = request.args.get('id')
     try:
          response = ShopService().delete_shop(shop_id)
     except NotFoundException as e:
          return jsonify({'404': "shop {}".format(e.msg)}), 404
     except:
          raise
     else:
          return jsonify({'OK': "Shop deleted"}), 200

@admins_blueprint.route('/admin/shop', methods=['PUT'])
@auth_required
@user_is_admin
def update_shop():
     shop_id = request.args.get('id')
     content = request.get_json()
     try: 
          response = ShopService().update_shop(shop_id, content)
     except NotFoundException as e:
          return jsonify({'404': "shop {}".format(e.msg)}), 404
     except:
          raise
     else:
          return jsonify({"OK": "Shop actualizado con exito!"}), 200

###################### DELIVERYS ######################
@admins_blueprint.route('/admin/deliveries', methods=['GET'])
@auth_required
@user_is_admin
def deliveries():
     pageNumber = request.args.get('p')
     pageSize = request.args.get('pSize')
     result = DeliveryService().get_N_deliverys(int(pageNumber), int(pageSize))
     return jsonify(result), 200

@admins_blueprint.route('/admin/delivery', methods=['POST'])
@auth_required
@user_is_admin
def create_delivery():
     try:
          content = request.get_json()
          DeliveryService().create_delivery_user(content)
     except ValidationError:
        return jsonify({"error": "Informacion del delivery Incorrecta"}), 420
     except:
          raise
     else:
          return jsonify({"OK": "Delivery creado con exito!"}), 200


@admins_blueprint.route('/admin/delivery', methods=['GET'])
@auth_required
@user_is_admin
def get_delivery():
     delivery_id = request.args.get('id')
     try:
          response = DeliveryService().get_delivery(delivery_id)
     except NotFoundException as e:
          return jsonify({'404': "delivery {}".format(e.msg)}), 404
     except:
          raise
     else:
          return jsonify(response), 200

@admins_blueprint.route('/admin/delivery', methods=['DELETE'])
@auth_required
@user_is_admin
def delete_delivery():
     delivery_id = request.args.get('id')
     try:
          response = DeliveryService().delete_delivery(delivery_id)
     except NotFoundException as e:
          return jsonify({'404': "delivery {}".format(e.msg)}), 404
     except:
          raise
     else:
          return jsonify({'OK': "delivery deleted"}), 200


@admins_blueprint.route('/admin/delivery', methods=['PUT'])
@auth_required
@user_is_admin
def update_delivery():
     delivery_id = request.args.get('id')
     content = request.get_json()
     try: 
          response = DeliveryService().update_delivery(delivery_id, content)
     except NotFoundException as e:
          return jsonify({'404': "delivery {}".format(e.msg)}), 404
     except:
          raise
     else:
          return jsonify({"OK": "Delivery actualizado con exito!"}), 200