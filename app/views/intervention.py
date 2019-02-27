from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from ..models.incident import Incident
from ..models.user import User, users
from ..validator import Validator
from ..helpers import encode_token, auth
from ..Database.db import Database
from app import app


incident_validator = Validator()
database_obj = Database()





@app.route('/api/v2/interventions', methods=['POST'])
@auth
def create_intervention(current_user):
    """
    creates intervention
    """
    request_data = request.get_json(force=True)
    location = request_data.get('location')
    file = request_data.get('file')
    comment = request_data.get('comment')
    createdby = current_user['user']
    print(current_user)
    invalid_incident = incident_validator.validate_incident(file, comment)
    if invalid_incident:
        return jsonify({"status": 400, "message": invalid_incident}), 400
    invalid_location = incident_validator.validate_location(location)
    if invalid_location:
        return jsonify({"status": 400, "message": invalid_location}), 400
    incident_obj = database_obj.create_intervention(
        location, file, comment, createdby)
    if incident_obj:
        return jsonify({"status": 201, "message": "intervention has been created", "data": [incident_obj]}), 201




@app.route('/api/v2/interventions', methods=['GET'])
@auth
def all_interventions(current_user):
    """
    gets all interventions
    """
    if current_user['isadmin']==True:
        all_records = database_obj.get_all_interventions()
        if all_records:
            return jsonify({"data": all_records, "status": 200, "message": "all interventions"}), 200
        return jsonify({"status": 200, "message": "No interventions to display"}), 200
    createdby=current_user['user']
    records=database_obj.get_user_interventions(createdby)
    if records:
        return jsonify({"data": records, "status": 200, "message": "all interventions"}), 200
    return jsonify({"status": 200, "message": "No interventions to display"}), 200


@app.route('/api/v2/interventions/<int:incident_id>', methods=['GET'])
@auth
def get_single_intervention(current_user,incident_id):
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
def delete_single_interevention(current_user,incident_id):
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
def edit_intervention_location(current_user, incident_id):
    """
    edits location of a single intervention
    """
    edit_intervention_location = request.get_json(force=True)
    location = edit_intervention_location.get("location")
    valid_edit = incident_validator.validate_location(location)
    if valid_edit:
        return jsonify({"status": 400, "message": valid_edit}), 400
    intervention = database_obj.get_single_intervention(incident_id)
    if intervention and intervention["status"] == "draft":
        database_obj.update_intervention_location(location, incident_id)
        return jsonify({"status": 200, "data": [{"incident_id": incident_id,
                                                 "message": "Updated intervention's location"}]}), 200
    return jsonify({"status": 404, "message": "no intervention with id"}), 404


@app.route('/api/v2/interventions/<int:incident_id>/comment', methods=['PATCH'])
@auth
def edit_intervention_comment(current_user,  incident_id):
    """
    edits comment of a single intervention
    """
    edit_intervention_comment = request.get_json(force=True)
    comment = edit_intervention_comment.get("comment")
    valid_edit = incident_validator.validate_new_comment(comment)
    if valid_edit:
        return jsonify({"status": 400, "message": valid_edit}), 400
    intervention = database_obj.get_single_intervention(incident_id)
    if intervention and intervention["status"] == "draft":
        database_obj.update_intervention_comment(comment, incident_id)
        return jsonify({"status": 200, "data": [{"incident_id": incident_id, "message": "Updated intervention's comment"}]}), 200
    return jsonify({"status": 404, "message": "No intervention with such an id"}), 404


@app.route('/api/v2/interventions/<int:incident_id>/status', methods=["PATCH"])
@auth
def update_interventions_status(current_user, incident_id):
    """ 
    updates status of intervention
    """
    if current_user['isadmin'] == True:
        status_data = request.get_json(force=True)
        status = status_data.get("status")
        invalid_status = incident_validator.validate_status(status)
        if invalid_status:
            return jsonify({"status": 400, "message": invalid_status}), 400
        intervention = database_obj.get_single_intervention(incident_id)
        if intervention:
            database_obj.update_intervention_status(status, incident_id)
            return jsonify({"status": 200, "data": [{"id": incident_id, "message": "updated Interventions status"}]}), 200
        return jsonify({"status": 404, "message": "record doesnot exist"}), 404
    return jsonify({"message": "You are not authorized to acces this route", "status": 401}), 401



    
