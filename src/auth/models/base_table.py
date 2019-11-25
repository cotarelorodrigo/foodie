from src.app import db
from src.auth.auth_exception import NotFoundException

class BaseModel(db.Model):
    __abstract__ = True #Which means SQLAlchemy will not create a table for that model (BaseModel)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return True

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return True

    def update(self, data):
        for key, value in data.items():
            setattr(self, key, value)
        db.session.commit()
        return True

    @classmethod 
    def get_instance(cls, id):
        response = cls.query.get(id)
        if not response:
            raise NotFoundException("Invalid ID")
        return response