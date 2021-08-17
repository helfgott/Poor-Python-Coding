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
def displayRC() :
    """
    Agregar estado de RC en mongo 
    """
    displayRCstatus = collection.find()
    return displayRCstatus
