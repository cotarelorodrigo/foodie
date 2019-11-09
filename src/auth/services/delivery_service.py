from geopy.distance import distance
from src.auth.services.delivery_rules import Delivery
import datetime
from dateutil import relativedelta

class DeliveryService:

    def get_distance(self,lat_1,long_1,lat_2,long_2):
        return distance((lat_1,long_1),(lat_2,long_2)).km

    def get_delivery_price(self,client,delivery,shop,client_lat,client_long):
        distance = self.get_distance(shop["latitude"],shop["longitude"],client_lat,client_long)
        delivery = Delivery(distance,datetime.datetime.now(),1,20)
        price = delivery.calculate_price()
        return price

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