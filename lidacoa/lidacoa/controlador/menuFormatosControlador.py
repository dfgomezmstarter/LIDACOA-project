from ..configuracion import *

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