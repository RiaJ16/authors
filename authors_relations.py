# -*- coding: utf-8 -*-
"""
/***************************************************************************
 AUTHORS
        copyright        : (C) 2020 by Jair Nájera / HTech
        email            : jair.najera@htech.mx
 ***************************************************************************/
/***************************************************************************
 *																		   *
 *	 This program is free software; you can redistribute it and/or modify  *
 *	 it under the terms of the GNU General Public License as published by  *
 *	 the Free Software Foundation; either version 2 of the License, or	   *
 *	 (at your option) any later version.								   *
 *																		   *
 ***************************************************************************/
"""

import ast
import json
import os


def print_json(filename, dictionary):
    try:
        with open(filename, 'w') as file:
            json.dump(dictionary, file)
        print("Archivo %s almacenado satisfactoriamente." % filename)
    except FileNotFoundError:
        print("Error con la ruta seleccionada.")


def print_dictionary(filename, dictionary):
    errores = 0
    try:
        with open(filename, 'w', newline='\n') as file:
            for autor in dictionary:
                try:
                    file.write(json.dumps(dictionary[autor]) + "\n")
                except UnicodeEncodeError:
                    print(json.dumps(dictionary[autor]))
                    errores += 1
        print("Se encontró el siguiente número de errores al exportar la información: %d." % errores)
        print("Archivo %s almacenado satisfactoriamente." % filename)
    except FileNotFoundError:
        print("Error con la ruta seleccionada.")


# Ruta del archivo a abrir
file1 = "%s/secondresults.txt" % os.path.expanduser('~')
# Ruta de uno de los archivos para exportar la información
outfile = "%s/output.json" % os.path.expanduser('~')
# Ruta de uno de los archivos para exportar la información
outfileAutores = "%s/outputautores.json" % os.path.expanduser('~')
archivo = open(file1, "r", encoding='utf-8')
objetos = []
for linea in archivo:
    #objetos.append(json.loads(linea)) #Comillas dobles
    objetos.append(ast.literal_eval(linea)) #Comillas simples
autoresRaw = []
dictAutores = dict()
for objeto in objetos:
    for autor in objeto["_source"]["authors"]:
        autoresRaw.append(autor)
i = 0
for autor in autoresRaw:
    try:
        if autor['id'] not in dictAutores:
            dictAutores[autor['id']] = {"name": autor['name'], "newId": "%09d" % i}
            i += 1
    except KeyError:
        try:
            if autor['id'] not in dictAutores:
                dictAutores[autor['id']] = {"name": '', "newId": "%09d" % i}
                i += 1
        except KeyError:
            try:
                if autor['name'] not in dictAutores:
                    dictAutores[autor['name']] = {"name": autor['name'], "newId": "%09d" % i}
                    i += 1
            except KeyError:
                try:
                    if autor['org'] not in dictAutores:
                        dictAutores[autor['org']] = {"name": autor['org'], "newId": "%09d" % i}
                        i += 1
                except KeyError:
                    pass
dictRelaciones = dict()
for objeto in objetos:
    autoresLocales = []
    llave = ''
    for autor in objeto["_source"]["authors"]:
        try:
            llave = autor['id']
        except KeyError:
            try:
                llave = autor['name']
            except KeyError:
                try:
                    llave = autor['org']
                except KeyError:
                    pass
        if not (llave == ''):
            autoresLocales.append(dictAutores[llave])
    if not (llave == ''):
        for i in range(0, len(autoresLocales)):
            for j in range(i + 1, len(autoresLocales)):
                llaveRelacion1 = "%s%s" % (autoresLocales[i]['newId'], autoresLocales[j]['newId'])
                llaveRelacion2 = "%s%s" % (autoresLocales[j]['newId'], autoresLocales[i]['newId'])
                if llaveRelacion1 not in dictRelaciones:
                    if llaveRelacion2 not in dictRelaciones:
                        dictRelaciones[llaveRelacion1] = {'a1Id': autoresLocales[i]['newId'],
                                                          'a1Nombre': autoresLocales[i]['name'],
                                                          'a2Id': autoresLocales[j]['newId'],
                                                          'a2Nombre': autoresLocales[j]['name'],
                                                          'weight': 1}
                    else:
                        dictRelaciones[llaveRelacion2]['weight'] += 1
                else:
                    dictRelaciones[llaveRelacion1]['weight'] += 1

print("Cálculo finalizado. Se encontraron %d autores y %d relaciones." % (len(dictAutores), len(dictRelaciones)))
print("Exportando...")

# La información obtenida se almacenó en dos diccionarios, dictAutores y dictRelaciones. Se usa la función print_json
# para almacenar dicha información en un archivo. El primer argumento de la función es la ruta completa del archivo y
# el segundo es el diccionario a exportar.
print_json(outfile, dictRelaciones)
#print_json(outfileAutores, dictAutores)
# print_dictionary(outfile, dictRelaciones)
# print_dictionary(outfileAutores, dictAutores)