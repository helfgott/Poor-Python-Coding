#!/usr/bin/python
# This script handles POST Requests  
# -------------------- Este script es entregado por puppet (role_base)
# Documentacion: 

from ast import literal_eval
import requests
import logging

def httpPostRequest(ENDPOINT,PAYLOAD,TIMEOUT) :
        # mortiz - 28/10/2020 se agrega excepcion para Cod. HTTP
        try :
        
            jsonHeaders = {'Content-Type':'application/json'}
            postRequest = requests.post(ENDPOINT,headers=jsonHeaders,json=PAYLOAD,timeout=TIMEOUT )
            # Si el codigo de salida no es HTTP 200, regresamos el error: 
            if postRequest.status_code != 200 :
                return {
                        'ReturnCode': 1,
                        'ReturnError': postRequest.status_code,
                        'ReturnMessage': 'No ha sido posible realizar el POST Request, cod. salida HTTP: {}'.format(postRequest.status_code)
                        }
            else:
                # Caso contrario, regresamos el contenido del request en una variable, lo decodificamos de bytes y lo evaluamos
                # Estamos esperando un diccionario como respuesta del servidor
                postRequest = postRequest.content.decode()
                return postRequest

        # Cuando desde el equipo no llegamos al url del api
        except requests.exceptions.ConnectionError as errconn: 
            return {
                    'ReturnCode': 11,
                    'ReturnError': str(errconn),
                    'ReturnMessage': 'Error al conectarse con: {}'.format(ENDPOINT)
                    }
        except :
            logging.error('Un nuevo problema no previsible ha aparecido, reporte a mygroup')
            raise 
