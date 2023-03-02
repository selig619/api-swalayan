from models.Transaction import Transaction
from configs.firebase import get_auth, get_database

from datetime import datetime, timezone
from flask import request
from marshmallow import Schema, fields, ValidationError, validate
from marshmallow.validate import Length, Range



USER_BASE_URL = '/transactions'

def routes_transaction(app):
    @app.route(USER_BASE_URL, methods = ['POST'])
    def insertTrans():
        # Dataset.insert(request.json)

        # insert datasets
        return {'message': 'Success Insert User'}
    
    @app.route(USER_BASE_URL + '/all', methods = ['GET'])
    # @check_token
    def getAllTrans():
        trans = Transaction.get_all()

        # db = get_database()
        # docs = db.collection('transactions').stream()
        # temp=[]
        # for doc in docs:
            # temp.append(doc)
            # print(f'{doc.id} => {doc.to_dict()}')
        

        return trans