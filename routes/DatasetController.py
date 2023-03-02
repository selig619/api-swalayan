from models.Dataset import Dataset
from configs.firebase import get_auth, get_database
from utils.middleware import check_token


from firebase_admin import firestore
from flask import request
from datetime import datetime, timezone, timezone
from marshmallow import Schema, fields, ValidationError, validate
from marshmallow.validate import Length, Range


USER_BASE_URL = '/datasets'

def routes_dataset(app):

    @app.route(USER_BASE_URL + '/all', methods = ['GET'])
    # @check_token
    def getAllDs():
        ds = Dataset.get_all()
        return ds
        

    @app.route(USER_BASE_URL, methods = ['POST'])
    # @check_token
    def insertDs():
        # insert datasets
        try:
            db = get_database()
            add_time, ds_ref = db.collection('dataset').add(
                {
                    "ds_name": request.json["name"],
                    # "user_id": request.user['uid'],
                    "user_id": 'seseorang',
                    "created_at": datetime.now(timezone.utc),
                    "updated_at": datetime.now(timezone.utc)
                }
            )

            for x in range(len(request.json['transactions'])):
                trans_ref = db.collection('transaction').add(
                    {
                        "dataset_id": ds_ref.id,
                        "trans_id": request.json["transactions"][x]['trans_id'],
                        "items" : request.json["transactions"][x]['items']
                    }
                )

            # bingung data di firestore dbkin satu2 kek di db??
            
            return {'message': 'Insert Success'}
            # return {'message': f"{ds_ref.id} is created at {add_time}"}
        except:
            return {'message': 'Insert Failed'}
            