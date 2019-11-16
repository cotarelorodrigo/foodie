from flask import Blueprint, request, jsonify
from src.auth.services.order_ofert_service import OrderOfferService
from src.auth.services.delivery_service import DeliveryService
from src.auth.services.direc_service import DirecService
import sqlalchemy
import marshmallow 

delivery_blueprint = Blueprint('delivery', __name__)

@delivery_blueprint.route('/delivery/<_id>/offers', methods=['POST'])
def add_delivery_offer(_id):
    service = OrderOfferService()
    try:
        content = request.get_json()
        service.create_order_ofert(content)
    except marshmallow.exceptions.ValidationError as e:
        return jsonify({'msg': 'Missing order ofert information: {}'.format(e)}), 400
    except sqlalchemy.exc.IntegrityError:
        return jsonify({'msg': 'order_id or delivery_id invalid'}), 430
    except:
        raise
    else:
        return jsonify({'msg': 'Order ofert created'}), 200

@delivery_blueprint.route('/delivery/<_id>/offers/<_offer_id>', methods=['PATCH'])
def put_delivery_state(_id,_offer_id):
    service = OrderOfferService()
    try:
        content = request.get_json()
        state = content['state']
        service.update_offer_state(_id,_offer_id,state)
    except:
        raise
    else:
        return jsonify({'msg': 'Offer modified'})

        


@delivery_blueprint.route('/delivery/<_id>/offers', methods=['GET'])
def getOffers(_id):
    service = OrderOfferService()
    response = service.get_delivery_current_offers(_id)
    return jsonify(response),200

@delivery_blueprint.route('/deliveries', methods=['GET'])
def get_deliveries():
    longitude = request.args.get('longitude')
    latitude = request.args.get('latitude')
    cantidad = request.args.get('cantidad')
    if (longitude is None) | (latitude is None) | (cantidad is None):
        raise InvalidQueryParameters("Invalid query values")
    delivery_service = DeliveryService()
    direc_service = DirecService()
    try:
        shop = {"latitude": latitude, "longitude": longitude}
        deliverys = delivery_service.get_available_deliverys()
        deliverys = direc_service.get_nearly_deliverys(shop,deliverys)
    except:
        raise
    else:
        if not deliverys:
            return jsonify({'msg': 'No hay deliveries cerca'}), 431
        return jsonify(deliverys), 200
        
@delivery_blueprint.route('/showoferts', methods=['GET'])
def show_oferts():
    service = OrderOfferService()
    oferts = service.get_oferts()
    return jsonify(oferts)
