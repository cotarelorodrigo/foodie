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

    def get_normal_user(self,_id):
        from src.auth.models.user_table import NormalUserModel
        user = NormalUserModel.get_user(_id)
        return self.sqlachemy_to_dict(user)

    def get_user(self, _id):
        from src.auth.models.user_table import UserModel
        response = UserModel.get_any_user(_id)
        return self.sqlachemy_to_dict(response)

    def delete_user(self, _id):
        from src.auth.models.user_table import NormalUserModel
        return NormalUserModel.get_user(_id).delete()

    def update_user(self, _id, data):
        from src.auth.models.user_table import NormalUserModel
        from src.auth.schemas.schemas import NormalUserSchema
        user_data = NormalUserSchema().load(data)
        return NormalUserModel.get_user(_id).update(user_data)
    
    def update_coordinates(self, _id, coordinates):
        from src.auth.schemas.schemas import CoordinateSchema
        from src.auth.models.user_table import UserModel
        data = CoordinateSchema().load(coordinates)
        user = UserModel.get_any_user(_id)
        user.latitude = data["latitude"]
        user.longitude = data["longitude"]
        user.save()

    def get_N_users(self, pageNumber, pageSize):
        from src.auth.models.user_table import NormalUserModel
        query = NormalUserModel.query.offset(pageNumber*pageSize).limit(pageSize)
        response = {}
        response['items'] = self.sqlachemy_to_dict(query.all())
        response['totalItems'] = query.count()
        return response    

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

