#!/usr/bin/python
# -------------------- Este script es entregado por puppet (role_base)
# Documentacion: 

import subprocess, socket
from datetime import datetime
today = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

def transformar_data_to_json():
	"""
	El objetivo de esta funcion es transformar los datos obtenidos por gsdGetRCinServer.sh a formato JSON
	de ese modo se pueden insertar en mongo 
	"""
	# La lista de releases regresa como un <str>
	deployedReleases = subprocess.check_output(["/usr/bin/bash","/usr/local/bin/gsdGetRCinServer.sh"])
	timeZoneInfo     = subprocess.check_output(["date","+%Z"]).strip()

	# Separamos el <str> por lineas
	deployedReleases = deployedReleases.split()

	# Generamos diccionario inicial
	hostname = (socket.gethostname())
        communicate = { 'server' : hostname,
                        'date': today,
                        'timezone': timeZoneInfo, 
                        'applications': {} 
                      }

	# Parseamos todos los despliegues encontrados
	for release in deployedReleases:

		# sanetizar los datos, debemos eliminar los "." dado que son representaciones especiales en mongo, el path tampoco nos importa porque es estandar
		release = release.replace('/opt/company/deploy/', '')
		release = release.replace('.', '-')

		# Verificamos si es un symlink (current es version actual desplegada)
		if 'current' in release :
			marker, appAndVersion = release.split('|')
                        if appAndVersion.count('/') > 1 :
                                rcversion = 'RC Format is wrong'
                                appname = marker.replace('/current', '')
                        else:
                                appname, rcversion = appAndVersion.split('/')

			if appname not in communicate['applications'] :
				communicate['applications'].update( { 
								appname: 
									{rcversion : 'current'} 
							     } )
			else:
				communicate['applications'][appname].update({rcversion : 'current'})

		# Verificamos si es un symlink (rollback es la version previa a current)
		elif 'rollback' in release:
			marker, appAndVersion = release.split('|')
                        if appAndVersion.count('/') > 1 :
                                rcversion = 'RC Format is wrong'
                                appname = marker.replace('/rollback', '')
                        else:
                                appname, rcversion = appAndVersion.split('/')

			if appname not in communicate['applications'] :
				communicate['applications'].update( { 
								appname: 
									{rcversion : 'rollback'} 
							     } )
			else:
				communicate['applications'][appname].update({rcversion : 'rollback'})

		# Lo que no es current o rollback es un despliegue mas viejo
		else :
                        appname, rcversion = release.split('/')
                        if appname not in communicate['applications'] :
                                communicate['applications'].update( {
                                                                appname:
                                                                        {rcversion : 'previous'}
                                                             } )
                        else:
                                if rcversion not in communicate['applications'][appname] :
                                        communicate['applications'][appname].update({rcversion : 'previous'})
                                else :
                                        # La version ya fue registrada como current o rollback, esto sucede porque el symlink comparte el mismo nombre que el directorio real a nivel dict
                                        pass

	return communicate
