from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service
import datetime
from dateutil import relativedelta

class OrderService(Service):
    def create_order(self, order_data):
        from src.auth.models.order_table import OrderModel, OrderProductsModel
        from src.auth.schemas.schemas import OrderSchema
        order_schema = OrderSchema()
        order_info, products_info = order_schema.load(order_data)
        order = OrderModel(order_info)
        products = [OrderProductsModel(product) for product in products_info]
        order.save() #Hay que guardar primero la orden orden porq es la parte unaria de la relacion
        for p in products:
            order.products.append(p)
            p.save()
        return order


    def get_orders(self):
        from src.auth.models.order_table import OrderModel
        response = OrderModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)
    
    def get_order_by_id(self, _order_id):
        from src.auth.models.order_table import OrderModel
        order = OrderModel.query.filter_by(order_id=_order_id).one()
        return self.sqlachemy_to_dict(order)


    def get_products_orders(self):
        from src.auth.models.order_table import OrderProductsModel
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

    def get_quantity_complete_orders(self):
        from src.auth.models.order_table import OrderModel
        return OrderModel.query.filter_by(state='delivered').count()

    def get_quantity_cancelled_orders(self):
        from src.auth.models.order_table import OrderModel
        return OrderModel.query.filter_by(state='cancelled').count()

    def get_quantity_orders_date(self, date_from, date_to, state='delivered'):
        from src.auth.models.order_table import OrderModel
        return OrderModel.query.filter(OrderModel.state == state).filter(OrderModel.created_at >= date_from).filter(OrderModel.created_at <= date_to).count()

    def get_quantity_orders_by_month(self, year_from, month_from, year_to, month_to, state):
        date_from = datetime.date(year=year_from,month=month_from, day=1)
        date_to = datetime.date(year=year_to,month=month_to, day=1)
        result = []
        delta = relativedelta.relativedelta(date_from, date_to)
        for delta_month in range(abs(delta.months)):
            date_from_aux = date_from + relativedelta.relativedelta(months=delta_month)
            date_to_aux = date_from + relativedelta.relativedelta(months=delta_month+1)
            result.append({"year": date_to_aux.year, "month": date_to_aux.month, "amount": self.get_quantity_orders_date(date_from_aux, date_to_aux, state)})
        return result