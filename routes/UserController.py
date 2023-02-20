import sys, os 
import string, secrets
from flask_expects_json import expects_json

sys.path.append(os.path.abspath(os.path.join('..', 'models')))
from models.User import User
from flask import request
from configs.firebase import get_auth, get_database
from datetime import datetime



USER_BASE_URL = '/users'

def routes_user(app):
    def genApiKey():
        num = 20 
        res = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(num))  
        return res
    # print(genApiKey())
    # print('==========')

    schema = {
        # "type": "object",
        "properties": {
            "name": { "type": "string" },
            "email": { "type": "string" }
        },
        "required": ["email"]
    }

    @app.route(USER_BASE_URL + '/register', methods = ['POST'])
    @expects_json(schema)
    def registerUser():
        auth = get_auth()
        try:
            # user = auth.create_user_with_email_and_password(request.json['email'], request.json['password'])

            # insert user
            # db = get_database()
            # db.collection('user').add(
            #     {
            #         "name": request.json["name"],
            #         "email": request.json["email"],
            #         "password": request.json["password"],
            #         "api-key": genApiKey(),
            #         "role": 'user',
            #         "plan": 0,
            #         "created_at": datetime.now(),
            #         "updated_at": datetime.now()
            #     }
            # )
            
            return {'message': 'Register Success'}, 200
        except:
            return {'message': 'Email Already Exist'}, 400


    @app.route(USER_BASE_URL + '/registerAdmin', methods = ['POST'])
    def registerAdmin():
        auth = get_auth()
        try:
            user = auth.create_user_with_email_and_password(request.json['email'], request.json['password'])

            # insert user
            db = get_database()
            db.collection('user').add(
                request.json
            )
            
            return {'message': 'Register Success'}, 200
        except:
            return {'message': 'Email Already Exist'}, 400

    @app.route(USER_BASE_URL + '/all', methods = ['GET'])
    def getAllUser():
        # print(sys.path.append(os.path.abspath(os.path.join('..', 'configs'))))
        # print('halo')
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
