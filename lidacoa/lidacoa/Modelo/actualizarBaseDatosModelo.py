from ..configuracion import *

def actualizarBaseDatos(request):
    aux=request.POST.get('aux')
    aux = aux[0:len(aux) - 1]
    aux = aux.split(",")
    print("arreglo1: " + str(aux))
    for i in aux:
        nameDataBase = i[2:len(i) - 1]
        help = request.POST.get(nameDataBase)
        if str(help) == "ACTUALIZAR":
            print("Entra actualizar")
            basesDatos=database.child("bases_Datos").get()
            for baseDatos in basesDatos:
                if str(baseDatos.val()['nameDataBase']) == str(nameDataBase):
                    idDataBase=baseDatos.key()
                    api_key=baseDatos.val()['api_key']
                    customer_id=baseDatos.val()['customer_id']
                    nameDataBase=baseDatos.val()['nameDataBase']
                    passw=baseDatos.val()['pass']
                    platform=baseDatos.val()['platform']
                    requestor_id=baseDatos.val()['requestor_id']
                    url=baseDatos.val()['url']
                    user=baseDatos.val()['user']
                    return render(request, 'actualizarBaseDatos.html', {"idDataBase": idDataBase, "api_key":api_key, "customer_id":customer_id, "nameDataBase":nameDataBase, "passw":passw, "platform":platform, "requestor_id":requestor_id, "url":url, "user":user})
        elif str(help) == "ELIMINAR":
            print("Entra")
            basesDatos = database.child("bases_Datos").get()
            for baseDatos in basesDatos:
                if str(baseDatos.val()['nameDataBase']) == str(nameDataBase):
                    idDataBase=baseDatos.key()
                    database.child("bases_Datos").child(idDataBase).remove()
                    return render(request, 'eliminarBaseDatos.html', {"nombre":nameDataBase})
        else:
            None


def actualizar(request):
    nuevaInformacion={
        "api_key":request.POST.get('api_key'),
        "customer_id":request.POST.get('customer_id'),
        "name":request.POST.get('nameDataBase'),
        "pass":request.POST.get('pass'),
        "platform":request.POST.get('platform'),
        "requestor_id":request.POST.get('requestor_id'),
        "url":request.POST.get('url'),
        "user":request.POST.get('user')
    }
    database.child("bases_Datos").child(request.POST.get('id')).update(nuevaInformacion)
    return render(request, 'welcome.html')