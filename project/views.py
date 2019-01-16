from flask import Flask, jsonify, request
from .models import Incident, incidents, User, users
from .controllers.incident_cntr import IncidentCntr
from .controllers.user_cntr import UserController
from .validator import Validator

incident_controller = IncidentCntr()
user_cntr = UserController()
incident_validator = Validator()

app = Flask(__name__)


@app.route('/api/v1/welcome')
def index():
    """
        method for home page
    """
    return jsonify({"message": "Welcome to iReporter",
                    "status": 200}), 200


@app.route('/api/v1/users/signup', methods=['POST'])
def register_user():
    """
        method for creating user
    """
    request_data = request.get_json(force=True)
    first_name = request_data.get('first_name')
    last_name = request_data.get('last_name')
    other_names = request_data.get('other_names')
    email = request_data.get('email')
    telephone = request_data.get('telephone')
    user_name = request_data.get('user_name')
    password = request_data.get('password')
    invalid_user = incident_validator.validate_user_credentials(
        email, password, user_name, telephone)
    if invalid_user:
        return jsonify({"status": 400, "message": "some fields are missing"}), 400
    user = User(first_name=first_name, last_name=last_name, other_names=other_names,
                email=email, telephone=telephone, user_name=user_name, password=password)
    user_record = user_cntr.create_user(user)
    if user_record:
        return jsonify({"message": "User has been created",
                        "status": 200}), 200


@app.route('/api/v1/users', methods=['GET'])
def get_user():
    """
        method for getting all users
    """
    if len(users) > 0:
        all_users = user_cntr.get_all_users()
        if all_users:
            return jsonify({"data": all_users, "status": 200, "message": "all users"}), 200
    return jsonify({"status": 200, "message": "No Users to display"}), 200


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
    invalid_incident = incident_validator.validate_incident(created_by,
                                                            incident_type, location, file, comment)
    if invalid_incident:
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


@app.route('/api/v1/incidents/<int:incident_id>/comment', methods=['PATCH'])
def edit_comment(incident_id):
    """
    method for editing comment of a single redflag
    """
    edit_redflag = incident_controller.update_location(incident_id)
    if edit_redflag:
        edit_redflag[0]['comment'] = request.json.get(
            'comment', edit_redflag[0]['comment'])
    if edit_redflag[0]['comment']:
        return jsonify({"status": 200, "data": [{"incident_id": incident_id, "message": "Updated redflag's location"}]}), 200
    return jsonify({"status": 404, "error": "no incident with such an id"}), 404
