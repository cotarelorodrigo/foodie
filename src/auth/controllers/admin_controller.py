from flask import Blueprint, request, jsonify
from src.auth.services.user_service import UserService
from src.auth.services.delivery_service import DeliveryService
from src.auth.services.order_service import OrderService
from src.auth.services.shop_service import ShopService
from src.auth.services.direc_service import DirecService
from src.auth.services.products_service import ProductService
from src.auth.schemas.schemas import StaticsDatetimeRangeSchema
from src.auth.controllers.common_functions_controllers import auth_required, user_is_admin
from marshmallow import ValidationError
from src.auth.auth_exception import NotFoundException
import sqlalchemy
import marshmallow

admins_blueprint = Blueprint('admins', __name__)
# admin_service = AdminService()
statics_datetime_schema = StaticsDatetimeRangeSchema()


@admins_blueprint.route('/admin', methods=['GET'])
@auth_required
@user_is_admin
def admin():
    return jsonify({'200': 'Hola admin!!!'}), 200


###################### STATISTICS ######################

@admins_blueprint.route('/admin/statistics', methods=['GET'])
@auth_required
@user_is_admin
def statics():
    return jsonify(
        {"users": UserService().get_quantity_users(), "deliveries": DeliveryService().get_quantity_deliverys(),
         "completedOrders": OrderService().get_quantity_complete_orders(),
         "canceledOrders": OrderService().get_quantity_cancelled_orders()}), 200


@admins_blueprint.route('/admin/statistics/users', methods=['GET'])
@auth_required
@user_is_admin
def statics_users():
    try:
        data = {"year_from": request.args.get('year_from'), "month_from": request.args.get('month_from'),
                "year_to": request.args.get('year_to'), "month_to": request.args.get('month_to')}
        data = statics_datetime_schema.load(data)
        result = UserService().get_quantity_users_by_month(data['year_from'], data['month_from'], data['year_to'],
                                                           data['month_to'])
    except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
    except:
        raise
    else:
        return jsonify(result), 200


@admins_blueprint.route('/admin/statistics/deliveries', methods=['GET'])
@auth_required
@user_is_admin
def statics_deliverys():
    try:
        data = {"year_from": request.args.get('year_from'), "month_from": request.args.get('month_from'),
                "year_to": request.args.get('year_to'), "month_to": request.args.get('month_to')}
        data = statics_datetime_schema.load(data)
        result = DeliveryService().get_quantity_deliverys_by_month(data['year_from'], data['month_from'],
                                                                   data['year_to'], data['month_to'])
    except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
    except:
        raise
    else:
        return jsonify(result), 200


@admins_blueprint.route('/admin/statistics/orders/completed', methods=['GET'])
@auth_required
@user_is_admin
def statics_orders_completed():
    try:
        data = {"year_from": request.args.get('year_from'), "month_from": request.args.get('month_from'),
                "year_to": request.args.get('year_to'), "month_to": request.args.get('month_to')}
        data = statics_datetime_schema.load(data)
        result = OrderService().get_quantity_orders_by_month(data['year_from'], data['month_from'], data['year_to'],
                                                             data['month_to'], 'delivered')
    except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
    except:
        raise
    else:
        return jsonify(result), 200


@admins_blueprint.route('/admin/statistics/orders/canceled', methods=['GET'])
@auth_required
@user_is_admin
def statics_orders_cancelled():
    try:
        data = {"year_from": request.args.get('year_from'), "month_from": request.args.get('month_from'),
                "year_to": request.args.get('year_to'), "month_to": request.args.get('month_to')}
        data = statics_datetime_schema.load(data)
        result = OrderService().get_quantity_orders_by_month(data['year_from'], data['month_from'], data['year_to'],
                                                             data['month_to'], 'cancelled')
    except ValidationError:
        return jsonify({"error": "Informacion Incorrecta"}), 410
    except:
        raise
    else:
        return jsonify(result), 200


###################### SHOPS ######################

@admins_blueprint.route('/admin/shops', methods=['GET'])
@auth_required
@user_is_admin
def shops():
    pageNumber = request.args.get('p')
    pageSize = request.args.get('pSize')
    result = ShopService().get_N_shops(int(pageNumber) - 1, int(pageSize))
    return jsonify(result), 200


@admins_blueprint.route('/admin/shop', methods=['POST'])
@auth_required
@user_is_admin
def create_shop():
    try:
        content = request.get_json()
        ShopService().create_shop(content)
    except ValidationError:
        return jsonify({"error": "Informacion del shop Incorrecta"}), 420
    except:
        raise
    else:
        return jsonify({"OK": "Shop creado con exito!"}), 200

@admins_blueprint.route('/admin/shop/zone', methods=['POST'])
@auth_required
@user_is_admin
def create_shops_from_zone():
    try:
        content = request.get_json()
        shops = DirecService().get_shops_info({"latitude": content["latitude"], "longitude": content["longitude"]}, content["radius"])
        for shop in shops:
            shop["menu"] = ProductService().get_sample_products(5)
            ShopService().create_shop(shop)
    except ValidationError:
        return jsonify({"error": "Informacion del shop Incorrecta"}), 420
    except:
        raise
    else:
        if not shops:
            return jsonify({"error": "No hay shops en esa zona"}), 420
        return jsonify({"OK": "Shops creados con exito!"}), 200


@admins_blueprint.route('/admin/shop', methods=['GET'])
@auth_required
@user_is_admin
def get_shop():
    shop_id = request.args.get('id')
    try:
        response = ShopService().get_shop(shop_id)
    except NotFoundException as e:
        return jsonify({'404': "shop {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify(response), 200


@admins_blueprint.route('/admin/shop', methods=['DELETE'])
@auth_required
@user_is_admin
def delete_shop():
    shop_id = request.args.get('id')
    try:
        response = ShopService().delete_shop(shop_id)
    except NotFoundException as e:
        return jsonify({'404': "shop {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({'OK': "Shop deleted"}), 200


@admins_blueprint.route('/admin/shop', methods=['PUT'])
@auth_required
@user_is_admin
def update_shop():
    shop_id = request.args.get('id')
    content = request.get_json()
    try:
        response = ShopService().update_shop(shop_id, content)
    except NotFoundException as e:
        return jsonify({'404': "shop {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({"OK": "Shop actualizado con exito!"}), 200


###################### DELIVERYS ######################
@admins_blueprint.route('/admin/deliveries', methods=['GET'])
@auth_required
@user_is_admin
def deliveries():
    pageNumber = request.args.get('p')
    pageSize = request.args.get('pSize')
    result = DeliveryService().get_N_deliverys(int(pageNumber) - 1, int(pageSize))
    return jsonify(result), 200


@admins_blueprint.route('/admin/delivery', methods=['POST'])
@auth_required
@user_is_admin
def create_delivery():
    try:
        content = request.get_json()
        content['role'] = 'delivery'
        DeliveryService().create_delivery_user(content)
    except ValidationError:
        return jsonify({"error": "Informacion del delivery Incorrecta"}), 420
    except:
        raise
    else:
        return jsonify({"OK": "Delivery creado con exito!"}), 200


@admins_blueprint.route('/admin/delivery', methods=['GET'])
@auth_required
@user_is_admin
def get_delivery():
    delivery_id = request.args.get('id')
    try:
        response = DeliveryService().get_delivery(delivery_id)
    except NotFoundException as e:
        return jsonify({'404': "delivery {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify(response), 200


@admins_blueprint.route('/admin/delivery', methods=['DELETE'])
@auth_required
@user_is_admin
def delete_delivery():
    delivery_id = request.args.get('id')
    try:
        response = DeliveryService().delete_delivery(delivery_id)
    except NotFoundException as e:
        return jsonify({'404': "delivery {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({'OK': "delivery deleted"}), 200


@admins_blueprint.route('/admin/delivery', methods=['PUT'])
@auth_required
@user_is_admin
def update_delivery():
    delivery_id = request.args.get('id')
    content = request.get_json()
    try:
        response = DeliveryService().update_delivery(delivery_id, content)
    except NotFoundException as e:
        return jsonify({'404': "delivery {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({"OK": "Delivery actualizado con exito!"}), 200


###################### USERS ######################

@admins_blueprint.route('/admin/users', methods=['GET'])
@auth_required
@user_is_admin
def users():
    pageNumber = request.args.get('p')
    pageSize = request.args.get('pSize')
    result = UserService().get_N_users(int(pageNumber) - 1, int(pageSize))
    return jsonify(result), 200


@admins_blueprint.route('/admin/user', methods=['POST'])
@auth_required
@user_is_admin
def create_user():
    try:
        content = request.get_json()
        content['role'] = 'usuario'
        UserService().create_normal_user(content)
    except ValidationError:
        return jsonify({"error": "Informacion del usuario Incorrecta"}), 420
    except:
        raise
    else:
        return jsonify({"OK": "Usuario creado con exito!"}), 200


@admins_blueprint.route('/admin/user', methods=['GET'])
@auth_required
@user_is_admin
def get_user():
    user_id = request.args.get('id')
    try:
        response = UserService().get_user(user_id)
    except NotFoundException as e:
        return jsonify({'404': "user {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify(response), 200


@admins_blueprint.route('/admin/user', methods=['DELETE'])
@auth_required
@user_is_admin
def delete_user():
    user_id = request.args.get('id')
    try:
        response = UserService().delete_user(user_id)
    except NotFoundException as e:
        return jsonify({'404': "user {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({'OK': "user deleted"}), 200


@admins_blueprint.route('/admin/user', methods=['PUT'])
@auth_required
@user_is_admin
def update_user():
    user_id = request.args.get('id')
    content = request.get_json()
    try:
        response = UserService().update_user(user_id, content)
    except NotFoundException as e:
        return jsonify({'404': "user {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({"OK": "user actualizado con exito!"}), 200


###################### ORDERS ######################

@admins_blueprint.route('/admin/orders', methods=['GET'])
@auth_required
@user_is_admin
def orders():
    pageNumber = request.args.get('p')
    pageSize = request.args.get('pSize')
    filters = {'user_id': request.args.get('user_id'), 'delivery_id': request.args.get('delivery_id'),
               'shop_id': request.args.get('shop_id')}

    result = OrderService().get_N_orders_filtered(int(pageNumber) - 1, int(pageSize), filters)
    return jsonify(result), 200


###################### MENU ######################

@admins_blueprint.route('/admin/menu', methods=['GET'])
@auth_required
@user_is_admin
def get_menu():
    pageNumber = request.args.get('p')
    pageSize = request.args.get('pSize')
    shop_id = request.args.get('id')
    result = ProductService().get_N_products(shop_id, int(pageNumber) - 1, int(pageSize))
    return jsonify(result), 200


@admins_blueprint.route('/admin/product', methods=['POST'])
@auth_required
@user_is_admin
def create_product():
    try:
        content = request.get_json()
        ProductService().create_product(content)
    except ValidationError:
        return jsonify({"error": "Informacion del producto Incorrecta"}), 420
    except:
        raise
    else:
        return jsonify({"OK": "Producto creado con exito!"}), 200



@admins_blueprint.route('/admin/product', methods=['DELETE'])
@auth_required
@user_is_admin
def delete_product():
    product_id = request.args.get('id')
    try:
        response = ProductService().delete_product(product_id)
    except NotFoundException as e:
        return jsonify({'404': "product {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({'OK': "product deleted"}), 200


@admins_blueprint.route('/admin/product', methods=['PUT'])
@auth_required
@user_is_admin
def update_product():
    product_id = request.args.get('id')
    content = request.get_json()
    try:
        response = ProductService().update_product(product_id, content)
    except NotFoundException as e:
        return jsonify({'404': "product {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify({"OK": "product actualizado con exito!"}), 200


@admins_blueprint.route('/admin/product', methods=['GET'])
@auth_required
@user_is_admin
def get_product():
    product_id = request.args.get('id')
    try:
        response = ProductService().get_product(product_id)
    except NotFoundException as e:
        return jsonify({'404': "product {}".format(e.msg)}), 404
    except:
        raise
    else:
        return jsonify(response), 200