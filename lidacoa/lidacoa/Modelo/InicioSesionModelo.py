"""from django.shortcuts import render
from ..configuracion import authe

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
    return render(requets, "welcome.html",{"e":email})"""