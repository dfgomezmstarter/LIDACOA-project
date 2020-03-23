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
        if consultas.val()['fechaInicio'] == fechaInicial and consultas.val()['fechaFinal'] == fechaFinal and consultas.val()['nombreBaseDatos'] == nombre_BaseDatos and consultas.val()['formatoConsulta'] == formato:
            data = {
                'Base_Datos': consultas.val()['nombreBaseDatos'],
                'Fecha Inicial': consultas.val()['fechaInicio'],
                'Fecha Final': consultas.val()['fechaFinal'],
                'Formato': consultas.val()['formatoConsulta'],
                'Total': consultas.val()['totalReporte']
            }
    print(str(data))
    file_to_Excel(data)


def file_to_Excel(file):
    df = pd.DataFrame(file, columns=['Base_Datos', 'Fecha Inicial', 'Fecha Final', 'Formato', 'Total'])
    # df['Total'].sum()
    df.to_excel('Reporte Consultas', sheet_name='registro')
