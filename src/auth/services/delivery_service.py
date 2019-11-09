from geopy.distance import distance
from src.auth.services.delivery_rules import Delivery
from datetime import datetime

class DeliveryService:

    def get_distance(self,lat_1,long_1,lat_2,long_2):
        return distance((lat_1,long_1),(lat_2,long_2)).km

    def get_delivery_price(self,client,delivery,shop,client_lat,client_long):
        distance = self.get_distance(shop["latitude"],shop["longitude"],client_lat,client_long)
        delivery = Delivery(distance,datetime.now(),1,20)
        price = delivery.calculate_price()
        return price

    def get_quantity_deliverys(self):
        from src.auth.models.user_table import DeliveryUserModel
        return DeliveryUserModel.query.count()