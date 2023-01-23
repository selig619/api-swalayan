from flask_restful import Resource, Api, reqparse
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
        return request.json['name']
        return 'hai'