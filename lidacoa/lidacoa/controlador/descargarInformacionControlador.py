from ..configuracion import *

def descargar(request):
    baseDatos = database.child('bases_Datos').get()
    nombreBaseDatos = []
    for i in baseDatos:
        nombreBaseDatos.append(i.val()['nameDataBase'])
    print(nombreBaseDatos)
    return render(request,"descargarInformacion.html",{"arregloBasesDatos" : nombreBaseDatos})