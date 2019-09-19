from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.auth.services.user_service import UserService
from src.auth.schemas.schemas import UserSchema

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


@pedido_blueprint.route('/user', methods=['POST'])
def add_user():
    service = UserService()
    content = request.get_json()
    
    try:
        user_data = users_schema.load(content)
    except:
        return jsonify({"error": "faltan parametros para agregar un usuario"}), 420

    try:
        service.create_user(user_data=user_data)
    except IntegrityError as e:
        return jsonify({'409': 'user with this email already exists.'})
    else:
        return jsonify({'200': 'a new user was created.'})