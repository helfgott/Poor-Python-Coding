#!/usr/bin/python
# --------------------------------------------------------------------------- Logging
# avoiding to use dict.config from flask
# Logging file while land in private systemd /tmp folder
import logging
logFormat = '%(asctime)s : %(levelname)s : %(filename)s : %(message)s'
logging.basicConfig(filename='/tmp/apilogging.log',filemode='w', format=logFormat, datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)

import flask
from flask import Flask, render_template, request
# --------------------------------------------------------------------------- Load rest of the modules
from PJVariables import LDAPSERVER 
import pjTestLDAP          		# Este modulo tiene una funcion para verificar la conexion basica a LDAP
#import pjLoginsNotebooks
import pjChallengeLDAP     		# Este modulo se encarga de presentar usuario y clave a LDAP para validarlo
import pjPasswordChangeRequests 	# Con este modulo invocamos el cambio de password de un usuario
import pjParameters			# Controla los parametros centralizados de los clientes
import json, time, sys
#from pymongo import MongoClient
from datetime import datetime
app = Flask(__name__)
sys.dont_write_bytecode = True 		# Deshabilita la cache de python

# ___________________________________________________ [[  NOTEBOOKS ]] ________________________________________________

@app.route("/")
def hello():
        return str('API PJ, consulte documentacion en: http://url_docs')

@app.route('/post/notebooks/passwordchange', methods = ['POST'])
def passwordChangeHandlerPJ():
    """
    Se encarga de cambiar claves vencidas
    """
    logging.info('Invocamos /post/notebooks/passwordchange')
    passwordChangeRequest = request.get_json()
    # Preparamos los datos para consultar a LDAP
    USER = passwordChangeRequest['user']
    PASSWORD = passwordChangeRequest['currentpassword']
    NEWPASSWORD = passwordChangeRequest['newpassword']
    changePassword = pjPasswordChangeRequests.cambioClave(USER,PASSWORD,NEWPASSWORD)
    return str(changePassword)

@app.route('/post/logins/notebooks', methods = ['POST'])
def loginHandlerPJ():
   """
    Procesa el login de los usuarios 
   """
   logging.info('Invocamos /post/logins/notebooks')
   # Recibimos la peticion en formato JSON
   LoginNotebook = request.get_json()
   # Registramos el Login
   # deshabilitado 29/30/2020 hasta tener pymongo en rhel
   #registerLogin = pjLoginsNotebooks.insertLoginMongo(LoginNotebook)
   # Preparamos los datos para consultar a LDAP
   USER = LoginNotebook['user']
   PASSWORD = LoginNotebook['password']
   USERTYPE = LoginNotebook['usertype']
   challengeLDAP = pjChallengeLDAP.conectarLDAP(USER, PASSWORD, USERTYPE, LDAPSERVER)
   return str(challengeLDAP) # Siempre debemos regresar un string

@app.route('/post/logins/parameters', methods = ['POST'])
def loginParametersPJ():
    """
    Determina los parametros centralizados, por ejemplo que todas las notebooks inicien con cliente viejo o nuevo de thetech 
    El cliente envia TRUE si quiere los parametros del servidor o FALSE si no
    """
    logging.info('Invocamos /post/logins/parameters')
    getParameters = request.get_json()
    if getParameters == True :
        getParametersforNotebooks = pjParameters.requestStartParameters() 
        return json.dumps(
                {
                    'ReturnCode' : int(666),
                    'ReturnMessage' : 'Parametros Centralizados',
                    'ReturnValue':getParametersforNotebooks
                }
                )
    else:
        return json.dumps( 
                 {
                    'ReturnCode' : int(665),
                    'ReturnMessage' : 'El cliente rechaza las variables centralizadas. Se usan variables locales definidas en el cliente.',
                    'ReturnValue': '{}'
                }
                )   

