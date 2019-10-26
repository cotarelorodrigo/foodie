from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.auth.services.user_service import UserService
from src.auth.schemas.schemas import LoginSchema
from src.auth.auth_exception import NotFoundException
from src.jwt_handler import encode_data_to_jwt

login_blueprint = Blueprint('login', __name__)
login_schema = LoginSchema()

def get_user_token(user_data):
    return encode_data_to_jwt(user_data)

@login_blueprint.route('/user/login', methods=['POST'])
def login():
    try: 
        content = request.get_json()
        user_data = login_schema.load(content)
        service = UserService()
        user = service.get_user_by_email(user_data["email"])
    except NotFoundException as e:
        return jsonify({"error": e.msg}), 411
    except ValidationError:
        return jsonify({"error": "Falta informacion de login"}), 410
    except:
        raise
    else:
        is_valid = UserService.compare_password(
            hashed=user["password"],
            plain=user_data["password"]
        )
        if not is_valid:
            return jsonify({"error": "User not found or wrong password"}), 412
        return jsonify(user["token"]), 200