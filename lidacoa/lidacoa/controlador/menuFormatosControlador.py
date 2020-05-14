"""from ..configuracion import *

def menuFormatos(request):
    return render(request,"menuFormatos.html")

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
    return render(request, "verFormatoConsulta.html", {"nombreFormato": nombre, "idFormato": idFormato})"""