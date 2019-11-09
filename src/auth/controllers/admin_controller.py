from flask import Blueprint, request, jsonify
from src.auth.services.user_service import UserService
from src.auth.services.delivery_service import DeliveryService
from src.auth.services.order_service import OrderService
from src.auth.schemas.schemas import StaticsDatetimeRangeSchema
from src.auth.controllers.common_functions_controllers import auth_required, user_is_admin
from marshmallow import ValidationError
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


@admins_blueprint.route('/admin/statics', methods=['GET'])
@auth_required
@user_is_admin
def statics():
    return jsonify({"users": UserService().get_quantity_users(), "deliverys": DeliveryService().get_quantity_deliverys(), 
    "completeOrders": OrderService().get_quantity_complete_orders(), "canceledOrders": OrderService().get_quantity_cancelled_orders()}), 200

@admins_blueprint.route('/admin/statics/users', methods=['GET'])
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

@admins_blueprint.route('/admin/statics/deliverys', methods=['GET'])
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
    

