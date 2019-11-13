from flask import Blueprint, request, jsonify
from src.auth.services.order_ofert_service import OrderOfertService
from src.auth.services.direc_service import DirecService
import sqlalchemy
import marshmallow 

delivery_blueprint = Blueprint('delivery', __name__)

@delivery_blueprint.route('/delivery/ofert', methods=['POST'])
def add_delivery_ofert():
    service = OrderOfertService()
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

@delivery_blueprint.route('/deliveries', methods=['GET'])
def get_deliveries():
    longitud = request.args.get('longitud')
    latitud = request.args.get('latitud')
    cantidad = request.args.get('cantidad')
    service = OrderOfertService()
    direc_service = DirecService()
    try:
        deliverys = service.get_available_deliverys()
        deliverys = direc_service(shop,deliverys)

@delivery_blueprint.route('/showoferts', methods=['GET'])
def show_oferts():
    service = OrderOfertService()
    oferts = service.get_oferts()
    return jsonify(oferts)
