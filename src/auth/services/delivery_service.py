from geopy.distance import distance
from src.auth.services.delivery_rules import Delivery
from src.auth.services.service import Service
from src.auth.services.order_service import OrderService
from src.auth.services.user_service import UserService
import datetime
from dateutil import relativedelta

class DeliveryService(Service):

    def create_delivery_user(self, user_data):
        from src.auth.models.user_table import DeliveryUserModel
        user_data["password"] = self._encrypt_password(user_data["password"])
        user = DeliveryUserModel(user_data)
        user.save()

    def get_delivery(self, _id):
        from src.auth.models.user_table import DeliveryUserModel
        response = DeliveryUserModel.get_delivery(_id)
        return self.sqlachemy_to_dict(response)

    def delete_delivery(self, _id):
        from src.auth.models.user_table import DeliveryUserModel
        return DeliveryUserModel.get_delivery(_id).delete()

    def update_delivery(self, _id, data):
        from src.auth.models.user_table import DeliveryUserModel
        from src.auth.schemas.schemas import DeliveryUserSchema
        delivery_data = DeliveryUserSchema().load(data)
        return DeliveryUserModel.get_delivery(_id).update(delivery_data)

    def get_N_deliverys(self, pageNumber, pageSize):
        from src.auth.models.user_table import DeliveryUserModel
        query = DeliveryUserModel.query.offset(pageNumber*pageSize).limit(pageSize)
        response = {}
        response['items'] = self.sqlachemy_to_dict(query.all())
        response['totalItems'] = query.count()
        return response
    
    def refresh_delivery_is_online(self):
        from src.auth.models.user_table import DeliveryUserModel
        deliveries = DeliveryUserModel.query.all()
        #for d in deliveries:
            #d.state =  
            #d.save()

    def get_available_deliverys(self):
        from src.auth.models.user_table import DeliveryUserModel
        deliverys = DeliveryUserModel.query.filter_by(state = 'free').all()
        return self.sqlachemy_to_dict(deliverys)

    def get_distance(self,lat_1,long_1,lat_2,long_2):
        return distance((lat_1,long_1),(lat_2,long_2)).km

    def get_delivery_price_and_pay(self,client,delivery,shop,client_lat,client_long):
        distance = self.get_distance(shop["latitude"],shop["longitude"],client_lat,client_long)
        order_service = OrderService()
        user_service = UserService()
        subscription = user_service.get_user(client)["suscripcion"]
        delivery = Delivery(distance,datetime.datetime.now(),order_service.get_historical_user_orders(client),order_service.get_today_delivery_orders(delivery),premium= subscription == "premium")
        price = delivery.calculate_price()
        pay = delivery.calculate_delivery_pay()
        return price, pay

    def get_quantity_deliverys(self):
        from src.auth.models.user_table import DeliveryUserModel
        return DeliveryUserModel.query.count()

    def get_quantity_deliverys_date(self, date_from, date_to):
        from src.auth.models.user_table import DeliveryUserModel
        return DeliveryUserModel.query.filter(DeliveryUserModel.created_at >= date_from).filter(DeliveryUserModel.created_at <= date_to).count()

    def get_quantity_deliverys_by_month(self, year_from, month_from, year_to, month_to):
        date_from = datetime.date(year=year_from,month=month_from, day=1)
        date_to = datetime.date(year=year_to,month=month_to, day=1)
        result = []
        delta = relativedelta.relativedelta(date_from, date_to)
        for delta_month in range(abs(delta.months)):
            date_from_aux = date_from + relativedelta.relativedelta(months=delta_month)
            date_to_aux = date_from + relativedelta.relativedelta(months=delta_month+1)
            result.append({"year": date_to_aux.year, "month": date_to_aux.month, "amount": self.get_quantity_deliverys_date(date_from_aux, date_to_aux)})
        return result