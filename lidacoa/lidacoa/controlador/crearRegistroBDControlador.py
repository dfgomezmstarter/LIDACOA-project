from ..configuracion import *

def create_report(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    # database.child('bases_Datos').child("d0oIsERZMEMziEvqotmB6bBFjsu2").remove() Para eliminar un registro

    basesDatos=database.child('bases_Datos').get()
    nombreBasesDatos=[]
    for i in basesDatos.each():
        informacionBaseDatos=i.val()
        nombre=informacionBaseDatos.get('nameDataBase')
        nombreBasesDatos.append(nombre)

    name=database.child('users').child(a).child('details').get().val()['name']
    e = name
    return render(request,"createReport.html",{"arregloBasesDatos":nombreBasesDatos,"e":e})