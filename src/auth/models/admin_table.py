import datetime
from src.app import db
from src.auth.models.base_table import BaseModel

class AdminModel(BaseModel):

  # table name
  __tablename__ = 'admins'

  admin_id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(128), nullable=False, unique=True)
  password = db.Column(db.String(128), nullable=False)
  last_login = db.Column(db.DateTime)

  # class constructor
  def __init__(self, data):
    """
    Class constructor
    """
    self.email = data.get('email')
    self.password = data.get('password')
    self.last_login = datetime.datetime.utcnow()