from ..configuracion import *
from urllib.request import Request, urlopen
import json
from time import time

def create_report(requets):
    tiempoInicial = time()
    arregloConsultas=[]
    aux = requets.POST.get('aux')
    aux = aux[0:len(aux)-1]
    aux = aux.split(",")
    arreglo=[]
    for i in aux:
        valor=i[2:len(i)-1]
        help = requets.POST.get(valor)
        if str(help) == "1":
            arreglo.append(valor)
    formato="PR_P1"
    #formato = requets.POST.get('formato')
    #bd = requets.POST.get('basesDeDatos')
    #print("formato: " + str(formato))
    idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']

    listaBD = database.child('bases_Datos').get()

    for seleccionBD in range(len(arreglo)):
        for BD in listaBD.each():
            if (str(BD.val()['nameDataBase']) == arreglo[seleccionBD]):
                url=BD.val()['url']
                customer_id= BD.val()['customer_id']
                requestor_id = BD.val()['requestor_id']
                api_key = BD.val()['api_key']
                begin_date = requets.POST.get('fechaInicial')
                end_date = requets.POST.get('fechaFinal')
                platform = BD.val()['platform']
                informacionUso = pedirInformacion(url,customer_id,requestor_id,api_key,begin_date,end_date,platform,formato)
                #print("Informacion: " + str(informacionUso))
                nombreBaseDatos=BD.val()['nameDataBase']
                for informacion in informacionUso['Report_Items']:
                    performance = informacion['Performance']
                    for i in performance:
                        fechaInicio = i['Period']['Begin_Date']
                        fechaFinal = i['Period']['End_Date']
                        for j in i['Instance']:
                            if j['Metric_Type'] == "Total_Item_Requests":
                                totalMes = j['Count']
                                consultaRealizada = {
                                    "nombreBaseDatos": nombreBaseDatos,
                                    "formatoConsulta": formato,
                                    "fechaInicio": fechaInicio,
                                    "fechaFinal": fechaFinal,
                                    "totalMes": totalMes
                                }
                                database.child('Consulta').push(consultaRealizada)
                                arregloConsultas.append(consultaRealizada)
                #consultaRealizada=organizarReporte(informacionUso, begin_date, end_date, formato,nombreBaseDatos)
                #database.child('Consulta').push(consultaRealizada)
    tiempoFinal = time()
    print("Tiempo: " + str(tiempoFinal - tiempoInicial))
    return render(requets, 'verConsulta.html',context={"consultaRealizada":arregloConsultas})

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

"""def organizarReporte(archivoJson, begin_date, end_date, formato,nombreBaseDatos):
    totalReporte = 0
    for informacion in archivoJson['Report_Items']:
        performance = informacion['Performance']
        for i in performance:
            fechaInicio = i['Period']['Begin_Date']
            fechaFinal = i['Period']['End_Date']
            for j in i['Instance']:
                if j['Metric_Type'] == "Total_Item_Requests":
                    cantidad = j['Count']
                    print("Fecha Inicio: " + str(fechaInicio))
                    print("Fecha Final: " + str(fechaFinal))
                    print("Cantidad: " + str(cantidad))
                    totalReporte = totalReporte + cantidad
    consultaRealizada={
        "nombreBaseDatos":nombreBaseDatos,
        "formatoConsulta":formato,
        "fechaInicio":begin_date,
        "fechaFinal":end_date,
        "totalReporte":totalReporte
    }
    return consultaRealizada"""



"""
Metodo para la consulta, sin un ciclo... Pero se demora más asi que que gonorrea pas
tiempoInicial = time()
    arregloConsultas = []
    formato = "PR_P1"
    # formato = requets.POST.get('formato')
    # bd = requets.POST.get('basesDeDatos')
    # print("formato: " + str(formato))
    idToken = requets.session['uid']
    a = authe.get_account_info(idToken)
    a = a['users']
    a = a[0]
    a = a['localId']
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
            informacionUso = pedirInformacion(url, customer_id, requestor_id, api_key, begin_date, end_date, platform, formato)
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
                                "nombreBaseDatos": nombreBaseDatos,
                                "formatoConsulta": formato,
                                "fechaInicio": fechaInicio,
                                "fechaFinal": fechaFinal,
                                "totalMes": totalMes
                            }
                            database.child('Consulta').push(consultaRealizada)
                            arregloConsultas.append(consultaRealizada)
            # consultaRealizada=organizarReporte(informacionUso, begin_date, end_date, formato,nombreBaseDatos)
            # database.child('Consulta').push(consultaRealizada)
        tiempoFinal = time()
        print("Tiempo: " + str(tiempoFinal-tiempoInicial))
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
                                    "nombreBaseDatos": nombreBaseDatos,
                                    "formatoConsulta": formato,
                                    "fechaInicio": fechaInicio,
                                    "fechaFinal": fechaFinal,
                                    "totalMes": totalMes
                                }
                                database.child('Consulta').push(consultaRealizada)
                                arregloConsultas.append(consultaRealizada)
                # consultaRealizada=organizarReporte(informacionUso, begin_date, end_date, formato,nombreBaseDatos)
                # database.child('Consulta').push(consultaRealizada)
        tiempoFinal = time()
        print("Tiempo: " + str(tiempoFinal - tiempoInicial))
        return render(requets, 'verConsulta.html', context={"consultaRealizada": arregloConsultas})
"""
