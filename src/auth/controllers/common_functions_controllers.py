

from flask import request, jsonify
from functools import wraps
from src.jwt_handler import decode_jwt_data

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error":"Token is missing!"}), 403

        try:
            data = decode_jwt_data(token)
        except:
            return jsonify({"error":"Invalid token"}), 404
        
        return f(*args, **kwargs)
    
    return decorated