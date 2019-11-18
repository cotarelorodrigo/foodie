from src.app import db

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
        self.__init__(data)
        db.session.commit()
        return True

    @staticmethod
    def get_instance(id):
        response = UserModel.query.get(id)
        if not response:
            raise NotFoundException("Invalid ID")
        return response