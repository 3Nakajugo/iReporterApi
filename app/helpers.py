from functools import wraps
import datetime
from flask import jsonify, request
import jwt


SECRECT_KEY = "edna123"


def encode_token(user_name, isadmin):
    """ creates payload for token"""
    payload = {
        "user": user_name,
        "isadmin": isadmin,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(
        payload,
        'edna123',
        'HS256'
    ).decode('utf-8')
    return token


def auth(func):
    """ creates decorator to protect routes"""
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({"message": "Missing Authorization Header", "status": "401"}), 401
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            try:
                current_user = jwt.decode(token, SECRECT_KEY, algorithms=['HS256'])
            except jwt.InvalidSignatureError:
                return jsonify({"message": "token is invalid", "status": 401}), 401
            except jwt.ExpiredSignatureError:
                return jsonify({"message": " Your token has expired", "status": 401}), 401
        return func(current_user, *args, **kwargs)
    return decorator
