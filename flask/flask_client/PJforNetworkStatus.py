#!/usr/local/bin/python

import re
import subprocess, netifaces
import logging

interfacesList = netifaces.interfaces()

#--------------------------------------------------------------------------------------- VERIFICAR DIRECCIONES IP 
#                                                                                        E INTERFACES

def verificarInterfaces() :
    # Listar interfaces disponibles
    availableInterfaces = str(netifaces.interfaces())
    logging.info("Interfaces disponibles: {}".format(availableInterfaces))
        
    # Lista para almacenar las interfaces con IP valida
    validInterfaces = []
    # Analizando que interfaces tienen familia de IP valida (AF_INET)
    for interface in interfacesList :
        if interface == 'lo' :
            logging.info('Ignorando interfaz local: {}'.format(interface))
            pass        
        else :
            logging.info('Evaluando interfaz : {}'.format(interface))
            try :
                thisInterface = netifaces.ifaddresses(interface)
                validIPInterface = thisInterface[netifaces.AF_INET][0]['addr']
                if validIPInterface :
                    logging.info('Interfaz valida: {}:{}'.format(interface, validIPInterface))
                    validInterfaces.append(interface)
                    logging.info('Agregando esta interfaz en la lista: {}'.format(interface))
                else:
                    logging.warning('Esta interfaz no sera tomada en cuenta: {}'.format(thisInterface['addr'][netifaces.AF_INET]))
            except KeyError:
                logging.warning("Interfaz no valida: {} ".format(interface))      
            continue
        
        # Mostar interfaces con IP valida
        logging.debug(" Interfaces con IP valida AF_INET: {}".format(validInterfaces))
        
    # Caso 1: Ninguna interfaz
    ethIP=None
    if len(validInterfaces) == 0 :
        noInterfaces = { 
                         'ReturnCode': 51,
                         'ReturnError':'No hay interfaces validas', 
                         'ReturnMessage':validInterfaces
                        }
        logging.error(noInterfaces)
        return noInterfaces
    if 'eth0' in validInterfaces :
        # extraemos informacion de la interfaz eth0
        ethIP = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']
        # comparamos la direccion ip obtenida
        if re.match (r'^76\.' , ethIP) :
            ethInterface = {
                                'ReturnCode': 60,
                                'ReturnValue': ethIP,
                                'ReturnMessage': 'Se detecta red de sucursales en interfaz eth0 con IP: {}'.format(ethIP)
                            }
            logging.info(ethInterface)
            return ethInterface 
        elif 'cscotun0' in validInterfaces:
            cscotunInterface = {
                                'ReturnCode': 62,
                                'ReturnValue': ethIP,
                                'ReturnMessage': 'Se detecta cscotun0 conectado: {}'.format(ethIP)
                                }
            logging.info(cscotunInterface)
            return cscotunInterface 
        else :
            ethInvalid = {
                            'ReturnCode': 61,
                            'ReturnError': ethIP,
                            'ReturnMessage': 'Red cableada no pertenece al banco, no se puede continuar, eth0 : {}'.format(ethIP)
                            }
            logging.info(ethInvalid)
            return ethInvalid 

    # Caso 3: WLAN
    if 'wlan0' in validInterfaces and not 'cscotun0' in validInterfaces :
        wlanIP = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
        wlanInterface = {
                            'ReturnCode': 71,
                            'ReturnError': 'DEBE CONECTARSE A LA VPN',
                            'ReturnMessage': 'Usuario conectado a WiFi pero no hay VPN.wlanIP: {} '.format(wlanIP)
                         }

        logging.debug(wlanInterface)
        return wlanInterface
        
    # Caso 4: WLAN 0 y CSCOTUN0
    if 'wlan0' in validInterfaces and 'cscotun0' in validInterfaces and len(validInterfaces) == 2 :
        wlanIP = netifaces.ifaddresses('wlan0')[netifaces.AF_INET][0]['addr']
        cscotunIP = netifaces.ifaddresses('cscotun0')[netifaces.AF_INET][0]['addr']
        wlanWithCsco = {
                        'ReturnCode': 80,
                        'ReturnValue': cscotunIP,
                        'ReturnMessage': 'Usuario conectado a Wifi y VPN Cisco, IP wlan: {}, IPCsco: {}'.format(wlanIP, cscotunIP)
                         }
        logging.debug(wlanWithCsco)
        return wlanWithCsco
        
def networkStatus():
    estadoInterfazRed = verificarInterfaces()
    if estadoInterfazRed['ReturnCode'] % 2 == 0 :
        logging.debug(estadoInterfazRed)
        return estadoInterfazRed
    else:
        logging.error(estadoInterfazRed)
        return estadoInterfazRed
