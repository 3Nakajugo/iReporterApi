import re


class Validator:

    """
    validates incident
    """

    def validate_incident(self, file, comment):
        """
        validates create incident
        """
        if not file:
            return "An image is missing"
        if not comment or comment.isspace():
            return"comment is missing"

    def validate_new_comment(self, comment):
        if not comment or comment.isspace():
            return"comment is missing"

    def validate_login(self, user_name, password):
        """
        validates login user
        """
        if not user_name or user_name.isspace():
            return "username Cannot be empty"
        if not password or password.isspace():
            return "password cannot be empty"

    def validate_location(self, location):
        """
        validates edit location
        """
        if not location or location.isspace():
            return "location is missing"

    def edit_comment(self, comment):
        """
        validates edit comment
        """
        if not comment:
            return "comment is missing"
        if comment.isspace():
            return "comment must not be empty"

    def validate_user_credentials(self, password, user_name, telephone):
        """
        validates create user
        """
        if not user_name or user_name.isspace():
            return "username is missing"
        if not telephone:
            return "please input telephone"
        if not telephone.isdigit():
            return "phone number should be intergers"
        if not user_name.isalpha():
            return "username should contain no spaces"
        if len(telephone) is not 10:
            return "Phone number must be 10 characters"
        if len(user_name) < 5:
            return "username must be longer than 5 characters"

    def validate_password(self, password):
        if not password or password.isspace():
            return "password is missing"
        if not re.match(r'[A-Za-z0-9@#$%^&+=]{8,}', password):
            return "password must be longer than 8 characters and cannot contain an underscore"
        if re.search(r'\s', password):
            return "password should not contain spaces"

    def validate_email(self, email):
        """
        validates email
        """
        if not email or email.isspace():
            return "please input email"
        valid_email = re.compile(
            r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-z]+$)")
        if not valid_email.match(email):
            return "please input valid email"

    def validate_names(self, first_name, last_name):
        """ 
        validates names
        """
        if not first_name:
            return "first_name is missing"
        if not last_name:
            return "last_name is missing"
        if not first_name.isalpha():
            return "firstname should not contain spaces or special characters"
        if not last_name.isalpha():
            return "last_name should not contain spaces or special characters"
        if len(first_name) > 15 or len(last_name) > 15:
            return "names must not exceed 15 characters"

    def validate_isadmin(self, isadmin):
        """
        validates role
        """
        if not isadmin:
            return "role is missing"
        if isadmin.isspace():
            return "role cannot be  empty"
        if isadmin not in ["True", "False"]:
            return "role should be True or False"

    def validate_status(self, status):
        if not status or status.isspace():
            return "status is missing"
        if status not in ["rejected","resolved","under investigation"]:
            return "status should be resolved,rejected or under investigation"
