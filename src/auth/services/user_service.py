class UserService:
    def create_user(self, user_data):
        from src.auth.models.user_table import UserModel
        user = UserModel(user_data)
        user.save()

    def get_users(self):
        from src.auth.models.user_table import UserModel
        return UserModel.query.all()

    def get_user(self,_id):
        from src.auth.models.user_table import UserModel
        return UserModel.query.get(_id)

    def check_email(self, user_email):
        from src.app import db
        query_emails = db.engine.execute("SELECT email from users")
        emails = []
        for email in list(query_emails):
            emails.append(email[0])
        return (user_email in emails)
