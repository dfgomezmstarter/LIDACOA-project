from ..configuracion import *

def create_report(requets):
    email = requets.POST.get('formato')
    bd = requets.POST.get('basesDeDatos')
    print("formato: " + str(email) + " bd: " + str(bd))
    idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']


    #datos= database.child('bases_Datos').child(a).get().val()['nameDataSet']
    #print(datos)

    return render(requets,'welcome.html')