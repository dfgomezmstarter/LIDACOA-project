from ..configuracion import *
import pandas as pd
from datetime import datetime

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
    outfile = r'C:\Users\CESAR GARCIA\Desktop\Resultado_1.xlsx'
    writer = pd.ExcelWriter(outfile, engine="xlsxwriter")
    df.to_excel(writer, sheet_name="Hola")
    #print("Exporta")
    writer.save()


def verReporte(request):
    arreglodeConsultas=[]
    if len(request.POST.get('nombreBaseDatos'))==0:
        fechaInicial = datetime.strptime(request.POST.get('fechaInicial'), '%Y-%m-%d').date()
        yearInicial=fechaInicial.year
        mesInical=fechaInicial.month
        diaInicial=fechaInicial.day
        fechaFinal=datetime.strptime(request.POST.get('fechaFinal'), '%Y-%m-%d').date()
        yearFinal=fechaFinal.year
        mesFinal=fechaFinal.month
        diaFinal=31
        #print("AÑO INICIO: " + str(yearInicial) + " MES INICIO: " + str(mesInical) + " DIA INICIAL: " + str(diaInicial))
        #print("AÑO FINAL: " + str(yearFinal) + " MES FINAL: " + str(mesFinal) + " DIA FINAL: " +str(diaFinal))
        #formato = request.POST.get('formato')
        formato="PR_P1"
        consultas = database.child('Consulta').get()
        for i in consultas.each():
            fechaInicioConsulta=datetime.strptime(i.val()['fechaInicio'], '%Y-%m-%d').date()
            yearInicioConsulta=fechaInicioConsulta.year
            mesInicioConsulta=fechaInicioConsulta.month
            diaInicioConsulta=fechaInicioConsulta.day
            #print("AÑO INICIO CONSULTA: " +str(yearInicioConsulta))
            #print("MES INICIO CONSULTA: " +str(mesInicioConsulta))
            #print("DIA INICIO CONSULTA: " +str(diaInicioConsulta))
            fechaFinalConsulta=datetime.strptime(i.val()['fechaFinal'], '%Y-%m-%d').date()
            yearFinalConsulta=fechaFinalConsulta.year
            mesFinalConsulta=fechaFinalConsulta.month
            diaFinalConsulta=fechaFinalConsulta.day
            #print("AÑO FINAL CONSULTA: " + str(yearFinalConsulta))
            #print("MES FINAL CONSULTA: " + str(mesFinalConsulta))
            #print("DIA FINAL CONSULTA: " + str(diaFinalConsulta))
            if i.val()['formatoConsulta'] == formato:
                if yearInicioConsulta>=yearInicial and yearFinalConsulta<=yearFinal:
                    #print("AÑO INICIO BD: " + str(yearInicioConsulta) + " AÑO FINAL BD: " + str(yearFinalConsulta))
                    if mesInicioConsulta>=mesInical and mesFinalConsulta<=mesFinal:
                        #print("MES INICIO BD: " +str(mesInicioConsulta) + " MES FINAL BD: " +str(mesFinalConsulta))
                        #print("DIA INICIO BD: " + str(diaInicioConsulta) + " dia Inicial: " + str(diaInicial) + " DIA FINAL BD: " + str(diaFinalConsulta) + " dia Final: " + str(diaFinal))
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
                            #arregloValores=[baseDatos,formato,i.val()['fechaInicio'],i.val()['fechaFinal'],total]
                            #print("consulta: " +str(arregloValores))
        #print("año I: " + str(yearInicial) + " mes I: " + str(mesInical) + " dia I: " + str(diaInicial))
        #print("año F: " + str(yearFinal) + " mes F: " + str(mesFinal) + " dia F: " + str(diaFinal))
        #print("Formato: " + str(formato))
        return render(request,'visualizacion.html',{"registros":arreglodeConsultas})
    else:
        print("Algo")
        print(request.POST.get('nombreBaseDatos'))


