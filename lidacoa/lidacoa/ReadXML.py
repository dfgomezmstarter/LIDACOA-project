import xml.etree.ElementTree as tr
import lxml.etree as etree
from lxml import etree
"""""
PRIMER INTENTO CON EL MÉTODO PARA VER EL XML COMO UN ARBOL
"""""
doc = etree.parse('prueba')
rval = {}
for org in doc.xpath('//orgID[text()="127"]'):
    for ancestor in org.iterancestors('Department'):
        id=ancestor.find('./orgID').text
        name=ancestor.find('./name').text
        rval[name]=id

#print(rval)

"""""
SEGUNDO INTENTO CON EL MÉTODO MANUAL CON CICLOS Y CONDICIONALES
"""""
file_xml= tr.parse('Respuesta_BDD_ACS')

raiz = file_xml.getroot()


def encontrarCustomer(firstRoot):
    rootCustomer=firstRoot
    return rootCustomer


raiz2 = raiz[0]
raiz3 = raiz2[0]
raiz4 = raiz3[3]
raiz5 = raiz4[0]
raiz6 = raiz5[1]
raiz7 = raiz6[3]

#print(len(raiz3))
#print(str(raiz2[0]))
#print(str(raiz2[0])[53])

#for hijo in raiz7:
 #   print(hijo)

""""
 TERCER INTENTO CONVIRTIENDO EL XML A JSON PARA ANALIZARLO MEJOR
 NOTA: NO LO CONVIERTE CON UN FORMATO JSON SINO QUE CREA UN DICCIONARIO CON TODO LA INFORMACIÓN

with open('prueba') as in_file:
    xml = in_file.read()
    with open('jsondata.json', 'w') as out_file:
        json.dump(xmltodict.parse(xml), out_file)


"""
import xmltodict
import json
import csv
import pandas as pd



leer = json.loads(open('jsondata.json').read())
print(leer)


f = csv.writer(open("test.csv", "wb+"))

df = pd.read_csv('test.csv')
print(df)
