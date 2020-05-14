"""from ..configuracion import *

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

    return render(request, "verBaseDatosConsulta.html", {"nombreBaseDatos": nombre, "idBaseDatos": idBaseDatos})"""
