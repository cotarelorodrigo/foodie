import datetime
from src.app import db

class ShopModel(db.Model):

  # table name
  __tablename__ = 'shops'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  address = db.Column(db.String(128), nullable=False)
  description = db.Column(db.String(128), nullable=False)
  photoUrl = db.Column(db.String(128), nullable=False)
  rating = db.Column(db.Integer, nullable=False)


  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.id = data.get('id')
    self.name = data.get('name')
    self.address = data.get('address')
    self.description = data.get('description')
    self.photoUrl = data.get('photoUrl')
    self.rating = data.get('rating')

  def save(self):
    db.session.add(self)
    db.session.commit()
