from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import UserNotFoundException

class UserService:
    def create_user(self, user_data):
        from src.auth.models.user_table import UserModel
        user_data["password"] = self._encrypt_password(user_data["password"])
        user = UserModel(user_data)
        user.save()

    def get_users(self):
        from src.auth.models.user_table import UserModel
        return UserModel.query.all()

    def get_user(self,_id):
        from src.auth.models.user_table import UserModel
        return UserModel.query.get(_id)

    def delete_user(self,_id):
        from src.app import db
        from src.auth.models.user_table import UserModel
        response = UserModel.query.filter_by(id=_id).delete()
        db.session.commit()
        return response

    def get_user_by_email(self,value):
        from src.app import db
        from src.auth.models.user_table import UserModel
        try:
            response = UserModel.query.filter_by(email=value).one().__dict__
        except NoResultFound:
            raise UserNotFoundException("No user with provided email")
        response.pop("_sa_instance_state")
        return response 

    def check_email(self, user_email):
        from src.app import db
        query_emails = db.engine.execute("SELECT email from users")
        emails = []
        for email in list(query_emails):
            emails.append(email[0])
        return (user_email in emails)

    @staticmethod
    def compare_password(hashed, plain):
        import hashlib
        return hashed == hashlib.md5(plain.encode('utf-8')).hexdigest()

    @staticmethod
    def _encrypt_password(password):
        import hashlib
        return hashlib.md5(password.encode('utf-8')).hexdigest()

