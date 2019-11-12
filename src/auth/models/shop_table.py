import datetime
from src.app import db
from src.auth.auth_exception import NotFoundException
from src.auth.models.base_table import BaseModel

class ShopModel(BaseModel):

  # table name
  __tablename__ = 'shops'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  address = db.Column(db.String(128), nullable=False)
  description = db.Column(db.String(128), nullable=True)
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
    self.description = data.get('description', '')
    self.latitude = data.get('latitude')
    self.longitude = data.get('longitude')
    self.photoUrl = data.get('photoUrl')
    self.rating = data.get('rating')


  @staticmethod
  def get_shop(shop_id):
    response = ShopModel.query.get(shop_id)
    if not response:
        raise NotFoundException("Invalid ID")
    return response