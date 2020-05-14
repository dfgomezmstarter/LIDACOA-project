"""from ..configuracion import *

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
    
    data={"name":name}
    database.child("users").child(uid).child("details").set(data)

    return render(request,"signIn.html")"""