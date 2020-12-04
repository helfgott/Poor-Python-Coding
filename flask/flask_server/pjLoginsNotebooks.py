#!/usr/bin/python
from pymongo import MongoClient
from datetime import datetime
import json

# establish connex
uri = "mongodb://admin:password@localhost/pjData?authSource=admin"
conn = MongoClient(uri)

# create db
db = conn.pjData

# create collection
collection = db.pjLoginsNB

# <-------------------------------------------------------- INSERT 
# Funciones o clases para insertar datos
def insertLoginMongo(LoginNotebook) :
    """
    Agregar el intento de Login en Mongo
    """
    insertLoginNotebook = collection.insert(LoginNotebook)
    return 'Registro de Login de Notebook'

