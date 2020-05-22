from ..configuracion import *
from django.shortcuts import render
from ..configuracion import authe

def signIn(request):
    return render(request, "signIn.html")

def logout(request):
    auth.logout(request)
    return render(request,'signIn.html')

def signUp(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').get().val()['name']
    return render(request,"signUp.html",{"e":name})

def postsign(requets):
    """idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').get().val()['name']"""
    email = requets.POST.get('email')
    passw = requets.POST.get("pass")
    consultas = database.child('Consulta').get()
    try:
        for i in consultas.each():
            agregarConfiguracion(arregloFaltantes,diccionario, i.val()['Base de Datos'], i.val()['Fecha de Inicio'], i.val()['Fecha de Fin'],i.val()['Formato'])
        user = authe.sign_in_with_email_and_password(email, passw)
    except:
        try:
            user= authe.sign_in_with_email_and_password(email,passw)
        except:
            message= "credencial invalida"
            return render(requets,"signIn.html",{"messg":message})
    session_id=user['idToken']
    requets.session['uid']=str(session_id)
    return render(requets, "welcome.html")


def postsignup(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    passw = request.POST.get('pass')

    try:
        user = authe.create_user_with_email_and_password(email, passw)
        uid = user['localId']
    except:
        message = "Unable to create acocount try again"
        return render(request, "signUp.html", {"messg": message})

    data = {"name": name}
    database.child("users").child(uid).child("details").set(data)

    return render(request, "welcome.html")