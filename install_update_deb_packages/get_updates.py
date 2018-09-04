#!/usr/bin/python
# miguel.ortiz
# This script update and install custom deb packages and it requires:
#   - file "availables in webserver with the output of md5sum"
#   - file "package.deb"
#   - file "package.ver" (a text file with the version of the deb package) 
#                       my main server was SuSe and I cound't verify the version using dpkg :(

import urllib2, subprocess, time 
import logging, sys, os

logging.basicConfig(filename="updates.log", level=logging.DEBUG)

remote_sources = [ 	'http://<SERVER>:<PORT>' ]
# paths		    
rootDir = '/srv/updateNotebooks/'

# required data structures
remote_packages_md5 = {}
remote_packages_version = {}
installed_packages = {}
not_installed_packages = []

# TODO - Validar que todos los archivos existen en origen y tienen informacion

def get_remote_packages() :
	""" 	Del servidor elegido trae :
	1) Nombre de los paquetes disponibles 
	2) MD5SUM de cada paquete
	3) Version de cada paquete
	"""
 	logging.info( '...................................................... getting remote packages .... \n') # add formato logger
	time.sleep(3)
	try : 
		Pack = urllib2.urlopen( remote_sources[0] + "/updatesNotebooks/availables")
		PackResponse = Pack.read()
		PackResponse = PackResponse.split('\n')
	except urllib2.HTTPError, error :
		logging.error(error, remote_sources[0] + "/updatesNotebooks/availables", 'not found')
		
	for package in PackResponse :
		if ".deb" in package :
			# get packages
			package=package.split()
			package_name = package[1].replace('.deb','')
		        remote_packages_md5.update({package_name : package[0]})	
			
			# get versions
			try :
			 	PackVersion = urllib2.urlopen( remote_sources[0] + \
								"/updatesNotebooks/" + \
								 package_name + \
								'.ver')
			except urllib2.HTTPError, error:
				logging.error(error, remote_sources[0], '/updatesNotebooks/', package_name + '.ver')
				
			PackVersion = PackVersion.read()
		        remote_packages_version.update({package_name : PackVersion.replace('\n','')})
	logging.info('This remote packages were found: \n  %s \n ' ,remote_packages_version)
			
def get_local_packages() :
	"""Compara los paquetes disponibles en remote_packages_md5 (generado por get_remote_packages)
	y busca si estan instalados en el equipo local.
	1) Genera Diccionario de los que estan instalados paquete:version
	2) Genera Lista de los "no instalados" 
	"""
	logging.info('...................................................  getting local packages .... \n') # add formato logger
	for package_name, md5sum in remote_packages_md5.iteritems():
		try:
			installed_package = subprocess.check_output([ \
				'dpkg -s ' + package_name \
				 + '| grep Version'], \
				shell=True, \
				stderr=subprocess.STDOUT)
		
			installed_package = installed_package.split()
			installed_packages.update({package_name : installed_package[1]})
			time.sleep(3)
			logging.info( package_name + ' ' + installed_package[1] + ' This remote package is INSTALLED locally') 
		except :
			time.sleep(3)
			logging.info(package_name + ' <-- This remote package is NOT INSTALLED locally')
			not_installed_packages.append(package_name)	
	if not installed_packages :
		logging.info('None of the remote packages are installed locally \n')

def process_packages() :
	""" Ya que tenemos la informacion remota y local procesamos los datos
	para definir que se descarga e instala y que no. Reglas:
	1) Si el paquete no existe localmente, descarga e instala
	2) Si el paquete existe localmente compara version local y remota
		2.1) Si la version local es menor a la remota, descarga e instala
		2.2) Si la version local y remota son iguales no hacer nada
	3) Solo se tienen en cuenta los paquetes disponibles remotamente. No hace nada con los locales
	   que no tengan homonimo en el remoto.
	"""
	#TODO: Falta comparacion de MD5
	# comparar instalados contra remotos
	for package, version in installed_packages.iteritems():
		# paquetes instalados de la misma version que los remotos
		if installed_packages[package] == remote_packages_version[package] :
			logging.info('local ' + package + ': ' + installed_packages[package] +\
			 ' Same as remote_version: ' + remote_packages_version[package] + ' not updating')
		# actualizacion de paquetes instalados
		elif installed_packages[package] < remote_packages_version[package] :
			logging.info('updating: ' + package + ' - ' + installed_packages[package] + ' to ' + remote_packages_version[package])
			try:
				download_new_version = subprocess.check_output([ \
				'wget -qN ' + remote_sources[0] \
				 + '/updatesNotebooks/' + package + '.deb'], \
				shell=True, \
				stderr=subprocess.STDOUT)
			except subprocess.CalledProcessError, error :
				logging.info('The file %s listed in "availables" on the remote server doesn\'t exist, error: %s \n', package, error )
				# delete unavailable files from local list to avoid install trying

			try:
 				if os.path.isfile(rootDir + package + '.deb') : 
					if md5sum_local_validation(package) :
						download_new_version = subprocess.check_output([ \
									'dpkg -i ' + package + '.deb'], \
									shell=True, \
									stderr=subprocess.STDOUT)
				else :
					logging.error('the package %s wasn\'t downloaded to be installed, check previous errors \n', package)

			except subprocess.CalledProcessError, error :
				logging.error('Failed updating package %s with error: %s ' , package,error)
		elif installed_packages[package] > remote_packages_version[package] :	
			logging.warning('This is weird, version of: ' + package + ' on remote file "availables" is older than the local one')
	for notInstalled in not_installed_packages :
		try:
			download_abscent = subprocess.check_output([ \
				'wget -qN ' + remote_sources[0] \
				 + '/updatesNotebooks/' + notInstalled + '.deb'], \
				shell=True, \
				stderr=subprocess.STDOUT)
		except subprocess.CalledProcessError, error :
			logging.error('the file %s listed in "availables" on the remote server doesn\'t exist, error: %s \n', notInstalled, error )
		try :
			if os.path.isfile(rootDir + notInstalled + '.deb') : 
				if md5sum_local_validation(notInstalled) :
					logging.info( 'Installing: ' + notInstalled + '-' + remote_packages_version[notInstalled])
					install_abscent = subprocess.check_output([ \
							'dpkg -i ' + notInstalled + '.deb'], \
							shell=True, \
							stderr=subprocess.STDOUT)
			else :
				logging.error('the package %s wasn\'t downloaded to be installed, check previous errors \n', notInstalled)
		except subprocess.CalledProcessError, error :
			logging.error('MD5SUM process failed or you have a corrupt package: \n unable to install downloaded package: %s \n', error)

def md5sum_local_validation(package) :
	"""
	Verifica el MD5SUM del paquete local y remoto
	- validar la existencia del archivo antes de llamar esta funcion
	"""
        check_md5sum_dl_package = subprocess.check_output([ \
	                         'md5sum ' + package + '.deb | awk \'{print $1}\' '], \
       	                   shell=True, \
               	           stderr=subprocess.STDOUT)
        md5_downloaded_package = check_md5sum_dl_package.split() # elimina el salto de linea de la salida de md5sum
        md5_downloaded_package = md5_downloaded_package[0]       #  

        if str(remote_packages_md5[package]) == str(md5_downloaded_package) :
       		logging.info('local package %s and its remote namesake have equal md5', package)
       		return True			
        else:	
       		logging.error('different md5values for: %s package on remote and local', package)
       		logging.error(remote_packages_md5[package], check_md5_downloaded_package)
       		return False

# remove downloaded packages after install
def delete_downloaded_packages() :
	"""
	Los paquetes descargados e instalados ya no son requeridos
	"""
	getrootDir = os.listdir(rootDir)
	for item in getrootDir:
	    if item.endswith(".deb"):
		logging.info('deleting: %s, %s', rootDir, item)
        	os.remove(os.path.join(rootDir, item))

get_remote_packages()
get_local_packages()
process_packages()
delete_downloaded_packages()

