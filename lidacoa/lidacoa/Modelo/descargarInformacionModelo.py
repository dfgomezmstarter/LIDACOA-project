from ..configuracion import *
import pandas as pd


def descargar(request):
    print("entro")
    data = {}
    nombre_BaseDatos = request.POST.get('nombreBaseDatos')
    fechaInicial = request.POST.get('fechaInicial')
    fechaFinal = request.POST.get('fechaFinal')
    formato = request.POST.get('formato')

    print(str(nombre_BaseDatos) + str(fechaInicial) + str(fechaFinal) + str(formato))

    consultas = database.child('Consulta').get()
    for i in consultas:
        if i.val()['fechaInicio'] == fechaInicial and i.val()['fechaFinal'] == fechaFinal and i.val()['nombreBaseDatos'] == nombre_BaseDatos and i.val()['formatoConsulta'] == formato:
            data = {
                'Base_Datos': i.val()['nombreBaseDatos'],
                'Fecha Inicial': i.val()['fechaInicio'],
                'Fecha Final': i.val()['fechaFinal'],
                'Formato': i.val()['formatoConsulta'],
                'Total': i.val()['totalReporte']
            }
    print(str(data))
    df = pd.DataFrame(data, columns=['Base_Datos', 'Fecha Inicial', 'Fecha Final', 'Formato', 'Total'])
    # df['Total'].sum()
    df.to_excel('Reporte Consultas', sheet_name='registro')
    #file_to_Excel(data)


def file_to_Excel(file):
    df = pd.DataFrame(file, columns=['Base_Datos', 'Fecha Inicial', 'Fecha Final', 'Formato', 'Total'])
    # df['Total'].sum()
    df.to_excel('Reporte Consultas', sheet_name='registro')
