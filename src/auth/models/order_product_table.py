import datetime
from src.app import db


class OrderProductsModel(db.Model):

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

  def save(self):
    db.session.add(self)
    db.session.commit()