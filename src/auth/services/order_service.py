from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service

class OrderService(Service):
    def create_order(self, order_data):
        from src.auth.models.order_table import OrderModel
        from src.auth.models.order_product_table import OrderProductsModel
        from src.auth.schemas.schemas import OrderSchema
        order_schema = OrderSchema()
        order_info, products_info = order_schema.load(order_data)
        order = OrderModel(order_info)
        products = [OrderProductsModel(product) for product in products_info]
        order.save() #Hay que guardar primero la orden orden porq es la parte unaria de la relacion
        for p in products:
            order.products.append(p)
            p.save()


    def get_orders(self):
        from src.auth.models.order_table import OrderModel
        response = OrderModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)
    
    def get_products_orders(self):
        from src.auth.models.order_product_table import OrderProductsModel
        response = OrderProductsModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)

    def catch_order(self, _order_id, _delivery_id):
        from src.app import db
        from src.auth.models.order_table import OrderModel
        order = OrderModel.query.filter_by(order_id=_order_id).one()
        order.delivery_id = _delivery_id
        order.state = "onWay"
        
        return order

    def change_order_state(self, _order_id, _state):
        from src.app import db
        from src.auth.models.order_table import OrderModel
        from src.auth.schemas.schemas import OrderState
        from src.auth.auth_exception import InvalidInformation
        order = OrderModel.query.filter_by(order_id=_order_id).one()
        if _state in OrderState:
            order.state = _state
            db.session.commit()
        else:
            raise InvalidInformation('Estado de orden invalido')
        return order
