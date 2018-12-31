from flask import Flask, jsonify, request
from .models import Incident, incidents
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
    request_data = request.get_json(force=True)
    created_by = request_data.get('created_by')
    incident_type = request_data.get('incident_type')
    location = request_data.get('location')
    file = request_data.get('file')
    comment = request_data.get('comment')
    valid_incident = incident_validator.validate_incident(created_by,
                                                          incident_type, location, file, comment)
    if valid_incident:
        return jsonify({"status": 400, "message": "some fields are empty"}), 400
    incident_obj = Incident(created_by,
                            incident_type, location, file, comment)

    add_incident = incident_controller.create_incident(incident_obj)
    if add_incident:
        return jsonify({"status": 201, "data": [{"message": "incident {} has been created".format(incident_type)}]}), 201
    return jsonify({"status": 400, "message": "could not create incident"}), 400


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


@app.route('/api/v1/incidents/<int:incident_id>', methods=['DELETE'])
def delete_single_redflag(incident_id):
    """
    method for deleting a single redflag
    """
    delete_single_redflag = incident_controller.delete_single_redflag(
        incident_id)
    if delete_single_redflag:
        return jsonify({"status": 200, "data": [{"id": incident_id, "message": "red-flag record has been deleted"}]}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v1/incidents/<int:incident_id>/location', methods=['PATCH'])
def edit_location(incident_id):
    """
    method for editing location of a single redflag
    """
    edit_redflag = incident_controller.update_location(incident_id)
    if edit_redflag:
        edit_redflag[0]['location'] = request.json.get(
            'location', edit_redflag[0]['location'])
    if edit_redflag[0]['location']:
        return jsonify({"status": 200, "data": [{"incident_id": incident_id, "message": "Updated redflag's location"}]}), 200
    return jsonify({"status": 404, "error": "no incident with such an id"}), 404


# @app.route('/api/v1/incidents/<int:incident_id>/comment', methods=['PATCH'])
# def edit_comment(incident_id):
#     """
#     method for editing comment of a single redflag
#     """
#     edit_redflag = incident_controller.update_location(incident_id)
#     if edit_redflag:
#         edit_redflag[0]['comment'] = request.json.get(
#             'comment', edit_redflag[0]['comment'])
#     if edit_redflag[0]['comment']:
#         return jsonify({"status": 200, "data": [{"incident_id": incident_id, "message": "Updated redflag's location"}]}), 200
#     return jsonify({"status": 404, "error": "no incident with such an id"}), 404
