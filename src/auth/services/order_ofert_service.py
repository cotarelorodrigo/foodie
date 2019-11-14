from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service
import time
from multiprocessing import Process


class OrderOfferService(Service):
    def create_order_ofert(self, data):
        from src.auth.models.order_table import OrderOfertsModel
        from src.auth.schemas.schemas import OrderOfertSchema

        def auto_cancel_ofert(order_ofert):
            TIME_OFERT_IS_VALID = 120
            time.sleep(TIME_OFERT_IS_VALID)
            if order_ofert.state == 'oferted':
                order_ofert.state = 'cancelled'
                order_ofert.save()

        order_ofert_data = OrderOfertSchema().load(data)
        order_ofert_data["state"] = 'oferted'
        order_ofert = OrderOfertsModel(order_ofert_data)
        order_ofert.save()
        Process(target=auto_cancel_ofert, args=(order_ofert,)).start()

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


