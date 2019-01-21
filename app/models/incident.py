import datetime

incidents = []


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

    @staticmethod
    def create(incident):
        """ 
        method to create incident
        """
        new_incident = incident.to_json()
        incidents.append(new_incident)
        return incidents

    @staticmethod
    def get_all(incident_type):
        """
        gets all incident
        """
        redflags_list = []
        interventions_list = []
        for incident in incidents:
            if incident_type == "redflag":
                redflags_list.append(incident)
            elif incident_type == "intervention":
                interventions_list.append(incident)
        if incident_type == "redflag"and redflags_list:
            return redflags_list
        elif incident_type == "intervention" and interventions_list:
            return interventions_list
        else:
            return None
        

    @staticmethod
    def get_single(incident_id):
        """
        gets single redflags
        """

        for incident in incidents:
            if incident['incident_id'] == incident_id:
                return incident

    @staticmethod
    def delete(incident_id):
        """
        deletes single  redflags
        """
        for incident in incidents:
            if incident["incident_id"] == incident_id:
                incidents.remove(incident)
                return "incident was deleted"

    @staticmethod
    def update(incident_id):
        """
        updates single  redflags
        """
        incident = [
            incident for incident in incidents if incident['incident_id'] == incident_id]
        if incident:
            return incident
        return None
