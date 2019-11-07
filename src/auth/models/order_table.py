import datetime
from src.app import db
#from src.auth.models.order_product_table import OrderProductsModel

class OrderModel(db.Model):

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

  def save(self):
    db.session.add(self)
    db.session.commit()