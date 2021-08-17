#!/bin/bash
# script para buscar releases en path estandar devops - mortiz 15/06/2021
# -------------------- Este script es entregado por puppet (role_base)
# Documentacion: 

# declaramos los array que vamos a usar
declare -a despliegues
declare -a releases
declare -a releases_symlinks
declare -a releases_final

# listamos los despliegues disponibles en el path estandar 
despliegues=( $(ls -d /opt/company/deploy/* |grep "build\|distro") ) 

# array vacio para guardar las posibles releases encontradas 
releases=()
releases_final=()

# recorremos el <array> despliegues para ver cuales se encontraron
# y los agregamos en releases
for deploy in ${despliegues[@]}; do releases+=( $(ls -d $deploy/* | grep -v "^-" ) ) ; done

# detectamos los releases, si son symlinks de current y rollback los detectamos, modificamos y agregamos a releases_final
# si son directorios comunes van al array de releases_final directamente
for deploy in ${releases[@]}
	do
		if [[ "$deploy" =~ 'current' ]] || [[ "$deploy" =~ 'rollback' ]]; then
#			onesymlink= 
			releases_final+=($(ls -la $deploy | awk '{print $9"|"$11}'))
		else
			: # echo $deploy 
			releases_final+=" $deploy "
		fi
	done

# finalmente, listamos nuestros resultados
for deploy in ${releases_final[@]}; do echo $deploy ; done

