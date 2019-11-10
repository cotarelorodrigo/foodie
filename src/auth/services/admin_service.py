from src.auth.services.service import Service
from src.auth.auth_exception import NotFoundException
from sqlalchemy.orm.exc import NoResultFound

class AdminService(Service):

    def _get_admin_by_email(self, email):
        from src.auth.models.admin_table import AdminModel
        try:
            user = AdminModel.query.filter_by(email=email).one()
        except NoResultFound:
            raise NotFoundException("No admin with provided email")
        except:
            raise
        else:
            return user

    
    def user_is_admin(self, email, password):
        try:    
            user = self._get_admin_by_email(email)
        except:
            return False
        else:
            return user.password == password