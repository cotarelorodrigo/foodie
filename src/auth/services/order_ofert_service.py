from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException,InvalidStateChange
from src.auth.services.service import Service
import time
from src.auth.services.order_service import OrderService

from multiprocessing import Process


class OrderOfferService(Service):
    def create_order_ofert(self, data):
        from src.auth.models.order_table import OrderOffersModel
        from src.auth.schemas.schemas import OrderOfferSchema

        def auto_cancel_ofert(order_ofert):
            TIME_OFERT_IS_VALID = 120
            time.sleep(TIME_OFERT_IS_VALID)
            if order_ofert.state == 'offered':
                order_ofert.state = 'cancelled'
                order_ofert.save()

        order_ofert_data = OrderOfferSchema().load(data)
        order_ofert_data["state"] = 'offered'
        order_ofert = OrderOffersModel(order_ofert_data)
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

    def get_delivery_current_offers(self,_id):
        from src.auth.models.order_table import OrderOffersModel
        response = OrderOffersModel.query.filter(OrderOffersModel.delivery_id == _id).filter(OrderOffersModel.state == 'offered' ).all()
        return self.sqlachemy_to_dict(response)

    def update_offer_state(self,del_id,offer_id,state):
        from src.auth.models.order_table import OrderOffersModel
        offer = OrderOffersModel.query.filter(OrderOffersModel.delivery_id == del_id).filter(OrderOffersModel.id == offer_id).one()
        if (offer.state != "offered"):
            message="Error: la oferta " + str(offer_id)
            if (offer.state == "cancelled" ):
                message = message + " ya se encuentra cancelada"
            elif (offer.state == "rejected"):
                message = message + " ya se encuentra rechazada"
            else:
                message = message + "ya se encuentra aceptada"
            raise InvalidStateChange(message)
            
        offer.state = state
        offer.save()

        if (state == "accepted"):
            OrderService().change_order_state(offer.order_id,"onWay")