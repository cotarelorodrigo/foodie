from flask_sqlalchemy import SQLAlchemy

class Service:
    
    def sqlachemy_to_dict(self, response):
        def without_keys(d, keys):
            return {k: v for k, v in d.items() if k not in keys}
        
        try:
            response = [p.__dict__ for p in response]
            response = [without_keys(object_sql, {'_sa_instance_state'}) for object_sql in response]
        except TypeError:
            response = response.__dict__
            response = without_keys(response, {"_sa_instance_state"})
        except:
            raise
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