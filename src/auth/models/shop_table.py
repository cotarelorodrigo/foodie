import datetime
from src.app import db

class ShopModel(db.Model):

  # table name
  __tablename__ = 'shops'

  shop_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  address = db.Column(db.String(128), nullable=False)
  descripton = db.Column(db.String(128), nullable=True)
  photoUrl = db.Column(db.String(128), nullable=False)
  rating = db.Column(db.Integer, nullable=False)
  latitude = db.Column(db.Float, nullable=False)
  longitude = db.Column(db.Float, nullable=False)
  menu = db.relationship('ProductModel', backref='order', lazy=True)


  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.address = data.get('address')
    self.descripton = data.get('descripton', '')
    self.latitude = data.get('latitude')
    self.longitude = data.get('longitude')
    self.photoUrl = data.get('photoUrl')
    self.rating = data.get('rating')

  def save(self):
    db.session.add(self)
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()