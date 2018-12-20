from project.models import Incident, incidents


class IncidentCntr:

    def create_incident(self, incident_id, date, created_by, incident_type, location, status, file, comment):
        incident = Incident(
            incident_id=incident_id,
            date=date,
            created_by=created_by,
            incident_type=incident_type,
            location=location,
            status=status,
            file=file,
            comment=comment
        )
        new_incident = incident.to_json()
        incidents.append(new_incident)
        return incidents


