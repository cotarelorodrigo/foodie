from flask_sqlalchemy import SQLAlchemy

class Service:
    
    def sqlachemy_to_dict(self, response):
        try:
            response = [p.__dict__ for p in response]
            for object_sql in response: object_sql.pop("_sa_instance_state")
        except TypeError:
            response = response.__dict__
            response.pop("_sa_instance_state")
        #except AttributeError:
            #response = [dict(zip(response.keys(), row)) for row in response.fetchall()]
        finally:
            return response

    @staticmethod
    def compare_password(hashed, plain):
        import hashlib
        return hashed == hashlib.md5(plain.encode('utf-8')).hexdigest()

    @staticmethod
    def _encrypt_password(password):
        import hashlib
        return hashlib.md5(password.encode('utf-8')).hexdigest()