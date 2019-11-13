from src.app import db
from src.auth.models.base_table import BaseModel

class ProductModel(BaseModel):

  # table name
  __tablename__ = 'products'

  id = db.Column(db.Integer, primary_key=True)
  shop_id = db.Column(db.Integer, db.ForeignKey('shops.id', ondelete='CASCADE'), nullable=False)
  name = db.Column(db.String(128), nullable=False)
  description = db.Column(db.String(128), nullable=False)
  price = db.Column(db.Float, nullable=False)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.shop_id = data.get('shop_id')
    self.name = data.get('name')
    self.description = data.get('description')
    self.price = data.get('price')
