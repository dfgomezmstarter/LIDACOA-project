from django.shortcuts import  render
import pyrebase
import time
from datetime import datetime
from django.contrib import auth



config = {
    'apiKey': "AIzaSyAGBKr0cSU1ocPy7SXxIBBuTylDBxHmD-o",
    'authDomain': "lidacoa.firebaseapp.com",
    'databaseURL': "https://lidacoa.firebaseio.com",
    'projectId': "lidacoa",
    'storageBucket': "lidacoa.appspot.com",
    'messagingSenderId': "696040231838",
    'appId': "1:696040231838:web:a0ff0aec08cf241b727c8f",
    'measurementId': "G-0PC4JJMEWH"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()


diccionario ={}
diccionarioFechas = {}
FinDeMes = {'01':'-31','02':'-28','03':'-31','04':'-30','05':'-31','06':'-30','07':'-31','08':'-31','09':'-30','10':'-31','11':'-30','12':'-31'}
arregloFaltantes = []
#diccionario['Cual Quier Cosa']=["kbsrjvajsv","nvsbbasbdkbsa"]

def fechaDeConsulta():
    now = datetime.now()
    format = str(now.strftime('Día :%d, Mes: %m, Año: %Y, Hora: %H, Minutos: %M, Segundos: %S'))
    return format

def limpiarArreglo():
    arregloFaltantes=[]

def agregarConfiguracion(fechasFaltantes,diccionario,nombrebaseDeDatos,fechaInicial,fechaFinal,formato):
    consulta = False
    arregloLlaves = diccionario.keys()
    if (str(nombrebaseDeDatos) + "/" + str(formato) in arregloLlaves):  # si esta la BD en el diccionario
        separadorFechaInicial = fechaInicial.index('-')
        separadorFechaFinal = fechaFinal.index('-')
        if (int(fechaInicial[0:separadorFechaInicial]) == int(fechaFinal[0:separadorFechaFinal])):  # si son del mismo año
            for i in range(int(fechaInicial[-5:-3]), int(fechaFinal[-5:-3]) + 1):
                if i >= 10:
                    fechaIngresar = str(int(fechaInicial[0:separadorFechaInicial])) + "-" + str(i) + "-30"
                else:
                    fechaIngresar = str(int(fechaInicial[0:separadorFechaInicial])) + "-0" + str(i) + "-30"
                if (not (fechaIngresar in diccionario[str(nombrebaseDeDatos) + "/" + str(formato)])):
                    consulta = True
                    diccionario[str(nombrebaseDeDatos) + "/" + str(formato)].append(fechaIngresar)
                    fechasFaltantes.append(fechaIngresar)
        else:
            for i in range(int(fechaInicial[0:separadorFechaInicial]), int(fechaFinal[0:separadorFechaFinal]) + 1):
                if (i == int(fechaFinal[0:separadorFechaFinal])):
                    for j in range(1, int(fechaFinal[-5:-3]) + 1):
                        if j >= 10:
                            fechaIngresar = str(int(fechaInicial[0:separadorFechaInicial])) + "-" + str(j) + "-30"
                        else:
                            fechaIngresar = str(int(fechaInicial[0:separadorFechaInicial])) + "-0" + str(j) + "-30"
                        if (not (fechaIngresar in diccionario[str(nombrebaseDeDatos) + "/" + str(formato)])):
                            consulta = True
                            diccionario[str(nombrebaseDeDatos) + "/" + str(formato)].append(fechaIngresar)
                            fechasFaltantes.append(fechaIngresar)
                else:
                    for j in range(1, 13):
                        if j >= 10:
                            fechaIngresar = str(str(i) + "-" + str(j) + "-30")
                        else:
                            fechaIngresar = str(str(i) + "-0" + str(j) + "-30")
                        if (not (fechaIngresar in diccionario[str(nombrebaseDeDatos) + "/" + str(formato)])):
                            consulta = True
                            diccionario[str(nombrebaseDeDatos) + "/" + str(formato)].append(fechaIngresar)
                            fechasFaltantes.append(fechaIngresar)
    else:
        diccionario[str(nombrebaseDeDatos) + "/" + str(formato)] = []
        crearArregloConfiguracion(fechasFaltantes, diccionario, nombrebaseDeDatos, fechaInicial, fechaFinal, formato)
        consulta = True
    return consulta

def crearArregloConfiguracion(fechasFaltantes,diccionario,nombrebaseDeDatos1,fechaInicial1,fechaFinal1,formato1):
    separadorFechaInicial = fechaInicial1.index('-')
    separadorFechaFinal = fechaFinal1.index('-')
    if(int(fechaInicial1[0:separadorFechaInicial])==int(fechaFinal1[0:separadorFechaFinal])): # si son del mismo año
        for i in range(int(fechaInicial1[-5:-3]),int(fechaFinal1[-5:-3])+1):
            if i >= 10:
                fechaIngresar = str(str(int(fechaInicial1[0:separadorFechaInicial])) + "-" + str(i) + "-30")
            else:
                fechaIngresar = str(str(int(fechaInicial1[0:separadorFechaInicial])) + "-0" + str(i) + "-30")
            diccionario[str(nombrebaseDeDatos1)+"/"+str(formato1)].append(fechaIngresar)
            fechasFaltantes.append(fechaIngresar)
    else:
        for i in range(int(fechaInicial1[0:separadorFechaInicial]),int(fechaFinal1[0:separadorFechaFinal])+1):
            if (i == int(fechaFinal1[0:separadorFechaFinal])):
                for j in range(1,int(fechaFinal1[-5:-3])+1):
                    if j>=10:
                        fechaIngresar = str(str(i)+"-"+str(j)+"-30")
                    else:
                        fechaIngresar = str(str(i)+"-0"+str(j)+"-30")
                    if(not(fechaIngresar in diccionario[str(nombrebaseDeDatos1)+"/"+str(formato1)])):
                        diccionario[str(nombrebaseDeDatos1)+"/"+str(formato1)].append(fechaIngresar)
                        fechasFaltantes.append(fechaIngresar)
            else:
                for j in range(1,13):
                    if j>=10:
                        fechaIngresar = str(str(i)+"-"+str(j)+"-30")
                    else:
                        fechaIngresar = str(str(i)+"-0"+str(j)+"-30")
                    if(not(fechaIngresar in diccionario[str(nombrebaseDeDatos1)+"/"+str(formato1)])):
                        diccionario[str(nombrebaseDeDatos1)+"/"+str(formato1)].append(fechaIngresar)
                        fechasFaltantes.append(fechaIngresar)

arregloDescarga=[]

def limpiarArregloDescargar():
    arregloDescarga = []

