from ..configuracion import *

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
