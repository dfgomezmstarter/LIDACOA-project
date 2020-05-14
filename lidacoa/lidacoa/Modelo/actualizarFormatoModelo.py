"""from ..configuracion import *

def actualizar(request):
    nuevaInformacion={
        "Report_Id":request.POST.get('reporteID'),
        "descripcion":request.POST.get('details'),
        "nombre":request.POST.get('name'),
    }
    print("id: " + str(request.POST.get('id')))
    database.child("formatos").child(request.POST.get('id')).update(nuevaInformacion)
    return render(request, 'welcome.html')

def eliminarFormato(request):
    formatoSelected = request.GET.get('idFormato')
    formatos = database.child("formatos").get()
    for formato in formatos:
        if str(formato.val()['Report_Id']) == str(formatoSelected):
            idFormatoDelete = formato.key()
            database.child("formatos").child(idFormatoDelete).remove()
            return render(request, 'eliminarFormato.html', {"nombre": formatoSelected})
        else:
            None

def agregar(request):
    formatoSelected=request.GET.get('idFormato')
    formatos = database.child("formatos").get()
    for formato in formatos:
        if str(formato.val()['Report_Id']) == str(formatoSelected):
            idFormatoBD = formato.key()
            idFormatoActualizar = formato.val()['Report_Id']
            nombreFormato = formato.val()['nombre']
            descripcionFormato = formato.val()['descripcion']
            return render(request, 'actualizarFormato.html', {"idFormatoBD": idFormatoBD, "idFormatoActualizar": idFormatoActualizar, "nombreFormato": nombreFormato, "descripcionFormato": descripcionFormato})
        else:
            None"""