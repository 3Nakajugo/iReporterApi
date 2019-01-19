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
    def get_all():
        """
        gets all redflags
        """
        return incidents

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
        red_flag = [
            incident for incident in incidents if incident['incident_id'] == incident_id]
        if red_flag:
            return red_flag
        return None
