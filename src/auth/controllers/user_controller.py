from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.auth.services.user_service import UserService
from src.auth.schemas.schemas import UserSchema, LoginSchema, CreditCardSchema
from src.auth.auth_exception import InvalidUserInformation, NotFoundEmail, AccessDeniedException, NotFoundException
from src.jwt_handler import encode_data_to_jwt
from src.auth.controllers.common_functions_controllers import auth_required

user_blueprint = Blueprint('users', __name__)
users_schema = UserSchema()
card_schema = CreditCardSchema()

@user_blueprint.route('/', methods=['GET'])
def hello_world():
    return jsonify("Hello world"), 200

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
    user = service.get_normal_user(_id)
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

@user_blueprint.route('/user/<_id>/premium_subscription', methods=['PUT'])
def set_premium_subscription(_id):
    service = UserService()
    user = service.get_normal_user(_id)
    if not user: 
        raise NotFoundException("user with that id doesn't exist.")
    content = request.get_json()
    card = card_schema.load(content)
    service.update_user(_id,{"suscripcion": "premium"})
    return jsonify("subscription updated to premium")

@user_blueprint.route('/users/<_id>/picture',methods=["PUT"])
def change_picture(_id):
    content = request.get_json()
    picture = content["picture"]
    service = UserService()
    service.update_user(_id,content)
    return jsonify({"msg": "Profile picture changed"}),200


@user_blueprint.route('/users/profile/<email>', methods=['GET'])
@auth_required
def get_user_profile(email):
    service = UserService()
    response = service.get_user_profile(email)
    return jsonify(response), 200

@user_blueprint.route('/users/<_id>/position', methods=['PATCH'])
def update_user_coordinates(_id):
    service = UserService()
    content = request.get_json()
    try:
        coordinates = {"latitude": content['latitude'],"longitude": content['longitude'] }
        service.update_coordinates(_id, coordinates)
    except:
        raise
    else:
        return jsonify({"msg": "Coordenadas actualizadas"}), 200


@user_blueprint.route('/users/<_id>', methods=['PATCH'])
def update_user_info(_id):
    service = UserService()
    content = request.get_json()
    try:
        response = UserService().update_user(_id, content)
    except NotFoundException as e:
        return jsonify({'404': "user {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({"OK": "user actualizado con exito!"}), 200

@user_blueprint.route('/users/favours', methods=['GET'])
def get_users_favours():
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    cantidad = int(request.args.get('cantidad'))
    if (longitude is None) | (latitude is None) | (cantidad is None):
        raise InvalidQueryParameters("Invalid query values")
    user_service = UserService()
    direc_service = DirecService()
    try:
        shop = {"latitude": latitude, "longitude": longitude}
        users = user_service.get_available_users_favours()
        users = direc_service.get_nearly_deliverys(shop,users)
    except:
        raise
    else:
        if not users:
            return jsonify({'msg': 'No hay users cerca'}), 431
        return jsonify(users[:cantidad]), 200

@user_blueprint.route('/users/<_id>/password', methods=['PUT'])
def change_user_password(_id):
    service = UserService()
    user = service.get_user(_id)
    content = request.get_json()
    new_pass = content["password"] 
    service.change_password(user["email"], new_pass)
    return jsonify({"msg":"Password changed"}),200


