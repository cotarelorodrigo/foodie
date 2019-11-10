from flask import request, jsonify
from functools import wraps
from src.jwt_handler import decode_jwt_data
import src.settings
from flask import g
from firebase_admin import auth
import firebase_admin

firebase_app = firebase_admin.initialize_app()

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({"error":"Token is missing!"}), 421

        try:
            g.data = decode_jwt_data(token)
        except:
            return jsonify({"error":"Invalid token"}), 422
        
        return f(*args, **kwargs)
    
    return decorated


def user_is_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not g.data["is_admin"]:
            return jsonify({"error":"You are not an admin"}), 422
        #del kwargs['data']
        return f(*args, **kwargs)
    return decorated


def verify_firebase_uid(token):
    cred = auth.verify_id_token(token)
    return cred
