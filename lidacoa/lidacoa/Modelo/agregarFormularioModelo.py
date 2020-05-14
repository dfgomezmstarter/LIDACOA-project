"""from ..configuracion import *

def agregarFormulario(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a =a['users']
    a =a[0]
    a =a['localId']
    idMayuscula=request.POST.get('reporteID')
    idMayuscula=idMayuscula.upper()
    data = {
        "Report_Id": idMayuscula,
        "nombre": request.POST.get('name'),
        "descripcion": request.POST.get('details'),
    }

    database.child('formatos').push(data)
    email=database.child('users').child(a).child('details').get().val()['name']
    return render(request,'welcome.html',{"e":email})"""