"""from ..configuracion import *

def actualizar(request):
    arregloFormatos = []
    formatos = database.child('formatos').get()
    for formato in formatos.each():
        nombreFormato = formato.val()['Report_Id']
        if request.POST.get(nombreFormato) == "1":
            arregloFormatos.append(nombreFormato)
    nuevaInformacion={
        "api_key":request.POST.get('api_key'),
        "customer_id":request.POST.get('customer_id'),
        "name":request.POST.get('nameDataBase'),
        "pass":request.POST.get('pass'),
        "platform":request.POST.get('platform'),
        "requestor_id":request.POST.get('requestor_id'),
        "url":request.POST.get('url'),
        "user":request.POST.get('user'),
        "formatos": arregloFormatos,
    }
    database.child("bases_Datos").child(request.POST.get('id')).update(nuevaInformacion)
    return render(request, 'welcome.html')

def eliminarBaseDatos(request):
    dataBaseSelected = request.GET.get('bbd')
    basesDatos = database.child("bases_Datos").get()
    print(basesDatos)
    for baseDatos in basesDatos.each():
        if str(baseDatos.val()['nameDataBase']) == str(dataBaseSelected):
            idDataBase = baseDatos.key()
            database.child("bases_Datos").child(idDataBase).remove()
            return render(request, 'eliminarBaseDatos.html', {"nombre": dataBaseSelected})
        else:
            None

def agregar(request):
    dataBaseSelected=request.GET.get('bbd')
    basesDatos = database.child("bases_Datos").get()
    formatos=database.child("formatos").get()
    arregloFormatos=[]
    for formato in formatos.each():
        arregloFormatos.append(formato.val()['Report_Id'])

    for baseDatos in basesDatos.each():
        if str(baseDatos.val()['nameDataBase']) == str(dataBaseSelected):
            idDataBase = baseDatos.key()
            api_key = baseDatos.val()['api_key']
            customer_id = baseDatos.val()['customer_id']
            nameDataBase = baseDatos.val()['nameDataBase']
            passw = baseDatos.val()['pass']
            platform = baseDatos.val()['platform']
            requestor_id = baseDatos.val()['requestor_id']
            url = baseDatos.val()['url']
            user = baseDatos.val()['user']
            arregloFormatosBaseDatos = baseDatos.val()['formatos']
            return render(request, 'actualizarBaseDatos.html', {"idDataBase": idDataBase, "api_key": api_key, "customer_id": customer_id, "nameDataBase": nameDataBase, "passw": passw, "platform": platform, "requestor_id": requestor_id, "url": url, "user": user, "arregloFormatosBaseDatos": arregloFormatosBaseDatos, "arregloFormatos": arregloFormatos})
        else:
            None"""