from project.models import Incident, incidents


class IncidentCntr:

    def create_incident(self, created_by, incident_type, location, file, comment):
        incident = Incident(
            created_by=created_by,
            incident_type=incident_type,
            location=location,
            file=file,
            comment=comment
        )
        new_incident = incident.to_json()
        incidents.append(new_incident)
        return incidents

    def get_all_redflags(self):
        if len(incidents) > 0:
            return incidents

    def get_single_redflag(self, incident_id):
        for incident in incidents:
            if incident['incident_id'] == incident_id:
                return incident
