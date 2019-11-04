from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.auth.services.user_service import UserService
from src.auth.schemas.schemas import NormalUserSchema, DeliveryUserSchema
from marshmallow import ValidationError
from src.auth.auth_exception import InvalidUserInformation
#from src.jwt_handler import encode_data_to_jwt

register_blueprint = Blueprint('register', __name__)
normal_user_schema = NormalUserSchema()
delivery_user_schema = DeliveryUserSchema()

@register_blueprint.route('/user', methods=['POST'])
def add_user():
    content = request.get_json()
    service = UserService()
    try:
        user_data = normal_user_schema.load(content)
        service.create_normal_user(user_data=user_data)
    except ValidationError:
        raise InvalidUserInformation("Falta informacion del usuario")
    except IntegrityError as e:
        return jsonify({'409': 'user with this email already exists.'}), 409
    except:
        raise
    else:
        return jsonify({'200': 'a new user was created.'}), 200

@register_blueprint.route('/delivery', methods=['POST'])
def add_delivery():
    content = request.get_json()
    service = UserService()
    try:
        user_data = delivery_user_schema.load(content)
        service.create_delivery_user(user_data=user_data)
    except ValidationError:
        raise InvalidUserInformation("Falta informacion del usuario")
    except IntegrityError as e:
        return jsonify({'409': 'user with this email already exists.'}), 409
    except:
        raise
    else:
        return jsonify({'200': 'a new user was created.'}), 200