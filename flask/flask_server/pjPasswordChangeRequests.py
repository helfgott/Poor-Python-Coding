#!/usr/bin/python

from PJVariables import LDAPSERVER
#from pymongo import MongoClient
from datetime import datetime
import json
import pjTestLDAP # importamos la request basica a ldap
import sys, os
import ldap, ldap.modlist
import httplib, socket, time, re
import logging
## establish connex
#uri = "mongodb://admin:secret@localhost/pjData?authSource=admin"
#conn = MongoClient(uri)
#
## create db
#db = conn.pjData
#
## create collection
#collection = db.pjLoginsNotebooks


# <-------------------------------------------------------- INSERT 
# Funciones o clases para insertar datos
def passwordChange(passwordChangeRequest) :
    """
    Registramos el evento de cambio de password por fines estadisticos y de soporte
    """
#    insertLoginNotebook = collection.insert()
#    encodedPasswords for security tests
    return 'Cambio de password para el legajo'

def testClave(USER, PASSWORD, LDAPSERVER):
	logging.info('Se inicia prueba de contrasena para: {}'.format(USER)) 
        res = ""
        try:
                testLDAPServer = pjTestLDAP.testLDAPConex( LDAPSERVER )
                ldapServer = testLDAPServer
                rta = ldapServer.simple_bind_s('cn=%s,ou=people,c=arg,o=company' % USER ,'%s' % PASSWORD)
		sucessTestClave = {
					'ReturnCode': 800,
					'ReturnValue': rta,
					'ReturnMesssage': 'Se ha cambiado con exito la contrasena.'
					}		
		logging.info('Cambio de clave exitoso para: {}, {}'.format(USER,sucessTestClave))
		return sucessTestClave 
        except ldap.INVALID_CREDENTIALS as e:
		failTestClave = {
					'ReturnCode': 801,
					'ReturnError': e,
					'ReturnMessage': 'Algo salio mal con la nueva clave, reintente ingresar con el ultimo password conocido, si no funciona, intente nuevamente con la clave nueva.'
					}

		logging.error('Error en cambio de clave para: {}, {}'.format(USER,failTestClave))
                return failTestClave 
        except ldap.SERVER_DOWN as e:
		failTestClave = {
					'ReturnCode': 803,
					'ReturnError': e,
					'ReturnMessage':'PJLogin no puede contactarse con LDAP, por favor cierre el cliente de Conectar a Sucursal e intente nuevamente.'					
					}
		logging.error('Error en cambio de clave, no puedo contactar al servidor LDAP {},{}',format(USER,failTestClave))
                return failTestClave 
        except Exception as e :
		failTestClave = {
					'ReturnCode': 805,
					'ReturnError': e,
					'ReturnMessage': 'Error inesperado en testClave, por favor intente nuevamente o reporte un caso en helpdesk.'	
					}
		logging.error(failTestClave)
                return failTestClave 
        else:
		failTestClave = {
					'ReturnCode': 807,
					'ReturnError': None,
					'ReturnMessage': 'No hay alternativas para try en testClave, por favor inicie un caso en helpdesk'
				}
		logging.error(failTestClave)
                return failTestClave 

def cambioClave(USER, CURRENTPASSWORD, NEWPASSWORD): 
	"""
        esta funcion se ocupa de cambiar la clave y probar el cambio de clave
        los mensajes por exito o error van del 700 al 799
        """ 
       
	try:
		# cthetech es un diccionario del modulo pjTestLDAP
                cthetech=pjTestLDAP.testLDAPConex(LDAPSERVER)
		#mortiz 2020/11/02: actualizo el formato de reemplazo de variables para ldapAction
                #ldapAction = cthetech.simple_bind_s('cn=%s,ou=people,c=arg,o=company' % USER ,'%s/%s' % (CURRENTPASSWORD, NEWPASSWORD))
		if cthetech['ReturnCode'] % 2 == 0 :
			ldapAction = cthetech['ReturnValue'].simple_bind_s('cn={},ou=people,c=arg,o=company'.format(USER) ,'{}/{}'.format(CURRENTPASSWORD, NEWPASSWORD))
			cthetech['ReturnValue'].unbind()
	                respuestaTestClave = testClave( USER , NEWPASSWORD , LDAPSERVER )
			if respuestaTestClave['ReturnCode'] %2 :
				testNewPassword = {
							'ReturnCode': 700,
							'ReturnValue': None,
							'ReturnMessage': 'La clave se cambio correctamente, el sistema ha probado su nueva clave, por favor intente ingresar con su nueva clave.'
							}	
				return testNewPassword
			else:
				failedTestNewPassword = {
							'ReturnCode': 701,
							'Returnvalue': None,
							'ReturnMessage': 'Al parecer se ha cambiado la clave pero no hemos podido validarlo, por favor intente ingresar con su nueva clave, si no funciona, intente con la anterior.'
							}
				return failedTestNewPassword
		else :
			return (cthetech,'<---')
	except ldap.INVALID_CREDENTIALS:
		error=sys.exc_info()[1][0]['info'].split(" ")[0]
		if(error =='R004111'):
			failCambioCalve = {
						'ReturnCode': 703,
						'ReturnError': error,
						'ReturnMessage': 'La contrasena anterior es incorrecta, intente nuevamente.'
					}
			return failCambioClave 
		elif(error =='R004128'):
			failCambioClave = {
						'ReturnCode': 705,
						'ReturnError': error,
						'ReturnMessage': 'Password invalido, no cumple con los requisitos de seguridad: Mayusculas, Minusculas, Numeros y no mayor a 8 digitos, tambien es posible que ya haya usado esa clave anteriormente, lo cual no esta permitido, intente con una nueva clave.'
						}
			logging.error('Error en cambio de clave para: {}, {}'.format(USER, failCambioClave))
			return failCambioClave
		else:
			failCambioClave = {
						'ReturnCode': 707,
						'ReturnError': error,
						'ReturnMessage': 'Error desconocido, por favor inicie un caso en helpdesk con una foto de este error.'
						}
			logging.error('Error en cambio de clave para: {}, {}'.format(USER, failCambioClave))
			return failCambioClave
	except ldap.OPERATIONS_ERROR:
		error=sys.exc_info()[1][0]['info'].split(" ")[0]
		if(error =='R000208'):
			failCambioClave = {
						'ReturnCode': 709,
						'ReturnError': error,
						'ReturnMessage': 'Perfil de licencia, por favor contacte a HelpDesk por medio de helpdesk.'
						}	
			return failCambioClave 
		else:
				
			return (711,'Error desconocido ldap.OPERATIONS_ERROR, por favor inicie un caso en helpdesk', error)
        except ldap.SERVER_DOWN:
		#return ldapAction, aunque salga bien la operacion de bind_s siempre retorna con ldap.SERVER_DOWN 
                respuestaTestClave = testClave( USER , NEWPASSWORD , LDAPSERVER )
		return respuestaTestClave
        else:
		failCambioClave = {
					'ReturnCode': 717,
					'ReturnError': None,
					'ReturnMessage':'No hay alernativa para el "try" en cambio de clave, por favor inicie un caso en helpdesk'
					}
                return failCambioClave 
