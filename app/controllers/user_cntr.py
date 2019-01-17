from ..models import User, users


class UserController:

    def create_user(self, user):
        new_user = user.user_to_json()
        users.append(new_user)
        return new_user

    def get_all_users(self):
        return users

    def check_user_exists(self, user_name):
        for user in users:
            if user["user_name"] == user_name:
                return True
