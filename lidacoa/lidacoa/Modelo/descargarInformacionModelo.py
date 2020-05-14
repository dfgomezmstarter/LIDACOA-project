"""from ..configuracion import *
import pandas as pd
from datetime import datetime
import xlsxwriter


def descargar(request):
    print("entra Prueba")
    arregloAux=request.GET.get('informacion')

    aux = eval(arregloAux)

    nombre_BaseDatos = []
    fechaInicial = []
    fechaFinal = []
    formato = []
    Total = []

    for i in aux:
        print("Prueba Arreglo")
        nombre_BaseDatos.append(i['Base de Datos'])
        fechaInicial.append(i['Fecha de Inicio'])
        fechaFinal.append(i['Fecha de Fin'])
        formato.append(i['Formato'])
        Total.append(i['Total'])


    data = pd.DataFrame({
        'Base de Datos' : nombre_BaseDatos,
        'Formato' : formato,
        'Fecha de Inicio' : fechaInicial,
        'Fecha de Fin' : fechaFinal,
        'Total' : Total
    })

    print(data)
    outfile = r'C:\Users\CESAR GARCIA\Desktop\Resultado_1.xlsx'
    writer = pd.ExcelWriter(outfile, engine="xlsxwriter", )
    data.to_excel(writer, sheet_name="Hola", index=None)
    # print("Exporta")
    writer.save()
    return render(request, 'welcome.html')


def verReporte(request):
    arreglodeConsultas = []
    fechaInicial = datetime.strptime(str(request.POST.get('fechaInicial')), '%Y-%m-%d')
    yearInicial = fechaInicial.year
    mesInical = fechaInicial.month
    diaInicial = fechaInicial.day
    fechaFinal = datetime.strptime(str(request.POST.get('fechaFinal')), '%Y-%m-%d')
    yearFinal = fechaFinal.year
    mesFinal = fechaFinal.month
    diaFinal = 31
    formato = request.POST.get('formato')
    print("Fecha Incial: " + str(fechaInicial) + " dia: " + str(diaInicial) + " mes: " + str(mesInical) + " año: " + str(yearInicial))
    print("Fecha Final: " + str(fechaFinal) + " dia: " + str(diaFinal) + " mes: " + str(mesFinal) + " año: " + str(yearFinal))
    print("FORMATO: " + str(formato))
    consultas = database.child('Consulta').order_by_child('nombreBaseDatos').get()
    if request.POST.get('allDataBase') == "1":
        for i in consultas.each():
            fechaInicioConsulta = datetime.strptime(i.val()['fechaInicio'], '%Y-%m-%d').date()
            yearInicioConsulta = fechaInicioConsulta.year
            mesInicioConsulta = fechaInicioConsulta.month
            diaInicioConsulta = fechaInicioConsulta.day
            fechaFinalConsulta = datetime.strptime(i.val()['fechaFinal'], '%Y-%m-%d').date()
            yearFinalConsulta = fechaFinalConsulta.year
            mesFinalConsulta = fechaFinalConsulta.month
            diaFinalConsulta = fechaFinalConsulta.day
            print("Fecha Incial consulta: " + str(fechaInicioConsulta) + " dia: " + str(diaInicioConsulta) + " mes: " + str(
                mesInicioConsulta) + " año: " + str(yearInicioConsulta))
            print("Fecha Final consulta: " + str(fechaFinalConsulta) + " dia: " + str(diaFinalConsulta) + " mes: " + str(
                mesFinalConsulta) + " año: " + str(yearFinalConsulta))
            if i.val()['formatoConsulta'] == formato:
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
    else:
        nombreBasesDatos = database.child('bases_Datos').get()
        for baseDatos in nombreBasesDatos.each():
            nameDataBase = baseDatos.val()['nameDataBase']
            if request.POST.get(nameDataBase) == "1":
                for i in consultas.each():
                    fechaInicioConsulta = datetime.strptime(i.val()['fechaInicio'], '%Y-%m-%d').date()
                    yearInicioConsulta = fechaInicioConsulta.year
                    mesInicioConsulta = fechaInicioConsulta.month
                    diaInicioConsulta = fechaInicioConsulta.day
                    fechaFinalConsulta = datetime.strptime(i.val()['fechaFinal'], '%Y-%m-%d').date()
                    yearFinalConsulta = fechaFinalConsulta.year
                    mesFinalConsulta = fechaFinalConsulta.month
                    diaFinalConsulta = fechaFinalConsulta.day
                    print("Fecha Incial consulta: " + str(fechaInicioConsulta) + " dia: " + str(
                        diaInicioConsulta) + " mes: " + str(
                        mesInicioConsulta) + " año: " + str(yearInicioConsulta))
                    print("Fecha Final consulta: " + str(fechaFinalConsulta) + " dia: " + str(
                        diaFinalConsulta) + " mes: " + str(
                        mesFinalConsulta) + " año: " + str(yearFinalConsulta))
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

    for i in range(0, len(arreglodeConsultas)-2):
        for j in range(i+1, len(arreglodeConsultas)-1):
            if (arreglodeConsultas[j]['Fecha de Inicio'] < arreglodeConsultas[i]['Fecha de Inicio']) and (arreglodeConsultas[j]['Base de Datos'] == arreglodeConsultas[i]['Base de Datos']):
                arreglodeConsultas[i], arreglodeConsultas[j] = arreglodeConsultas[j], arreglodeConsultas[i]
    return render(request, 'visualizacion.html', {"registros": arreglodeConsultas})"""



