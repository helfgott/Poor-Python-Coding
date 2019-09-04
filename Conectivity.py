#!/usr/local/bin/python
import subprocess, logging, os

"""
El proposito de este modulo es:

Elegir VPNSERVERA o VPNSERVERB si:
	a) Se puede conectar al puerto 22 con netcat
	b) Se puede conectar al puerto 389 con netcat
	c) !FIXME: Puede validar una consulta logica a LDAP
	Si se cumplen a,b,c entonces elige el primer servidor de la lista, en este caso VPNSERVERA
	Si falla alguno de a,b,c entonces prueba con el segundo servidor de la lista, en este caso VPNSERVERB
        Finalmente si probamos que funciona todo generar un daemon para monitorizar la llegada y registrar las continuas caidas de red,
        de este modo obtener estadisticas y clavarlas en le rostro de los que proveen la conectividad.

"""

#--------------------------------------------------------------------------------------- DEFINIR SERVIDOR DE INGRESO
#											 Y AUTENTICACION 

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)


VPNSERVERS = ['VPNSERVERB', 'VPNSERVERB']
invalidServers=[]
validServer=[]

def whichVPNServer():
	for vpnserver in VPNSERVERS:
		ncSSH = "nc -vz " + vpnserver + " 22 -w 5"
		ncLDAP = "nc -vz " + vpnserver + " 389 -w 5"
		reachVPNSRV = subprocess.Popen(ncSSH.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		outputSRV, errorSRV = reachVPNSRV.communicate()
		print reachVPNSRV.returncode	

		if not reachVPNSRV.returncode == 0 :
			# Verificar si se llega al puerto de SSH
			logging.warning('Proyecto: DNS - no puedo resolver el hostname: ' + vpnserver)
			invalidServers.append( (vpnserver,outputSRV,errorSRV,'No se pudo llegar al host al puerto 22') )
		else :
			# Verififcar si se llega al puerto de LDAP
			reachVPNLDAP = subprocess.Popen(ncSSH.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			outputLDAP, errorLDAP = reachVPNLDAP.communicate()
			invalidServers.append( (vpnserver,outputLDAP,errorLDAP, 'No se pudo llegar al host al puerto 389')  )
			# valida si llega a 22 y 389 de un servidor, de ser asi lo usa
			# NTH: validacion logica de LDAP
			if reachVPNLDAP.returncode == 0 :
				logging.debug('Proyecto: Llego al puerto 22 en: ' + vpnserver)
				logging.debug('Proyecto: Llego al puerto 389 en: ' + vpnserver)
			        validServer.append( (vpnserver, '22', '389') )	
			else :
				invalidServers.append( (vpnserver,outputLDAP,'No llego a LDAP') )
		
selectedServers = whichVPNServer()

print "invalidos:", invalidServers
print "validos:", validServer 


