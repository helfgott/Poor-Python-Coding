#!/usr/bin/python
from pymongo import MongoClient
from datetime import datetime
import json

# establish connex
uri = "mongodb://localhost/gsdData?authSource=admin"
conn = MongoClient(uri)

# create db
db = conn.gsdData

# create collection
collection = db.gsdRCstatus

# <-------------------------------------------------------- INSERT 
# Funciones o clases para insertar datos
def insertMongo(RCstatus) :
    """
    Agregar estado de RC en mongo 
    """
    try :
        insertRCstatus = collection.insert(RCstatus)
        return {
                'ReturnCode': 222,
                'ReturnValue': str(insertRCstatus),
                'ReturnMessage': str('Se ha insertado el dato de las RC en servidor correctamente.')
                }
    except Exception as e:
        return {
                'ReturnCode': 111,
                'ReturnError': str(e),
                'ReturnMessage': 'No es posible agregar el dato en Mongo: {}'.format(e) 
                }

def updateMongo(server, RCstatus) :
    """
    Con la condicion upsert, si el objeto como coleccion no existe, entonces lo crea. Si ya existe, entonces lo actualiza. 
    """
    try :
        updateRCstatus = collection.update( {"server" : server}, RCstatus, upsert=True)
        return {
                'ReturnCode': 444,
                'ReturnValue': str(updateRCstatus),
                'ReturnMessage': str('Se ha updateado el dato de las RC en servidor correctamente.')
                }
    except Exception as e:
        return {
                'ReturnCode': 333,
                'ReturnError': str(e),
                'ReturnMessage': 'No es posible agregar el dato en Mongo: {}'.format(e) 

                }
