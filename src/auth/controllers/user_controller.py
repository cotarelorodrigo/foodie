from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from src.auth.services.user_service import UserService
from src.auth.services.order_ofert_service import OrderOfferService
from src.auth.schemas.schemas import UserSchema, LoginSchema, CreditCardSchema
from src.auth.auth_exception import InvalidUserInformation, NotFoundEmail, AccessDeniedException, NotFoundException, NotEnoughFavourPoints, InvalidQueryParameters
from src.jwt_handler import encode_data_to_jwt
from src.auth.controllers.common_functions_controllers import auth_required
from src.auth.services.direc_service import DirecService
import marshmallow 
import sqlalchemy

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
    user = service.get_normal_user(_id, dict_format=True)
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

@user_blueprint.route('/users/<_id>/premium_subscription', methods=['PUT'])
def set_premium_subscription(_id):
    service = UserService()
    user = service.get_normal_user(_id)
    if not user: 
        raise NotFoundException("user with that id doesn't exist.")
    content = request.get_json()
    card = card_schema.load(content)
    service.update_user(int(_id),{"suscripcion": "premium"})
    return jsonify({"msg":"subscription updated to premium"}),200
    

@user_blueprint.route('/users/<_id>/premium_subscription', methods=['DELETE'])
def cancel_premium_subscription(_id):
    service = UserService()
    user = service.get_normal_user(_id)
    if not user: 
        raise NotFoundException("user with that id doesn't exist.")
    service.update_user(int(_id),{"suscripcion": "flat"})
    return jsonify({"msg":"subscription updated to flat"}),200

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

@user_blueprint.route('/users/<_id>/favour_offers',methods=['GET'])
def get_current_offers(_id):
    service = UserService()
    response = service.get_user_favour_offers(_id)
    return jsonify(response),200

@user_blueprint.route('/users/<_id>/favour_offers',methods=['POST'])
def offer_a_favour(_id):
    service = OrderOfferService()
    try:
        content = request.get_json()
        offer_id = service.create_favour_offer(content)
    except marshmallow.exceptions.ValidationError as e:
        return jsonify({'msg': 'Missing order ofert information: {}'.format(e)}), 400
    except sqlalchemy.exc.IntegrityError:
        return jsonify({'msg': 'order_id or delivery_id invalid'}), 430
    except NotEnoughFavourPoints:
        return jsonify({"msg": "No tienes suficientes puntos"}), 408

    except:
        raise
    else:
        return jsonify({'id': offer_id }), 200

@user_blueprint.route('/users/<_id>/favour_offers/<_offer_id>', methods=['PATCH'])
def put_delivery_state(_id,_offer_id):
    service = OrderOfferService()
    try:
        content = request.get_json()
        state = content['state']
        service.update_favour_offer_state(_id,_offer_id,state)
    except:
        return jsonify({"msg": "Error: oferta inválida o cancelada"}), 409
    else:
        return jsonify({'msg': 'Offer modified'}),200

@user_blueprint.route('/users/<_id>/favour_offers/<_offer_id>',methods=['GET'])
def get_favour_offer_by_user_and_id(_id,_offer_id):
    service = OrderOfferService()
    offer = service.get_favour_offer_by_id(_offer_id)
    return jsonify(offer),200

@user_blueprint.route('/users/<_id>/make_favours',methods=['PUT'])
def put_make_favours_indicator(_id):
    service = UserService()
    content = request.get_json()
    make_favours = content['make_favours']
    if make_favours is None:
        return jsonify({'msg': 'Contenido del request es inválido'}), 409
    user = service.put_making_favours(_id,make_favours)
    return jsonify({'msg':'Usuario modificado con exito'}), 200

@user_blueprint.route("/favour_offers/<_id>",methods=['GET'])
def get_favour_offer_by_id(_id):
    service = OrderOfferService()
    offer = service.get_favour_offer_by_id(_id)
    return jsonify(offer), 200
 
@user_blueprint.route("/favour_offers/<_id>",methods=['PATCH'])
def update_favour_offer_state(_id):
    service = OrderOfferService()
    content = request.get_json()
    state = content['state']
    try:
        service.update_favour_offer_state()
    except:
        return jsonify({'msg': 'Error: la oferta fue cancelada o el id de oferta es invalido'}),409
    return jsonify({'msg': 'Offer modified'}), 200