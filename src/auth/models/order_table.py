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


  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.shop_id = data.get('shop_id')
    self.latitud = data.get('latitud')
    self.longitud = data.get('longitud')
    self.payWithPoints = data.get('payWithPoints')

  def save(self):
    db.session.add(self)
    db.session.commit()