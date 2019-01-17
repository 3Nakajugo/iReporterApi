import datetime


incidents = []
users = []


class Incident:
    """class for incidents"""

    def __init__(self, created_by, incident_type, location, file, comment):
        self.incident_id = len(incidents)+1
        self.date = datetime.date.today()
        self.created_by = created_by
        self.incident_type = incident_type
        self.location = location
        self.status = "draft"
        self.file = file
        self.comment = comment

    def to_json(self):
        """ 
        method to turn incident to dictionary
        """
        return {
            "incident_id": self.incident_id,
            "date": self.date,
            "created_by": self.created_by,
            "incident_type": self.incident_type,
            "location": self.location,
            "status": self.status,
            "file": self.file,
            "comment": self.comment
        }


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
        """ 
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
