#!/usr/bin/env python3
"""
Encripta una contrasena en texto plano a base 64
"""
import base64, logging, os

# mortiz 8/05/2020: En python3 es necesario pasar bytes y codifcacion para la encriptacion, agrego encode y decode
def encriptarClave(password):
        logging.info('<<        Comienza modulo PJforEncriptarClave        >> ')
        base64clave = base64.b64encode(bytes(password, 'utf-8'))
        logging.debug('Se ejecuto la funcion de encriptar contrasena del usuario')
        return base64clave.decode('utf-8')

def encriptarClaveLegacyTech(clave):
    passEnc=os.popen("perl codPass.prl {}".format(clave)).read().split('\n')[1]
    return passEnc

