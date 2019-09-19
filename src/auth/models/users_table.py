import datetime
from src.app import db

class UserModel(db.Model):
  # table name
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  first_name = db.Column(db.String(128), nullable=False)
  last_name = db.Column(db.String(128), nullable=False)
  password = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), nullable=False)
  phone_number = db.Column(db.Integer, nullable=False)
  picture_uri = db.Column(db.String(128), nullable=True)
  created_at = db.Column(db.DateTime, nullable=False)
  last_login = db.Column(db.DateTime, nullable=False)
  token = db.Column(db.String(128), nullable=True)
  reputation = db.Column(db.Integer, nullable=True)
  gratitude_points = db.Column(db.Integer, nullable=True)
  modified_at = db.Column(db.DateTime)
  #falta suscription = 

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.id = data.get('id')
    self.first_name = data.get('first_name')
    self.last_name = data.get('last_name')
    self.password = data.get('password')
    self.email = data.get('email')
    self.phone_number = data.get('phone_number')
    self.picture_uri = data.get('picture_uri')
    self.created_at = datetime.datetime.utcnow()
    self.last_login = datetime.datetime.utcnow()
    self.token = data.get('token')
    self.reputation = data.get('reputation')
    self.gratitude_points = data.get('gratitude_points')
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def get_one_user(id):
    return UserModel.query.get(id)