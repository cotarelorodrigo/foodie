from flask import request, jsonify
from functools import wraps
from src.jwt_handler import decode_jwt_data

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error":"Token is missing!"}), 421

        try:
            kwargs['data'] = decode_jwt_data(token)
        except:
            return jsonify({"error":"Invalid token"}), 422
        
        return f(*args, **kwargs)
    
    return decorated


def user_is_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not kwargs['data']["is_admin"]:
            return jsonify({"error":"You are not an admin"}), 422
        del kwargs['data']
        return f(*args, **kwargs)
    return decorated
