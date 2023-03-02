import string, secrets

from models.User import User
from configs.firebase import get_auth, get_database
from configs.constants import ADMIN, CUSTOMER
from utils.middleware import check_token

from flask import request
from datetime import datetime, timezone
from firebase_admin import exceptions
from marshmallow import Schema, fields, ValidationError, validate
from marshmallow.validate import Length, Range
# from cerberus import Validator
# unins flask expects json


USER_BASE_URL = '/users'

def routes_user(app):
    def genApiKey():
        num = 20 
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
        return res
    # print(genApiKey())
    # print('==========')

    # LIB expects_json | kembalian bkn json ================================
    # schema = {
    #     # "type": "object",
    #     "properties": {
    #         "name": { "type": "string" },
    #         "email": { "type": "string" }
    #     },
    #     "required": ["email"]
    # }
    # ===================================================================

    # LIB RequestParser =================================================
    # video_update_args = reqparse.RequestParser()
    # video_update_args.add_argument("name", type=str, help="Name of the video is required")
    # video_update_args.add_argument("views", type=int, help="Views of the video")
    # video_update_args.add_argument("likes", type=int, help="Likes of the video")
    # ===================================================================


    # LIB cerberus | bingung custom response msg =============================
    # v = Validator()
    # schema = {
    #     'name': {
    #         'type': 'string', 
    #         'required' : True
    #     },
    #     'email': {
    #         'type': 'string', 
    #         'required' : True,
    #         'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    #     },
    #     'password': {
    #         'type': 'string', 
    #         'required' : True,
    #         'regex': '"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"'
    #     }
        
    # }
    # v.validate(request.json, schema)
    # if v.errors != []:
    #     return v.errors, 400
    # ===================================================================

    # marsmalow tp ga pake class, pake func
    # udh install marsmawlow trs coba

    class registerSchema(Schema):
        name = fields.Str(required=True)
        email = fields.Str(required=True, validate=validate.Email())
        password = fields.Str(required=True, validate=Length(min=8))

    @app.route(USER_BASE_URL + '/register', methods = ['POST'])
    # @expects_json(schema)
    def registerUser():
        errors = registerSchema().validate(request.json)
        if errors:
            return errors, 400
        # return 'lolos'

        auth = get_auth()
        try:
            user = auth.create_user_with_email_and_password(request.json['email'], request.json['password'])

            # insert user
            db = get_database()
            db.collection('user').document(user['localId']).set(
                {
                    "name": request.json["name"],
                    "email": request.json["email"],
                    "password": request.json["password"],
                    "api-key": genApiKey(),
                    "role": CUSTOMER,
                    "plan": 0,
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                }
            )
            
            return {'message': 'Register Success'}, 200
        except:
            return {'message': 'Email Already Exist'}, 400
        # except Exception as e:
        #     print('=============')
        #     print(e['error'])
        #     return {'message': e}, 400


    @app.route(USER_BASE_URL + '/registerAdmin', methods = ['POST'])
    def registerAdmin():
        errors = registerSchema().validate(request.json)
        if errors:
            return errors, 400

        auth = get_auth()
        try:
            user = auth.create_user_with_email_and_password(request.json['email'], request.json['password'])

            # insert user
            db = get_database()
            db.collection('user').document(user['localId']).set(
                {
                    "name": request.json["name"],
                    "email": request.json["email"],
                    "password": request.json["password"],
                    "role": ADMIN,
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                }
            )
            
            return {'message': 'Register Success'}, 200
        except Exception as e:
            return {'message': 'Email Already Exist'}, 400
            
    class loginSchema(Schema):
        email = fields.Str(required=True, validate=validate.Email())
        password = fields.Str(required=True, validate=Length(min=8))
        
    @app.route(USER_BASE_URL + '/login', methods = ['POST'])
    def login():
        errors = loginSchema().validate(request.json)
        if errors:
            return errors, 400

        auth = get_auth()

        email = request.json['email']
        password = request.json['password']
        try:
            user = auth.sign_in_with_email_and_password(email, password)
            # print(user)
            # user = auth.refresh(user['refreshToken'])
            # print(f'use auth refreshToken {user}')
            # user = user['userId']
            # print(f'user idToken {user_id}')
            # user = auth.get_account_info(user['idToken'])
            # print(f'get acc info {info}')
            
            return {'message': user}, 200
        except Exception as e:
            return {'message': 'Email / password invalid!'}, 400
        # except auth as e:
        # except exceptions.FirebaseError as exc:
            # print(exc.code)
            print(e.code)
            
        

    @app.route(USER_BASE_URL + '/resetPassword', methods = ['POST'])
    def resetPass():
        auth = get_auth()

        email = request.json['email']
        try:
            reset = auth.send_password_reset_email(email)
            
            return {'message': reset}, 200
        except :
        # except auth as e:
            # return {'message': 'Login Failed'}, 400
            return {'message': 'Email not found '}, 400
            

    @app.route(USER_BASE_URL + '/all', methods = ['GET'])
    # @check_token
    def getAllUser():
        users = User.get_all()
        return users
        
    @app.route(USER_BASE_URL + '/<id>', methods = ['GET'])
    def getUser(id):
        user = User.get_by_id(id)
        return user   

    @app.route(USER_BASE_URL, methods = ['POST'])
    def insertUser():
        User.insert(request.json)
        return {'message': 'Success Insert User'}

    @app.route(USER_BASE_URL + '/<id>', methods = ['PUT'])
    def updateUser(id):
        return User.update(id, request.json)
        
    @app.route(USER_BASE_URL + '/<id>', methods = ['DELETE'])
    def deleteUser(id):
        return User.delete(id)
