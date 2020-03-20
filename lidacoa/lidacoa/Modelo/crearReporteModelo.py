from ..configuracion import *
from urllib.request import Request, urlopen
import json

def create_report(requets):
    aux = requets.POST.get('aux')
    aux = aux[0:len(aux)-1]
    aux = aux.split(",")
    arreglo=[]
    for i in aux:
        valor=i[2:len(i)-1]
        help = requets.POST.get(valor)
        if str(help) == "1":
            arreglo.append(valor)
    print("Arreglo de base de datos: " +str(arreglo)) # Mostrar el arreglo de las bdb que se seleccionaron
    formato = requets.POST.get('formato')
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
                #print(informacionUso)
                print("---------------------------------------------------------------------------")
                print()

    #datos= database.child('bases_Datos').child(a).get().val()['nameDataSet']
    #print(datos)

    return render(requets, 'welcome.html')

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
    print(formato)
    peticion=Request(formato, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(peticion).read()
    decoded = json.loads(webpage)
    return decoded
