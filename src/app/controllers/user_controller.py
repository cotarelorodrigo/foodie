from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.app.services.user_service import UserService
from src.app.schemas.schemas import UserSchema, LoginSchema
from src.app.app_exception import InvalidUserInformation, NotFoundEmail, AccessDeniedException
from src.jwt_handler import encode_data_to_jwt

pedido_blueprint = Blueprint('pedido', __name__)
users_schema = UserSchema()
login_schema = LoginSchema()

def get_user_token(user_data):
    return encode_data_to_jwt(user_data)

@pedido_blueprint.route('/user/login', methods=['POST'])
def login():
    content = request.get_json()
    user_data = login_schema.load(content)
    service = UserService()
    user = service.get_user_by_email(user_data["email"])
    is_valid = UserService.compare_password(
        hashed=user["password"],
        plain=user_data["password"]
    )
    if not is_valid:
        raise AccessDeniedException({"error": "User not found or wrong password"})
    del user["password"]
    token = get_user_token({
        "email": user["email"]
    })
    user.update({"token": token})
    return jsonify(user)


@pedido_blueprint.route('/get_users', methods=['GET'])
def get_users():
    service = UserService()
    all_users = service.get_users()
    result = {}
    print(all_users)
    for u in all_users:
        result[u.name] = u.email
    return result

@pedido_blueprint.route('/user/<_id>', methods=['GET'])
def get_user(_id):
    service = UserService()
    user = service.get_user(_id)
    if not user: 
        return jsonify({'404': "user with that id doesn't exist."}), 404
    return jsonify({'200': "user with that id exists."}), 200

@pedido_blueprint.route('/user/<_id>', methods=['DELETE'])
def delete_user(_id):
    service = UserService()
    user = service.delete_user(_id)
    if not user: 
        return jsonify({'404': "user with that id doesn't exist."}), 404
    return jsonify({'200': "user with that id was deleted."}), 200


@pedido_blueprint.route('/user', methods=['POST'])
def add_user():
    service = UserService()
    content = request.get_json()
    
    try:
        user_data = users_schema.load(content)
    except:
        raise InvalidUserInformation("Falta informacion del usuario")

    try:
        service.create_user(user_data=user_data)
    except IntegrityError as e:
        return jsonify({'409': 'user with this email already exists.'})
    else:
        return jsonify({'200': 'a new user was created.'})


@pedido_blueprint.route('/user/email/<email>', methods=['GET'])
def check_user_email(email):
    service = UserService()
    if service.check_email(email):
        return "user with that email exists", 200
    else:
        raise NotFoundEmail("user with that email doesnt exist")
