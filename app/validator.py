import re
from app.models import incidents


class Validator:
    """
    method to validate incident
    """

    def validate_incident(self, created_by, incident_type, location, file, comment):

        if not created_by or created_by.isspace():
            return "Name of creator is missing"
        if not incident_type or incident_type.isspace():
            return "please mark the incident as redflag or intervention"
        if not location or location.isspace():
            return "location is missing"
        if not file or file.isspace():
            return "An image or video is missing"
        if not comment or comment.isspace():
            return"comment is missing"

    def validate_incidentid(self, incident_id):
        if not isinstance(incident_id, int):
            return "id should be an integer"

    def validate_user_credentials(self, email, password, user_name, telephone):
        if not user_name or user_name.isspace():
            return "username is missing"
        if not password or password.isspace():
            return "password is missing"
        if not email or email.isspace():
            return "please input email"
        if not telephone or telephone.isspace():
            return "please input telephone"
        if not re.search("[0-9]", telephone):
            return "contact must be digits"
        if len(user_name) < 5:
            return "username must be longer than  5 characters"
