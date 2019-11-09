from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service
import datetime
from dateutil import relativedelta

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
    
    def get_quantity_users(self):
        from src.auth.models.user_table import NormalUserModel
        return NormalUserModel.query.count()

    def get_quantity_users_date(self, date_from, date_to):
        from src.auth.models.user_table import NormalUserModel
        return NormalUserModel.query.filter(NormalUserModel.created_at >= date_from).filter(NormalUserModel.created_at <= date_to).count()

    def get_quantity_users_by_month(self, year_from, month_from, year_to, month_to):
        date_from = datetime.date(year=year_from,month=month_from, day=1)
        date_to = datetime.date(year=year_to,month=month_to, day=1)
        result = []
        delta = relativedelta.relativedelta(date_from, date_to)
        for delta_month in range(abs(delta.months)):
            date_from_aux = date_from + relativedelta.relativedelta(months=delta_month)
            date_to_aux = date_from + relativedelta.relativedelta(months=delta_month+1)
            result.append({"year": date_to_aux.year, "month": date_to_aux.month, "amount": self.get_quantity_users_date(date_from_aux, date_to_aux)})
        return result


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
        response = db.engine.execute("""SELECT *
                                    FROM users u
                                    LEFT OUTER JOIN normal_users nu
                                    ON u.user_id = nu.user_id
                                    LEFT OUTER JOIN delivery_users du
                                    ON u.user_id = du.user_id
                                    WHERE u.email = '{}'""".format(email_d))
        #return self.sqlachemy_to_dict(user)
        return [dict(zip(response.keys(), row)) for row in response.fetchall()]


    @staticmethod
    def compare_password(hashed, plain):
        import hashlib
        return hashed == hashlib.md5(plain.encode('utf-8')).hexdigest()

    @staticmethod
    def _encrypt_password(password):
        import hashlib
        return hashlib.md5(password.encode('utf-8')).hexdigest()

