from flask import Flask, jsonify, request
from .models import Incident, User, incidents
from .controllers.incident_cntr import IncidentCntr
from .validator import Validator

incident_controller = IncidentCntr()
incident_validator = Validator()

app = Flask(__name__)


@app.route('/api/v1/welcome')
def index():
    """
        method for home page
    """
    return jsonify({"message": "Welcome to iReporter",
                    "status": 200})


@app.route('/api/v1/incidents', methods=['POST'])
def create_incident():
    """
    method for creating an incident
    """
    request_data = request.get_json()
    # created_by = request_data.get('created_by')
    # incident_type = request_data.get('incident_type')
    # location = request_data.get('location')
    # file = request_data.get('file')
    # comment = request_data.get('comment')
    created_by = request_data['created_by']
    incident_type = request_data['incident_type']
    location = request_data['location']
    file = request_data['file']
    comment = request_data['comment']
    valid_incident = incident_validator.validate_incident(created_by,
                                                          incident_type, location, file, comment)
    if valid_incident:
        return jsonify({"status": 400, "message": "some fields are empty"}), 400
    incident_obj = Incident(created_by,
                            incident_type, location, file, comment)

    add_incident = incident_controller.create_incident(
        created_by=incident_obj.created_by,
        incident_type=incident_obj.incident_type,
        location=incident_obj.location,
        file=incident_obj.file,
        comment=incident_obj.comment)
    if add_incident:
        return jsonify({"status": 201, "data": incidents, "message": "incident {} has been created".format(incident_type)}), 201


@app.route('/api/v1/incidents', methods=['GET'])
def get_all_redflags():
    """
    method for getting all red flags
    """
    all_incidents = incident_controller.get_all_redflags()
    if all_incidents:
        return jsonify({"data": all_incidents, "status": 200, "message": "all incidents"}), 200
    return jsonify({"status": 200, "message": "No incidents to display"}), 200


@app.route('/api/v1/incidents/<int:incident_id>', methods=['GET'])
def get_single_redflag(incident_id):
    """
    method for getting single redflag
    """
    single_redflag = incident_controller.get_single_redflag(incident_id)
    if single_redflag:
        return jsonify({"status": 200, "data": single_redflag}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404
