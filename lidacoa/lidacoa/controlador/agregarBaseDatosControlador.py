from ..configuracion import *

def agregarBaseDatos(request):
    formatos = database.child('formatos').get()
    arregloFormatos=[]
    for formato in formatos.each():
        arregloFormatos.append(formato.val()['Report_Id'])
    return render(request,"agregarBaseDatos.html",{"arregloFormatos" : arregloFormatos})