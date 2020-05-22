from ..configuracion import *

def agregarBaseDatos(request):
    formatos = database.child('formatos').get()
    arregloFormatos=[]
    for formato in formatos.each():
        arregloFormatos.append(formato.val()['Report_Id'])
    return render(request,"agregarBaseDatos.html",{"arregloFormatos" : arregloFormatos})

def menuBaseDatosBibliograficas(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    email = database.child('users').child(a).child('details').get().val()['name']
    return render(request,"menuBaseDatosBibliografica.html",{"e":email})

def verBaseDatos(request):
    basesDatos = database.child('bases_Datos').get()
    nombreBasesDatos = []
    idBasesDatos = []
    for i in basesDatos.each():
        informacionBaseDatos = i.val()
        nombre = informacionBaseDatos.get('nameDataBase')
        nombreBasesDatos.append(nombre)
        keyBaseDatos = i.key()
        idBasesDatos.append(keyBaseDatos)

    return render(request, "verBasesDatosBibliograficas.html", {"arregloBasesDatos": nombreBasesDatos, "idBasesDatos": idBasesDatos})

def verBaseDatosConsulta(request):
    basesDatos = database.child('bases_Datos').get()
    dataBaseSelected = request.GET.get('bd')

    for i in basesDatos.each():
        informacionBaseDatos = i.val()
        if informacionBaseDatos.get('nameDataBase') == str(dataBaseSelected):
            nombre = dataBaseSelected
            idBaseDatos = i.key()

    return render(request, "verBaseDatosConsulta.html", {"nombreBaseDatos": nombre, "idBaseDatos": idBaseDatos})

def actualizar(request):
    actualizarBD = request.GET.get('id')
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
    database.child("bases_Datos").child(actualizarBD).update(nuevaInformacion)
    mensaje = "Se actualizó correctamente la Base de Datos " + str(request.POST.get('nameDataBase'))
    return render(request, 'menuBaseDatosBibliografica.html', {"mensaje": mensaje})

def eliminarBaseDatos(request):
    dataBaseSelected = request.GET.get('bbd')
    basesDatosNombre = dataBaseSelected
    basesDatos = database.child("bases_Datos").get()
    reportes = database.child("Consulta").get()
    for baseDatos in basesDatos.each(): # Se elimina la BD bibliográfica de la BD
        if str(baseDatos.val()['nameDataBase']) == str(dataBaseSelected):
            for consultas in reportes.each():  # Se eliminan las consultas que se hallan hecho con esa BD bibliografica.
                idConsulta = consultas.key()
                if str(consultas.val()['Base de Datos']) == str(basesDatosNombre):
                    database.child("Consulta").child(idConsulta).remove()
            idDataBase = baseDatos.key()
            eliminarReportesDiccionario(database.child("bases_Datos").child(idDataBase).get().val()['nameDataBase'])
            database.child("bases_Datos").child(idDataBase).remove()
    consultas2 = database.child('Consulta').get()
    try:
        for i in consultas2.each():
            agregarConfiguracion(arregloFaltantes,diccionario, i.val()['Base de Datos'], i.val()['Fecha de Inicio'], i.val()['Fecha de Fin'],i.val()['Formato'])
        mensaje = "Se Elimino correctamente la Base de Datos "
        return render(request, 'menuBaseDatosBibliografica.html', {"mensaje": mensaje})
    except:
        mensaje = "Se Elimino correctamente la Base de Datos "
        return render(request, 'menuBaseDatosBibliografica.html', {"mensaje": mensaje})

def eliminarReportesDiccionario (nombreBD):
    for i in diccionario:
        if nombreBD in i:
            diccionario[i] = []

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
            None


def agregarBaseDatosFormulario(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a =a['users']
    a =a[0]
    a =a['localId']
    arregloFormatos=[]
    formatos = database.child('formatos').get()
    for formato in formatos.each():
        nombreFormato=formato.val()['Report_Id']
        if request.POST.get(nombreFormato) == "1":
            arregloFormatos.append(nombreFormato)

    data = {
        "api_key": request.POST.get('api_key'),
        "customer_id": request.POST.get('customer_id'),
        "nameDataBase": request.POST.get('nameDataBase'),
        "pass": request.POST.get('pass'),
        "platform": request.POST.get('platform'),
        "requestor_id": request.POST.get('requestor_id'),
        "url": request.POST.get('url'),
        "user": request.POST.get('user'),
        "formatos" : arregloFormatos,
    }

    database.child('bases_Datos').push(data)
    email=database.child('users').child(a).child('details').get().val()['name']
    mensaje = "Se agrego correctamente la Base de Datos "
    return render(request,'menuBaseDatosBibliografica.html', {"mensaje": mensaje, "e":email})