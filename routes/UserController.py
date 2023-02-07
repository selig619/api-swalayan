
import sys, os

sys.path.append(os.path.abspath(os.path.join('..', 'models')))
from models.User import User
from flask import request

# class Users(Resource):
#     def get(self):
#         return 'ini users'

#     def post(self):
#         return request.json

USER_BASE_URL = '/user'

def routes_user(app):
    @app.route(USER_BASE_URL + '/all', methods = ['GET'])
    def getAllUser():
        users = User.get_all()
        return users
        
    @app.route(USER_BASE_URL + '/<id>', methods = ['GET'])
    def getUser(id):
        user = User.get_by_id(id)
        return user