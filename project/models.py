import datetime
import random


incidents = []


class Incident:
    def __init__(self, created_by, incident_type, location, file, comment):
        self.incident_id = random.randint(1, 1000)
        self.date = datetime.datetime.now()
        self.created_by = created_by
        self.incident_type = incident_type
        self.location = location
        self.status = "draft"
        self.file = file
        self.comment = comment

    def to_json(self):
        return {
            "id": self.incident_id,
            "date": self.date,
            "created_by": self.created_by,
            "incident_type": self.incident_type,
            "status": self.status,
            "file": self.file,
            "comment": self.comment
        }


class User:
    def __init__(self, user_id, first_name, last_name, other_names, email, tel, user_name, registered, isadmin):
        self.user_id = random.randint(1, 5000)
        self.first_name = first_name
        self.last_name = last_name
        self.other_names = other_names
        self.email = email
        self.tel = tel
        self.user_name = user_name
        self.registered = datetime.datetime.now()
        self.isadmin = isadmin

    def user_to_json(self):
        return {
            "user_id": self.user_id,
            "First Name": self.first_name,
            "Last Name": self.last_name,
            "Other Names": self.last_name,
            "Email": self.email,
            "Telephone": self.tel,
            "user_name": self.user_name,
            "Registered": self.registered,
            "Is Admin": self.isadmin
        }
