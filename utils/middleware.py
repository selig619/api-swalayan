from flask import request
from functools import wraps
from configs.firebase import auth

def check_token(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if not request.headers.get('authorization'):
            return {'message': 'No token provided'},401
        try:
            user = auth.verify_id_token(request.headers['authorization'])
            # print(user)
            request.user = user
        except:
            return {'message':'Invalid token provided.'},400
        return f(*args, **kwargs)
    return wrap