from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.auth.services.user_service import UserService
from src.auth.schemas.schemas import UserSchema, LoginSchema
from src.auth.auth_exception import InvalidUserInformation, NotFoundEmail, AccessDeniedException
from src.jwt_handler import encode_data_to_jwt
from src.auth.controllers.common_functions_controllers import auth_required

user_blueprint = Blueprint('users', __name__)
users_schema = UserSchema()

@user_blueprint.route('/users', methods=['GET'])
def get_users():
    service = UserService()
    all_users = service.get_users()
    return jsonify(all_users), 200

@user_blueprint.route('/get_normal_users', methods=['GET'])
def get_normal_users():
    service = UserService()
    all_users = service.get_normal_users()
    return jsonify(all_users), 200

@user_blueprint.route('/get_delivery_users', methods=['GET'])
def get_delivery_users():
    service = UserService()
    all_users = service.get_delivery_users()
    return jsonify(all_users), 200

@user_blueprint.route('/users/<_id>', methods=['GET'])
def get_user(_id):
    service = UserService()
    user = service.get_user(_id)
    if not user: 
        return jsonify({'404': "user with that id doesn't exist."}), 404
    return jsonify(user), 200

@user_blueprint.route('/users/<_id>', methods=['DELETE'])
def delete_user(_id):
    service = UserService()
    user = service.delete_user(_id)
    if not user: 
        return jsonify({'404': "user with that id doesn't exist."}), 404
    return jsonify({'200': "user with that id was deleted."}), 200


@user_blueprint.route('/users/email/<email>', methods=['GET'])
def check_user_email(email):
    service = UserService()
    if service.check_email(email):
        return "user with that email exists", 200
    else:
        raise NotFoundEmail("user with that email doesnt exist")


@user_blueprint.route('/users/profile/<email>', methods=['GET'])
@auth_required
def get_user_profile(email):
    service = UserService()
    response = service.get_user_profile(email)
    return jsonify(response), 200