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

@app.route('/api/v2/welcome')
def index():
    """
        method for home page
    """
    return jsonify({"message": "Welcome to iReporter application",
                    "status": 200}), 200


@app.route('/api/v2/redflags', methods=['POST'])
@auth
def create_redflag(current_user):
    """
    creates redflag
    """
    request_data = request.get_json(force=True)
    location = request_data.get('location')
    file = request_data.get('file')
    comment = request_data.get('comment')
    print(current_user)
    createdby = current_user['user']
    invalid_incident = incident_validator.validate_incident(file, comment)
    if invalid_incident:
        return jsonify({"status": 400, "message": invalid_incident}), 400
    invalid_location = incident_validator.validate_location(location)
    if invalid_location:
        return jsonify({"status": 400, "message": invalid_location}), 400
    incident_obj = database_obj.create_redflag(location, file, comment, createdby)
    if incident_obj:
        return jsonify({"status": 201, "message": "Redflag has been created", "data": [incident_obj]}), 201

@app.route('/api/v2/redflags', methods=['GET'])
@auth
def get_all_redflags(current_user):
    """
    gets all red flags
    """
    if current_user['isadmin'] == True:
        all_redflags = database_obj.get_all_redflags()
        if all_redflags:
            return jsonify({"data": all_redflags, "status": 200, "message": "all Redflags"}), 200
        return jsonify({"data": [], "status": 200, "message": "No Redflags to display"}), 200
    createdby=current_user['user']
    print(createdby)
    user_records = database_obj.get_user_redflags(createdby)
    if user_records:
            return jsonify({"data": user_records, "status": 200, "message": "all Redflags"}), 200
    return jsonify({"data": [], "status": 200, "message": "No Redflags to display"}), 200
    


@app.route('/api/v2/redflags/<int:incident_id>', methods=['GET'])
@auth
def get_single_redflag(current_user,incident_id):
    """
    gets single redflag
    """
    single_redflag = database_obj.get_single_redflag(incident_id)
    if single_redflag:
        return jsonify({"status": 200, "data": single_redflag}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v2/redflags/<int:incident_id>', methods=['DELETE'])
@auth
def delete_single_redflag(current_user,incident_id):
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
def edit_location(current_user,incident_id):
    """
    edits location of a single redflag
    """
    edit_redflag_location = request.get_json(force=True)
    location = edit_redflag_location.get("location")
    invalid_edit = incident_validator.validate_location(location)
    if invalid_edit:
        return jsonify({"status": 400, "message": invalid_edit}), 400
    redflag = database_obj.get_single_redflag(incident_id)
    print(redflag)
    if redflag and redflag["status"] == "draft":
        database_obj.update_location(location, incident_id)
        return jsonify({"status": 200, "data": [{"incident_id": incident_id,
                                                 "message": "Updated redflag's location"}]}), 200
    return jsonify({"status": 404, "message": "No redflag with such id or failed to update location"}), 404


@app.route('/api/v2/redflags/<int:incident_id>/comment', methods=['PATCH'])
@auth
def edit_comment(current_user,incident_id):
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
    if redflag and redflag["status"] == "draft":
        database_obj.update_comment(comment, incident_id)
        return jsonify({"status": 200, "data": [{"incident_id": incident_id,
                                                 "message": "Updated redflag's comment"}]}), 200
    return jsonify({"status": 404, "message": "No redflag with such id or failed to update comment"}), 404

@app.route('/api/v2/redflags/<int:incident_id>/status', methods=["PATCH"])
@auth
def update_redflag_status(current_user,incident_id):
    """ 
    updates status of redflag
    """
    if current_user['isadmin'] == True:
        status_data = request.get_json(force=True)
        status = status_data.get("status")
        invalid_status = incident_validator.validate_status(status)
        if invalid_status:
            return jsonify({"status": 400, "message": invalid_status}), 400
        redflag = database_obj.get_single_redflag(incident_id)
        if redflag:
            database_obj.update_redflag_status(status, incident_id)
            return jsonify({"status": 200, "data": [{"id": incident_id, "message": "updated redflag's status"}]}), 200
        return jsonify({"status": 404, "message": "record doesnot exist"}), 404
    return jsonify({"message": "You are not authorized to acces this route", "status": 401}), 401