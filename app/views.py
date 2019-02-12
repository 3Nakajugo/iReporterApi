from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from .models.incident import Incident
from .models.user import User, users
from .validator import Validator
from .helpers import encode_token, auth
from .Database.db import Database


incident_validator = Validator()
database_obj = Database()

app = Flask(__name__)
CORS(app, resources=r'/api/*')

database = Database()
database.create_tables()


@app.route('/api/v2/welcome')
def index():
    """
        method for home page
    """
    return jsonify({"message": "Welcome to iReporter application",
                    "status": 200}), 200


@app.route('/api/v2/auth/signup', methods=['POST'])
def register_user():
    """
        method for creating user
    """
    request_data = request.get_json(force=True)
    first_name = request_data.get('first_name')
    last_name = request_data.get('last_name')
    email = request_data.get('email')
    telephone = request_data.get('telephone')
    user_name = request_data.get('user_name')
    password = request_data.get('password')
    isadmin = 'False'
    if (user_name == 'admin'):
        isadmin = 'True'
    invalid_user = incident_validator.validate_user_credentials(
        password, user_name, telephone)
    if invalid_user:
        return jsonify({"status": 400, "message": invalid_user}), 400
    invalid_password = incident_validator.validate_password(password)
    if invalid_password:
        return jsonify({"status": 400, "message": invalid_password}), 400
    user_exists = database.get_user_by_username(user_name)
    if user_exists:
        return jsonify({"status": 400, "message": "username already exists"}), 400
    invalid_email = incident_validator.validate_email(email)
    if invalid_email:
        return jsonify({"status": 400, "message": invalid_email}), 400
    invalid_names = incident_validator.validate_names(first_name, last_name)
    if invalid_names:
        return jsonify({"status": 400, "message": invalid_names}), 400
    invalid_isadmin = incident_validator.validate_isadmin(isadmin)
    if invalid_isadmin:
        return jsonify({"status": 400, "message": invalid_isadmin}), 400
    user_record = database_obj.create_user(
        first_name, last_name,  email, telephone, user_name, password, isadmin)
    if not user_record:
        return jsonify({"status": 400, "message": "user has not been created"}), 400
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
    if user_credentials is None:
        return jsonify({"message": "no user with such credentials", "status": 401}), 401
    user_login = user_credentials["user_name"]
    isadmin = user_credentials["isadmin"]
    token = encode_token(user_login, isadmin)
    return jsonify({"message": "successfully logged in", "status": 200,
                    "token": token, "data": [user_credentials]}), 200


@app.route('/api/v2/redflags', methods=['POST'])
@auth
def create_redflag(current_user, admin):
    """
    creates redflag
    """
    request_data = request.get_json(force=True)
    location = request_data.get('location')
    file = request_data.get('file')
    comment = request_data.get('comment')
    print(current_user)
    createdby = current_user
    invalid_incident = incident_validator.validate_incident(
        location, file, comment)
    if invalid_incident:
        return jsonify({"status": 400, "message": invalid_incident}), 400
    incident_obj = database.create_redflag(location, file, comment, createdby)
    if incident_obj:
        return jsonify({"status": 201, "message": "Redflag has been created", "data": [incident_obj]}), 201


@app.route('/api/v2/interventions', methods=['POST'])
@auth
def create_intervention(current_user, admin):
    """
    creates intervention
    """
    request_data = request.get_json(force=True)
    location = request_data.get('location')
    file = request_data.get('file')
    comment = request_data.get('comment')
    createdby = current_user
    print(current_user)
    invalid_incident = incident_validator.validate_incident(
        location, file, comment)
    if invalid_incident:
        return jsonify({"status": 400, "message": invalid_incident}), 400
    incident_obj = database.create_intervention(
        location, file, comment, createdby)
    if incident_obj:
        return jsonify({"status": 201, "message": "intervention has been created", "data": [incident_obj]}), 201


@app.route('/api/v2/redflags', methods=['GET'])
@auth
def get_all_redflags(current_user, admin):
    """
    gets all red flags
    """
    all_redflags = database_obj.get_all_redflags()
    if all_redflags:
        return jsonify({"data": all_redflags, "status": 200, "message": "all Redflags"}), 200
    return jsonify({"data": [], "status": 200, "message": "No Redflags to display"}), 200


@app.route('/api/v2/redflags/<int:incident_id>', methods=['GET'])
@auth
def get_single_redflag(current_user, admin, incident_id):
    """
    gets single redflag
    """
    single_redflag = database_obj.get_single_redflag(incident_id)
    if single_redflag:
        return jsonify({"status": 200, "data": single_redflag}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v2/redflags/<int:incident_id>', methods=['DELETE'])
@auth
def delete_single_redflag(current_user, admin, incident_id):
    """
    deletes a single redflag
    """
    incident = database_obj.get_single_redflag(incident_id)
    if incident:
        database_obj.delete_redflag(incident_id)
        return jsonify({"status": 200, "data": [{"id": incident_id, "message": "red-flag record has been deleted"}]}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v2/redflags/<int:incident_id>/location', methods=['PATCH'])
@auth
def edit_location(current_user, admin, incident_id):
    """
    edits location of a single redflag
    """
    edit_redflag_location = request.get_json(force=True)
    location = edit_redflag_location.get("location")
    invalid_edit = incident_validator.edit_location(location)
    if invalid_edit:
        return jsonify({"status": 400, "message": invalid_edit}), 400
    redflag = database_obj.get_single_redflag(incident_id)
    print(redflag)
    if redflag:
        database_obj.update_location(location, incident_id)
        return jsonify({"status": 200, "data": [{"incident_id": incident_id,
                                                 "message": "Updated redflag's location"}]}), 200
    return jsonify({"status": 404, "message": "No redflag with such id"}), 404


@app.route('/api/v2/redflags/<int:incident_id>/comment', methods=['PATCH'])
@auth
def edit_comment(current_user, admin, incident_id):
    """
    method for editing comment of a single redflag
    """
    edit_redflag_comment = request.get_json(force=True)
    comment = edit_redflag_comment.get("comment")
    invalid_edit = incident_validator.edit_comment(comment)
    if invalid_edit:
        return jsonify({"status": 400, "message": invalid_edit}), 400
    redflag = database_obj.get_single_redflag(incident_id)
    print(redflag)
    if redflag:
        database_obj.update_comment(comment, incident_id)
        return jsonify({"status": 200, "data": [{"incident_id": incident_id,
                                                 "message": "Updated redflag's comment"}]}), 200
    return jsonify({"status": 404, "message": "No redflag with such id"}), 404


@app.route('/api/v2/interventions', methods=['GET'])
@auth
def all_interventions(current_user, admin):
    """
    gets all interventions
    """
    all_records = database_obj.get_all_interventions()
    if all_records:
        return jsonify({"data": all_records, "status": 200, "message": "all interventions"}), 200
    return jsonify({"status": 200, "message": "No interventions to display"}), 200


@app.route('/api/v2/interventions/<int:incident_id>', methods=['GET'])
@auth
def get_single_intervention(current_user, admin, incident_id):
    """
    gets single intervention 
    """
    single_intervention = database_obj.get_single_intervention(incident_id)
    if single_intervention:
        return jsonify({"status": 200, "data": [single_intervention]}), 200
    message = jsonify(
        {"status": 404, "message": "no incident with such an id"}), 404
    return message


@app.route('/api/v2/interventions/<int:incident_id>', methods=['DELETE'])
@auth
def delete_single_interevention(current_user, admin, incident_id):
    """
    deletes single intervention
    """
    incident = database_obj.get_single_intervention(incident_id)
    if incident:
        database_obj.delete_intervention(incident_id)
        return jsonify({"status": 200, "id": incident_id, "message": "intervention was deleted"}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v2/interventions/<int:incident_id>/location', methods=['PATCH'])
@auth
def edit_intervention_location(current_user, admin, incident_id):
    """
    edits location of a single intervention
    """
    edit_intervention_location = request.get_json(force=True)
    location = edit_intervention_location.get("location")
    valid_edit = incident_validator.edit_location(location)
    if valid_edit:
        return jsonify({"status": 400, "message": valid_edit}), 400
    intervention = database_obj.get_single_intervention(incident_id)
    if intervention:
        database_obj.update_intervention_location(location, incident_id)
        return jsonify({"status": 200, "data": [{"incident_id": incident_id,
                                                 "message": "Updated intervention's location"}]}), 200
    return jsonify({"status": 404, "message": "no intervention with id"}), 404


@app.route('/api/v2/interventions/<int:incident_id>/comment', methods=['PATCH'])
@auth
def edit_intervention_comment(current_user, admin, incident_id):
    """
    edits comment of a single intervention
    """
    edit_intervention_comment = request.get_json(force=True)
    comment = edit_intervention_comment.get("comment")
    valid_edit = incident_validator.validate_new_comment(comment)
    if valid_edit:
        return jsonify({"status": 400, "message": valid_edit}), 400
    intervention = database_obj.get_single_intervention(incident_id)
    if intervention:
        database_obj.update_intervention_comment(comment, incident_id)
        return jsonify({"status": 200, "data": [{"incident_id": incident_id, "message": "Updated intervention's comment"}]}), 200
    return jsonify({"status": 404, "message": "No intervention with such an id"}), 404


@app.route('/api/v2/interventions/<int:incident_id>/status', methods=["PATCH"])
@auth
def update_interventions_status(current_user, admin, incident_id):
    """ 
    updates status of intervention
    """
    if admin == True:
        status_data = request.get_json(force=True)
        status = status_data.get("status")
        intervention = database_obj.get_single_intervention(incident_id)
        if intervention and intervention["status"] == "draft":
            database_obj.update_intervention_status(status, incident_id)
            return jsonify({"status": 200, "data": [{"id": incident_id, "message": "updated Interventions status"}]}), 200
        return jsonify({"status": 400, "message": "record can not be updated because status is not draft or doesnot exist"}), 400
    return jsonify({"message": "You are not authorized to acces this route", "status": 401}), 401


@app.route('/api/v2/redflags/<int:incident_id>/status', methods=["PATCH"])
@auth
def update_redflag_status(current_user, admin, incident_id):
    """ 
    updates status of redflag
    """
    if admin == True:
        status_data = request.get_json(force=True)
        status = status_data.get("status")
        invalid_status = incident_validator.validate_status(status)
        if invalid_status:
            return jsonify({"status": 400, "message": invalid_status}), 400
        redflag = database_obj.get_single_redflag(incident_id)
        if redflag and redflag["status"] == "draft":
            database_obj.update_redflag_status(status, incident_id)
            return jsonify({"status": 200, "data": [{"id": incident_id, "message": "updated redflag's status"}]}), 200
        return jsonify({"status": 400, "message": "record can not be updated because status is not draft or doesnot exist"}), 400
    return jsonify({"message": "You are not authorized to acces this route", "status": 401}), 401
