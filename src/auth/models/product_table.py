from src.app import db

class ProductModel(db.Model):

  # table name
  __tablename__ = 'products'

  id = db.Column(db.Integer, primary_key=True)
  shop_id = db.Column(db.Integer, db.ForeignKey('shops.shop_id', ondelete='CASCADE'), nullable=False)
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
    
  def save(self):
    db.session.add(self)
    db.session.commit()
