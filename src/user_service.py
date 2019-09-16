class UserService:
    def create_user(self, user_data):
        from models import UserModel
        user = UserModel(user_data)
        user.save()

    def get_users(self):
        from models import UserModel
        return UserModel.query.all()
