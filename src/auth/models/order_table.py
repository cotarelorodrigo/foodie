import datetime
from src.app import db

class OrderModel(db.Model):

  # table name
  __tablename__ = 'orders'

  id = db.Column(db.Integer, primary_key=True)
  shop_id = db.Column(db.Integer, nullable=False)
  item = db.Column(db.Integer, nullable=False)
  cantidad = db.Column(db.Integer, nullable=False)
  latitud = db.Column(db.Float, nullable=False)
  longitud = db.Column(db.Float, nullable=False)
  #payWithPoints = db.Column(db.Boolean, nullable=False)


  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.shop_id = data.get('shop_id')
    self.item = data.get('item')
    self.cantidad = data.get('cantidad')
    self.latitud = data.get('latitud')
    self.longitud = data.get('longitud')
    #self.payWithPoints = data.get('payWithPoints')

  def save(self):
    db.session.add(self)
    db.session.commit()