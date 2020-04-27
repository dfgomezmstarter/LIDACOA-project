from ..configuracion import *

def menuBaseDatosBibliograficas(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    email = database.child('users').child(a).child('details').get().val()['name']
    return render(request,"menuBaseDatosBibliografica.html",{"e":email})