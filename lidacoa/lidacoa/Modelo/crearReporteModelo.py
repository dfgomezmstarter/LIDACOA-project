from ..configuracion import *

def create_report(requets):
    email = requets.POST.get('nameDataSet')
    print(email)
    idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']

    datos= database.child('users').child(a).child('reports').get().val()['nameDataSet']

    return render(requets,'welcome.html')