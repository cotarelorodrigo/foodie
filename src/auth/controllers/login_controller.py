from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from src.auth.services.user_service import UserService
from src.auth.services.admin_service import AdminService
from src.auth.schemas.schemas import LoginSchema, RecoverSchema, LoginSchemaToken
from src.auth.auth_exception import NotFoundException
from src.jwt_handler import encode_data_to_jwt
#from src.auth.controllers.common_functions_controllers import verify_firebase_uid


login_blueprint = Blueprint('login', __name__)
login_schema = LoginSchema()
login_schema_token = LoginSchemaToken()
recover_schema = RecoverSchema()

def get_user_token(user_data):
    return encode_data_to_jwt(user_data)

@login_blueprint.route('/user/login', methods=['POST'])
def login():
    MINUTES_VALID_TOKEN = 20
    content = request.get_json()
    try:
        user_data = login_schema_token.load(content)
        verify_firebase_uid(user_data['firebase_uid'])
    except:
        try:
            user_data = login_schema.load(content)
            service = UserService()
            user = service.get_user_by_email(user_data["email"])
        except ValidationError:
            return jsonify({"msg": "Informacion Incorrecta"}), 410
        except NotFoundException as e:
            service = AdminService()
            is_admin = service.user_is_admin(user_data["email"], user_data["password"])
            if is_admin:
                token = encode_data_to_jwt({"user":user_data["email"], "is_admin": True}, MINUTES_VALID_TOKEN)
                return jsonify({"token": token}), 200
            return jsonify({"msg": e.msg}), 411
        except ValidationError:
            return jsonify({"msg": "Falta informacion de login"}), 410
        except:
            raise
        else:
            is_valid = UserService.compare_password(
                hashed=user["password"],
                plain=user_data["password"]
            )

            if not is_valid:
                return jsonify({"msg": "User not found or wrong password"}), 412
            
            token = encode_data_to_jwt({"user":user_data["email"], "is_admin": False}, MINUTES_VALID_TOKEN)
            return jsonify({"token": token}), 200
    else:
        token = encode_data_to_jwt({"user":user_data["email"], "is_admin": False}, MINUTES_VALID_TOKEN)
        return jsonify({"token": token}), 200


@login_blueprint.route('/user/recover', methods=['POST'])
def recover():
    from src.app import send_email
    try: 
        content = request.get_json()
        user_data = recover_schema.load(content)
        service = UserService()
        user = service.get_user_by_email(user_data["email"])
        msg_info = {}
        msg_info['tittle'] = "Foodie recover password"
        msg_info['body'] = "Hello {}, you recover token is: {}".format(user["name"], user["token"])
        msg_info['recipients'] = [user_data['email']]
        send_email(msg_info)
    except NotFoundException as e:
        return jsonify({"msg": e.msg}), 411
    except ValidationError:
        return jsonify({"msg": "Informacion Incorrecta"}), 410
    except:
        raise
    else:
        return jsonify({'msg':'Recover email sended'}), 200


@login_blueprint.route('/user/password', methods=['POST'])
def new_password():
    try: 
        token = request.headers.get('recover-password-token')
        content = request.get_json()
        user_data = login_schema.load(content)
        service = UserService()
        service.change_password(user_data["email"], user_data["password"])
    except NotFoundException as e:
        return jsonify({"msg": e.msg}), 411
    except ValidationError:
        return jsonify({"msg": "Informacion Incorrecta"}), 410
    except:
        raise
    else:
        return jsonify({'msg': 'New password seted'}), 200