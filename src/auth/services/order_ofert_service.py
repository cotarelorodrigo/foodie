from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException,InvalidStateChange, NotEnoughFavourPoints
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
        return order_ofert.id

    def create_favour_offer(self,data):
        from src.auth.schemas.schemas import FavourOfferSchema
        from src.auth.models.order_table import FavourOfferModel
        from src.auth.services.user_service import UserService
        def auto_cancel_offer(offer):
            TIME_OFERT_IS_VALID = 120
            time.sleep(TIME_OFERT_IS_VALID)
            if offer.state == 'offered':
                offer.state = 'cancelled'
                offer.save()        

        service = OrderService()
        user_service = UserService()
        order = service.get_order_by_id(data["order_id"])
        user = user_service.get_normal_user(order['user_id'])

        if not user_service.user_order_by_favour(int(order['user_id']), int(data["points"])):
            raise NotEnoughFavourPoints("Favour points insuficientes")
    
        favour_offer_data = FavourOfferSchema().load(data)
        favour_offer_data["state"] = 'offered'
        favour_offer = FavourOfferModel(favour_offer_data)
        favour_offer.save()
        Process(target=auto_cancel_offer,args=(favour_offer,)).start()
        return favour_offer.id

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

    def get_favour_offer_by_id(self,_id):
        from src.auth.models.order_table import FavourOfferModel
        response = FavourOfferModel.get_offer(_id)
        return self.sqlalchemy_to_dict(response)

    def get_delivery_current_offers(self,_id):
        from src.auth.models.order_table import OrderOffersModel
        response = OrderOffersModel.query.filter(OrderOffersModel.delivery_id == _id).filter(OrderOffersModel.state == 'offered' ).all()
        return self.sqlachemy_to_dict(response)

    def update_offer_state(self,del_id,offer_id,state):
        from src.auth.models.order_table import OrderOffersModel
        offer = OrderOffersModel.query.filter(OrderOffersModel.delivery_id == del_id).filter(OrderOffersModel.id == offer_id).one()
        offer_info = self.sqlachemy_to_dict(offer)        
        if (offer.state != "offered"):
            message="Error: la oferta " + str(offer_id)
            if (offer.state == "cancelled" ):
                message = message + " ya se encuentra cancelada"
            elif (offer.state == "rejected"):
                message = message + " ya se encuentra rechazada"
            else:
                message = message + "ya se encuentra aceptada"
            raise InvalidStateChange(message)
        if (state == "accepted"):
            now = int(round(time.time()))
            if ( now >= (offer_info["created_at_seconds"] + 120)):
                offer.state = "cancelled"
                offer.save()
                raise InvalidStateChange("Error: el tiempo de validez de la oferta ha terminado")
            else:
                OrderService().catch_order(offer.order_id, offer.delivery_id, offer_info)
        offer.state = state
        offer.save()

    def update_favour_offer_state(self,user_id,offer_id,state):
        from src.auth.models.order_table import FavourOfferModel
        offer = FavourOfferModel.query.filter(FavourOfferModel.user_id == user_id).filter(FavourOfferModel.id == offer_id).one()
        offer_info = self.sqlachemy_to_dict(offer)
        if (offer.state != "offered"):
            message="Error: la oferta " + str(offer_id)
            if (offer.state == "cancelled" ):
                message = message + " ya se encuentra cancelada"
            elif (offer.state == "rejected"):
                message = message + " ya se encuentra rechazada"
            else:
                message = message + "ya se encuentra aceptada"
            raise InvalidStateChange(message)
        if (state == "accepted" ):
            now = int(round(time.time()))
            if ( now >= (offer_info["created_at_seconds"] + 120)):
                offer.state = "cancelled"
                offer.save()
                raise InvalidStateChange("Error: el tiempo de validez de la oferta ha terminado")
            else:
                OrderService().catch_order(offer.order_id, offer.user_id, offer_info)
        offer.state = state
        offer.save()