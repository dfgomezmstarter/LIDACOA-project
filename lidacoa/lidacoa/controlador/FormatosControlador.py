from ..configuracion import *

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
    mensaje = "Se agrego correctamente el formato"
    return render(request,'menuFormatos.html',{"e":email, "mensaje":mensaje})

def actualizar(request):
    actualizar = request.GET.get('id')
    nuevaInformacion={
        "Report_Id":request.POST.get('reporteID'),
        "descripcion":request.POST.get('details'),
        "nombre":request.POST.get('name'),
    }
    print("valor: ")
    print(str(actualizar))
    print("id: " + str(request.POST.get('id')))
    database.child("formatos").child(actualizar).update(nuevaInformacion)
    mensaje = "Se actualizó correctamente el formato " + str(request.POST.get('reporteID'))
    return render(request, 'menuFormatos.html',{"mensaje":mensaje})

def eliminarFormato(request):
    formatoSelected = request.GET.get('idFormato')
    formatos = database.child("formatos").get()
    for formato in formatos.each():
        if str(formato.val()['Report_Id']) == str(formatoSelected):
            idFormatoDelete = formato.key()
            database.child("formatos").child(idFormatoDelete).remove()
            mensaje = "Se Elimino correctamente el formato " + str(formatoSelected)
            return render(request, 'menuFormatos.html', {"mensaje": mensaje})
        else:
            None

def agregar(request):
    formatoSelected=request.GET.get('idFormato')
    formatos = database.child("formatos").get()
    for formato in formatos.each():
        if str(formato.val()['Report_Id']) == str(formatoSelected):
            idFormatoBD = formato.key()
            idFormatoActualizar = formato.val()['Report_Id']
            nombreFormato = formato.val()['nombre']
            descripcionFormato = formato.val()['descripcion']
            return render(request, 'actualizarFormato.html', {"idFormatoBD": idFormatoBD, "idFormatoActualizar": idFormatoActualizar, "nombreFormato": nombreFormato, "descripcionFormato": descripcionFormato})
        else:
            None


def menuFormatos(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']

    email = database.child('users').child(a).child('details').get().val()['name']
    return render(request,"menuFormatos.html",{"e":email})

def agregarFormato(request):
    return render(request,"agregarFormato.html")

def verFormatos(request):
    formatos = database.child('formatos').get()
    arregloFormatos = []
    for i in formatos.each():
        informacionFormatos = i.val()
        idFormato = informacionFormatos.get('Report_Id')
        arregloFormatos.append(idFormato)
    return render(request, "verFormatos.html", {"arregloformatos": arregloFormatos})

def verFormatoConsulta(request):
    formatos = database.child('formatos').get()
    formatoSelected = request.GET.get('form')

    for i in formatos.each():
        informacionFormatos = i.val()
        if informacionFormatos.get('Report_Id') == str(formatoSelected):
            nombre = formatoSelected
            idFormato = i.key()

    print("for: " + str(nombre) )
    return render(request, "verFormatoConsulta.html", {"nombreFormato": nombre, "idFormato": idFormato})