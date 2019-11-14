import json
from business_rules.variables import BaseVariables, string_rule_variable, numeric_rule_variable, boolean_rule_variable
from business_rules.actions import rule_action, BaseActions
from business_rules import run_all
from datetime import datetime as dt
from business_rules.fields import FIELD_NUMERIC
import os 

class DeliveryVariables(BaseVariables):

    def __init__(self, delivery):
        self.delivery = delivery

    @numeric_rule_variable
    def distance(self):
        return self.delivery.distance
    
    @numeric_rule_variable
    def day_of_week(self):
        return self.delivery.datetime.weekday()
    
    @numeric_rule_variable
    def hour(self):
        hours = self.delivery.datetime.hour
        minutes = self.delivery.datetime.minute
        seconds = self.delivery.datetime.second
        return hours + minutes/60 + seconds/3600
    
    @numeric_rule_variable
    def customer_previous_orders(self):
        return self.delivery.customer_previous_orders
    
    @numeric_rule_variable
    def delivery_orders_today(self):
        return self.delivery.delivery_orders_today

class DeliveryActions(BaseActions):

    def __init__(self, delivery):
        self.delivery = delivery

    @rule_action()
    def extra_distance_price(self):
        self.delivery.base_price = 20 + (self.delivery.distance - 2)*15
        
    @rule_action()
    def min_distance_price(self):
        self.delivery.base_price = 20
        
    @rule_action(params={"discount": FIELD_NUMERIC})
    def set_discount(self,discount):
        self.delivery.set_discount(discount)
        
    @rule_action(params={"charge": FIELD_NUMERIC})
    def set_extra_charge(self,charge):
        self.delivery.set_extra_charge(charge)

    @rule_action(params={"discount": FIELD_NUMERIC})
    def set_delivery_discount(self,discount):
        self.delivery.set_delivery_discount(discount)
        
    @rule_action(params={"amount": FIELD_NUMERIC})
    def set_delivery_raise(self,amount):
        self.delivery.set_delivery_raise(amount)

class Delivery():
    
    def __init__(self,distance,datetime,customer_previous_orders,delivery_orders_today):
        self.distance = distance
        self.datetime = datetime
        self.base_price = 0
        self.discounts = []
        self.extra_charges = []
        self.delivery_discounts = []
        self.delivery_raises = []
        self.customer_previous_orders = customer_previous_orders
        self.delivery_orders_today = delivery_orders_today
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(dir_path,"delivery_rules.json")) as f:
            d = json.load(f)
            self.user_rules = d["user"]
            self.delivery_rules = d["delivery"]
        
    def __str__(self):
        return f"""
Delivery
base_price: {self.base_price}
discounts: {self.discounts}
extra_charges: {self.extra_charges}
delivery_discounts: {self.delivery_discounts}
delivery_raises: {self.delivery_raises}
        """
        
    def set_discount(self,discount):
        self.discounts.append(discount)
        
    def set_extra_charge(self,charge):
        self.extra_charges.append(charge)

    def set_delivery_raise(self,amount):
        self.delivery_raises.append(amount)

    def set_delivery_discount(self,discount):
        self.discounts.append(discount)
        
    def get_total_discounts(self):
        total = 0
        for d in self.discounts:
            if d > 1: total += d
            else: total += d*self.base_price
        return total

    def get_delivery_discounts(self,price):
        total = 0
        for d in self.delivery_discounts:
            if d > 1: total += d
            else: total += d*price
        return total
    
    def get_total_charges(self):
        total = 0
        for c in self.extra_charges:
            if c > 1: total += c
            else: total += c*self.base_price
        return total
       
    def get_delivery_raises(self,price):
        total = 0
        for c in self.delivery_raises:
            if c > 1: total += c
            else: total += c*price
        return total

    def calculate_price(self):
        run_all(
            rule_list=self.user_rules,
            defined_actions=DeliveryActions(self),
            defined_variables=DeliveryVariables(self)
        )
        price = self.base_price - self.get_total_discounts() + self.get_total_charges()
        if price < 0: return 0
        return price

    def calculate_delivery_pay(self,price):
        run_all(
            rule_list=self.delivery_rules,
            defined_actions=DeliveryActions(self),
            defined_variables=DeliveryVariables(self)
        )
        price = price - self.get_delivery_discounts(price) + self.get_delivery_raises(price)
        if price < 0: return 0
        return price