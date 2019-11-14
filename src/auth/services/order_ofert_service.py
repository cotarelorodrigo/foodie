from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service
import datetime


class OrderOfferService(Service):
    def create_order_ofert(self, data):
        from src.auth.models.order_table import OrderOffersModel
        from src.auth.schemas.schemas import OrderOfferSchema
        order_ofert_data = OrderOfferSchema().load(data)
        order_ofert_data["state"] = 'oferted'
        order_ofert = OrderOffersModel(order_ofert_data)
        order_ofert.save() 

    def get_oferts(self):
        from src.auth.models.order_table import OrderOffersModel
        response = OrderOffersModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)

    def get_offer_by_id(self,_id):
        from src.auth.models.order_table import OrderOffersModel
        response = OrderOffersModel.get_offer(_id)
        return self.sqlachemy_to_dict(response)


