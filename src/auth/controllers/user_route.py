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
        result[u.first_name] = u.last_name
        result[str(u.id)] = u.email
    return result


@pedido_blueprint.route('/add_user', methods=['GET'])
def add_user():
    service = UserService()
    user_data = {'id':1, 'first_name':'Rodrigo', 'last_name':'Cotarelo',
    'email': 'asd@asd.com', 'password':'123qwe', 'phone_number':523952,
    'token':'gwhehwhw', 'reputation': 340, 'gratitude_points':210, 'picture_uri':'sdgHQEH'}
    try:
        service.create_user(user_data=user_data)
    except IntegrityError:
        return jsonify({'200': 'El usuario default ya esta agregado'})
    else:
        return jsonify({'200': 'Usuario default agregado'})