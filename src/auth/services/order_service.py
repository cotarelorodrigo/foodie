from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service

class OrderService(Service):
    def create_order(self, order_data):
        from src.auth.models.order_table import OrderModel
        order = OrderModel(order_data)
        order.save()

    def get_orders(self):
        from src.auth.models.order_table import OrderModel
        response = OrderModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)

    def delete_order(self,_id):
        from src.app import db
        from src.auth.models.order_table import OrderModel
        response = OrderModel.query.filter_by(order_id=_id).delete()
        db.session.commit()
        return response
