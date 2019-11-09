from flask import Blueprint, request, jsonify
from src.auth.services.user_service import UserService
from src.auth.services.delivery_service import DeliveryService
from src.auth.controllers.common_functions_controllers import auth_required, user_is_admin
import sqlalchemy
import marshmallow 

admins_blueprint = Blueprint('admins', __name__)
#admin_service = AdminService()


@admins_blueprint.route('/admin', methods=['GET'])
@auth_required
@user_is_admin
def admin():
     return jsonify({'200': 'Hola admin!!!'}), 200


@admins_blueprint.route('/admin/statics', methods=['GET'])
@auth_required
@user_is_admin
def statics():
    return jsonify({"users": UserService().get_quantity_users(), "deliverys": DeliveryService().get_quantity_deliverys(), "completeOrders": 0, "canceledOrders": 0}), 200



    

