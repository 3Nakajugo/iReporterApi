from project.models import  incidents

class Validator:
    """
    method to validate incident
    """

    def validate_incident(self, created_by, incident_type, location, file, comment):
        if not created_by and created_by == "":
            return "Name of creator is missing"
        if not incident_type and incident_type == "":
            return "please mark the incident as redflag or intervention"
        if not location and location == "":
            return "location is missing"
        if not file and file == "":
            return "An image or video is missing"
        if not comment and comment == "":
            return"comment is missing"

   

    def validate_user(self):
        pass
