from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from .models.incident import Incident, incidents
from .models.user import User, users
from .validator import Validator


incident_validator = Validator()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'edna123'
jwt = JWTManager(app)


@app.route('/api/v1/welcome')
def index():
    """
        method for home page
    """
    return jsonify({"message": "Welcome to iReporter",
                    "status": 200}), 200


@app.route('/api/v1/auth/signup', methods=['POST'])
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
    user_exists = User.check_user_exists(user_name, password)
    if user_exists:
        return jsonify({"status": 400, "message": user_exists}), 400
    invalid_email = incident_validator.validate_email(email)
    if invalid_email:
        return jsonify({"status": 400, "message": invalid_email}), 400
    invalid_names=incident_validator.validate_names(first_name,last_name,other_names)
    if invalid_names:
        return jsonify({"status": 400, "message": invalid_names}), 400
    # name_not_alpha = incident_validator.validate_name_input(first_name)
    # if name_not_alpha:
    #     return jsonify({"status": 400, "message": name_not_alpha}), 400
    user = User(first_name=first_name, last_name=last_name, other_names=other_names,
                email=email, telephone=telephone, user_name=user_name, password=password)
    user_record = User.create(user)
    if user_record:
        return jsonify({"data": [{"user": user_record}],
                        "status": 201, "message": "user has been created"}), 201


@app.route('/api/v1/users', methods=['GET'])
@jwt_required
def get_users():
    """
        method for getting all users
    """

    get_role = get_jwt_identity()["Is Admin"]
    if not get_role:
        return jsonify({"status": 401, "message": "Unauthorized access"}), 401
    all_users = User.get_all_users()
    if all_users is None:
        return jsonify({"data": all_users, "status": 200, "message": "No Users to display"}), 200
    return jsonify({"data": all_users, "status": 200, "role": get_role, "message": "all users"}), 200


@app.route('/api/v1/auth/login', methods=['POST'])
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
    user_credentials = User.login(user_name, password)
    token = create_access_token(identity=user_credentials)
    if user_credentials is None:
        return jsonify({"message": "no user with such credentials", "status": 401}), 401
    return jsonify({"message": "successfully logged in", "status": 200, "token": token, "data": [{"user": user_credentials}]}), 200


@app.route('/api/v1/redflags', methods=['POST'])
@jwt_required
def create_redflag():
    """
    creates redflag
    """
    request_data = request.get_json(force=True)
    created_by = request_data.get('created_by')
    incident_type = "redflag"
    location = request_data.get('location')
    file = request_data.get('file')
    comment = request_data.get('comment')
    invalid_incident = incident_validator.validate_incident(created_by,
                                                            incident_type, location, file, comment)
    if invalid_incident:
        return jsonify({"status": 400, "message": invalid_incident}), 400
    incident_obj = Incident(created_by,
                            incident_type, location, file, comment)

    add_redflag = Incident.create(incident_obj)
    if add_redflag:
        return jsonify({"status": 201, "data": [{"message": "incident {} has been created".format(incident_type)}]}), 201


@app.route('/api/v1/redflags', methods=['GET'])
@jwt_required
def get_all_redflags():
    """
    gets all red flags
    """
    all_redflags = Incident.get_all("redflag")
    if all_redflags is None:
        return jsonify({"status": 200, "all Red flags": [], "message": "No Redflags to display"}), 200
    return jsonify({"data": all_redflags, "status": 200, "message": "all Redflags"}), 200


@app.route('/api/v1/redflags/<int:incident_id>', methods=['GET'])
@jwt_required
def get_single_redflag(incident_id):
    """
    gets single redflag
    """
    single_redflag = Incident.get_single(incident_id)
    if single_redflag:
        return jsonify({"status": 200, "data": single_redflag}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v1/redflags/<int:incident_id>', methods=['DELETE'])
@jwt_required
def delete_single_redflag(incident_id):
    """
     deletes a single redflag
    """
    delete_single_redflag = Incident.delete(incident_id)
    if delete_single_redflag:
        return jsonify({"status": 200, "data": [{"id": incident_id, "message": "red-flag record has been deleted"}]}), 200
    return jsonify({"status": 404, "message": "no incident with such an id"}), 404


@app.route('/api/v1/redflags/<int:incident_id>/location', methods=['PATCH'])
@jwt_required
def edit_location(incident_id):
    """
    edits location of a single redflag
    """
    edit_redflag = Incident.update(incident_id)
    if not edit_redflag:
        return jsonify({"status": 404, "error": "no incident with such an id"}), 404
    edit_redflag[0]['location'] = request.json.get(
        'location', edit_redflag[0]['location'])

    if edit_redflag[0]['location']:
        return jsonify({"status": 200, "data": [{"incident_id": incident_id, "message": "Updated redflag's location"}]}), 200


@app.route('/api/v1/redflags/<int:incident_id>/comment', methods=['PATCH'])
@jwt_required
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


