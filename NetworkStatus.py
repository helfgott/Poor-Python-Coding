#!/usr/local/bin/python
# mortiz: usando netifaces para ver estado de interfaces

import re
import subprocess, netifaces
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.DEBUG)

interfacesList = netifaces.interfaces()

#--------------------------------------------------------------------------------------- VERIFICAR DIRECCIONES IP 
#											 E INTERFACES

# Listar interfaces disponibles
availableInterfaces = str(netifaces.interfaces())
logging.debug( "Project: Interfaces disponibles : " + availableInterfaces)

# Lista para almacenar las interfaces con IP valida
validInterfaces = []

# Analizando que interfaces tienen familia de IP valida (AF_INET)
for interface in interfacesList :
	if interface == 'lo' :
		logging.debug('Project: Ignorando interfaz local: ' + interface)
		pass	
	else :
		logging.debug('Project: Evaluando interfaz : ' + interface)
		try :
			thisInterface = netifaces.ifaddresses(interface)
			validInterfaces.append(interface)
		except KeyError:
		        logging.debug("Project: Interfaz no valida: " + str(interface))	
			continue

# Mostar interfaces con IP valida
logging.debug("Project: Interfaces con IP valida AF_INET: " + str(validInterfaces))

# Caso 1: Ninguna interfaz
if len(validInterfaces) == 0 :
	logging.error('Project: El equipo no esta conectado a ninguna red')
	# bye bye

# Caso 2: ETH0
if 'eth0' in validInterfaces :
	# extraemos informacion de la interfaz eth0
	addrEth0 = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
	
	# comparamos la direccion ip obtenida
	if re.match (r'^172\.' , addrEth0) :
		logging.debug('Project: Se detecta red de oficina en interfaz: eth0')
		# netcat bip bop bup
	else : 
		logging.debug('Project: Red cableada no valida en interfaz: eth0')

# Caso 3: WLAN
if 'wlan0' in validInterfaces and not 'cscotun0' in validInterfaces :
	logging.debug('Project: Usuario conectado a WiFi pero no hay VPN: wlan0 no cscotun0')

# Caso 4: WLAN 0 y CSCOTUN0
if 'wlan0' in validInterfaces and 'cscotun0' in validInterfaces and len(validInterfaces) == 2 :
	logging.debug('Project: Usuario conectado a VPN BRAND: wlan0 y cscontun0 unicamente.')	

# Caso 5: ETH0, WLAN0, CSCOTUN0 (Don full conectividad)
if 'wlan0' in validInterfaces and 'cscotun0' in validInterfaces and 'eth0' in validInterfaces and len(validInterfaces) == 3 :
	logging.debug('Project: Cable de Red, WiFi y VPN levantados, prioridad para eth0 : eth0, wlan0, cscotun0')

