from ..configuracion import *

def descargar(request):
    for i in range(0,len(arregloDescarga)):
        arregloDescarga.pop()
    baseDatos = database.child('bases_Datos').get()
    nombreBaseDatos = []
    for i in baseDatos.each():
        nombreBaseDatos.append(i.val()['nameDataBase'])

    formatos = database.child('formatos').get()
    nombreFormatos = []
    for i in formatos.each():
        informacionFormato = i.val()
        nombreFormato = informacionFormato.get('Report_Id')
        nombreFormatos.append(nombreFormato)

    return render(request,"descargarInformacion.html",{"arregloBasesDatos" : nombreBaseDatos, "arregloFormatos":nombreFormatos})