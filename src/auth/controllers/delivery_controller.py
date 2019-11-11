from flask import Blueprint, request, jsonify
from src.auth.services.order_ofert_service import OrderOfertService
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
        return jsonify({'msg': 'The order ofert was created without problems'}), 200


@delivery_blueprint.route('/showoferts', methods=['GET'])
def show_oferts():
    service = OrderOfertService()
    oferts = service.get_oferts()
    return jsonify(oferts)
