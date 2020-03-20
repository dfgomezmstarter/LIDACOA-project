from ..configuracion import *

def create_report(requets):
    aux = requets.POST.get('aux')
    aux = aux[0:len(aux)-1]
    aux = aux.split(",")
    arreglo=[]
    for i in aux:
        valor=i[2:len(i)-1]
        help = requets.POST.get(valor)
        if str(help) == "1":
            arreglo.append(valor)
    print("Arreglo de base de datos: " +str(arreglo)) # Mostrar el arreglo de las bdb que se seleccionaron
    email = requets.POST.get('formato')
    #bd = requets.POST.get('basesDeDatos')
    print("formato: " + str(email))
    idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']



    #datos= database.child('bases_Datos').child(a).get().val()['nameDataSet']
    #print(datos)

    return render(requets,'welcome.html')