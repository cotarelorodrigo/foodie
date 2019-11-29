import datetime
from src.app import db
from src.auth.auth_exception import NotFoundException
from src.auth.models.base_table import BaseModel
from src.auth.models.user_table import DeliveryUserModel
import time
class OrderModel(BaseModel):

  # table name
  __tablename__ = 'orders'

  order_id = db.Column(db.Integer, primary_key=True)
  shop_id = db.Column(db.Integer, nullable=False)
  products = db.relationship('OrderProductsModel', backref='order', lazy=True)
  latitud = db.Column(db.Float, nullable=False)
  longitud = db.Column(db.Float, nullable=False)
  payWithPoints = db.Column(db.Boolean, nullable=False)
  favourPoints = db.Column(db.Integer, nullable=False)
  state = db.Column(db.String(128), nullable=False)
  price = db.Column(db.Float,nullable = False)
  deliver_price = db.Column(db.Float)
  delivery_pay = db.Column(db.Float)
  user_id = db.Column(db.Integer, db.ForeignKey('normal_users.user_id'), nullable=False)
  delivery_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)
  delivery_review = db.Column(db.Float, nullable = True)
  shop_review = db.Column(db.Float, nullable = True)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.shop_id = data.get('shop_id')
    self.latitud = data.get('latitude')
    self.longitud = data.get('longitude')
    self.payWithPoints = data.get('payWithPoints')
    self.favourPoints = data.get('favourPoints', 0)
    self.state = data.get('state')
    self.user_id = data.get('user_id')
    self.delivery_id = data.get('delivery_id', None)
    self.price = data.get("price")
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()
    self.delivery_review = None
    self.shop_review = None 
    
class OrderProductsModel(BaseModel):

  # table name
  __tablename__ = 'order_products'

  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
  product_id = db.Column(db.Integer, nullable=False)
  units = db.Column(db.Integer, nullable=False)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.product_id = data.get('product_id')
    self.units = data.get('units')

  
class OrderOffersModel(BaseModel):

  # table name
  __tablename__ = 'order_oferts'

  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
  delivery_id = db.Column(db.Integer, db.ForeignKey('delivery_users.user_id', ondelete='CASCADE'), nullable=False)
  delivery_price = db.Column(db.Float,nullable=False)
  delivery_pay = db.Column(db.Float,nullable = False)
  created_at = db.Column(db.DateTime)
  created_at_seconds = db.Column(db.Integer)
  state = db.Column(db.String(128), nullable=False)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.order_id = data.get("order_id")
    self.delivery_id = data.get('delivery_id')
    self.delivery_price = data.get('delivery_price')
    self.delivery_pay = data.get('delivery_pay')
    self.created_at = datetime.datetime.utcnow()
    self.created_at_seconds = int(round(time.time()))
    self.state = data.get('state')

  @staticmethod
  def get_offer(offer_id):
    response = OrderOffersModel.query.get(offer_id)
    if not response:
        raise NotFoundException("Invalid ID")
    return response

class FavourOfferModel(BaseModel):
  __tablename__='favour_offers'

  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
  # usuario que entrega el pedido
  user_id = db.Column(db.Integer, db.ForeignKey('normal_users.user_id', ondelete='CASCADE'), nullable=False)
  points = db.Column(db.Integer,nullable = False)
  created_at = db.Column(db.DateTime)
  created_at_seconds = db.Column(db.Integer)
  state = db.Column(db.String(128), nullable=False)

    # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.order_id = data.get("order_id")
    self.user_id = data.get('user_id')
    self.points = data.get('points')
    self.created_at = datetime.datetime.utcnow()
    self.created_at_seconds = int(round(time.time()))
    self.state = data.get('state')

  @staticmethod
  def get_offer(offer_id):
    response = FavourOfferModel.query.get(offer_id)
    if not response:
        raise NotFoundException("Invalid ID")
    return response