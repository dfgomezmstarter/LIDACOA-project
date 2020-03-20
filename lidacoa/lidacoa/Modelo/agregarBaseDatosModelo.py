from ..configuracion import *

def agregarBaseDatos(request):
    name =request.POST.get('nameDataBase')
    url = request.POST.get('url')
    user = request.POST.get('user')
    passw = request.POST.get('pass')

    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a =a['users']
    a =a[0]
    a =a['localId']
    data = {
        "nameDataBase":name,
        'url':url,
        'user':user,
        'pass':passw
    }
    database.child('bases_Datos').push(data)
    email=database.child('users').child(a).child('details').get().val()['name']
    return render(request,'welcome.html',{"e":email})