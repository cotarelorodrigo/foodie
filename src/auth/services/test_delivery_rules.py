from unittest import TestCase
from src.auth.services.delivery_rules import Delivery
import datetime

class DeliveryRulesTest(TestCase):

    def test_calculate_price(self):
        distance = 10
        dt = datetime.datetime(2019,11,13,18)
        user_previous_orders = 6
        delivery_orders_today = 0
        d = Delivery(distance,dt,user_previous_orders,delivery_orders_today)
        self.assertEqual(d.calculate_price(),147)

    def test_calculate_price(self):			
        dt = datetime.datetime(2019,11,13,18)
        delivery_orders_today = 20
        base_price = 85
        d = Delivery(None,dt,None,delivery_orders_today)
        self.assertEqual(d.calculate_delivery_pay(base_price),89.25)