from ..configuracion import *

def agregarBaseDatos(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a =a['users']
    a =a[0]
    a =a['localId']
    data = {
        "api_key": request.POST.get('api_key'),
        "customer_id": request.POST.get('customer_id'),
        "nameDataBase": request.POST.get('nameDataBase'),
        "pass": request.POST.get('pass'),
        "platform": request.POST.get('platform'),
        "requestor_id": request.POST.get('requestor_id'),
        "url": request.POST.get('url'),
        "user": request.POST.get('user')
    }

    database.child('bases_Datos').push(data)
    email=database.child('users').child(a).child('details').get().val()['name']
    return render(request,'welcome.html',{"e":email})