from sqlalchemy.orm.exc import NoResultFound
from src.auth.auth_exception import NotFoundException
from src.auth.services.service import Service
import datetime
from dateutil import relativedelta

class UserService(Service):
    def create_normal_user(self, user_data):
        from src.auth.models.user_table import NormalUserModel
        try:
            user_data["password"] = self._encrypt_password(user_data["password"])
        except KeyError:
            pass
        user = NormalUserModel(user_data)
        user.save()
        return user

    def get_normal_user(self, _id, dict_format=False):
        from src.auth.models.user_table import NormalUserModel
        user = NormalUserModel.get_instance(_id)
        if dict_format:
            return self.sqlachemy_to_dict(user)
        return user

    def get_delivery_user(self,_id, dict_format=False):
        from src.auth.models.user_table import DeliveryUserModel
        user = DeliveryUserModel.get_instance(_id)
        if dict_format:
            return self.sqlachemy_to_dict(user)
        return user

    def get_user(self, _id, dict_format=False):
        from src.auth.models.user_table import UserModel
        user = UserModel.get_instance(_id)
        if dict_format:
            return self.sqlachemy_to_dict(user)
        return user

    def delete_user(self, _id):
        from src.auth.models.user_table import NormalUserModel
        return NormalUserModel.get_user(_id).delete()

    def update_user(self, _id, data):
        try:
            user = self.get_normal_user(_id)
        except Exception:
            user = self.get_delivery_user(_id)
        except Exception:
            user = None
        finally:
            if not user:
                raise NotFoundException("El user id que se quiere actualziar es invalido")
            user_data = self.get_user(_id, dict_format=True)
            user_data.update(data)
            assert user.update(user_data) == True
    
    def update_coordinates(self, _id, coordinates):
        from src.auth.schemas.schemas import CoordinateSchema
        data = CoordinateSchema().load(coordinates)
        user = self.get_user(_id)
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

    def user_order_by_favour(self, user_id, points_for_favour):
        from src.auth.models.user_table import NormalUserModel
        try:
            user = self.get_user(user_id)
        except NotFoundException:
            raise NotFoundException("ID invalido: Solo los usuarios comunes pueden solicitar favores")
        return (user.favourPoints >= points_for_favour)

    def get_available_users_favours(self):
        from src.auth.models.user_table import NormalUserModel, UserModel
        time = datetime.datetime.now() - datetime.timedelta(hours=2)
        users = NormalUserModel.query.filter_by(make_favours = True).filter(UserModel.last_login >= time).all()
        return self.sqlachemy_to_dict(users)

    def get_user_by_email(self, email):
        return self.sqlachemy_to_dict(self._get_userModel_email(email))

    def get_user_by_uid(self,uid):
        from src.auth.models.user_table import UserModel
        user = UserModel.query.filter_by(firebase_uid=uid).one()
        return self.sqlachemy_to_dict(user)

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

    def update_user_login(self, email):
        user = self._get_userModel_email(email)
        user.last_login = datetime.datetime.utcnow()
        user.save()

    def user_start_working(self, id, _order_id):
        user = self.get_user(id)
        user.state = "working"
        user.current_order = _order_id
        user.save()

    def user_finish_working(self, id):
        user = self.get_user(id)
        user.state = "free"
        user.current_order = None
        user.save()

    def pay_order(self, user_who_pay, user_to_pay, info_order):
        from src.auth.models.user_table import UserModel,NormalUserModel,DeliveryUserModel
        user_who_pay = self.get_user(user_who_pay)
        if info_order['payWithPoints']:
            user_to_pay = self.get_normal_user(user_to_pay)
            # la quita de puntos debe hacerse cuando se acepta la orden, si no podría ofrecer 
            # simultaneamente mas puntos de los que tiene
            # user_who_pay.favourPoints -= info_order['favourPoints']
            user_to_pay.favourPoints += info_order['favourPoints']
        else:
            user_to_pay = self.get_delivery_user(user_to_pay)
            user_to_pay.balance += info_order['delivery_price']
        user_who_pay.save()
        user_to_pay.save()

    def wait_order(self, id):
        normal_user = self.get_normal_user(id)
        normal_user.state = 'waiting'
        normal_user.save()

    def receive_order(self, id):
        normal_user = self.get_normal_user(id)
        normal_user.state = 'free'
        normal_user.save()

    def get_user_favour_offers(self,_id):
        from src.auth.models.order_table import FavourOfferModel
        response = FavourOfferModel.query.filter(FavourOfferModel.user_id == _id).filter(FavourOfferModel.state == 'offered' ).all()
        return self.sqlachemy_to_dict(response)

    def put_making_favours(self,id,make_favours):
        from src.auth.models.user_table import NormalUserModel
        user =  NormalUserModel.get_instance(id)
        user.make_favours = make_favours
        user.save()
        return user