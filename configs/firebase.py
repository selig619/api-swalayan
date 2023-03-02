import pyrebase as pb
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Use a service account.

pyrebaseLib = None
firestoreDb = None

def init_firebase():

    # init pyrebase
    global pyrebaseLib

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

    pyrebaseLib = pb.initialize_app(config)

    # init firestore
    global firestoreDb

    cred = credentials.Certificate("key-supermarket.json")
    firebase_admin.initialize_app(cred)

    firestoreDb = firestore.client()


def get_database():
    return firestoreDb

def get_auth():
    return pyrebaseLib.auth()

def get_storage():
    return pyrebaseLib.storage()

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

# cred = credentials.Certificate('key-supermarket.json')
# firebase = firebase_admin.initialize_app(cred)

# firebase = pyrebase.initialize_app(config)
# db = firebase.database()
# auth = firebase.auth()

# email = "selig668@gmail.com"
# password = "12345678"

# auth.create_user_with_email_and_password(email, password)
# user = auth.sign_in_with_email_and_password(email, password)
# token = user['idToken']
# print(user)

# storage = firebase.storage()
# storage.child("folder1/folder2/contoh.jpg").put("./resources/aplikasi.png")
# storage.child("folder1/folder2/contoh.jpg").download("","download1.jpg")

# url = storage.child("folder1/folder2/contoh.jpg").get_url(token)
# print(url)
