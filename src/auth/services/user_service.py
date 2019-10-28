from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service
from sqlalchemy.orm import with_polymorphic

class UserService(Service):
    def create_normal_user(self, user_data):
        from src.auth.models.user_table import NormalUserModel
        user_data["password"] = self._encrypt_password(user_data["password"])
        user = NormalUserModel(user_data)
        user.save()
    
    def create_delivery_user(self, user_data):
        from src.auth.models.user_table import DeliveryUserModel
        user_data["password"] = self._encrypt_password(user_data["password"])
        user = DeliveryUserModel(user_data)
        user.save()

    def get_users(self):
        from src.auth.models.user_table import UserModel
        response = UserModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)
    
    def get_normal_users(self):
        from src.auth.models.user_table import NormalUserModel
        response = NormalUserModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)

    def get_delivery_users(self):
        from src.auth.models.user_table import DeliveryUserModel
        response = DeliveryUserModel.query.all()
        if not response:
            return []
        return self.sqlachemy_to_dict(response)


    def get_user(self,_id):
        from src.auth.models.user_table import UserModel
        return UserModel.query.get(_id)

    def delete_user(self,_id):
        from src.auth import db
        from src.auth.models.user_table import UserModel
        response = UserModel.query.filter_by(id=_id).delete()
        db.session.commit()
        return response

    def _get_userModel_email(self, email):
        from src.auth.models.user_table import UserModel
        try:
            user = UserModel.query.filter_by(email=email).one()
        except NoResultFound:
            raise NotFoundException("No user with provided email")
        except:
            raise
        else:
            return user

    def get_user_by_email(self, email):
        return self.sqlachemy_to_dict(self._get_userModel_email(email))

    def check_email(self, user_email):
        from src.auth import db
        query_emails = db.engine.execute("SELECT email from users")
        emails = []
        for email in list(query_emails):
            emails.append(email[0])
        return (user_email in emails)
        
    def change_password(self, email, new_password):
        from src.app import db
        user = self._get_userModel_email(email)
        user.password = self._encrypt_password(new_password)
        db.session.commit()

    def get_user_profile(self, email_d):
        from src.app import db
        user = self._get_userModel_email(email_d)
        print("response 1: {}".format(user))
        user = db.engine.execute("""SELECT *
                                    FROM users u
                                    LEFT OUTER JOIN normal_users nu
                                    ON u.user_id = nu.user_id
                                    LEFT OUTER JOIN delivery_users du
                                    ON u.user_id = du.user_id
                                    WHERE u.email = '{}'""".format(email_d))
        print("response 2: {}".format(user))
        return self.sqlachemy_to_dict(user)          


    @staticmethod
    def compare_password(hashed, plain):
        import hashlib
        return hashed == hashlib.md5(plain.encode('utf-8')).hexdigest()

    @staticmethod
    def _encrypt_password(password):
        import hashlib
        return hashlib.md5(password.encode('utf-8')).hexdigest()

