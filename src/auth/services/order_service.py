from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service

class OrderService(Service):
    def create_order(self, order_data):
        from src.auth.models.order_table import OrderModel
        order = OrderModel(order_data)
        order.save()