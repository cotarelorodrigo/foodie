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

    def test_calculate_pay(self):			
        dt = datetime.datetime(2019,11,13,18)
        delivery_orders_today = 20
        base_price = 100
        d = Delivery(None,dt,None,delivery_orders_today)
        d.base_price = base_price
        self.assertEqual(d.calculate_delivery_pay(),89.25)

    def test_calculate_pay_sunday_discount(self):           
        dt = datetime.datetime(2019,11,17,11)
        delivery_orders_today = 0
        base_price = 100
        d = Delivery(None,dt,None,delivery_orders_today)
        d.base_price = base_price
        self.assertEqual(d.calculate_delivery_pay(),68)

    def test_calculate_pay_free_order(self):         
        dt = datetime.datetime(2019,11,13,18)
        delivery_orders_today = 20
        user_previous_orders = 0
        distance = 1
        d = Delivery(distance,dt,user_previous_orders,delivery_orders_today)
        self.assertEqual(d.calculate_delivery_pay(),17.85)

    def test_subscription_discount(self):
        distance = 10
        dt = datetime.datetime(2019,11,16,18)
        user_previous_orders = 1
        delivery_orders_today = 0
        d = Delivery(distance,dt,user_previous_orders,delivery_orders_today,premium=True)
        self.assertEqual(d.calculate_price(),105)