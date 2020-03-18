from ..configuracion import *

def create_report(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']

    datos = database.child('users').child(a).child('reports').get().val()['nameDataSet']
    name=database.child('users').child(a).child('details').get().val()['name']
    arreglo=[]
    arreglo.append(datos)
    print(arreglo[0])
    e=name
    return render(request,"createReport.html",{"arreglo":arreglo,"e":e})