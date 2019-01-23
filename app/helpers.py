from functools import wraps
import datetime
from flask import jsonify, request
import jwt


SECRECT_KEY = "edna123"


def encode_token(user_name):
    payload = {
        "user": user_name,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }
    token = jwt.encode(
        payload,
        'edna123',
        'HS256'
    ).decode('utf-8')
    return token


def auth(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        if 'Authorization' not in request.headers:
            return jsonify({"message": "Missing Authorization Header", "status": "401"}), 401
        if 'Authorization' in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
            try:
                payload = jwt.decode(token, SECRECT_KEY, algorithms=['HS256'])
                print(payload)
            except jwt.InvalidSignatureError:
                return jsonify({"message": "token is invalid", "status": 401}), 401

        return func(*args, **kwargs)
    return decorator
