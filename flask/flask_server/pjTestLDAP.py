#!/usr/local/bin/python
# Este modulo se encarga de probar la conexion basica a ldap con una consulta al LDAPSERVER + 389

from PJVariables import LDAPSERVER
import sys, logging, ldap

#<<< mortiz: To enable hard debugging on ldap library: >>>
# ldap.set_option(ldap.OPT_DEBUG_LEVEL, 4095)

# mortiz: El puerto por defecto de la libreria ldap es 389, pero mejor lo pasamos explicito

#----------------------------------------------------------------------------------- [Identificar LDAP a usar]
def testLDAPConex( LDAPSERVER ) :
    """
    Realiza una consulta basica a un servidor LDAP, esto verifica que:
	a. Hay conectividad
	b. Hay funcionalidad
    """
    try:
	#<<< mortiz: to enable hard debugging on ldap library >>>
        #ldap_obj = ldap.initialize("ldap://%s:389" % LDAPSERVER ,trace_level=2)
	
	# Iniciamos la clase de LDAP, no se ha establecido la conexion.
        ldap_obj = ldap.initialize("ldap://{}:{}".format(LDAPSERVER, int(389)))
	# Timeout para las operaciones contra LDAP
	ldap_obj.set_option(ldap.OPT_TIMEOUT, 5)
	# Timeout para la conectividad contra LDAP
        ldap_obj.set_option(ldap.OPT_NETWORK_TIMEOUT, 5)
	# Version de protocolo, tambien se puede usar int(3) por ldap.VERSION3
       	ldap_obj.protocol_version = ldap.VERSION3

	# mortiz 28710/2020: Realizamos una busqueda simple, se puede usar search_st (synchronous with timeout) si en el futuro pasa algo.
        ldap_result_id = ldap_obj.search("ou=people,c=arg,o=company", ldap.SCOPE_SUBTREE, "cn=xXuserXx", None)
	
	# Resultado de la busqueda, debe traer un objeto ldap, hacemos unpacking con variables
       	result_type, result_data = ldap_obj.result(ldap_result_id, 0)
        
	# Tomamos el objeto en la variable ret_val, el objeto viaja en forma de dict() como 'ReturnValue' de esta funcion
	ret_val = ldap_obj
	logging.info("210: La consulta basica a LDAP se realizo exitosamente. ")
        response = {
		'ReturnCode':int(210),
		'ReturnValue': ret_val,
		'ReturnMessage': str('La consulta basica a LDAP se realizo exitosamente.')		
		}
	# Regresamos el dict() con el objeto si todo sale bien
	return response
    # En caso de errores, asignamos la variable "e" como el mensaje de error de LDAP y lo pasamos asi como venga.	
    except ldap.LDAPError, e : 
	logging.error("211: No puedo conectarme al servidor LDAP" + str(LDAPSERVER) + str(e) )
        response = {
		'ReturnCode': int(211),
		'ReturnError': str(e),
		'ReturnMessage': str('La consulta basica a LDAP ha FALLADO')
		}
	return response
