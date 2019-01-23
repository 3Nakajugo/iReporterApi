from flask import Flask, jsonify, request
import jwt
import datetime
from os import environ
from .models.incident import Incident
from .models.user import User, users
from .validator import Validator
from .Database.db import Database


incident_validator = Validator()
database_obj = Database()

app = Flask(__name__)
jwt_secret_key = environ.get("JWT_SECRET_KEY", "edna1234")
database = Database()
database.create_tables()


@app.route('/api/v2/welcome')
def index():
    """
        method for home page
    """
    return jsonify({"message": "Welcome to iReporter",
                    "status": 200}), 200


@app.route('/api/v2/auth/signup', methods=['POST'])
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
        return jsonify({"status": 400, "message": invalid_user}), 400
    invalid_email = incident_validator.validate_email(email)
    if invalid_email:
        return jsonify({"status": 400, "message": invalid_email}), 400
    invalid_names = incident_validator.validate_names(
        first_name, last_name, other_names)
    if invalid_names:
        return jsonify({"status": 400, "message": invalid_names}), 400
    user_exists = database.get_user_by_username(user_name)
    if user_exists:
        return jsonify({"status": 400, "message": "username already exists"}), 400
    user_record = database_obj.create_user(
        first_name, last_name, other_names, email, telephone, user_name, password)
    if not user_record:
        return jsonify({"status": 400, "message": "user has been created"}), 400
    return jsonify({"data": [user_record],
                    "status": 201, "message": "user has been created"}), 201


@app.route('/api/v2/auth/login', methods=['POST'])
def login():
    """
        method user login
    """
    request_data = request.get_json(force=True)
    user_name = request_data.get('user_name')
    password = request_data.get('password')
    missing_credentials = incident_validator.validate_login(
        user_name, password)
    if missing_credentials:
        return jsonify({"message": missing_credentials, "status": 400}), 400
    user_credentials = database.login(user_name, password)
    payload = {
        "user": user_credentials.get("user_name"),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    token = jwt.encode(
        payload,
        'edna1234',
        algorithm='HS256'
    )
    if user_credentials is None:
        return jsonify({"message": "no user with such credentials", "status": 401}), 401
    return jsonify({"message": "successfully logged in", "status": 200,
                    "token": token.decode('utf-8'), "data": [{"user": user_credentials}]}), 200


@app.route('/api/v2/redflags', methods=['POST'])
def create_redflag():
    """
    creates redflag
    """
    request_data = request.get_json(force=True)
    # created_by = request_data.get('created_by')
    location = request_data.get('location')
    file = request_data.get('file')
    comment = request_data.get('comment')
    invalid_incident = incident_validator.validate_incident(
        location, file, comment)
    if invalid_incident:
        return jsonify({"status": 400, "message": invalid_incident}), 400
    incident_obj = database.create_redflag(location, file, comment)
    if incident_obj:
        return jsonify({"status": 201, "message": "Redflag has been created", "data": [incident_obj]}), 201


@app.route('/api/v2/interventions', methods=['POST'])
def create_intervention():
    """
    creates intervention
    """
    request_data = request.get_json(force=True)
    # created_by = request_data.get('created_by')
    location = request_data.get('location')
    file = request_data.get('file')
    comment = request_data.get('comment')
    invalid_incident = incident_validator.validate_incident(
        location, file, comment)
    if invalid_incident:
        return jsonify({"status": 400, "message": invalid_incident}), 400
    incident_obj = database.create_intervention(location, file, comment)
    if incident_obj:
        return jsonify({"status": 201, "message": "intervention has been created", "data": [incident_obj]}), 201


@app.route('/api/v2/redflags', methods=['GET'])
def get_all_redflags():
    """
    gets all red flags
    """
    all_redflags = database_obj.get_all_redflags()
    if all_redflags is None:
        return jsonify({"status": 200,  "message": "No Redflags to display"}), 200
    return jsonify({"data": all_redflags, "status": 200, "message": "all Redflags"}), 200


@app.route('/api/v2/redflags/<int:incident_id>', methods=['GET'])
def get_single_redflag(incident_id):
    """
    gets single redflag
    """
    single_redflag = database_obj.get_single_redflag(incident_id)
    if single_redflag:
        return jsonify({"status": 200, "data": single_redflag}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v2/redflags/<int:incident_id>', methods=['DELETE'])
def delete_single_redflag(incident_id):
    """
    deletes a single redflag
    """
    delete_single_redflag = Incident.delete(incident_id)
    if delete_single_redflag:
        return jsonify({"status": 200, "data": [{"id": incident_id, "message": "red-flag record has been deleted"}]}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v2/redflags/<int:incident_id>/location', methods=['PATCH'])
def edit_location(incident_id, location):
    """
    edits location of a single redflag
    """
    edit_redflag_location = request.get_json(force=True)
    location = edit_redflag_location.get("location")
    valid_edit = incident_validator.edit_location(location)
    if not valid_edit:
        return jsonify({"status": 400, "message": valid_edit}), 400
    edited_location = database_obj.update_location(location, incident_id)
    if edited_location:
        return jsonify({"status": 200, "data": [{"incident_id": incident_id,
                                                 "message": "Updated redflag's location"}]}), 200
    return jsonify({"status": 200, "message": "location was updated"}), 200


@app.route('/api/v2/redflags/<int:incident_id>/comment', methods=['PATCH'])
def edit_comment(incident_id):
    """
    method for editing comment of a single redflag
    """
    edit_redflag = Incident.update(incident_id)
    if not edit_redflag:
        return jsonify({"status": 404, "error": "no incident with such an id"}), 404
    edit_redflag[0]['comment'] = request.json.get(
        'comment', edit_redflag[0]['comment'])
    if edit_redflag[0]['comment']:
        return jsonify({"status": 200, "data": [{"incident_id": incident_id, "message": "Updated redflag's comment"}]}), 200


@app.route('/api/v2/interventions', methods=['GET'])
def all_interventions():
    """
    gets all interventions
    """
    all_records = database_obj.get_all_interventions()
    if all_records is None:
        return jsonify({"status": 200,  "message": "No interventions to display"}), 200
    return jsonify({"data": all_records, "status": 200, "message": "all interventions"}), 200


@app.route('/api/v2/interventions/<int:incident_id>', methods=['GET'])
def get_single_intervention(incident_id):
    """
    gets single intervention 
    """
    single_intervention = database_obj.get_single_intervention(incident_id)
    if single_intervention:
        return jsonify({"status": 200, "data": [single_intervention]}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404
