from flask import Blueprint, request, jsonify


shops_blueprint = Blueprint('shops', __name__)


@shops_blueprint.route('/shop/<int(min=1, max=300):id>', methods=['GET'])
def get_shop(id):
    return jsonify({'response': 'hello shop controller'})