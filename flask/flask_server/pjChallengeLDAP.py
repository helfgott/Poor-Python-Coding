#!/usr/local/bin/python
'''
Contactando a LDAP
Las funciones de este modulo solo deben contener interaccion con LDAP
'''
from PJVariables import LDAPSERVER
import pjTestLDAP
import ldap, logging
import sys, os, subprocess 

#---------------------------------------------------------------------------------- [Autenticar al usuario en LDAP]
# Si hay un servidor disponible, entonces verificar al usuario

def conectarLDAP( USER, PASSWORD, USERTYPE, LDAPSERVER ):
    """
    Esta funcion recibe cuatro parametros
    """
    auth = '' 
    # Si el usuario es de tipo sucursal realizo la autenticacion para confirmar que el usuario esta operativo
    if USERTYPE == "notebook":
            try:

		    # Probamos si podemos establecer una conexion basica con LDAP
                    testLDAPServer = pjTestLDAP.testLDAPConex( LDAPSERVER )
		    logging.info('Return code para conexion basica de LDAP: {}'.format(testLDAPServer['ReturnCode'])) 

		    # Si la prueba fue exitosa, revisamos el ReturnCode y asignamos el objeto de LDAP a una variable
		    if testLDAPServer['ReturnCode'] % 2 == 0:
			ldapServer = testLDAPServer['ReturnValue']
		    else :
			logging.error(testLDAPServer['ReturnError'])
			return {
				'ReturnCode': int(309),
				'ReturnError': str(testLDAPServer['ReturnError']),
				'ReturnMessage': str('Ha ocurrido un error con el modulo pjTestLDAP en PJLOGINSERVER1, debe revisarse el server.')
				}		
		
		    # Con el objeto de LDAP podemos probar los datos proporcionados por el usuario
		    logging.info('Probando Login: {0:<10} {0:<10} {0:<10}'.format(USER, USERTYPE, LDAPSERVER))
                    auth = ldapServer.simple_bind_s('cn=%s,ou=people,c=arg,o=company' % USER ,'%s' % PASSWORD)
		    logging.info('310, Usuario Autenticado') 

                    auth= {
				'ReturnCode': int(310),
				'ReturnMessage': str('Usuario {} autenticado en LDAP correctamente.'.format(USER))
			  }
		 
		    # Cerramos la sesion de LDAP
                    testLDAPServer['ReturnValue'].unbind()
		    
		    # Conexion exitosa, regresa un diccionario al cliente PJLogin en la notebook
                    return auth 
	    
	    # En caso de autenticar pero LDAP nos dice que hay un error, evaluamos: 
            except ldap.INVALID_CREDENTIALS:
		   
		    # Obtenemos el codigo de error:
                    error=sys.exc_info()[1][0]['info'].split(" ")[0]
                    auth='No se pudo validar usuario'

                    if(error =='R004109'):
			    # Requiere cambio de clave
                            logging.warning("Clave vencida ejecutando pyCambio")
			    # PyCambio se inicia desde el cliente 
                            # este servidor es python2.7 con lo cual siempre devuelve bytes a las notebooks con python3
			    logging.warning('319, Se requiere cambio de clave para legajo: {}'.format(USER))
                            return {
					'ReturnCode': int(319),
					'ReturnError': str(error),
					'ReturnMessage': str('Clave vencida, ejecutando ChangePassword')
				   }
                    elif(error =='R004110'):
			    # Usuario Bloqueado
			    
			    logging.error('311, Legajo: {} Bloqueado'.format(USER))
			    return {
					'ReturnCode': int(311),
					'ReturnError': str(error),	
					'ReturnMessage': str('El legajo {} se encuentra bloqueado.'.format(USER))
			           }		
                    else:
			    # Usuario y clave incorrectos
			    logging.error('313: Usuario y/o clave incorrectos')
			    return  {
					'ReturnCode': int(313), 
					'ReturnError': str(error),
					'ReturnMessage': str('313, Usuario y/o clave incorrectos, error LDAP')				   
				     }
            except ldap.SERVER_DOWN :
		    # No se puede contactar el servidor LDAP, probablemente caido
		    return {
				'ReturnCode'  : int(317),
				'ReturnError' : str(ldap.SERVER_DOWN),
				'ReturnValue' : str('Imposible realizar consulta de ldap')
			   }  
	    except ldap.LDAPError as e:
		    auth="315,error desconocido"
		    logging.error('315: Error desconocido al contactar LDAP: {} '.format(e))
		    return {
				'ReturnCode' : int(315),
				'ReturnError': str(e),
				'ReturnValue': str('Error desconocido consultando a servidor LDAP') 	
			   }   
		   
    return auth 
