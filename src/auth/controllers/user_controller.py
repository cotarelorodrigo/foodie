from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.auth.services.user_service import UserService
from src.auth.schemas.schemas import UserSchema
from src.auth.auth_exception import InvalidUserInformation, NotFoundEmail

pedido_blueprint = Blueprint('pedido', __name__)
users_schema = UserSchema()

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
    if not user: return jsonify({'404': "user with that id doesn't exist."})
    return jsonify({'200': "user with that id exists."})


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


@pedido_blueprint.route('/user/email', methods=['POST'])
def check_user_email():
    service = UserService()
    content = request.get_json()
    if service.check_email(content['email']):
        return "user with that email exists", 200
    else:
        raise NotFoundEmail("user with that email doesnt exist")
