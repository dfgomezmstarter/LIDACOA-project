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


def CrearReporte(requets):
    tiempoInicial = time()
    arregloConsultas = []
    #formato = "PR_P1"
    formato = requets.POST.get('formato')
    # bd = requets.POST.get('basesDeDatos')
    # print("formato: " + str(formato))
    idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("Formato: " + str(formato))
    listaBD = database.child('bases_Datos').get()

    if requets.POST.get('seleccionarTodas') == "1":
        for BD in listaBD.each():
            nombreBaseDatos = BD.val()['nameDataBase']
            url = BD.val()['url']
            customer_id = BD.val()['customer_id']
            requestor_id = BD.val()['requestor_id']
            api_key = BD.val()['api_key']
            begin_date = requets.POST.get('fechaInicial')
            end_date = requets.POST.get('fechaFinal')
            platform = BD.val()['platform']
            informacionUso = pedirInformacion(url, customer_id, requestor_id, api_key, begin_date, end_date, platform,
                                              formato)
            # print("Informacion: " + str(informacionUso))
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
                            database.child('Consulta').push(consultaRealizada)
                            arregloConsultas.append(consultaRealizada)
            # consultaRealizada=organizarReporte(informacionUso, begin_date, end_date, formato,nombreBaseDatos)
            # database.child('Consulta').push(consultaRealizada)
        tiempoFinal = time()
        print("Tiempo: " + str(tiempoFinal - tiempoInicial))
        return render(requets, 'verConsulta.html', context={"consultaRealizada": arregloConsultas})
    else:
        for BD in listaBD.each():
            nombreBaseDatos = BD.val()['nameDataBase']
            if requets.POST.get(nombreBaseDatos) == "1":
                url = BD.val()['url']
                customer_id = BD.val()['customer_id']
                requestor_id = BD.val()['requestor_id']
                api_key = BD.val()['api_key']
                begin_date = requets.POST.get('fechaInicial')
                end_date = requets.POST.get('fechaFinal')
                platform = BD.val()['platform']
                if (agregar(diccionario,url, begin_date,end_date)):
                    informacionUso = pedirInformacion(url, customer_id, requestor_id, api_key, begin_date, end_date,
                                                      platform,
                                                      formato)
                    # print("Informacion: " + str(informacionUso))
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
                                    database.child('Consulta').push(consultaRealizada)
                                    arregloConsultas.append(consultaRealizada)
                    # consultaRealizada=organizarReporte(informacionUso, begin_date, end_date, formato,nombreBaseDatos)
                    # database.child('Consulta').push(consultaRealizada)
                    print(diccionario)
        tiempoFinal = time()
        print("Tiempo: " + str(tiempoFinal - tiempoInicial))
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

def agregar(diccionario,baseDeDatos,fechaInicial,fechaFinal):
    arregloTemp =[]
    arregloLlaves = diccionario.keys()
    if (not(baseDeDatos in arregloLlaves)):
        for i in range(int(fechaInicial[-5:-3]),int(fechaFinal[-5:-3])+1):
            arregloTemp.append(str("2019-"+str(i)+"-30"))
        diccionario[baseDeDatos] = arregloTemp
    else:
        return False
    return True


def descargar(request):
    arregloAux=request.GET.get('informacion')

    aux = eval(arregloAux)

    nombre_BaseDatos = []
    fechaInicial = []
    fechaFinal = []
    formato = []
    Total = []
    print("----------------------------------------------------------------------------------------------------------------")

    for i in aux:
        print(i['Base de Datos'])
        nombre_BaseDatos.append(i['Base de Datos'])
        fechaInicial.append(i['Fecha de Inicio'])
        fechaFinal.append(i['Fecha de Fin'])
        formato.append(i['Formato'])
        Total.append(i['Total'])


    print("Arreglo: " + str(nombre_BaseDatos))
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

    """for i in range(0, len(arreglodeConsultas)-2):
        for j in range(i+1, len(arreglodeConsultas)-1):
            if (arreglodeConsultas[j]['Fecha de Inicio'] < arreglodeConsultas[i]['Fecha de Inicio']) and (arreglodeConsultas[j]['Base de Datos'] == arreglodeConsultas[i]['Base de Datos']):
                arreglodeConsultas[i], arreglodeConsultas[j] = arreglodeConsultas[j], arreglodeConsultas[i]"""
    return render(request, 'visualizacion.html', {"registros": arreglodeConsultas})