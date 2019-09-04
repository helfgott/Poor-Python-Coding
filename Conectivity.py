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
"""
#--------------------------------------------------------------------------------------- DEFINIR SERVIDOR DE INGRESO
#											 Y AUTENTICACION 

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

VPNSERVERS = ['VPNSERVERA', 'VPNSERVERB']
invalidServers=[]
validServer=[]
DEVNULL = open(os.devnull,'w')

def whichVPNServer():
	for vpnserver in VPNSERVERS:
		ncSSH = "nc -vz " + vpnserver + " 22 -w 5"
		ncLDAP = "nc -vz " + vpnserver + " 389 -w 5"
		reachVPNSRV = subprocess.Popen(ncSSH.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		outputSRV, errorSRV = reachVPNSRV.communicate()
		# Si llegamos al 22 del servidor con codigo 0 se avanza
		if reachVPNSRV.returncode == 0 :
			reachVPNLDAP = subprocess.Popen(ncSSH.split(), stdout=DEVNULL, stderr=subprocess.STDOUT)
			outputLDAP, errorLDAP = reachVPNLDAP.communicate()
			# Si llegamos al 389 del servidor con codigo 0 se avanza
			if reachVPNLDAP.returncode == 0 :
				logging.debug('Proyecto: Llego al puerto 22 en: ' + vpnserver)
				logging.debug('Proyecto: Llego al puerto 389 en: ' + vpnserver)
			        validServer.append( (vpnserver, '22', '389') )	
			else :
				# Si no llegamos al 389 del servidor lo ponemos en la lista negra
				invalidServers.append( (vpnserver,outputLDAP,errorLDAP, 'No se pudo llegar al host al puerto 389')  )
		else :	
			# si no llegamos al 22 del servidor lo ponemos en la lista negra
			logging.warning('Proyecto: DNS - no puedo resolver el hostname: ' + vpnserver)
			invalidServers.append( (vpnserver,outputSRV,errorSRV,'No se pudo llegar al host al puerto 22') )

selectedServers = whichVPNServer()

print "invalidos:", invalidServers
print "validos:", validServer

 
