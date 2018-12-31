from project.models import incidents


class Validator:
    """
    method to validate incident
    """

    def validate_incident(self, created_by, incident_type, location, file, comment):
        try:
            if created_by == "":
                return "Name of creator is missing"
            if incident_type == "":
                return "please mark the incident as redflag or intervention"
            if location == "":
                return "location is missing"
            if file == "":
                return "An image or video is missing"
            if comment == "":
                return"comment is missing"

        except KeyError:
            return "please enter all fields"
        
    def validate_incidentid(self,incident_id):
        if not isinstance(incident_id,int):
            return "id should be an integer"


    def validate_user(self):
        pass
