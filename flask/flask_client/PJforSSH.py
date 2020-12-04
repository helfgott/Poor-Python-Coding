#!/usr/local/bin

import paramiko, os, sys, logging
from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException
# Importamos variables necesarias para este modulo
from PJVariables import PRI_KEY, PRI_KEY_THE_TECH, PUB_KEY, PUB_KEY_THE_TECH, THE_TECH_SERVER, DEVICEINFORMATION, remoteCmdSSH, localCmdAuthorizedKeys,localCmdPrivateTHETECH, localCmdPrivateUserKey

"""
Este modulo se encarga de :

1) la generacion de llaves localmente
        1.1) genera llaves para los server sin passphrase
        1.2) genera llaves para otros server con passphrase (requerido)
2) la conexion a SSH usando paramiko y la copia de las llaves via SFTP
3) ejecutar comandos remotos por SSH

"""

def execute_remote_commands(sshConex,theCommand):
    """
    Basicamente esta funcion recibe como parametros un objeto de conexion ssh <obj> y un comando <str> a ejecutar.
    """
    try:
        ssh = sshConex
        # mortiz 2020/11/18
        # Hacemos unpack pero no se toca el stdin, por obvias razones
        # Que no haya nada en stdout depende del script / comando de destino
        # Para lo ejecutado a la fecha no hay salida estandar por lo cual no se registra error alguno
        logging.info('Preparados para ejecutar comando:{}'.format(theCommand))
        stdin, stdout, stderr = ssh.exec_command(theCommand)
        execErrors = []
        for i in stderr :
            execErrors.append(i)
        for i in stdout :
            execErrors.append(i)
        logging.info('PJ CODE: 244, El comando remoto se ejecuto')
        # salida para errores en la ejecucion de comandos remotos
        if execErrors:
            badRemoteCmd = {
                             'ReturnCode': 241,
                             'ReturnError': execErrors, 
                             'ReturnMessage': 'Problemas al ejecutar comando via SSH: {}'.format(remoteCmdSSH)
                            }
            logging.error(badRemoteCmd)
            return badRemoteCmd 
        else :
            remoteCompleted = {
                               'ReturnCode': 240,
                               'ReturnValue':None,
                               'ReturnMessage': 'Se ejecuto el comando remoto sin problemas: {}'.format(remoteCmdSSH)
                              }
            logging.info(remoteCompleted)
            return remoteCompleted

    # Salida para errores en la ejecucion de la libreria paramiko
    except Exception as SSHExec :
        errorInCommand = {
                              'ReturnCode': 243,
                              'ReturnError': str(SSHExec),
                              'ReturnMessage': 'Ocurrio un problema con paramiko y la conexion SSH para ejecutar el comando remoto.'
                        }
        logging.error(errorInCommand)
        return errorInCommand 

def create_ssh_keys( SERVER , usuario , password ):
    """
    La funcion se conecta por SSH utilizando la libreria de paramiko, establece conexiones SFTP y ejecuta comandos remotos en
    el servidor elegido VPNSRV{REC,VEN}
    """
    #__________________________________________________________________________________________Create SSH connection
    try :
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        logging.info('Estableciendo conexion SSH para: {} en {}'.format(usuario,SERVER))
        ssh.connect( SERVER , username=usuario, password=password)
        sshConnected = {
                        'ReturnCode': 220,
                        'ReturnValue': str(ssh.get_transport().is_active()),
                        'ReturnMessage': 'La conexion SSH se establecio correctamente'
                        }
        logging.info(sshConnected)

    except Exception as unknownException:
        sshNOTConnected = {
                        'ReturnCode': 221,
                        'ReturnError': str(unknownException),
                        'ReturnMessage': 'No fue posible establecer una conexion SSH, contacte a Soporte Tecnico.'
                        }
        logging.error(sshNOTConnected)
        return sshNOTConnected
    #_________________________________________________________________________________________ Create SFTP connection    
    try:
        logging.info('Inicio del tramo SFTP')
        sftp = ssh.open_sftp()
        sftpConnected = {
                        'ReturnCode': 230,
                        'ReturnValue': str(sftp.listdir(path='.')), 
                        'ReturnMessage': 'La conexion SFTP se establecio correctamente'
                        }
        logging.info(sftpConnected)
        #------------------------------------------------------------------------------- Enviar device.current
        logging.info('Enviamos por SFTP device.current al home remoto del usuario')
        sftp.put(DEVICEINFORMATION,'.device.current')
        #------------------------------------------------------------------------------- Creacion de llaves locales 
        privateUserKeys = localCmdPrivateUserKey[0] + usuario + localCmdPrivateUserKey [1]
        logging.debug('Ejecutando comando local:{}'.format(privateUserKeys))
        if os.system(privateUserKeys) == 0:
            logging.debug('El comando se ejecuto con exito: {}'.format(privateUserKeys))
            try :
                #--------------------------------------------------------------------------- Send private key
                dst_file = '.ssh/id_rsa'
                sftp.put(PRI_KEY, dst_file)
                sftp.chmod(dst_file,0o0600)
                #--------------------------------------------------------------------------- Send public key
                logging.info('Enviando llave publica')
                dst_file = '.ssh/id_rsa.pub'
                sftp.put(PUB_KEY, dst_file)
                sftp.chmod(dst_file, 0o0644)
                logging.info('PJ CODIGO: 294, Se copiaron las llaves pub/priv exitosamente via SFTP.')
            except Exception as SFTPError :
                SFTPErrorPut =  {
                                'ReturnCode': 295,
                                'ReturnError': str(SFTPError),
                                'ReturnMessage': 'Ha ocurrido un error enviando las llaves priv/pub del legajo via SFTP a su home'
                                }
                logging.error(SFTPErrorPut)
                return SFTPErrorPut
            #---------------------------------------------------------------------------- Borrar Keys
            # borra cualquier lave previa en authorized_keys
            # cat de id_rsa.pub >> authorized_keys
            logging.debug('Borrando llaves previas')
            authorizedKeys = localCmdAuthorizedKeys[0] + usuario + localCmdAuthorizedKeys[1]
            remoteAuthorized = execute_remote_commands(ssh,authorizedKeys)
            if not remoteAuthorized['ReturnCode'] % 2 == 0:
                return remoteAuthorized
            #_____________________________________________________________________________  Generate Private Keys THETECH
            localGenPrivateKeyTHETECH = localCmdPrivateTHETECH[0] + usuario + localCmdPrivateTHETECH[1]
            logging.info('Ejecutando comando local: {}'.format(localGenPrivateKeyTHETECH))            
            if os.system(localGenPrivateKeyTHETECH) == 0:
                logging.info('PJ CODIGO: 250, El comando local se ejecuto correctamente.')
                #------------------------------------------------------------------------ Send thetech private key
                try :
                    logging.info('Enviando llave privada de NoMachine')
                    dst_file = '.ssh/id_rsa_thetech'
                    sftp.put(PRI_KEY_THE_TECH, dst_file)
                    sftp.chmod(dst_file, 0o0644)
                    #-------------------------------------------------------------------- Send thetech public key
                    logging.info('Enviando llave publica de NoMachine')
                    dst_file = '.ssh/id_rsa_thetech.pub'
                    sftp.put(PUB_KEY_THE_TECH, dst_file)
                    sftp.chmod(dst_file, 0o0644)

                    # ----------------------------------------------------------------------------------- Ultimo paso--
                    # Borrar la config de thetech, regenerar directorios, convertir publica en authorized.crt
                    #--------------------------------------------------------------------------------------------------
                    logging.info('Borrando los directorios de thetech remotos y renombrar llave publica a authorized.crt')
                    lastStep = execute_remote_commands(ssh,remoteCmdSSH)
                    ssh.close()
                    return lastStep                                           
                except Exception as e:
                    return {
                            'ReturnCode': 271,
                            'ReturnError': str(e),
                            'ReturnMessage': 'Tuvimos problemas enviando las llaves pub/priv de THETECH via SFTP'
                            }

            else:
                # problemas comando local 2 
                return  {
                          'ReturnCode': 251,
                          'ReturnError': 'Problemas ejecutando local:{}'.format(localGenPrivateKeyTHETECH), 
                          'ReturnMessage': 'Problemas al ejecutar el comando local para llaves PrivateTHETECH'
                        }
        else:
            #problemas comando local 1
            return {
                       'ReturnCode': 261,
                       'ReturnError': 'Problemas ejecutando local: {}'.format(privateUserKeys), 
                       'ReturnMessage': 'Problemas al ejecutar el comando local para llaves puv/priv del usuario'
                     }

    except Exception as unknownException:
       return  {
                'ReturnCode': 231,
                'ReturnError': str(unknownException),
                'ReturnMessage': 'Problemas al copiar archivos via SFTP: {}'.format(unknownException)
                }
