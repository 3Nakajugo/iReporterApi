import random
import datetime
from flask import Flask, jsonify, request
from .models import Incident, User, incidents
from .controllers.incident_cntr import IncidentCntr
from .validator import Validator

incident_controller = IncidentCntr()
incident_validator = Validator()

app = Flask(__name__)

"""
route for home page
"""

@app.route('/api/v1/welcome')
def index():
    return jsonify({"message": "Welcome to iReporter",
                    "status": 200})



"""
route for posting/creating an incident
"""
@app.route('/api/v1/incidents', methods=['POST'])
def create_incident():
    request_data = request.get_json()
    incident_id = random.randint(1, 1000)
    date = datetime.datetime.now()
    created_by = request_data.get('created_by')
    incident_type = request_data.get('incident_type')
    location = request_data.get('location')
    status = request_data.get('status')
    file = request_data.get('file')
    comment = request_data.get('comment')
    valid_incident = incident_validator.validate_incident(created_by,
                                                          incident_type, location, status, file, comment)
    if valid_incident:
        return jsonify({"status": 400, "message": "some fields are empty"}), 400
    incident_obj = Incident(incident_id, date, created_by,
                            incident_type, location, status, file, comment)

    add_incident = incident_controller.create_incident(
        incident_id=incident_obj.incident_id,
        date=incident_obj.date,
        created_by=incident_obj.created_by,
        incident_type=incident_obj.incident_type,
        location=incident_obj.location,
        status=incident_obj.status,
        file=incident_obj.file,
        comment=incident_obj.comment)
    if add_incident:
        return jsonify({"status": 201, "data": incidents, "message": "incident {} has been created".format(incident_type)}), 201
