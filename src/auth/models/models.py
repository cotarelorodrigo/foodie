import datetime

class UserModel(db.Model):
  from src.app import db

  # table name
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False)
  email = db.Column(db.String(128), unique=True, nullable=False)
  password = db.Column(db.String(128), nullable=False)
  signup_datetime = db.Column(db.DateTime, nullable=False)
  firebase_uid = db.Column(db.String(128), unique=True, nullable=False)
  picture = db.Column(db.String(128), nullable=True)
  created_at = db.Column(db.DateTime)
  modified_at = db.Column(db.DateTime)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.name = data.get('fullName')
    self.email = data.get('email')
    self.password = data.get('password')
    self.signup_datetime = data.get('signUpDate')
    self.firebase_uid = data.get('firebaseUid')
    self.picture = data.get('picture')
    self.created_at = datetime.datetime.utcnow()
    self.modified_at = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()

  @staticmethod
  def get_one_user(id):
    return UserModel.query.get(id)