class Service:
    
    def sqlachemy_to_dict(self, response):
        try:
            response = [p.__dict__ for p in response]
            for object_sql in response: object_sql.pop("_sa_instance_state")
        except TypeError:
            response = response.__dict__
            response.pop("_sa_instance_state")
        except:
            raise
        finally:
            return response