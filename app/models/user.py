import datetime

users = []


class User:
    """
    class for users
    """

    def __init__(self, **kwargs):
        self.user_id = len(users)+1
        self.first_name = kwargs.get("first_name")
        self.last_name = kwargs.get("last_name")
        self.other_names = kwargs.get("other_names")
        self.email = kwargs.get("email")
        self.telephone = kwargs.get("telephone")
        self.user_name = kwargs.get("user_name")
        self.password = kwargs.get("password")
        self.registered = datetime.datetime.now()
        self.isadmin = False

    def user_to_json(self):
        """\
        method to turn user to dictionary
        """
        return {
            "user_id": self.user_id,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Other Names": self.other_names,
            "Email": self.email,
            "Telephone": self.telephone,
            "user_name": self.user_name,
            "password": self.password,
            "Registered": self.registered,
            "Is Admin": self.isadmin

        }

    @staticmethod
    def create(user):
        """\
        creates user
        """
        new_user = user.user_to_json()
        users.append(new_user)
        return new_user

    @staticmethod
    def get_all_users():
        """\
        returns all users
        """
        return users

    @staticmethod
    def login(user_name, password):
        """\
        logs in user
        """
        for user in users:
            if user["user_name"] == user_name and user["password"] == password:
                return user
            return None

    @staticmethod
    def check_user_exists(user_name, password):
        """
        checks if user exists
        """
        for user in users:
            if user["user_name"] == user_name:
                return "user with username already exists"
            elif user["password"] == password:
                return "user with password already exists"
            return False
