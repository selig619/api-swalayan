import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'models')))
from models.User import User
from flask import request
from configs.firebase import get_auth, get_database


USER_BASE_URL = '/users'

def routes_user(app):
    @app.route(USER_BASE_URL + '/register', methods = ['POST'])
    def registerUser():
        auth = get_auth()
        try:
            user = auth.create_user_with_email_and_password(request.json['email'], request.json['password'])

            # insert user
            db = get_database()
            db.collection('user').add(
                request.json
            )
            # error pas insert lama pol jd deadline exceeded
            return 'ok'
        except:
            return {'message': 'Email Already Exist'}, 400

    @app.route(USER_BASE_URL + '/all', methods = ['GET'])
    def getAllUser():
        # print(sys.path.append(os.path.abspath(os.path.join('..', 'configs'))))
        print('halo')
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
