import datetime
from src.app import db

class UserModel(db.Model):

  # table name
  __tablename__ = 'users'

  user_id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  phone_number = db.Column(db.Integer, nullable=False)
  role = db.Column(db.String(128), nullable=False)
  password = db.Column(db.String(128), nullable=False)
  firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
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
    self.firebase_uid = data.get('firebase_uid')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def get_one_user(id):
    return UserModel.query.get(id)


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


class DeliveryUserModel(UserModel):

  # table name
  __tablename__ = 'delivery_users'

  user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), primary_key=True)
  balance = db.Column(db.Integer, nullable=False)
  picture = db.Column(db.String(128), nullable=False)

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