from flask import Flask
from flask_restful import Resource, Api, reqparse

from routes.UserController import routes_user  
from routes.DatasetController import routes_dataset
from routes.TransactionController import routes_transaction
from configs.firebase import get_auth, get_database, get_storage, init_firebase

app = Flask(__name__)
api = Api(app)

# api.add_resource(Users,'/users')

init_firebase()
db = get_database()
auth = get_auth()
storage = get_storage()


routes_user(app)
routes_dataset(app)
routes_transaction(app)


if __name__ == '__main__':
    # app.run(debug=True, port=5000)
    app.run()