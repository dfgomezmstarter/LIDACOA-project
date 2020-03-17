from django.shortcuts import  render
import pyrebase
from django.contrib import auth



config = {
    'apiKey': "AIzaSyAGBKr0cSU1ocPy7SXxIBBuTylDBxHmD-o",
    'authDomain': "lidacoa.firebaseapp.com",
    'databaseURL': "https://lidacoa.firebaseio.com",
    'projectId': "lidacoa",
    'storageBucket': "lidacoa.appspot.com",
    'messagingSenderId': "696040231838",
    'appId': "1:696040231838:web:a0ff0aec08cf241b727c8f",
    'measurementId': "G-0PC4JJMEWH"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
