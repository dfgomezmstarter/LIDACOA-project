from ..configuracion import *
import pandas as pd
from datetime import datetime

import xlsxwriter


def descargar(request):
    print("entra Prueba")
    arregloAux=request.GET.get('informacion')
    print(str(arregloAux))




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
    outfile = r'C:\Users\CESAR GARCIA\Desktop\Resultado_1.xlsx'
    writer = pd.ExcelWriter(outfile, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Hola")
    #print("Exporta")
    writer.save()


def verReporte(request):
    validar=False
    arreglodeConsultas = []
    nombreBasesDatos=database.child('bases_Datos').get()
    for baseDatos in nombreBasesDatos.each():
        nameDataBase=baseDatos.val()['nameDataBase']
        if request.POST.get(nameDataBase) == "1":
            validar=True
            fechaInicial = datetime.strptime(request.POST.get('fechaInicial'), '%Y-%m-%d').date()
            yearInicial = fechaInicial.year
            mesInical = fechaInicial.month
            diaInicial = fechaInicial.day
            fechaFinal = datetime.strptime(request.POST.get('fechaFinal'), '%Y-%m-%d').date()
            yearFinal = fechaFinal.year
            mesFinal = fechaFinal.month
            diaFinal = 31
            formato = "PR_P1"
            # formato=request.POST.get('formato')
            consultas = database.child('Consulta').get()
            for i in consultas.each():
                fechaInicioConsulta = datetime.strptime(i.val()['fechaInicio'], '%Y-%m-%d').date()
                yearInicioConsulta = fechaInicioConsulta.year
                mesInicioConsulta = fechaInicioConsulta.month
                diaInicioConsulta = fechaInicioConsulta.day
                fechaFinalConsulta = datetime.strptime(i.val()['fechaFinal'], '%Y-%m-%d').date()
                yearFinalConsulta = fechaFinalConsulta.year
                mesFinalConsulta = fechaFinalConsulta.month
                diaFinalConsulta = fechaFinalConsulta.day
                if i.val()['formatoConsulta'] == formato:
                    if i.val()['nombreBaseDatos'] == str(nameDataBase):
                        if yearInicioConsulta >= yearInicial and yearFinalConsulta <= yearFinal:
                            if mesInicioConsulta >= mesInical and mesFinalConsulta <= mesFinal:
                                if diaInicioConsulta >= diaInicial and diaFinalConsulta <= diaFinal:
                                    baseDatos = i.val()['nombreBaseDatos']
                                    total = i.val()['totalMes']
                                    visualizacionConsulta = {
                                        "Base de Datos": baseDatos,
                                        "Formato": formato,
                                        "Fecha de Inicio": i.val()['fechaInicio'],
                                        "Fecha de Fin": i.val()['fechaFinal'],
                                        "Total": total
                                    }
                                    arreglodeConsultas.append(visualizacionConsulta)

    if validar==False or request.POST.get('allDataBase')=="1":
        fechaInicial = datetime.strptime(request.POST.get('fechaInicial'), '%Y-%m-%d').date()
        yearInicial=fechaInicial.year
        mesInical=fechaInicial.month
        diaInicial=fechaInicial.day
        fechaFinal=datetime.strptime(request.POST.get('fechaFinal'), '%Y-%m-%d').date()
        yearFinal=fechaFinal.year
        mesFinal=fechaFinal.month
        diaFinal=31
        formato="PR_P1"
        #formato=request.POST.get('formato')
        consultas = database.child('Consulta').get()
        for i in consultas.each():
            fechaInicioConsulta=datetime.strptime(i.val()['fechaInicio'], '%Y-%m-%d').date()
            yearInicioConsulta=fechaInicioConsulta.year
            mesInicioConsulta=fechaInicioConsulta.month
            diaInicioConsulta=fechaInicioConsulta.day
            fechaFinalConsulta=datetime.strptime(i.val()['fechaFinal'], '%Y-%m-%d').date()
            yearFinalConsulta=fechaFinalConsulta.year
            mesFinalConsulta=fechaFinalConsulta.month
            diaFinalConsulta=fechaFinalConsulta.day
            if i.val()['formatoConsulta'] == formato:
                if yearInicioConsulta>=yearInicial and yearFinalConsulta<=yearFinal:
                    if mesInicioConsulta>=mesInical and mesFinalConsulta<=mesFinal:
                        if diaInicioConsulta>=diaInicial and diaFinalConsulta<=diaFinal:
                            baseDatos=i.val()['nombreBaseDatos']
                            total=i.val()['totalMes']
                            visualizacionConsulta={
                                "Base de Datos" : baseDatos,
                                "Formato" : formato,
                                "Fecha de Inicio" : i.val()['fechaInicio'],
                                "Fecha de Fin" : i.val()['fechaFinal'],
                                "Total" : total
                            }
                            arreglodeConsultas.append(visualizacionConsulta)

        return render(request,'visualizacion.html',{"registros":arreglodeConsultas})
    else:
        return render(request, 'visualizacion.html', {"registros": arreglodeConsultas})



