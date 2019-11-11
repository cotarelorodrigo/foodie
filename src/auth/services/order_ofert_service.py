from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service
import datetime


class OrderOfertService(Service):
    def create_order_ofert(self, data):
        from src.auth.models.order_table import OrderOfertsModel
        from src.auth.schemas.schemas import OrderOfertSchema
        order_ofert_data = OrderOfertSchema().load(data)
        order_ofert_data["state"] = 'oferted'
        order_ofert = OrderOfertsModel(order_ofert_data)
        order_ofert.save() 
