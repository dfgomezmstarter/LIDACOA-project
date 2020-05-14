"""from ..configuracion import *

def post_create(request):
    name =request.POST.get('nameDataSet')
    url = request.POST.get('url')
    user = request.POST.get('user')
    passw = request.POST.get('pass')

    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a =a['users']
    a =a[0]
    a =a['localId']
    data = {
        "nameDataSet":name,
        'url':url,
        'user':user,
        'pass':passw
    }
    database.child('users').child(a).child('reports').push(data)
    email=database.child('users').child(a).child('details').get().val()['name']
    return render(request,'welcome.html',{"e":email})"""