import datetime
from src.app import db
from src.auth.models.base_table import BaseModel
from src.auth.models.user_table import DeliveryUserModel

class OrderModel(BaseModel):

  # table name
  __tablename__ = 'orders'

  order_id = db.Column(db.Integer, primary_key=True)
  shop_id = db.Column(db.Integer, nullable=False)
  products = db.relationship('OrderProductsModel', backref='order', lazy=True)
  latitud = db.Column(db.Float, nullable=False)
  longitud = db.Column(db.Float, nullable=False)
  payWithPoints = db.Column(db.Boolean, nullable=False)
  state = db.Column(db.String(128), nullable=False)
  user_id = db.Column(db.Integer, db.ForeignKey('normal_users.user_id'), nullable=False)
  delivery_id = db.Column(db.Integer, db.ForeignKey('delivery_users.user_id'), nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.shop_id = data.get('shop_id')
    self.latitud = data.get('latitude')
    self.longitud = data.get('longitude')
    self.payWithPoints = data.get('payWithPoints')
    self.state = data.get('state')
    self.user_id = data.get('user_id')
    self.delivery_id = data.get('delivery_id', None)
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()


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

  
class OrderOfertsModel(BaseModel):

  # table name
  __tablename__ = 'order_oferts'

  id = db.Column(db.Integer, primary_key=True)
  order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id', ondelete='CASCADE'), nullable=False)
  delivery_id = db.Column(db.Integer, db.ForeignKey('delivery_users.user_id', ondelete='CASCADE'), nullable=False)
  created_at = db.Column(db.DateTime)
  state = db.Column(db.String(128), nullable=False)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.order_id = data.get("order_id")
    self.delivery_id = data.get('delivery_id')
    self.created_at = datetime.datetime.utcnow()
    self.state = data.get('state')