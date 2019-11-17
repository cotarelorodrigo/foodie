import datetime
import secrets
from src.auth.auth_exception import NotFoundException
from src.app import db
from src.auth.models.base_table import BaseModel

class UserModel(BaseModel):

  # table name
  __tablename__ = 'users'

  user_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  phone_number = db.Column(db.Integer, nullable=False)
  role = db.Column(db.String(128), nullable=False)
  password = db.Column(db.String(128), nullable=True)
  latitude = db.Column(db.Float, nullable=True)
  longitude = db.Column(db.Float, nullable=True)
  firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
  favourPoints = db.Column(db.Integer, nullable=False)
  token = db.Column(db.String(128), unique=True, nullable=False)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  __mapper_args__ = {
    'polymorphic_identity':'users'
  }

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('name')
    self.email = data.get('email')
    self.phone_number = data.get('phone_number')
    self.role = data.get('role')
    self.password = data.get('password')
    self.latitude = data.get("latitude", None)
    self.longitude = data.get("longitude", None)
    self.firebase_uid = data.get('firebase_uid')
    self.favourPoints = data.get("favourPoints", 30)
    self.token = secrets.token_hex(32)
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  @staticmethod
  def get_any_user(user_id):
    response = UserModel.query.get(user_id)
    if not response:
        raise NotFoundException("Invalid ID")
    return response

class NormalUserModel(UserModel):

  # table name
  __tablename__ = 'normal_users'

  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
  suscripcion = db.Column(db.String(128), nullable=False)
  picture = db.Column(db.String(128), nullable=True)

  __mapper_args__ = {
    'polymorphic_identity':'normal_users',
  }

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    super(NormalUserModel, self).__init__(data)
    self.suscripcion = data.get('suscripcion')
    self.picture = data.get('picture')

  @staticmethod
  def get_user(user_id):
    response = NormalUserModel.query.get(user_id)
    if not response:
        raise NotFoundException("Invalid ID")
    return response


class DeliveryUserModel(UserModel):

  # table name
  __tablename__ = 'delivery_users'

  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
  balance = db.Column(db.Integer, nullable=False)
  picture = db.Column(db.String(128), nullable=False)
  rating = db.Column(db.Float,nullable=False)
  reviews = db.Column(db.Integer,nullable=False)
  state = db.Column(db.String(128), nullable=False)

  __mapper_args__ = {
    'polymorphic_identity':'delivery_users',
  }

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    super(DeliveryUserModel, self).__init__(data)
    self.balance = data.get('balance')
    self.picture = data.get('picture')
    self.rating = 0.0
    self.reviews = 0
    self.state = data.get('state', 'free')


  @staticmethod
  def get_delivery(user_id):
    response = DeliveryUserModel.query.get(user_id)
    if not response:
        raise NotFoundException("Invalid ID")
    return response