import datetime
from src.app import db

class AdminModel(db.Model):

  # table name
  __tablename__ = 'admins'

  admin_id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(128), nullable=False, unique=True)
  password = db.Column(db.String(128), nullable=False)
  last_login = db.Column(db.DateTime)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.username = data.get('username')
    self.password = data.get('password')
    self.last_login = datetime.datetime.utcnow()

  def save(self):
    db.session.add(self)
    db.session.commit()