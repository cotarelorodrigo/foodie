from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.auth.services.user_service import UserService
from src.auth.schemas.schemas import LoginSchema, RecoverSchema
from src.auth.auth_exception import NotFoundException
from src.jwt_handler import encode_data_to_jwt
from flask_mail import Message

login_blueprint = Blueprint('login', __name__)
login_schema = LoginSchema()
recover_schema = RecoverSchema()

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


@login_blueprint.route('/user/recover', methods=['POST'])
def recover():
    from src.app import mail, app
    try: 
        content = request.get_json()
        user_data = recover_schema.load(content)
        service = UserService()
        user = service.get_user_by_email(user_data["email"])
    except NotFoundException as e:
        return jsonify({"error": e.msg}), 411
    except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
    except:
        raise
    else:
        msg = Message("Hello, you recover token is: {}".format(user["token"]),
                recipients=user_data['email'])
        
        mail.send(msg)
        return jsonify('Recover email sended'), 200