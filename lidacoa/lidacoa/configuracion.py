from django.shortcuts import  render
import pyrebase
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

def agregarConfiguracion(diccionario,nombrebaseDeDatos,fechaInicial,fechaFinal,formato):
    consulta = False
    arregloTemp =[]
    diccionarioFormato = {}
    arregloLlaves = diccionario.keys()
    if (str(nombrebaseDeDatos)+"/"+str(formato) in arregloLlaves): # si esta la BD en el diccionario
        separadorFechaInicial = fechaInicial.index('-')
        separadorFechaFinal = fechaFinal.index('-')
        if(int(fechaInicial[0:separadorFechaInicial])==int(fechaFinal[0:separadorFechaFinal])): # si son del mismo año
            for i in range(int(fechaInicial[-5:-3]),int(fechaFinal[-5:-3])+1):
                if(not(str(int(fechaInicial[0:separadorFechaInicial]))+"-"+str(i)+"-30" in diccionario[str(nombrebaseDeDatos)+"/"+str(formato)])):
                    consulta= True
                    diccionario[str(nombrebaseDeDatos)+"/"+str(formato)].append(str(int(fechaInicial[0:separadorFechaInicial]))+"-"+str(i)+"-30")
        else:
            for i in range(int(fechaInicial[0:separadorFechaInicial]),int(fechaFinal[0:separadorFechaFinal])+1):
                if (i == int(fechaFinal[0:separadorFechaFinal])):
                    for j in range(1,int(fechaFinal[-5:-3])+1):
                        if(not(str(i)+"-"+str(j)+"-30" in diccionario[str(nombrebaseDeDatos)+"/"+str(formato)])):
                            consulta= True
                            diccionario[str(nombrebaseDeDatos)+"/"+str(formato)].append(str(i)+"-"+str(j)+"-30")
                else:
                    for j in range(1,13):
                        if(not(str(i)+"-"+str(j)+"-30" in diccionario[str(nombrebaseDeDatos)+"/"+str(formato)])):
                            consulta= True
                            diccionario[str(nombrebaseDeDatos)+"/"+str(formato)].append(str(i)+"-"+str(j)+"-30")
    else:
        diccionario[str(nombrebaseDeDatos)+"/"+str(formato)] = []
        crearArregloConfiguracion(diccionario,nombrebaseDeDatos,fechaInicial,fechaFinal,formato)
        consulta= True
    return consulta

def crearArregloConfiguracion(diccionario,nombrebaseDeDatos1,fechaInicial1,fechaFinal1,formato1):
    separadorFechaInicial = fechaInicial1.index('-')
    separadorFechaFinal = fechaFinal1.index('-')
    if(int(fechaInicial1[0:separadorFechaInicial])==int(fechaFinal1[0:separadorFechaFinal])): # si son del mismo año
        for i in range(int(fechaInicial1[-5:-3]),int(fechaFinal1[-5:-3])+1):
            diccionario[str(nombrebaseDeDatos1)+"/"+str(formato1)].append(str(int(fechaInicial1[0:separadorFechaInicial]))+"-"+str(i)+"-30")
    else:
        for i in range(int(fechaInicial1[0:separadorFechaInicial]),int(fechaFinal1[0:separadorFechaFinal])+1):
            for j in range(1,13):
                if(not(str(i)+"-"+str(j)+"-30" in diccionario[str(nombrebaseDeDatos1)+"/"+str(formato1)])):
                    consulta= True
                    diccionario[str(nombrebaseDeDatos1)+"/"+str(formato1)].append(str(i)+"-"+str(j)+"-30")