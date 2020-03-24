from ..configuracion import *
import pandas as pd
import xlsxwriter


def descargar(request):
    print("entro")
    data = {}
    nombre_BaseDatos = request.POST.get('nombreBaseDatos')
    fechaInicial = request.POST.get('fechaInicial')
    fechaFinal = request.POST.get('fechaFinal')
    formato = request.POST.get('formato')

    print(str(nombre_BaseDatos) + str(fechaInicial) + str(fechaFinal) + str(formato))

    consultas = database.child('Consulta').get()
    for i in consultas.each():
        if i.val()['fechaInicio'] == fechaInicial and i.val()['fechaFinal'] == fechaFinal and i.val()['nombreBaseDatos'] == nombre_BaseDatos and i.val()['formatoConsulta'] == formato:
            data = {
                'Base_Datos': i.val()['nombreBaseDatos'],
                'Fecha Inicial': i.val()['fechaInicio'],
                'Fecha Final': i.val()['fechaFinal'],
                'Formato': i.val()['formatoConsulta'],
                'Total': i.val()['totalReporte']
            }
    print(data)
    file_to_Excel(data)
    return render(request, 'welcome.html')


def file_to_Excel(file):
    df = pd.DataFrame.from_dict(file, orient="index")
    print(df)
    outfile = r'C:\Users\MSI\Desktop\Resultado_1.xlsx'
    writer = pd.ExcelWriter(outfile, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Hola")
    #print("Exporta")
    writer.save()

