from ..models import User, users


class UserController:

    def create_user(self, user):
        new_user = user.user_to_json()
        users.append(new_user)
        return users
