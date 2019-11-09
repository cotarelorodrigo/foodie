from flask import Blueprint, request, jsonify
#from src.auth.services.admin_service import AdminService
from src.auth.controllers.common_functions_controllers import auth_required, user_is_admin
#from src.auth.schemas.schemas import OrderSchema
import sqlalchemy
import marshmallow 

admins_blueprint = Blueprint('admins', __name__)
#order_schema = OrderSchema()

@admins_blueprint.route('/admin', methods=['GET'])
@auth_required
@user_is_admin
def admin():
     return jsonify({'200': 'Hola admin!!!'}), 200
