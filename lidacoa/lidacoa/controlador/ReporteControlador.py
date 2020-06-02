from ..configuracion import *
from urllib.request import Request, urlopen
import json
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from django.shortcuts import render
from matplotlib.backends.backend_agg import FigureCanvasAgg
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def create_report(request):
    for i in range(0,len(arregloDescarga)):
        arregloDescarga.pop()
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']

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
    arregloFechas=[]
    arregloConsultas = []
    formato = requets.POST.get('formato')
    #direccion = requets.POST.get('direccion')
    idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').get().val()['name']
    listaBD = database.child('bases_Datos').get()
    totalItemRequest = 0
    uniqueTitleInvestigation = 0
    uniqueItemInvestigation = 0
    totalItemInvestigation = 0
    searchesPlatform = 0
    consultaRealizada = {}

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
                    if "PR" in formato:
                        for informacion in informacionUso['Report_Items']:
                            performance = informacion['Performance']
                            for i in performance:
                                fechaInicio = i['Period']['Begin_Date']
                                fechaFinal = i['Period']['End_Date']
                                for j in i['Instance']:
                                    if j['Metric_Type'] == "Total_Item_Requests":
                                        totalItemRequest = j['Count']
                                    if j['Metric_Type'] and j['Metric_Type'] == "Unique_Title_Investigations":
                                        uniqueTitleInvestigation = j['Count']
                                    if j['Metric_Type'] and j['Metric_Type'] == "Unique_Item_Investigations":
                                        uniqueItemInvestigation = j['Count']
                                    if j['Metric_Type'] and j['Metric_Type'] == "Total_Item_Investigations":
                                        totalItemInvestigation = j['Count']
                                    if j['Metric_Type'] and j['Metric_Type'] == "Searches_Platform":
                                        searchesPlatform = j['Count']

                                consultaRealizada['Base de Datos'] = str(nombreBaseDatos)
                                consultaRealizada['Formato'] = str(formato)
                                consultaRealizada['Fecha de Inicio'] = str(fechaInicio)
                                consultaRealizada['Fecha de Fin'] = str(fechaFinal)

                                consultaRealizada['Total Item Requests'] = totalItemRequest
                                consultaRealizada['Unique Titile Investigations'] = uniqueTitleInvestigation
                                consultaRealizada['Unique Item Investigation'] = uniqueItemInvestigation
                                consultaRealizada['Total Item Investigation'] = totalItemInvestigation
                                consultaRealizada['Searches Platform'] = searchesPlatform

                                database.child('Consulta').push(consultaRealizada)
                    elif "TR_J" in formato:
                        for informacion in informacionUso['Report_Items']:
                            performance = informacion['Performance']
                            titulo = informacion['Title']
                            for i in performance:
                                fechaInicio = i['Period']['Begin_Date']
                                fechaFinal = i['Period']['End_Date']
                                for j in i['Instance']:
                                    if j['Metric_Type'] == "Total_Item_Requests":
                                        totalMes = j['Count']
                                        consultaRealizada = {
                                            "Base de Datos": nombreBaseDatos,
                                            "Titulo": titulo,
                                            "Formato": formato,
                                            "Fecha de Inicio": fechaInicio,
                                            "Fecha de Fin": fechaFinal,
                                            "Total": totalMes
                                        }
                                        database.child('Consulta').push(consultaRealizada)
            Consultas = database.child('Consulta').get()
            for consulta in Consultas.each():
                if consulta.val()['Base de Datos'] == nombreBaseDatos and consulta.val()['Formato'] == formato:
                    if consulta.val()['Fecha de Inicio'] >= requets.POST.get('fechaInicial') and consulta.val()['Fecha de Fin'] <= requets.POST.get('fechaFinal'):


                        if "PR" in formato:
                            consultaTotalItemRequest = 0
                            cunsoltaUniqueTitleInvestigation = 0
                            consultaUniqueItemInvestigation = 0
                            consultaTotalItemInvestigation = 0
                            consultaSearchesPlatform = 0

                            if consulta.val()['Total Item Requests']:
                                consultaTotalItemRequest = consulta.val()['Total Item Requests']
                            if consulta.val()['Unique Titile Investigations']:
                                cunsoltaUniqueTitleInvestigation = consulta.val()['Unique Titile Investigations']
                            if consulta.val()['Unique Item Investigation']:
                                consultaUniqueItemInvestigation = consulta.val()['Unique Item Investigation']
                            if consulta.val()['Total Item Investigation']:
                                consultaTotalItemInvestigation = consulta.val()['Total Item Investigation']
                            if consulta.val()['Searches Platform']:
                                consultaSearchesPlatform = consulta.val()['Searches Platform']

                            consultaRealizada = {
                                "Base de Datos": consulta.val()['Base de Datos'],
                                "Formato": consulta.val()['Formato'],
                                "Fecha de Inicio": consulta.val()['Fecha de Inicio'],
                                "Fecha de Fin": consulta.val()['Fecha de Fin'],
                                "Total Item Requests": consultaTotalItemRequest,
                                "Unique Titile Investigations": cunsoltaUniqueTitleInvestigation,
                                "Unique Item Investigation": consultaUniqueItemInvestigation,
                                "Total Item Investigation": consultaTotalItemInvestigation,
                                "Searches Platform": consultaSearchesPlatform,
                            }
                        elif "TR_J" in formato:
                            consultaRealizada = {
                                "Base de Datos": consulta.val()['Base de Datos'],
                                "Titulo": consulta.val()['Titulo'],
                                "Formato": consulta.val()['Formato'],
                                "Fecha de Inicio": consulta.val()['Fecha de Inicio'],
                                "Fecha de Fin": consulta.val()['Fecha de Fin'],
                                "Total": consulta.val()['Total']
                            }
                        arregloAux.append(consultaRealizada)
                        fechaAux = str(consulta.val()['Base de Datos'])+"/"+str(consulta.val()['Formato'])+"/"+str(consulta.val()['Fecha de Inicio'])
                        if(not(fechaAux in arregloFechas)):
                            arregloFechas.append(fechaAux)
            for fecha3 in arregloFechas:
                aux = str(fecha3)
                separador = aux.index("/")
                nombreBD = aux[0:separador]
                aux = aux[separador + 1:]
                separador = aux.index("/")
                formato2 = aux[0:separador]
                fecha4 = aux[separador + 1:]
                anexarFechasNombre = {
                    "Ultima consulta": fechaDeConsulta()
                }
                try:
                    database.child('Fechas').child(nombreBD).child(formato2).child(fecha4).update(anexarFechasNombre)
                except:
                    database.child('Fechas').child(nombreBD).child(formato2).child(fecha4).push(anexarFechasNombre)

            if "PR" in formato:
                for i in range(0, len(arregloAux)):
                    for j in range(i + 1, len(arregloAux) - 1):
                        if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]
            elif "TR_J" in formato:
                for i in range(0, len(arregloAux)):
                    for j in range(i + 1, len(arregloAux) - 1):
                        if (arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']) and (arregloAux[j]['Titulo'] < arregloAux[i]['Titulo']):
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]
            for i in arregloAux:
                arregloConsultas.append(i)
                arregloDescarga.append(i)
        if "PR" in formato:
            return render(requets, 'verConsultaTipoFormatoI.html', context={"consultaRealizada": arregloConsultas, "formato":formato, "e":name,"fechaInicio":begin_date,"fechaFin":end_date})
        elif "TR_J" in formato:
            return render(requets, 'verConsultaTipoFormatoII.html', context={"consultaRealizada": arregloConsultas, "formato":formato, "e":name})
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



                        if "PR" in formato:
                            for informacion in informacionUso['Report_Items']:
                                performance = informacion['Performance']
                                for i in performance:
                                    fechaInicio = i['Period']['Begin_Date']
                                    fechaFinal = i['Period']['End_Date']
                                    for j in i['Instance']:
                                        if j['Metric_Type'] == "Total_Item_Requests":
                                            totalItemRequest = j['Count']
                                        if j['Metric_Type'] and j['Metric_Type'] == "Unique_Title_Investigations":
                                            uniqueTitleInvestigation = j['Count']
                                        if j['Metric_Type'] and j['Metric_Type'] == "Unique_Item_Investigations":
                                            uniqueItemInvestigation = j['Count']
                                        if j['Metric_Type'] and j['Metric_Type'] == "Total_Item_Investigations":
                                            totalItemInvestigation = j['Count']
                                        if j['Metric_Type'] and j['Metric_Type'] == "Searches_Platform":
                                            searchesPlatform = j['Count']

                                    consultaRealizada['Base de Datos'] = str(nombreBaseDatos)
                                    consultaRealizada['Formato'] = str(formato)
                                    consultaRealizada['Fecha de Inicio'] = str(fechaInicio)
                                    consultaRealizada['Fecha de Fin'] = str(fechaFinal)

                                    consultaRealizada['Total Item Requests'] = totalItemRequest
                                    consultaRealizada['Unique Titile Investigations'] = uniqueTitleInvestigation
                                    consultaRealizada['Unique Item Investigation'] = uniqueItemInvestigation
                                    consultaRealizada['Total Item Investigation'] = totalItemInvestigation
                                    consultaRealizada['Searches Platform'] = searchesPlatform

                                    database.child('Consulta').push(consultaRealizada)
                        elif "TR_J" in formato:
                            for informacion in informacionUso['Report_Items']:
                                performance = informacion['Performance']
                                titulo = informacion['Title']
                                for i in performance:
                                    fechaInicio = i['Period']['Begin_Date']
                                    fechaFinal = i['Period']['End_Date']
                                    for j in i['Instance']:
                                        if j['Metric_Type'] == "Total_Item_Requests":
                                            totalMes = j['Count']
                                            consultaRealizada = {
                                                "Base de Datos": nombreBaseDatos,
                                                "Titulo": titulo,
                                                "Formato": formato,
                                                "Fecha de Inicio": fechaInicio,
                                                "Fecha de Fin": fechaFinal,
                                                "Total": totalMes
                                            }
                                            database.child('Consulta').push(consultaRealizada)
                Consultas = database.child('Consulta').get()
                for consulta in Consultas.each():
                    if consulta.val()['Base de Datos'] == nombreBaseDatos and consulta.val()['Formato'] == formato:
                        if consulta.val()['Fecha de Inicio'] >= requets.POST.get('fechaInicial') and consulta.val()['Fecha de Fin'] <= requets.POST.get('fechaFinal'):
                            if "PR" in formato:
                                consultaTotalItemRequest = 0
                                cunsoltaUniqueTitleInvestigation = 0
                                consultaUniqueItemInvestigation = 0
                                consultaTotalItemInvestigation = 0
                                consultaSearchesPlatform = 0

                                if consulta.val()['Total Item Requests']:
                                    consultaTotalItemRequest = consulta.val()['Total Item Requests']
                                if consulta.val()['Unique Titile Investigations']:
                                    cunsoltaUniqueTitleInvestigation = consulta.val()['Unique Titile Investigations']
                                if consulta.val()['Unique Item Investigation']:
                                    consultaUniqueItemInvestigation = consulta.val()['Unique Item Investigation']
                                if consulta.val()['Total Item Investigation']:
                                    consultaTotalItemInvestigation = consulta.val()['Total Item Investigation']
                                if consulta.val()['Searches Platform']:
                                    consultaSearchesPlatform = consulta.val()['Searches Platform']
                                consultaRealizada = {
                                    "Base de Datos": consulta.val()['Base de Datos'],
                                    "Formato": consulta.val()['Formato'],
                                    "Fecha de Inicio": consulta.val()['Fecha de Inicio'],
                                    "Fecha de Fin": consulta.val()['Fecha de Fin'],
                                    "Total Item Requests": consultaTotalItemRequest,
                                    "Unique Titile Investigations": cunsoltaUniqueTitleInvestigation,
                                    "Unique Item Investigation": consultaUniqueItemInvestigation,
                                    "Total Item Investigation": consultaTotalItemInvestigation,
                                    "Searches Platform": consultaSearchesPlatform,
                                }
                            elif "TR_J" in formato:
                                consultaRealizada = {
                                    "Base de Datos": consulta.val()['Base de Datos'],
                                    "Titulo": consulta.val()['Titulo'],
                                    "Formato": consulta.val()['Formato'],
                                    "Fecha de Inicio": consulta.val()['Fecha de Inicio'],
                                    "Fecha de Fin": consulta.val()['Fecha de Fin'],
                                    "Total": consulta.val()['Total']
                                }
                            arregloAux.append(consultaRealizada)
                            fechaAux = str(consulta.val()['Base de Datos']) + "/" + str(consulta.val()['Formato']) + "/" + str(consulta.val()['Fecha de Inicio'])
                            if (not (fechaAux in arregloFechas)):
                                arregloFechas.append(fechaAux)
                for fecha3 in arregloFechas:
                    aux = str(fecha3)
                    separador = aux.index("/")
                    nombreBD = aux[0:separador]
                    aux = aux[separador + 1:]
                    separador = aux.index("/")
                    formato2 = aux[0:separador]
                    fecha4 = aux[separador + 1:]
                    anexarFechasNombre = {
                        "Ultima consulta": fechaDeConsulta()
                    }
                    try:
                        database.child('Fechas').child(nombreBD).child(formato2).child(fecha4).update(
                            anexarFechasNombre)
                    except:
                        database.child('Fechas').child(nombreBD).child(formato2).child(fecha4).push(anexarFechasNombre)

                if "PR" in formato:
                    for i in range(0, len(arregloAux) - 1):
                        for j in range(i + 1, len(arregloAux)):
                            if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                                arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]

                elif "TR_J" in formato:
                    for i in range(0, len(arregloAux) - 1):
                        for j in range(i + 1, len(arregloAux)):
                            if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                                arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]

                    for i in range(0, len(arregloAux) - 1):
                        for j in range(i + 1, len(arregloAux)):
                            if arregloAux[j]['Titulo'] < arregloAux[i]['Titulo']:
                                arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]
                for i in arregloAux:
                    arregloConsultas.append(i)
                    arregloDescarga.append(i)

        if "PR" in formato:
            return render(requets, 'verConsultaTipoFormatoI.html',context={"consultaRealizada": arregloConsultas, "formato":formato, "e":name,"fechaInicio":begin_date,"fechaFin":end_date})
        elif "TR_J" in formato:
            return render(requets, 'verConsultaTipoFormatoII.html', context={"consultaRealizada": arregloConsultas, "formato":formato, "e":name})

def pedirInformacion(url,customer_id,requestor_id,api_key,begin_date,end_date,platform,formato):
    formato = str(formato.lower())
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
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').get().val()['name']
    correo = database.child('users').child(a).child('details').get().val()['Correo']
    correo = str(correo)
    formatoConsulta = request.GET.get('formato')
    #direccion = request.GET.get('direccion') para futuro trabajo
    #direccion = str(direccion)
    nombre_BaseDatos = []
    titulo = []
    fechaInicial = []
    fechaFinal = []
    formato = []
    Total = []
    TotalItemRequest = []
    UniqueTitleInvestigation = []
    UniqueItemInvestigation = []
    TotalItemInvestigation = []
    SearchesPlatform = []

    if "PR" in formatoConsulta:
        for i in arregloDescarga:
            nombre_BaseDatos.append(i['Base de Datos'])
            fechaInicial.append(i['Fecha de Inicio'])
            fechaFinal.append(i['Fecha de Fin'])
            formato.append(i['Formato'])
            TotalItemRequest.append(i['Total Item Requests'])
            UniqueTitleInvestigation.append(i['Unique Titile Investigations'])
            UniqueItemInvestigation.append(i['Unique Item Investigation'])
            TotalItemInvestigation.append(i['Total Item Investigation'])
            SearchesPlatform.append(i['Searches Platform'])
        data = pd.DataFrame({
            'Base de Datos': nombre_BaseDatos,
            'Formato': formato,
            'Fecha de Inicio': fechaInicial,
            'Fecha de Fin': fechaFinal,
            "Total Item Requests": TotalItemRequest,
            "Unique Titile Investigations": UniqueTitleInvestigation,
            "Unique Item Investigation": UniqueItemInvestigation,
            "Total Item Investigation": TotalItemInvestigation,
            "Searches Platform": SearchesPlatform,
        })
        outfile = r'templates/Resultado_Consulta.xlsx'
        writer = pd.ExcelWriter(outfile, engine="xlsxwriter", )
        data.to_excel(writer, sheet_name="Consulta", index=None)
        writer.save()
    elif "TR_J" in formatoConsulta:
        for i in arregloDescarga:
            nombre_BaseDatos.append(i['Base de Datos'])
            fechaInicial.append(i['Fecha de Inicio'])
            fechaFinal.append(i['Fecha de Fin'])
            formato.append(i['Formato'])
            Total.append(i['Total'])
            titulo.append(i['Titulo'])
        data = pd.DataFrame({
            'Base de Datos': nombre_BaseDatos,
            'Titulo': titulo,
            'Formato': formato,
            'Fecha de Inicio': fechaInicial,
            'Fecha de Fin': fechaFinal,
            'Total': Total
        })
        outfile = r'templates/Resultado_Consulta.xlsx'
        writer = pd.ExcelWriter(outfile, engine="xlsxwriter", )
        data.to_excel(writer, sheet_name="Consulta", index=None)
        writer.save()

    if(correo!=''):
        # Iniciamos los parámetros del script
        remitente = 'lidacoacompany@gmail.com'
        destinatarios = [correo]
        asunto = 'Consulta de la base de datos'
        cuerpo = 'El archivo excel contine la informacion solicitada proveniente de la pagina web de LIDACOA'
        ruta_adjunto = 'templates/Resultado_Consulta.xlsx'
        nombre_adjunto = 'Resultado_Consulta.xlsx'

        # Creamos el objeto mensaje
        mensaje = MIMEMultipart()

        # Establecemos los atributos del mensaje
        mensaje['From'] = remitente
        mensaje['To'] = ", ".join(destinatarios)
        mensaje['Subject'] = asunto

        # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        # Abrimos el archivo que vamos a adjuntar
        archivo_adjunto = open(ruta_adjunto, 'rb')

        # Creamos un objeto MIME base
        adjunto_MIME = MIMEBase('application', 'octet-stream')
        # Y le cargamos el archivo adjunto
        adjunto_MIME.set_payload((archivo_adjunto).read())
        # Codificamos el objeto en BASE64
        encoders.encode_base64(adjunto_MIME)
        # Agregamos una cabecera al objeto
        adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
        # Y finalmente lo agregamos al mensaje
        mensaje.attach(adjunto_MIME)

        # Creamos la conexión con el servidor
        sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)

        # Ciframos la conexión
        sesion_smtp.starttls()

        # Iniciamos sesión en el servidor
        sesion_smtp.login('lidacoacompany@gmail.com', 'Lidacoa123*')

        # Convertimos el objeto mensaje a texto
        texto = mensaje.as_string()

        # Enviamos el mensaje
        sesion_smtp.sendmail(remitente, destinatarios, texto)

        # Cerramos la conexión
        sesion_smtp.quit()

    for i in range(0,len(arregloDescarga)):
        arregloDescarga.pop()
    mensaje = "Se te enviará la informacion a tu correo "+ correo +" Resultado_Consulta.xlsx"
    return render(request, 'createReport.html',{"mensaje":mensaje,"e":name})

def generarGrafico(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').get().val()['name']
    nombre_BaseDatos = []
    titulo = []
    fechaInicial = []
    fechaFinal = []
    formato = []
    Total = []
    fechaInicio = request.GET.get('fechaInicio')
    fechaFin = request.GET.get('fechaFin')
    tituloGrafico = str(fechaInicio) + " / " + str(fechaFin)

    for i in arregloDescarga:
        nombre_BaseDatos.append(i['Base de Datos'])
        fechaInicial.append(i['Fecha de Inicio'])
        fechaFinal.append(i['Fecha de Fin'])
        formato.append(i['Formato'])
        Total.append(i['Total Item Requests'])
    data = pd.DataFrame({
        'Base de Datos': nombre_BaseDatos,
        'Formato': formato,
        'Fecha de Inicio': fechaInicial,
        'Fecha de Fin': fechaFinal,
        'Total Item Requests': Total
    })

    agrupar = data.groupby(['Base de Datos'])['Total Item Requests'].sum().reset_index()
    name_DB = []
    total_DB = []
    for index, row in agrupar.iterrows():
        name_DB.append(row['Base de Datos'])
        total_DB.append(row['Total Item Requests'])

    f = plt.figure()
    axes = f.add_axes([0.15, 0.15, 0.75, 0.75])
    xx = range(len(total_DB))

    axes.bar(xx, total_DB, width=0.8, align='center')
    axes.set_xticks(xx)
    axes.set_xticklabels(name_DB)
    axes.set_title(tituloGrafico)
    axes.set_xlabel('Base de Datos')
    axes.set_ylabel('Total Items Request')

    buf = io.BytesIO()
    canvas = FigureCanvasAgg(f)
    canvas.print_png(buf)
    # Creamos la respuesta enviando los bytes en tipo imagen png
    response = HttpResponse(buf.getvalue(), content_type='image/png')
    # Limpiamos la figura para liberar memoria
    f.clear()
    # Añadimos la cabecera de longitud de fichero para más estabilidad
    response['Content-Length'] = str(len(response.content))
    # Devolvemos la response
    return response

def vistaGrafica(request):
    fechaInicial = request.GET.get('fechaInicio')
    fechaFin = request.GET.get('fechaFin')
    if(fechaInicial!='' and len(fechaInicial)>10):fechaInicial = fechaInicial[0:len(fechaInicial) - 10]
    if(fechaFin!='' and len(fechaFin)>10):fechaFin = fechaFin[0:len(fechaFin) - 10]
    return render(request, 'visualizarGrafica.html',context={"fechaInicio":fechaInicial,"fechaFin":fechaFin})

def verReporte(request):
    idToken = request.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
    name = database.child('users').child(a).child('details').get().val()['name']
    arreglodeConsultas = []
    fechaInicial = datetime.strptime(str(request.POST.get('fechaInicial')), '%Y-%m-%d')
    #direccion= request.POST.get('direccion')
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
            consultas = database.child('Consulta').get()
            for i in consultas.each():
                if (i.val()['Base de Datos']==nombreBaseDatos):
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
                                    if "PR" in formato:
                                        consultaTotalItemRequest = 0
                                        cunsoltaUniqueTitleInvestigation = 0
                                        consultaUniqueItemInvestigation = 0
                                        consultaTotalItemInvestigation = 0
                                        consultaSearchesPlatform = 0

                                        if i.val()['Total Item Requests']:
                                            consultaTotalItemRequest = i.val()['Total Item Requests']
                                        if i.val()['Unique Titile Investigations']:
                                            cunsoltaUniqueTitleInvestigation = i.val()['Unique Titile Investigations']
                                        if i.val()['Unique Item Investigation']:
                                            consultaUniqueItemInvestigation = i.val()['Unique Item Investigation']
                                        if i.val()['Total Item Investigation']:
                                            consultaTotalItemInvestigation = i.val()['Total Item Investigation']
                                        if i.val()['Searches Platform']:
                                            consultaSearchesPlatform = i.val()['Searches Platform']

                                        visualizacionConsulta = {
                                            "Base de Datos": i.val()['Base de Datos'],
                                            "Formato": i.val()['Formato'],
                                            "Fecha de Inicio": i.val()['Fecha de Inicio'],
                                            "Fecha de Fin": i.val()['Fecha de Fin'],
                                            "Total Item Requests": consultaTotalItemRequest,
                                            "Unique Titile Investigations": cunsoltaUniqueTitleInvestigation,
                                            "Unique Item Investigation": consultaUniqueItemInvestigation,
                                            "Total Item Investigation": consultaTotalItemInvestigation,
                                            "Searches Platform": consultaSearchesPlatform,
                                        }
                                    elif "TR_J" in formato:
                                        baseDatos = i.val()['Base de Datos']
                                        total = i.val()['Total']
                                        visualizacionConsulta = {
                                            "Base de Datos": baseDatos,
                                            "Titulo": i.val()['Titulo'],
                                            "Formato": formato,
                                            "Fecha de Inicio": i.val()['Fecha de Inicio'],
                                            "Fecha de Fin": i.val()['Fecha de Fin'],
                                            "Total": total
                                        }
                                    arregloAux.append(visualizacionConsulta)

            if "PR" in formato:
                for i in range(0, len(arregloAux) - 1):
                    for j in range(i + 1, len(arregloAux)):
                        if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]

            elif "TR_J" in formato:
                for i in range(0, len(arregloAux) - 1):
                    for j in range(i + 1, len(arregloAux)):
                        if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]

                for i in range(0, len(arregloAux) - 1):
                    for j in range(i + 1, len(arregloAux)):
                        if arregloAux[j]['Titulo'] < arregloAux[i]['Titulo']:
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]



            for i in arregloAux:
                arreglodeConsultas.append(i)
                arregloDescarga.append(i)
        if "PR" in formato:
            return render(request, 'verConsultaTipoFormatoI.html',context={"consultaRealizada": arreglodeConsultas,"formato": formato, "e":name,"fechaInicio":fechaInicial,"fechaFin":fechaFinal})
        elif "TR_J" in formato:
            return render(request, 'verConsultaTipoFormatoII.html',context={"consultaRealizada": arreglodeConsultas,"formato": formato, "e":name})

    else:
        nombreBasesDatos = database.child('bases_Datos').get()
        for baseDatos in nombreBasesDatos.each():
            arregloAux = []
            nameDataBase = baseDatos.val()['nameDataBase']
            if request.POST.get(nameDataBase) == "1":
                consultas = database.child('Consulta').get()
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
                        if i.val()['Base de Datos'] == str(nameDataBase):
                            if yearInicioConsulta >= yearInicial and yearFinalConsulta <= yearFinal:
                                if mesInicioConsulta >= mesInical and mesFinalConsulta <= mesFinal:
                                    if diaInicioConsulta >= diaInicial and diaFinalConsulta <= diaFinal:

                                        if "PR" in formato:
                                            consultaTotalItemRequest = 0
                                            cunsoltaUniqueTitleInvestigation = 0
                                            consultaUniqueItemInvestigation = 0
                                            consultaTotalItemInvestigation = 0
                                            consultaSearchesPlatform = 0

                                            if i.val()['Total Item Requests']:
                                                consultaTotalItemRequest = i.val()['Total Item Requests']
                                            if i.val()['Unique Titile Investigations']:
                                                cunsoltaUniqueTitleInvestigation = i.val()[
                                                    'Unique Titile Investigations']
                                            if i.val()['Unique Item Investigation']:
                                                consultaUniqueItemInvestigation = i.val()['Unique Item Investigation']
                                            if i.val()['Total Item Investigation']:
                                                consultaTotalItemInvestigation = i.val()['Total Item Investigation']
                                            if i.val()['Searches Platform']:
                                                consultaSearchesPlatform = i.val()['Searches Platform']

                                            visualizacionConsulta = {
                                                "Base de Datos": i.val()['Base de Datos'],
                                                "Formato": i.val()['Formato'],
                                                "Fecha de Inicio": i.val()['Fecha de Inicio'],
                                                "Fecha de Fin": i.val()['Fecha de Fin'],
                                                "Total Item Requests": consultaTotalItemRequest,
                                                "Unique Titile Investigations": cunsoltaUniqueTitleInvestigation,
                                                "Unique Item Investigation": consultaUniqueItemInvestigation,
                                                "Total Item Investigation": consultaTotalItemInvestigation,
                                                "Searches Platform": consultaSearchesPlatform,
                                            }
                                        elif "TR_J" in formato:
                                            baseDatos = i.val()['Base de Datos']
                                            total = i.val()['Total']
                                            visualizacionConsulta = {
                                                "Base de Datos": baseDatos,
                                                "Titulo": i.val()['Titulo'],
                                                "Formato": formato,
                                                "Fecha de Inicio": i.val()['Fecha de Inicio'],
                                                "Fecha de Fin": i.val()['Fecha de Fin'],
                                                "Total": total
                                            }
                                        arregloAux.append(visualizacionConsulta)
            if "PR" in formato:
                for i in range(0, len(arregloAux) - 1):
                    for j in range(i + 1, len(arregloAux)):
                        if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]

            elif "TR_J" in formato:
                for i in range(0, len(arregloAux) - 1):
                    for j in range(i + 1, len(arregloAux)):
                        if arregloAux[j]['Fecha de Inicio'] < arregloAux[i]['Fecha de Inicio']:
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]

                for i in range(0, len(arregloAux) - 1):
                    for j in range(i + 1, len(arregloAux)):
                        if arregloAux[j]['Titulo'] < arregloAux[i]['Titulo']:
                            arregloAux[i], arregloAux[j] = arregloAux[j], arregloAux[i]
            for i in arregloAux:
                arreglodeConsultas.append(i)
                arregloDescarga.append(i)

        if "PR" in formato:
            return render(request, 'verConsultaTipoFormatoI.html',context={"consultaRealizada": arreglodeConsultas,"formato": formato, "e":name,"fechaInicio":fechaInicial,"fechaFin":fechaFinal})
        elif "TR_J" in formato:
            return render(request, 'verConsultaTipoFormatoII.html',context={"consultaRealizada": arreglodeConsultas,"formato": formato, "e":name})
