import re


class Validator:

    """
    validates incident
    """

    def validate_incident(self, location, file, comment):
        """
        validates create incident
        """
        if not (isinstance(location, int)):
            return "location must be an integer of less then 9 integers"
        if not location:
            return "location is missing"
        if not file or file.isspace():
            return "An image or video is missing"
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

    def validate_user_credentials(self, email, password, user_name, telephone):
        """
        validates create user
        """
        if not user_name or user_name.isspace():
            return "username is missing"
        if not password or password.isspace():
            return "password is missing"
        if not email or email.isspace():
            return "please input email"
        if not telephone or telephone.isspace():
            return "please input telephone"
        if not telephone.isdigit():
            return "phone number should be intergers"
        if len(telephone) is not 10:
            return "Phone number must be longer than 10 characters"
        if len(user_name) < 5:
            return "username must be longer than 5 characters"
        if len(password) < 8:
            return "password must be longer than 8 characters"

    def validate_email(self, email):
        valid_email = re.compile(
            r"(^[a-zA-Z0-9_.]+@[a-zA-Z0-9]+\.[a-z]+$)")
        if not valid_email.match(email):
            return "please input valid email"

    def validate_names(self, first_name, last_name, other_names):
        if not first_name:
            return "first_name is missing"
        if not last_name:
            return "last_name is missing"
        if not other_names:
            return "other_name is missing"
        if not first_name.isalpha():
            return "firstname should be alphabetical characters"
        if not last_name.isalpha():
            return "last_name should be alphabetical characters"
        if not other_names.isalpha():
            return "other_name should be alphabetical characters"
        if len(first_name) > 15 or len(last_name) > 15 or len(other_names) > 15:
            return "names must not exceed 15 characters"
    
  
