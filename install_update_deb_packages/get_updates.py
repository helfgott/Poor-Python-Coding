#!/usr/bin/python
# miguel.ortiz
# updates notebooks

import urllib2, subprocess, time 
import logging, sys, os, glob

#-----------------------------------------------------------------------------------------  Required Variables

remote_sources = [ 	'http://host:port', \
			'http://host:port', \
		]
logPath= '/tmp/updatesNotebooks.log'
rootDir = '/srv/updatesNotebooks/'

#----------------------------------------------------------------------------------------    Logging
# Define the output of the log if you're experiencing issues
# Possible values: <DEBUG, INFO, WARNING, ERROR, CRITICAL>
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', \
				filename=logPath, level=logging.DEBUG)

#---------------------------------------------------------------------------------------     Required data structures

remote_packages_md5 = {}
remote_packages_version = {}
installed_packages = {}
not_installed_packages = []

# FIXME - Validar que todos los archivos existen en origen y tienen informacion
# FIXME - Validar que un paquete a instalar <control> se llama igual que su nombre .deb

def verify_servers() :
	"""
	Verifica la disponibilidad de los servidores
	"""
	count = 0
	while count < 2 :
		for server in remote_sources :
			try:
	        		Pack = urllib2.urlopen( server + "/updatesNotebooks/availables", timeout=3 )
 	       			PackResponse = Pack.read()
				count +=1
				logging.info('server available: %s', server)
			except urllib2.HTTPError, error :
				logging.error('Failed retreving the file "availables" from %s with error: %s', server, error)
				remote_sources.remove(server)
				count +=1
			except urllib2.URLError, error:
				logging.error('Failed to reach server %s', server )
				remote_sources.remove(server)
				count+=1

def get_remote_packages() :
	""" 	Del servidor elegido trae :
	1) Nombre de los paquetes disponibles (archivo "availables") 
	2) MD5SUM de cada paquete (archivo "availables")
	3) Version de cada paquete (archivos .ver)
	"""
 	logging.info( '...................................................... getting remote packages .... \n') 
	time.sleep(3)
	PackVersion=None
	try : 
		Pack = urllib2.urlopen( remote_sources[0] + "/updatesNotebooks/availables")
		PackResponse = Pack.read()
		PackResponse = PackResponse.split('\n')
		logging.info('Reading the file "availables" in the remote server')
	except urllib2.HTTPError, error :
		logging.error(error, remote_sources[0] + "/updatesNotebooks/availables", 'not found')
	  	sys.exit()	
	for package in PackResponse :
		if ".deb" in package :
			# get packages
			package=package.split()
			package_name = package[1].replace('.deb','')
		        remote_packages_md5.update({package_name : package[0]})	
			logging.info('processing packages of "availables" file into a dict')
			# get versions
			try :
			 	PackVersion = urllib2.urlopen( remote_sources[0] + \
								"/updatesNotebooks/" + \
								 package_name + \
								'.ver')
				logging.info('success downloading version file: %s.ver', package_name)
			except urllib2.HTTPError, error:
				logging.error('unable to find version file %s.ver, %s, package not elegible to be installed',\
						 package_name, error)	
				del remote_packages_md5[package_name]	
				continue
			if PackVersion == None :		
				logging.error('%s %s/updatesNotebooks/%s.ver ',error, remote_sources[0], package_name)
			else :
				PackVersion = PackVersion.read()
			        remote_packages_version.update({package_name : PackVersion.replace('\n','')})
	if not remote_packages_version :
		logging.error('unable to verify remote package .ver files, check log for errors')
		sys.exit()
	else :	
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

def download_packages() :
	""" Ya que tenemos la informacion remota y local procesamos los datos
	para definir que se descarga e instala y que no. Reglas:
	1) Si el paquete no existe localmente, descarga 
	2) Si el paquete existe localmente compara version local y remota
		2.1) Si la version local es menor a la remota, descarga
		2.2) Si la version local y remota son iguales no descarga
	3) Solo se tienen en cuenta los paquetes disponibles remotamente. No hace nada con los locales
	   que no tengan homonimo en el remoto.
        REQUERIDO: Verificar que sudoers tenga la regla para ejecutar dpkg como xxxxuser
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
				'wget -qN -P /srv/updatesNotebooks/ ' + remote_sources[0] \
				 + '/updatesNotebooks/' + package + '.deb'], \
				shell=True, \
				stderr=subprocess.STDOUT)
			except subprocess.CalledProcessError, error :
				logging.info('The file %s listed in "availables" do not match its ".deb" name, \
						error: %s \n', package, error )
				# delete unavailable files from local list to avoid install trying

		elif installed_packages[package] > remote_packages_version[package] :	
			logging.warning('This is weird, version of: ' + package + ' on remote file "availables"\
					 is older than the local one')
	for notInstalled in not_installed_packages :
		try:
			download_abscent = subprocess.check_output([ \
				'wget -qN -P /srv/updatesNotebooks/ ' + remote_sources[0] \
				 + '/updatesNotebooks/' + notInstalled + '.deb'], \
				shell=True, \
				stderr=subprocess.STDOUT)
			logging.info('\n Downloaded: %s.deb \n', notInstalled)
		except subprocess.CalledProcessError, error :
			# TODO FIXME error 3 y 8
			logging.error('Unable to retrieve %s listed in "availables",\
			 error: %s , %s \n', notInstalled, error.returncode, error.output )
	logging.info('End of processing process')

def install_packages():
	"""
	Realiza la instalacion de paquetes - usa dependencias descargadas localmente
	"""
	os.chdir(rootDir)
	for package in glob.glob("*.deb"):		
		try:
 			if os.path.isfile(rootDir + package) :
				if md5sum_local_validation(package[:-4]) :
					install = subprocess.check_output([ \
								'sudo dpkg -i ' + package ], \
								shell=True, \
								stderr=subprocess.STDOUT)
				else :
					logging.error('Unable to process MD5 for %s', package)
			else :
				logging.error('Unable to Install:  %s to be installed, check previous errors \n', package)

		except subprocess.CalledProcessError, error :
			logging.error('Failed updating package %s with error: %s ' , package,error)

	logging.info('End of installing process')

def md5sum_local_validation(package) :
	"""
	Verifica el MD5SUM del paquete local y remoto
	- validar la existencia del archivo antes de llamar esta funcion
	"""
	try :
		logging.info('Verifying md5 on local package %s', package)
	        check_md5sum_dl_package = subprocess.check_output([ \
	                         'md5sum '+ rootDir + package + '.deb | awk \'{print $1}\' '], \
       		                   shell=True, \
               		           stderr=subprocess.STDOUT)
	        md5_downloaded_package = check_md5sum_dl_package.split() # elimina el salto de linea de la salida de md5sum
        	md5_downloaded_package = md5_downloaded_package[0]       #
		logging.info('Local package %s has md5: %s', package, md5_downloaded_package)  
	except :
		logging.error('unable to execute md5sum for file: %s.deb', package)
        	check_md5_downloaded_package=None

	if str(remote_packages_md5[package]) == str(md5_downloaded_package) :
       		logging.info('local package %s and its remote namesake have equal md5', package)
       		return True			
        else:	
       		logging.error('different md5values for remote and local package, \
				check previous errors related to: %s, \n value-remote: %s, value-local: %s',\
						 package, \
						 remote_packages_md5[package], \
						 md5_downloaded_package
						 )
		
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

# verificamos si hay servidores
logging.info('verifying available servers')
verify_servers()
logging.info('finished verifying available servers')

if not remote_sources :
	logging.error('No servers available')
else :
	
	get_remote_packages()
	get_local_packages()
	download_packages()
	install_packages()
	delete_downloaded_packages()

