import pyrebase as pb
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account.

firebase = None

def init_firebase():
    global firebase

    config = {
        'apiKey': "AIzaSyCO0n3pln59pmtGR9nNECnvRjfNnriRsy8",
        'authDomain': "ta-supermarket-1f444.firebaseapp.com",
        'databaseURL': "https://ta-supermarket-1f444-default-rtdb.asia-southeast1.firebasedatabase.app",
        'projectId': "ta-supermarket-1f444",
        'storageBucket': "ta-supermarket-1f444.appspot.com",
        'messagingSenderId': "673810078830",
        'appId': "1:673810078830:web:b733a2013db87e0ca55a7f",
        'measurementId': "G-L9V2YYG0S8"
    }

    cred = credentials.Certificate('key-supermarket.json')
    # firebase = firebase_admin.initialize_app(cred)
    firebase = pyrebase.initialize_app(config)

def get_database():
    # return firebase.client()
    return firebase.database()

