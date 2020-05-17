from ..configuracion import *
from urllib.request import Request, urlopen
import json
from time import time
import pandas as pd
from datetime import datetime
import xlsxwriter

def create_report(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    # database.child('bases_Datos').child("d0oIsERZMEMziEvqotmB6bBFjsu2").remove() Para eliminar un registro

    basesDatos=database.child('bases_Datos').get()
    nombreBasesDatos=[]
    for i in basesDatos.each():
        informacionBaseDatos=i.val()
        nombre=informacionBaseDatos.get('nameDataBase')
        nombreBasesDatos.append(nombre)

    formatos=database.child('formatos').get()
    nombreFormatos=[]
    for i in formatos.each():
        informacionFormato=i.val()
        nombreFormato=informacionFormato.get('Report_Id')
        nombreFormatos.append(nombreFormato)

    name=database.child('users').child(a).child('details').get().val()['name']
    return render(request,"createReport.html",{"arregloBasesDatos":nombreBasesDatos,"e":name, "arregloFormatos":nombreFormatos})

def AntesCrearReporte(request):
    consultas = database.child('Consulta').get()
    try:
        for i in consultas.each():
            agregarConfiguracion(arregloFaltantes, diccionario, i.val()['Base de Datos'], i.val()['Fecha de Inicio'],
                                 i.val()['Fecha de Fin'], i.val()['Formato'])
        return CrearReporte(request)
    except:
        return CrearReporte(request)

def CrearReporte(requets):
    arregloConsultas = []
    formato = requets.POST.get('formato')
    idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    listaBD = database.child('bases_Datos').get()

    if requets.POST.get('seleccionarTodas') == "1":
        for BD in listaBD.each():
            arregloAux = []
            arregloFaltantes = []
            url = BD.val()['url']
            customer_id = BD.val()['customer_id']
            requestor_id = BD.val()['requestor_id']
            api_key = BD.val()['api_key']
            begin_date = requets.POST.get('fechaInicial')
            end_date = requets.POST.get('fechaFinal')
            platform = BD.val()['platform']
            nombreBaseDatos = BD.val()['nameDataBase']
            if (agregarConfiguracion(arregloFaltantes, diccionario, nombreBaseDatos, begin_date, end_date, formato)):
                for k in arregloFaltantes:
                    fecha1 = k[:-3]
                    fecha1 += str("-01")
                    separador = str(k).index('-') + 1
                    diaFinMes = FinDeMes[str(k[separador:-3])]
                    fecha2 = str(k[0:5]) + str(k[separador:-3]) + diaFinMes
                    informacionUso = pedirInformacion(url, customer_id, requestor_id, api_key, fecha1, fecha2, platform,
                                                      formato)
                    nombreBaseDatos = BD.val()['nameDataBase']
                    for informacion in informacionUso['Report_Items']:
                        performance = informacion['Performance']
                        for i in performance:
                            fechaInicio = i['Period']['Begin_Date']
                            fechaFinal = i['Period']['End_Date']
                            for j in i['Instance']:
                                if j['Metric_Type'] == "Total_Item_Requests":
                                    totalMes = j['Count']
                                    consultaRealizada = {
                                        "Base de Datos": nombreBaseDatos,
                                        "Formato": formato,
                                        "Fecha de Inicio": fechaInicio,
                                        "Fecha de Fin": fechaFinal,
                                        "Total": totalMes
                                    }
                                    print("")
                                    database.child('Consulta').push(consultaRealizada)
                                    # arregloTemp.append(consultaRealizada)
                                    # arregloAux.append(consultaRealizada)
            Consultas = database.child('Consulta').get()
            for consulta in Consultas.each():
                if consulta.val()['Base de Datos'] == nombreBaseDatos and consulta.val()['Formato'] == formato:
                    if consulta.val()['Fecha de Inicio'] >= requets.POST.get('fechaInicial') and consulta.val()['Fecha de Fin'] <= requets.POST.get('fechaFinal'):
                        consultaRealizada = {
                            "Base de Datos": consulta.val()['Base de Datos'],
                            "Formato": consulta.val()['Formato'],
                            "Fecha de Inicio": consulta.val()['Fecha de Inicio'],
                            "Fecha de Fin": consulta.val()['Fecha de Fin'],
                            "Total": consulta.val()['Total']
                        }
                        arregloAux.append(consultaRealizada)
                        anexarFechasNombre = {
                            "Ultima consulta": fechaDeConsulta()
                        }
                        try:
                            database.child('Fechas').child(consulta.val()['Base de Datos']).child(
                                consulta.val()['Formato']).child(consulta.val()['Fecha de Inicio']).update(
                                anexarFechasNombre)
                        except:
                            database.child('Fechas').child(consulta.val()['Base de Datos']).child(consulta.val()['Formato']).child(consulta.val()['Fecha de Inicio']).push(anexarFechasNombre)
            for i in range(0, len(arregloAux)):
                for j in range(i + 1, len(arregloAux) - 1):
                    if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                        arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]
            for i in arregloAux:
                arregloConsultas.append(i)
        return render(requets, 'verConsulta.html', context={"consultaRealizada": arregloConsultas})
    else:
        for BD in listaBD.each():
            arregloFaltantes=[]
            arregloAux = []
            nombreBaseDatos = BD.val()['nameDataBase']
            if requets.POST.get(nombreBaseDatos) == "1":
                url = BD.val()['url']
                customer_id = BD.val()['customer_id']
                requestor_id = BD.val()['requestor_id']
                api_key = BD.val()['api_key']
                begin_date = requets.POST.get('fechaInicial')
                end_date = requets.POST.get('fechaFinal')
                platform = BD.val()['platform']
                if (agregarConfiguracion(arregloFaltantes,diccionario,nombreBaseDatos, begin_date,end_date,formato)):
                    for k in arregloFaltantes:
                        fecha1 = k[:-3]
                        fecha1 += str("-01")
                        separador = str(k).index('-') +1
                        diaFinMes = FinDeMes[str(k[separador:-3])]
                        fecha2 = str(k[0:5])+str(k[separador:-3])+diaFinMes
                        informacionUso = pedirInformacion(url, customer_id, requestor_id, api_key, fecha1, fecha2, platform, formato)
                        nombreBaseDatos = BD.val()['nameDataBase']
                        for informacion in informacionUso['Report_Items']:
                            performance = informacion['Performance']
                            for i in performance:
                                fechaInicio = i['Period']['Begin_Date']
                                fechaFinal = i['Period']['End_Date']
                                for j in i['Instance']:
                                    if j['Metric_Type'] == "Total_Item_Requests":
                                        totalMes = j['Count']
                                        consultaRealizada = {
                                            "Base de Datos": nombreBaseDatos,
                                            "Formato": formato,
                                            "Fecha de Inicio": fechaInicio,
                                            "Fecha de Fin": fechaFinal,
                                            "Total": totalMes
                                        }
                                        print("")
                                        database.child('Consulta').push(consultaRealizada)
                                        #arregloTemp.append(consultaRealizada)
                                        #arregloAux.append(consultaRealizada)
                Consultas = database.child('Consulta').get()
                for consulta in Consultas.each():
                    if consulta.val()['Base de Datos'] == nombreBaseDatos and consulta.val()['Formato'] == formato:
                        if consulta.val()['Fecha de Inicio'] >= requets.POST.get('fechaInicial') and consulta.val()['Fecha de Fin'] <= requets.POST.get('fechaFinal'):
                            consultaRealizada = {
                                "Base de Datos": consulta.val()['Base de Datos'],
                                "Formato": consulta.val()['Formato'],
                                "Fecha de Inicio": consulta.val()['Fecha de Inicio'],
                                "Fecha de Fin": consulta.val()['Fecha de Fin'],
                                "Total": consulta.val()['Total']
                            }
                            arregloAux.append(consultaRealizada)
                for i in range(0, len(arregloAux)):
                    for j in range(i + 1, len(arregloAux)-1):
                        if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]
                for i in arregloAux:
                    arregloConsultas.append(i)
        return render(requets, 'verConsulta.html', context={"consultaRealizada": arregloConsultas})

def pedirInformacion(url,customer_id,requestor_id,api_key,begin_date,end_date,platform,formato):
    formato=str(url)+"/reports/"+str(formato)+"?"
    if(requestor_id!=''):
        formato+= "requestor_id="+str(requestor_id)+"&"
    if(customer_id!=''):
        formato+= "customer_id="+str(customer_id)+"&"
    if(api_key!=''):
        formato+= "api_key="+str(api_key)+"&"
    if(begin_date!=''):
        formato+= "begin_date="+str(begin_date)+"&"
    if (end_date!=''):
        formato+= "end_date="+str(end_date)+"&"
    if (platform!=''):
        formato+= "platform="+str(platform)
    if (formato[len(formato)-1]=='&'):
        formato=formato[0:len(formato)-1]
    peticion=Request(formato, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(peticion).read()
    decoded = json.loads(webpage)
    return decoded

def descargar(request):
    arregloAux=request.GET.get('informacion')

    aux = eval(arregloAux)

    nombre_BaseDatos = []
    fechaInicial = []
    fechaFinal = []
    formato = []
    Total = []

    for i in aux:
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

    outfile = r'C:\Users\CESAR GARCIA\Desktop\Resultado_1.xlsx'
    writer = pd.ExcelWriter(outfile, engine="xlsxwriter", )
    data.to_excel(writer, sheet_name="Hola", index=None)
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
    if request.POST.get('allDataBase') == "1":
        basesDatos = database.child('bases_Datos').get()
        for baseDatos in basesDatos.each():
            arregloAux = []
            nombreBaseDatos = baseDatos.val()['nameDataBase']
            consultas = database.child('Consulta').order_by_child("Base de Datos").equal_to(str(nombreBaseDatos)).get()
            for i in consultas.each():
                fechaInicioConsulta = datetime.strptime(i.val()['Fecha de Inicio'], '%Y-%m-%d').date()
                yearInicioConsulta = fechaInicioConsulta.year
                mesInicioConsulta = fechaInicioConsulta.month
                diaInicioConsulta = fechaInicioConsulta.day
                fechaFinalConsulta = datetime.strptime(i.val()['Fecha de Fin'], '%Y-%m-%d').date()
                yearFinalConsulta = fechaFinalConsulta.year
                mesFinalConsulta = fechaFinalConsulta.month
                diaFinalConsulta = fechaFinalConsulta.day
                if i.val()['Formato'] == formato:
                    if yearInicioConsulta >= yearInicial and yearFinalConsulta <= yearFinal:
                        if mesInicioConsulta >= mesInical and mesFinalConsulta <= mesFinal:
                            if diaInicioConsulta >= diaInicial and diaFinalConsulta <= diaFinal:
                                baseDatos = i.val()['Base de Datos']
                                total = i.val()['Total']
                                visualizacionConsulta = {
                                    "Base de Datos": baseDatos,
                                    "Formato": formato,
                                    "Fecha de Inicio": i.val()['Fecha de Inicio'],
                                    "Fecha de Fin": i.val()['Fecha de Fin'],
                                    "Total": total
                                }
                                arregloAux.append(visualizacionConsulta)
            for i in range(0, len(arregloAux) - 1):
                for j in range(i + 1, len(arregloAux)):
                    if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                        arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]
            for i in arregloAux:
                    arreglodeConsultas.append(i)
    else:
        nombreBasesDatos = database.child('bases_Datos').get()
        for baseDatos in nombreBasesDatos.each():
            arregloAux = []
            nameDataBase = baseDatos.val()['nameDataBase']
            if request.POST.get(nameDataBase) == "1":
                consultas = database.child('Consulta').order_by_child("Base de Datos").equal_to(
                    str(nameDataBase)).get()
                for i in consultas.each():
                    fechaInicioConsulta = datetime.strptime(i.val()['Fecha de Inicio'], '%Y-%m-%d').date()
                    yearInicioConsulta = fechaInicioConsulta.year
                    mesInicioConsulta = fechaInicioConsulta.month
                    diaInicioConsulta = fechaInicioConsulta.day
                    fechaFinalConsulta = datetime.strptime(i.val()['Fecha de Fin'], '%Y-%m-%d').date()
                    yearFinalConsulta = fechaFinalConsulta.year
                    mesFinalConsulta = fechaFinalConsulta.month
                    diaFinalConsulta = fechaFinalConsulta.day
                    print("Fecha Incial consulta: " + str(fechaInicioConsulta) + " dia: " + str(
                        diaInicioConsulta) + " mes: " + str(
                        mesInicioConsulta) + " año: " + str(yearInicioConsulta))
                    print("Fecha Final consulta: " + str(fechaFinalConsulta) + " dia: " + str(
                        diaFinalConsulta) + " mes: " + str(
                        mesFinalConsulta) + " año: " + str(yearFinalConsulta))
                    if i.val()['Formato'] == formato:
                        if i.val()['Base de Datos'] == str(nameDataBase):
                            if yearInicioConsulta >= yearInicial and yearFinalConsulta <= yearFinal:
                                if mesInicioConsulta >= mesInical and mesFinalConsulta <= mesFinal:
                                    if diaInicioConsulta >= diaInicial and diaFinalConsulta <= diaFinal:
                                        baseDatos = i.val()['Base de Datos']
                                        total = i.val()['Total']
                                        visualizacionConsulta = {
                                            "Base de Datos": baseDatos,
                                            "Formato": formato,
                                            "Fecha de Inicio": i.val()['Fecha de Inicio'],
                                            "Fecha de Fin": i.val()['Fecha de Fin'],
                                            "Total": total
                                        }
                                        arregloAux.append(visualizacionConsulta)
                for i in range(0, len(arregloAux) - 1):
                        for j in range(i + 1, len(arregloAux)):
                            if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                                arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]
                for i in arregloAux:
                    arreglodeConsultas.append(i)
    return render(request, 'visualizacion.html', {"registros": arreglodeConsultas})