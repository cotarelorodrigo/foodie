import jwt
import os
import datetime

def encode_data_to_jwt(data, expiration_minutes):
    data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=expiration_minutes)
    token = jwt.encode(data, os.environ.get('JWT_SECRET', 'secret'), algorithm='HS256').decode('utf-8')
    return token


def decode_jwt_data(token):
    data = jwt.decode(token, os.environ.get('JWT_SECRET', 'secret'), algorithm='HS256')
    return data
