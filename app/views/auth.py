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
    user_exists = database_obj.get_user_by_username(user_name)
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
    user_credentials = database_obj.login(user_name, password)
    if user_credentials is None:
        return jsonify({"message": "no user with such credentials", "status": 401}), 401
    user_login = user_credentials["user_name"]
    isadmin = user_credentials["isadmin"]
    token = encode_token(user_login, isadmin)
    return jsonify({"message": "successfully logged in", "status": 200,
                    "token": token, "data": [user_credentials]}), 200


@app.route('/api/v2/users', methods=['GET'])
@auth
def get_all_users(current_user):
    if current_user["isadmin"] == True:
        all_users = database_obj.get_all_users()
        if all_users:
            return jsonify({"data": all_users, "status": 200, "message": "all users"}), 200
        return jsonify({"data": [], "status": 200, "message": "No users to display"}), 200
    return jsonify({"message": "You are not authorized to acces this route", "status": 401}), 401
