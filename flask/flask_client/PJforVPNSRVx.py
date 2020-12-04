#!/usr/bin/env python3
import subprocess, logging, os
from PJVariables import VPNSERVERS

"""
El proposito de este modulo es:

Elegir SERVER1 o SERVER2 si:
        a) Se puede conectar al puerto 22 con netcat
"""
#--------------------------------------------------------------------------------------- DEFINIR SERVIDOR DE INGRESO
#                                                                                        Y AUTENTICACION 

# mortiz: Ya no debo validar el 389 porque la autenticacion va por HTTP via pjLogins

def validateVPNServers():
    notValid={
              'ReturnCode': 111,
              'ReturnError': [],
              'ReturnMessage':'puerto 22 inaccesible en servidores encontrados.'
             }
    goodServers=[]
    for vpnserver in VPNSERVERS:
        ncSSH = "nc -vz " + vpnserver + " 22 -w 5"
        reachVPNSRV = subprocess.Popen(ncSSH.split(), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        outputSRV, errorSRV = reachVPNSRV.communicate()
        # Si llegamos al 22 del servidor con codigo 0 se avanza
        if reachVPNSRV.returncode == 0 :
            logging.info('Servidor: {} es valido al puerto 22'.format(vpnserver))
            goodServers.append( vpnserver )        
        else :
            # si no llegamos al 22 del servidor lo ponemos en la lista negra
            logging.error('PJ CODIGO ERROR: 111, servidor no valido: {}, {}, {}'.format(vpnserver, outputSRV,errorSRV))
            notValid['ReturnError'].append(
                                             {
                                              'ReturnMessage':'puerto 22 inaccesible en {}: {} {}'.format(vpnserver,outputSRV,errorSRV)
                                             }
                                          )

    return notValid, goodServers
