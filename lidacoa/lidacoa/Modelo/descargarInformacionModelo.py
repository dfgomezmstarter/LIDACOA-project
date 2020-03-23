from ..configuracion import *
import pandas as pd


def descargar(request):
    aux = request.POST.get('aux')
    aux = aux[0:len(aux) - 1]
    aux = aux.split(",")
    arreglo = []
    for i in aux:
        valor = i[2:len(i) - 1]
        help = request.POST.get(valor)
        if str(help) == "1":
            data = {}
            nombre_BaseDatos = request.POST.get('nombreBaseDatos')
            fechaInicial = request.POST.get('fechaInicial')
            fechaFinal = request.POST.get('fechaFinal')
            formato = request.POST.get('formato')
            total = request.POST.get('totalReporte')

            consultas = database.child('Consulta').get()
            for i in consultas:
                if consultas.val()['fechaInicio'] == fechaInicial and consultas.val()['fechaFinal'] == fechaFinal and \
                        consultas.val()['nombreBaseDatos'] == nombre_BaseDatos and consultas.val()[
                    'formatoConsulta'] == formato and consultas.val()['totalReporte'] == total:
                    data = {
                        'Base_Datos': consultas.val()['nombreBaseDatos'],
                        'Fecha Inicial': consultas.val()['fechaInicio'],
                        'Fecha Final': consultas.val()['fechaFinal'],
                        'Formato': consultas.val()['formatoConsulta'],
                        'Total': consultas.val()['totalReporte']
                    }
            print(data)
            file_to_Excel(data)


def file_to_Excel(file):
    df = pd.DataFrame(file, columns=['Base_Datos', 'Fecha Inicial', 'Fecha Final', 'Formato', 'Total'])
    # df['Total'].sum()
    df.to_excel('Reporte Consultas', sheet_name='registro')
