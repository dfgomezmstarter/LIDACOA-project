"""""
from django.shortcuts import  render
import pyrebase
from django.contrib import auth
"""""
"""""
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

database=firebase.database()
"""
"""""
def postsign(requets):
    email = requets.POST.get('email')
    passw = requets.POST.get("pass")
    try:
        user= authe.sign_in_with_email_and_password(email,passw)
    except:
        message= "credencial invalida"
        return render(requets,"signIn.html",{"messg":message})
    session_id=user['idToken']
    requets.session['uid']=str(session_id)
    return render(requets, "welcome.html",{"e":email})
"""

"""""
def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')
"""
"""""
def signUp(request):
    return render(request,"signUp.html")
"""""
"""""
def postsignup(request):
    name = request.POST.get('name')
    email=request.POST.get('email')
    passw = request.POST.get('pass')

    try:
        user=authe.create_user_with_email_and_password(email,passw)
        uid = user['localId']
    except:
        message ="Unable to create acocount try again"
        return  render(request,"signUp.html",{"messg": message})
        #uid = user['localId']

    #data={"name":name,"status":"1"}
    #database.child("users").child(uid).child("details").set(data)

    return render(request,"signIn.html")
"""""
"""""
def post_create(request):
    name =request.POST.get('nameDataSet')
    url = request.POST.get('url')
    user = request.POST.get('user')
    passw = request.POST.get('pass')

    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a =a['users']
    a =a[0]
    a =a['localId']
    print(str(a))
    data = {
        "nameDataSet":name,
        'url':url,
        'user':user,
        'pass':passw
    }
    database.child('users').child(a).child('reports').set(data)
    return render(request,'welcome.html')
"""""