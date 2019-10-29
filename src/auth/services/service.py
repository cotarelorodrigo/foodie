from flask_sqlalchemy import SQLAlchemy

class Service:
    
    def sqlachemy_to_dict(self, response):
        try:
            response = [p.__dict__ for p in response]
            for object_sql in response: object_sql.pop("_sa_instance_state")
        except TypeError:
            response = response.__dict__
            response.pop("_sa_instance_state")
        except AttributeError:
            print('error')
            print(type(response))
            print(response)
            print('++++++++++++++++++++')

            #response = [dict(zip(response.keys(), row)) for row in response.fetchall()]
        finally:
            return response